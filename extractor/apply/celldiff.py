import csv,sys
def rd(p):
    with open(p,encoding='utf-8',newline='') as f: r=csv.DictReader(f); return r.fieldnames,[x for x in r]
ca,a=rd(sys.argv[1]); cb,b=rd(sys.argv[2]); assert ca==cb and len(a)==len(b)
for x,y in zip(a,b):
    assert (x['id'],x['player'])==(y['id'],y['player'])
    for k in ca:
        if x[k]!=y[k]: print(x['id'],x['player'],k,x[k],'->',y[k])
