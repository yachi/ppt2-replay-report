# chain/sm: syakegohan vs ドラえもん, 15先×3 (uploaded 2025-08-27)

54 games, ids `d000`–`d053`, dataset `upload-2025-08-27`, three videos. This tree is a copy of `chain/sl`, run on the
three videos together and kept as it ran (its paths point at `/tmp/claude-0/sm/`, a cloud session's scratchpad). It
adds no frame image or video to the repo.

## Inputs

Each video is one set, first to 15 (the titles call the series 「15先×2+1」). syakegohan is the LEFT board (p1)
throughout.

| ids | video | opponent | score |
|---|---|---|---|
| d000–d018 | `btWygcgWSOs` (Part1) | ドラえもん | 15-4 |
| d019–d035 | `FsVlPseNc0o` (Part2) | ドラえもん | 15-2 |
| d036–d053 | `o_jajoEdYzA` (Part3) | ドラえもん | 15-3 |

syakegohan 45-9 over the 54 games, all three sets.

- The videos: the 720p uploads, downscaled to 854x480 (`scale=854:480`) when they were downloaded, which gives the
  layout ms's and qh's coordinates expect. **No rescale** in this tree.
- Games: `seg/` was run per video (`seg/v_<video>/`), as for `chain/sl`. seg never closes a video's last game, so
  `mkgames_sm.py` appends it: start 1.2 s after the previous end, end 9 s after the WIN counter's last change (read by
  eye off a crop at each game's start), capped at the video's length. It asserts each game moves one counter by one
  and each video ends at 15.

## What differs from chain/sl

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/sm/` |
| `mkgames_sm.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `sm` |
| `corr/merge_xo.py` | four groups (`range(4)`; g3 = the PC items) |
| `apply/hand_edits_sm.py` | `hand_edits_se.py` reading this set's `corr/cells.json` |

`corr/tools/nextcount.py` keeps `REF_FRAME_T` 30.0 s, which falls inside the first game of each video.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 97 flags: 57 PERFECT CLEAR banner onsets, 15 winner KO pieces, 10 gap
   windows, 8 T-spins with no banner, 5 KO-tail score jumps and 2 banner/type disagreements. `check/score/` found 34
   score spots; the 10 of them at 900 points or more became items.
2. **PERFECT CLEARs.** 16 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 20 clusters
   (`corr/pcclusters.json`). A lit-cell count of the board after each (`corr/litcount.txt`) left 13 that went to a
   frame check as group g3.
3. **Frame checks.** 50 non-PC items in three groups (`corr/groups/g0.json`–`g2.json`), of which
   `extractor/autosettle` settled 6 as no change (`corr/out/auto.json`), and the 13 PC items (`g3.json`). One agent
   per group proposed corrections (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`). The
   skeptics rejected 2 (d031 p1 and d043 p1: the KO piece locked one frame after the KO), amended 1 (d032 p1: the PC
   belongs on the 636.47 event, not 637.23) and added 11 the checkers missed (among them d025 p1's rebuilt PC window,
   d046 p1's piece count and six max-REN / max-B2B cells). All 13 PC items were real PERFECT CLEARs the chain had
   logged twice (the clear, then a duplicate clear on the next piece).
4. **Merge.** `corr/merge_xo.py` wrote 66 event corrections. Eleven were duplicates: g3's PC retypes repeated retypes
   g0, g1 and g2 had already proposed for the same events (d010, d014, d029, d034, d044 p1), and two d032 p1 entries
   (the un-amended g1 proposal, and the amendment, which the merge filed under d033 p2). They were removed by hand,
   keeping one entry per event: 53 corrections. Two duplicate cell edits (d029 p1 max_b2b, d034 p1 max_combo) were
   dropped the same way. `corr/fixwas.py` ran `w/tetrio/metrics.py` and needed no repair.
5. **Slow play.** d009 (about 512–530 s) and d046 (about 537–578 s) run in slow motion; extractor B spliced phantom
   clears and false REN BREAKs there, and the corrections remove them (d009 max REN 17 and 16, d046 15 and 7).
   d018 froze for the match-point cut-in at about 1044–1048.6 s, where the chain logged a phantom single.
6. **Cells.** 19 cell edits; the corrected event list already gives 10 of them (the max RENs and max B2Bs), so 9 are
   hand edits (`corr/hand_edits.csv`): 8 piece counts and d033 p2 max_b2b 0 → 1.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/nc_compare.json`). Of the 108 player-games 86 agree exactly
and 9 are off by one, all recounting lower. 10 are marked lost (bad bags or long unreadable stretches), all on the
opponent's board, and none was changed. 3 read more than one lower: d009 p1 (85 against 88), d009 p2 (78 against
81) and d018 p1 (464 against 468). All three sit in the slow-motion or cut-in stretches above, and the d009 counts
are the ones both agents set from the frames; they were not changed.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- the d009 and d018 p1 recount differences above are not explained piece by piece.
- No opener labels (the `opener` column is empty).
