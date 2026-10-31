import sys,json,pickle
ids=sys.argv[1:]
exec(open('R/evmatch.py').read())
for gid in ids:
  a,s,e=a_run(gid)
  b,o=b_clears(gid)
  pickle.dump(dict(a=a,a_start=s,a_end=e,b=b,bo=o),open(f'R/ev/{gid}.pkl','wb'))
  print('done',gid,flush=True)
