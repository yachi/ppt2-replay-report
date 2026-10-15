# Event overlay for the PPT2 chain. Patches {B,Y,lg,cVO}/w/tetrio/metrics.py of a mirror that already carries
# patch_combo.py (renx + postko), so that a JSON list of frame-verified clear-event corrections is applied to the
# CORRECTED sequence (after pcfix/PCDEC/correct()/postko, i.e. the exact list tally() sees) just before tally().
# Every dependent field (clear counts, pc, lines_cleared, garbage_cleared, attack parts, max_combo, max_b2b) is then
# recomputed by the chain's own tally()/streaks(); nothing is typed into a cell.
#
# Correction record: {id, side, op, t, ...}
#   t      data event time (2 decimals). It must match EXACTLY ONE non-None, non-BREAK event of (id, side) in the
#          corrected sequence, or the build raises. ('add' instead requires that NO event sits at t.)
#   was    [kind, lines, pc]  required for remove/retype/setpc: the matched event must currently be exactly this.
#   op     remove                         drop the event (its lines and gc go with it)
#          retype   kind, lines           change kind/lines; pc, gc, origin kept
#          setpc    pc (0|1)              set the pc flag
#          add      kind, lines, pc, gc   insert (t, kind, lines, pc, gc, 'O') in time order
#          replace_window  t_end, events  drop every event with t <= time <= t_end (must be >= 1), insert events
#   source free text (frames, files, eye time)
# Corrections are applied in file order. Per set: every correction whose id is in this set's games must have been
# applied by the end of the run, else the run raises. Applied corrections are printed and written to
# <set>/w/tetrio/overlay_applied.json.
# combo2/apply copy: replace_window takes an optional was_old [[t,kind,lines],...] guard; retype takes optional pc, gc.
# usage: patch_overlay2.py <mirror> <corrections.json>
import sys, os, json
M, CJ = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
json.load(open(CJ))  # must parse
DEF = '''import json as _oj
OVL = _oj.load(open(%r))
OVL_APPLIED = []
def _ovl_hits(cs, t):
    return [i for i, z in enumerate(cs) if z[1] not in (None, 'BREAK') and round(z[0], 2) == round(t, 2)]
def overlay(g, p, cs):
    cs = list(cs)
    for ci, c in enumerate(OVL):
        if c['id'] != g or c['side'] != p: continue
        op = c['op']; t = c['t']
        if op == 'add':
            assert not [z for z in cs if round(z[0], 2) == round(t, 2)], ('OVERLAY add: an event already at t', c)
            new = (t, c['kind'], int(c['lines']), bool(c['pc']), int(c.get('gc', 0)), 'O')
            j = next((i for i, z in enumerate(cs) if z[0] > t), len(cs)); cs.insert(j, new)
            OVL_APPLIED.append((ci, g, p, op, None, new)); continue
        if op == 'replace_window':
            idx = [i for i, z in enumerate(cs) if t - 1e-9 <= z[0] <= c['t_end'] + 1e-9]
            assert idx, ('OVERLAY replace_window: empty window', c)
            old = [cs[i] for i in idx]
            if 'was_old' in c:
                assert [[round(z[0], 2), z[1], z[2]] for z in old] == [[round(w[0], 2), w[1], int(w[2])] for w in c['was_old']], ('OVERLAY replace_window was_old mismatch', c, old)
            cs = [z for i, z in enumerate(cs) if i not in set(idx)]
            for e in c['events']:
                new = (e['t'], e['kind'], int(e['lines']), bool(e['pc']), int(e.get('gc', 0)), 'O')
                j = next((i for i, z in enumerate(cs) if z[0] > new[0]), len(cs)); cs.insert(j, new)
            OVL_APPLIED.append((ci, g, p, op, old, c['events'])); continue
        h = _ovl_hits(cs, t)
        assert len(h) == 1, ('OVERLAY: t must match exactly one clear event', c, [cs[i] for i in h])
        i = h[0]; z = cs[i]
        w = c['was']; assert [z[1], z[2], int(bool(z[3]))] == [w[0], int(w[1]), int(w[2])], ('OVERLAY was-mismatch', c, z)
        if op == 'remove': cs.pop(i); new = None
        elif op == 'retype': new = (z[0], c['kind'], int(c['lines']), bool(c['pc']) if 'pc' in c else z[3], int(c['gc']) if 'gc' in c else z[4], z[5]); cs[i] = new
        elif op == 'setpc': new = (z[0], z[1], z[2], bool(c['pc']), z[4], z[5]); cs[i] = new
        else: raise ValueError(('OVERLAY unknown op', c))
        OVL_APPLIED.append((ci, g, p, op, z, new))
    return cs

''' % CJ
for s in ['B', 'Y', 'lg', 'cVO']:
    f = f'{M}/{s}/w/tetrio/metrics.py'; src = open(f).read()
    out = f'{M}/{s}/w/tetrio/overlay_applied.json'
    reps = [
        ("def tally(seq):\n", DEF + "def tally(seq):\n"),
        ("        CURX[0] = (g, p); T = tally(cseq); CURX[0] = None\n",
         "        cseq = overlay(g, p, cseq)\n        CURX[0] = (g, p); T = tally(cseq); CURX[0] = None\n"),
        ("print('rows', len(out));",
         "_miss = [c for ci, c in enumerate(OVL) if c['id'] in R and ci not in {a[0] for a in OVL_APPLIED}]\n"
         "assert not _miss, ('OVERLAY corrections not applied', _miss)\n"
         "for _a in OVL_APPLIED: print('OVERLAY', _a)\n"
         f"_oj.dump([dict(index=a[0], id=a[1], side=a[2], op=a[3], before=a[4], after=a[5]) for a in OVL_APPLIED], open({out!r}, 'w'), indent=1)\n"
         "print('rows', len(out));"),
    ]
    for a, b in reps:
        assert src.count(a) == 1, (s, a); src = src.replace(a, b)
    open(f, 'w').write(src)
    print('patched', f)
