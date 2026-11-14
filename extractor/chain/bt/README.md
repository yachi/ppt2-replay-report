# chain/bt: ナリクラ's stream of 2026-11-12 (「レートでRENするか…♡」, online rated 1v1, first to 2)

79 games, ids `f000`–`f078`, dataset `stream-2026-11-12`, video `4Btsf0blGBQ`. This tree is a copy of `chain/jb`,
run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/bt/`, a cloud session's
scratchpad). It adds no frame image or video to the repo.

## Inputs

ナリクラ is the LEFT board (p1) throughout. The stream's Tetris part is 33 first-to-2 matches against 19 opponent
names (`mkgames_bt.py` holds the list); ナリクラ won 47 of the 79 games. 「???」 is the name as displayed, for four
matches that may be different players.

- The video: fetched with yt-dlp through a Tailscale exit node (native 854x480, larger layout), rescaled to no's
  geometry (`scale=834:468,pad=854:480:10:7`), as for jb.
- Games: `seg/` (78 segments, every one a Tetris-vs-Tetris game). The stream's other stretches are not games: Puyo
  matches and menus, and one Tetris-vs-Puyo match at 5993-6268 s, which is not counted. The last match's 1-1 decider
  (vs かいてと) runs to the end of the video and seg missed it, so it is appended by hand (f078). WIN stars are read by
  `seg/stars_bt.py`; every match's final game is won by the side whose WIN!/LOSE screen shows at its end, read by
  eye. `mkgames_bt.py` asserts each match ends on 2.

## What differs from chain/jb

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/bt/`, video `4Btsf0blGBQ` |
| `mkgames_bt.py`, `seg/stars_bt.py` | this stream's games and the WIN-star reader |
| banner, word and score-digit templates, `T.npy` | as for jb. Not committed |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 204, a clean online frame of this video (game f000) |
| `corr/merge_xo.py` | three groups (`range(3)`) |
| `apply/hand_edits_bt.py` | the hand-edit writer, paths to this run |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-narikura/` (appended after the earlier streams').

1. **Flags.** `apply/checks_xo.py` raised 123 flags (`out/flags.json`): 72 PERFECT CLEAR banner onsets,
   30 winner KO pieces, 7 banners with no clear, 5 gap windows (two at a game's tail), 4 bad bags,
   2 T-spins with no banner, 2 KO-tail score jumps and 1 banner/type disagreement.
2. **PERFECT CLEARs.** 20 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the others make
   34 clusters (`corr/pcclusters.json`), checked on contact sheets four frames per cluster. None is a hidden PC,
   so `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 6 spots; one, 900 points or more unexplained, was kept as an item.
4. **Auto-settle.** `extractor/autosettle/autosettle.py` settled 15 of the KO-piece flags without frames
   (`corr/out/auto.json`, rule `ko-flat-v1`).
5. **Frame checks.** The other 37 items went to three groups (`corr/groups/`). One agent per group proposed
   corrections (`corr/out/b0-b2.json`), one more per group tried to refute each (`corr/out/v*.json`). The skeptics
   kept every proposal, amended the garbage-row counts of two rebuilt windows (f016 p1, f055 p2), and found one
   lock group 0 had missed: in f018 p2 a PERFECT CLEAR double was logged one piece late, which rebuilt 1740.4-1741.1.
6. **Merge.** `corr/merge_xo.py` wrote 13 event corrections (9 rebuilt windows, 2 retypes, 1 added event,
   1 removal) and 11 cell edits. Four of the windows remove phantom locks logged at the same time as real ones
   (f049 p1 at 4936.40 and 4937.87, f061 p1, f065 p2); the merge collapses one-lock-per-entry removals at one time,
   so those were written by hand to keep the real clears and drop exactly the phantoms the checker counted.
   `corr/fixwas.py` then ran `w/tetrio/metrics.py`.
7. **Cells.** Of the 11 cell edits, the corrected event list already gives the 2 REN maxima, so 9 are hand edits,
   all piece counts.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game` (two workers), and
`corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 158 player-games, 134
agree exactly, 19 differ by one piece (18 of them the table one higher) and 2 are lost reads (bad bags or long
unknown stretches: f027 p2, f049 p1). Three clean reads differ by more, each the table higher: f055 p2 by 4,
f059 p2 by 3 and f061 p2 by 2. The first two are already hand edits from frame checks (67 to 65, 63 to 62), so the
recount and the checkers disagree there. No piece count was changed from the recount alone, as for the earlier
streams.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height where the frames were not
  checked row by row.
- No opener labels (the `opener` column is empty, as for the streams).
