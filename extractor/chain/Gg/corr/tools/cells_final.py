# final hand edits: skeptic-kept cell edits, piece counts replaced by the whole-game NEXT-queue count where it ran
import json, csv
CSV = {(r['id'], r['player']): r for r in csv.DictReader(open('/private/tmp/claude-501/Gg/out/chain_games.csv'))}
cells = json.load(open('cells.json'))['cells']
NC = {(x['id'], x['player']): x for x in json.load(open('out/pieces.json'))}
NC_SRC = 'whole-game NEXT-queue count (corr/tools/nextcount.py: every shift read, 7-bag consistent; minus the first hold into an empty box, minus a last piece not locked by the KO): '
MINE = {('y009', 'p1'): (94, '96 NEXT shifts, minus the first hold (757.60 L) and the last piece (spawn 810.96, p1 score frozen at 54147 to the KO 811.7) = 94; chain events at 777.1 and 810.83 have no shift'),
        ('y043', 'p1'): (65, '66 NEXT shifts, minus the first hold (2785.26 Z) = 65; the last piece (spawn 2816.50) locks as the TSD at 2816.70 (+3600) before the KO 2817.0; chain events 2804.5 twice at one time'),
        ('y006', 'p2'): (130, 'NEXT shifts 132 minus the first hold (522.90 T) = 131, less the last piece = 130: the shifts at 531.70 and 538.14 are real spawns (plain locks), so removing those two clears does not remove pieces; the earlier 129 edit is dropped'),
        ('y037', 'p2'): (42, '44 NEXT shifts minus the first hold (2483.27 S) and the last piece (spawn 2501.87, KO 2501.97) = 42')}
out = []
for c in cells:
    k = (c['id'], c['player'])
    if c['field'] == 'pieces' and (k in NC or k in MINE): continue
    out.append(dict(id=c['id'], player=c['player'], field=c['field'], value=str(c['value']), source=c['source']))
for k, x in NC.items(): out.append(dict(id=k[0], player=k[1], field='pieces', value=str(x['value']), source=NC_SRC + x['source']))
for k, (v, s) in MINE.items(): out.append(dict(id=k[0], player=k[1], field='pieces', value=str(v), source='NEXT-queue count, checked against the score at the end: ' + s))
rows = []
for e in out:
    was = CSV[(e['id'], e['player'])][e['field']]
    if was == e['value']: continue
    rows.append(dict(id=e['id'], player=e['player'], field=e['field'], was=was, value=e['value'], source=e['source']))
rows.sort(key=lambda r: (r['id'], r['player'], r['field']))
w = csv.DictWriter(open('/home/user/ppt2-replay-report/analysis/ppt2-yuukun/hand-edits.csv', 'w', newline=''), fieldnames=['id', 'player', 'field', 'was', 'value', 'source'], lineterminator='\n')
w.writeheader(); w.writerows(rows)
for r in rows: print(r['id'], r['player'], r['field'], r['was'], '->', r['value'])
print(len(rows))
