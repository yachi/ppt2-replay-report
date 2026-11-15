# chain/sq: syakegohan vs あてん, one game (uploaded 2025-08-17)

One game, id `ab00`, dataset `upload-2025-08-17`, one video (`JCJkunwkkxw`). This tree is a copy of
`chain/sp`, run on the one video and kept as it ran (its paths point at `/tmp/claude-0/sq/`, a cloud session's
scratchpad). It adds no frame image or video to the repo. Ids follow `chain/sp`'s two-letter scheme: this set is `ab`.

## Inputs

| id | video | WIN counters (syakegohan first) | length |
|---|---|---|---|
| ab00 | `JCJkunwkkxw` | 2-0 → 3-0 | 9:28 |

The upload holds one game of a set whose earlier games were not uploaded; the WIN counters read 2-0 when it starts
and 3-0 when it ends, so syakegohan won it. syakegohan is the LEFT board (p1).

- The video: native 854x480, リプレイVer 3.5, the layout the coordinates expect. **No rescale.**
- Games: `seg/` found no game in a video this short, so `mkgames_sq.py` writes the one game by hand: ゴー！ shows at
  2.0 s and the first pieces drop at 2.4 s, so `start_s` is 1.8; the end is the video's end less 0.2 s. A first run
  used `start_s` 5.3, read off a misread clock, and lost each player's first pieces; the NEXT recount's bag offset
  and its bad bags showed it, and the tree was rebuilt (the frame-check corrections were kept). Extractor A's winner
  agrees with the counters.

## What differs from chain/sp

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/sq/` |
| `mkgames_sq.py` | the one game, by hand (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `sq` |
| `corr/merge_xo.py` | two groups (`range(2)`; g1 = the PC items) |
| `corr/dedupe_note.txt` | nothing dropped |
| `apply/hand_edits_sp.py` | removed: no cell edits |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

## Corrections

All event corrections are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 7 flags: 3 PERFECT CLEAR banner onsets, 2 T-spins with no banner, 1
   banner with no clear and 1 winner KO piece. `check/score/` found 5 score spots, given to the readers beside them.
2. **PERFECT CLEARs.** None of the 3 onsets carries `pcmap`'s "PC = clear at"; they make 3 clusters, and the lit-cell
   count (`corr/litcount.txt`) sent 2 to a frame check as group g1. Both were real PERFECT CLEARs (あてん, 139.7 s and
   about 503 s) that the chain had missed.
3. **Frame checks.** 4 non-PC items in g0 and the 2 PC items in g1; `extractor/autosettle` settled none. One agent per
   group proposed corrections (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`); they kept
   all of them, amended none and added none.
4. **Merge.** `corr/merge_xo.py` wrote 4 event corrections (three retypes: p1 68.30 mini T-spin to no clear, p1
   115.10 double to TSD, p2 139.73 quad to PC; one rebuilt window, p2 501.53–502.9); none was dropped.
   `corr/fixwas.py` needed no repair.
5. **Cells.** No cell edits.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted both player-games' spawns with `corr/tools/nextcount.py --game` (the 4-of-5-frame
template from `chain/sp`), and `corr/nc_compare.py` compared them with the table: both agree exactly.

## Known gaps

- garbage-row counts (`gc`) inside the rebuilt window were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty).
