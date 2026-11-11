# chain/p: amemiya's live stream of 2026-10-29 (video `0Akye6ouJbw`)

152 games, ids `p000`–`p151`, dataset `stream-2026-10-29`. This tree is a copy of `chain/t` (itself `chain/d`, `chain/c`,
`chain/s`, `chain/oc`) run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/p/`, a cloud
session's scratchpad). It adds no frame image or video to the repo.

## Inputs

amemiya is the LEFT board (p1) throughout. Six first-to-15 sets:

| ids | opponent | set |
|---|---|---|
| p000–p018 | 3200↑てとぼ | 15-4 |
| p019–p046 | Yuukun3798 | 13-15 |
| p047–p075 | Yuukun3798 | 14-15 |
| p076–p102 | uyeshota | 15-13 |
| p103–p125 | uyeshota | 15-8 |
| p126–p151 | uyeshota | 11-15 |

amemiya 83-69 over the 152 games. Every winner agrees with the on-screen WIN counter.

- The video: fetched with yt-dlp through a Tailscale exit node, rescaled with `scale=837:470,pad=854:480:8:6` as for c.
- Games: `seg/` as in t. `mkgames_p.py` writes `games.json` from the WIN counters read by eye and asserts each game moves
  one counter by one, with one exception: at 7562 s the stream skips a whole game (the counter goes 12-3 → 12-4 → 12-5
  within 1.5 s), so the fourth set has 27 ids for 28 games and `mkgames_p.py` marks the skip. p091's cut lands on the
  skip: the stream cuts away at 7560.97 s and the real KO is 7560.93 s, so its duration is a hand edit (106.57 → 106.33 s).

## What differs from chain/t

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/p/`, video `0Akye6ouJbw` |
| `mkgames_p.py` | this stream's games |
| banner, word and score-digit templates | **c's, reused** through d (`w/R/fr/*.png`, `w/ocr/T.npy`); not committed |
| `corr/tools/nextcount.py` | reference frame 2370 s (mid p005) |
| `corr/merge_xo.py` | five groups (g0–g3 and g4, the NEXT-queue recount) |
| `corr/SKEPTIC4.md` | the recount group's skeptic brief (t's skeptic for g4 reused SKEPTIC.md) |

As for t, `pool/pool.py` needs `pool/out/` to exist, `w/tetrio/metrics.py` needs scipy, and `corr/drive_nc.sh` needs
`corr/nc/` to exist.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-amemiya/` (appended after the 2025-08-20 upload's).

1. **Flags.** `apply/checks_xo.py` raised 270 flags (`corr/flags.json`): 156 PERFECT CLEAR banner onsets, 52 winner KO
   pieces, 45 gap windows, 7 T-spins with no banner, 7 KO-tail score jumps, 3 banners with no clear.
2. **PERFECT CLEARs.** 51 accepted (`corr/pcaccepted.json`). The onsets away from an accepted PC make 66 clusters
   (`corr/pcclusters.json`), drawn as strips with `check/pc/strip2.py`: all are line-clear flashes, so
   `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 53 spots (`corr/score/spots.json`).
4. **Frame checks.** 136 items in four groups (`corr/groups/g0-g3`). One agent per group proposed corrections
   (`corr/out/b*.json`), one more per group tried to refute each (`corr/out/v*.json`). The skeptics rejected 7 proposals
   (all in g1), amended 2 and added 1 the checker missed; the rest were kept. p024–p040 run through a stretch of stream
   lag in which pieces fall in slow motion; the chain logged locks there that the frames do not show (p040 p1 173 → 146
   pieces, the largest edit).
5. **NEXT-queue recount** (`corr/drive_nc.sh`, `corr/nc_compare.py`, reference frame 2370 s): against the applied table,
   11 player-games were two or more pieces off. They were a fifth group (`corr/groups/g4.json`, briefs `corr/CHECKER4.md`
   and `corr/SKEPTIC4.md`) with its own checker and skeptic, all of whose proposals were kept. p127 p1: the chain logged
   phantom locks and one REN break marker (190 → 186 pieces, garbage received 47 → 46). In p006 p1 the recount misread a
   TETRIS flash as spawns; in the other nine the table is right and the recount starts after the first spawns under
   READY/GO. Final comparison: 235 agree, 36 one off, 23 lost, 10 still two or more off for those reasons
   (`corr/nc_compare.json`).
6. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (50: 19 rebuilt windows, 24 removals, 4 retypes,
   3 added events) and `corr/cells.json` (52 cells). `corr/fixwas.py` ran `w/tetrio/metrics.py`. The corrected event list
   already gives the other 21, so 31 cells are hand edits (29 piece counts, one REN maximum, one garbage-row count), plus
   p091's two durations: 33 in all.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- The game skipped at 7562 s is not in the dataset.
- No opener labels (the `opener` column is empty, as for the other streams).
