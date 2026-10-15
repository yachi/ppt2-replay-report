import json, sys, time
import extract_b as X, endfix
endfix.install(X)
out = sys.argv[1]; ids = sys.argv[2:]
games = {g['id']: g for g in json.load(open('/private/tmp/claude-501/sk/metrics/more/games_YbMeCRhjG1k.json'))}
for gid in ids:
    t = time.time(); rec = X.run_game(games[gid])[0]
    rec['notes'] = (rec['notes'] + '; ' if rec['notes'] else '') + ('end forced to A KO frame' if gid in endfix.FORCED else 'own end')
    with open(out, 'a') as f: f.write(json.dumps(rec) + '\n')
    print(gid, round(time.time() - t, 1), gid in endfix.FORCED, flush=True)
