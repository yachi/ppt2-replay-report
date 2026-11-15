# chain/so: syakegohan vs kazu, 15先×2 (uploaded 2025-08-22)

44 games, ids `f000`–`f043`, dataset `upload-2025-08-22`, two videos. This tree is a copy of `chain/sn`, run on the
two videos together and kept as it ran (its paths point at `/tmp/claude-0/so/`, a cloud session's scratchpad). It
adds no frame image or video to the repo.

## Inputs

Each video is one set, first to 15. syakegohan is the RIGHT board in both.

| ids | video | opponent | score (syakegohan first) |
|---|---|---|---|
| f000–f025 | `Pjn05duM_gQ` (Part1) | kazu | 15-11 |
| f026–f043 | `r4sZZlfYNqI` (Part2) | kazu | 15-3 |

syakegohan 30-14 over the 44 games, both sets.

- The videos: native 854x480, recorded as リプレイVer 3.5, the layout the coordinates expect. **No rescale.**
- Sides: the chain reads the LEFT board as p1, so inside this tree p1 is kazu and p2 is syakegohan.
  `apply/swap_sides.py` turns the table and the hand edits round so that p1 is syakegohan, and
  `apply/swap_events.py` flips `side` in the event corrections the same way (as for `chain/sn`).
- Games: `seg/` was run per video (`seg/v_<video>/`); `mkgames_so.py` appends each video's last game and asserts
  each game moves one WIN counter by one and each video ends at 15. Extractor A's winners agree with the counters in
  all 44 games.

## What differs from chain/sn

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/so/`; no rescale |
| `mkgames_so.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `so` |
| `corr/merge_xo.py` | three groups (`range(3)`; g2 = the PC items) |
| `corr/extra/` | removed (sn's g3 item; no extra group here) |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 40 s for both videos |
| `corr/dedupe_note.txt` | **new**: the five corrections dropped after the merge (below) |
| `apply/hand_edits_so.py` | `hand_edits_se.py` reading this set's `corr/cells.json` |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets'), in
the swapped frame (p1 = syakegohan). The files under `corr/` are in the chain's frame (p1 = kazu).

1. **Flags.** `apply/checks_xo.py` raised 110 flags: 84 PERFECT CLEAR banner onsets, 11 winner KO pieces, 8
   banner/type disagreements, 4 T-spins with no banner and 3 banners with no clear. `check/score/` found 39 score
   spots.
2. **PERFECT CLEARs.** 22 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 29 clusters
   (`corr/pcclusters.json`), and a lit-cell count of the board after each (`corr/litcount.txt`) left the 18 items of
   group g2. All 18 were real PERFECT CLEARs the chain had logged twice.
3. **Frame checks.** Non-PC items in two groups (`corr/groups/g0.json`, `g1.json`) and the PC items (`g2.json`);
   `extractor/autosettle` settled 6 as no change (`corr/out/auto.json`). One agent per group proposed corrections
   (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`). The skeptics rejected none and
   amended two: f028 kazu's clear is a double with no garbage row, and f038's PC clears no garbage row.
4. **Merge.** `corr/merge_xo.py` wrote 40 event corrections; five were dropped by hand (`corr/dedupe_note.txt`),
   leaving 35. Four g2 windows (f006 p1 339.27, f017 p1 1086.87, f032 p1 586.17, f033 p1 666.83) repeated retypes
   g0 had already proposed, so the retypes were kept. g1's retype of f038 p1 1068.53 conflicted with g2's window
   there (the PC is on the Z spawned at 1067.63; 1068.53 is a plain lock, and `score.py` shows one jump, +4650 at
   1068.47), so g2's window was kept. `corr/fixwas.py` needed no repair.
5. **Cells.** 2 cell edits; the corrected event list already gives f028's max REN, so one is a hand edit
   (`corr/hand_edits.csv`): f010 kazu's pieces 136 → 137 (p2 after the swap).

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table plus the hand edit (`corr/nc_compare.json`, chain frame). Of the 88
player-games 74 agree exactly and 8 are off by one: seven recount one lower (f010 kazu among them, the KO piece the
hand edit adds) and one (f025 kazu) one higher. f030 syakegohan recounts two lower (192 against 194) with no bad bag
or unreadable stretch; the table stands, as for the earlier sets' undercounts. 5 are marked lost (bad bags or long
unreadable stretches), all on syakegohan's board: f001 (148 / 145), f012 (132 / 139), f017 (120 / 125), f027
(319 / 320) and f037 (29 / 33). None was changed.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty).
