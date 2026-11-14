"""Run a chain's corr/tools/nextcount.py with fastnc's locate/classify2/white. The chain's file is read, never
edited; its command line is unchanged:

    python3 run_nextcount.py [--check] [--tool PATH] p1|p2 T0 T1 --video ID [--dump]
    python3 run_nextcount.py [--check] [--tool PATH] --game GID p1

It refuses a nextcount.py whose replaced functions or their constants differ from the version fastnc was checked
against (fastnc.KNOWN), unless --force is given.

PATH defaults to corr/tools/nextcount.py under the current directory. --check also reads every frame with the
original functions and stops unless read_state() returns the same queue, hold and (dx, dy, score), exactly."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fastnc

args = sys.argv[1:]
check = '--check' in args; force = '--force' in args
args = [a for a in args if a not in ('--check', '--force')]
tool = 'corr/tools/nextcount.py'
if '--tool' in args:
    i = args.index('--tool'); tool = args[i + 1]; del args[i:i + 2]
sys.argv = [tool] + args
src = open(tool).read()
fp = fastnc.fingerprint(src)
if fp not in fastnc.KNOWN and not force:
    sys.exit(f'nextcount-fast: {tool} differs from the nextcount.py fastnc was checked against (fingerprint {fp}); '
             'run with --check --force and add the fingerprint to fastnc.KNOWN once it passes')
cut = src.index("if __name__ == '__main__' and sys.argv[1] != '--game':")
ns = {'__name__': '__main__', '__file__': tool}
exec(compile(src[:cut], tool, 'exec'), ns)
orig = fastnc.install(ns)
stats = {'frames': 0, 't_fast': 0.0, 't_orig': 0.0}

if check:
    read_fast = ns['read_state']   # the chain's read_state, now calling the fast helpers by name

    def read_state(fr, pl):
        t0 = time.perf_counter(); a = read_fast(fr, pl); stats['t_fast'] += time.perf_counter() - t0
        fast = {k: ns[k] for k in orig}
        ns.update(orig)
        try:
            t0 = time.perf_counter(); b = read_fast(fr, pl); stats['t_orig'] += time.perf_counter() - t0
        finally:
            ns.update(fast)
        stats['frames'] += 1
        if a != b:
            sys.exit(f'nextcount-fast MISMATCH frame {stats["frames"]} {pl}: fast={a} orig={b}')
        return a
    ns['read_state'] = read_state

exec(compile(src[cut:], tool, 'exec'), ns)
if check:
    print(f'nextcount-fast check: {stats["frames"]} frames identical, fast {stats["t_fast"]:.1f}s, '
          f'original {stats["t_orig"]:.1f}s', file=sys.stderr)
