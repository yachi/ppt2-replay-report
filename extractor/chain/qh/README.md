# chain/qh: syakegohan's stream of 2026-11-09 (vs ゆうくん)

176 games, ids `q000`–`q175`, dataset `stream-2026-11-09`, video `QheX1_UP5W4`. This tree is a copy of
`chain/oc`, run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/qh/`, a cloud
session's scratchpad). It adds no frame image or video to the repo.

## Inputs

syakegohan is the LEFT board (p1) throughout. The opponent is ゆうくん (in-game Yuukun3798) in all 24 sets,
each first to 5.

| ids | set | score |
|---|---|---|
| q000–q006 | 1 | 5-2 |
| q007–q015 | 2 | 5-4 |
| q016–q023 | 3 | 5-3 |
| q024–q030 | 4 | 5-2 |
| q031–q035 | 5 | 5-0 |
| q036–q042 | 6 | 5-2 |
| q043–q050 | 7 | 5-3 |
| q051–q056 | 8 | 5-1 |
| q057–q065 | 9 | 5-4 |
| q066–q070 | 10 | 5-0 |
| q071–q079 | 11 | 4-5 |
| q080–q087 | 12 | 3-5 |
| q088–q096 | 13 | 5-4 |
| q097–q104 | 14 | 5-3 |
| q105–q110 | 15 | 5-1 |
| q111–q116 | 16 | 5-1 |
| q117–q125 | 17 | 5-4 |
| q126–q130 | 18 | 5-0 |
| q131–q137 | 19 | 5-2 |
| q138–q145 | 20 | 5-3 |
| q146–q152 | 21 | 5-2 |
| q153–q161 | 22 | 5-4 |
| q162–q168 | 23 | 5-2 |
| q169–q175 | 24 | 5-2 |

syakegohan 117-59 over the 176 games, 22 sets to 2.

- The video: fetched with yt-dlp through a Tailscale exit node right after the live ended. The h264 formats gave
  no fragments for the post-live archive; VP9 itag 244 with `--live-from-start` worked, remuxed to mp4.
- **No rescale.** The archive is native 854x480 in the layout xt's coordinates expect.
- Games: `seg/` as in oc (176 segments after the menu filter, every one a game). `mkgames_qh.py` writes
  `games.json` and `games_all.json` from the WIN counters read by eye off contact sheets, and asserts each game
  moves one counter by one and each set ends on its final score.
- **Set finals.** A set's last game runs into the next set's room, so its end counter already reads 0-0 (or the
  Now Loading screen). Its winner was read off the WIN pill 3-9 s before the loading screen (`seg/fin*.py`,
  `seg/fin_load.json`), and that loading time is the game's `end_upper_s`.

## What differs from chain/oc

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/qh/`, video `QheX1_UP5W4`, player name `syakegohan` |
| `mkgames_qh.py`, `drive_qh1.sh`, `drive_qh2.sh` | this stream's games and the two stage drivers (`drive_qh2.sh` is drive.sh's tail, banscan at `-P 3`; `drive_wait.sh` started it) |
| `seg/fin.py`, `fin2.py`, `fin3.py`, `fin_load.json` | the set-final WIN-pill reads above |
| banner, word and score-digit templates | **recut from this video** (`b2` 66.0 s, `b3` 73.8, `b_single` 263.1, the Mini word from 2067.65; digits from `check/ocr/mktpl.py`'s frames at 2245/2500/3050/4700/6300/7900 s). Not committed. The Mini banner here reads "Mini" left of the T and shifts T-SPIN right, which banscan's Mini box (473,325–493,338) already reads |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 2200 → 2300, a clean online frame of this video |
| `check/ocr/jumps.py` | must be copied beside the OCR outputs for `apply/checks_xo.py` to import it |
| `ocr_all.sh` | runs `check/ocr/ocr_game.py` over all 176 games, four at a time |

As for oc, `pool/pool.py` needs `pool/out/` to exist, `w/tetrio/metrics.py` needs scipy and `witnessed.json`
(`[]` here), and `corr/tools/score.py` needs `check/ocr/reader.py` beside `w/ocr/T.npy`.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 357 flags (`corr/flags.json`): 246 PERFECT CLEAR banner onsets,
   55 winner KO pieces, 18 banner/type disagreements, 15 T-spins with no banner, 13 KO-tail score jumps,
   6 gap windows and 4 banners with no clear. The WIN counter agrees with the csv in 176 of 176 games.
2. **PERFECT CLEARs.** 133 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). The other onsets
   away from an accepted PC make 59 clusters (`corr/pcclusters.json`), drawn as strips with `check/pc/strip2.py`.
   A lit-cell count of the board after each one (about 23 on an empty board after an accepted PC, 62 or more after
   every cluster) shows every cluster is a line-clear flash on a stack, so there are no hidden PCs and
   `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 78 spots (`corr/score/spots.json`); the 6 with an unexplained score
   change of 900 or more were kept as items.
4. **Frame checks.** The 111 non-PC flags and the 6 spots made 117 items in four groups (`corr/groups/`).
   One agent per group proposed corrections (`corr/out/b*.json`), one more per group tried to refute each
   (`corr/out/v*.json`). The skeptics kept every proposal and added one the checker had left: a rebuilt window
   in q035 p1 (an I PERFECT CLEAR quad at 2554.80 and two plain locks), which changes no count. Phantom quads and
   T-spins logged twice, and pieces locked on the KO frame, were the largest sources.
5. **Merge.** `corr/merge_xo.py` wrote 22 event corrections (10 rebuilt windows, 7 retypes, 3 added events,
   2 removals) and 18 cell edits. `corr/fixwas.py` ran `w/tetrio/metrics.py` and needed no repair.
6. **Cells.** Of the 18 cell edits, the corrected event list already gives 6 (REN and B2B maxima), so 12 are hand
   edits: 11 piece counts and q055 p2's max REN.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game` (one worker while
the frame-check agents ran, then four), and `corr/nc_compare.py` compared them with the final table
(`corr/nc_compare.json`). Of the 352 player-games, 305 agree exactly, 35 differ by one piece (32 of them the table
one higher, mostly a piece locked on the KO frame) and 8 are lost reads (bad bags or long unknown stretches:
q008 p1, q085 p1, q092 p2, q094 p2, q100 p1, q133 p1, q161 p2, q162 p1). Four clean reads differ by more:
q021 p1, q040 p1 and q048 p1 read 3 higher, and each has three NEXT shifts in one frame about 1.5 s before the end
(`multi`) with no lock behind them, which a player cannot do, so the recount is wrong there; q174 p2 reads 249
against 251, a game whose count the frame checks rebuilt from the spawns directly. No piece count was changed from
the recount alone, as for xo, xt, tx, nk, aj and oc.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- q057 p1's last O locks on the frame where p2's board first tilts; it is counted (27 pieces).
- No opener labels (the `opener` column is empty, as for the streams).
