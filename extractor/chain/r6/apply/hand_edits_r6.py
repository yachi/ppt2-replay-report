# [r6, new file] corr/cells.json -> rows for analysis/ppt2-syakegohan/hand-edits.csv. A cell the corrected event list
# already gives (metrics recomputes REN and B2B maxima) is dropped; where the corrected event list moved a REN or B2B
# maximum under the edit, `was` is set to the chain's new value (the frame-read `value` is kept). Usage:
#   python3 hand_edits_r6.py <chain games.csv> >> analysis/ppt2-syakegohan/hand-edits.csv
import csv, json, sys
R = {(r['id'], r['player']): r for r in csv.DictReader(open(sys.argv[1]))}
w = csv.writer(sys.stdout, lineterminator='\n')
for c in json.load(open('/tmp/claude-0/r6/corr/cells.json'))['cells']:
    now = R[(c['id'], c['player'])][c['field']]
    if now == str(c['value']):
        print('chain already gives', c['id'], c['player'], c['field'], now, file=sys.stderr); continue
    was = str(c['was'])
    if now != was:
        assert c['field'] in ('max_combo', 'max_b2b'), c
        print('chain moved', c['id'], c['player'], c['field'], was, '->', now, file=sys.stderr); was = now
    w.writerow([c['id'], c['player'], c['field'], was, c['value'], c['source']])
