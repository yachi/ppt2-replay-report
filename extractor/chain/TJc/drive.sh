#!/bin/bash
# drive.sh <set>  — the archived chain, in order: A features+events, B cells+solve, R events/gaps/bags/part/banners/fusion/build, tetrio metrics
set -e
W=/tmp/claude-0/chain/$1/w; cd $W; export PYTHONDONTWRITEBYTECODE=1
IDS=$(python3 -c "import json;print(' '.join(g['id'] for g in json.load(open('../games.json'))))")
mkdir -p A/feat B/cells2 R/ev R/ban R/pcban
[ -f A/games.jsonl ] || python3 A/run_all.py > A/run_all.out 2>&1
for g in $IDS; do python3 B/sample.py $g; done > B/sample.out 2>&1
[ -f B/games.jsonl ] || (cd B && python3 runner.py games.jsonl $IDS > runner.out 2>&1)
python3 R/evrun.py $(for g in $IDS; do [ -f R/ev/$g.pkl ] || echo $g; done) > R/evrun.out 2>&1
python3 R/gapchk.py > R/gapchk.out 2>&1
python3 R/bagchk.py > R/bagchk.out 2>&1
python3 R/part.py > R/part.out 2>&1
python3 R/banscan.py $(for g in $IDS; do [ -f R/ban/$g.npz ] || echo $g; done) > R/banscan.out 2>&1
python3 R/kofinal.py > R/kofinal.out 2>&1   # port addition: the winner's last piece at the KO (README)
python3 R/fuse.py > R/fuse.out 2>&1
python3 R/build.py > R/build.out 2>&1
python3 tetrio/seqs.py > tetrio/seqs.out 2>&1
python3 R/pcscan.py k000 ... k031; python3 R/pcscan.py k032 ... k063   # PC banners; candidates checked by eye (check/pcsheet.py)
python3 R/pcmap.py > ../pcmap.out            # writes ../pcdec.json, pasted into tetrio/metrics.py PCDEC
python3 tetrio/metrics.py > tetrio/metrics.out 2>&1
echo DONE; tail -3 tetrio/metrics.out
