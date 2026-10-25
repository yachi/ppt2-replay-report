# chain/TJc: the 2026-10-18 set vs ぶぶ (`TJcCRfhwNNI`)

64 games, ids `k000`–`k063`, dataset `stream-2026-10-18`. This tree is a copy of `chain/cVO/w` run on the
new video, kept as it ran (its paths point at `/tmp/claude-0/chain/kbb/`). It adds no frame image to the repo.

## Inputs

- Video: 480p MP4 from SnapYT (`seg/snap480.js VIDEO_ID 7`), since yt-dlp is blocked from the cloud host.
- Games: `games.json`. Starts come from `seg/seg.py` (both boards empty for at least 0.8 s, then filling)
  and `seg/gamefilter.py` (drops menu screens). Winners come from `seg/winner.py` (WIN-counter changes). The
  start sits 0.67–0.77 s before A's first queue shift, the same offset the repo's cVO2 starts have, so it
  keeps the 0.1–0.2 s-before-GO convention. 50–14 to syakegohan, matching the WIN counter.

## What differs from chain/cVO/w

| file | change |
|---|---|
| all | paths rewritten to the new work tree and video |
| `B/extract_b.py` | imports `solve_fast.solve` (`extractor/perf/solve_fast.py`, byte-identical output) |
| `R/fr/*.png` | banner templates rebuilt from cVO2 480p frames (TST 192.53 s, TSD 165.07 s, TSS 254.23 s, +0.5 s). Not committed: they are frame crops. No Mini banner was found, so `b_mini2.png` is blank and **T-spin Minis are not detected** (`tsmini` is 0 on every row) |
| `R/kofinal.py` | **new.** A never tallies its last spawn interval, so the winner's final piece (and its clear) at the KO was lost. It is counted when its clear flashes, or when the next spawn shows by KO+3 frames. Lines come from the flash, and `fuse.py` types a T-spin from the banner as usual |
| `R/pcmap.py` | **new.** Builds the PCDEC table from the PERFECT CLEAR banner scan |
| `tetrio/metrics.py` | PCDEC is this video's table; `UNRESOLVED` is `R/build.py`'s list; witnessed, KOTAB and event corrections are empty |

## Checks

- Port validation on cVO2 (66 player-games, the repo's own rows as reference). Winners and durations
  match 66/66. With `kofinal.py`, winner piece counts match in 31 of 32 games (h017's last S locks on the KO frame, a hand edit), and
  46 of 64 included rows match on every count column. Totals: pieces +5, lines +12 (+0.3%), attack +26 (+0.4%),
  if h030 p2 is left out. In that row A lost the queue read, and B's splice was unresolved.
- KO frames: the 28 winners that a first version of `kofinal.py` (next spawn only after the KO) gave no
  piece were checked on frames KO-8/-3/0/+3 (`check/kosheet.py`). The frames showed that a next spawn just
  before the KO, which A misses, also marks a lock. With that rule, 8 of the 28 gain a piece and 20 are left.
  Of those, k006 locks between KO and KO+3 (the score changes there), and k010 and k033 may do the same
  (the score is hidden). All three stay uncounted, because the repo counts only locks at or before the KO.
  The other 17 show only soft drop, or a lock A already counted.
- Perfect Clears: all 57 banner onsets were checked by eye on contact sheets (`check/pcsheet.py`).
  Every onset at least 0.9 s long is a PC. Shorter ones are either the tail of the same banner or
  effects (TETRIS flash, garbage). That gives 53 PCs.
  `pcmap.py` takes the clear nearest the banner as the PC. It drops A's double-logged halves: a clear
  with the same line count up to 0.65 s before, and any clear up to 0.5 s after.
- k007 runs 466.6 s. Frames every 30 s show one game: the score rises and the WIN counter stays at 6–1.
  A lost the queue read for 41 s, so k007 is excluded as an unresolved lower bound, like k004 and k013.

## Known gaps

- T-spin Minis are not counted (see above).
- A piece that locks on the KO frame itself, with no clear and no visible next spawn, is not counted.
  On cVO2 the rule finds five of the six KO-frame pieces the repo fixed by hand (not h017's S).
- There are no `event-corrections.json` or `hand-edits.csv` entries for this set.
