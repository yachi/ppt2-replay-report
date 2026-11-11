# chain/r: amemiya's live stream of 2026-10-31 (video `bExpa2eFlOw`)

101 games, ids `r000`–`r100`, dataset `stream-2026-10-31`. This tree is a copy of `chain/p` (itself `chain/t`, `chain/d`,
`chain/c`, `chain/s`, `chain/oc`) run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/r/`,
a cloud session's scratchpad). It adds no frame image or video to the repo.

## Inputs

amemiya is the LEFT board (p1) throughout. Four first-to-15 sets:

| ids | opponent | set |
|---|---|---|
| r000–r022 | どらえもん | 15-8 |
| r023–r049 | ゆうくん | 12-15 |
| r050–r074 | ゆうくん | 15-10 |
| r075–r100 | てつ | 15-11 |

amemiya 57-44 over the 101 games. Every winner agrees with the on-screen WIN counter; the second set's last game cuts
away before the counter moves, so its winner was read off the result screen at 4320 s.

- The video: fetched with yt-dlp through a Tailscale exit node, rescaled with `scale=837:470,pad=854:480:8:6` as for c.
- Games: `seg/` as in p. `mkgames_r.py` writes `games.json` from the WIN counters read by eye and asserts each game moves
  one counter by one.

## What differs from chain/p

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/r/`, video `bExpa2eFlOw` |
| `mkgames_r.py` | this stream's games |
| banner, word and score-digit templates | **c's, reused** through d (`w/R/fr/*.png`, `w/ocr/T.npy`); not committed |
| `corr/tools/nextcount.py` | reference frame 3280 s (mid r031) |
| `corr/BRIEF.md` | this stream's header |

As for p, `pool/pool.py` needs `pool/out/` to exist, `w/tetrio/metrics.py` needs scipy, and `corr/drive_nc.sh` needs
`corr/nc/` to exist.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-amemiya/` (appended after the 2026-10-29 stream's).

1. **Flags.** `apply/checks_xo.py` raised 154 flags (`corr/flags.json`): 77 PERFECT CLEAR banner onsets, 42 gap windows,
   26 winner KO pieces, 3 T-spins with no banner, 3 KO-tail score jumps, 2 banners with no clear, 1 banner/type
   disagreement.
2. **PERFECT CLEARs.** 27 accepted (`corr/pcaccepted.json`), none of them amemiya's. The onsets away from an accepted PC
   make 32 clusters (`corr/pcclusters.json`), drawn as strips with `check/pc/strip2.py`: all are line-clear flashes, so
   `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 44 spots (`corr/score/spots.json`).
4. **Frame checks.** 89 items in four groups (`corr/groups/g0-g3`). One agent per group proposed corrections
   (`corr/out/b*.json`), one more per group tried to refute each (`corr/out/v*.json`). The skeptics rejected 1 proposal
   and amended 1 (both in g0); the rest were kept. Most fixes are phantom singles, locks and REN break markers that
   extractor B logged during stream lag and long REN chains (r000, r001, r013, r014, r070, r078, r085); the largest edit
   is r078 p1, 149 → 130 pieces, where both players also ran REN chains of 18 and 17 that the break markers had cut.
5. **NEXT-queue recount** (`corr/drive_nc.sh`, `corr/nc_compare.py`, reference frame 3280 s): against the applied table,
   6 player-games were two or more pieces off. They were a fifth group (`corr/groups/g4.json`, briefs `corr/CHECKER4.md`
   and `corr/SKEPTIC4.md`) with its own checker and skeptic, whose one proposal was kept. r032 p1: an earlier piece edit
   had counted two REN break markers as locks (216 → 214). In the other five the table is right: the recount starts after
   the first spawns under READY/GO, or a shift left over at the end is the loser's last spawn, which never locked. Final
   comparison: 167 agree, 25 one off, 5 lost, 5 still two or more off for those reasons (`corr/nc_compare.json`).
6. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (45: 12 rebuilt windows, 23 removals, 8 retypes,
   2 added events) and `corr/cells.json` (34 cells). `corr/fixwas.py` ran `w/tetrio/metrics.py`. The corrected event list
   already gives the other 15, so 19 cells are hand edits (16 piece counts, 3 REN maxima).

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the other streams).
