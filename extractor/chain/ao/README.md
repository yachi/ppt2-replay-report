# chain/ao: syakegohan vs しょうがく5ねんせい, 15先 Part1-2 (uploaded 2025-06-25)

39 games, ids `ao00`–`ao38`, dataset `upload-2025-06-25`, two videos. This tree is a copy of `chain/ai`, run on the
two videos together and kept as it ran (its paths point at `/tmp/claude-0/ao/`, a cloud session's scratchpad). It
adds no frame image or video to the repo.

## Inputs

syakegohan is the LEFT board (p1) throughout. The opponent is named as the nameplate reads, しょうがく5ねんせい; the
corpus also holds stream games against しょうがく6ねんせい, probably the same player a year later, but nothing here
links the two and the names are kept apart.

| ids | video | WIN counters at the end (syakegohan first) |
|---|---|---|
| ao00–ao23 | `N6zCCPeWIvM` (Part1) | 15-9 |
| ao24–ao38 | `Yd3EgRMn1Z8` (Part2) | 15-0 |

syakegohan 30-9 over the 39 games.

- The videos: リプレイVer 3.5, fetched at 720p and scaled to 854x480 before the chain ran (no layout rescale).
- Games: `seg/` was run per video (`seg/v_<video>/`); `seg` never closes a video's last game, so `mkgames_ao.py`
  appends it and asserts each game moves one WIN counter by one.

## What differs from chain/ai

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/ao/` |
| `mkgames_ao.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `ao` |
| `corr/dedupe.py` | as in `chain/am`, no NEXT recount decision (`NC = {}`) |
| `corr/dedupe_note.txt` | what `dedupe.py` dropped |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 92 flags: 58 PERFECT CLEAR banner onsets, 15 winner KO pieces, 6 T-spins
   with no banner, 5 banner/type disagreements, 3 KO-tail score jumps, 2 gap windows over 4 s, 2 banners with no
   clear and 1 bad bag. `check/score/` found 26 score spots.
2. **PERFECT CLEARs.** 13 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 20 clusters
   (`corr/pcclusters.json`), checked with a lit-cell count of the board after each (`corr/litcount.txt`); 9 left in
   doubt went to a frame check. The set holds 22 PCs (syakegohan 15, しょうがく5ねんせい 7). As in the earlier sets,
   the chain had logged most missed PCs as a clear with pc=0 and then the same clear again on the next spawn.
3. **Frame checks.** `extractor/autosettle` settled 3 items as no change (`corr/out/auto.json`); the other items went
   to groups g0 (17 items), g1 (17) and g2 (9). One agent per group proposed corrections (`corr/out/b*.json`) and
   another tried to refute each (`corr/out/v*.json`): they kept every one.
4. **Merge.** `corr/merge_xo.py` wrote the event corrections and `corr/dedupe.py` dropped 4 ao15/ao23 retypes that
   g1 and g2 had both proposed, leaving 26 (`corr/dedupe_note.txt`).
5. **Cells.** Two: ao24 p1 pieces 65 -> 63 and ao30 p1 pieces 229 -> 226 (phantom locks the frames do not show).

## NEXT-queue recount

`corr/drive_nc.sh` re-counted all 78 player-games' spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/hand_edits.csv` is the cells without a header): 50 agree,
3 differ by one, one reads two fewer (ao11 p2, 68 against 70) and 24 are lost reads, 22 of them in Part2's games
ao25–ao38, where the recount's NEXT template stops matching for long stretches. That was not chased. No piece count
was changed from the recount.

## Known gaps

- The NEXT recount is mostly blind in Part2 (above), so its piece counts rest on the chain and the frame checks only.
- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty).
