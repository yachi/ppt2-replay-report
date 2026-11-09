set -x
cd /tmp/claude-0/xk/won/chain/am/w
until [ -f B/done.txt ]; do sleep 20; done
python3 - <<'P'
import json
rows={}
for k in range(3):
    for l in open(f'B/out{k}.jsonl'): j=json.loads(l); rows[j['id']]=j
ids=[g['id'] for g in json.load(open('../games.json'))]
with open('B/games.jsonl','w') as f:
    for i in ids: f.write(json.dumps(rows[i])+'\n')
P
python3 R/part.py > R/part.log 2>&1
mkdir -p R/ev R/ban R/pc
for k in 0 1 2; do python3 R/evrun.py $(cat /tmp/claude-0/xk/ids$k) > R/evrun$k.log 2>&1 & done; wait
for k in 0 1 2; do python3 R/banscan.py $(cat /tmp/claude-0/xk/ids$k) > R/ban$k.log 2>&1 & done; wait
python3 R/fuse.py > R/fuse.log 2>&1
python3 R/gapchk.py > R/gapchk.log 2>&1
python3 R/bagchk.py > R/bagchk.log 2>&1
python3 R/build.py > R/build.log 2>&1
python3 tetrio/seqs.py > tetrio/seqs.log 2>&1
echo RDONE1 > R/done1.txt
P2=$(python3 -c "
import json;g=json.load(open('../games.json'));g.sort(key=lambda x:x['start_s']-x['end_upper_s'])
print(' '.join(x['id'] for x in g[0::2]))")
P3=$(python3 -c "
import json;g=json.load(open('../games.json'));g.sort(key=lambda x:x['start_s']-x['end_upper_s'])
print(' '.join(x['id'] for x in g[1::2]))")
python3 R/pcscan.py $P2 > R/pc0.log 2>&1 &
python3 R/pcscan.py $P3 > R/pc1.log 2>&1 &
wait
echo RDONE2 > R/done2.txt
