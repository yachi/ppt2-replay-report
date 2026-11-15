# chain/ss: syakegohan vs uyeshota, 15先 Part1-2 (uploaded 2025-08-09)

41 games, ids `ad00`–`ad40`, dataset `upload-2025-08-09`, two videos. This tree is a copy of `chain/sp`, run on the
two videos together and kept as it ran (its paths point at `/tmp/claude-0/ss/`, a cloud session's scratchpad). It
adds no frame image or video to the repo. Ids follow `chain/sp`'s two-letter scheme: this set is `ad`.

## Inputs

syakegohan is the LEFT board (p1) throughout; the opponent is uyeshota.

| ids | video | WIN counters at the end (syakegohan first) | length |
|---|---|---|---|
| ad00–ad21 | `t3BxXn5MwnM` (Part1) | 15-7 | 34:03 |
| ad22–ad40 | `owRKVhriypk` (Part2) | 15-4 | 18:57 |

syakegohan 30-11 over the 41 games; each part is one whole set.

- The videos: native 854x480, リプレイVer 3.5, the layout the coordinates expect. **No rescale.**
- Games: `seg/` was run per video (`seg/v_<video>/`); `seg` never closes a video's last game, so `mkgames_ss.py`
  appends it (start = previous end + 1.2 s, end = the video's end less 0.2 s) and asserts each game moves one WIN
  counter by one. The chain's winners agree with the counters in all 41 games.

## What differs from chain/sp

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/ss/` |
| `mkgames_ss.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `ss` |
| `corr/merge_xo.py` | three groups (`range(3)`; g2 = the PC items) |
| `corr/dedupe.py` | **new**: run after `merge_xo.py`; drops repeated proposals (asserting they agree) and drops cells the corrected events already give |
| `corr/dedupe_note.txt` | what `dedupe.py` dropped |
| `apply/hand_edits_sp.py` | removed: the cell edit goes straight to `analysis/ppt2-syakegohan/hand-edits.csv` |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 91 flags: 65 PERFECT CLEAR banner onsets, 14 winner KO pieces, 5 KO-tail
   score jumps, 3 T-spins with no banner, 2 banner/type disagreements and 2 banners with no clear. `check/score/`
   found 44 score spots, 5 of them taken as frame-check items.
2. **PERFECT CLEARs.** 24 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 23 clusters
   (`corr/pcclusters.json`), and a lit-cell count of the board after each (`corr/litcount.txt`) left 10 that went to
   a frame check as group g2. All 10 were real PERFECT CLEARs (5 each side) that the chain had not logged as PCs.
3. **Frame checks.** 31 non-PC items; `extractor/autosettle` settled 5 as no change (`corr/out/auto.json`), and the
   other 26 went to two groups (`corr/groups/g0.json`, `g1.json`) beside the 10 PC items (`g2.json`). One agent per
   group proposed corrections (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`): they
   rejected 2.
4. **Merge.** `corr/merge_xo.py` wrote 41 event corrections; `corr/dedupe.py` dropped 5 that repeated another group's
   fix, leaving 36 (`corr/dedupe_note.txt`). `corr/fixwas.py` found no `was` to repair.
5. **Cells.** One: ad22 p1 pieces 95 -> 96 (the T locked on the KO frame). The checkers also proposed `max_combo` and
   `max_b2b` cells; the chain recomputes them from the corrected events and already gives each one, so `dedupe.py`
   dropped them.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted all 82 player-games' spawns with `corr/tools/nextcount.py --game` (the 4-of-5-frame
template from `chain/sp`), and `corr/nc_compare.py` compared them with the table after the cell edit: 72 agree, 7
differ by one and 3 are lost reads. No piece count was changed from it.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty).
