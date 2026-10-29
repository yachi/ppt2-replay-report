# How a stream extraction is parallelised

This is how the `uP3FeprmAGI` stream (`chain/uP`, 84 games, 5665 s of video) was extracted and checked. It
has two levels: process pools on one machine for the chain, and Claude Code workflows for the frame checks.
Copy both for the next player or video. Every number here comes from the run's own notes: `chain/uP/README.md`,
`chain/uP/drive.sh` and the work-tree files `w/TIMES.md`, `w/PREFLIGHT.md` and `out/REPORT.md` (under
`/private/tmp/claude-501/uP/`, not committed), plus the workflow scripts as they ran
(`chain/uP/workflows/round1.js`, `round2-score.js`) and their run journals (not committed).

## 1. Preflight, before any full run

Run the preflight as its own agent. The workflow stops if it returns `ok=false`, and nothing else runs.

- **Geometry gate.** Decode six frames from six games with the chain's constants, then compare each with the
  frame image. Check cells, garbage, the clear flash, NEXT, HOLD, borders and the nameplates. For `uP` the
  TJc constants passed unchanged. Recalibrate only if this gate fails.
- **Segmentation.** Run the segmenter over the whole video (see 2.3), then the menu filter. This gave
  100 segments, then 85 games.
- **Starts and winners.** Each start must be GO, not READY (defect D5). Read the right nameplate on every
  game. Read the WIN counter by eye at start+3 s: all 72 in-set transitions were +1 on exactly one side, with
  0 disagreements with `winner.py`. Read the five 4-4 finals on their KO frames.
- **Do not run extractors A and B on any whole game yet.** Drop or mark a broken game in `games.json`
  during preflight, not only in the notes. Preflight noted that l084 has no KO but left it in `games.json`,
  so `R/part.py` still crashed with rc=1 in the full run.

## 2. Process level: one machine, 11 cores

### 2.1 Rules

| rule | why |
|---|---|
| every per-game step runs as a pool of **9 workers** | the brief's rule for the 11-core machine. It leaves 2 cores free. The brief does not record why |
| **one pool at a time** | each worker already runs ffmpeg plus python (A's docstring: "2 workers = 2 ffmpeg + 2 python processes"), so two pools would likely oversubscribe the cores. The brief states the rule but not the reason |
| the output is **built to equal a serial run** | the same per-game code, with shards joined in `games.json` order (2.2). No serial run was compared |
| the expensive per-game steps **skip finished games** | a rerun resumes rather than starting over (2.4). `pcscan` and the serial steps always rerun |
| cheap or cross-game steps **stay serial** | they read every game at once, and together they took about 7 s |

### 2.2 Per-game sharding (`drive.sh`)

- `xargs -P 9 -n 1` over the game ids from `games.json`. This applies to B `sample.py`, R `evrun.py` and
  R `banscan.py`. `pcscan.py` takes 10 ids per process (`-n 10`).
- B `runner.py` appends rows to its output file. So each game writes its own shard, `B/shard/<id>.jsonl`.
  Those shards are then joined in `games.json` order into `B/games.jsonl`, "as the serial runner wrote it".
- A `run_all.py`: the feature dump uses `ThreadPoolExecutor(9)` of `feat.py` subprocesses (it was 2).
  `analyse()` was a serial loop and is now `ProcessPoolExecutor(9)` under a `__main__` guard.
  `ex.map` returns results in input order, so `games.jsonl` keeps the order of `games.json`. A failed game
  becomes a row that says so. It is never dropped.
- The KO-tail score reader used 9 workers, over each game's window from start-1 to A's end + 1.5 s.

### 2.3 Time shards for the segmenter (`seg/occ_shard.py`, `seg/par.py`)

- The segmenter is not per game: it finds the games. So the 5665 s video is cut into 9 time shards
  instead. Each shard runs `occ_shard.py VIDEO T0 DUR OUT.npz`, which samples at 10 fps and stores absolute
  times. `seg/merge.py` keeps `[i*630, (i+1)*630)` s from shard i, asserts one continuous 0.1 s grid
  (`np.diff(t) == 0.1`), then runs `seg.games()` unchanged. Wall time was 41 s. The launch command was not
  saved. An equivalent is
  `seq 0 8 | xargs -P 9 -I{} sh -c 'python3 occ_shard.py VIDEO $(({}*630)) 631 shard{}.npz'`.
- `par.py` runs the menu-filter brightness check and the WIN-counter crops in a `multiprocessing.Pool(9)`.
  The archived scripts loop over games serially.

### 2.4 Resume guards

| step | skipped when |
|---|---|
| A `run_all.py` | `A/games.jsonl` exists; per game, `A/feat/<id>.npz` exists |
| B `sample.py` | per game, `<id>.npz` exists (`w/B/sample.py:43`) |
| B runner | `B/games.jsonl` exists; per game, `B/shard/<id>.jsonl` is non-empty (this guard also stops doubled rows) |
| R evrun / banscan | `R/ev/<id>.pkl` / `R/ban/<id>.npz` exists (only the missing ids go to `xargs`) |

### 2.5 Measured wall time (`w/TIMES.md`)

| step | workers | wall |
|---|---|---|
| A run_all (feat + analyse) | 9 + 9 | 111 s |
| B sample | 9 | 85 s |
| B runner (one shard per game) | 9 | 8 s |
| R evrun | 9 | 8 s |
| R banscan (Mini template re-cut) | 9 | 469 s |
| R pcscan | 9 | 82 s |
| KO-tail score reader | 9 | 67 s |
| gapchk, bagchk, part, kofinal, fuse, build, seqs, pcmap, metrics (incl. the l084 rerun) | serial | 7 s |
| **sum of step walls** | | **837 s (about 14 min)** |
| pool.py, build_games_csv.py, checks_uP.py, batch split (not timed, not in the sum) | serial | < 3 s each |

`banscan` is 469 of the 837 s (56%), so it is the step to shard more finely next time. No serial runtime
of the archived chain is recorded, so no speed-up is claimed.

## 3. Agent level: Claude Code workflows

### 3.1 Shape of round 1 (`syakegohan-up3feprmagi-*.js`)

`preflight -> extract -> [audit || pipeline(check -> verify) over the batches]`

- **No barrier between the check and verify phases.** `pipeline(ids, check, verify)` starts batch i's
  skeptic as soon as its own checker returns, so a slow checker holds up only its own batch. Start times
  from the journals:

| run | flags or spots | batches | skeptic starts before the slowest checker ends |
|---|---|---|---|
| uP round 1 | 246 | 3 | verify:b1 at +69.8 min, while check:b0 ran on to +80.1 min (10.3 min earlier) |
| uP score round | 26 spots + 2 items | 2 | verify:s0 at +7.5 min, while score:b1 ran on to +15.4 min |
| amemiya frame-check | 199 | 4 | verify:b1 at +30.2 min, while check:b0 ran on to +39.9 min |

- **The audit agent runs beside the pipeline.** It is started before the pipeline and awaited after it.
  Its job is to ask "is the check aimed at the right problem?":
  - Walk 3 unflagged games clear by clear. It found 2 missed REN singles.
  - Measure lag slow-motion. It found 1.43 s.
  - Sample the footage between games for a missed game. It found none.
- **Batch size.** uP's extract prompt used `B = max(1, min(3, ceil(n_flags/45)))`, and each game's flags
  stay in one batch. The cap of 3 gave 82 flags per batch. amemiya used a fixed 4 batches, about 50 flags
  each. Checker walls: amemiya 30.1, 31.0, 31.1, 39.9 min; uP 32.1, 34.0, 42.5 min. So 82 flags cost about
  2.6 min more on the slowest checker than ~50. A higher cap may help, but these runs do not show it.
- **One frame folder per agent**, all under `corr/fr/`: `b<i>/` (checker), `v<i>/` (skeptic), `audit/`,
  and `s<i>/` and `sv<i>/` in the score round. The skeptic must extract and Read its own frames.
  It never reuses the checker's.
- **Agents propose, the main thread applies.** Checkers return corrections only as structured output
  (`decisions`, `event_corrections`, `cell_edits`). Skeptics return `reviews` (keep, reason, `amended`) and a
  `missed` list. Only the main thread merges the kept proposals into `event-corrections.json` and
  `hand-edits.csv`, so these files have a single writer.
- **Stale proposals fail loudly.** remove, retype and setpc must name `t` (2 decimals) and `was` equal to
  exactly one event in the current `cseq.json`. replace_window can carry `was_old`. `apply/patch_overlay3.py`
  asserts on any mismatch. So a proposal made against an older event list stops the apply; it is not
  applied to the wrong event.

### 3.2 Second round as a new workflow (`syakegohan-up-score-round-*.js`)

Round 2 was written only after reading round 1's results. It is a new two-batch `pipeline(check -> verify)`
over 26 score-sum spots of 450 points or more. Its prompt says the round-1 corrections are already applied,
that `was` must match the current `cseq.json`, and that an edit inside an existing replace_window must say so
(the caller merges it). It fixed 21 events. Totals: 71 event corrections and 22 cell edits (`chain/uP/README.md`).

### 3.3 Wall time per run (journals)

| run | agents | wall |
|---|---|---|
| uP preflight + extract + round 1 | 9 | 92.8 min (preflight 16.4, extract 21.1) |
| uP score round | 4 | 19.1 min |
| amemiya frame-check | 9 | 48.4 min |
| amemiya KO-tail | 4 | 18.9 min |

## 4. Pitfalls seen in these runs

- **Partial `amended` records.** In the amemiya KO-tail run, a skeptic's `amended` left out `id`, `op`, `t`
  and other fields, and one for a cell edit left out `id`, `player`, `field`, `was` and `value`. In uP round 1,
  one left out `was` although the prompt asked for the "full record". Asking does not prevent it: merge
  `amended` over the proposal (`{**proposal, **amended}`), never replace the proposal with it.
- **A replace_window that deletes a `BREAK` also deletes its REN reset.** Clears that become adjacent then
  count as a REN. Put the None locks back, and check `max_combo` after the edit.
- **The score reader merges clears that are close together.** Never flag a whole-game count of score versus
  clears. Use only KO-tail jumps (60 points or more in the last 1.5 s) and score sums at points where the
  score stays still for 2 s. A merged jump keeps its sum.
- **A game with no KO crashes the serial steps.** l084 made `R/part.py` exit with rc=1. It was dropped from
  `games.json`, and gapchk, bagchk and part were rerun.
- **Hidden scores.** An attack effect or the KO art can hide the score or the NEXT queue. A reader catching
  up after a hidden stretch can attribute a jump to the wrong clear (l079).
