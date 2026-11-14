# chain/sk: syakegohan's stream of 2026-04-12 (「人が増えてほしいレート戦①」)

18 games, ids `b000`–`b017`, dataset `stream-2026-04-12`, video `UZJvlgvO2FQ`. This tree is a copy of `chain/se`,
run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/sk/`, a cloud session's
scratchpad). It adds no frame image or video to the repo.

## Inputs

syakegohan is the LEFT board (p1) throughout. These are rate battles, each set first to 2 (the stars), all nine
against どらさ as the nameplate prints it.

| ids | set | opponent | score |
|---|---|---|---|
| b000–b001 | 1 | どらさ | 2-0 |
| b002–b003 | 2 | どらさ | 2-0 |
| b004–b005 | 3 | どらさ | 2-0 |
| b006–b007 | 4 | どらさ | 2-0 |
| b008–b009 | 5 | どらさ | 2-0 |
| b010–b011 | 6 | どらさ | 2-0 |
| b012–b013 | 7 | どらさ | 2-0 |
| b014–b015 | 8 | どらさ | 2-0 |
| b016–b017 | 9 | どらさ | 2-0 |

syakegohan 18-0 over the 18 games, 9 sets to 0.

- The video: drawn about 2% larger than qh's layout, as for se to si: **rescaled to 836x470 and padded by 9,5 back
  to 854x480** (`video/nat_UZJvlgvO2FQ.mp4` is the native file, not used).
- Games: `seg/` as in qh (18 segments after `filt.py`, each one game). `mkgames_sk.py` writes `games.json` and
  `games_all.json` from the stars read off each game's start and end; it asserts each set ends at 2. No set went
  to a decider.

## What differs from chain/se

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/sk/`, video `UZJvlgvO2FQ` |
| `mkgames_sk.py` | this stream's games (above) |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 43.9 s, a frame of b000 with both NEXT columns at rest |
| `corr/nc_compare.py` | reads this set's chain table and hand edits |
| `corr/merge_xo.py` | two groups |
| `apply/hand_edits_sk.py` | `hand_edits_se.py` reading this set's `corr/cells.json` |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 32 flags (`corr/flags.json`): 22 PERFECT CLEAR banner onsets, 4 winner
   KO pieces, 2 gap windows, 2 T-spins with no banner, 1 banner/type disagreement and 1 banner with no clear.
2. **PERFECT CLEARs.** 11 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). A lit-cell count of the
   board after each of the other 11 (`corr/litcount.txt`) stayed above 40 or sat within 2 s of an accepted one,
   except b006 p2 at 558.7 s (lowest count 19), which became its own frame-check group.
3. **Frame checks.** 10 items in two groups (`corr/groups/g0.json`, `g1.json`). `extractor/autosettle` settled 2
   as no change (b014 p1 and b015 p1: the score did not move between the last spawn and the KO) and gave 2 hints
   (`corr/out/auto.json`). One agent per group proposed corrections (`corr/out/b0.json`, `b1.json`) and another
   tried to refute each (`corr/out/v0.json`, `v1.json`); they kept all 8 proposals.
4. **Merge.** `corr/merge_xo.py` wrote 7 event corrections (4 rebuilt windows, 3 retypes) and 1 cell edit.
   `corr/fixwas.py` ran `w/tetrio/metrics.py` and found every `was` matching the chain. The b006 p2 flash at 558.0 s
   is retyped to a PERFECT CLEAR; b010's 938.4–945.3 s stall held two phantom locks spliced in by extractor B and a
   false REN BREAK, removed.
5. **Cells.** One hand edit (`corr/hand_edits.csv`): b010 p1 pieces 104 → 102 (the two phantom locks).

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/nc_compare.json`). Of the 36 player-games 23 agree exactly.
13 are marked lost (bad bags or long unreadable stretches in the NEXT read); every one recounts lower than the
table, the usual sign of a blind stretch, and none was changed.

## Known gaps

- The 13 lost recounts leave those player-games' piece counts checked only by the frame-check items.
- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
