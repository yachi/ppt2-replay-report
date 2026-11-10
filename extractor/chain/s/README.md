# chain/s: amemiya's upload of 2025-07-05 (「VS uyeshota！15先×3回【ぷよぷよテトリス2】」)

75 games, ids `s000`–`s074`, dataset `upload-2025-07-05`, video `6nzD6OsKuuY`. This tree is a copy of
`chain/oc` run on one edited upload and kept as it ran (its paths point at `/tmp/claude-0/s/`, a cloud session's
scratchpad). It adds no frame image or video to the repo.

## Inputs

amemiya is the LEFT board (p1) throughout.

| ids | opponent | set |
|---|---|---|
| s000–s022 | uyeshota | 15-8 |
| s023–s045 | uyeshota | 8-15 |
| s046–s074 | uyeshota | 15-14 |

amemiya 38-37 over the 75 games.

- The video: fetched with yt-dlp through a Tailscale exit node (as for oc).
- **Rescale, although the upload is already 854x480.** The upload fills the frame, so its boards sit a few pixels
  away from where oc's coordinates expect them. Run natively, the chain cut every game to about 2 s and called p1
  the winner of all of them, and patching the constants only half worked. `scale=837:470,pad=854:480:8:6` (the
  same rescale as oc) puts every board cell where the coordinates expect it, and the oc files then run unpatched.
- Games: `seg/` as in oc (75 segments after the menu filter, one per game). `mkgames_s.py` writes `games.json`
  from the WIN counters read by eye off contact sheets, and asserts each game moves one counter by one and each set
  ends on its final score. **The upload is edited: each set's last game cuts to the loading screen right after the
  KO**, before the WIN counter moves, so those winners were read off the result screen just before the cut.

## What differs from chain/oc

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/s/`, video `6nzD6OsKuuY` |
| `mkgames_s.py` | this upload's games |
| banner, word and score-digit templates | **recut from this video** (`b2` 340.6 s, `b3` 387.2, `b_single` 290.9; this upload never shows a Mini banner on p2's side, so p1's Mini word from 354.6 s is pasted into p2's window, as oc did; digits from six frames whose scores were read by eye, `check/ocr/mktpl.py`). Not committed |
| `corr/merge_xo.py` | three groups, not four |

As for oc, `pool/pool.py` needs `pool/out/` to exist and `w/tetrio/metrics.py` needs scipy.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-amemiya/` (appended after the streams').

1. **Flags.** `apply/checks_xo.py` raised 122 flags (`corr/flags.json`): 72 PERFECT CLEAR banner onsets,
   22 winner KO pieces, 9 gap windows, 5 T-spins with no banner, 5 KO-tail score jumps, 4 banners with no clear,
   4 banner/type disagreements, 1 bad bag. The WIN counter agrees with the chain's winner in all 75 games.
2. **PERFECT CLEARs.** Every PERFECT CLEAR in this upload is uyeshota's; amemiya has none. The onsets on p1's side
   are 0.1-0.3 s line-clear flashes. The onsets away from an accepted PC make 18 clusters
   (`corr/pcclusters.json`), drawn as strips with `check/pc/strip2.py`: every one is a line-clear flash on a stack
   that keeps its garbage rows, so `corr/hidden_pc.json` is empty. **One hidden PC was found anyway**: in s044
   uyeshota clears three PCs in a row, and the clustering rule (skip any onset within 3 s of an accepted one) hid the
   third, at about 2712 s. It was made a frame-check item and confirmed.
3. **Score spots.** `check/score/` found 31 spots (`corr/score/spots.json`); the 6 with an unexplained score
   change of 900 or more were kept as items.
4. **Frame checks.** The 50 non-PC flags, the 6 spots and the s044 PC made 57 items in three groups
   (`corr/groups/`). One agent per group proposed corrections (`corr/out/b*.json`), one more per group tried to
   refute each (`corr/out/v*.json`); the skeptics kept every proposal and added none. Stream stalls were the largest
   source again: s055 froze about 12 s and s058 about 4 s, and the chain had logged phantom locks and
   REN BREAKs inside them (s015 has a T that hovered about 7 s, with the same phantoms). Two Mini T-spins clear no line (s005 uyeshota, s013 amemiya: the banner reads Mini T-SPIN
   with no Single and the score rises 300); they are `tsmini` with `lines` 0.
5. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (13 rebuilt windows, 8 retypes,
   2 removals, 3 added events) and `corr/cells.json` (22 cells, after the NEXT recount below). `corr/fixwas.py` ran `w/tetrio/metrics.py`
   and needed no repair.
6. **Cells.** Of the 22 cell edits, the corrected event list already gives 7 (REN and B2B maxima), so 15 are hand
   edits: 13 piece counts and 2 REN maxima (s055 uyeshota 9, s058 amemiya 6, where the chain's BREAKs inside a stall
   still cut the run). s038's piece counts (amemiya 90 → 76, uyeshota 111 → 100) were inflated by B's splice and
   were re-counted from the NEXT queue by the checker.

7. **NEXT-queue recount** (`corr/drive_nc.sh`, `corr/nc_compare.py` against the applied table): of 150 player-games,
   103 agree, 30 are one off, 16 read more pieces than the table and 1 is lost (s069 p1, a TETRIS blast over the
   NEXT box). The 19 disagreements of two or more were a fourth group (`corr/groups/g3.json`, items 100-118, brief
   `corr/CHECKER3.md`) with its own checker and skeptic. In 17 the table is right: nextcount misses the first 2-4
   spawns under the READY/GO overlay, and its last shift is a spawn that never locks before the KO. Two were wrong,
   both from B's splice inside a stream stall: s055 p2 54 → 49 (supersedes group 2's 54; `merge_xo.py` keeps the
   later edit of a cell) and s058 p1 106 → 94.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
