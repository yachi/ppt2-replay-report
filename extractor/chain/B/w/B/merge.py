import json, glob
order = [g['id'] for g in json.load(open('/private/tmp/claude-501/sk/games.json'))]
recs = {}
for f in sorted(glob.glob('parts/*.jsonl')):
    for l in open(f):
        d = json.loads(l); recs[d['id']] = d
with open('games.jsonl', 'w') as out:
    for gid in order:
        d = recs.get(gid) or dict(id=gid, p1=None, p2=None, duration_s=None, winner=None, confidence=0.0, notes='not measured: worker produced no record')
        out.write(json.dumps(d, ensure_ascii=False) + '\n')
nul = [g for g in order if not recs.get(g) or recs[g]['p1'] is None]
print('written', len(order), 'null', len(nul), nul)
conf = [recs[g]['confidence'] for g in order if g in recs and recs[g]['p1']]
import statistics as st; print('confidence median', st.median(conf), 'min', min(conf))
print('winner counts', {w: sum(1 for g in order if g in recs and recs[g]['winner'] == w) for w in ('p1', 'p2', None)})
