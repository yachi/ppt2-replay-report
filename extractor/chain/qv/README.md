# chain/qv: uyeshota's upload of 2026-11-03 (「VS 最強格」 vs ゆうくん)

23 games, ids `d000`–`d022`, dataset `upload-2026-11-03`, video `qvB4pt22yPw` (「【VS 最強格】ゆうくん【ぷよぷよテトリス2】」).
This tree is a copy of `chain/pp`, run on one uploaded video and kept as it ran (its paths point at
`/tmp/claude-0/qv/`, a cloud session's scratchpad). It adds no frame image or video to the repo.

## Inputs

uyeshota is the LEFT board (p1), ゆうくん the right (p2), so no side swap was needed.

| ids | score (uyeshota-ゆうくん) |
|---|---|
| d000–d022 | 14-9 |

The video ends during game 24 (uyeshota at 14), so the set's last game is not in it and is not in the table.

- The video: 480p h264, then **rescaled** like every uyeshota and amemiya video (`scale=837:470,pad=854:480:8:6`).
- Games: `seg/` as in pp (23 segments, every one a game). `mkgames_qv.py` writes `games.json` and `games_all.json`
  from the WIN counters read by eye off contact sheets (`seg/cnt.py`).

## What differs from chain/pp

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/qv/`, video `qvB4pt22yPw` |
| `mkgames_qv.py`, `drive_s1.sh`, `drive_s2.sh` | this video's games and the two stage drivers |
| banner and word templates, `T.npy` | copied from `chain/pp` (same rescale geometry). Not committed |
| `check/score/scoresum.py` | its `chain/pp/` paths pointed at this run |
| `corr/tools/nextcount.py` | `REF_FRAME_T` set to a clean online frame of this video |
| `corr/merge_xo.py` | one group (`range(1)`) |
| `apply/hand_edits_qv.py` | the hand-edit writer, paths to this run |

As for pp, `corr/tools/score.py` needs `check/ocr/reader.py` copied beside `w/ocr/T.npy`.

## Corrections

All corrections are in `analysis/ppt2-uyeshota/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 34 flags (`corr/flags.json`): 19 PERFECT CLEAR banner onsets,
   11 winner KO pieces, 3 T-spins without a banner and 1 banner without a clear. The WIN counter agrees with the csv
   in 23 of 23 games.
2. **PERFECT CLEARs.** 6 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the others make 6
   clusters (`corr/pcclusters.json`). One rejected onset whose board read low after it (`corr/litcount.out`, d007 p2)
   went to the checker as a frame-check item: it was the banner of the PC already logged, still showing.
   `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 2 spots (`corr/score/spots.json`); both are the T-spins retyped below.
4. **Frame checks.** The 15 flagged events and the PC onset made 16 items in one group (`corr/groups/g0.json`). One
   agent proposed corrections (`corr/out/b0.json`), one more tried to refute each (`corr/out/v0.json`); the skeptic
   kept every proposal and added one the checker had rejected (d021 p1, an I locked on the KO frame).
5. **Merge.** `corr/merge_xo.py` wrote 7 event corrections and 3 cell edits; `corr/fixwas.py` needed no repair.
   - retyped: d006 uyeshota single → T-spin Single, d008 ゆうくん double → T-spin Double, d018 uyeshota double →
     T-spin Double, d019 ゆうくん mini T-spin Single → a zero-line mini T-spin (after it `checks_xo` flags a KO-tail
     score jump of +300 with no clear, which is that mini).
   - added locks with no clear on the KO frame: d001 uyeshota, d009 ゆうくん, d021 uyeshota.
6. **Cells.** The 3 hand edits are those added locks, piece counts one up: d001 uyeshota 37 → 38, d009 ゆうくん
   104 → 105, d021 uyeshota 37 → 38.

## NEXT-queue recount

`corr/drive_nc.sh` and `corr/nc_compare.py` (`corr/nc_compare.json`): of the 46 player-games, 43 agree exactly,
1 differs by one (d001 uyeshota, the hand-edited KO lock, which the recount drops after the last chain event) and 2
lost count (d017 and d018 ゆうくん, the recount 3 and 2 low). No piece count was changed from the recount alone.

## Known gaps

- No opener labels (the `opener` column is empty, as for the streams).
- The set's last game is past the end of the video.
