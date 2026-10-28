# Match each chain clear event to a score jump by time. A chain event's t is the spawn of its piece, so its
# score jump falls in [t, next piece's spawn + 1.0 s]. Unmatched on either side = a spot to frame-check.
import json, sys
sys.path.insert(0, '/private/tmp/claude-501/am/corr/ocrall')
from compare import events, J, S, D  # noqa: E402
import os
rows = []
for g in sorted(J):
    if not os.path.exists(f'{D}/{g}.json'): continue
    r = json.load(open(f'{D}/{g}.json')); end = J[g]['end_s']
    for p, si in (('p1', 1), ('p2', 3)):
        jumps = [x for x in events([(x[0], x[si]) for x in r]) if x[0] <= end + 0.5]
        seq = S[f'{g} {p}']
        ch = [(i, z) for i, z in enumerate(seq) if z[1] not in (None, 'BREAK')]
        used = set(); miss_chain = []
        for i, z in ch:
            hi = (seq[i + 1][0] if i + 1 < len(seq) else end) + 1.0
            k = next((k for k, (t, d) in enumerate(jumps) if k not in used and z[0] - 0.1 <= t <= hi), None)
            if k is None: miss_chain.append(z)
            else: used.add(k)
        extra = [jumps[k] for k in range(len(jumps)) if k not in used]
        if miss_chain or extra:
            rows.append(dict(id=g, player=p, chain_without_jump=miss_chain, jump_without_chain=extra, end=end))
json.dump(rows, open(f'{D}/align.json', 'w'), indent=0)
n1 = sum(len(x['chain_without_jump']) for x in rows); n2 = sum(len(x['jump_without_chain']) for x in rows)
print(len(rows), 'player-games with a mismatch;', n1, 'chain clears with no score jump;', n2, 'score jumps with no chain clear')
tail = [(x['id'], x['player'], j) for x in rows for j in x['jump_without_chain'] if j[0] > x['end'] - 1.5]
print(len(tail), 'unmatched jumps in the last 1.5 s before KO')
