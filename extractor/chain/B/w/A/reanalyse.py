import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import analyze as A
games = json.load(open('/private/tmp/claude-501/sk/games.json'))
rows = []
for g in games:
    p = os.path.join(HERE, 'feat', g['id'] + '.npz')
    try:
        if not os.path.exists(p):
            raise FileNotFoundError('feature dump missing')
        r = A.analyse(p, g)
    except Exception as e:
        r = dict(id=g['id'], p1=None, p2=None, duration_s=None, winner=None, confidence=0,
                 notes=f'analysis failed: {type(e).__name__}: {e}')
    for k in ('p1', 'p2'):
        if r.get(k):
            for x in ('_events', '_seq', '_hold_empty'):
                r[k].pop(x, None)
    rows.append(r)
with open(os.path.join(HERE, 'games.jsonl'), 'w') as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
print(len(rows))
