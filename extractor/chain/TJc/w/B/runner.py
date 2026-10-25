import json, sys, traceback, time
import extract_b as X
out = sys.argv[1]; ids = sys.argv[2:]
games = {g['id']: g for g in json.load(open('/tmp/claude-0/chain/kbb/games.json'))}
for gid in ids:
    t = time.time()
    try:
        rec = X.run_game(games[gid])[0]
    except Exception as e:
        rec = dict(id=gid, p1=None, p2=None, duration_s=None, winner=None, confidence=0.0,
                   notes='not measured: ' + repr(e)[:300])
    with open(out, 'a') as f: f.write(json.dumps(rec) + '\n')
    print(gid, round(time.time() - t, 1), flush=True)
