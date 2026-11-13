# [ac, new file] The video is a replay recording with uyeshota on the RIGHT board, so the chain reads him as p2.
# build_games_csv labels p1 'uyeshota' by position; this swaps every column from `won` on between the two rows of a
# game (the measured board goes with its result), so that p1 is uyeshota as the repo requires, and flips `player`
# in the hand-edit rows. Usage: python3 swap_sides.py <chain games.csv> <hand_edits.csv> <out games.csv> <out hand_edits.csv>
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1]))); F = list(rows[0].keys()); k = F.index('won')
by = {}
for r in rows: by.setdefault(r['id'], {})[r['player']] = r
out = []
for r in rows:
    o = by[r['id']]['p2' if r['player'] == 'p1' else 'p1']
    out.append({**{f: r[f] for f in F[:k]}, **{f: o[f] for f in F[k:]}})
for g in by: assert {by[g]['p1']['won'], by[g]['p2']['won']} == {'0', '1'}, g
w = csv.DictWriter(open(sys.argv[3], 'w'), F, lineterminator='\n'); w.writeheader(); w.writerows(out)
hw = csv.writer(open(sys.argv[4], 'w'), lineterminator='\n')
for r in csv.reader(open(sys.argv[2])):
    r[1] = {'p1': 'p2', 'p2': 'p1'}[r[1]]; hw.writerow(r)
print(len(out), 'rows swapped')
