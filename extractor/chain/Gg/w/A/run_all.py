"""Run extractor A over all games: feature dump (2 workers = 2 ffmpeg + 2 python processes), then event analysis."""
import json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze as A

games = json.load(open('/private/tmp/claude-501/Gg/w/chain/yu/games.json'))
FD = os.path.join(HERE, 'feat'); os.makedirs(FD, exist_ok=True)
PROG = os.path.join(HERE, 'progress.txt')
done = [0]

def dur(path, cache={}):
    if path not in cache:
        cache[path] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                                           capture_output=True, text=True).stdout.strip())
    return cache[path]

def one(g):
    out = os.path.join(FD, g['id'] + '.npz')
    if not os.path.exists(out):
        t0 = max(0.0, g['start_s'] - 1.5)
        t1 = min(dur(g['path']), g['end_upper_s'] + 0.5)
        try:
            subprocess.run([sys.executable, os.path.join(HERE, 'feat.py'), g['path'], f'{t0:.3f}', f'{t1:.3f}', out],
                           check=True, capture_output=True)
        except Exception as e:
            with open(PROG, 'a') as f:
                f.write(f'feat FAILED {g["id"]}: {e}\n')
    done[0] += 1
    with open(PROG, 'a') as f:
        f.write(f'{time.strftime("%H:%M:%S")} feat {done[0]}/{len(games)} {g["id"]}\n')

def ana(g):   # [uP run] same body as the archived serial loop, one game per call
    try:
        r = A.analyse(os.path.join(FD, g['id'] + '.npz'), g)
    except Exception as e:  # never drop a game silently
        r = dict(id=g['id'], p1=None, p2=None, duration_s=None, winner=None, confidence=0,
                 notes=f'analysis failed: {type(e).__name__}: {e}')
    for k in ('p1', 'p2'):
        if r.get(k):
            for x in ('_events', '_seq', '_hold_empty'):
                r[k].pop(x, None)
    return r

if __name__ == '__main__':   # [uP run] guard: the analyse stage uses a spawn process pool
  for g in games:
    dur(g['path'])
  with ThreadPoolExecutor(4) as ex:   # [uP port: was 2; 9 ffmpeg+feat subprocesses]
    list(ex.map(one, games))
  T1 = time.time()
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(4) as ex:  # [uP run] analyse() was a serial loop; 9 processes, results kept in games.json order
    rows = list(ex.map(ana, games))
  with open(PROG, 'a') as f:
    f.write(f'{time.strftime("%H:%M:%S")} analyse {len(rows)}/{len(games)} pool9 {time.time()-T1:.1f}s\n')
  with open(os.path.join(HERE, 'games.jsonl'), 'w') as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
  with open(PROG, 'a') as f:
    f.write('DONE\n')
