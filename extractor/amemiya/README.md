# extractor/amemiya/ — the chain as it ran on amemiya's stream 4xcAmo-s-Tg (2026-10-27)

An archive, like `../chain/`: the code is kept byte for byte as it ran, with absolute paths under
`/private/tmp/claude-501/am/`. There is no video, frame or feature file here.

| path | what |
|---|---|
| `PORT.md`, `port_diffs.txt` | every file copied from `../chain/cVO` (and `../start`, `../apply`, `../perf`) and every change, as diffs |
| `REPORT.md` | the chain run: timings, the geometry gate, games found, the flags it raised |
| `chain/am/w/` | the ported set. Geometry is recalibrated for this capture (cell 16.0 px, x0 137/556, floor 391); D1 is fixed |
| `start/mkgames.py` | new: 227 start candidates to 118 online games |
| `check/ocr/`, `check/ocrall/` | the score reader, and the cross-check of score jumps against the chain's clear events |
| `check/freezes.json` | the lag slow-motion windows (284.6 s in 10 games) |
| `check/offline_games.json` | the 34 offline games the chain cannot read, not in games.csv |
| `h3F/` | the same chain run on the second stream, h3FUsPBZmzE (2026-10-28, vs ふられ): its diffs, frame check and run report |

## How analysis/ppt2-amemiya/ was made

1. The chain wrote `chain_games.csv` (118 games, 199 flags).
2. Workflow 2: four agents frame-checked the 199 flags, and four skeptic agents re-read the frames of each correction.
3. The score reader ran over all 118 games. Its jumps in the last 1.5 s before each KO with no chain clear
   (32 spots) were frame-checked and verified the same way. In long REN chains the reader merges score
   changes, so it is a check of the KO tail only, not of every clear.
4. `chain/am/w/tetrio/metrics.py` reads `event-corrections.json` (106 events) and re-tallies;
   `python3 -m pipeline.ppt2_page --apply amemiya <chain.csv>` lays `hand-edits.csv` (76 cells) over it.

`analysis/ppt2-amemiya/games.csv` now holds both streams; `h3F/README.md` says how to rebuild it with `--apply`.
