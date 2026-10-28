# Score-jump clear count vs the chain's clear events, per player-game.
import json, sys, os
sys.path.insert(0, '/private/tmp/claude-501/am/corr/ocr')
import deltas3  # noqa: E402
def events(seq, th=60):
    st = deltas3.stable(seq); ev = []; cur = None
    for i, (t, v) in enumerate(st):
        if cur is None: cur = v; continue
        nxt = [w for _, w in st[i + 1:i + 4]]
        if v < cur - 100 or v - cur > 20000: continue
        if nxt and sum(abs(w - v) < 200 or w > v for w in nxt) < len(nxt) / 2: continue
        d = v - cur
        if d >= th: ev.append((round(t, 2), d))
        if d > 0 or d < -100: cur = v
        elif d < 0: cur = max(cur, v)
    return ev
D = '/private/tmp/claude-501/am/corr/ocrall'
J = {j['id']: j for j in map(json.loads, open('/private/tmp/claude-501/am/w/chain/am/w/A/games.jsonl'))}
S = json.load(open('/private/tmp/claude-501/am/w/chain/am/w/tetrio/cseq.json'))
out = []
for g in sorted(J):
    f = f'{D}/{g}.json'
    if not os.path.exists(f): continue
    r = json.load(open(f)); end = J[g]['end_s']
    for p, si in (('p1', 1), ('p2', 3)):
        jumps = [(t, d) for t, d in events([(x[0], x[si]) for x in r]) if t <= end + 0.5]
        ch = [z for z in S[f'{g} {p}'] if z[1] not in (None, 'BREAK')]
        out.append(dict(id=g, player=p, score_jumps=len(jumps), chain_clears=len(ch), diff=len(jumps) - len(ch),
                        tail=[x for x in jumps if x[0] > end - 1.5], last_chain=ch[-1][0] if ch else None, end=end))
json.dump(out, open(f'{D}/compare.json', 'w'), indent=0)
bad = [o for o in out if o['diff']]
print(len(out), 'player-games;', len(bad), 'disagree')
for o in bad: print(o['id'], o['player'], 'score', o['score_jumps'], 'chain', o['chain_clears'], 'tail', o['tail'], 'end', o['end'])
