#!/bin/bash
# [r6] score OCR for every game (check/ocr/ocr_game.py, copied to /tmp/claude-0/r6/w/ocrall), after drive_c.sh
cd /tmp/claude-0/r6/w/ocrall
IDS=$(python3 -c "import json;print(' '.join(g['id'] for g in json.load(open('/tmp/claude-0/r6/w/chain/r6/games.json'))))")
for g in $IDS; do [ -f $g.json ] || echo $g; done | xargs -P 4 -n 1 python3 ocr_game.py > ocr.out 2>&1
echo OCR_DONE
