# chain/t: amemiya's upload of 2025-08-20 vs uyeshota (video `armDs7VaDyk`)

57 games, ids `t000`–`t056`, dataset `upload-2025-08-20`. This tree is a copy of `chain/d` (itself `chain/c`, `chain/s`,
`chain/oc`) run on one video and kept as it ran (its paths point at `/tmp/claude-0/t/`, a cloud session's scratchpad). It
adds no frame image or video to the repo.

## Inputs

amemiya is the LEFT board (p1) throughout. Six first-to-7 sets, all against uyeshota:

| ids | set |
|---|---|
| t000–t009 | 7-3 |
| t010–t018 | 7-2 |
| t019–t027 | 7-2 |
| t028–t035 | 1-7 |
| t036–t045 | 3-7 |
| t046–t056 | 7-4 |

amemiya 32-25 over the 57 games. Every winner agrees with the on-screen WIN counter.

- The video: fetched with yt-dlp through a Tailscale exit node. It has no 480p stream, only 720p60 (itag 298), so it was
  rescaled with `fps=30,scale=837:470,pad=854:480:8:6`: the frame rate first, then the same geometry as for c and d.
- Games: `seg/` as in d (57 segments, every one a game). `mkgames_t.py` writes `games.json` from the WIN counters read by
  eye and asserts each game moves one counter by one. The upload is edited, but every set's last game shows the counter
  move (or the WINNER screen) before the cut, so each set-final winner was read there.

## What differs from chain/d

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/t/`, video `armDs7VaDyk` |
| `mkgames_t.py` | this video's games |
| banner, word and score-digit templates | **c's, reused** through d (`w/R/fr/*.png`, `w/ocr/T.npy`); not committed |
| `corr/tools/nextcount.py` | reference frame 2210 s (mid t033). d's 2410 s and oc's 2200 s fall between games here |
| `corr/merge_xo.py` | d's without its d041 patch |

As for d, `pool/pool.py` needs `pool/out/` to exist, `w/tetrio/metrics.py` needs scipy, and `corr/drive_nc.sh` needs
`corr/nc/` to exist.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-amemiya/` (appended after the 2026-11-06 stream's).

1. **Flags.** `apply/checks_xo.py` raised 79 flags (`corr/flags.json`): 51 PERFECT CLEAR banner onsets, 16 winner KO
   pieces, 5 T-spins with no banner, 3 KO-tail score jumps, 2 banners with no clear, 1 gap window, 1 bad bag.
2. **PERFECT CLEARs.** 22 accepted (`corr/pcaccepted.json`). The onsets away from an accepted PC make 15 clusters
   (`corr/pcclusters.json`), drawn as strips with `check/pc/strip2.py`: all are line-clear flashes, so
   `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 19 spots (`corr/score/spots.json`).
4. **Frame checks.** 32 items in four groups (`corr/groups/g0-g3`). One agent per group proposed corrections
   (`corr/out/b*.json`), one more per group tried to refute each (`corr/out/v*.json`): all 17 kept.
5. **NEXT-queue recount** (`corr/drive_nc.sh`, `corr/nc_compare.py`, reference frame 2210 s): against the applied table,
   8 player-games were two or more pieces off. They were a fifth group (`corr/groups/g4.json`, brief `corr/CHECKER4.md`)
   with its own checker and skeptic, all four of whose proposals were kept. t007 p1: the chain logged one None lock twice
   at 419.53 (74 → 73 pieces). t021 p2 and t052 p2: the quad PERFECT CLEAR sat on the wrong piece and one lock was missing,
   so each window was rebuilt with one more event; the table's piece count was already right, and the cleared rows hold no
   garbage (gc 4 → 0). In the other five the table is right: the recount starts after the first one to three spawns under
   READY/GO, and a shift left over at the end is the loser's last spawn, which never locked. Final comparison: 91 agree,
   10 one off, 6 lost, and 7 still two or more off for that reason (`corr/nc_compare.json`).
6. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (13: 7 rebuilt windows, 3 added events, 3 retypes;
   `corr/fixwas.py` widened t007's removal into a window over the two same-t events) and `corr/cells.json` (8 cells).
   The corrected event list already gives the 2 REN/B2B maxima, so 6 are hand edits, all piece counts. The largest is
   t037 p2 (66 → 61).

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the other streams).
