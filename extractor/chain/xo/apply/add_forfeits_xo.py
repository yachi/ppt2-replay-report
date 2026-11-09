"""[xo] Append u093 and u094 to the chain's games csv. Extractor A returned None on u094 (ゆうくん stacked every
piece in one column and topped out in about 2 s, twice), so both games were dropped from games.json before the
event steps and have no chain rows. Their counts below were read off the video frame by frame:

u093 (start 5828.7, ~2.27 s): uyeshota 7 pieces, 0 lines (score rose 7 drops); ゆうくん 7 pieces (J,T,O,L,I,Z,I in one column), 0 lines.
u094 (start 5837.3, ~2.2 s):  uyeshota 1 piece (L), 0 lines; ゆうくん 8 pieces, 0 lines.
Every other count of both games is 0. The rows go in as included; hand-edits.csv excludes them with the reason.

usage: python3 apply/add_forfeits_xo.py <chain games.csv>   (rewrites it in place, games in id order)
"""
import csv, json, sys

G = {g['id']: g for g in json.load(open('/tmp/claude-0/xo/w/chain/xo/games_all.json'))}
COUNTS = {('u093', 'p1'): (2.27, 7), ('u093', 'p2'): (2.27, 7), ('u094', 'p1'): (2.2, 1), ('u094', 'p2'): (2.2, 8)}

path = sys.argv[1]
with open(path, encoding='utf-8', newline='') as fh:
    rd = csv.DictReader(fh); rows = list(rd); cols = rd.fieldnames
assert not [r for r in rows if r['id'] in ('u093', 'u094')], 'forfeit rows already present'
for (gid, p), (dur, pieces) in COUNTS.items():
    g = G[gid]
    r = {c: '0' for c in cols}
    r.update(id=gid, dataset=g['dataset'], video=g['video'], start_s=g['start_s'], opener='', opponent=g['opponent'],
             player=p, who='uyeshota' if p == 'p1' else g['opponent'], won='1' if (p == 'p1') == (g['counter_winner'] == 1) else '0',
             excluded='0', reason='', duration_s=dur, pieces=pieces)
    rows.append(r)
rows.sort(key=lambda r: (r['id'], r['player']))
with open(path, 'w', encoding='utf-8', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=cols, lineterminator='\n'); w.writeheader(); w.writerows(rows)
print(len(rows), 'rows')
