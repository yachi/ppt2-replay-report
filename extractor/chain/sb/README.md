# chain/sb: syakegohan's stream of 2026-08-20 (「vs あちみつさん 50先」)

83 games, ids `s000`–`s082`, dataset `stream-2026-08-20`, video `kgdvQLQyxp8`. This tree is a copy of `chain/qh`,
run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/sb/`, a cloud session's
scratchpad). It adds no frame image or video to the repo.

## Inputs

syakegohan is the LEFT board (p1) throughout; the opponent is あちみつ in every game.

| ids | room | WIN counter at the end |
|---|---|---|
| s000–s007 | 1 | 7-1, then the stream cuts to black and the room select mid-game (`s_cut_8`, in `games_all.json` only) |
| s008–s082 | 2 | 49-26, the WIN screen and 「ありがとうございました」 |

syakegohan 56-27 over the 83 games. The second room restarted the counter, so the title's 50先 is not one set on
screen.

- The video: native 854x480 h264, the layout qh's coordinates expect. **No rescale.**
- Games: `seg/` as in qh (84 segments after the menu filter). `mkgames_sb.py` writes `games.json` and
  `games_all.json` from the WIN counters read by eye off the contact sheets, and asserts each game moves one counter
  by one and each room ends on its final count. The last game is closed by seg (the stream sits in the room select
  after it).

## What differs from chain/qh

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/sb/`, video `kgdvQLQyxp8` |
| `mkgames_sb.py` | this stream's games (above); `drive_qh1.sh`, `drive_qh2.sh` are qh's stage drivers |
| banner, word and score-digit templates, `w/ocr/T.npy` | copied from `chain/qh` (same channel, same native layout). Not committed |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 2300 s, checked to be an online frame of this video with both NEXT columns at rest |
| `corr/nc_compare.py` | reads this set's chain table and hand edits instead of the analysis games.csv |

As for qh, `pool/pool.py` needs `pool/out/` to exist, `w/tetrio/metrics.py` needs scipy and `witnessed.json`
(`[]` here), and `corr/tools/score.py` needs `check/ocr/reader.py` beside `w/ocr/T.npy`.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 185 flags (`corr/flags.json`): 128 PERFECT CLEAR banner onsets,
   31 winner KO pieces, 9 KO-tail score jumps, 8 banner/type disagreements, 5 banners with no clear, 3 gap windows
   and 1 T-spin with no banner.
2. **PERFECT CLEARs.** 64 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). The other 64 make
   30 clusters (`corr/pcclusters.json`). A lit-cell count of the board after each onset (`corr/litcount.txt`) reads
   a stack after every rejected one (no minimum of 40 or less), so there are no hidden PCs and
   `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 26 spots (`corr/score/spots.json`); 2 with an unexplained change of 900 or
   more were kept as items.
4. **Frame checks.** 50 non-PC flags and the 2 spots made 52 items in three groups (`corr/groups/`).
   `extractor/autosettle` settled 7 as no change and gave 1 hint (`corr/out/auto.json`); nothing from it was merged.
   One agent per group proposed corrections (`corr/out/b*.json`), one more per group tried to refute each
   (`corr/out/v*.json`). The skeptics kept all 27 proposals and added one the checker had missed (s075 p1, a phantom
   lock at 5122.83).
5. **Merge.** `corr/merge_xo.py` wrote 16 event corrections (6 added events, 5 retypes, 5 rebuilt windows) and
   13 cell edits. `corr/fixwas.py` ran `w/tetrio/metrics.py` and needed no repair.
6. **Cells.** Of the 13 cell edits the corrected event list already gives 3 (REN and B2B maxima), so 10 are hand
   edits, all piece counts (`corr/hand_edits.csv`).

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game` and
`corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 166 player-games, 139 agree
exactly, 20 differ by one piece (all of them the recount one lower, mostly a piece locked on the KO frame) and 6 are
lost reads (s000 p1, s015 p2, s033 p2, s038 p1 and p2, s047 p1). One clean read differs by more: s046 p1 reads 55
against the table's 57, a hand edit from a frame check that found the PERFECT CLEAR L and one more lock missing from
the chain. It was not changed from the recount alone, as for the earlier streams.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
