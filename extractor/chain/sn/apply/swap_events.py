# [sn, new file] Flips `side` in the event corrections (written in the chain's frame, p1 = あてん) so that they are in
# the swapped frame the analysis files use (p1 = syakegohan). Usage: python3 swap_events.py <in.json> <out.json>
import json, sys
d = json.load(open(sys.argv[1]))
for e in d: e['side'] = {'p1': 'p2', 'p2': 'p1'}[e['side']]
json.dump(d, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1); open(sys.argv[2], 'a').write('\n')
print(len(d), 'corrections swapped')
