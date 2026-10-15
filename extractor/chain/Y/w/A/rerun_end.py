import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze as A, endfix_a as endfix
endfix.install(A)
G = {g['id']: g for g in json.load(open('/private/tmp/claude-501/sk/metrics/more/games_YbMeCRhjG1k.json'))}
rows = [json.loads(l) for l in open('A/games.raw.jsonl')]
out = []
for r in rows:
    if r['duration_s'] is None:
        r = A.analyse(f'A/feat/{r["id"]}.npz', G[r['id']])
        for k in ('p1', 'p2'):
            if r.get(k):
                for x in ('_events', '_seq', '_hold_empty'): r[k].pop(x, None)
        r['notes'] = (r['notes'] + '; ' if r['notes'] else '') + 'end via endfix fallback (winner border dimmed)'
        print(r['id'], r['winner'], r['duration_s'], r['end_s'], r['p1']['pieces'], r['p2']['pieces'])
    out.append(r)
with open('A/games.jsonl', 'w') as f:
    for r in out: f.write(json.dumps(r, ensure_ascii=False) + '\n')
