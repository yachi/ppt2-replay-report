#!/bin/bash
# drive.sh <set>  — the archived chain, in order: A features+events, B cells+solve, R events/gaps/bags/part/banners/fusion/build, tetrio metrics
# [uP port] paths -> /tmp/claude-0/xo/w/chain/$1/w; every per-game step runs as a 9-process pool (xargs -P 4),
# one pool at a time; pcscan ids come from games.json instead of TJc's literal k000..k063 list (R/pcon.py globs R/pcban/*.json).
set -e
W=/tmp/claude-0/xo/w/chain/$1/w; cd $W; export PYTHONDONTWRITEBYTECODE=1
IDS=$(python3 -c "import json;print(' '.join(g['id'] for g in json.load(open('../games.json'))))")
mkdir -p A/feat B/cells2 R/ev R/ban R/pcban B/shard
[ -f A/games.jsonl ] || python3 A/run_all.py > A/run_all.out 2>&1          # ThreadPoolExecutor(9) of feat.py subprocesses
echo $IDS | tr ' ' '\n' | xargs -P 4 -n 1 python3 B/sample.py > B/sample.out 2>&1
if [ ! -f B/games.jsonl ]; then
  (cd B && echo $IDS | tr ' ' '\n' | xargs -P 4 -I{} sh -c '[ -s shard/{}.jsonl ] || python3 runner.py shard/{}.jsonl {}' > runner.out 2>&1)
  for g in $IDS; do cat B/shard/$g.jsonl; done > B/games.jsonl                  # games.json order, as the serial runner wrote it
fi
for g in $IDS; do [ -f R/ev/$g.pkl ] || echo $g; done | xargs -P 4 -n 1 python3 R/evrun.py > R/evrun.out 2>&1
python3 R/gapchk.py > R/gapchk.out 2>&1
python3 R/bagchk.py > R/bagchk.out 2>&1
python3 R/part.py > R/part.out 2>&1
for g in $IDS; do [ -f R/ban/$g.npz ] || echo $g; done | xargs -P 4 -n 1 python3 R/banscan.py > R/banscan.out 2>&1
python3 R/kofinal.py > R/kofinal.out 2>&1   # port addition: the winner's last piece at the KO (README)
python3 R/fuse.py > R/fuse.out 2>&1
python3 R/build.py > R/build.out 2>&1
python3 tetrio/seqs.py > tetrio/seqs.out 2>&1
echo $IDS | tr ' ' '\n' | xargs -P 2 -n 10 python3 R/pcscan.py > R/pcscan.out 2>&1   # PC banners; candidates checked by eye (check/pcsheet.py)
python3 R/pcmap.py > ../pcmap.out            # writes ../pcdec.json, pasted into tetrio/metrics.py PCDEC (TJc's table must be replaced)
python3 tetrio/metrics.py > tetrio/metrics.out 2>&1
echo DONE; tail -3 tetrio/metrics.out
