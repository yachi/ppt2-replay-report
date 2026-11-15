# chain/ae: syakegohan vs ドラえもん, 15先 Part1-2 (uploaded 2025-08-08)

38 games, ids `ae00`–`ae37`, dataset `upload-2025-08-08`, two videos. This tree is a copy of `chain/sp`, run on the
two videos together and kept as it ran (its paths point at `/tmp/claude-0/ae/`, a cloud session's scratchpad). It
adds no frame image or video to the repo. Ids follow `chain/sp`'s two-letter scheme: this set is `ae`.

## Inputs

syakegohan is the LEFT board (p1) throughout; the opponent is ドラえもん.

| ids | video | WIN counters at the end (syakegohan first) | length |
|---|---|---|---|
| ae00–ae21 | `Rkj1nbxRO18` (Part1) | 15-7 | 27:01 |
| ae22–ae37 | `pgQ9un3zSec` (Part2) | 15-1 | 16:31 |

syakegohan 30-8 over the 38 games; each part is one whole set.

- The videos: native 854x480, リプレイVer 3.5, the layout the coordinates expect. **No rescale.**
- Games: `seg/` was run per video (`seg/v_<video>/`); `seg` never closes a video's last game, so `mkgames_ae.py`
  appends it (start = previous end + 1.2 s, end = the video's end less 0.2 s) and asserts each game moves one WIN
  counter by one. The chain's winners agree with the counters in all 38 games.

## What differs from chain/sp

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/ae/` |
| `mkgames_ae.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `ae` |
| `corr/merge_xo.py` | five groups (`range(5)`; g4 = the PC items) |
| `corr/dedupe.py` | **new** (as in `chain/ss`): run after `merge_xo.py`; drops repeated proposals (asserting they agree) and drops cells the corrected events already give |
| `corr/dedupe_note.txt` | what `dedupe.py` dropped |
| `apply/hand_edits_sp.py` | removed: the cell edits go straight to `analysis/ppt2-syakegohan/hand-edits.csv` |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 122 flags: 75 PERFECT CLEAR banner onsets, 17 winner KO pieces, 12 banners
   with no clear, 7 banner/type disagreements, 5 T-spins with no banner, 4 KO-tail score jumps and 2 gap windows
   over 4 s. `check/score/` found 34 score spots, 14 of them taken as frame-check items.
2. **PERFECT CLEARs.** 31 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 19 clusters
   (`corr/pcclusters.json`), and a lit-cell count of the board after each (`corr/litcount.txt`) left 5 that went to a
   frame check as group g4. All 5 were real PERFECT CLEARs (2 syakegohan, 3 ドラえもん) that the chain had logged as a
   clear plus one or two phantom pieces.
3. **Frame checks.** 61 non-PC items; `extractor/autosettle` settled 7 as no change (`corr/out/auto.json`), and the
   other 54 went to four groups (`corr/groups/g0.json`–`g3.json`) beside the 5 PC items (`g4.json`). One agent per
   group proposed corrections (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`): they
   rejected none and amended 2 (ae20 p2: the gap window widened to 1553.4–1561.5, and its pieces cell).
4. **Merge.** `corr/merge_xo.py` wrote 43 event corrections; `corr/dedupe.py` dropped 6 that repeated another
   proposal, leaving 37 (`corr/dedupe_note.txt`). `corr/fixwas.py` found no `was` to repair.
5. **Cells.** Three, all piece counts: ae12 p2 37 -> 38 and ae21 p1 46 -> 47 (pieces locked on the KO frame), and
   ae20 p2 290 -> 281 (nine pieces `R/build.py` spliced into two B gaps and a phantom lock). The checkers also
   proposed `max_combo` and `max_b2b` cells; the chain recomputes them from the corrected events and already gives
   each one, so `dedupe.py` dropped them.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted all 76 player-games' spawns with `corr/tools/nextcount.py --game` (the 4-of-5-frame
template from `chain/sp`), and `corr/nc_compare.py` compared them with the table after the cell edits: 67 agree, 7
differ by one and 2 are lost reads (ae12 p1, ae24 p2). No piece count was changed from it.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty).
