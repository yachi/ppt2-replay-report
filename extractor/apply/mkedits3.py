import csv, sys
sys.path.insert(0, '/Users/yachi/github/tetrio-replay-report')
from pipeline.ppt2_page import apply_hand_edits
D = '/private/tmp/claude-501/sk/endfix/combo3/apply'
CHAIN = f'{D}/c3/games.csv'
with open(CHAIN, encoding='utf-8', newline='') as fh:
    rd = csv.DictReader(fh); cols = rd.fieldnames; rows = list(rd)
at = {(r['id'], r['player']): r for r in rows}
with open(f'{D}/hand-edits.base.csv', encoding='utf-8', newline='') as fh:
    old = list(csv.DictReader(fh))
assert len(old) == 58
print('existing rows whose was != new chain value:')
for e in old:
    v = at[(e['id'], e['player'])][e['field']]
    if v != e['was']: print('  MOVED', e['id'], e['player'], e['field'], 'was', repr(e['was']), 'chain', repr(v), 'value', repr(e['value']))
# rewrite the source of the existing i015 p2 pieces row (advisor F5); id/player/field/was/value untouched
hit = [e for e in old if (e['id'], e['player'], e['field']) == ('i015', 'p2', 'pieces')]
assert len(hit) == 1 and hit[0]['value'] == '62', hit
print('REWRITE source i015 p2 pieces; old source:', hit[0]['source'])
hit[0]['source'] = ('video frames: exactly 11 locks in 1605-1634 where the chain counts 16 (combo2/framesB/RESULTS.txt); '
    'the B single at 1574.7 is an O still falling (combo2/verify/VERDICTS.txt); the surplus is B\'s locks and pace-estimated '
    'gap pieces spliced into A\'s gap windows 1560.0-1581.37, 1581.37-1607.97, 1607.97-1625.24 (R/build.py:64-75), which '
    'double-count A\'s own intervals; 62 = A\'s own count, 2026-10-15')
ST = ('GO overlay read on video frames: start_s fell on the READY (レディ) overlay, 1.2-1.4 s before GO; the other 204 games '
      'start 0.10-0.20 s before GO onset (combo3/start/RESULTS.txt, go_res.json), 2026-10-15')
new = [
 ('g018', 'p2', 'pieces', '151', "video frames: the first piece (T) is held at the game's first spawn (T spawns 16.400, HOLD 16.467, S spawns 16.567) and A counts the empty interval as a lock (A: 'hold appeared at frame 71 with no matching queue shift', duplicated spawn at frame 71), 2026-10-15; combo3/pieces/fr_g018p2_16.30.png, combo3/advise/holdchk.py"),
 ('h011', 'p1', 'pieces', '32', "video frames: the first piece (Z) is held at the game's first spawn (Z spawns 968.367, HOLD 968.400, S spawns 968.500) and A counts the empty interval as a lock (A: 'hold appeared at frame 69 with no matching queue shift'), 2026-10-15; combo3/pieces/fr_h011p1_968.10.png, combo3/advise/holdchk.py"),
 ('i015', 'p1', 'pieces', '69', "video frames: A's three gap windows 1560.37-1587.63, 1587.63-1609.9, 1609.9-1623.8 hold exactly three locks (I 1587.0 +900, I 1609.0 +1050, Z hard drop 1623.7 +40); the pieces resting on the floor at 1570-1575.8 and 1620-1623.2 leave by hold swap, not lock; B's 2 locks + 15 pace-estimated gap pieces spliced by R/build.py:64-75 double-count A's intervals; 69 = A's own count, 2026-10-15; combo3/advise/fr_i015p1_1560.00.png, fr_i015bp1_1593.00.png, fr_i015zp1_1575.40.png, fr_i015z2p1_1622.40.png"),
 ('i017', 'p1', 'pieces', '233', "video frames: A's three gap windows 1907.8-1919.83, 1919.83-1926.13, 1926.13-1934.6 hold exactly one lock each (O 1919.0 +900, I 1925.5 +1050, L 1934.0 +1802), score flat and no second piece on the board while each rests on the stack; B's 3 locks + 3 pace-estimated gap pieces spliced by R/build.py:64-75 double-count A's intervals; 233 = A's own count; at the KO edge the Z of A's 2018.97 interval locks by 2019.650, before K 2019.8, and the next O hard-drops at 2019.833, after K, 2026-10-15; combo3/advise/fr_i017p1_1907.00.png, fr_i017k30p1_2019.50.png, bd_adv_i017_ko.txt, combo/tie/verdicts.csv"),
]
for g, v, sheet in [('h004', '449.4', 'start/sheets/h004.png GO streak 449.4; start/go_res.json'),
                    ('h006', '605.9', 'start/sheets/h006.png; start/six_gridn.txt'),
                    ('h017', '1469.9', 'start/sheets/h017.png; start/six_gridn.txt'),
                    ('g060', '984.3', 'start/sheets/g060.png GO streak 984.3'),
                    ('g083', '3032.3', 'start/sheets/g083.png; start/six_gridn.txt'),
                    ('g086', '3231.3', 'start/sheets/g086.png (excluded game; edited so the pair and the link stay consistent)')]:
    for p in ('p1', 'p2'):
        new.append((g, p, 'start_s', v, f'{ST}; combo3/{sheet}'))
keys = {(e['id'], e['player'], e['field']) for e in old}
edits = list(old)
for g, p, f, v, src in new:
    assert (g, p, f) not in keys, ('overlap with existing edit', g, p, f)
    w = at[(g, p)][f]
    edits.append(dict(id=g, player=p, field=f, was=w, value=v, source=src))
    print('NEW', g, p, f, w, '->', v)
assert len(edits) == 74
apply_hand_edits(rows, edits)
with open(f'{D}/fin/hand-edits.csv', 'w', encoding='utf-8', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=['id', 'player', 'field', 'was', 'value', 'source'], lineterminator='\n'); w.writeheader(); w.writerows(edits)
with open(f'{D}/fin/games.csv', 'w', encoding='utf-8', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=cols, lineterminator='\n'); w.writeheader(); w.writerows(rows)
fin = {(r['id'], r['player']): r for r in csv.DictReader(open(f'{D}/fin/games.csv', encoding='utf-8', newline=''))}
assert all(fin[(e['id'], e['player'])][e['field']] == e['value'] for e in edits)
print('edits', len(edits))
