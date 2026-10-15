#!/bin/bash
# usage: build.sh <name> <corrections.json>   mirror = combo/rerun/fixed + renx metrics + overlay2, metrics-only rerun
set -e
A=/private/tmp/claude-501/sk/endfix/combo3/apply; M=/private/tmp/claude-501/sk/endfix/combo2/mech
X=$A/$1
rsync -a /private/tmp/claude-501/sk/endfix/combo/rerun/fixed/ $X/
$M/restore_metrics.sh $X
sed -i '' "s#^M = .*#M = '$X/B/w'#; s#^OUT = .*#OUT = '$X/pool'#" $X/pool/pool.py
if grep -rln /private/tmp/claude-501/sk/endfix/combo/rerun/fixed $X --include='*.py'; then echo STRAY PATH; exit 1; fi
python3 $A/patch_overlay3.py $X $2
$M/drive_metrics.sh $X
python3 $M/check_applied.py $X $2
