import pickle,sys
F='/private/tmp/claude-501/sk/endfix/combo/rerun/fixed'
Q=[('j009','p1',2237.8),('j027','p1',4277.6),('g070','p1',1716.1),('g070','p1',1716.47),('j033','p2',4846.67),('j033','p2',4846.45),('g042','p1',268.17),('i015','p1',1560.37),('i015','p1',1560.6),('g007','p1',1496.0)]
for s in 'B Y lg cVO'.split():
    S=pickle.load(open(f'{F}/{s}/w/tetrio/seqs.pkl','rb'))
    for g,p,t in Q:
        if (g,p) in S:
            seq=S[(g,p)]['seq']
            near=[z for z in seq if abs(z[0]-t)<=1.2]
            print(s,g,p,t,'->',near)
