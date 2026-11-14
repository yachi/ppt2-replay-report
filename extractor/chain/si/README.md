# chain/si: syakegohan's stream of 2026-05-10 (「人が増えてほしいレート戦③」)

37 games, ids `z000`–`z036`, dataset `stream-2026-05-10`, video `IF3HCznmhOU`. This tree is a copy of `chain/se`,
run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/si/`, a cloud session's
scratchpad). It adds no frame image or video to the repo.

## Inputs

syakegohan is the LEFT board (p1) throughout. These are rate battles, each set first to 2 (the stars), against the
opponents as their nameplates print them.

| ids | set | opponent | score |
|---|---|---|---|
| z000–z001 | 1 | べんちぷれす | 2-0 |
| z002–z004 | 2 | べんちぷれす | 1-2 |
| z005–z007 | 3 | べんちぷれす | 1-2 |
| z008–z009 | 4 | べんちぷれす | 2-0 |
| z010–z012 | 5 | べんちぷれす | 2-1 |
| z013–z014 | 6 | べんちぷれす | 2-0 |
| z015–z017 | 7 | べんちぷれす | 2-1 |
| z018–z020 | 8 | ドラえもん | 2-1 |
| z021–z022 | 9 | べんちぷれす | 2-0 |
| z023–z024 | 10 | べんちぷれす | 2-0 |
| z025–z026 | 11 | べんちぷれす | 2-0 |
| z027–z028 | 12 | あとうてん | 2-0 |
| z029–z030 | 13 | ドラえもん | 2-0 |
| z031–z033 | 14 | ドラえもん | 2-1 |
| z034–z036 | 15 | べんちぷれす | 2-1 |

syakegohan 28-9 over the 37 games, 13 sets to 2.

- The video: drawn about 2% larger than qh's layout, as for se to sh: **rescaled to 836x470 and padded by 9,5 back
  to 854x480** (`video/nat_IF3HCznmhOU.mp4` is the native file, not used).
- Games: `seg/` as in qh (38 segments after `filt.py`; segment 0 is a solo 40-line run and is skipped, the other 37
  are one game each). `mkgames_si.py` writes `games.json` and `games_all.json` from the stars read off the next
  game's start counter, and each 1-1 decider's winner off the WIN/LOSE and WINNER screens; it asserts each set ends
  at 2.

## What differs from chain/se

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/si/`, video `IF3HCznmhOU` |
| `mkgames_si.py` | this stream's games (above) |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 679.8 s, a frame of z000 with both NEXT columns at rest |
| `corr/nc_compare.py` | reads this set's chain table and hand edits |
| `corr/merge_xo.py` | two groups |
| `apply/hand_edits_si.py` | `hand_edits_se.py` reading this set's `corr/cells.json` |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 100 flags (`corr/flags.json`): 70 PERFECT CLEAR banner onsets, 14 winner
   KO pieces, 9 gap windows, 3 T-spins with no banner, 2 banners with no clear and 2 KO-tail score jumps.
2. **PERFECT CLEARs.** 32 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). A lit-cell count of the
   board after each of the other 38 (`corr/litcount.txt`) stayed above 40, or the onset sat within 2 s of an accepted
   one, so none needed a frame check.
3. **Frame checks.** 28 items in two groups (`corr/groups/g0.json`, `g1.json`), from the non-PC flags and 1 score
   spot. `extractor/autosettle` settled 3 as no change (the score did not move between the last spawn and the KO) and
   gave 3 hints (`corr/out/auto.json`). One agent per group proposed corrections (`corr/out/b0.json`, `b1.json`) and
   another tried to refute each (`corr/out/v0.json`, `v1.json`); they kept all 23 proposals. Most are z024 (a
   match-point cut-in froze the game from about 2474 s to 2484 s) and z035 (heavy slow motion from about 3307 s to
   3348 s), where the chain logged phantom clears and false REN BREAKs.
4. **Merge.** `corr/merge_xo.py` wrote 10 event corrections (5 rebuilt windows, 2 retypes, 2 removals, 1 addition)
   and 13 cell edits. `corr/fixwas.py` ran `w/tetrio/metrics.py` and found every `was` matching the chain.
5. **Cells.** The corrected event list already gives 6 of the 13 (the max RENs and z023 p2's max B2B), so 7 are hand
   edits (`corr/hand_edits.csv`), all piece counts: z003 p2 38 → 39, z017 p1 143 → 144 and z030 p1 65 → 66 (a piece
   locked on the KO frame), z024 p1 114 → 113, z024 p2 101 → 100, z035 p1 148 → 144 and z035 p2 150 → 149 (phantom
   locks removed).

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/nc_compare.json`). Of the 74 player-games 52 agree exactly
and 3 are off by one (z012 p1, z017 p1, z028 p2). 19 are marked lost (bad bags or long unreadable stretches in the
NEXT read); every one recounts lower than the table, the usual sign of a blind stretch, and none was changed. No
clean read differs by more than one.

## Known gaps

- The 19 lost recounts leave those player-games' piece counts checked only by the frame-check items.
- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
