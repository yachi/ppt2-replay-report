# chain/ac: uyeshota's upload of 2026-11-10 (vs あちみつ, three first-to-5 sets)

22 games, ids `f000`–`f021`, dataset `upload-2026-11-10`, video `AmcnYVHJOkM` (「良い動きができたセット VS あちみつ」).
This tree is a copy of `chain/pp`, run on one uploaded video and kept as it ran (its paths point at
`/tmp/claude-0/ac/`, a cloud session's scratchpad). It adds no frame image or video to the repo.

## Inputs

**The video is a replay recording with uyeshota on the RIGHT board.** The chain reads it as filmed, so in every file
of this tree p1 is あちみつ (left) and p2 is uyeshota (right). `apply/swap_sides.py` turns the chain table and the
hand edits round before they go into `analysis/ppt2-uyeshota/` (p1 is always the subject there); no event
correction was needed, so nothing else had to be turned.

| ids | set | score (あちみつ-uyeshota) |
|---|---|---|
| f000–f007 | 1 | 3-5 |
| f008–f014 | 2 | 2-5 |
| f015–f021 | 3 | 2-5 |

uyeshota 15-7 over the 22 games, all three sets.

- The video: 480p h264, then **rescaled** like every uyeshota and amemiya video (`scale=837:470,pad=854:480:8:6`).
- Games: `seg/` as in pp (22 segments, every one a game). `mkgames_ac.py` writes `games.json` and `games_all.json`
  from the WIN counters read by eye off contact sheets (`seg/cnt.py`). The upload cuts between sets, so no set final
  runs into the next set's room.

## What differs from chain/pp

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/ac/`, video `AmcnYVHJOkM` |
| `mkgames_ac.py`, `drive_s1.sh`, `drive_s2.sh` | this video's games and the two stage drivers |
| banner and word templates, `T.npy` | copied from `chain/pp` (same rescale geometry). Not committed |
| `check/score/scoresum.py` | its `chain/pp/` paths pointed at this run |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 75, a clean online frame of this video (game f001) |
| `corr/merge_xo.py` | one group (`range(1)`) |
| `apply/hand_edits_ac.py` | the hand-edit writer, paths to this run (left/right frame) |
| `apply/swap_sides.py` | **new**: turns the table and the hand edits round so that p1 is uyeshota |

As for pp, `corr/tools/score.py` needs `check/ocr/reader.py` copied beside `w/ocr/T.npy`.

## Corrections

All corrections are in `analysis/ppt2-uyeshota/` (appended after the earlier datasets'), in the swapped frame.

1. **Flags.** `apply/checks_xo.py` raised 45 flags (`corr/flags.json`): 40 PERFECT CLEAR banner onsets and 5 winner
   KO pieces. The WIN counter agrees with the csv in 22 of 22 games.
2. **PERFECT CLEARs.** 17 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the others make 11
   clusters (`corr/pcclusters.json`). The 3 rejected onsets whose board read low after them (`corr/litcount.out`)
   went to the checker as frame-check items; each was the banner of a PC already logged, still showing. 
   `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 3 spots (`corr/score/spots.json`), none large enough to keep.
4. **Frame checks.** The 5 KO pieces and the 3 PC onsets made 8 items in one group (`corr/groups/g0.json`). One
   agent proposed corrections (`corr/out/b0.json`), one more tried to refute each (`corr/out/v0.json`); the skeptic
   kept both proposals.
5. **Merge.** `corr/merge_xo.py` wrote no event correction and 2 cell edits; `corr/fixwas.py` needed no repair.
6. **Cells.** Both are hand edits, piece counts one up: f008 あちみつ 51 → 52 and f018 uyeshota 133 → 134, a piece
   out of HOLD that locks by the KO frame without clearing a line.

## NEXT-queue recount

`corr/drive_nc.sh` and `corr/nc_compare.py` (`corr/nc_compare.json`, left/right frame): of the 44 player-games, 41
agree exactly and 3 differ by one, each the table one higher: the two hand-edited ones (the recount drops a spawn
after the last chain event, which is where those locks are) and f021 uyeshota. No piece count was changed from the
recount alone.

## Known gaps

- No opener labels (the `opener` column is empty, as for the streams).
