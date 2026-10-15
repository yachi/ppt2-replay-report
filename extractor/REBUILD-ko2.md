# Rebuilding games.csv with FIX 1 (find_end refine) + FIX 2 (slot-5 re-read)

All commands run from `/private/tmp/claude-501/sk/endfix/ko2/rerun` (bash). Every step writes only under this dir.
Inputs read (never written): `endfix/rebuild/run` (committed-chain mirror), `endfix/fixA/{analyze_fix.py,endfix_a.py,fix/}`,
`ko2/find_end/{analyze_ko2.py,endfix_a.py,run.py}`, `ko2/flash_miss/{analyze_ko2.py,regen_ev.py}`, `sk/metrics/**` (A feature files).

## 0. Files in this dir

| file | what |
|---|---|
| `analyze_merged.py` | `ko2/find_end/analyze_ko2.py` with `spawns()` replaced by `ko2/flash_miss/analyze_ko2.py`'s. `diff fixA/analyze_fix.py analyze_merged.py` = FIX 1 hunk + FIX 2 hunk, nothing else (`merged.diff`, `f1.diff`, `f2.diff`) |
| `endfix_a.py` | copy of `ko2/find_end/endfix_a.py` (Y fallback, refined) |
| `run.py` | copy of `ko2/find_end/run.py` (reruns A over all 210 games) |
| `regen_ev.py` | copy of `ko2/flash_miss/regen_ev.py`; only change: `MODDIR` env selects where the module and `endfix_a` are imported from |
| `mkmirror.sh` | rsync copy of `rebuild/run` (symlinks kept); `fixed` excludes the four `*/w/A/analyze.py` symlinks and `Y/w/A/endfix_a.py`, so they can be written as regular files with no deletion |
| `patch_mirror.py` | writes `<S>/w/A/analyze.py` = the set's original analyze.py with `spawns()` and `find_end()` (+ `_detect`/`refine`/`KO_*`) from a module; `Y/w/A/endfix_a.py`; `<S>/w/A/games.jsonl` from a jsonl dir |
| `drive.sh` | byte-identical copy of `endfix/rebuild/drive.sh` (gaps → fusion → metrics → pool → build_games_csv) |
| `rowdiff.py` / `rowdiff.txt` | three-way row diff (control vs repo, fixed vs control, fixed vs repo) with attribution |

## 1. Control A: committed chain, no fixes

```bash
./mkmirror.sh run_ctrl
./drive.sh run_ctrl                    # ~12 s
md5 -q run_ctrl/games.csv              # c0cd326115ea6c18cfc84e2ef5087f70 (= endfix/rebuild/run/games.csv)
```

It does **not** equal the repo's `analysis/ppt2-syakegohan/games.csv` (md5 `9eb7a5eeb3cbeaee8c4d4df11c76b584`), and no
chain run can: the repo file is chain output plus a hand-edit layer from commit a67711b — 24 rows in 13 games
(opponent nameplates on g062 g071 g074 g086 g088 g090 g092 g094 g096 g101; h002 p1 attack/max_combo and i016 p1 from
video frames; j008 reason text). Expected control md5 is therefore `c0cd…`, not `9eb7…`.

## 2. Control B: the patch procedure with the UNFIXED module

```bash
mkdir -p ctrlproc && cp ../../fixA/analyze_fix.py ../../fixA/endfix_a.py ctrlproc/
./mkmirror.sh run_proc2 fixed
python3 patch_mirror.py run_proc2 ctrlproc/analyze_fix.py ctrlproc/endfix_a.py ../../fixA/fix
md5 -q run_proc2/*/w/A/analyze.py      # all 6c48513e… (= the original set analyze.py)
MODDIR=$PWD/ctrlproc python3 regen_ev.py analyze_fix run_proc2 --check   # "differing 0"
MODDIR=$PWD/ctrlproc python3 regen_ev.py analyze_fix run_proc2
./drive.sh run_proc2
md5 -q run_proc2/games.csv             # c0cd326115ea6c18cfc84e2ef5087f70
```

(`run_proc` is an earlier attempt whose region cut copied four harmless constants; superseded by `run_proc2`.)

## 3. Fixed build

```bash
python3 - <<'EOF'                      # analyze_merged.py
def fn(s,name):
    a=s.index(f'def {name}('); b=s.index('\ndef ',a+5); return a,b
k=open('../find_end/analyze_ko2.py').read(); f=open('../flash_miss/analyze_ko2.py').read()
a,b=fn(k,'spawns'); na,nb=fn(f,'spawns')
open('analyze_merged.py','w').write(k[:a]+f[na:nb]+k[b:])
EOF
cp ../find_end/endfix_a.py endfix_a.py
cp ../find_end/run.py run.py
python3 run.py analyze_merged out      # ~8 s; out/games_{B,Y,lg,cVO}.jsonl + ev_*.pkl
./mkmirror.sh run fixed
python3 patch_mirror.py run $PWD/analyze_merged.py $PWD/endfix_a.py out
MODDIR=$PWD python3 regen_ev.py analyze_merged run   # rewrites A half of R/ev (Y: R/ev_endfix), keeps B half
./drive.sh run
md5 -q run/games.csv                   # 89d6f3ea7a342f862efdf59578caf499
python3 rowdiff.py > rowdiff.txt
```

Extractor B is not rerun: neither fix touches it (regen_ev keeps `b`/`bo`).

## 4. Result

fixed vs control: 68 rows in 52 games, all attributed — FIX 1: 32 rows in 17 games; FIX 2: 36 rows in 35 games;
0 unexplained. Every FIX 2 row equals `ko2/flash_miss/run_fix/games.csv` (FIX 2 alone). No change to won, excluded,
reason, opener or who. fixed vs repo: 83 rows in 57 games = (hand layer, 24 rows) ∪ (fix rows, 68), overlap 9 rows.
Details in `rowdiff.txt`.

## 5. Scope check: find_end in the mirror's A/analyze.py

`patch_mirror.py` also puts FIX 1's `find_end` into the mirror's `A/analyze.py`, which `R/gapchk.py` / `R/bagchk.py`
import (FIX 2's own patch swapped only `spawns`). `gaps.json` / `bag.json` do change for FIX 1 games (each tail grows by
the refined frames, e.g. g060 p1 0.20 → 0.63 s, far below GAPMIN 4 s). Counterfactual, mirror keeps the original
`find_end` (FIX 2 spawns only), same A outputs:

```bash
./mkmirror.sh run_alt fixed
python3 patch_mirror.py run_alt ../flash_miss/analyze_ko2.py ../../fixA/endfix_a.py out
MODDIR=$PWD python3 regen_ev.py analyze_merged run_alt
./drive.sh run_alt
cmp run_alt/games.csv run/games.csv    # identical: the choice is inert for games.csv
```
