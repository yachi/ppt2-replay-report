# chain/no: ナリクラ's stream of 2026-11-01 (ranked Puzzle League)

82 games, ids `b000`–`b081`, dataset `stream-2026-11-01`, video `QZzZ6dWVqYk`. This tree is a copy of
`chain/ne`, run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/no/`, a cloud
session's scratchpad). It adds no frame image or video to the repo.

## Inputs

Online ranked Tetris matches (「パズルリーグ」), first to 2 wins. ナリクラ is the LEFT board (p1) in every game.

| games | opponent | match (ナリクラ–opponent) |
|---|---|---|
| b000–b004 | こざとへん | 2–1, 0–2 |
| b005–b009 | Yuio | 2–1, 2–0 |
| b010–b012 | ゆうれい | 2–1 |
| b013–b017 | いか | 1–2, 2–0 |
| b018–b020 | イチゴだいふく | 1–2 |
| b021–b022 | すっきーに | 2–0 |
| b023–b025 | てらこ | 1–2 |
| b026–b028 | こまる | 1–2 |
| b029–b030 | みしゅ | 2–0 |
| b031–b033 | たむら | 2–1 |
| b034–b040 | ゆきかき | 2–0, 2–0, 1–2 |
| b041–b042 | みしゅ | 2–0 |
| b043–b044 | ゆきかき | 2–0 |
| b045–b047 | ぬろ | 2–1 |
| b048–b054 | ゆうれい | 1–2, 0–2, 0–2 |
| b055–b057 | こまる | 2–1 |
| b058–b067 | さむい | 0–2, 1–2, 0–2, 2–1 |
| b068–b070 | NAOKI | 2–1 |
| b071–b073 | ゆきかき | 2–1 |
| b074–b075 | Aloud | 2–0 |
| b076–b078 | Ando | 2–1 |
| b079–b081 | おーわ | 2–1 |

ナリクラ won 20 of the 32 matches and 47 of the 82 games.

- The video: fetched with yt-dlp through a Tailscale exit node (as for nk, nc and ne), itag 135 (480p30). Its
  overlay is larger than ne's, so it was rescaled once with `scale=834:468,pad=854:480:10:7`, which puts the
  boards where ne's sit; ne's templates and OCR digit set then work unchanged.
- Games: `seg/` as in ne (82 game segments). The stream's other segments are Puyo matches and menus, checked on a
  contact sheet and left out. `mkgames_no.py` writes `games.json` and `games_all.json` from the WIN-star counters
  (`seg/stars.json`).
- **Match winners by eye.** Every final that started 1–1, and three that looked odd, were read off the WIN!/WINNER
  screen (`WL_EYE` in `mkgames_no.py`). A final that started 1–0 or 0–1 must be won by the leader, because the next
  segment starts 0–0; the asserts check it. `apply/checks_xo.py` then agreed with every counter winner, 82 of 82.

## What differs from chain/ne

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/no/`, video `QZzZ6dWVqYk`, ids `b` |
| `mkgames_no.py` | this stream's games (replacing `mkgames_ne.py`) |
| `corr/tools/nextcount.py` | reference frame at 850 s (b006) |
| `corr/merge_xo.py` | four groups; ne's e108 patch removed, there is no same-time duplicate here |
| `corr/nc_compare.py` | reads the `b` rows |

`/tmp/claude-0/no/corr` is a symlink to this tree's `corr/`.

## Corrections

All 28 event corrections and 9 hand edits are in `analysis/ppt2-narikura/`.

1. **Flags.** `apply/checks_xo.py` raised 140 flags (`corr/flags.json`): 89 PERFECT CLEAR banner onsets,
   34 winner KO pieces, 4 bad bags, 4 banners with no clear, 4 T-spins with no banner, 3 KO-tail score jumps,
   1 gap window and 1 gap window at the tail.
2. **PERFECT CLEARs.** The table holds 26 PCs, all from `pcmap`, each with its banner. The 37 clusters of short
   onsets away from an accepted PC (`corr/pcclusters.json`) were drawn as strips; every one is a line-clear
   flash, so `corr/hidden_pc.json` is empty.
3. **Frame checks.** `check/score/` found 21 spots in 18 player-games (`corr/score/`). The 51 non-PC flags and the
   spots made 72 items in four groups (`corr/groups/`). One agent per group proposed corrections
   (`corr/out/b*.json`, 28 events and 15 cells), one more per group tried to refute each (`corr/out/v*.json`).
   The skeptics kept every proposal and added one: b016 p1's back-to-back maximum is 5, not 3.
4. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (15 retypes, 8 rebuilt windows, 4 added
   events, 1 removed) and `corr/cells.json` (16 cells). `corr/fixwas.py` ran `w/tetrio/metrics.py`; nothing
   needed fixing.
5. **Cells.** Of the 16 cell edits, the corrected event list already gives 7 (REN and back-to-back maxima), so
   9 are hand edits, all piece counts.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game` (reference frame
850 s), and `corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 164
player-games, 148 agree exactly, 14 are one off (12 lower in the recount, 2 higher: b018 p1, b020 p1), none is a
lost read, and 2 are two lower (b059 p2 and b080 p2, neither touched by the frame checks). No piece count was
changed from the recount alone; those two may be high.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the frames by the checkers, not counted row by
  row by a second reader.
- No opener labels (the `opener` column is empty, as for the streams).
