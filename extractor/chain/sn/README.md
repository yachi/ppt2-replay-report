# chain/sn: syakegohan vs あてん, 5先あきぬけ ×3 (uploaded 2025-12-22)

17 games, ids `e000`–`e016`, dataset `upload-2025-12-22`, three videos. This tree is a copy of `chain/sm`, run on the
three videos together and kept as it ran (its paths point at `/tmp/claude-0/sn/`, a cloud session's scratchpad). It
adds no frame image or video to the repo.

## Inputs

Each video is one set, first to 5. These uploads are recorded as 「リプレイVer 4.0」, which draws the boards about 2%
larger than the earlier uploads, and syakegohan is the RIGHT board.

| ids | video | opponent | score (syakegohan first) |
|---|---|---|---|
| e000–e006 | `ewFgsvZkuII` | あてん | 5-2 |
| e007–e011 | `jeH2N-kjDUw` | あてん | 5-0 |
| e012–e016 | `lK7Nd8Nqh1c` | あてん | 5-0 |

syakegohan 15-2 over the 17 games, all three sets.

- The videos: native 854x480, **rescaled** with `scale=836:470,pad=854:480:9:5` (as for `chain/se`) when they were
  downloaded. On the native video extractor A's border feature reads about 0.5 instead of 0.95, every game gets a
  false early KO and `pcmap` finds no PC; after the rescale it reads 0.8–1.0.
- Sides: the chain reads the LEFT board as p1, so inside this tree p1 is あてん and p2 is syakegohan.
  `apply/swap_sides.py` (chain/ac's) turns the table and the hand edits round so that p1 is syakegohan, and
  `apply/swap_events.py` flips `side` in the event corrections the same way.
- Games: `seg/` was run per video (`seg/v_<video>/`); `mkgames_sn.py` appends each video's last game as `chain/sm`
  does and asserts each video ends at 5.

## What differs from chain/sm

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/sn/`; the rescale above |
| `mkgames_sn.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `sn` |
| `w/A/analyze.py` | a 4-line clear read as a T piece is typed `quad` (it cannot be a T-spin); e007 raised `KeyError: None` |
| `corr/merge_xo.py` | three groups (`range(3)`; g2 = the PC items) |
| `corr/extra/` | g3: one more item (e014 p1's T-spin Triple), checked after the merge; no change |
| `corr/tools/nextcount.py` | `REF_FRAME_T` per video (25 s, 40 s, 40 s): no single time has both NEXT columns at rest in all three |
| `apply/hand_edits_sn.py` | `hand_edits_se.py` reading this set's `corr/cells.json` |
| `apply/swap_sides.py`, `apply/swap_events.py` | **new**: the side swap above |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets'), in
the swapped frame (p1 = syakegohan). The files under `corr/` are in the chain's frame (p1 = あてん).

1. **Flags.** `apply/checks_xo.py` raised 42 flags: 16 banner/type disagreements, 12 PERFECT CLEAR banner onsets,
   5 banners with no clear, 5 winner KO pieces, 2 KO-tail score jumps, 1 T-spin with no banner and 1 bad bag.
   `check/score/` found 30 score spots.
2. **PERFECT CLEARs.** 2 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 6 clusters
   (`corr/pcclusters.json`), and a lit-cell count of the board after each (`corr/litcount.txt`) left the items of
   group g2.
3. **Frame checks.** Non-PC items in two groups (`corr/groups/g0.json`, `g1.json`) and the PC items (`g2.json`);
   `extractor/autosettle` settled 5 as no change (`corr/out/auto.json`). One agent per group proposed corrections
   (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`). The skeptics kept every proposal and
   amended one (e013 p2's triple PC: the cleared rows are all piece colours, so `gc` is 0, not 1).
4. **Merge.** `corr/merge_xo.py` wrote 25 event corrections. Most are retypes: six T-spin Singles that were T-spin
   Doubles (and one that was a Triple), 4-line clears typed `tst` or `tsmini` that were T-spin Doubles or quads, and
   one T-spin Double that was a Triple. The rest rebuild short windows: e004 あてん's two phantom locks, missed singles
   in e009 and e012, e011 syakegohan's TSS, and the PERFECT CLEARs of e013 and e014, which the chain had logged on the
   wrong lock. `corr/fixwas.py` needed no repair.
5. **Cells.** 4 cell edits; the corrected event list already gives e012's max REN, so 3 are hand edits
   (`corr/hand_edits.csv`): the KO piece of e003 and e004 on syakegohan's board, and e004 あてん's two phantom locks.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/nc_compare.json`, chain frame). Of the 34 player-games 23
agree exactly and 2 recount one lower (e003 and e004 syakegohan, the KO piece the hand edits add). 9 are marked lost
(bad bags or long unreadable stretches), 8 of them on syakegohan's board, and none was changed: e006 あてん (54 against
55), and syakegohan's e007 (178 / 183), e008 (55 / 62), e010 (47 / 48), e011 (196 / 193), e012 (65 / 66), e014
(84 / 107), e015 (62 / 80) and e016 (27 / 32).

With the single 30 s reference frame `chain/sm` used, 27 of the 34 came back lost: at 30 s the NEXT columns of the
first two videos are mid-animation, so the template matched nothing. The per-video times were picked by the template
score over 50–70 s of each video.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- the large lost recounts on syakegohan's board (e014, e015) are not explained piece by piece.
- No opener labels (the `opener` column is empty).
