# Auto-settle frame-check items the score OCR already decides, before the groups go to the checkers.
# usage: python3 autosettle.py OCR_DIR GROUPS_DIR OUT_FILE [--dry]
#   e.g. autosettle.py /tmp/claude-0/<set>/w/ocrall corr/groups corr/out/auto.json, after the grouping step and
#   before the checkers. Reads GROUPS_DIR/g*.json and the per-game score OCR OCR_DIR/GID.json
#   [(t, s1, d1, s2, d2), ...] that ocr_all.sh writes; rewrites the groups without the settled items and
#   writes OUT_FILE {rule_version, no_change: [{group, n, id, player, rule, why}], audit: [{group, n}], hints: [...]}.
#   merge_xo.py ignores no_change, so a settled item changes no output; it only skips the frame check.
#
# Rules (each item carries its rule id, so a wrong rule can be found and reverted):
#   ko-flat-v1   'winner KO piece not counted': the player's stable score at the last spawn equals the last
#                stable score read after KO + 0.2 s. A piece that locked on the KO frame scores at least its
#                drop points, so an unchanged score means nothing locked -> no change. Only this direction
#                is settled; a rise stays with the checker (backtest: a rise was a real piece in 18 of 52).
#   tsb-hint-v1  'T-spin without a banner': not settled. The one score jump near the clear is compared with
#                the T-spin and the plain value sets (level 3, B2B x1.5 on hard clears, REN 0..30, drop 0..80)
#                and the verdict is appended to the item's detail as evidence for the checker.
# Backtest 2026-11-14 on two streams with checker labels (xo, te): ko-flat-v1 settled 49 items, all labelled
# no change by the checkers; tsb-hint-v1 decided 10 of 15 items, none against the label.
# AUDIT_MOD: every AUDIT_MOD-th settled item (by a stable hash) stays in its group as an audit sample.
import sys, os, re, json, glob, zlib
AUDIT_MOD = 10
a = [x for x in sys.argv[1:] if x != '--dry']; DRY = '--dry' in sys.argv
OCR, GROUPS, OUT = a
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jumps import stable, events   # the chains' check/ocr/jumps.py, copied

_cache = {}
def ocr(g):
    if g not in _cache:
        f = f'{OCR}/{g}.json'
        _cache[g] = json.load(open(f)) if os.path.exists(f) else None
    return _cache[g]
def seq(g, p, t0, t1):
    r = ocr(g)
    if r is None: return None
    si = 1 if p == 'p1' else 3
    return [(x[0], x[si]) for x in r if t0 <= x[0] <= t1]

def ko_flat(x):
    m = re.search(r'last spawn ([\d.]+) s', x['detail'])
    if not m: return None
    ko = x['t_s']; ts = ko - float(m.group(1))
    s = seq(x['id'], x['player'], ts - 1.0, ko + 1.5)
    if not s: return None
    st = stable(s)
    before = [v for t, v in st if t <= ts + 0.02]; after = [v for t, v in st if t >= ko + 0.2]
    if not before or not after: return None
    if after[-1] != before[-1]: return None
    return f'score {before[-1]} at the last spawn ({ts:.2f} s) and still {after[-1]} after the KO ({ko:.2f} s): nothing locked'

V = {'single': 100, 'double': 300, 'triple': 500, 'tss': 800, 'tsd': 1200, 'tst': 1600, 'tsmini': 200}
PLAIN = {'tss': 'single', 'tsd': 'double', 'tst': 'triple', 'tsmini': 'single'}
def values(k):
    out = set()
    for b2b in (1, 1.5):
        if b2b == 1.5 and k in ('single', 'double', 'triple'): continue
        for r in range(31): out.add(int(V[k] * 3 * b2b) + 150 * r)
    return out
def tsb_hint(x):
    m = re.match(r'A (\w+) at ([\d.]+) s', x['detail'])
    if not m or m.group(1) not in PLAIN: return None
    k, t = m.group(1), float(m.group(2))
    s = seq(x['id'], x['player'], t - 1.0, t + 1.5)
    if not s: return None
    ev = [(tt, d) for tt, d in events(s) if t - 0.4 <= tt <= t + 1.0]
    if len(ev) != 1: return f'[{RULE_TSB}] score jumps near the clear: {ev}; undecided'
    d = ev[0][1]
    fit = lambda kk: any(0 <= d - v <= 80 for v in values(kk))
    ts, pl = fit(k), fit(PLAIN[k])
    v = f'fits {k} only' if ts and not pl else f'fits plain {PLAIN[k]} only' if pl and not ts else 'fits both or neither'
    return f'[{RULE_TSB}] one score jump +{d} at {ev[0][0]} s: {v}'

RULE_KO, RULE_TSB = 'ko-flat-v1', 'tsb-hint-v1'
files = sorted(glob.glob(f'{GROUPS}/g*.json'))
res = {'rule_version': [RULE_KO, RULE_TSB], 'no_change': [], 'audit': [], 'hints': [], 'no_ocr': []}
for f in files:
    g = json.load(open(f)); keep = []; gk = os.path.basename(f)[:-5]
    for x in g:
        if ocr(x['id']) is None and x['id'] not in res['no_ocr']: res['no_ocr'].append(x['id'])
        if x['field_or_issue'] == 'winner KO piece not counted':
            why = ko_flat(x)
            if why:
                key = f"{x['id']} {x['player']} {x['t_s']}"
                if zlib.crc32(key.encode()) % AUDIT_MOD == 0:
                    res['audit'].append(dict(group=gk, n=x['n'])); x = dict(x, detail=x['detail'] + f' [audit sample of {RULE_KO}: {why}]')
                else:
                    res['no_change'].append(dict(group=gk, n=x['n'], id=x['id'], player=x['player'], rule=RULE_KO, why=why)); continue
        elif x['field_or_issue'] == 'T-spin without a banner':
            h = tsb_hint(x)
            if h: res['hints'].append(dict(group=gk, n=x['n'], hint=h)); x = dict(x, detail=x['detail'] + ' ' + h)
        keep.append(x)
    if not DRY: json.dump(keep, open(f, 'w'), ensure_ascii=False, indent=1)
    print(f, len(g), '->', len(keep))
if not DRY:
    os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True); json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(f"settled {len(res['no_change'])} ({RULE_KO}), audit {len(res['audit'])}, hints {len(res['hints'])}, games without OCR {len(res['no_ocr'])}")
