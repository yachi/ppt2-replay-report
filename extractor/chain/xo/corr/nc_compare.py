# [xo] NEXT-queue recount against the final table (ach's rule): spawns = shifts_total, less the first hold into an
# empty box, less an unmatched last spawn (a last shift after the last chain event). Bad bags or long unknown
# stretches mark the reading as lost.
import csv, json, glob, os, collections
T = {(r['id'], r['player']): r for r in csv.DictReader(open('analysis/ppt2-uyeshota/games.csv'))}
res = collections.Counter(); rows = []
for f in sorted(glob.glob('/tmp/claude-0/xo/corr/nc/*.json')):
    gid, p = os.path.basename(f)[:-5].split('_')
    try: d = json.load(open(f))
    except Exception: res['unreadable'] += 1; rows.append((gid, p, 'unreadable')); continue
    est = d['shifts_total'] - (1 if d.get('first_hold') else 0) - (1 if d['last_shift'] and d['last_shift'][0] > d['last_event'] + 0.05 else 0)
    have = int(T[(gid, p)]['pieces']); diff = est - have
    lost = bool(d['bag_bad_blocks']) or bool(d['long_unknown'])
    k = 'lost' if lost and diff else ('same' if diff == 0 else ('one' if abs(diff) == 1 else 'more'))
    res[k] += 1; rows.append((gid, p, k, est, have, diff, len(d['bag_bad_blocks']), len(d['long_unknown'])))
print(dict(res), sum(res.values()))
for r in rows:
    if r[2] in ('more', 'unreadable'): print(r)
json.dump(rows, open('/tmp/claude-0/xo/corr/nc_compare.json', 'w'))
