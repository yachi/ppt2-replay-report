# chain/wr: amemiya's stream of 2026-11-11 (「超久しぶりの連勝企画」)

182 games, ids `g000`–`g181`, dataset `stream-2026-11-11`, video `wrUXrGsHWLU`. This tree is a copy of `chain/te`,
run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/wr/`, a cloud session's
scratchpad). It adds no frame image or video to the repo.

## Inputs

amemiya is the LEFT board (p1) throughout. The stream is a run of first-to-5 sets against whoever joined
(35 sets, 21 opponents); `mkgames_wr.py` holds the full list. amemiya won 168 of the 182 games.

- The video: fetched with yt-dlp through a Tailscale exit node, rescaled as for te (`scale=837:470,pad=854:480:8:6`).
- Games: `seg/` (185 segments). Segment 0 is a COM game and is not counted. Segments 88 (vs だいご at 1-0) and 112
  (vs リミレ at 2-0) end with the opponent disconnected mid-game: they have no result and are in `games_all.json`
  only; the games before them in those sets are counted. Segments 82 and 102 end under the Switch's pause menu, and
  their winner is read off the next segment's starting counter. `mkgames_wr.py` asserts each set ends on 5 (bar the
  two cut sets) and that every segment is used once.

## What differs from chain/te

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/wr/`, video `wrUXrGsHWLU` |
| `mkgames_wr.py`, `drive_s1.sh`, `drive_s2.sh` | this stream's games and the stage drivers |
| `drive_s2b.sh` | re-ran the banner pass with a tight T-SPIN crop |
| banner, word and score-digit templates, `T.npy` | as for te. Not committed |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 215, a clean online frame of this video (game g001) |
| `corr/merge_xo.py` | seven groups (`range(7)`) |
| `apply/hand_edits_wr.py` | the hand-edit writer, paths to this run |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-amemiya/` (appended after the earlier streams').

1. **Flags.** `apply/checks_xo.py` raised 213 flags (`corr/flags.json`): 127 PERFECT CLEAR banner onsets,
   50 winner KO pieces, 14 T-spins with no banner, 7 banner/type disagreements, 7 KO-tail score jumps,
   6 gap windows and 2 bad bags.
2. **PERFECT CLEARs.** 49 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the others make
   38 clusters (`corr/pcclusters.json`). None is a hidden PC, so `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 52 spots; 6 were kept as items.
4. **Frame checks.** 124 items in seven groups (`corr/groups/`), 32 of them games whose PPS fell outside
   0.5–4. One agent per group proposed corrections (`corr/out/b0-b6.json`), one more per group tried to refute
   each (`corr/out/v*.json`). The skeptics kept every proposal but five: group 3's four (all resting on a
   last piece that locked after the game's end) were rejected, and one in group 6 (g148) was amended.
5. **Merge.** `corr/merge_xo.py` wrote 25 event corrections (12 retypes, 9 of them to a T-spin mini; 7 removals;
   3 rebuilt windows; 3 added events) and 16 cell edits. `corr/fixwas.py` ran `w/tetrio/metrics.py`.
6. **Cells.** Of the 16 cell edits, the corrected event list already gives the 6 REN and 1 B2B maxima, so 9 are
   hand edits, all piece counts.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 364 player-games, 332
agree exactly, 25 differ by one piece, 2 are lost reads (g006 p1, g151 p2), and 5 read higher by more than one
(g077, g130, g135 and g179 p2 by two, g157 p2 by four). No piece count was changed from the recount alone, as for
the earlier streams.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
