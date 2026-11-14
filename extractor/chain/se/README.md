# chain/se: syakegohan's stream of 2026-07-31 (「レート戦⑦」)

34 games, ids `u000`–`u033`, dataset `stream-2026-07-31`, video `T8HfGflEsSc`. This tree is a copy of `chain/qh`,
run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/se/`, a cloud session's
scratchpad). It adds no frame image or video to the repo.

## Inputs

syakegohan is the LEFT board (p1) throughout. These are rate battles, each set first to 2 (the stars), against
あめみや　はいしん in 13 sets and しょうがく6ねんせい in one.

| ids | set | opponent | score |
|---|---|---|---|
| u000–u001 | 1 | あめみや　はいしん | 2-0 |
| u002–u003 | 2 | あめみや　はいしん | 2-0 |
| u004–u006 | 3 | あめみや　はいしん | 1-2 |
| u007–u008 | 4 | あめみや　はいしん | 2-0 |
| u009–u010 | 5 | あめみや　はいしん | 2-0 |
| u011–u013 | 6 | あめみや　はいしん | 2-1 |
| u014–u016 | 7 | あめみや　はいしん | 1-2 |
| u017–u019 | 8 | あめみや　はいしん | 2-1 |
| u020–u021 | 9 | しょうがく6ねんせい | 2-0 |
| u022–u023 | 10 | あめみや　はいしん | 2-0 |
| u024–u025 | 11 | あめみや　はいしん | 2-0 |
| u026–u027 | 12 | あめみや　はいしん | 2-0 |
| u028–u030 | 13 | あめみや　はいしん | 2-1 |
| u031–u033 | 14 | あめみや　はいしん | 1-2 |

syakegohan 25-9 over the 34 games, 11 sets to 3.

- The video: 854x480 h264, but this stream draws the game about 2% larger than qh's layout. It was **rescaled to
  836x470 and padded by 9,5 back to 854x480** (`video/nat_T8HfGflEsSc.mp4` is the native file, not used), after
  which qh's coordinates read it.
- Games: `seg/` as in qh (34 segments after the menu filter, every one a game). `mkgames_se.py` writes `games.json`
  and `games_all.json` from the stars read by eye off the contact sheets, and each set-ending game's winner off the
  WINNER screen; it asserts each set ends at 2.

## What differs from chain/qh

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/se/`, video `T8HfGflEsSc` |
| `mkgames_se.py` | this stream's games (above) |
| banner, word and score-digit templates, `w/ocr/T.npy` | copied from `chain/qh` (same channel, layout matched by the rescale). Not committed |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 65 s, a frame of u000 with both NEXT columns at rest |
| `corr/nc_compare.py` | reads this set's chain table and hand edits instead of the analysis games.csv |
| `corr/merge_xo.py` | three groups; a later cell edit whose `was` is an earlier edit's `value` folds into one edit |

As for qh, `pool/pool.py` needs `pool/out/` to exist, `w/tetrio/metrics.py` needs scipy and `witnessed.json`
(`[]` here), and `corr/tools/score.py` needs `check/ocr/reader.py` beside `w/ocr/T.npy`.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 55 flags (`corr/flags.json`): 29 PERFECT CLEAR banner onsets,
   10 winner KO pieces, 8 gap windows, 3 KO-tail score jumps, 2 banners with no clear, 2 T-spins with no banner
   and 1 banner/type disagreement.
2. **PERFECT CLEARs.** 8 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). The others make
   15 clusters (`corr/pcclusters.json`). A lit-cell count of the board after each (`corr/litcount.txt`) never fell
   to 40 or less after a rejected one, so there are no hidden PCs and `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 16 spots (`corr/score/spots.json`); 2 were kept as items.
4. **Frame checks.** 28 items in two groups (`corr/groups/g0.json`, `g1.json`). `extractor/autosettle` settled 2 as
   no change (u010 p1 and u026 p1: the score did not move between the last spawn and the KO) and gave 2 hints
   (`corr/out/auto.json`). One agent per group proposed corrections (`corr/out/b*.json`), one more per group tried
   to refute each (`corr/out/v*.json`); the skeptics kept every proposal. The largest was u015, where both boards
   lag through 1040-1085 s and the chain had logged phantom clears there: two windows were rebuilt, and both max
   RENs move to 16.
5. **Merge.** `corr/merge_xo.py` wrote 5 event corrections (3 retypes, 2 rebuilt windows) and 5 cell edits.
   `corr/fixwas.py` ran `w/tetrio/metrics.py` and needed no repair.
6. **Cells.** Of the 5 cell edits, the corrected event list already gives 2 (u015's max RENs), so 3 are hand edits,
   all piece counts (`corr/hand_edits.csv`).

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/nc_compare.json`). The first comparison found three clean
reads 4 or 5 pieces higher in the table than in the recount: u011 p1 and both sides of u015. Those went to a third
group (`corr/groups/g2.json`, `corr/out/b2.json`, `v2.json`). In each, the extra pieces were ones extractor B had
spliced in over a lost extractor-A NEXT read (`w/reconciled.jsonl`). They were counted in `pieces` but never became
chain events, and the frames show no lock behind them. The checker set the three counts to A's (u011 p1 106 → 102,
u015 p1 246 → 238, u015 p2 208 → 200), and the skeptic kept all three. After that, of the 68 player-games 64 agree
exactly and 4 differ by one piece. None differs by more.

## Known gaps

- u011 p1's `lines_cleared` still carries the 6 lines B spliced in over the same lost read; lines is not a cell
  the hand edits can change.
- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
