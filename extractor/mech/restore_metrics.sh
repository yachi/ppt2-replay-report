#!/bin/bash
# usage: restore_metrics.sh <mirror>  overwrite the mirror's four tetrio/metrics.py with the renx 'fixed' build's
# (combo/rerun/fixed) and repoint Y's hardcoded output path at the mirror. Overwrite only; nothing is deleted.
set -e
R=$(cd $1 && pwd); SRC=/private/tmp/claude-501/sk/endfix/combo/rerun/fixed
for s in B Y lg cVO; do cp $SRC/$s/w/tetrio/metrics.py $R/$s/w/tetrio/metrics.py; done
sed -i '' "s#$SRC#$R#g" $R/Y/w/tetrio/metrics.py
! grep -rn "$SRC" $R --include='*.py'
echo restored $R
