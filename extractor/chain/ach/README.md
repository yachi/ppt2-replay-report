# chain/ach: five uploads of 2026-10-28 vs あちみつ (15先2セット先取)

117 games, ids `m000`–`m116`, dataset `upload-2026-10-28`. This tree is a copy of `chain/uP` run on five
videos, kept as it ran (its paths point at `/tmp/claude-0/ak/`, a cloud session's scratchpad). It adds no
frame image or video to the repo.

## Inputs

| video | title part | games | set (syakegohan–あちみつ) |
|---|---|---|---|
| `FAsKhtwulHA` | 1回目 Part1 | m000–m023 (24) | 15–9 |
| `IJGqwSdiKwk` | 1回目 Part2 | m024–m046 (23) | 15–8 |
| `-zR8CNrXdCI` | 2回目 Part1 | m047–m074 (28) | 13–15 |
| `b-o1kjuoygk` | 2回目 Part2 | m075–m095 (21) | 15–6 |
| `pUZUSoR6VSU` | 2回目 Part3 | m096–m116 (21) | 15–6 |

- Downloaded from SnapYT at 480p (`check/pc/snap.js`, Playwright; yt-dlp is not used). 854x480, 30 fps,
  replay footage. Left board = syakegohan, right = あちみつ on every nameplate checked.
- Geometry: the uP constants (cell 15.7 px, board x 142.5 / 553.6, floor 389) fit unchanged.
- Games: `seg/` as in uP, one occupancy file per video. `seg.games()` never closes a video's last game
  (the video ends on the result screen, not on empty boards), so each video's last game was appended by
  hand. `mkgames_ach.py` writes `games.json` from the per-video WIN-counter strings, read by eye from
  contact sheets (`check/pc/cnt.py`) at start+3 s and end−0.3 s; it asserts the counter rises by one per game.
- Winners: A's KO winner agrees with the WIN counter on 117 of 117. syakegohan 73–44.

## What differs from chain/uP

| file | change |
|---|---|
| all | paths rewritten to the new work tree; `games.json` has a `path` per game (five videos) |
| `drive*.sh`, `A/run_all.py` | pools of 4 (the container had 4 cores and 15 GB); `pcscan` at 2. `drive_ab.sh` / `drive_b.sh` / `drive_c.sh` are the stage splits that ran after a container restart |
| `w/R/fr/*.png` | banner templates (TST, TSD, TSS, Mini) re-cut from these videos with `check/pc/banfind.py` / `bansheet.py` (not committed). A whole-video scan at 10 fps float32 needs ~9 GB, so it ran on two videos only |
| `check/ocr/` | score-digit templates (`T.npy`, not committed) from six frames read by eye (`mktpl.py`), checked on six held-out frames. `ocr_game.py` reads each game's own video |
| `apply/checks_ach.py` | `checks_uP.py` less its uP-only flags |
| `corr/` | **new**: the frame-check brief, tools, item groups, every proposal and verdict, and `merge_ach.py` |

## Corrections

All 73 event corrections and 10 cell edits are in `analysis/ppt2-syakegohan/` (ids `m…`).

1. **Flags.** The chain raised 322 flags: 200 PERFECT CLEAR banner onsets, and 122 others (winner KO piece,
   banner/type disagreements, gap windows, bad bags, KO-tail score jumps, unresolved games).
2. **PERFECT CLEARs.** All 88 onsets that `pcmap` accepted show the banner (`check/pc/pcsheet2.py`). Of
   the 112 short onsets it rejected, 51 sit on an accepted PC and the other 61 fall in 40 clusters;
   `check/pc/pcstrip.py` drew 11 frames around each. 11 are real PCs that cut-in effects split into short
   onsets (`corr/hidden_pc.json`): m004p2, m029p1, m041p1 (two), m044p1, m053p1, m058p1, m065p2, m093p1,
   m098p1, m114p1. Each is the clear before the banner, and its double-logged half is removed.
3. **Frame checks.** `check/score/` (score sum against the event list, as in uP) found 36 spots of 450
   points or more. The 122 flags and the 36 spots, less the two unresolved games, made 132 items in six
   groups (`corr/groups/`). One agent per group read the frames and proposed corrections (`corr/out/b*.json`);
   three more agents tried to refute each one (`corr/out/v*.json`). None was rejected; five were amended
   (gc counts, a window end, a PC flag, a piece count). `corr/merge_ach.py` merges them with the hidden PCs.
   Where a frame check and the hidden-PC list touch the same event, the frame check wins; for m041p1 at
   861 s the PC sits on the 860.97 quad.
4. **Cells.** 18 cell edits were proposed; 8 of them (B2B and REN maxima) the corrected event list already
   gives, so 10 are hand edits.

## NEXT-queue recount

`corr/tools/nextcount.py --game` re-counted every player-game's spawns. Against the final table, with the first
hold into an empty box and an unmatched last spawn taken off, 154 of the 230 included player-games agree
exactly, 52 differ by one piece (mostly the piece falling at the KO, which the frame checks found unlocked in
almost every flagged case), and 24 are games where the reader lost the queue for seconds or read bad bags.
No piece count was changed from the recount alone; only frame-checked counts were.

## Known gaps

- m021 and m058 stay excluded as unresolved lower bounds (the build step lost syakegohan's board partway).
- Piece counts can be off by one at the KO in up to 52 player-games (see above).
- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
