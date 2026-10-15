# Reconciliation patch (YbMeCRhjG1k): B's border_end misfires mid-game on this stream (13 of 34 games end
# >1.5 s before A's KO). Wrapper: when B's own end is >1.5 s (45 frames) before A's KO frame, replace it by A's
# KO frame for A's loser. A's KO agrees with the independent winners file on all 34 games (0.0-0.4 s).
import json
A = {j['start_s']: j for j in map(json.loads, open('/private/tmp/claude-501/sk/metrics/more/Y/A/games.jsonl'))}
G = {g['start_s']: g for g in json.load(open('/private/tmp/claude-501/sk/metrics/more/games_YbMeCRhjG1k.json'))}
FORCED = []
def install(Bm):
    orig = Bm.border_end
    def border_end(z, start, end_upper, t0):
        res, match = orig(z, start, end_upper, t0)
        g = G[start]; a = [x for x in A.values() if x['id'] == g['id']][0]
        fa = int(round((a['end_s'] - t0) * Bm.FPS)); loser = 0 if a['winner'] == 'p2' else 1
        cand = [f for f in res.values() if f is not None]
        if not cand or min(cand) < fa - 45:
            FORCED.append(g['id']); return {loser: fa, 1 - loser: None}, match
        return res, match
    Bm.border_end = border_end
