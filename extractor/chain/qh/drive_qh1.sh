#!/bin/bash
# [qh] stage 1: A features, then drive_b.sh (B sample/solve, R evrun/gapchk/bagchk/part)
set -e
W=/tmp/claude-0/qh/w/chain/qh/w; cd $W; export PYTHONDONTWRITEBYTECODE=1
mkdir -p A/feat
[ -f A/games.jsonl ] || python3 A/run_all.py > A/run_all.out 2>&1
echo A_DONE
bash ../drive_b.sh qh
