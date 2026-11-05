# chain/nk: ナリクラ's stream of 2026-11-04 (【ぷよテト2】全世界パズル…, ranked Puzzle League)

67 games, ids `y000`–`y066`, dataset `stream-2026-11-04`, video `m2-MB304ydQ`. This tree is a copy of
`chain/xt`, by way of the amemiya run of 2026-11-03 (`chain/tx`, in a separate pull request), run on one
live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/nk/`, a cloud session's
scratchpad). It adds no frame image or video to the repo.

## Inputs

28 ranked Tetris matches, first to 2 wins; ナリクラ is the LEFT board (p1).

| games | opponent | match (ナリクラ–opponent) |
|---|---|---|
| y000–y009 | にくうどん | 1–2, 0–2, 0–2, 1–2 |
| y010–y013 | かにずし, のこ | 2–0, 2–0 |
| y014–y019 | ずみ, マサムネ | 2–1, 2–1 |
| y020–y023 | sa, harukun101 | 0–2, 0–2 |
| y024–y027 | あ, パルスィ | 2–0, 2–0 |
| y028–y036 | まきょぽん | 2–0, 2–1, 2–0, 0–2 |
| y037–y047 | ゆづり〜ん | 2–0, 2–1, 0–2, 0–2, 0–2 |
| y048–y049 | まきょぽん | 0–2 |
| y050–y055 | ピロ, ayt | 2–1, 2–1 |
| y056–y063 | ゆづり〜ん | 1–2, 2–0, 1–2 |
| y064–y066 | テトリスおもろすぎ | 2–1 |

ナリクラ won 15 of the 28 matches and 34 of the 67 games.

- The video: fetched with yt-dlp through a Tailscale exit node (as for tx). The archive has 360p and
  720p60; the 720p60 stream was transcoded to 854x480.
- **Rescale.** The stream's game layout fills a little more of the frame than in xt's videos, so the
  boards, NEXT queues and banners fell off xt's fixed coordinates; the first run (`old_unscaled/`, not
  committed) read garbage. The transcode shrinks it with `scale=834:469,pad=854:480:10:6`, which puts every board
  cell where xt's coordinates expect it. Check the gridlines against xt's coordinates before running A.
- Games: `seg/` as in xt (67 segments after `par.py`'s menu filter, `seg/seg_games.json`; the stream's
  Puyo matches fall in menu segments). `mkgames_nk.py` writes `games.json` and `games_all.json` (the same
  67 games) from the WIN-star counters read by eye off contact sheets, and asserts each game moves one
  counter by one and each match ends at 2.
- Winners: A's KO winner agrees with the WIN counter on all 67 games.

## What differs from chain/xt

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/nk/`, video `m2-MB304ydQ`, subject narikura |
| `mkgames_nk.py`, `drive_nk1.sh` | this stream's games and stage-1 driver (replacing `mkgames_xt.py`, `drive_xt1.sh`) |
| `w/A/analyze.py` | `WINNER_MIN_FALLBACK = 0.45`: in y022 and y023 the winner's border dims to about 0.5 at the KO, so when no KO passes 0.7 A retries at 0.45 |
| `w/R/banner.py`, `check/pc/banfind_s.py` | banner position: p1 x=79, p2 x=489, y=320 (p2 = p1 + 410) |
| `w/R/banner.py`, `w/R/banscan.py` | **per-side word templates** (`WORDS_P`). The words Single/Double/Triple sit on a blue/purple background on the left and yellow on the right, so a word cut on one side misreads the other (a p1 Triple scored Single 0.85 against Triple 0.67). The first fuse had 301 banner/type disagreements; with one word set per side it has 2 |
| `w/R/banscan.py` | the "Mini" template is cut at 470,325 (Mini sits left of the T here), from p2 3031.0 s |
| banner, Mini and score-digit templates | **recut from this video** (`w/R/fr/`, `check/ocr/`). Not committed |
| `corr/merge_xo.py` | three groups |
| `look/` | not here: no replayed set |

As for xt, `pool/pool.py` needs `pool/out/` to exist and `w/tetrio/metrics.py` needs scipy.
`/tmp/claude-0/nk/corr` is a symlink to this tree's `corr/`.

## Corrections

All 21 event corrections and 5 hand edits are in `analysis/ppt2-narikura/`.

1. **Flags.** `apply/checks_xo.py` raised 104 flags (`corr/flags.json`): 64 PERFECT CLEAR banner onsets,
   22 winner KO pieces, 5 T-spins with no banner, 4 banners with no clear, 3 gap windows, 3 KO-tail score
   jumps, 2 banner/type disagreements, 1 bad bag. No structural failure.
2. **PERFECT CLEARs.** All 17 PCs that `pcmap` accepted show the banner. The 32 clusters of short onsets away
   from an accepted PC (`corr/pcclusters.json`) were drawn as strips; every one is a garbage or clear
   flash, so `corr/hidden_pc.json` is empty.
3. **Frame checks.** `check/score/` found 11 spots (`corr/score/spots.json`). The 40 non-PC flags and the
   spots made 51 items in three groups (`corr/groups/`). One agent per group proposed corrections
   (`corr/out/b*.json`: 22 event corrections, 7 cell edits), one more per group tried to refute each
   (`corr/out/v*.json`). The skeptics kept 27 and rejected 2, both y017 p1's KO piece, which lands one
   frame after the KO; they added none.
4. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (9 retypes, 8 rebuilt windows,
   4 added events) and `corr/cells.json` (6 cells). `corr/fixwas.py` ran `w/tetrio/metrics.py` and found
   no `was` field to repair.
5. **Cells.** Of the 6 cell edits, y025 p2's maximum REN (4 → 5) the corrected event list already gives,
   so 5 are hand edits, all piece counts.
6. Three PERFECT CLEARs (y041 p1, y048 p2 twice) sat on the piece after the one that cleared, where
   `pcmap` had dropped the real event as a double log; they were moved onto the right piece.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 134 player-games,
122 agree exactly, 9 differ by one piece and 2 are unreadable stretches. One differs by more on a clean
read: y022 p2 (harukun101), where the recount is 2 lower than the table's 173. The frame check raised that
count by one for a piece locked on the KO frame, which the skeptic called borderline (the score changes one
frame later). No piece count was changed from the recount alone, as for xo, xt and tx.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- y052 p1: a single at 5243.03 scores +1050 where a single in REN 1 gives 450; the frames show one row
  cleared by a J, so it was left as a single.
- No opener labels (the `opener` column is empty, as for the streams).
