#!/bin/bash
# [r6] re-run after the B border-end fix: B solve (cells2 kept), R stage, then drive_c minus banscan (kept)
set -e
W=/tmp/claude-0/r6/w/chain/r6/w; cd $W; export PYTHONDONTWRITEBYTECODE=1
IDS=$(python3 -c "import json;print(' '.join(g['id'] for g in json.load(open('../games.json'))))")
rm -f B/games.jsonl B/shard/*.jsonl R/ev/*.pkl R/pcban/*.json
(cd B && echo $IDS | tr ' ' '\n' | xargs -P 4 -I{} sh -c '[ -s shard/{}.jsonl ] || python3 runner.py shard/{}.jsonl {}' > runner.out 2>&1)
for g in $IDS; do cat B/shard/$g.jsonl; done > B/games.jsonl
echo $IDS | tr ' ' '\n' | xargs -P 4 -n 1 python3 R/evrun.py > R/evrun.out 2>&1
python3 R/gapchk.py > R/gapchk.out 2>&1
python3 R/bagchk.py > R/bagchk.out 2>&1
python3 R/part.py > R/part.out 2>&1
echo STAGE2_DONE
bash ../drive_c.sh r6
