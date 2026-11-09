cd /tmp/claude-0/xk/won/chain/am/w
for k in 0 1 2; do python3 B/sample.py $(cat /tmp/claude-0/xk/ids$k) > B/sample$k.log 2>&1 & done; wait
rm -f B/games.jsonl.part*
for k in 0 1 2; do python3 B/runner.py B/out$k.jsonl $(cat /tmp/claude-0/xk/ids$k) > B/run$k.log 2>&1 & done; wait
echo BDONE > B/done.txt
