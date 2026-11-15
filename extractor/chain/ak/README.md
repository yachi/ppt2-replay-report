# chain/ak: syakegohan vs あちみつ, 15先×2 in one video (uploaded 2025-07-11)

35 games, ids `ak00`–`ak34`, dataset `upload-2025-07-11`, one video. This tree is a copy of `chain/ai`, run on the
video and kept as it ran (its paths point at `/tmp/claude-0/ak/`, a cloud session's scratchpad). It adds no frame
image or video to the repo. Ids follow `chain/sp`'s two-letter scheme: this set is `ak`.

## Inputs

syakegohan is the LEFT board (p1) throughout (nameplate akashirobo1); the opponent is あちみつ.

| ids | video | WIN counters at each set's end (syakegohan first) |
|---|---|---|
| ak00–ak18 | `U1yBGMCQR_A`, first set | 15-4 |
| ak19–ak34 | `U1yBGMCQR_A`, second set (the counters reset) | 15-1 |

syakegohan 30-5 over the 35 games.

- The video is a PS4 capture of リプレイVer 3.5 whose board sits smaller than the layout the coordinates expect. It
  was fetched at 720p, scaled to 854x480 and then rescaled with `scale=837:470,pad=854:480:8:6` before the chain ran.
- Games: `seg/` was run on the video (`seg/v_U1yBGMCQR_A/`); `seg` never closes the last game, so `mkgames_ak.py`
  appends it and asserts each game moves one WIN counter by one, resetting the counters at the second set.

## What differs from chain/ai

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/ak/` |
| `mkgames_ak.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `ak` |
| `w/R/pcon.py` | PERFECT CLEAR banner threshold `o` 0.08 -> 0.04: this capture draws the banner at `o` 0.05-0.13, so at 0.08 no onset lasted 0.9 s and the chain found no PC |
| `corr/dedupe.py` | as in `chain/saj`, no NEXT recount decision (`NC = {}`) |
| `corr/dedupe_note.txt` | what `dedupe.py` dropped and decided |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 100 flags, 83 of them PERFECT CLEAR banner onsets.
2. **PERFECT CLEARs.** 19 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`), and the lit-cell count of
   the board after each confirmed all 19; the other onsets in `corr/pcclusters.json` are repeats of those. The set holds
   19 PCs (syakegohan 14, あちみつ 5).
3. **Frame checks.** `extractor/autosettle` settled 1 item as no change (`corr/out/auto.json`); the other 19 went to
   group g0. One agent proposed corrections (`corr/out/b0.json`) and another tried to refute each (`corr/out/v0.json`):
   it kept all of them.
4. **Merge.** `corr/merge_xo.py` wrote 11 event corrections and `corr/dedupe.py` dropped none: ak01 p1 rebuilt (a TSD
   then a garbage Tetris), two ak04 p1 Tetrises moved to where they happened, a mini TSS that was a plain lock, two TSS
   read as TSD, an O single, and three winner KO pieces (ak09, ak24, ak32).
5. **Cells.** Three, all piece counts, each a KO-frame or opening lock the chain missed: ak09 p1 25 -> 26 (a
   frame-by-frame count of the game found 26 locks), ak24 p1 78 -> 79 and ak32 p1 213 -> 214.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted all 70 player-games' spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/hand_edits.csv` is the cells without a header): 47 agree,
7 differ by one, 15 are lost reads (bad bags or long unknown stretches, all but one on あちみつ's side) and one reads
more: ak09 p1, 24 against 26, where five pieces came out of a full hold and the recount misses them. No piece count
was changed from the recount.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty).
