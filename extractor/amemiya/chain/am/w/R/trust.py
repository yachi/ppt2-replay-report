# [am port, new file] R/unresolved.json = build.py's unres_pg (printed by R/build.py; recomputed here from reconciled notes)
# and R/not_trust.json = games whose reconciled winner disagrees with the on-screen WIN counter (games.json
# win_counter_at_start of the next game of the same set; the set's last game is decided by who reached 15).
import json
R={j['id']:j for j in map(json.loads,open('reconciled.jsonl'))}
G=json.load(open('../games.json')); ids=[g['id'] for g in G]; byid={g['id']:g for g in G}
unres=[f"{g}{p}" for g in R for p in ('p1','p2') if 'LOWER BOUNDS (unresolved)' in R[g][p]['notes']]
def truth(i):
    k=ids.index(i); g=byid[i]; a0,b0=map(int,g['win_counter_at_start'].split('-'))
    if k+1<len(ids) and ids[k+1] and byid[ids[k+1]]['opponent']==g['opponent'] and byid[ids[k+1]]['win_counter_at_start']!='0-0':
        a1,b1=map(int,byid[ids[k+1]]['win_counter_at_start'].split('-'))
        return 'p1' if (a1,b1)==(a0+1,b0) else 'p2' if (a1,b1)==(a0,b0+1) else None
    return 'p1' if a0==14 else 'p2' if b0==14 else None   # last game of an FT15 set: only a 14 can finish it
T={i:truth(i) for i in ids}
nt=[i for i in ids if T[i] is None or R[i]['winner']!=T[i]]
json.dump(unres,open('R/unresolved.json','w')); json.dump(nt,open('R/not_trust.json','w'))
json.dump(T,open('R/counter_winner.json','w'))
print('unresolved',unres,'not_trust',nt, 'counter-decided',sum(v is not None for v in T.values()))
