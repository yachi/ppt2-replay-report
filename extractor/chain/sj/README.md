# chain/sj: syakegohan's stream of 2026-04-19 (「人が増えてほしいレート戦②」)

36 games, ids `a000`–`a035`, dataset `stream-2026-04-19`, video `GC9tyaPCEk8`. This tree is a copy of `chain/se`,
run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/sj/`, a cloud session's
scratchpad). It adds no frame image or video to the repo.

## Inputs

syakegohan is the LEFT board (p1) throughout. These are rate battles, each set first to 2 (the stars), against the
opponents as their nameplates print them.

| ids | set | opponent | score |
|---|---|---|---|
| a000–a002 | 1 | どらさ | 2-1 |
| a003–a004 | 2 | どらさ | 2-0 |
| a005–a006 | 3 | になな | 2-0 |
| a007–a008 | 4 | どらさ | 2-0 |
| a009–a010 | 5 | どらさ | 2-0 |
| a011–a013 | 6 | Yuukun3798 | 2-1 |
| a014–a015 | 7 | Yuukun3798 | 2-0 |
| a016–a018 | 8 | Yuukun3798 | 2-1 |
| a019–a020 | 9 | あ | 0-2 |
| a021–a022 | 10 | あ | 2-0 |
| a023–a025 | 11 | あ | 2-1 |
| a026–a028 | 12 | あ | 2-1 |
| a029–a030 | 13 | あ | 2-0 |
| a031–a033 | 14 | あ | 2-1 |
| a034–a035 | 15 | あ | 2-0 |

syakegohan 28-8 over the 36 games, 14 sets to 1.

- The video: drawn about 2% larger than qh's layout, as for se to si: **rescaled to 836x470 and padded by 9,5 back
  to 854x480** (`video/nat_GC9tyaPCEk8.mp4` is the native file, not used).
- Games: `seg/` as in qh (36 segments after `filt.py`, each one game). `mkgames_sj.py` writes `games.json` and
  `games_all.json` from the stars read off each game's start and end, and each 1-1 decider's winner off the WIN/LOSE
  and WINNER screens; it asserts each set ends at 2.

## What differs from chain/se

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/sj/`, video `GC9tyaPCEk8` |
| `mkgames_sj.py` | this stream's games (above) |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 352.0 s, a frame of a000 with both NEXT columns at rest |
| `corr/nc_compare.py` | reads this set's chain table and hand edits |
| `corr/merge_xo.py` | two groups |
| `apply/hand_edits_sj.py` | `hand_edits_se.py` reading this set's `corr/cells.json` |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 80 flags (`corr/flags.json`): 49 PERFECT CLEAR banner onsets, 16 winner
   KO pieces, 9 gap windows, 3 KO-tail score jumps, 2 banners with no clear and 1 T-spin with no banner.
2. **PERFECT CLEARs.** 25 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). A lit-cell count of the
   board after each of the other 24 (`corr/litcount.txt`) stayed above 40, or the onset sat within 2 s of an accepted
   one, so none needed a frame check.
3. **Frame checks.** 24 items in two groups (`corr/groups/g0.json`, `g1.json`), from the non-PC flags and 1 score
   spot. `extractor/autosettle` settled 8 as no change and gave 1 hint (`corr/out/auto.json`). One agent per group
   proposed corrections (`corr/out/b0.json`, `b1.json`) and another tried to refute each (`corr/out/v0.json`,
   `v1.json`); they kept all 33 proposals. Most are a027 and a032, where the stream ran in slow motion (about 2980 s
   to 3005 s and 3323 s to 3340 s) and the chain logged phantom spawns and false REN BREAKs.
4. **Merge.** `corr/merge_xo.py` wrote 22 event corrections (17 rebuilt windows, 3 removals, 2 retypes) and 11 cell
   edits. `corr/fixwas.py` ran `w/tetrio/metrics.py` and found every `was` matching the chain after one fold.
5. **NEXT-recount check.** The recount below found a002 (the first set's decider) 4 pieces short on both boards on a
   clean read. Its frames (`corr/fr/a002/sheet.png`) show a match-point cut-in freezing both boards from about
   489.5 s to 495.5 s, so the 4 pieces extractor B spliced into each player's stalled window are phantoms: 2 more
   cell edits (`corr/cells.json`).
6. **Cells.** The corrected event list already gives 5 of the 13 (the max RENs of a026, a027 and a032), so 8 are
   hand edits (`corr/hand_edits.csv`), all piece counts: a009 p1 139 → 140 and a014 p1 141 → 142 (a piece locked on
   the KO frame), a027 p1 102 → 94, a027 p2 95 → 89, a032 p1 94 → 93 and a032 p2 108 → 104 (phantom locks in the
   slow motion), a002 p1 31 → 27 and a002 p2 28 → 24 (the cut-in).

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table and its hand edits (`corr/nc_compare.json`). Of the 72
player-games 55 agree exactly and 2 are off by one (a026 p1, a034 p1). 15 are marked lost (bad bags or long
unreadable stretches in the NEXT read); 14 recount lower than the table, the usual sign of a blind stretch, and
a020 p2 one higher. None was changed.

## Known gaps

- The 15 lost recounts leave those player-games' piece counts checked only by the frame-check items.
- a002's lines and garbage inside the cut-in window were left as the chain has them; only its piece counts changed.
- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
