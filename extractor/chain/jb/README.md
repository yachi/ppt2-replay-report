# chain/jb: ナリクラ's stream released 2026-11-10 (online 1v1, first to 2)

98 games, ids `d000`–`d097`, dataset `stream-2026-11-10`, video `JBE9iDhAbJI`. This tree is a copy of `chain/no`,
run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/jb/`, a cloud session's
scratchpad). It adds no frame image or video to the repo.

## Inputs

ナリクラ is the LEFT board (p1) throughout. The stream is 40 first-to-2 matches against 22 opponents
(`mkgames_jb.py` holds the list); ナリクラ won 45 of the 98 games.

- The video: fetched with yt-dlp through a Tailscale exit node (native 854x480, larger layout), rescaled to no's
  geometry (`scale=834:468,pad=854:480:10:7`).
- Games: `seg/` (98 segments). Segment 92 is the character-select screen before the ごはんのおとも room match and is
  left out. The last match's 1-1 decider (vs まきょぽん) runs to the end of the video and seg missed it, so it is
  appended by hand. WIN stars are read by `seg/stars_jb.py`; every match's final game is won by the side whose
  WIN!/LOSE screen shows at its end, read by eye. `mkgames_jb.py` asserts each match ends on 2.

## What differs from chain/no

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/jb/`, video `JBE9iDhAbJI` |
| `mkgames_jb.py`, `seg/stars_jb.py` | this stream's games and the WIN-star reader |
| banner, word and score-digit templates, `T.npy` | as for no. Not committed |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 290, a clean online frame of this video (game d000) |
| `corr/merge_xo.py` | four groups (`range(4)`); a single event inside a window the same player's `replace_window` rebuilds is dropped |
| `apply/hand_edits_jb.py` | the hand-edit writer, paths to this run |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-narikura/` (appended after the earlier streams').

1. **Flags.** `apply/checks_xo.py` raised 166 flags (`out/flags.json`): 93 PERFECT CLEAR banner onsets,
   46 winner KO pieces, 9 banners with no clear, 6 bad bags, 6 gap windows (one at a game's tail),
   3 banner/type disagreements and 3 T-spins with no banner.
2. **PERFECT CLEARs.** 32 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the others make
   31 clusters (`corr/pcclusters.json`), checked on contact sheets four frames per cluster. Every one is a
   line-clear or TETRIS flash with garbage left below, so `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 14 spots; none was kept as an item.
4. **Auto-settle.** `extractor/autosettle/autosettle.py` settled 26 of the KO-piece flags without frames
   (`corr/out/auto.json`, rule `ko-flat-v1`: the score did not move between the last spawn and the KO).
5. **Frame checks.** The other 47 items went to four groups (`corr/groups/`). One agent per group proposed
   corrections (`corr/out/b0-b3.json`), one more per group tried to refute each (`corr/out/v*.json`). The skeptics
   kept every proposal but three in group 0: two were rejected (one rested on a lock after the KO) and one piece
   count was amended. Groups 1 and 2 both fixed d045 p1 inside the same window; the rebuilt window agrees with
   group 2's events and is the one kept.
6. **Merge.** `corr/merge_xo.py` wrote 14 event corrections (8 rebuilt windows, 5 retypes, 1 added event) and
   16 cell edits. `corr/fixwas.py` ran `w/tetrio/metrics.py` and needed no repair.
7. **Cells.** Of the 16 cell edits, the corrected event list already gives the 3 REN and 2 B2B maxima, so 11 are
   hand edits, all piece counts.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game` (two workers), and
`corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 196 player-games, 168
agree exactly, 24 differ by one piece (22 of them the table one higher) and 3 are lost reads (bad bags or long
unknown stretches: d060 p2, d061 p1, d069 p1). One clean read differs by more: d063 p1, the table higher by 2. No
piece count was changed from the recount alone, as for the earlier streams.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
