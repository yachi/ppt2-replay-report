# chain/tx: amemiya's stream of 2026-11-03 (VS最強格テトラー ゆうくん！テトリス15先2回)

82 games, ids `w000`–`w081`, dataset `stream-2026-11-03`, video `_TXAJq53mWU`. This tree is a copy of
`chain/xt` run on one live-stream archive, kept as it ran (its paths point at `/tmp/claude-0/tx/`, a cloud
session's scratchpad). It adds no frame image or video to the repo.

## Inputs

| games | opponent | set (amemiya–opponent) |
|---|---|---|
| w000–w007 (8) | ゆうくん | 6–2, then a disconnect |
| w008–w032 (25) | ゆうくん | 15–10 |
| w033–w060 (28) | ゆうくん | 15–13 |
| w061–w081 (21) | ぶぶ | 15–6 |

- The video: youtubetoolkit.com refuses an archive this long, so it was fetched with yt-dlp through a Tailscale
  exit node. The archive has only 360p and 720p60; the 720p60 stream was transcoded to 854x480 in chunks (a
  container restart killed a single-pass transcode). amemiya is the LEFT board.
- Games: `seg/` as in xt (85 segments after `par.py`'s menu filter, `seg/seg_games.json`). `mkgames_tx.py` writes
  `games.json` (82 games) and `games_all.json` (plus the disconnect) from the WIN-counter strings read by eye off
  contact sheets (`seg/cnt.py`); it asserts the counter rises by one per game.
- Not counted: segment 0 is a game against COM2; segment 9 (6–2 in the first set) ended in
  「通信相手との接続が切断されました」 with no result (it is in `games_all.json` as `w_disconnect`), after which the
  room was remade and the sets restarted from 0–0; 3918–4789 s and 6023 s on are offline local games
  (amemiyataiyou vs Player 2), and the last segment is another game (Kirby Air Riders).
- No replayed set: the streamer did not seek back in his archive, so xt's `look/` is not here.
- Winners: A's KO winner agrees with the WIN counter on all 82 games. amemiya 51–31.

## What differs from chain/xt

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/tx/`, video `_TXAJq53mWU`, subject amemiya |
| `mkgames_tx.py`, `drive_tx1.sh` | this stream's games and stage-1 driver (replacing `mkgames_xt.py`, `drive_xt1.sh`) |
| banner and score-digit templates | **recut from this video** (xt's are uyeshota's): `check/pc/banfind_s.py` over 2077–3917 s and a `check/pc/bansheet.py` contact sheet, then the T-SPIN Single/Double/Triple/Mini frames picked by hand. Not committed |
| `drive_b.sh` | skips games whose `B/cells2/<id>.npz` exists (resumable) |
| `look/` | not here: no replayed set |

As for xt, `pool/pool.py` needs `pool/out/` to exist and `w/tetrio/metrics.py` needs scipy. `apply/checks_xo.py`
imports `check/ocr/jumps.py`, which must sit beside the OCR output it reads. xt's `corr/` held xt's own outputs
(flags, groups, out); they were moved aside before the checks, and `/tmp/claude-0/tx/corr` is a symlink to this
tree's `corr/` (BRIEF, metrics' correction path and `fixwas.py` use it).

## Corrections

All 55 event corrections and 25 cell edits are in `analysis/ppt2-amemiya/` (after the 10-27 and 10-28 ones).

1. **Flags.** `apply/checks_xo.py` raised 147 flags (`corr/flags.json`): 78 PERFECT CLEAR banner onsets,
   30 gap windows and 2 more at a game's tail, 19 winner KO pieces, 6 banners with no clear, 3 banner/type
   disagreements, 3 T-spins with no banner, 3 KO-tail score jumps, 3 bad bags. No structural failure.
2. **PERFECT CLEARs.** All 22 onsets that `pcmap` accepted show the banner. The 38 clusters of short onsets away
   from an accepted PC (`corr/pcclusters.json`) were drawn by `check/pc/pcstrip.py`; every one is a garbage or
   clear flash, so `corr/hidden_pc.json` is empty. One accepted onset, w068 p2 at 5191.6 s, was a second PC the
   chain had not counted; it went to the frame checks, which confirmed it (23 PCs in all).
3. **Frame checks.** `check/score/` found 29 spots (`corr/score/spots.json`). The non-PC flags, the spots and the
   w068 PC made 99 items in four groups (`corr/groups/`). One agent per group proposed corrections
   (`corr/out/b*.json`), one more per group tried to refute each (`corr/out/v*.json`). The skeptics kept all 94
   proposals and added none.
4. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (20 rebuilt windows, 15 removed events,
   13 retypes, 7 added events) and `corr/cells.json` (39 cells). `corr/fixwas.py` then ran `w/tetrio/metrics.py`
   and found no `was` field to repair.
5. **Cells.** Of the 39 cell edits, 14 the corrected event list already gives, so 25 are hand edits: all piece
   counts but one, w003 p1's maximum REN (14 → 18), whose BREAK at 370.3 s lies outside the rebuilt window.
6. **Lag.** w076 runs in slow motion for about 40 s (5650–5690 s, network lag); its pieces and REN were counted
   frame by frame (p1 71 pieces, REN 13; p2 71 pieces, REN 12). In w020 and w023 the picture freezes for 10–25 s at
   a time. Durations include that time, so those games' rates are low.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` (xo's rule: the first hold into an empty box and an unmatched last spawn taken off) compared
them with the final table (`corr/nc_compare.json`). Of the 164 player-games, 149 agree exactly, 7 differ by one
piece and 3 differ where the reader read bad bags (w036 p2, w055 p1, w067 p1). Five differ by more on a clean
read (no bad bag, no unreadable stretch), and in all five the recount is LOWER than the table: w003 p1 (−3),
w020 p1 (−6), w020 p2 (−4), w023 p2 (−4), w029 p1 (−2). All five are player-games whose piece count the frame
check had already lowered inside its own window, and four sit in w020–w029; in w020 p1 the queue stalls for
10–20 s between spawns (network lag). For w020 p1 the recount agrees with the frame check inside its window (18 spawns
there against its 19) and finds the difference in the first 24 s, outside it. No piece count was changed from
the recount alone, as for xo and xt, so these five may still be too high.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- w060 p2's piece count (93) may be one off.
- No opener labels (the `opener` column is empty, as for the streams).
