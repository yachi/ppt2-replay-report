# chain/xo: uyeshota's stream of 2026-10-30 (てとぼ　レート3500↑)

139 games, ids `u000`–`u138`, dataset `stream-2026-10-30`, video `XoaWLJowuCQ`. This tree is a copy of
`chain/ach` run on one live-stream archive, kept as it ran (its paths point at `/tmp/claude-0/xo/`, a cloud
session's scratchpad). It adds no frame image or video to the repo.

## Inputs

| games | opponent | set (uyeshota–opponent) |
|---|---|---|
| u000–u023 (24) | いんたい | 15–9 |
| u024–u051 (28) | ゆうくん | 13–15 |
| u052–u075 (24) | ゆうくん | 15–9 |
| u076–u094 (19) | ゆうくん | 15–4 |
| u095–u118 (24) | お | 15–9 |
| u119–u138 (20) | お | 15–5 |

- The SnapYT live-archive merge failed in the cloud, so the video was downloaded on the user's computer and
  rescaled here to 854x480 (`scale=837:470,pad=854:480:8:6`, as for the Gg stream). uyeshota is the LEFT board.
- Games: `seg/` as in ach, on one video. `mkgames_xo.py` writes `games_all.json` (139 games) from the WIN-counter
  strings read by eye off contact sheets (`seg/cnt.py`); it asserts the counter rises by one per game.
- **u093 and u094 are not in `games.json`** (137 games). ゆうくん stacked every piece in one column and topped out
  after about 2 s, twice; extractor A returned None on u094 and `R/evrun.py` crashed on it. Both games were counted
  frame by frame instead and are appended by `apply/add_forfeits_xo.py`, then excluded by
  `analysis/ppt2-uyeshota/hand-edits.csv` (the WIN counter still counts them).
- Winners: A's KO winner agrees with the WIN counter on all 137 chain games. uyeshota 88–51 on the counter,
  86–51 over the 137 counted games.

## What differs from chain/ach

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/xo/`; one video |
| `w/B/extract_b.py` | the border-end rule from the Gg run: this capture's frame border glows during play, so the end needs `match < 0.2` for 15 frames (was 0.5 for 10) |
| `w/R/fr/*.png` | banner templates re-cut from this video (not committed) with `check/pc/banfind_s.py`, a streamed banfind over 140–1540 s |
| `check/ocr/` | score-digit templates from six frames read by eye (`mktpl.py`), checked on two held-out frames |
| `witnessed.json` | `[]`; `w/tetrio/metrics.py` needs the file (and scipy) |
| `apply/checks_xo.py`, `pool/pool.py`, `w/tetrio/metrics.py` | player name `uyeshota` |
| `apply/add_forfeits_xo.py` | **new**: the two forfeit games' frame-counted rows |
| `corr/` | the frame-check brief (`BRIEF.md`, `CHECKER.md`, `SKEPTIC.md`), tools, flags, item groups, every proposal and verdict, `merge_xo.py` and `fixwas.py` |

## Corrections

All 70 event corrections and 26 cell edits are in `analysis/ppt2-uyeshota/`.

1. **Flags.** `apply/checks_xo.py` raised 284 flags (`corr/flags.json`): 142 PERFECT CLEAR banner onsets,
   54 winner KO pieces, 25 banners with no clear, 18 gap windows and 3 gap tails, 13 bad bags, 11 T-spins with
   no banner, 10 banner/type disagreements, 8 KO-tail score jumps.
2. **PERFECT CLEARs.** All 61 onsets that `pcmap` accepted show the banner (`check/pc/pcsheet2.py`). Of the
   81 short onsets, the 46 clusters away from an accepted PC (`corr/pcclusters.json`) were drawn by
   `check/pc/pcstrip.py`; every one is a garbage or clear flash, so `corr/hidden_pc.json` is empty.
3. **Frame checks.** `check/score/` (score sum against the event list) found 34 spots in 26 player-games
   (`corr/score/spots.json`). The 142 non-PC flags and the 34 spots made 176 items in six groups
   (`corr/groups/`). One agent per group read the frames and proposed corrections (`corr/out/b*.json`); one
   more agent per group tried to refute each (`corr/out/v*.json`). The skeptics rejected 7 of 108 proposals:
   six added a winner's last piece (in u105 also its lock event) that lands one frame after the KO frame, in
   five games, and one raised a REN maximum (the csv counts REN steps, consecutive clears less one). They amended two, both u101 p2: a piece count that
   counted the first spawn twice, and a REN maximum by the REN-step rule.
   The Workflow tool's concurrency cap is CPUs − 2, two agents on this 4-core container, so the twelve agents
   ran as background Agent calls instead, each skeptic starting as soon as its own checker finished.
4. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` and `corr/cells.json`. `corr/fixwas.py`
   then runs `w/tetrio/metrics.py` and repairs the `was` fields metrics' overlay asserts on: one checker
   wrote the event's garbage count where the overlay wants its PC flag, two retypes gave no `was`, and one
   window held two lock events at the same time where the checker named one. Each repair changes only the
   `was` record, never the correction, and the script refuses one whose kind or line count disagrees.
5. **Cells.** 31 cell edits survived; 5 of them (B2B and REN maxima) the corrected event list already gives,
   so 26 are hand edits, all piece counts.

## NEXT-queue recount

`corr/tools/nextcount.py --game` re-counted every player-game's spawns (`corr/nc_compare.py`, ach's rule: the
first hold into an empty box and an unmatched last spawn taken off). Of the 274 player-games, 251 agree with the
final table exactly, 11 differ by one piece, 8 differ where the reader read bad bags or lost the queue, and 4
differ by more on a clean read: u006 p2 (237 against 240; the frame check removed three phantom locks in one
window and kept 240), u023 p1 (114 against 112, a resync near the KO), u076 p1 (84 against 86, two unmatched chain
events at 4933.0) and u085 p2 (190 against 204, the stretch the skeptic flagged at 5444–5447 s and more). No
piece count was changed from the recount alone; only frame-checked counts were.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- u051 p1's piece count (152) and its rebuilt window are lower bounds (the checker could not see every lock).
- u006 p2, u023 p1, u076 p1 and u085 p2 disagree with the NEXT-queue recount by 2 to 14 pieces (above); their
  piece counts were not changed.
- No opener labels (the `opener` column is empty, as for the streams).
