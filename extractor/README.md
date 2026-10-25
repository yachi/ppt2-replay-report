# extractor/ — the video extraction chain, archived as it ran

This directory holds the source code that wrote the chain output under
`analysis/ppt2-syakegohan/games.csv`. It is an **archive, not a runnable package**.

## What you cannot do with it alone

- **Rebuild from zero without the videos.** The repo holds no video, no frame image and no derived
  feature file (`*.npz`, `*.pkl`). To start again, download the 18 videos listed in `games.csv`
  (column `video`) with `uvx yt-dlp -f "bv*[height<=480][ext=mp4]"`, then run extractors A and B.
- **Run the scripts in place.** They contain absolute paths to the original work tree,
  `/private/tmp/claude-501/sk/...`. The code is kept byte for byte as it ran. It was not rewritten,
  because a rewrite that nobody runs is a second, untested copy.

## Layout

| path | what |
|---|---|
| `start/` | game start detection (`grid.py`, `starts.py`) and the first-bag tools (`bag.py`, `seq.py`, `run.py`) |
| `chain/<set>/w/A/` | extractor A: NEXT-queue spawn intervals. An event's `t` is the spawn time of its interval |
| `chain/<set>/w/B/` | extractor B: the cell solve of the board |
| `chain/<set>/w/R/` | fusion of A and B (`build.py`, `fuse.py`) and the frame checks (gaps, bags, banners, ends) |
| `chain/<set>/w/tetrio/metrics.py` | the tally: clears, attack from the PPT2 attack table, REN, B2B |
| `chain/pool/pool.py` | pools the sets into `all_rows.csv` and `pooled.md` |
| `apply/` | `build.sh`, the event-correction patcher (`patch_overlay3.py`) and `build_games_csv.py` |
| `mech/` | `drive_metrics.sh`, `restore_metrics.sh`, `check_applied.py`: the metrics-only rerun |
| `perf/solve_fast.py` | the bitboard rewrite of B's `solve()`. It is byte-identical in output and about 52 times faster |
| `REBUILD-ko2.md` | the end-of-game rebuild recipe, kept verbatim with its original paths |

`<set>` is one work tree per batch of videos: `Y`, `lg` and `cVO` are the three streams
`YbMeCRhjG1k`, `lgszEWNFSx0` and `cVO2eGipjV0`. `B` holds the other videos. The four trees are
near-copies, and some files differ from tree to tree. `TJc` is a later port of `cVO` to the 2026-10-18
video `TJcCRfhwNNI`; its README lists what it changes and how it was checked.

## How games.csv is made

1. The chain writes a chain `games.csv`. Before the tally, `apply/patch_overlay3.py` applies
   `analysis/ppt2-syakegohan/event-corrections.json` to the event sequences.
2. `python3 -m pipeline.ppt2_page --apply <chain games.csv>` lays
   `analysis/ppt2-syakegohan/hand-edits.csv` over the chain output and writes the repo's `games.csv`.
3. `bin/build-docs` renders `docs/` from that file.

## Known defects, not fixed in the code

| id | defect |
|---|---|
| D1 | A counts a first-piece hold made before the second spawn (`cand` admits `q=0` in `A/analyze.py`). The fix is `if q > 0 and s >= hf-1` |
| D2, D3 | `R/build.py` adds B's pace-estimated gap pieces on top of A's interval in stall windows longer than 4 s |
| D4 | nine bad-bag rows are not frame-checked: g043p1 g061p1 g102p2 j002p1 i014p2 i017p2 i021p2 i031p1 h027p2 |
| D5 | start detection has no GO-template gate, so six games took READY as the start (fixed by hand) |
| D6 | i015 p2 `garbage_received_rows` is 2, but the frames show one grey row |

The hand fixes for these rows are in `analysis/ppt2-syakegohan/`. See `HISTORY.md` at the repo root.
