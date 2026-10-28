# amemiya PPT2 stream 4xcAmo-s-Tg: chain run report

This is chain output only: no hand edits, no event corrections, no frame-check round. The old set had two frame-check rounds before it was published.

## What ran (2026-10-27, London time)

| Step | Scripts | Time |
|---|---|---|
| Board counts at 10 fps over the whole video | start/grid.py | ~3 min |
| Start candidates to games | start/mkgames.py (new) | ~3.5 min; 227 candidates, 118 games |
| Extractor A | A/run_all.py | ~5 min |
| Extractor B (sampling + solve_fast) | B/sample.py, B/runner.py | ~3 min |
| Events, T-spin banner scan, fusion | R/part.py, R/evrun.py, R/banscan.py, R/fuse.py | ~6 min |
| Gap/bag checks, reconcile | R/gapchk.py, R/bagchk.py, R/build.py, tetrio/seqs.py | <1 min |
| PERFECT CLEAR banner scan | R/pcscan.py | ~50 min, the slowest stage |
| Tally, pool, csv, checks | R/trust.py, R/pcban.py, tetrio/metrics.py, pool.py, build_games_csv.py, apply/checks_am.py | <1 min |

## Geometry gate
- **On the archived constants it failed.** A's 11x11 sample patches sat on the gridlines, so most cells read as uncertain, and the frame-border reading was about 0.5 instead of 1.0, so the KO detector could not work.
- **Recalibration:** fitted to gridlines on frames 622, 640 and 700 s — cell 16.0 px, board x0 137/556, floor y 391. Every other box was scaled the same way.
- **After recalibration it passed** on frames 622, 640, 700 (k008), 3275 (k041), 5135 (k070) and 8265 (k100):
  - Boards, NEXT and HOLD match the image. The only misses are cells covered by the falling piece, the ghost piece or clear/attack effects.
  - Frame borders read 0.96-1.00, except under a clear flash.

## Games found
227 start candidates; 118 are online Tetris-vs-Tetris games in 5 FT15 sets:

| Games | Opponent | amemiya W-L |
|---|---|---|
| k000-k027 | どらえもん | 15-13 |
| k028-k054 | kazu | 15-12 |
| k055-k077 | kazu | 15-8 |
| k078-k095 | さむい | 15-3 |
| k096-k117 | あ | 15-7 |

The 109 other candidates are not in the csv:
- menus and lobby screens
- pause screens
- a Puyo screen at 25.8 s
- Kirby Air Riders from 9221 s to the end
- about 10-13 offline local games ("amemiyataiyou" vs "Player 2", different stage and HUD), skipped and not measured

## Exclusions
None:
- No player-game is an unresolved lower bound: build.py's unres_pg is empty.
- No game is "not trustworthy": the winner matches the WIN counter in 118/118.
- No non-Tetris-vs-Tetris game entered the csv.

The old reason strings are still wired through metrics.py.

## Sanity checks
- Every game has one p1 row, one p2 row, one winner, a duration above 0 and the same opponent on both rows.
- PPS is within 0.5-4 on all 236 rows.
- APP is within 0-1.5 except k113 p1 at 1.63 (REN 19). That fits amemiya's REN play, which is visible on video, but it is flagged.
- WIN counter cross-check: 118/118 agree. This is a stronger outside check of the winner than the old chain had.
- 105.8 minutes of play in total; mean game 53.8 s.

## Flags (199)

| Issue | Count |
|---|---|
| Gap window over 4 s (B's estimated pieces are added there, defects D2/D3) | 53, plus 2 at the game's end |
| PC-fix lines | 40 |
| Possible KO-frame last piece | 28 |
| Banner with no matching A clear | 29 |
| PC rows | 20 |
| Bad bag | 12 |
| Banner word disagrees with A's line count | 9 |
| A T-spin with no banner | 3 |
| APP outlier (k113 p1) | 1 |
| B truncated (k103) | 1 |
| k085 crash guard | 1 |

- **Unreadable nameplates:** none.
- **Freezes:** most long gaps hit both players at once and the scores do not move on frames (for example k008, 636 s and 642 s are identical). These are stream or online freezes. The durations include the frozen time, so PPS is deflated for those games.

## Deviations from the archived chain
1. Geometry recalibrated. The banner and PERFECT CLEAR templates were re-cut from this video, because the archived templates are not in the repo.
2. D1 fixed in A/analyze.py, as instructed.
3. Crash guard for k085: the frame shows a T-spin Single, so that row needs a frame check.
4. B's solver replaced by perf/solve_fast.py.
5. PC handling uses lg's banner-driven PC fix plus the generic duplicate rule, instead of cVO's hand-made PC table.
   - Result: 22 PCs, all by the opponents; amemiya has none.
   - B's one PC for amemiya (k068) is false: the frame shows garbage left on the board.
6. The per-set hand data files are empty: witnessed REN, KO table, event corrections.
7. pool.py is reduced to one set; its row checks are kept.
8. Game start (D5): A's start is 0.67-0.77 s after the detected start in every game. No game started on READY. As in the old chain, start_s is the detector's time.
9. Four scratch files went to /tmp, outside the allowed tree.

## Not done
- No frame-check round on the 199 flags.
- The offline local games were not measured.
- A and B disagree a lot. Pieces match on only 18 of 234 player-games, because the heavy garbage and REN stacking in this stream are hard for B. Outside the gap windows the csv uses A's values.