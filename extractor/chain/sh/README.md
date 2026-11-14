# chain/sh: syakegohan's stream of 2026-05-31 (「人が増えてほしいレート戦④」)

17 games, ids `y000`–`y016`, dataset `stream-2026-05-31`, video `O3c6BqscsQw`. This tree is a copy of `chain/sf`
(itself a copy of `chain/se`), run on one live-stream archive and kept as it ran (its paths point at
`/tmp/claude-0/sh/`, a cloud session's scratchpad). It adds no frame image or video to the repo.

## Inputs

syakegohan is the LEFT board (p1) throughout. These are rate battles, each set first to 2 (the stars), all against
ドラえもん (the nameplate as drawn).

| ids | set | score |
|---|---|---|
| y000–y001 | 1 | 2-0 |
| y002–y003 | 2 | 0-2 |
| y004–y005 | 3 | 2-0 |
| y006–y007 | 4 | 2-0 |
| y008–y009 | 5 | 2-0 |
| y010–y011 | 6 | 2-0 |
| y012–y014 | 7 | 2-1 |
| y015–y016 | 8 | 2-0 |

syakegohan 14-3 over the 17 games, 7 sets to 1.

- The video: drawn about 2% larger than qh's layout, as for se, sf and sg: **rescaled to 836x470 and padded by 9,5
  back to 854x480** (`video/nat_O3c6BqscsQw.mp4` is the native file, not used).
- Games: `seg/` as in qh (17 segments, every one a game). `mkgames_sh.py` writes `games.json` and `games_all.json`
  from the stars read off the next game's start counter, and the 1-1 decider's winner off the WIN/LOSE and WINNER
  screens; it asserts each set ends at 2.

## What differs from chain/sf

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/sh/`, video `O3c6BqscsQw` |
| `mkgames_sh.py` | this stream's games (above) |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 510.7 s, a frame of y000 with both NEXT columns at rest |
| `corr/nc_compare.py` | reads this set's chain table and hand edits |
| `corr/merge_xo.py` | one group |
| `apply/hand_edits_sh.py` | `hand_edits_se.py` reading this set's `corr/cells.json` |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 27 flags (`corr/flags.json`): 12 PERFECT CLEAR banner onsets, 10 gap
   windows, 4 winner KO pieces and 1 KO-tail score jump.
2. **PERFECT CLEARs.** 9 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). A lit-cell count of the
   board after each of the other 3 (`corr/litcount.txt`) stayed above 40, so none needed a frame check.
3. **Frame checks.** 13 items in one group (`corr/groups/g0.json`). `extractor/autosettle` settled 2 as no change (the
   score did not move between the last spawn and the KO; `corr/out/auto.json`). One agent proposed corrections for
   the rest (`corr/out/b0.json`) and another tried to refute each (`corr/out/v0.json`); it kept all 6 proposals.
   The proposals are all y001, where both players run a slow REN race from about 560 s to 652 s and the chain logged
   phantom clears and false BREAKs on both boards.
4. **Merge.** `corr/merge_xo.py` wrote 2 event corrections (one rebuilt window per player over the REN race) and 4
   cell edits. `corr/fixwas.py` ran `w/tetrio/metrics.py` and found every `was` matching the chain.
5. **Cells.** The corrected event list already gives the two max RENs (p1 14, p2 11), so 2 are hand edits
   (`corr/hand_edits.csv`): y001 p1 pieces 78 → 63 and p2 77 → 60, each equal to extractor A's count.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/nc_compare.json`). Of the 34 player-games 25 agree exactly
and 1 is off by one (y005 p1). 8 are marked lost (bad bags or long unreadable stretches in the NEXT read); 7 of those
recount lower than the table and y011 p1 recounts 1 higher, and none was changed. No clean read differs by more
than one.

## Known gaps

- The 8 lost recounts leave those player-games' piece counts checked only by the frame-check items.
- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
