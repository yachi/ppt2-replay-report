"""Build all_rows.csv (old + new rows, with an opponent column) and pool metrics.

Pooling is a RATIO OF SUMS over included rows (excluded == 0).
"""
import csv, glob, json, os, collections

M = '/private/tmp/claude-501/sk/endfix/combo3/apply/c3/B/w'
OUT = '/private/tmp/claude-501/sk/endfix/combo3/apply/c3/pool'

# --- verify.md findings: games whose rows the checker found wrong ----------
# No opponent-name corrections: verify.md section 1 found 102/102 names correct.
CHECKER_EXCLUDE = {
    'i033': 'checker: p1 quad count 25 in rows, 26 in video (game-ending Tetris at ~3784.0 s dropped; '
            'recorded end falls before the final clear)',
    'j008': 'checker: p1 T-spin Triple 3 in rows, 4 in video (game-ending TST at ~1857.85 s dropped; '
            'recorded end falls before the final clear)',
}

old = list(csv.DictReader(open(f'{M}/metrics.csv')))
header = list(old[0].keys())
opp = json.load(open(f'{M}/opp/opponents.json'))
new = []
for f in sorted(glob.glob(f'{OUT}/rows_*.csv')):
    rs = list(csv.DictReader(open(f)))
    assert list(rs[0].keys()) == header, f
    new += rs

for r in old:
    r['source'] = 'old'
    r['opponent'] = opp.get(r['id'], '')
newopp = {r['id']: r['who'] for r in new if r['player'] == 'p2'}
for r in new:
    r['source'] = 'new'
    r['opponent'] = newopp[r['id']]
rows = old + new

exclusions = []  # (id, player, opponent, reason, source)
for r in rows:
    if r['id'] in CHECKER_EXCLUDE and r['excluded'] != '1':
        r['excluded'] = '1'
        r['reason'] = (r['reason'] + ' ' if r['reason'] else '') + CHECKER_EXCLUDE[r['id']]
for r in rows:
    if r['excluded'] == '1':
        exclusions.append((r['id'], r['player'], r['opponent'] or '(name not read)', r['reason'].strip(), r['source']))

ids = [r['id'] for r in rows]
assert len(ids) == len(set((r['id'], r['player']) for r in rows)), 'duplicate id/player'
# whole-game exclusion consistency
byg = collections.defaultdict(list)
for r in rows:
    byg[r['id']].append(r)
for g, rs in byg.items():
    assert len(rs) == 2 and {x['player'] for x in rs} == {'p1', 'p2'}, g
    assert len({x['excluded'] for x in rs}) == 1, f'{g} half-excluded'
    assert rs[0]['opponent'] == rs[1]['opponent']
    if rs[0]['excluded'] == '0':
        assert rs[0]['opponent'], f'{g} included with no opponent name'
        w = sorted(int(x['won']) for x in rs)
        assert w == [0, 1], f'{g} winners {w}'

with open(f'{OUT}/all_rows.csv', 'w', newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=header + ['opponent', 'source'])
    wr.writeheader()
    wr.writerows(rows)

F = lambda r, k: float(r[k]) if r[k] not in ('', None) else 0.0


def pool(rs):
    n = len(rs)
    if n == 0:
        return None
    S = lambda k: sum(F(r, k) for r in rs)
    t = S('duration_s'); pcs = S('pieces'); atk = S('attack'); dsc = S('garbage_cleared')
    lines = S('lines_cleared')
    q = S('quad'); tss = S('tss'); tsd = S('tsd'); tst = S('tst'); mini = S('tsmini')
    clears = S('single') + S('double') + S('triple') + q + tss + tsd + tst + mini
    mn = t / 60
    return dict(
        games=n, wins=int(S('won')), PPS=pcs / t, APM=60 * atk / t, VS=100 * (atk + dsc) / t,
        APP=atk / pcs, DS_per_piece=dsc / pcs, DS_per_s=dsc / t, LPM=lines / mn,
        quads_per_min=q / mn, tspins_per_min=(tss + tsd + tst) / mn, TSD_per_min=tsd / mn,
        quad_pct_clears=100 * q / clears, tspin_pct_clears=100 * (tss + tsd + tst) / clears,
        PCs=int(S('pc')), max_REN=int(max(F(r, 'max_combo') for r in rs)),
        max_B2B=int(max(F(r, 'max_b2b') for r in rs)), recv_rows_per_min=S('garbage_received_rows') / mn,
        mean_game_s=t / n, total_min=mn,
    )


inc = [r for r in rows if r['excluded'] == '0']
p1 = [r for r in inc if r['player'] == 'p1']
p2 = [r for r in inc if r['player'] == 'p2']
opps = sorted({r['opponent'] for r in p2}, key=lambda o: -sum(r['opponent'] == o for r in p2))

table = []  # (scope, player, metrics)
table.append(('all', 'syakegohan', pool(p1)))
table.append(('all', 'all opponents', pool(p2)))
for o in opps:
    table.append((f'vs {o}', 'syakegohan', pool([r for r in p1 if r['opponent'] == o])))
    table.append((f'vs {o}', o, pool([r for r in p2 if r['opponent'] == o])))

keys = list(table[0][2].keys())
with open(f'{OUT}/pooled.csv', 'w', newline='') as fh:
    wr = csv.writer(fh)
    wr.writerow(['scope', 'player'] + keys)
    for s, p, m in table:
        wr.writerow([s, p] + [round(m[k], 4) if isinstance(m[k], float) else m[k] for k in keys])

# --- self-check: old-only subset -------------------------------------------
op1 = pool([r for r in p1 if r['source'] == 'old'])
op2 = pool([r for r in p2 if r['source'] == 'old'])
checks = [('syakegohan PPS', op1['PPS'], 1.956, 3), ('syakegohan APM', op1['APM'], 91.26, 2),
          ('opponents PPS', op2['PPS'], 1.909, 3), ('opponents APM', op2['APM'], 89.05, 2)]
check_lines = []
allpass = True
for name, got, want, dp in checks:
    ok = round(got, dp) == want
    allpass &= ok
    check_lines.append(f'| {name} | {want} | {got:.{dp + 2}f} | {"PASS" if ok else "FAIL"} |')

# --- markdown --------------------------------------------------------------
def fmt(m, k):
    v = m[k]
    if k in ('games', 'wins', 'PCs', 'max_REN', 'max_B2B'):
        return str(v)
    if k in ('PPS', 'APP', 'DS_per_piece', 'DS_per_s'):
        return f'{v:.3f}'
    return f'{v:.2f}' if k != 'mean_game_s' else f'{v:.1f}'

cols = [('games', 'G'), ('wins', 'W'), ('PPS', 'PPS'), ('APM', 'APM'), ('VS', 'VS'), ('APP', 'APP'),
        ('DS_per_piece', 'DS/pc'), ('DS_per_s', 'DS/s'), ('LPM', 'LPM'), ('quads_per_min', 'Q/min'),
        ('tspins_per_min', 'TS/min'), ('TSD_per_min', 'TSD/min'), ('quad_pct_clears', 'Q %clr'),
        ('tspin_pct_clears', 'TS %clr'), ('PCs', 'PC'), ('max_REN', 'maxREN'), ('max_B2B', 'maxB2B'),
        ('recv_rows_per_min', 'recv/min'), ('mean_game_s', 'mean s')]

L = []
L.append('# syakegohan vs opponents: pooled metrics, old + new games\n')
n_old = len({r['id'] for r in rows if r['source'] == 'old'}); n_new = len({r['id'] for r in rows if r['source'] == 'new'})
n_inc = len({r['id'] for r in inc})
n_inc_old = len({r['id'] for r in inc if r['source'] == 'old'}); n_inc_new = n_inc - n_inc_old
L.append(f'Games: {n_old + n_new} found ({n_old} old, {n_new} new). Included: **{n_inc}** '
         f'({n_inc_old} old, {n_inc_new} new). Excluded: {n_old + n_new - n_inc} (listed below).\n')
L.append('Every figure is a ratio of sums over included games: e.g. PPS = sum(pieces)/sum(seconds), '
         'APM = 60*sum(attack)/sum(s), VS = 100*sum(attack+garbage_cleared)/sum(s), APP = sum(attack)/sum(pieces), '
         'DS = garbage_cleared. T-spins = TSS+TSD+TST (Minis not counted). Clears for the % columns = '
         'single+double+triple+quad+TSS+TSD+TST+Mini (untyped gap lines are not clears). '
         'max REN is the max of `max_combo`. recv/min = garbage rows received per minute. '
         'mean s = sum(seconds)/games.\n')
L.append('Files: `all_rows.csv` (old + new rows, `opponent` and `source` columns), `pooled.csv`, `pool.py`.\n')

L.append('## Pooled table\n')
L.append('| scope | player | ' + ' | '.join(c[1] for c in cols) + ' |')
L.append('|---|---|' + '---|' * len(cols))
for s, p, m in table:
    L.append(f'| {s} | {p} | ' + ' | '.join(fmt(m, k) for k, _ in cols) + ' |')
L.append('')

L.append("## syakegohan's record per opponent\n")
L.append('| opponent | games | syakegohan W-L | win % | syake PPS / APM / VS | opp PPS / APM / VS | APP syake / opp |')
L.append('|---|---|---|---|---|---|---|')
for o in ['all opponents'] + opps:
    a = pool(p1) if o == 'all opponents' else pool([r for r in p1 if r['opponent'] == o])
    b = pool(p2) if o == 'all opponents' else pool([r for r in p2 if r['opponent'] == o])
    L.append(f"| {o} | {a['games']} | {a['wins']}-{a['games'] - a['wins']} | {100 * a['wins'] / a['games']:.0f}% | "
             f"{a['PPS']:.3f} / {a['APM']:.2f} / {a['VS']:.2f} | {b['PPS']:.3f} / {b['APM']:.2f} / {b['VS']:.2f} | "
             f"{a['APP']:.3f} / {b['APP']:.3f} |")
L.append('')

L.append('## Sample size: opponents with >= 10 included games\n')
cnt = collections.Counter(r['opponent'] for r in p2)
L.append('| opponent | included games | >= 10? |')
L.append('|---|---|---|')
for o in opps:
    L.append(f"| {o} | {cnt[o]} | {'yes' if cnt[o] >= 10 else '**no**'} |")
yes = [o for o in opps if cnt[o] >= 10]; no = [o for o in opps if cnt[o] < 10]
L.append(f'\n{len(yes)} of {len(opps)} opponent names reach 10: {", ".join(yes)}. '
         f'Below 10: {", ".join(f"{o} ({cnt[o]})" for o in no)}. '
         'Remakun needs at least 1 more included game (2 of its 11 found games, i002 and i004, are excluded as unresolved lower bounds; resolving either bound is the cheapest route to 10). '
         'いんたい has only 2 games and should be read as anecdote, or as part of あめみや　はいしん if that link is confirmed.\n')

L.append('## Name variants that may be the same person (NOT merged)\n')
L.append('- **しょうがく5ねんせい / しょうがく6ねんせい**: only しょうがく6ねんせい occurs in the included rows '
         f"({cnt.get('しょうがく6ねんせい', 0)} games: old + new). The string しょうがく5ねんせい appears nowhere under /private/tmp/claude-501/sk/ (grep of every text file), so nothing to merge here; "
         'if a 5ねんせい nameplate turns up in other videos it is probably the same player one school year earlier (unverified).')
L.append(f"- **あめみや variants**: `あめみや　はいしん` (full-width space) is the only spelling in the rows "
         f"({cnt.get('あめみや　はいしん', 0)} games; 3 old + new). Old and new spell it identically (same code points), "
         'so pooling them under one name is a string match, not a merge. A grep of every text file under /private/tmp/claude-501/sk/ finds no other '
         'あめみや player spelling; the only other hit is the opener name あめみや砲 on the shiwehi page dumps, which is not a player.')
L.append(f"- **いんたい** ({cnt.get('いんたい', 0)} games, i018-i019) appears between two runs of あめみや　はいしん games in the same "
         'video (i011-i017, i020-i034). It may be the same account under a temporary name ("引退" = retired); '
         'the checker read the nameplate as いんたい in both games. Kept separate.')
L.append('')

L.append('## Exclusions (every one listed)\n')
L.append('| game | player | opponent | source | reason |')
L.append('|---|---|---|---|---|')
for e in sorted(exclusions):
    L.append(f'| {e[0]} | {e[1]} | {e[2]} | {e[4]} | {e[3]} |')
L.append('\nWhole games are excluded when either player\'s row is excluded, so no game contributes one side only. '
         'The 10 old excluded games have no opponent name recorded (opponents.json does not cover them). '
         'i033 and j008 were excluded on the checker\'s findings rather than patched by hand, as instructed.\n')
L.append('**Caveat from the checker**: in both i033 and j008 the recorded game end falls just before the final, '
         'winning clear, so that clear was dropped. Only 6 of 102 new games were checked; other games may also miss '
         'their last clear. Effect, if it is common: a downward bias in the winner\'s (usually syakegohan\'s) attack, lines and '
         'clear counts. Its size is unmeasured: 2 of the 6 checked games lost exactly one clear each.\n')
L.append('No opponent-name corrections were needed: the checker read all 102 new nameplates and found no disagreement.\n')

L.append('## Self-check: old-only subset reproduces the original figures\n')
L.append('| figure | expected | old-only subset | result |')
L.append('|---|---|---|---|')
L += check_lines
L.append(f"\nOverall: **{'PASS' if allpass else 'FAIL'}** (old-only subset = {op1['games']} games).")

open(f'{OUT}/pooled.md', 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
