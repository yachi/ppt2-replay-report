#!/bin/bash
# [xt] NEXT-queue recount of every player-game, two at a time (frame-check agents share the 4 cores), resumable.
cd /tmp/claude-0/ms/corr/tools
python3 -c "import json;[print(g['id'],p) for g in json.load(open('/tmp/claude-0/ms/w/chain/ms/games.json')) for p in ('p1','p2')]" |
while read g p; do
  [ -s ../nc/${g}_$p.json ] && continue
  echo "$g $p"
done | xargs -P ${NCP:-2} -n 2 sh -c 'python3 nextcount.py --game $0 $1 > ../nc/$0_$1.json.tmp 2>../nc/$0_$1.err && mv ../nc/$0_$1.json.tmp ../nc/$0_$1.json'
echo DONE
