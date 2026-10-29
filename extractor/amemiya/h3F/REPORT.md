# amemiya PPT2 stream h3FUsPBZmzE: run report

## The video
About 2 h 15 min, 32 parts. Three stretches of online play against ふられ (FT15):

| Segment | Video time | Games | amemiya |
|---|---|---|---|
| set 1 | 1510-3250 s | f000-f026 (+ f027) | 14-13, then f027 ends in a disconnect |
| set 2 | 3308-5485 s | f028-f056 | 15-14 |
| "set 3" | 6100-8077 s | — | the stream re-shows set 1; same boards and scores, not counted |

The first 24 minutes are offline local games (different layout), not read. f027 has no result and is not in the csv;
the WIN counter goes 14-13 into it and the next set starts at 0-0, so `trust.py` takes f026's counter as `14-13`.

## Checks
- Every game has one p1 row, one p2 row and one winner. The winner agrees with the WIN counter in 56/56.
- Result over the 56 read games: amemiya 29-27. ふられ has 22 Perfect Clears; amemiya none.
- PPS outlier: f025 (0.45 for both players): see the lag below.

## Frame check (180 items)
146 chain flags (gap windows, PC banner fixes, KO-frame last piece, bad bags, banner/type disagreements) and 34 KO-tail
score jumps. Kept after the refute pass: 74 event fixes, 87 cell fixes (49 of them reproduced by the re-tally, so 38
went to `hand-edits.csv`), 5 freeze windows. Of the 34 KO-tail spots, 30 changed something; 24 added a missed last piece.

## Freezes and exclusions
- f008 1991.1-1993.6: the stream rolls back about 2.4 s and replays; the duplicate clears are removed.
- f023 2855.9-2859.8: the stream skips game time, then slows down. At least 4 of ふられ's clears fall in the skip,
  so every count is a lower bound. **Excluded.**
- f025 3052.8-3176: 123 of the game's 152 s are heavy lag (a score change every 4-25 s). The clears inside the lag
  were not reconstructed. **Excluded.**
- f040 4233-4286.7 and f042 4467.4-4505.9: lag; counted, with durations that include it (92 s, 2.8% of the
  counted game time), so their PPS and APM read low.
- f052: only p1 stalls; not a freeze.

Counted: 54 games, amemiya 28-26.

## Left open
- f031 p1: an O locked near the KO is not added (the frames do not settle it).
- f040 p2: one bad-bag flag is unresolved.
- Max REN is still from the clear order; f023 and f025 carry max REN edits read off score steps and REN banners, but are excluded.
