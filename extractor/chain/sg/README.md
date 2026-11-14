# chain/sg: syakegohan's stream of 2026-06-06 (「人が増えてほしいレート戦⑤」)

24 games, ids `x000`–`x023`, dataset `stream-2026-06-06`, video `ypLHWB94OBU`. This tree is a copy of `chain/sf`
(itself a copy of `chain/se`), run on one live-stream archive and kept as it ran (its paths point at
`/tmp/claude-0/sg/`, a cloud session's scratchpad). It adds no frame image or video to the repo.

## Inputs

syakegohan is the LEFT board (p1) throughout. These are rate battles, each set first to 2 (the stars).

| ids | set | opponent | score |
|---|---|---|---|
| x000–x001 | 1 | になな | 2-0 |
| x002–x003 | 2 | になな | 2-0 |
| x004–x005 | 3 | すずもりれむ | 2-0 |
| x006–x007 | 4 | すずもりれむ | 2-0 |
| x008–x010 | 5 | すずもりれむ | 2-1 |
| x011–x012 | 6 | すずもりれむ | 2-0 |
| x013–x014 | 7 | すずもりれむ | 2-0 |
| x015–x016 | 8 | すずもりれむ | 2-0 |
| x017–x019 | 9 | すずもりれむ | 2-1 |
| x020–x021 | 10 | あてん | 2-0 |
| x022–x023 | 11 | あてん | 2-0 |

syakegohan 22-2 over the 24 games, 11 sets to 0.

- The video: drawn about 2% larger than qh's layout, as for se and sf: **rescaled to 836x470 and padded by 9,5 back
  to 854x480** (`video/nat_ypLHWB94OBU.mp4` is the native file, not used).
- Games: `seg/` as in qh (24 segments, every one a game). `mkgames_sg.py` writes `games.json` and `games_all.json`
  from the stars read off the next game's start counter, and each 1-1 decider's winner off the WIN/LOSE and WINNER
  screens; it asserts each set ends at 2.

## What differs from chain/sf

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/sg/`, video `ypLHWB94OBU` |
| `mkgames_sg.py` | this stream's games (above) |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 519.1 s, a frame of x000 with both NEXT columns at rest |
| `corr/nc_compare.py` | reads this set's chain table and hand edits |
| `corr/merge_xo.py` | one group (g1, the recount item below, proposed no change) |
| `apply/hand_edits_sg.py` | `hand_edits_se.py` reading this set's `corr/cells.json` |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 53 flags (`corr/flags.json`): 39 PERFECT CLEAR banner
   onsets, 8 winner KO pieces, 2 banners with no clear, 2 KO-tail score jumps, 1 banner/type disagreement and 1 T-spin
   with no banner.
2. **PERFECT CLEARs.** 22 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). A lit-cell count of the
   board after each of the other 17 (`corr/litcount.txt`) stayed above 40, or the onset sat within 2 s of an accepted
   one, so none needed a frame check.
3. **Frame checks.** 14 items in one group (`corr/groups/g0.json`). `extractor/autosettle` settled 5 as no change (the
   score did not move between the last spawn and the KO) and gave 1 hint (`corr/out/auto.json`). One agent proposed
   corrections for the other 9 (`corr/out/b0.json`) and another tried to refute each (`corr/out/v0.json`); it kept all
   11 proposals.
4. **Merge.** `corr/merge_xo.py` wrote 7 event corrections (4 retypes, 2 rebuilt windows, 1 addition) and 4 cell edits.
   `corr/fixwas.py` ran `w/tetrio/metrics.py` and found every `was` matching the chain.
5. **Cells.** Of the 4 cell edits, the corrected event list already gives 3 (x000 p1's max REN, the x022 and x023 p2
   max B2Bs), so 1 is a hand edit (`corr/hand_edits.csv`): x007 p1 pieces 50 → 51, a Z that locked into the garbage
   hole just before the KO.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/nc_compare.json`). Of the 48 player-games 36 agree exactly
and 11 are marked lost (bad bags or long unreadable stretches in the NEXT read); 10 of those recount lower than the
table and x010 p1 recounts 2 higher, all on unreadable stretches, and none was changed. One clean read differed:
x003 p2 recounts 28 against the table's 34. It went to its own frame check (`corr/groups/g1.json`,
`corr/out/b1.json`): the recount skipped about 1.6 s (687.84–689.47 s) where the NEXT queue could not be read, and the
frames show 5 pieces spawning there, matching the chain's 5 events, so the table's 34 stands (no change, so no
skeptic).

## Known gaps

- The 11 lost recounts leave those player-games' piece counts checked only by the frame-check items.
- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
