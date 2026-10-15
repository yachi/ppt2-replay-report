# usage: check_applied.py <mirror> <corrections.json>  raise unless every correction was applied exactly once across the
# four sets (catches an id that is in no set, which the per-set check cannot see).
import json, glob, sys
A = [x for f in sorted(glob.glob(f'{sys.argv[1]}/*/w/tetrio/overlay_applied.json')) for x in json.load(open(f))]
C = json.load(open(sys.argv[2]))
got = sorted(a['index'] for a in A)
assert got == list(range(len(C))), ('applied', got, 'of', len(C))
print('all', len(C), 'corrections applied once')
