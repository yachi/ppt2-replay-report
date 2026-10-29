# chain/uP: the 2026-10-28 stream vs ふられ (`uP3FeprmAGI`)

84 games, ids `l000`–`l083`, dataset `stream-2026-10-28`. This tree is a copy of `chain/TJc` run on the new
video, kept as it ran (its paths point at `/private/tmp/claude-501/uP/`). It adds no frame image to the repo.

## Inputs

- Video: 854x480, 30 fps, 5665 s. Left board = syakegohan, right = ふられ on all 85 nameplates (the title
  says ふれあさん, the nameplate does not).
- Geometry: the TJc constants (cell 15.7 px, board x 142.5 / 553.6, floor 389) pass a six-frame gate unchanged.
- Games: `seg/seg.py` over 9 time shards (`seg/occ_shard.py`), `seg/par.py` for the menu filter and the
  WIN-counter winner, `mkgames.py` writes `games.json`. 85 games were found. l084 has no KO (the stream froze,
  then the opponent disconnected), so it is left out. l014–l017 are a set that the opponent left at 2-2.
- Winners: 84 of 84 agree with the WIN counter read by eye, including the five 4-4 finals.

## What differs from chain/TJc

| file | change |
|---|---|
| all | paths rewritten to the new work tree and video |
| `drive.sh`, `A/run_all.py` | every per-game step runs as a 9-process pool. The whole chain runs in about 14 min |
| `R/fr/*.png` | banner templates re-cut from this video (not committed). `b_mini2.png` is cut from a Mini T-SPIN Single at 152.3 s, so **T-spin Minis are detected** here (21 in the final csv) |
| `R/build.py` | writes `R/unresolved.json`, which `tetrio/metrics.py` reads as `UNRESOLVED` |
| `tetrio/metrics.py` | PCDEC from `pcdec.json`. The event overlay is this set's `event-corrections.json`. It dumps the event list it tallied to `tetrio/cseq.json` |
| `seg/track.py`, `seg/occ_shard.py`, `seg/par.py`, `mkgames.py` | **new**: the segmenter's missing module and parallel wrappers |
| `pool/pool.py`, `apply/build_games_csv.py` | the amemiya port's copies, with paths changed. `apply/checks_uP.py` writes the flags |

## Corrections

All 71 event corrections and 22 cell edits are in `analysis/ppt2-syakegohan/` (ids `l…`). They came from two
workflow rounds. In each round, one agent per batch read video frames and proposed corrections, and a second agent
re-read its own frames to refute each one.

1. **Flag round.** The chain raised 246 flags (gap windows, banner disagreements, PC banner onsets, KO-tail
   score jumps, bad bags). 50 events and 22 cells. An audit of three unflagged games found 2 more missed
   singles in REN chains (l022 p1, l040 p1). The audit also found no missed game between games, and only
   1.43 s of lag (l012, a hang just before the KO).
2. **Score-sum round** (`check/score/`). `check/ocr/` reads both scores at 30 fps. `scoresum.py` and
   `steps.py` compare the running sum of score jumps with the points that the corrected event list predicts
   (guideline scoring, level 3), at points where the score stays still for 2 s. A merged jump keeps its sum,
   so the reader's merging of close clears does not cause a false spot. 26 spots of 450 points or more were
   checked (`check/score/round2.js`). 21 events were fixed: doubles read as singles, phantom clears, missed REN
   singles and a quad read as a triple. The 9 spots that remain are timing artifacts at a window edge.

The score templates (`check/ocr/C.npy`) are digit crops and are not committed. `check/ocr/collect.py`
samples the cells that they were clustered from.

## Known gaps

- Eight games stay excluded as unresolved lower bounds: l007, l020, l029, l043, l062, l063, l078, l083.
- A replace_window that deletes a `BREAK` also deletes its REN reset. Check `max_combo` after such an edit.
