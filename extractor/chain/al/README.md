# chain/al: syakegohan vs あめみや, 15先 Part1-2 (uploaded 2025-07-09)

48 games, ids `al00`–`al47`, dataset `upload-2025-07-09`, two videos. This tree is a copy of `chain/ai`, run on the
two videos together and kept as it ran (its paths point at `/tmp/claude-0/al/`, a cloud session's scratchpad). It
adds no frame image or video to the repo. Ids follow `chain/sp`'s two-letter scheme: this set is `al`.

## Inputs

syakegohan is the LEFT board (p1) throughout; the opponent is あめみや.

| ids | video | WIN counters at the end (syakegohan first) |
|---|---|---|
| al00–al24 | `BvWqKzuS65Q` (Part1) | 15-10 |
| al25–al47 | `A9WD7IyT8es` (Part2) | 15-8 |

syakegohan 30-18 over the 48 games.

- The videos: リプレイVer 3.5, the layout the coordinates expect. Both were fetched at 720p and scaled to 854x480
  before the chain ran (no layout rescale).
- Games: `seg/` was run per video (`seg/v_<video>/`); `seg` never closes a video's last game, so `mkgames_al.py`
  appends it and asserts each game moves one WIN counter by one.

## What differs from chain/ai

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/al/` |
| `mkgames_al.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `al` |
| `corr/dedupe.py` | as in `chain/saj`, plus two rules this set needed (below) and one NEXT recount decision |
| `corr/dedupe_note.txt` | what `dedupe.py` dropped and decided |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

The two `dedupe.py` rules:

- **`was` read differently.** Two groups retyped the same al22 p1 event and agreed on everything but the third slot
  of `was` (the chain's PC flag); the duplicate is dropped and the kept one takes the other's `was`, which
  `corr/fixwas.py` then re-reads from the chain.
- **Point removals inside a window.** al44 is a six-minute REN game that two groups rebuilt: g2 by per-event
  removals, g3 by `replace_window`s over the same stretch, both verified and with the same piece counts. g3's windows
  are kept, and every retype, removal or single-event point window of g2's inside them is dropped.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 139 flags: 68 PERFECT CLEAR banner onsets, 39 gap windows over 4 s, 19
   winner KO pieces, 5 T-spins with no banner, 3 banners with no clear, 2 PPS outliers, 2 KO-tail score jumps and 1
   banner/type disagreement. `check/score/` found 21 score spots.
2. **PERFECT CLEARs.** 26 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 16 clusters
   (`corr/pcclusters.json`), checked with a lit-cell count of the board after each (`corr/litcount.txt`); those left
   in doubt went to a frame check as group g4 (8 items). The set holds 33 PCs, all syakegohan's.
3. **Frame checks.** `extractor/autosettle` settled 5 items as no change (`corr/out/auto.json`); the other items went
   to groups g0 (17 items), g1 (15), g2 (19) and g3 (20) beside the PC items (g4, 8). One agent per group proposed
   corrections (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`): g1's rejected 2 (an al38
   add and its piece count) and g4's amended 4 (garbage-row counts to 0).
4. **Merge.** `corr/merge_xo.py` wrote the event corrections and `corr/dedupe.py` dropped 4 duplicates and 58 events
   inside another group's window, leaving 39 (`corr/dedupe_note.txt`).
5. **Cells.** Eleven, all piece counts: al06 p1 28 -> 29, al07 p2 47 -> 48, al13 p2 92 -> 89, al13 p1 109 -> 102
   (below), al16 p1 60 -> 58, al16 p2 41 -> 40, al22 p1 56 -> 57, al29 p1 137 -> 135, al29 p2 110 -> 108, and the
   rebuilt al44, p1 112 -> 71 and p2 99 -> 69.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted all 96 player-games' spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/hand_edits.csv` is the cells without a header): 85 agree,
9 differ by one, 1 is a lost read (al15 p2) and one reads more: al13 p1, 102 against 108. That read is clean (14 whole
bags, no unknown stretch) and the corrected events also number 102, so the piece count was set to 102 (`NC` in
`corr/dedupe.py`); the chain's piece column had stood 6 above its own event list for that game.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty).
