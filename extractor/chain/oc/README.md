# chain/oc: amemiya's stream of 2026-11-08 (「【VS最強格テトラー】uyeshota！テトリス15先×2回」)

128 games, ids `o000`–`o127`, dataset `stream-2026-11-08`, video `O1rC0XcFy64`. This tree is a copy of
`chain/tx` with `chain/aj`'s `w/A/analyze.py`, run on one live-stream archive and kept as it ran (its paths point
at `/tmp/claude-0/oc/`, a cloud session's scratchpad). It adds no frame image or video to the repo.

## Inputs

amemiya is the LEFT board (p1) throughout.

| ids | opponent | set | note |
|---|---|---|---|
| o000–o026 | いんたい | 15-12 | |
| o027–o047 | uyeshota | 15-6 | |
| o048–o052 | uyeshota | 3-2, stopped | the next game stopped when the Switch software restarted (`o_restart`), and the first game in the remade room stopped 16 s in with 「インターネットから切断しています」 (`o_disconnect`); both are in `games_all.json` only, the five games before them ARE counted (tx precedent) |
| o053–o081 | uyeshota | 15-14 | |
| o082–o103 | たわ | 15-7 | |
| o104–o127 | ふまんなつれ | 15-9 | |

amemiya 78-50 over the 128 games.

- The video: fetched with yt-dlp through a Tailscale exit node (as for tx, nk and aj).
- **Rescale.** `scale=837:470,pad=854:480:8:6` puts every board cell where xt's coordinates expect it.
- Games: `seg/` as in tx (131 segments after the menu filter). Segment 0 is a COM game (COM1 vs COM2) and is not
  counted; the stream moves to Kirby Air Riders after 8180 s, which was never segmented. `mkgames_oc.py` writes
  `games.json` and `games_all.json` from the WIN counters read by eye off contact sheets, and asserts each game
  moves one counter by one and each set ends on its final score.

## What differs from chain/tx

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/oc/`, video `O1rC0XcFy64` |
| `mkgames_oc.py`, `drive_oc1.sh` | this stream's games and stage-1 driver |
| `w/A/analyze.py` | aj's version (the NEXT-queue I-flash stall rules; see `chain/aj/README.md`) |
| banner, word and score-digit templates | **recut from this video** (`b2` 2178.6 s, `b3` 2179.2, `b_single` 2182.2, the Mini word pasted from 2433.3; digits from `check/ocr/mktpl.py`'s frames at 2245/2500/3050/4700/6300/7900 s). Not committed |
| `check/pc/strip2.py` | aj's `pcstrip.py` with offsets −0.4 to +2.2 s, for the hidden-PC strips |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 400 → 2200: the 400 s frame is in the COM game, whose NEXT cards are white, so every read was `?` and no spawn was counted |
| `check/ocr/reader.py` | must be copied beside `w/ocr/T.npy` for `corr/tools/score.py` to import it |

As for nk and aj, `pool/pool.py` needs `pool/out/` to exist and `w/tetrio/metrics.py` needs scipy.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-amemiya/` (appended after the earlier streams').

1. **Flags.** `apply/checks_xo.py` raised 225 flags (`corr/flags.json`): 137 PERFECT CLEAR banner onsets,
   44 winner KO pieces, 19 gap windows, 15 T-spins with no banner, 4 KO-tail score jumps, 3 banners with no
   clear, 1 banner/type disagreement, 1 bad bag, 1 APP outlier.
2. **PERFECT CLEARs.** 38 onsets carry `pcmap`'s "PC = clear at" (accepted; test that string, not "accepted").
   The other onsets away from an accepted PC make 59 clusters (`corr/pcclusters.json`), drawn as strips with
   `check/pc/strip2.py`: **every one is a line-clear flash on a stack that keeps its garbage rows**, so there are
   no hidden PCs and `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 33 spots (`corr/score/spots.json`); the 10 with an unexplained score
   change of 900 or more were kept as items.
4. **Frame checks.** The 88 non-PC flags and the 10 spots made 98 items in four groups (`corr/groups/`).
   One agent per group proposed corrections (`corr/out/b*.json`), one more per group tried to refute each
   (`corr/out/v*.json`). The skeptics kept every proposal and added two the checker had left: o096's piece
   counts (p1 136 → 134, p2 147 → 144). Freezes and lag were the largest source: o052 froze about 4 s, o110
   and o120 had lag and a long REN stall, and the chain had logged phantom clears and REN BREAKs inside them.
5. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (16 rebuilt windows, 7 retypes,
   7 removals, 2 added events) and `corr/cells.json` (29 cells). `corr/fixwas.py` ran `w/tetrio/metrics.py`
   and needed no repair.
6. **Cells.** Of the 29 cell edits, the corrected event list already gives the 12 REN maxima, so 17 are hand
   edits, all piece counts.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game` (one worker while
the frame-check agents ran, then three), and `corr/nc_compare.py` compared them with the final table
(`corr/nc_compare.json`). Of the 256 player-games, 226 agree exactly, 19 differ by one piece and 8 are lost reads
(bad bags: o001 p1, o013 p1, o024 p2, o052 p2, o057 p1, o079 p2, o107 p1, o121 p1). Five of the one-piece
differences are games whose piece count the frame checks changed (o006 p2, o008 p2, o031 p1, o099 p2, o110 p1);
the frame checks looked at the KO frame or the spawns directly. Three clean reads are 2 lower than the table:
o007 p2 (54, raised by one by the frame checks for a piece locked on the KO frame), o020 p2 (83) and o042 p2 (155).
No piece count was changed from the recount alone, as for xo, xt, tx, nk and aj.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- o096 p2's last J: the frames do not show whether it locked out; the count is 144 (145 if it did).
- No opener labels (the `opener` column is empty, as for the streams).
