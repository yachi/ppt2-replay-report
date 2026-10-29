# chain/Gg: Yuukun3798 vs uyeshota, stream `Ggl5NeUAYEA` (dataset `stream-2026-10-29`)

51 games, ids `y000`–`y050`. This tree is a copy of `chain/uP` run on a new video, kept as it ran (its paths
point at `/private/tmp/claude-501/Gg/`). `diffs.txt` holds every code change against `../uP`. No video, frame or
feature file is committed.

## Inputs

- Video: downloaded at 480p with SnapYT (yt-dlp is blocked from the cloud). The capture is about 1.02x larger
  than the uP geometry, so the whole video was rescaled before anything read it:
  `ffmpeg -i in.mp4 -vf "scale=837:470:flags=bicubic,pad=854:480:8:6" -c:v libx264 -preset veryfast -crf 16 -g 30 -an`.
  After that the uP constants (cell 15.7 px, boards at x 142.5 / 553.6, floor 389) fit unchanged.
- Left board = Yuukun3798, right = uyeshota in every game.
- Games: `seg/` (the uP segmenter, re-run on the rescaled video) found 52 segments. The first (30.1–119.5 s) is
  the room menu and is dropped (`mkgames.py`). Two sets: FT15 aborted at 11-13 when the opponent disconnected
  right after the y023 KO (the window is cut at 1717.6, before the 通信中 dialog), then a fresh set that
  uyeshota took 15-12.
- Winners: 51 of 51 agree with the WIN counter, read by eye from contact sheets at every game start.

## What differs from chain/uP

| file | change |
|---|---|
| all | paths, ids (`y…`), dataset, names |
| `drive.sh`, `w/A/run_all.py` | 4 workers instead of 9; `R/pcscan.py` runs 2 at a time, one game each (about 5 GB per game) |
| `w/B/extract_b.py` | `border_end`: this capture's board border glows during play, so the end-of-game test is `match < 0.2` for 15 frames (was `< 0.5` for 10). With that, B's game ends agree with A's KO within 0.14 s on 51 of 51 games |
| `w/R/fr/*.png` | banner templates re-cut from this video (not committed) |
| `mkgames.py` | the WIN counters and the two set finals for this stream |
| `apply/checks_yu.py` | `checks_uP.py` without the l084 flag, with the y023 disconnect flag; the score reader is `ocr/` |
| `ocr/` | digit templates cut from this video (`tmpl.py`; `T.npy` not committed), reader and KO-tail jump finder |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-yuukun/`. The frame check is in `corr/`:

1. `corr/items.json`: 123 items, the chain's 80 flags plus 43 score-sum spots (`corr/tools/score.py`).
   Three readers (`out/b0-2.json`) each frame-checked a group (`group0-2.json`) under `BRIEF.md`; three skeptics
   (`out/v0-2.json`) tried to refute every fix on their own frames.
2. **PERFECT CLEAR banners.** In this video the banner is usually hidden by the character cut-in, so `R/pcon.py`
   sees an onset only 0.1 s long and `R/pcmap.py` (which wants 0.9 s) drops it. A reader checked the 33 short onsets
   no correction already covered (`group_pc.json`, `out/bpc.json`), and a skeptic (`out/vpc.json`) checked those fixes
   plus 5 spots where the chain logs one clear twice (`group_dup.json`). Perfect clears went from 7 to 39.
3. `corr/tools/merge.py` keeps what survived (77 event fixes) and writes `event-corrections.json`, which
   `w/tetrio/metrics.py` reads before the tally.
4. **Pieces.** `corr/tools/nextcount.py` reads the NEXT queue at 30 fps, rebuilds the whole piece sequence and
   checks every 7-piece block is a complete bag. pieces = shifts − the first hold into an empty box − a last piece
   not locked by the KO. Validated on two games where the chain's count was not in doubt, then run on all 102
   player-games (`corr/nextcount/`): 90 agree with the chain within the last-piece rule, 12 do not. Those 12, plus
   y050 p2 (its last piece is seen locking before the KO), are the 13 hand edits (`corr/tools/cells_final.py`).
   Gap windows (extractor B's spliced counts) account for most of them. Every final count fits the NEXT count.

`chain_games.csv`, `flags.json` and `sanity.txt` are the chain output after the event fixes, before `hand-edits.csv`.
