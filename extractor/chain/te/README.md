# chain/te: uyeshota's stream of 2026-11-10 (15先 ×5)

115 games, ids `e000`–`e114`, dataset `stream-2026-11-10`, video `10ell5aAJuo`. This tree is a copy of `chain/qv`,
run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/te/`, a cloud session's
scratchpad). It adds no frame image or video to the repo.

## Inputs

uyeshota is the LEFT board (p1). Five sets, each first to 15, against four opponents:

| ids | set | opponent | score |
|---|---|---|---|
| e000–e017 | 1 | あかさ | 15-3 |
| e018–e046 | 2 | どらえもん | 15-14 |
| e047–e069 | 3 | どらえもん | 15-8 |
| e070–e092 | 4 | よわいこん | 15-8 |
| e093–e114 | 5 | あちみつ | 15-7 |

uyeshota 75-40 over the 115 games, five sets to none. The WIN counters read off the video agree with the table's
winners in all 115 games (`apply/checks_xo.py`).

- The video: rescaled like every uyeshota and amemiya video (`scale=837:470,pad=854:480:8:6`), so qv's board
  geometry holds. A stream bar sits across the top; the boards are clear.
- Games: `seg/` as in qv. `mkgames_te.py` writes `games.json` and `games_all.json` from the WIN counters read by eye
  off contact sheets (`seg/cnt.py`).

## What differs from chain/qv

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/te/`, video `10ell5aAJuo`, player `uyeshota` |
| `mkgames_te.py`, `drive_s1.sh`, `drive_s2.sh` | this stream's games and the two stage drivers |
| banner and word templates, `T.npy` | copied as for qv (same rescale geometry and digit font). Not committed |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 362, a clean online frame of this video (game e003) |
| `corr/merge_xo.py` | four groups (`range(4)`), and it drops a correction or cell edit proposed twice (two groups held overlapping windows) |
| `corr/nc_compare.py` | compares with this run's chain table plus its hand edits, not with `games.csv` |
| `apply/hand_edits_te.py` | the hand-edit writer, paths to this run |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-uyeshota/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 194 flags (`corr/flags.json`): 121 PERFECT CLEAR banner onsets,
   48 winner KO pieces, 11 gap windows (one at a game's tail), 6 KO-tail score jumps, 4 T-spins with no banner,
   2 bad bags and 2 banners with no clear.
2. **PERFECT CLEARs.** 49 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the others make
   36 clusters (`corr/pcclusters.json`). One rejected onset whose board read low (`corr/litcount.out`) went to the
   checkers as a frame-check item; `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 26 spots (`corr/score/spots.json`); 2 were kept as items.
4. **Frame checks.** The non-PC flags, the PC item and the 2 spots made 76 items in four groups (`corr/groups/`).
   One agent per group proposed corrections (`corr/out/b0-b3.json`), one more per group tried to refute each
   (`corr/out/v*.json`). Of 52 proposals the skeptics kept 50, amended 1 (a garbage-row count) and rejected 1
   (an e012 p1 cell edit).
5. **Merge.** `corr/merge_xo.py` wrote 27 event corrections (18 rebuilt windows, 5 retypes, 3 added events,
   1 removal) and 13 cell edits. `corr/fixwas.py` ran `w/tetrio/metrics.py` and needed no repair.
6. **Recount follow-up.** One more agent checked the recount's largest gap (`corr/out/b4.json`): e045 p1's last
   piece never locks before the KO and the window around it held phantom locks, so its piece count goes 87 → 80.
7. **Cells.** Of the 14 cell edits, the corrected event list already gives the 3 REN maxima, so 11 are hand edits,
   all piece counts.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game` (two workers), and
`corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 230 player-games, 219 agree
exactly, 4 differ by one piece and 6 are lost reads (long unknown stretches: e026 p1, e054 p2, e063 p1, e069 p2,
e103 p2, e108 p2). One clean read is higher than the table: e031 p2 by 3. Its frames show the table's count; a
TETRIS flash hid the fifth NEXT box and the recount read extra shifts. No piece count was changed from the recount
alone.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
