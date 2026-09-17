import json
import tempfile
import unittest
from pathlib import Path

from usage import SessionUsage, estimate_usd, select_thread, quota_window


def event(total, last=None):
    return {"type": "event_msg", "timestamp": "2026-09-16T12:00:00Z", "payload": {
        "type": "token_count", "info": {"total_token_usage": total,
        "last_token_usage": last or total, "model_context_window": 258400}}}


class UsageTests(unittest.TestCase):
    def test_cached_and_reasoning_not_double_counted(self):
        tokens = dict(input_tokens=1000, cached_input_tokens=800,
                      output_tokens=100, reasoning_output_tokens=80)
        self.assertAlmostEqual(estimate_usd(tokens, "gpt-6-astra"), .0078)
        self.assertAlmostEqual(estimate_usd(tokens, "gpt-6-astra", "priority"), .0156)
        self.assertIsNone(estimate_usd(tokens, "unknown-model"))

    def test_long_context_and_cache_writes(self):
        tokens = dict(input_tokens=300000, cached_input_tokens=100000,
                      cache_write_input_tokens=50000, output_tokens=1000)
        self.assertAlmostEqual(estimate_usd(tokens, "gpt-6-astra"), 4.525)

    def test_incremental_dedup_partial_lines_and_model_switch(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "rollout.jsonl"
            a = dict(input_tokens=1000, cached_input_tokens=800, output_tokens=100, total_tokens=1100)
            b = dict(input_tokens=2000, cached_input_tokens=1600, output_tokens=200, total_tokens=2200)
            ctx = {"type": "turn_context", "payload": {"model": "gpt-6-astra", "effort": "high"}}
            p.write_text(json.dumps(ctx)+"\n"+json.dumps(event(a))+"\n"+json.dumps(event(a))+"\n", encoding="utf-8")
            s = SessionUsage(p)
            s.refresh()
            self.assertEqual(s.total['total_tokens'], 1100)
            self.assertAlmostEqual(s.usd, .0078)
            with p.open('ab') as f:
                f.write((json.dumps({"type": "turn_context", "payload": {"model": "gpt-5.6-sol"}})+'\n').encode())
                line = json.dumps(event(b, a)).encode()
                f.write(line[:40])
            s.refresh()
            self.assertEqual(s.total['total_tokens'], 1100)
            with p.open('ab') as f: f.write(line[40:]+b'\n')
            s.refresh()
            self.assertEqual(s.total['total_tokens'], 2200)
            self.assertAlmostEqual(s.usd, .01092)
            s.refresh()
            self.assertAlmostEqual(s.usd, .01092)

    def test_active_title_beats_latest_writer_and_stale_route(self):
        rows = [dict(id='new', name='Widget', title='', cwd='B'),
                dict(id='old', name='3D website', title='', cwd='A')]
        row, mode = select_thread(rows, '3D website', '')
        self.assertEqual(row['id'], 'old')
        self.assertEqual(mode, 'follow')
        self.assertEqual(select_thread(rows, '', 'old')[0]['id'], 'old')
        self.assertEqual(select_thread(rows, '', '')[1], 'recent')
        self.assertEqual(select_thread(rows, '', 'deleted'), (None, 'missing'))

    def test_limits_use_duration_not_primary_slot(self):
        limits = {'primary': {'usedPercent': 40, 'windowDurationMins': 10080, 'resetsAt': 200},
                  'secondary': {'usedPercent': 70, 'windowDurationMins': 300, 'resetsAt': 200}}
        self.assertEqual(quota_window(limits, 300, now=100)['remaining'], 30)
        self.assertTrue(quota_window(limits, 300, now=201)['expired'])
        self.assertIsNone(quota_window(limits, 123, now=100))


if __name__ == '__main__': unittest.main()
