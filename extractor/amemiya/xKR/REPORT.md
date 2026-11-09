# amemiya PPT2 stream xKRq6okdeUI: run report

## The video
About 5 h 03 min, 854x480, downloaded with yt-dlp through a Tailscale exit node (the web downloaders refused a fresh
live archive this long). The PPT2 part is the first part; the stream then moves to Kirby Air Riders, which is not read.
amemiya is the LEFT board (p1).

| ids | opponent | set | amemiya |
|---|---|---|---|
| x000-x011 | uyeshota | 15 先, stopped at 5-7 | x012 ends in a disconnect, no result, dropped; the 12 games before it are counted and x011 carries `win_counter_after` 5-7 |
| x013-x041 | uyeshota | 15 先 | 14-15 |
| x042-x045 | いっせい | 3 先 | 3-1 |
| x046-x049 | いっせい | 3 先 | 3-1 |
| x050-x078 | ゆうくん | 15 先 | 14-15 |
| x079-x101 | ゆうくん | 15 先 | 15-8 |
| x102-x128 | ゆうくん | 15 先 | 15-12 |

いっせい is not in the stream title. 128 games, amemiya 69-59 (uyeshota 19-22, いっせい 6-2, ゆうくん 44-35).

Banner templates re-cut from this video: b2 225.0 s, b3 265.0, b_single 1159.3, b_mini2 5843.1, t_pc 5068.0.
Digit templates for the score reader: 5050/2300/3100/4200/5200 s. yt-dlp's DASH file was remuxed with
`-movflags +faststart` before the chain (seek time 2.4 s to 0.14 s, same frames).

## Checks
- Every game has one p1 row, one p2 row and one winner; the winner agrees with the WIN counter in 128/128.
- No PPS or APP outliers after the corrections.

## Frame check (363 items)
272 chain flags (105 PC banner fixes, 47 PC counts, 42 banner/type disagreements, 31 KO-frame last pieces,
20 gap windows, 8 bad bags, 8 T-spins with no banner, 8 banners with no A clear, 3 B truncations) and 91 KO-tail
score jumps. Five readers, five skeptics. The skeptics rejected 23 fixes (most were last pieces logged twice: the chain
logs a clear at spawn, up to 0.7 s before the lock, so a reader matching lock times proposed a duplicate), amended
others and added a few of their own. Kept: 121 event fixes, 152 cell fixes (92 went to `hand-edits.csv`), 6 freeze
windows, no exclusions.

## Lag
x008 747.7-753.1 slow motion, two short freezes each in x076 and x098, and x112 6978.7-6983.0. Counted; their
durations include the lag.

## Left open
- x076 ゆうくん: the NEXT-queue recount could not read the queue (long unknown stretches), so its pieces (340) are the
  event tally. x076 amemiya's recount gives 290, which the hand edit uses.
- x001 amemiya: the NEXT recount gives 81 against the csv's 79; not changed.
- Max REN is still from the clear order.
