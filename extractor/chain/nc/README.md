# chain/nc: ナリクラ's stream of 2026-11-06 (ranked Puzzle League)

99 games, ids `c000`–`c098`, dataset `stream-2026-11-06`, video `QvoCgqvJ6MY`. This tree is a copy of
`chain/nk`, run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/nc/`, a cloud
session's scratchpad). It adds no frame image or video to the repo.

## Inputs

40 ranked Tetris matches, first to 2 wins; ナリクラ is the LEFT board (p1) in every game, even when the
character select shows him as 2P.

| games | opponent | match (ナリクラ–opponent) |
|---|---|---|
| c000–c001 | ¤やなせたかしす¤ | 2–0 |
| c002–c004 | o | 1–2 |
| c005–c006 | あ | 2–0 |
| c007–c009 | ??? | 1–2 |
| c010–c013 | いっせい | 0–2, 0–2 |
| c014–c016 | Xenon/キセノン | 2–1 |
| c017–c021 | ??? | 0–2, 1–2 |
| c022–c023 | たわ | 0–2 |
| c024–c025 | あ | 0–2 |
| c026–c033 | ひろ | 2–1, 2–0, 2–1 |
| c034–c039 | くくすす | 2–1, 1–2 |
| c040–c041 | さむい | 2–0 |
| c042–c043 | ぬ | 2–0 |
| c044–c045 | くくすす | 0–2 |
| c046–c047 | SEGA | 2–0 |
| c048–c049 | ゆび | 2–0 |
| c050–c054 | たわ | 0–2, 2–1 |
| c055–c057 | SEGA | 2–1 |
| c058–c059 | ks | 0–2 |
| c060–c062 | ぬ | 1–2 |
| c063–c064 | いけとろ | 2–0 |
| c065–c070 | SEGA | 2–1, 1–2 |
| c071–c075 | まきょぽん | 0–2, 1–2 |
| c076–c080 | くくすす | 0–2, 1–2 |
| c081–c083 | たなばた | 2–1 |
| c084–c086 | ks | 1–2 |
| c087–c089 | razania | 2–1 |
| c090–c091 | フォス | 2–0 |
| c092–c098 | manato | 2–1, 2–0, 2–0 |

ナリクラ won 21 of the 40 matches and 51 of the 99 games. `???` is the name the game prints for a player whose
name is hidden, so the three `???` rows may be different people. `SEGA` is a CPU opponent.

- Which streams count: of ナリクラ's streams from 2026-11-01 to 2026-11-09, the ones titled 「30REN」 or 「4人」 are
  four-player rooms (11-05, 11-07, 11-09), 「スワップ」 (11-03) is swap mode and 「連鎖」 is Puyo; only the 1v1
  ranked streams (11-06, 11-08) are here.
- The video: fetched with yt-dlp through a Tailscale exit node (as for nk). VP9 itag 244 (480p) was downloaded
  and transcoded once to H.264. It is native 854x480 in nk's rescaled layout, so it is **not** rescaled.
- Games: `seg/` as in nk (99 segments after the menu filter). `mkgames_nc.py` writes `games.json` and
  `games_all.json` from the WIN-star counters read off contact sheets.

## What differs from chain/nk

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/nc/`, video `QvoCgqvJ6MY` |
| `mkgames_nc.py` | this stream's games (replacing `mkgames_nk.py`) |
| `w/R/banner.py`, `w/R/banscan.py` | the banner sits 8 px left and 5 px lower than nk's: T-SPIN p2 at 481,325, words at 510,323 (p1 = −410), Mini at 471,327 |
| banner, Mini and score-digit templates | **recut from this video** (`w/R/fr/`, `check/ocr/`). Not committed |
| `corr/merge_xo.py` | five groups; c085 p1's correction at 6572.47 s was proposed by two checkers and is kept once |

`/tmp/claude-0/nc/corr` is a symlink to this tree's `corr/`.

## Corrections

All 39 event corrections and 12 hand edits are in `analysis/ppt2-narikura/`.

1. **Flags.** `apply/checks_xo.py` raised 111 flags (`corr/flags.json`): 50 PERFECT CLEAR banner onsets,
   28 winner KO pieces, 23 gap windows, 3 T-spins with no banner, 3 KO-tail score jumps, 2 banners with no
   clear, 1 banner/type disagreement, 1 bad bag.
2. **PERFECT CLEARs.** The table holds 19 PCs, all from `pcmap`. The 18 clusters of short onsets away from an accepted PC
   (`corr/pcclusters.json`) were drawn as strips; every one is a line-clear flash, so `corr/hidden_pc.json`
   is empty.
3. **Frame checks.** `check/score/` found 23 spots (`corr/score/spots.json`). The 61 non-PC flags and the
   spots made 84 items in five groups (`corr/groups/`). One agent per group proposed corrections
   (`corr/out/b*.json`), one more per group tried to refute each (`corr/out/v*.json`). The skeptics kept
   all 60 proposals and added one: the lock b1 adds to c047 p1 at 3975.7 s also needs the piece count raised.
4. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (16 rebuilt windows, 12 removals,
   9 retypes, 2 added events) and `corr/cells.json` (21 cells). `corr/fixwas.py` ran `w/tetrio/metrics.py`.
5. **Cells.** Of the 21 cell edits, the corrected event list already gives 9 (REN and back-to-back maxima), so
   12 are hand edits: 11 piece counts and c035 p1's REN, where the chain's run is still cut by a BREAK the
   score does not show. c087 is a slow REN battle (pieces fall at gravity for seconds at a time); both players'
   counts were rebuilt from the NEXT queue and the score.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 198 player-games,
169 agree exactly, 26 differ by one piece and 3 are lost reads (bad bags or long unknown stretches). One count
was changed by the recount: c035 p1, where the frame check took A's 74 pieces as the event count and removed
two phantoms to give 72; the NEXT queue gives 71 shifts less the first hold, 70, equal to the corrected event
count.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- c087 p1's `garbage_received_rows` reads 23 in the chain against 10 from A; nobody checked it in the video.
- No opener labels (the `opener` column is empty, as for the streams).
