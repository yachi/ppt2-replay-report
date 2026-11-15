# chain/sp: syakegohan vs ふれあ, 5先×6 (uploaded 2025-08-16)

45 games, ids `aa00`–`aa44`, dataset `upload-2025-08-16`, six videos. This tree is a copy of `chain/sl`, run on the
six videos together and kept as it ran (its paths point at `/tmp/claude-0/sp/`, a cloud session's scratchpad). It
adds no frame image or video to the repo.

The single letters a–z are all taken as id prefixes in `analysis/ppt2-syakegohan/games.csv`, and ids must stay four
characters (`R/match.py`, `tetrio/metrics.py`, `checks_xo`'s `[:4]`), so this set starts the two-letter scheme:
two letters and two digits. The next sets take `ab`, `ac`, ...

## Inputs

Each video is one set, first to 5. syakegohan is the LEFT board (p1) throughout. The opponent's nameplate reads
ふられ; the uploader's titles say ふれあ, which is the name used here.

| ids | video | score (syakegohan first) |
|---|---|---|
| aa00–aa08 | `qups09IM4MY` | 4-5 |
| aa09–aa17 | `jECOZWLWVLA` | 5-4 |
| aa18–aa23 | `4bOgIVzV4NI` | 5-1 |
| aa24–aa28 | `Q_k8Xkxb3jU` | 5-0 |
| aa29–aa35 | `j4G7JcRSOhs` | 5-2 |
| aa36–aa44 | `kaOfxT1BP-I` | 5-4 |

syakegohan 29-16 over the 45 games, 5 sets to 1.

- The videos: native 854x480, リプレイVer 3.5, the layout the coordinates expect. **No rescale.**
- Games: `seg/` was run per video (`seg/v_<video>/`); `mkgames_sp.py` appends each video's last game and asserts each
  game moves one WIN counter by one and each video ends at 5. Extractor A's winners agree with the counters in all 45
  games.

## What differs from chain/sl

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/sp/`; no rescale |
| `mkgames_sp.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `sp` |
| `corr/merge_xo.py` | four groups (`range(4)`; g3 = the PC items) |
| `corr/tools/nextcount.py` | the NEXT template is the pixels white in at least 4 of 5 frames (20, 25, 30, 35, 40 s), not one frame (below) |
| `corr/dedupe_note.txt` | **new**: the nine corrections dropped after the merge |
| `apply/hand_edits_sp.py` | `hand_edits_sl.py` reading this set's `corr/cells.json` |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 130 flags: 88 PERFECT CLEAR banner onsets, 12 winner KO pieces, 11 T-spins
   with no banner, 7 banner/type disagreements, 7 KO-tail score jumps, 2 gap windows, 2 banners with no clear and 1
   bad bag. `check/score/` found 68 score spots.
2. **PERFECT CLEARs.** 28 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 30 clusters
   (`corr/pcclusters.json`), and a lit-cell count of the board after each (`corr/litcount.txt`) left 13 that went to a
   frame check as group g3. All 13 were real PERFECT CLEARs the chain had logged twice.
3. **Frame checks.** 48 non-PC items in three groups (`corr/groups/g0.json`, `g1.json`, `g2.json`) and the 13 PC
   items (`g3.json`); `extractor/autosettle` settled 2 as no change (`corr/out/auto.json`). One agent per group
   proposed corrections (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`); they kept all of
   them, amended none and added none.
4. **Merge.** `corr/merge_xo.py` wrote 48 event corrections; nine repeated a fix another group had already made and
   were dropped by hand (`corr/dedupe_note.txt`), leaving 39. `corr/fixwas.py` needed no repair.
5. **Cells.** 7 cell edits; the corrected event list already gives four of them (aa18 p1 max REN 8, aa17 p1 max
   back-to-back 11, aa38 p1 max REN 2, aa41 p1 max back-to-back 2), so three are hand edits (`corr/hand_edits.csv`):
   aa00 p1 pieces 349 → 346 (three phantom locks at 60.30), aa01 p2 275 → 276 and aa29 p2 172 → 173 (the KO piece).

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table plus the hand edits (`corr/nc_compare.json`).

The first run built the NEXT-column template from one frame at 30 s, as `chain/sl` does, and lost 26 of the 90
player-games, nearly all in `4bOgIVzV4NI` and `Q_k8Xkxb3jU`: that frame holds a line-clear flash and sparkles beside
the NEXT boxes, which went into the template. A frame at 17 s was worse (82 lost: its template picked up half again as much transient white). The
template is now the pixels white in at least 4 of 5 frames from 20 s to 40 s, so a flash in one frame drops out.

With it, 76 of the 90 agree exactly and 8 are off by one, all recounting one lower (aa02 p2, aa03 p2, aa11 p2, aa20
p1, aa27 p2, aa29 p2, aa38 p2, aa41 p2; aa29 p2 recounts the 172 the hand edit raised to 173). 6 are marked lost
(bad bags or long unreadable stretches), and none was changed: aa01 p2 (275 / 276), aa16 p1 (275 / 272, four bad
bags), aa20 p2 (466 / 464, ten bad bags), aa24 p2 (420 / 425, three bad bags), aa37 p1 (490 / 491, 18 unreadable
stretches) and aa39 p2 (177 / 171, one bad bag).

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- The `jECOZWLWVLA` checker found `check/score/score.py` misreads in places; those spots were settled by eye.
- No opener labels (the `opener` column is empty).
