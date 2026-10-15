import csv, json, os
D = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(D, '..', 'metrics.csv'))))
stream = json.load(open(os.path.join(D, 'stream_names.json')))
LOW_CONF = set()  # every stream reading was 'high'; none flagged

games = {}
for r in rows:
    if r['excluded'] == '1':
        continue
    games.setdefault(r['id'], {})[r['player']] = r
opp = {}
for gid, g in games.items():
    p2 = g['p2']
    if p2['dataset'].startswith('stream'):
        if gid not in stream:
            raise SystemExit(f'no stream name for {gid}')
        opp[gid] = stream[gid]
    else:
        if not p2['who']:
            raise SystemExit(f'no who for {gid}')
        opp[gid] = p2['who']
json.dump(dict(sorted(opp.items())), open(os.path.join(D, 'opponents.json'), 'w'), ensure_ascii=False, indent=1)

F = ['duration_s', 'pieces', 'lines_cleared', 'attack', 'garbage_cleared']
def pool(rs):
    s = {f: sum(float(r[f]) for r in rs) for f in F}
    t = s['duration_s']
    return dict(PPS=s['pieces']/t, APM=60*s['attack']/t, VS=100*(s['attack']+s['garbage_cleared'])/t,
                APP=s['attack']/s['pieces'], DS_per_piece=s['garbage_cleared']/s['pieces'], LPM=60*s['lines_cleared']/t)

groups = {}
for gid, n in opp.items():
    groups.setdefault(n, []).append(gid)
order = sorted(groups, key=lambda n: -len(groups[n]))
sets = [(n, groups[n], False) for n in order]
sets.append(('stream (all)', [g for g in opp if games[g]['p2']['dataset'].startswith('stream')], True))
sets.append(('all opponents', list(opp), True))

M = ['PPS', 'APM', 'VS', 'APP', 'DS_per_piece', 'LPM']
out = []
for n, ids, agg in sets:
    o = pool([games[g]['p2'] for g in ids]); s = pool([games[g]['p1'] for g in ids])
    src = sorted({games[g]['p2']['dataset'] for g in ids})
    out.append(dict(opponent=n, aggregate=int(agg), sources=';'.join(src), games=len(ids),
                    opp_wins=sum(int(games[g]['p2']['won']) for g in ids),
                    **{'opp_'+m: o[m] for m in M}, **{'sk_'+m: s[m] for m in M}))
with open(os.path.join(D, 'opponents.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)

fmt = {'PPS': '{:.3f}', 'APM': '{:.2f}', 'VS': '{:.2f}', 'APP': '{:.3f}', 'DS_per_piece': '{:.3f}', 'LPM': '{:.2f}'}
L = ['| opponent | source | games | opp wins | opp PPS | opp APM | opp VS | opp APP | opp DS/piece | opp LPM | sk PPS | sk APM | sk VS | sk APP | sk DS/piece | sk LPM | flag |',
     '|' + '---|' * 17]
for r in out:
    flags = []
    if not r['aggregate'] and r['games'] < 3: flags.append('small n, do not compare')
    if r['opponent'] in LOW_CONF: flags.append('low-confidence name')
    L.append('| ' + ' | '.join([('**%s**' % r['opponent']) if r['aggregate'] else r['opponent'], r['sources'].replace(';', ', '),
        str(r['games']), str(r['opp_wins'])] + [fmt[m].format(r['opp_'+m]) for m in M] + [fmt[m].format(r['sk_'+m]) for m in M]
        + ['; '.join(flags)]) + ' |')
a = out[-1]; tot = sum(r['games'] for r in out if not r['aggregate'])
exp = dict(PPS=(1.909, 3), APM=(89.05, 2), VS=(183.54, 2), APP=(0.778, 3))
chk = [f"per-opponent games sum = {tot} (expect 98): {'PASS' if tot == 98 else 'FAIL'}"]
for m, (v, d) in exp.items():
    got = round(a['opp_'+m], d)
    chk.append(f"all-opponents {m} = {a['opp_'+m]:.6f} -> {got} (expect {v}): {'PASS' if got == v else 'FAIL'}")
nstream = len({opp[g] for g in opp if games[g]['p2']['dataset'].startswith('stream')})
md = ['# Opponent metrics (pooled, ratio of sums, non-excluded games)', '',
      'sk = syakegohan (p1). Rates are sums over the opponent\'s games: PPS = pieces/s, APM = 60·attack/s, VS = 100·(attack+garbage_cleared)/s, APP = attack/pieces, DS/piece = garbage_cleared/pieces, LPM = 60·lines/s.',
      'Opponents with fewer than 3 games are flagged "small n, do not compare". Every stream name was read by two independent readers, all at high confidence, so no name is flagged low-confidence.', '']
md += L + ['', f'Distinct stream opponents: {nstream}', '', '## Checks', ''] + ['- ' + c for c in chk]
open(os.path.join(D, 'opponents.md'), 'w').write('\n'.join(md) + '\n')
print('\n'.join(md))
