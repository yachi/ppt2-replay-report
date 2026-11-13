# chain/pp: uyeshota's stream of 2026-11-08 (てとぼ, 15先 ×6)

123 games, ids `c000`–`c122`, dataset `stream-2026-11-08`, video `Pp-m3oLlOBM`. This tree is a copy of `chain/qh`,
run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/pp/`, a cloud session's
scratchpad). It adds no frame image or video to the repo.

## Inputs

uyeshota is the LEFT board (p1). Six sets, each first to 15, against five opponents:

| ids | set | opponent | score |
|---|---|---|---|
| c000–c028 | 1 | どらえもん | 14-15 |
| c029–c052 | 2 | どらえもん | 15-9 |
| c053–c070 | 3 | ひかるきし　はいしん | 15-3 |
| c071–c086 | 4 | せい | 15-1 |
| c087–c106 | 5 | ふらいこん | 15-5 |
| c107–c122 | 6 | さむい | 15-1 |

uyeshota 89-34 over the 123 games, five sets to one.

- The video: 480p h264, then **rescaled** like every uyeshota and amemiya video (`scale=837:470,pad=854:480:8:6`),
  so qh's board geometry holds.
- Games: `seg/` as in qh (123 segments, every one a game). `mkgames_pp.py` writes `games.json` and `games_all.json`
  from the WIN counters read by eye off contact sheets (`seg/cnt.py`). Set 1's last game starts at 14-14 and its
  end counter already reads set 2's 0-0; its winner is read off the result screen at 1580 s (どらえもん, 14 WIN 15).

## What differs from chain/qh

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/pp/`, video `Pp-m3oLlOBM`, player `uyeshota` |
| `mkgames_pp.py`, `drive_s1.sh`, `drive_s2.sh` | this stream's games and the two stage drivers |
| banner and word templates | copied from `chain/u4` (same rescale geometry). Not committed |
| `check/ocr/mktpl.py` | not run: `T.npy` copied from `chain/fs` (same digit font), as for u4. Not committed |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 380, a clean online frame of this video (game c003) |
| `corr/merge_xo.py` | five groups (`range(5)`) |
| `corr/nc_compare.py` | compares with this run's chain table plus its hand edits, not with `games.csv` |
| `apply/hand_edits_pp.py` | the hand-edit writer, paths to this run |

As for qh, `pool/pool.py` needs `pool/out/` to exist, `w/tetrio/metrics.py` needs scipy and `witnessed.json`
(`[]` here), `check/score/steps.py` needs `corr/score/`, and `corr/tools/score.py` needs `check/ocr/reader.py`
beside `w/ocr/T.npy`.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-uyeshota/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 197 flags (`corr/flags.json`): 132 PERFECT CLEAR banner onsets,
   41 winner KO pieces, 7 gap windows, 7 T-spins with no banner, 5 banners with no clear, 4 KO-tail score jumps and
   1 bad bag.
2. **PERFECT CLEARs.** 50 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). The others make
   43 clusters (`corr/pcclusters.json`). On rescaled video a lit-cell count never reads 0 after a real PC (accepted
   PCs read 20-60), so the 16 rejected onsets whose board read low (`corr/litcount.out`) went to the checkers as
   frame-check items instead of into `corr/hidden_pc.json`, which is empty. Most were real PERFECT CLEARs that
   `pcmap` had dropped as a double log, with the chain one piece short around them; the rebuilt windows below hold
   12 PCs.
3. **Score spots.** `check/score/` found 30 spots (`corr/score/spots.json`); 3 were kept as items.
4. **Frame checks.** The 65 non-PC flags, the 16 PC onsets and the 3 spots made 84 items in five groups
   (`corr/groups/`). One agent per group proposed corrections (`corr/out/b*.json`), one more per group tried to
   refute each (`corr/out/v*.json`). The skeptics kept all 51 proposals.
5. **Merge.** `corr/merge_xo.py` wrote 28 event corrections (18 rebuilt windows, 6 retypes, 3 removals, 1 added
   event) and 23 cell edits. `corr/fixwas.py` ran `w/tetrio/metrics.py` and needed no repair.
6. **Cells.** Of the 23 cell edits, the corrected event list already gives the 4 REN maxima, so 19 are hand edits,
   all piece counts.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game` (two workers), and
`corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 246 player-games, 220 agree
exactly, 14 differ by one piece (each the table one higher) and 8 are lost reads (bad bags or long unknown
stretches: c021 p2, c026 p2, c065 p1, c065 p2, c068 p2, c080 p1, c106 p1, c118 p1). Four clean reads differ by
more, each the table higher: c047 p1 by 3, c047 p2 by 10, c048 p2 by 2 and c109 p1 by 2. No piece count was changed
from the recount alone, as for qh and u4.

## Known gaps

- c047 holds a 12 s stretch (from about 2516.5 s) where both NEXT queues stall and the chain spliced B's events in.
  The frame checks removed one phantom lock per board there; the recount through it still reads 3 (p1) and 10 (p2)
  fewer pieces than the table, so those two piece counts may be high.
- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
