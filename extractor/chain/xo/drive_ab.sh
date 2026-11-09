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
echo AB_DONE
