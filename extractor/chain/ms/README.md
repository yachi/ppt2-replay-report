# chain/ms: syakegohan's upload of 2026-11-10 (vs どらえもん, 15先あきぬけ)

156 games, ids `p000`–`p155`, dataset `upload-2026-11-10`, video `mtslCN3qVDY`. This tree is a copy of
`chain/qh`, run on one uploaded video and kept as it ran (its paths point at `/tmp/claude-0/ms/`, a cloud
session's scratchpad). It adds no frame image or video to the repo.

## Inputs

The upload is titled 「vs ドラえもんさん 15先あきぬけ」: seven sets, each first to 15. syakegohan is the LEFT board
(p1) throughout; the opponent's nameplate reads どらえもん.

| ids | set | score |
|---|---|---|
| p000–p020 | 1 | 15-6 |
| p021–p039 | 2 | 15-4 |
| p040–p065 | 3 | 15-11 |
| p066–p088 | 4 | 15-8 |
| p089–p117 | 5 | 14-15 |
| p118–p136 | 6 | 15-4 |
| p137–p155 | 7 | 15-4 |

syakegohan 104-52 over the 156 games, six sets to one.

- The video: native 854x480 h264, the layout qh's coordinates expect. **No rescale.**
- Games: `seg/` as in qh (156 segments after the menu filter, every one a game). `mkgames_ms.py` writes
  `games.json` and `games_all.json` from the WIN counters read by eye off contact sheets (`seg/cnt/`), and asserts
  each game moves one counter by one and each set ends on its final score.
- **Set finals.** The upload is edited: every set's last game cuts straight to the next set's room. Its end is the
  first end-dialog or loading frame (`seg/fin_ms.py` → `seg/fin_load.json`), and its winner is the WIN pill 1 s
  before it.

## What differs from chain/qh

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/ms/`, video `mtslCN3qVDY` |
| `mkgames_ms.py`, `drive_s1.sh`, `drive_s2.sh` | this video's games and the two stage drivers |
| `seg/fin_ms.py`, `fin_load.json` | the set-final reads above |
| banner, word and score-digit templates | copied from `chain/fs` (same font, same native layout); `check/ocr/mktpl.py` was not run, and `reader.py` read frames at 600, 1500, 3000, 5000 and 8000 s correctly. Not committed |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 220, a clean online frame of this video (game p004) |
| `corr/merge_xo.py` | nine groups (`range(9)`) |
| `corr/nc_compare.py` | compares with this run's chain table plus its hand edits, not with `games.csv` |
| `apply/hand_edits_ms.py` | the hand-edit writer, paths to this run |

As for qh, `pool/pool.py` needs `pool/out/` to exist, `w/tetrio/metrics.py` needs scipy and `witnessed.json`
(`[]` here), `check/score/steps.py` needs `corr/score/`, and `corr/tools/score.py` needs `check/ocr/reader.py`
beside `w/ocr/T.npy`.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 325 flags (`corr/flags.json`): 181 PERFECT CLEAR banner onsets,
   47 winner KO pieces, 29 gap windows, 24 banner/type disagreements, 17 KO-tail score jumps, 15 T-spins with no
   banner, 8 banners with no clear, 3 bad bags and 1 APP outlier.
2. **PERFECT CLEARs.** 65 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). The others make
   62 clusters (`corr/pcclusters.json`). A lit-cell count of the board after each (`corr/litcount.out`) reads a
   stack after most; the 11 rejected onsets whose board read near-empty went to the checkers as frame-check
   items rather than straight into `corr/hidden_pc.json`, which is therefore empty.
3. **Score spots.** `check/score/` found 110 spots (`corr/score/spots.json`); 13 were kept as items.
4. **Frame checks.** The 144 non-PC flags, the 11 PC onsets and the 13 spots made 168 items in nine groups
   (`corr/groups/`). One agent per group proposed corrections (`corr/out/b*.json`), one more per group tried to
   refute each (`corr/out/v*.json`). The skeptics kept 132 proposals, amended 2 and rejected none, and added one
   the checker had left: p039 p1's last O, which locks on the KO frame (an added event and a piece count).
5. **Merge.** `corr/merge_xo.py` wrote 100 event corrections (42 rebuilt windows, 41 retypes, 9 removals,
   8 added events; 16 of them carry a PERFECT CLEAR) and 36 cell edits. `corr/fixwas.py` ran
   `w/tetrio/metrics.py` and needed no repair.
6. **Cells.** Of the 36 cell edits, the corrected event list already gives the 14 REN and B2B maxima, so 22 are
   hand edits, all piece counts.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game` (two workers), and
`corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 312 player-games, 278
agree exactly, 24 differ by one piece (21 of them the table one higher) and 7 are lost reads (bad bags or long
unknown stretches: p034 p2, p117 p2, p122 p1, p134 p2, p141 p2, p152 p2, p153 p2). Three clean reads differ by
more, each the table higher: p031 p1 by 3, p038 p1 by 2 and p141 p1 by 6. No piece count was changed from the
recount alone, as for qh and fs.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the other videos).
