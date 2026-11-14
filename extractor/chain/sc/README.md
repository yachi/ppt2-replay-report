# chain/sc: syakegohan's stream of 2026-08-16 (「わんこそばさんの大会に出る」)

42 games, ids `t000`–`t041`, dataset `stream-2026-08-16`, video `n0Kbttgv3sQ`. This tree is a copy of `chain/qh`,
run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/sc/`, a cloud session's
scratchpad). It adds no frame image or video to the repo.

## Inputs

syakegohan is the LEFT board (p1) throughout. Opponents are read off the nameplate (Yuukun3798 is ゆうくん).

| ids | opponent | score |
|---|---|---|
| t000–t004 | ねっぷーさん | 5-0 |
| t005–t009 | meah | 5-0 |
| t010–t014 | Hirokiはいしん | 5-0 |
| t015–t021 | ゆうくん | 5-2 |
| t022–t031 | るる | 10-0 |
| t032–t041 | るる | 10-0 |

syakegohan 40-2 over the 42 games. るる's two sets are first to 10 (the counter shows 0 after the tenth win of the
first set); the rest are first to 5.

- The video: native 854x480 h264, the layout qh's coordinates expect. **No rescale.**
- Games: `seg/` as in qh (56 segments after the menu filter). `mkgames_sc.py` writes `games.json` and
  `games_all.json` from the WIN counters read by eye off the contact sheets, and asserts each game moves one counter
  by one and each set ends on its final score. Left out: the menu (segment 0), COM warm-up games (1, 7-10) and
  segments 28-35, where スラさん plays puyo (not tetris vs tetris).

## What differs from chain/qh

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/sc/`, video `n0Kbttgv3sQ` |
| `mkgames_sc.py` | this stream's games (above); `drive_qh1.sh`, `drive_qh2.sh` are qh's stage drivers |
| banner, word and score-digit templates, `w/ocr/T.npy` | copied from `chain/qh` (same channel, same native layout). Not committed |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 965 s, a frame of t000 with both NEXT columns at rest (qh's 2300 s is not a game frame here) |
| `corr/nc_compare.py` | reads this set's chain table and hand edits instead of the analysis games.csv |

As for qh, `pool/pool.py` needs `pool/out/` to exist, `w/tetrio/metrics.py` needs scipy and `witnessed.json`
(`[]` here), and `corr/tools/score.py` needs `check/ocr/reader.py` beside `w/ocr/T.npy`.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 79 flags (`corr/flags.json`): 50 PERFECT CLEAR banner onsets,
   10 banner/type disagreements, 8 winner KO pieces, 7 KO-tail score jumps, 2 T-spins with no banner, 1 gap window
   and 1 banner with no clear.
2. **PERFECT CLEARs.** 17 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). The other 33 make
   15 clusters (`corr/pcclusters.json`). A lit-cell count of the board after each onset (`corr/litcount.txt`) read
   a minimum of 40 or less after 4 rejected ones (t000, t006, t019 p1 and t030 p2). Those went to the frame checks
   as their own group, and all four were real PERFECT CLEARs.
3. **Score spots.** `check/score/` found 13 spots (`corr/score/spots.json`). None had an unexplained change of
   900 or more, so none was kept as an item.
4. **Frame checks.** The 29 non-PC flags and the 4 PC rejects made 33 items in three groups (`corr/groups/`).
   `extractor/autosettle` settled 1 as no change (t019 p1, nothing locked before the KO) and gave 2 hints
   (`corr/out/auto.json`); nothing from it was merged. One agent per group proposed corrections
   (`corr/out/b*.json`), and one more per group tried to refute each (`corr/out/v*.json`). The skeptics kept all
   19 proposals.
5. **Merge.** `corr/merge_xo.py` wrote 15 event corrections (11 retypes, 2 added events, 2 rebuilt windows) and
   4 cell edits. Eight of the retypes are the four hidden PCs: each is a clear marked as a PC plus a phantom
   duplicate lock retyped to a plain lock. `corr/fixwas.py` ran `w/tetrio/metrics.py` and needed no repair.
6. **Cells.** Of the 4 cell edits, the corrected event list already gives 1 (t033 p1's max REN), so 3 are hand
   edits, all piece counts (`corr/hand_edits.csv`).

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 84 player-games, 75 agree
exactly, 7 differ by one piece (all of them the recount one lower, mostly a piece locked on the KO frame) and 2 are
lost reads (t003 p1 and t041 p2). No clean read differs by more. No piece count was changed from the recount alone,
as for the earlier streams.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
