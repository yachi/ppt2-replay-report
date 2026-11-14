#!/bin/bash
# [pp] stage 2b: banners, KO, fusion, build, seqs, PC scan/map, metrics (drive.sh's tail)
set -e
W=/tmp/claude-0/yk/w/chain/yk/w; cd $W; export PYTHONDONTWRITEBYTECODE=1
IDS=$(python3 -c "import json;print(' '.join(g['id'] for g in json.load(open('../games.json'))))")
mkdir -p R/ban R/pcban
for g in $IDS; do [ -f R/ban/$g.npz ] || echo $g; done | xargs -r -P 3 -n 1 python3 R/banscan.py > R/banscan.out 2>&1
echo BANSCAN_DONE
python3 R/kofinal.py > R/kofinal.out 2>&1
python3 R/fuse.py > R/fuse.out 2>&1
python3 R/build.py > R/build.out 2>&1
python3 tetrio/seqs.py > tetrio/seqs.out 2>&1
echo BUILD_DONE
echo $IDS | tr ' ' '\n' | xargs -P 2 -n 10 python3 R/pcscan.py > R/pcscan.out 2>&1
python3 R/pcmap.py > ../pcmap.out
python3 tetrio/metrics.py > tetrio/metrics.out 2>&1
echo DONE; tail -3 tetrio/metrics.out
