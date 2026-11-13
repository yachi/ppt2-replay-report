# chain/fs: syakegohan's stream of 2026-10-30, first part (vs ふられ)

21 games, ids `o000`–`o020`, dataset `stream-2026-10-30`, video `-FTFs2Vv1ZI`. This tree is a copy of
`chain/qh`, run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/fs/`, a cloud
session's scratchpad). It adds no frame image or video to the repo.

## Inputs

The stream of 2026-10-30 was archived in two videos. The second, `6rUc3cXsjbo`, is already in the dataset
(`n000`–`n096`); this is the first. syakegohan is the LEFT board (p1); the opponent is ふられ in all three sets,
each first to 5. The video ends during set 3.

| ids | set | score |
|---|---|---|
| o000–o008 | 1 | 4-5 |
| o009–o014 | 2 | 5-1 |
| o015–o020 | 3 | 3-3 (unfinished: the video ends) |

syakegohan 12-9 over the 21 games.

- The video: yt-dlp through a Tailscale exit node (480p h264), remuxed to mp4. **No rescale**: native 854x480.
- Games: `seg/` as in qh (21 segments after the menu filter, every one a game). `mkgames_fs.py` writes
  `games.json` and `games_all.json` from the WIN counters read by eye off contact sheets (`seg/cnt.py`).
- **Set finals.** As in qh, the last game of sets 1 and 2 runs into the next set's room; its winner was read off
  the WIN pill before the loading screen (`seg/fin*.py`, `seg/fin_load.json`), and that loading time is its
  `end_upper_s`.

## What differs from chain/qh

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/fs/`, video `-FTFs2Vv1ZI` |
| `mkgames_fs.py`, `drive_s1.sh`, `drive_s2.sh` | this stream's games and the two stage drivers (replacing `mkgames_qh.py`, `drive_qh1.sh`, `drive_qh2.sh`) |
| banner and word templates | **recut from this video**: `b2` (Triple) 48.7 s, `b3` (Double) 60.4, `b_single` 111.3; the Mini word from p1's banner at 1511.8, pasted into p2's box. Not committed |
| `check/ocr/mktpl.py` | score digits recut from frames 343.2, 451.5, 713.1, 942.8, 1358.9, 1597.3 s. `T.npy` not committed |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 460, a clean online frame of this video (game o005) |
| `corr/merge_xo.py` | one group (`range(1)`) |
| `corr/nc_compare.py` | compares with this run's chain table plus its hand edit, not with `games.csv` |
| `apply/hand_edits_fs.py` | **new**: r6's hand-edit writer, paths to this run |

As for qh, `pool/pool.py` needs `pool/out/` to exist, `w/tetrio/metrics.py` needs scipy and `witnessed.json`
(`[]` here), `check/score/steps.py` needs `corr/score/`, and `corr/tools/score.py` needs `check/ocr/reader.py`
beside `w/ocr/T.npy`.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 45 flags (`corr/flags.json`): 31 PERFECT CLEAR banner onsets,
   6 winner KO pieces, 4 KO-tail score jumps, 3 banner/type disagreements and 1 banner with no clear. The WIN
   counter agrees with the csv in 21 of 21 games.
2. **PERFECT CLEARs.** 14 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). The others make
   8 clusters (`corr/pcclusters.json`); a lit-cell count of the board after each shows a stack, not an empty
   board, so `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 12 spots (`corr/score/spots.json`).
4. **Frame checks.** The non-PC flags and the spots made 15 items in one group (`corr/groups/g0.json`). One agent
   proposed corrections (`corr/out/b0.json`), one more tried to refute each (`corr/out/v0.json`). The skeptic kept
   three of the five event corrections and one of the three cell edits; the two pieces it rejected (o005, o016)
   lock one frame after the KO.
5. **Merge.** `corr/merge_xo.py` wrote 3 event corrections (a retype, a rebuilt window, an added clear) and
   1 cell edit. `corr/fixwas.py` ran `w/tetrio/metrics.py` and needed no repair.
6. **Cells.** The cell edit is a hand edit: o020 p2's pieces 127 → 128, an O that locks before the KO frame.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 42 player-games, 31 agree
exactly, 3 differ by one piece (each the table one higher: o004 p2, o010 p2, o014 p2) and 8 are lost reads (bad
bags or long unknown stretches: o001 p1, o004 p1, o007 p2, o008 p2, o011 p2, o012 p1, o019 p2, o020 p1). No piece
count was changed from the recount alone, as for qh.

## Known gaps

- Set 3 is unfinished: the video stops at 3-3, so its six games have winners but the set has none.
- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
