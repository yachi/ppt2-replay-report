# chain/xp: ゆうくん's stream of 2026-11-09 (「雑談兼てとぼ 強い人と対戦したい」)

108 games, ids `a000`–`a107`, dataset `stream-2026-11-09`, video `xp1R8-_Bi_I`. This tree is a copy of
`chain/aj`, run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/xp/`, a cloud
session's scratchpad). It adds no frame image or video to the repo.

## Inputs

Private-room sets, first to N on the room's WIN counter; ゆうくん is the LEFT board (p1) throughout.

- The video: fetched with yt-dlp through a Tailscale exit node (as for tx, nk and aj). **The archive had just gone
  from live to post_live, and every h264 itag listed 0 DASH fragments**, so `-f 135` failed with "The downloaded
  file is empty". The VP9 itags listed every fragment: itag 244 (480p VP9) was downloaded and transcoded once,
  sequentially (the fragment-built webm cannot seek), with aj's rescale, `scale=818:460,pad=854:480:26:7`.
- Games: `seg/` as in aj (292 candidate segments, `seg/seg_games.json`). `mkgames_xp.py` writes `games.json`
  from the WIN counters at start+3 s and end−0.3 s, read by eye off `seg/cnt/` contact sheets, and asserts each
  game moves one counter by one. Not counted: segments 0–4 (全世界パズルリーグ first-to-2 matches), 5 and 246
  (room menus) and 49 (a game against クッパ disconnected about 30 s in, no result).
- Sets: にくうどん FT5 5–0 and FT15 15–6; しょうがくよねんせい FT15 15–2; クッパ FT15 15–5; あめみや はいしん FT15
  15–11 and 4–15. ゆうくん 69–39 in games.
- **The 24 FT5 sets against syakegohan (segments 70–245, 176 games) are not in games.json.** They are the same
  games as syakegohan's own stream `QheX1_UP5W4` (chain `qh`, ids q000–q175), seen from the other side; yachi
  chose (2026-11-09) not to add them twice. `mkgames_xp.py` still parses them and asserts every winner against
  QheX1's games.csv (`seg/qh_winners.csv`, not committed), which is also where the six 4–4 set finals' winners
  come from.
- Each set's last game runs into the next room, so its end counter is already reset; the FT15 finals' winners
  were read off their last frames.

## What differs from chain/aj

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/xp/`, video `xp1R8-_Bi_I`, ids `a` |
| `mkgames_xp.py`, `drive_xp1.sh` | this stream's games and stage-1 driver |
| `w/R/banner.py`, `w/R/banscan.py` | **no camera box** here, so p2 gets a full "-SPIN" template again (p1 x=70 y=325, words x 99/509 y 323) and aj's two-frame minimum on p2 is dropped |
| `w/R/mini_xp.py` | no "Mini" banner was seen in this video either; the Mini series are zeros |
| banner, word and score-digit templates | recut from this video (`check/ocr/mktpl.py` frames 1000, 1500, 2200, 5000, 5500 and 8000 s). Not committed |
| `corr/tools/nextcount.py` | reference frame at 2200 s (a020) |
| `corr/mk_hidden_pc.py` | new: writes `corr/hidden_pc.json` from the hidden-PC strips (below) |
| `corr/merge_xo.py` | four groups; a skeptic's added window may list its events as lists, which are turned into the dicts `metrics.py` reads |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-yukun/`.

1. **Flags.** `apply/checks_xo.py` raised 172 flags (`corr/flags.json`): 72 PERFECT CLEAR banner onsets,
   45 winner KO pieces, 16 gap windows, 14 bad bags, 11 KO-tail score jumps, 6 banner/type disagreements,
   4 T-spins with no banner and 4 banners with no clear.
2. **PERFECT CLEARs.** `pcmap` accepted 9 PCs. The 42 clusters of short onsets away from an accepted PC
   (`corr/pcclusters.json`) were drawn as strips, and **24 of them are real PCs** that `pcmap` rejected. Most
   were logged twice about 0.9 s apart, but the earlier half is not always the same clear: in three (clusters
   c5, c15, c17) the board crops show a real lock that cleared nothing, so it is retyped to a plain lock instead
   of removed. Two phantom locks right after a PC (a010 p2, a099 p1) are removed. `corr/mk_hidden_pc.py` writes
   these 44 operations to `corr/hidden_pc.json`. The frame checks found one more PC (a059 p2), for 34 in all.
3. **Score spots.** `check/score/` found 67 spots (`corr/score/spots.json`); the 20 with an unexplained score
   change of 900 or more were kept, and 16 of them became items.
4. **Frame checks.** The 100 non-PC flags and the 16 spots made 116 items in four groups (`corr/groups/`). One
   agent per group proposed corrections (`corr/out/b*.json`), one more per group tried to refute each
   (`corr/out/v*.json`). The skeptics rejected nothing, amended six and added three the checkers had left
   (a039 p1's J and I before the KO, a049 p1's last eight events rebuilt, a phantom O removed from a101 p1).
   Two amendments change a count: a059 p1 is 86 pieces, not 85 (its last O locked out in the top row before the
   KO), and a082 p1 counts to the KO tilt at `end_s` 17198.2, not to the chain's last event (269).
5. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (95 operations: 42 retypes, 24 rebuilt
   windows, 18 removals, 11 added events, the hidden PCs included) and `corr/cells.json`. `corr/fixwas.py` ran
   `w/tetrio/metrics.py`, repaired the `was` fields that disagreed with the chain only in the third slot and widened one window (a078 p1). `corr/cells.json` was then edited
   by hand (re-running the merge would undo it): the a059 and a082 sources rewritten to the skeptics' counts,
   a101 p1's edit dropped (155 → 155), and a055 p2's REN set to 5 — the checker's 6 counted the run's clears,
   while the table's REN is the banner number (six clears in a row is REN 5).
6. **Cells.** Of the 33 cell edits, the corrected event list already gives 6 (REN and back-to-back maxima), so
   27 are hand edits: 26 piece counts and a014 p1's back-to-back, 9 from the score where the chain's run is cut
   by a BREAK the score does not show.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game` (four workers),
and `corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 216 player-games,
198 agree exactly, 16 differ by one piece and 2 are lost reads (bad bags: a044 p1, a046 p2). Six of the sixteen
are counts the frame checks changed: in a006, a011, a014, a022 and a059 p1 the last piece locked on or just
before the KO frame and has no chain event, which the recount's rule (drop a last spawn after the last chain
event) leaves out, and a074 p1's window was rebuilt from the frames. The other ten (a020 p1, a042 p1, a052 p1,
a065 p2, a078 p2, a079 p1, a084 p1, a102 p1, a105 p1, a106 p1) are one piece either way on games nobody flagged.
No piece count was changed from the recount alone, as for xo, xt, tx, nk and aj.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No Mini banner template: a mini T-spin the frame checks did not look at is counted as a plain clear.
- No opener labels (the `opener` column is empty, as for the streams).
