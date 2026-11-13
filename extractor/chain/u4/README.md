# chain/u4: uyeshota's upload of 2026-11-03 (名人戦 VS にんまる)

21 games, ids `b000`–`b020`, dataset `upload-2026-11-03`, video `u4P57GT3unk`. This tree is a copy of `chain/qh`,
run on one uploaded video and kept as it ran (its paths point at `/tmp/claude-0/u4/`, a cloud session's scratchpad).
It adds no frame image or video to the repo.

## Inputs

uyeshota is the LEFT board (p1); the opponent is にんまる in one first-to-20 set, which uyeshota won 20-1 (his only
loss is `b017`).

- The video: yt-dlp through a Tailscale exit node (480p h264), then **rescaled** like every uyeshota and amemiya
  video (`scale=837:470,pad=854:480:8:6`), so qh's board geometry holds.
- Games: `seg/` as in qh (21 segments after the menu filter, every one a game; the 112-936 s segment it drops is the
  menus). `mkgames_u4.py` writes `games.json` and `games_all.json` from the WIN counters read by eye off contact
  sheets. The last game ends on the victory banner, so its segment end is its end.

## What differs from chain/qh

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/u4/`, video `u4P57GT3unk`, player `uyeshota` |
| `mkgames_u4.py`, `drive_s1.sh`, `drive_s2.sh` | this video's games and the two stage drivers (replacing `mkgames_qh.py`, `drive_qh1.sh`, `drive_qh2.sh`) |
| banner and word templates | **recut from this video**: `b2` (Triple) 1756.4 s, `b3` (Double) 1240.8, `b_single` 1018.2, `b_mini2` 1675.4. Not committed |
| `check/ocr/mktpl.py` | not run: `T.npy` copied from `chain/fs` (same digit font), checked by eye at 1100, 1500 and 2000 s. Not committed |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 1010, a clean online frame of this video (game b001) |
| `corr/BRIEF.md` | header rewritten for this video |
| `corr/merge_xo.py` | one group (`range(1)`) |
| `corr/nc_compare.py` | compares with this run's chain table plus its hand edit, not with `games.csv` |
| `apply/hand_edits_u4.py` | **new**: r6's hand-edit writer, paths to this run |

As for qh, `pool/pool.py` needs `pool/out/` to exist, `w/tetrio/metrics.py` needs scipy and `witnessed.json`
(`[]` here), `check/score/steps.py` needs `corr/score/`, and `corr/tools/score.py` needs `check/ocr/reader.py`
beside `w/ocr/T.npy`.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-uyeshota/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 21 flags (`corr/flags.json`): 11 PERFECT CLEAR banner onsets,
   6 winner KO pieces, 3 KO-tail score jumps and 1 banner with no clear. The WIN counter agrees with the csv in
   21 of 21 games.
2. **PERFECT CLEARs.** 3 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). The others, less one
   that repeats an accepted onset, make 5 clusters (`corr/pcclusters.json`); a lit-cell count of the board after
   each reads 100 or more lit cells, a stack (an accepted PC reads 20-60 on this rescaled video, never 0), so
   `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 2 spots (`corr/score/spots.json`), neither of 900 or more, so neither became an item.
4. **Frame checks.** The 10 non-PC flags made 10 items in one group (`corr/groups/g0.json`). One agent
   proposed corrections (`corr/out/b0.json`), one more tried to refute each (`corr/out/v0.json`) and kept all
   four. The six winner KO pieces were still dropping at the KO frame and are not counted.
5. **Merge.** `corr/merge_xo.py` wrote 3 event corrections (b005 p1: the missed piece that made the PC double;
   b008 p1: a lock that cleared a single; b012 p2: a Mini T-spin Single that cleared nothing) and 1 cell edit.
   `corr/fixwas.py` ran `w/tetrio/metrics.py` and needed no repair.
6. **Cells.** The cell edit is a hand edit: b005 p1's pieces 24 → 25.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 42 player-games, 41 agree
exactly and 1 differs by one piece: b005 p1, where the recount gives the chain's 24 and the table holds the
frame-checked 25. No piece count was changed from the recount alone.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
