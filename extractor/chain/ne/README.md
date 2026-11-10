# chain/ne: ナリクラ's stream of 2026-11-08 (ranked Puzzle League, then room matches)

112 games, ids `e000`–`e111`, dataset `stream-2026-11-08`, video `RggpNNKC3uI`. This tree is a copy of
`chain/nc`, run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/ne/`, a cloud
session's scratchpad). It adds no frame image or video to the repo.

## Inputs

Tetris matches, first to 2 wins; from e067 on, every match is against ちょこみん.
ナリクラ is the LEFT board (p1) in every game.

| games | opponent | match (ナリクラ–opponent) |
|---|---|---|
| e000–e002 | あ | 2–1 |
| e003–e006 | C1 | 2–0, 2–0 |
| e007–e008 | rez102 | 2–0 |
| e009–e011 | まきょぽん | 2–1 |
| e012–e014 | みしゅ | 1–2 |
| e015–e018 | 3000↑いきたい | 0–2, 2–0 |
| e019–e020 | s0912 | 0–2 |
| e021–e022 | でんでん | 2–0 |
| e023–e024 | まきょぽん | 2–0 |
| e025–e027 | さいこう24REN | 2–1 |
| e028–e029 | テトリスおもろすぎ | 2–0 |
| e030–e039 | さいこう24REN | 2–0, 2–1, 2–0, 1–2 |
| e040–e041 | クッパ | 0–2 |
| e042–e044 | しふとへんこう | 2–1 |
| e045–e046 | しろぜ | 2–0 |
| e047–e052 | クッパ | 2–0, 0–2, 0–2 |
| e053–e054 | つっちー | 2–0 |
| e055–e056 | ちょこみん | 0–2 |
| e057–e058 | クッパ | 2–0 |
| e059–e061 | よしき | 2–1 |
| e062–e064 | ちょこみん | 2–1 |
| e065–e066 | NAOKI | 2–0 |
| e067–e111 | ちょこみん | 0–2, 0–2, 2–1, 0–2, 2–1, 1–2, 0–2, 2–1, 2–0, 1–2, 1–2, 2–0, 2–1, 1–2, 1–2, 0–2, 2–0, 1–1 |

ナリクラ won 28 of the 46 finished matches and 64 of the 112 games. The last match stood at 1–1 when ちょこみん
left the room during the decider (「たいせん相手が抜けた」); that game has no result, is kept in `games_all.json` only
(id `e_left`), and e111 carries `win_counter_after`.

- The video: fetched with yt-dlp through a Tailscale exit node (as for nk and nc), itag 298 (720p60 H.264),
  transcoded once to 854x480 at 30 fps. The result has nc's layout exactly, so nothing is rescaled and nc's
  templates and OCR digit set work unchanged.
- Games: `seg/` as in nc (114 segments after the menu filter). Segment 3 is a Puyo match (character select and two
  Puyo games) and is left out. `mkgames_ne.py` writes `games.json` and `games_all.json` from the WIN-star
  counters (`seg/stars.json`).
- **Match winners by eye.** A match's last game has no counter after it, and `stars.json`'s `wl` is wrong when its
  sample lands on a loading screen, so every match-final winner was read off the WIN banner or WINNER screen
  (`WL_EYE` in `mkgames_ne.py`). One was first misread: e014's KO winner in extractor A disagreed, and the WINNER
  screen at 1416 s names みしゅ. `apply/checks_xo.py` then agreed with every counter winner, 112 of 112.

## What differs from chain/nc

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/ne/`, video `RggpNNKC3uI`, ids `e` |
| `mkgames_ne.py` | this stream's games (replacing `mkgames_nc.py`) |
| `corr/tools/nextcount.py` | reference frame at 880 s (e006); 400 s, nc's, is the character select screen here |
| `corr/merge_xo.py` | e033 p1's cells were proposed by two checkers and are kept once; e108 p2's duplicate at 7438.43 s (A logged a single, B a quad, at the same time) becomes a window that keeps the single |
| `check/pc/strip2.py` | the PC-cluster strip script, copied from nc's run |

`/tmp/claude-0/ne/corr` is a symlink to this tree's `corr/`.

## Corrections

All 27 event corrections and 14 hand edits are in `analysis/ppt2-narikura/`.

1. **Flags.** `apply/checks_xo.py` raised 144 flags (`corr/flags.json`): 81 PERFECT CLEAR banner onsets,
   34 winner KO pieces, 12 gap windows, 5 T-spins with no banner, 4 bad bags, 4 banners with no clear and
   4 KO-tail score jumps.
2. **PERFECT CLEARs.** The table holds 22 PCs, all from `pcmap`. The 33 clusters of short onsets away from an
   accepted PC (`corr/pcclusters.json`) were drawn as strips; every one is a line-clear flash, so
   `corr/hidden_pc.json` is empty.
3. **Frame checks.** `check/score/` found 24 spots (`corr/score/spots.json`). The 63 non-PC flags and the
   spots made 87 items in five groups (`corr/groups/`). One agent per group proposed corrections
   (`corr/out/b*.json`, 29 events and 23 cells), one more per group tried to refute each (`corr/out/v*.json`).
   The skeptics rejected none, amended five and added four:
   - e033 p1's REN is 8, not 9 (nine singles in a row scoring 300 to 1500, and the banner reads 「8 REN」); its
     back-to-back maximum drops to 1;
   - e065's two piece counts (82 → 74 and 83 → 75), which the checker had left for lack of a NEXT-queue total;
   - e099 p2's two rebuilt windows keep their locks but four garbage-row counts change, and its piece count is
     138, not 139; e107 p2 is 45 and e108 p2 52 (the checker had counted the first piece on top of the NEXT
     shifts).
4. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (15 rebuilt windows, 9 retypes, 3 added
   events) and `corr/cells.json` (25 cells). `corr/fixwas.py` ran `w/tetrio/metrics.py`; nothing needed fixing.
5. **Cells.** Of the 25 cell edits, the corrected event list already gives 11 (REN and back-to-back maxima), so
   14 are hand edits: 13 piece counts and e065 p1's REN (20, from the banners 17→18→19→20), where the corrected
   events still give 16.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game` (reference frame
880 s), and `corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 224
player-games, 206 agree exactly, 16 are one piece lower in the recount, 1 is a lost read (e064 p2) and 1 is two
lower (e075 p2). In every one-piece case the table has the extra piece; four of them (e037 p1, e069 p2, e072 p1,
e085 p2) are counts the frame checks raised because the last piece locked on the KO frame, which the recount's
rule (drop a last spawn after the last chain event) leaves out. e075 p2 is the same case plus a hold swap on the
last spawn: the frame check saw the O on the stack at the KO frame and the score's drop points, so 62 stands. No
piece count was changed from the recount alone.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the frames by the checkers, not counted row by
  row by a second reader except in e049 p1 and e099 p2.
- No opener labels (the `opener` column is empty, as for the streams).
