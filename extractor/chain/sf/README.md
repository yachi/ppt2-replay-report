# chain/sf: syakegohan's stream of 2026-06-14 (「人が増えてほしいレート戦⑥」)

29 games, ids `w000`–`w028`, dataset `stream-2026-06-14`, video `Y8mIXYrRzAc`. This tree is a copy of `chain/se`
(itself a copy of `chain/qh`), run on one live-stream archive and kept as it ran (its paths point at
`/tmp/claude-0/sf/`, a cloud session's scratchpad). It adds no frame image or video to the repo.

## Inputs

syakegohan is the LEFT board (p1) throughout. These are rate battles, each set first to 2 (the stars).

| ids | set | opponent | score |
|---|---|---|---|
| w000–w002 | 1 | あめみや　はいしん | 2-1 |
| w003–w004 | 2 | あめみや　はいしん | 2-0 |
| w005–w006 | 3 | あめみや　はいしん | 2-0 |
| w007–w008 | 4 | あめみや　はいしん | 0-2 |
| w009–w010 | 5 | あめみや　はいしん | 0-2 |
| w011–w013 | 6 | ドラへもん | 2-1 |
| w014–w016 | 7 | しょうがく6ねんせい | 2-1 |
| w017–w018 | 8 | しょうがく6ねんせい | 2-0 |
| w019–w020 | 9 | あめみや　はいしん | 2-0 |
| w021–w023 | 10 | あめみや　はいしん | 2-1 |
| w024–w025 | 11 | しょうがく6ねんせい | 2-0 |
| w026–w028 | 12 | ドラへもん | 2-1 |

syakegohan 20-9 over the 29 games, 10 sets to 2. `ドラへもん` is the nameplate as drawn (a different name from the
`ドラえもん` of other streams).

- The video: drawn about 2% larger than qh's layout, as for se: **rescaled to 836x470 and padded by 9,5 back to
  854x480** (`video/nat_Y8mIXYrRzAc.mp4` is the native file, not used).
- Games: `seg/` as in qh (29 segments, every one a game). `mkgames_sf.py` writes `games.json` and `games_all.json`
  from the stars read by eye off the contact sheets, and each set-ending game's winner off the WINNER screen; it
  asserts each set ends at 2.

## What differs from chain/se

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/sf/`, video `Y8mIXYrRzAc` |
| `mkgames_sf.py` | this stream's games (above) |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 343.4 s, a frame of w000 with both NEXT columns at rest |
| `corr/nc_compare.py` | reads this set's chain table and hand edits |
| `corr/merge_xo.py` | four groups; overlapping groups keep one copy of an event correction, and g3's w007 cell edits replace the per-group ones |
| `apply/hand_edits_sf.py` | `hand_edits_se.py` reading this set's `corr/cells.json` |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 72 flags (`corr/flags.json`): 35 PERFECT CLEAR banner onsets, 22 gap
   windows, 10 winner KO pieces, 2 banner/type disagreements, 1 T-spin with no banner, 1 banner with no clear and
   1 KO-tail score jump.
2. **PERFECT CLEARs.** 9 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). The others make
   11 clusters (`corr/pcclusters.json`). A lit-cell count of the board after each (`corr/litcount.txt`) fell to 40
   or less after 4 of them (w002, w022, w023, w024 p1); those went to their own group (`corr/groups/g2.json`), and
   the frames show a real PERFECT CLEAR in all 4.
3. **Frame checks.** 38 items in two groups (`corr/groups/g0.json`, `g1.json`). `extractor/autosettle` settled 2 as
   no change (w000 p1 and w004 p1: the score did not move between the last spawn and the KO) and gave 1 hint
   (`corr/out/auto.json`). One agent per group proposed corrections (`corr/out/b*.json`), one more per group tried
   to refute each (`corr/out/v*.json`); the skeptics kept every proposal. The largest was w007, where the stream
   runs in extreme slow motion through about 890–1150 s and the chain logged phantom clears on both boards; g0 and
   g1 removed overlapping sets of them, so a fourth item (`corr/groups/g3.json`, `corr/out/b3.json`) re-counted
   both sides' pieces over the union of the removals, checked against extractor A and the NEXT queue
   (p1 239 → 211, p2 211 → 197). It has no skeptic: its counts equal extractor A's.
4. **Merge.** `corr/merge_xo.py` wrote 43 event corrections (21 removals, 12 rebuilt windows, 10 retypes) and 11
   cell edits. `corr/fixwas.py` ran `w/tetrio/metrics.py` and flagged one `was` that did not match the chain (a w023 p1 retype), which was set to the chain's value by hand.
5. **Cells.** Of the 11 cell edits, the corrected event list already gives 5 (max RENs and the w002 / w022 ones), so
   6 are hand edits (`corr/hand_edits.csv`): 5 piece counts and w010 p2's max REN, which the frames show reaching 19
   (the chain's own value after the corrections is 10).

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/nc_compare.json`). Of the 58 player-games 30 agree
exactly. The other 28 are marked lost (bad bags or long unreadable stretches in the NEXT read), and in every one the
recount is LOWER than the table, which is the recount missing spawns and not the table counting phantoms. None of
them was changed. No clean read differs from the table.

## Known gaps

- The 28 lost recounts leave those player-games' piece counts checked only by the frame-check items.
- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
