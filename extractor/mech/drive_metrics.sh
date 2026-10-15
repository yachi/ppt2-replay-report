#!/bin/bash
# usage: drive_metrics.sh <mirror>   metrics-only rerun (the overlay changes only tetrio/metrics.py): metrics in B,lg,cVO,
# opp, cp, Y metrics, pool, games.csv. Same commands as combo/rerun/drive.sh minus the upstream fusion steps.
set -e
R=$(cd $1 && pwd); export PYTHONDONTWRITEBYTECODE=1
grep -q "^M = '$R/B/w'" $R/pool/pool.py && grep -q "^OUT = '$R/pool'" $R/pool/pool.py || { echo pool paths; exit 1; }
for s in B lg cVO; do (cd $R/$s/w && python3 tetrio/metrics.py > $s.metrics.py.out 2>&1) || { echo FAIL $s; tail $R/$s/w/$s.metrics.py.out; exit 1; }; done
(cd $R/B/w && python3 opp/opp_metrics.py > opp.out 2>&1)
cp $R/lg/w/metrics.csv $R/pool/rows_lgszEWNFSx0.csv; cp $R/cVO/w/metrics.csv $R/pool/rows_cVO2eGipjV0.csv
(cd $R/Y/w && python3 tetrio/metrics.py > Y.metrics.py.out 2>&1) || { echo FAIL Y; tail $R/Y/w/Y.metrics.py.out; exit 1; }
(cd $R/pool && python3 pool.py > pool.out 2>&1)
(cd /Users/yachi/github/tetrio-replay-report && python3 /private/tmp/claude-501/sk/endfix/discover/run/build_games_csv.py $R/pool/all_rows.csv $R/games.csv)
md5 -q $R/games.csv; wc -l < $R/games.csv
