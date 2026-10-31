#!/bin/bash
# [r6] NEXT-queue recount of every player-game, three at a time (4-core container), resumable.
cd /tmp/claude-0/r6/corr/tools
python3 -c "import json;[print(g['id'],p) for g in json.load(open('/tmp/claude-0/r6/w/chain/r6/games.json')) for p in ('p1','p2')]" |
while read g p; do
  [ -s ../nc/${g}_$p.json ] && continue
  echo "$g $p"
done | xargs -P 3 -n 2 sh -c 'python3 nextcount.py --game $0 $1 > ../nc/$0_$1.json.tmp 2>../nc/$0_$1.err && mv ../nc/$0_$1.json.tmp ../nc/$0_$1.json'
echo DONE
