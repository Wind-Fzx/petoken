"""Opt-in validation against local numeric records; never exports transcripts."""
import json
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from usage import CodexStore,SessionUsage

store=CodexStore()
start=time.perf_counter()
data=store.read(include_history=True)
assert data.get('available'),data.get('status')
cold=time.perf_counter()-start
checked=0
for session in store.sessions.values():
    if session.fork_from or session.partial or any('reset' in n.lower() for n in session.notes):continue
    if not session.raw_total:continue
    for key,value in session.raw_total.items():
        if key in session.total:assert session.total[key]==value,(key,session.total[key],value)
    checked+=1
history=data['history']
assert sum(m['tokens']['total_tokens'] for m in history['models'])==history['tokens']['total_tokens']
assert sum(s['tokens']['total_tokens'] for s in history['sessions'])==history['tokens']['total_tokens']
before={key:value.offset for key,value in store.sessions.items()}
start=time.perf_counter();store.read(include_history=True);warm=time.perf_counter()-start
assert checked>=3
print(json.dumps(dict(sessions_reconciled=checked,models_reconcile=True,sessions_reconcile=True,
                     indexed_sessions=len(store.sessions),cold_seconds=round(cold,4),warm_seconds=round(warm,4))))
