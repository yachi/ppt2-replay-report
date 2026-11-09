cd /tmp/claude-0/qh/w/chain/qh
python3 -c "import json;print(' '.join(g['id'] for g in json.load(open('games.json'))))" | tr ' ' '\n' | xargs -P 4 -n 4 python3 check/ocr/ocr_game.py > ocr_all.out 2>&1
echo OCR_DONE >> ocr_all.out
