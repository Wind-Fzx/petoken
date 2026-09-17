import unittest
from datetime import date, timezone
from pathlib import Path
from analytics import normalize_usage, derive, aggregate, history_ranges
from usage import SessionUsage


class AnalyticsTests(unittest.TestCase):
    def test_subsets_unknowns_and_official_total(self):
        raw = {'input_tokens':100,'input_tokens_details':{'cached_tokens':80},
               'output_tokens':20,'output_tokens_details':{'reasoning_tokens':12},'total_tokens':121}
        t = normalize_usage(raw)
        d = derive(t)
        self.assertEqual(t['total_tokens'],121)
        self.assertIsNone(t['cache_write_input_tokens'])
        self.assertEqual(d['uncached_input_tokens'],20)
        self.assertEqual(d['non_reasoning_output_tokens'],8)
        self.assertEqual(d['new_work'],40)
        self.assertEqual(d['cache_hit_ratio'],80)
        self.assertEqual(d['reasoning_ratio'],60)
        self.assertIsNone(d['claude_raw'])
        self.assertEqual(d['known_processed'],120)
        t['cache_write_input_tokens']=5
        self.assertEqual(derive(t)['claude_raw'],120)  # writes are an input subset, not extra input
        self.assertEqual(derive(t)['comparison_uncached'],15)

    def test_missing_is_not_zero_and_malformed_is_unknown(self):
        t = normalize_usage({'input_tokens':100,'output_tokens':20,'cached_input_tokens':None,
                             'reasoning_output_tokens':-1,'cache_write_input_tokens':'bad'})
        self.assertEqual(t['total_tokens'],120)
        for k in ('cached_input_tokens','reasoning_output_tokens','cache_write_input_tokens'):
            self.assertIsNone(t[k])
        self.assertIsNone(derive(t)['new_work'])
        self.assertIsNone(derive(normalize_usage({'input_tokens':0,'output_tokens':0}))['cache_hit_ratio'])

    def test_duplicate_sessions_models_days_and_local_ranges(self):
        def r(s,m,stamp,i,c,o):
            return dict(session=s,model=m,timestamp=stamp,event_id=stamp,
                        tokens=normalize_usage(dict(input_tokens=i,cached_input_tokens=c,output_tokens=o,
                        reasoning_output_tokens=2,cache_write_input_tokens=0)))
        a=r('a','m1','2026-09-16T02:00:00Z',100,80,20)
        b=r('b','m2','2026-09-09T02:00:00Z',40,20,5)
        result=aggregate([a,a,b],tz=timezone.utc)
        self.assertEqual(result['tokens']['total_tokens'],165)
        self.assertEqual(sum(x['tokens']['total_tokens'] for x in result['models']),165)
        self.assertEqual(len(result['sessions']),2)
        h=history_ranges(result['daily'],date(2026,9,16))
        self.assertEqual(h['today']['tokens']['total_tokens'],120)
        self.assertEqual(h['last7']['tokens']['total_tokens'],120)
        self.assertEqual(h['last30']['tokens']['total_tokens'],165)

    def test_partial_coverage_exposes_known_subtotal(self):
        records=[dict(session='a',model='x',timestamp='2026-09-16T00:00:00Z',event_id='1',
                      tokens=normalize_usage({'input_tokens':10,'output_tokens':2,'cached_input_tokens':8})),
                 dict(session='a',model='x',timestamp='2026-09-16T00:00:01Z',event_id='2',
                      tokens=normalize_usage({'input_tokens':20,'output_tokens':3}))]
        a=aggregate(records)
        self.assertEqual(a['tokens']['input_tokens'],30)
        self.assertIsNone(a['tokens']['cached_input_tokens'])
        self.assertEqual(a['known']['cached_input_tokens'],8)
        self.assertEqual(a['coverage']['cached_input_tokens'],1)

    def test_recorded_reset_counts_last_request_only(self):
        s=SessionUsage(Path('unused'))
        s.consume({'type':'turn_context','payload':{'model':'gpt-6-astra'}})
        def e(total,last,ts):
            return {'type':'event_msg','timestamp':ts,'payload':{'type':'token_count','info':{
                'total_token_usage':{'input_tokens':total,'output_tokens':0,'total_tokens':total},
                'last_token_usage':{'input_tokens':last,'output_tokens':0,'total_tokens':last}}}}
        s.consume(e(100,100,'2026-09-16T00:00:00Z'))
        s.consume(e(20,20,'2026-09-16T00:01:00Z'))
        s.consume(e(20,20,'2026-09-16T00:01:00Z'))
        self.assertEqual(s.total['total_tokens'],120)
        self.assertEqual(aggregate(s.records)['tokens']['total_tokens'],120)

    def test_first_cumulative_carry_is_unattributed_not_assigned_today(self):
        s=SessionUsage(Path('unused'))
        s.consume({'type':'turn_context','payload':{'model':'gpt-6-astra'}})
        s.consume({'type':'event_msg','timestamp':'2026-09-16T00:00:00Z','payload':{'type':'token_count','info':{
            'total_token_usage':{'input_tokens':100,'output_tokens':10,'total_tokens':110},
            'last_token_usage':{'input_tokens':20,'output_tokens':2,'total_tokens':22}}}})
        a=aggregate(s.records)
        self.assertEqual(a['tokens']['total_tokens'],110)
        self.assertEqual(a['undated']['tokens']['total_tokens'],88)
        self.assertEqual(a['daily'][0]['tokens']['total_tokens'],22)

    def test_inherited_fork_prefix_removed_unique_child_preserved(self):
        from usage import unique_records
        base={'input_tokens':100,'output_tokens':10,'total_tokens':110}
        extra={'input_tokens':150,'output_tokens':15,'total_tokens':165}
        def session(sid,parent=None):
            s=SessionUsage(Path(sid))
            s.consume({'type':'session_meta','payload':{'id':sid,'forked_from_id':parent}})
            s.consume({'type':'turn_context','payload':{'model':'gpt-6-astra'}})
            s.consume({'type':'event_msg','timestamp':'2026-09-16T00:00:00Z','payload':{'type':'token_count','info':{'total_token_usage':base,'last_token_usage':base}}})
            return s
        parent=session('parent')
        child=session('child','parent')
        child.consume({'type':'event_msg','timestamp':'2026-09-16T00:01:00Z','payload':{'type':'token_count','info':{'total_token_usage':extra,'last_token_usage':{'input_tokens':50,'output_tokens':5,'total_tokens':55}}}})
        a=aggregate(unique_records([parent,child]))
        self.assertEqual(a['tokens']['total_tokens'],165)
        self.assertEqual(len(a['sessions']),2)


if __name__=='__main__':unittest.main()
