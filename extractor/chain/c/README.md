# chain/c: amemiya's live stream of 2026-11-04 (「【VS最上位テトラー】いんたい！おはゆれ！テトリス15先」)

123 games, ids `c000`–`c122`, dataset `stream-2026-11-04`, video `qNc6SS1aEXY`. This tree is a copy of
`chain/s` (itself `chain/oc`) run on one stream and kept as it ran (its paths point at `/tmp/claude-0/c/`, a cloud
session's scratchpad). It adds no frame image or video to the repo.

## Inputs

amemiya is the LEFT board (p1) throughout.

| ids | opponent | set |
|---|---|---|
| c000–c017 | いんたい | 10-8, abandoned (see below) |
| c018–c048 | OSW | 20-11 |
| c049–c070 | いんたい | 15-7 |
| c071–c095 | おはゆれ | 15-10 |
| c096–c122 | たわ | 15-12 |

amemiya 75-48 over the 123 games. Every winner agrees with the on-screen WIN counter.

- The video: fetched with yt-dlp through a Tailscale exit node (as for oc and s).
- Rescaled with `scale=837:470,pad=854:480:8:6`, as for oc and s, so oc's coordinates run unpatched.
- Games: `seg/` as in oc (128 segments after the menu filter). `mkgames_c.py` writes `games.json` from the WIN
  counters read by eye off contact sheets and asserts each game moves one counter by one. Left out: segments 0-1
  (COM2 practice), 20 (a game begun at いんたい 10-8 and abandoned after 15 s, the room closed with no winner) and
  126-127 (another game, after the stream left PPT2). c017 is one 400 s game, checked frame by frame. Each set's
  last game fades on the KO; its winner was read off the faded counter.

## What differs from chain/s

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/c/`, video `qNc6SS1aEXY` |
| `mkgames_c.py` | this stream's games |
| banner, word and score-digit templates | **recut from this video** (`w/R/fr/*.png`, `check/ocr/mktpl.py`). Not committed. The 11-06 and 11-07 runs (`chain/d`, `chain/e`) reuse these |
| `corr/merge_xo.py` | five groups; and every `missed` entry of a skeptic is merged, even several under one ref (the dict keyed by ref kept only the last; g4's skeptic filed three under one item, and that is the first time it happened, checked against every earlier run) |

As for oc, `pool/pool.py` needs `pool/out/` to exist and `w/tetrio/metrics.py` needs scipy.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-amemiya/` (appended after the 2025-07-05 upload's).

1. **Flags.** `apply/checks_xo.py` raised 192 flags (`corr/flags.json`): 99 PERFECT CLEAR banner onsets,
   37 winner KO pieces, 31 gap windows, 7 bad bags, 6 T-spins with no banner, 6 banners with no clear,
   5 KO-tail score jumps, 1 banner/type disagreement.
2. **PERFECT CLEARs.** 26 accepted (`corr/pcaccepted.json`). The onsets away from an accepted PC make 54 clusters
   (`corr/pcclusters.json`), drawn as strips with `check/pc/strip2.py`: all are line-clear flashes, so
   `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 31 spots (`corr/score/spots.json`).
4. **Frame checks.** 98 items in four groups (`corr/groups/g0-g3`). One agent per group proposed corrections
   (`corr/out/b*.json`), one more per group tried to refute each (`corr/out/v*.json`): 55 kept, 4 amended,
   2 rejected, 5 missed corrections added. Phantom pieces were the largest source again: c021, c036 and c075 have stream-lag
   windows, and in those and in c107, c112, c117 and c118 the chain held locks the frames do not show
   (c118 p1 132 → 104 pieces, c112 p2 100 → 87).
5. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (33: 16 rebuilt windows, 9 removals,
   6 retypes, 2 added events) and `corr/cells.json` (35 cells). `corr/fixwas.py` ran `w/tetrio/metrics.py` and
   needed no repair. The corrected event list already gives 12 of the cells (REN and B2B maxima), so 23 are hand
   edits: 21 piece counts, c107 amemiya's REN maximum (17) and c021 amemiya's garbage rows (38 → 36).
6. **NEXT-queue recount** (`corr/drive_nc.sh`, `corr/nc_compare.py`): of 246 player-games, 214 agreed, 19 were one
   off, 10 lost the queue and 3 read two or more pieces from the table. Those three were a fifth group
   (`corr/groups/g4.json`, brief `corr/CHECKER4.md`) with its own checker and skeptic. c027 p2 and c033 p2: the
   table is right (nextcount misses the first spawns under READY/GO). c021 p1 107 → 103: B's splice in a 9.7 s lag
   window added 4 phantom pieces, 7 untyped lines and 2 garbage rows; the skeptic removed the splice's three REN
   BREAKs, which gives back the REN run the score shows (max REN 9 → 10, lines 58 → 51). Against the applied
   table: 215 agree, 19 one off, 10 lost, 2 (c027 p2, c033 p2) as above (`corr/nc_compare.json`).

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the other streams).
