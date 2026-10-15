# usage: rowdiff.py <base.csv> <new.csv>  per-row cell diff keyed (id, player)
import csv, sys
a = {(r['id'], r['player']): r for r in csv.DictReader(open(sys.argv[1], encoding='utf-8'))}
b = {(r['id'], r['player']): r for r in csv.DictReader(open(sys.argv[2], encoding='utf-8'))}
assert a.keys() == b.keys()
n = 0
for k in sorted(a):
    d = [(f, a[k][f], b[k][f]) for f in a[k] if a[k][f] != b[k][f]]
    if d: n += 1; print(k[0], k[1], ' '.join(f'{f} {x}->{y}' for f, x, y in d))
print('rows changed', n)
