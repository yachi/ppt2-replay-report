# chain/xt: uyeshota's stream of 2026-11-02 (15先 ×4 回)

104 games, ids `v000`–`v103`, dataset `stream-2026-11-02`, video `XTveY1Z22jU`. This tree is a copy of
`chain/xo` run on one live-stream archive, kept as it ran (its paths point at `/tmp/claude-0/xt/`, a cloud
session's scratchpad). It adds no frame image or video to the repo.

## Inputs

| games | opponent | set (uyeshota–opponent) |
|---|---|---|
| v000–v016 (17) | あ | 15–2 |
| v017–v033 (17) | ふらいこん | 15–2 |
| v034–v048 (15) | ??? | 15–0 |
| v049–v072 (24) | おはゆれ | 15–9 |
| v073–v096 (24) | ろうがい | 15–9 |
| v097–v098 (2) | Solitar | 2–0 |
| v099–v103 (5) | Solitar | 5–0 |

- The video (480p) came from youtubetoolkit.com about 17 h after the stream and was rescaled to 854x480 as for
  xo. uyeshota is the LEFT board.
- Games: `seg/` as in xo (137 segments, `seg/seg_games.json`). `mkgames_xt.py` writes `games.json` (104 games)
  and `games_all.json` (plus the disconnect) from the WIN-counter strings read by eye off contact sheets
  (`seg/cnt.py`); it asserts the counter rises by one per game.
- **The streamer replays his own archive on stream.** Twice he seeks back in his YouTube archive (a fullscreen
  player with a win-prediction overlay) and plays a set again; those segments look like live games. `look/dup.py`
  matches every segment's board against every other's (`look/dup.txt`; `look/rep.py` and `look/title.py` were the
  first looks). Segments 17–26 replay set 1's games 7–16 and 44–60 replay set 2's 27–43; they are dropped. Near
  the end he seeks back during the fifth Solitar game: segment 132 is that game's live start, 133–135 replay
  129–131, and 136 is the replayed copy of 132 that runs to the result screen, so 136 stands for it.
- Also not counted: segment 126 ended in 「通信相手との接続が切断されました」 (no result; it is in
  `games_all.json` as `v_disconnect`), and 127 is a game against COM1.
- Winners: A's KO winner agrees with the WIN counter on all 104 games. uyeshota 82–22.

## What differs from chain/xo

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/xt/`, video `XTveY1Z22jU`; banner and score-digit templates are xo's (not committed) |
| `mkgames_xt.py`, `drive_xt1.sh` | this stream's games and stage-1 driver (replacing `mkgames_xo.py`, `drive_xo1.sh`) |
| `look/` | **new**: the replay finder above |
| `apply/add_forfeits_xo.py` | not here: no forfeit game |
| `corr/merge_xo.py` | four groups (was six); no `was` overrides |
| `corr/drive_nc.sh` | **new**: the NEXT-queue recount of every player-game, two at a time |

`w/tetrio/metrics.py` needs scipy: `drive_c.sh` runs it last under `set -e`, so without scipy it stops silently
after pcmap. `pool/pool.py` needs `pool/out/` to exist.

## Corrections

All 37 event corrections and 10 cell edits are in `analysis/ppt2-uyeshota/` (after xo's).

1. **Flags.** `apply/checks_xo.py` raised 200 flags (`corr/flags.json`): 133 PERFECT CLEAR banner onsets,
   46 winner KO pieces, 6 bad bags, 6 banners with no clear, 3 T-spins with no banner, 3 KO-tail score jumps,
   2 gap windows, 1 banner/type disagreement.
2. **PERFECT CLEARs.** All 58 onsets that `pcmap` accepted show the banner. The 39 clusters of short onsets away
   from an accepted PC (`corr/pcclusters.json`) were drawn by `check/pc/pcstrip.py`; every one is a garbage or
   clear flash, so `corr/hidden_pc.json` is empty.
3. **Frame checks.** `check/score/` found 28 spots (`corr/score/spots.json`). The non-PC flags and the spots made
   98 items in four groups (`corr/groups/`). One agent per group proposed corrections (`corr/out/b*.json`), one
   more per group tried to refute each (`corr/out/v*.json`). The skeptics kept all 51 proposals and added two
   the checkers missed: v023 p1's quad at 1955.67 (garbage cleared 4) and v091 p1's B2B maximum (5 → 4).
4. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (23 retypes, 12 rebuilt windows, 2 added
   events) and `corr/cells.json` (16 cells). `corr/fixwas.py` then ran `w/tetrio/metrics.py` and found no `was`
   field to repair.
5. **Cells.** Of the 16 cell edits, 6 (B2B and REN maxima) the corrected event list already gives, so 10 are hand
   edits, all piece counts.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` (xo's rule: the first hold into an empty box and an unmatched last spawn taken off) compared
them with the final table (`corr/nc_compare.json`). Of the 208 player-games, 200 agree exactly, 5 differ by one
piece and 3 differ where the reader read bad bags (v017 p1, v069 p1, v092 p1); none differs by more on a clean
read. Three of the one-piece differences (v023, v051 and v067, all p1) are pieces the frame check added; no piece
count was changed from the recount alone.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
