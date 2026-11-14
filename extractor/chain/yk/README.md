# chain/yk: amemiya's stream of 2026-11-12 (「【VS最強格テトラー】uyeshota！テトリス15先×2回」)

51 games, ids `a000`–`a050`, dataset `stream-2026-11-12`, video `YkPw_o7t6no`. This tree is a copy of `chain/oc`,
run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/yk/`, a cloud session's
scratchpad). It adds no frame image or video to the repo.

## Inputs

amemiya is the LEFT board (p1) throughout.

| ids | opponent | set |
|---|---|---|
| a000–a026 | uyeshota | 12-15 |
| a027–a050 | uyeshota | 9-15 |

amemiya 21-30 over the 51 games.

- The video: fetched with yt-dlp through a Tailscale exit node, rescaled as for oc (`scale=837:470,pad=854:480:8:6`).
- Games: `seg/` as in oc (55 segments). Segment 0 is a COM game, and the first 47 minutes (one long stretch
  before 2891 s) are local games against 「Player 2」: neither is counted. Segments 52-54 are Kirby Air Riders after
  the PPT2 part. `mkgames_yk.py` writes `games.json` and `games_all.json` from the WIN counters read by eye off
  contact sheets, and asserts each game moves one counter by one and each set ends on its final score.

## What differs from chain/oc

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/yk/`, video `YkPw_o7t6no` |
| `mkgames_yk.py`, `drive_s1.sh`, `drive_s2.sh` | this stream's games and the stage drivers |
| banner, word and score-digit templates, `T.npy` | as for oc. Not committed |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 2950, a clean online frame of this video (game a000) |
| `corr/merge_xo.py` | three groups (`range(3)`) |
| `apply/hand_edits_yk.py` | the hand-edit writer, paths to this run |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-amemiya/` (appended after the earlier streams').

1. **Flags.** `apply/checks_xo.py` raised 91 flags (`corr/flags.json`): 52 PERFECT CLEAR banner onsets,
   12 winner KO pieces, 8 banner/type disagreements, 6 gap windows (two at a game's tail), 5 T-spins with no
   banner, 3 bad bags, 2 banners with no clear, 2 unresolved lower bounds and 1 KO-tail score jump.
2. **PERFECT CLEARs.** 21 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the others make
   22 clusters (`corr/pcclusters.json`). None is a hidden PC, so `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 28 spots (`corr/score/spots.json`); 3 were kept as items.
4. **Frame checks.** The 39 non-PC flags and the 3 spots made 42 items in three groups (`corr/groups/`).
   One agent per group proposed corrections (`corr/out/b0-b2.json`), one more per group tried to refute each
   (`corr/out/v*.json`). The skeptics kept all 26 proposals and added one the checker had left: a TSD
   (a T-spin Double) for a020 p1 at 4138.77 s.
5. **Merge.** `corr/merge_xo.py` wrote 15 event corrections (10 rebuilt windows, 4 retypes, 1 added event) and
   12 cell edits. `corr/fixwas.py` ran `w/tetrio/metrics.py` and needed no repair.
6. **Cells.** Of the 12 cell edits, the corrected event list already gives the 2 REN and 2 B2B maxima, so 8 are
   hand edits, all piece counts.
7. **a037** stays an unresolved lower bound: a Switch HOME menu covers the board at the KO, so the chain's
   coverage ends before the game does and the game is excluded from the totals.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game` (one worker), and
`corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 102 player-games, 92 agree
exactly, 8 differ by one piece and 2 are lost reads (bad bags: a004 p1 and a037 p2, the latter the HOME-menu game).
No piece count was changed from the recount alone, as for xo, xt, tx, nk, aj and oc.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
