# chain/ap: syakegohan vs いわしせいじん, 15先 Part1-2 (uploaded 2025-06-22)

50 games, ids `ap00`–`ap49`, dataset `upload-2025-06-22`, two videos. This tree is a copy of `chain/ai`, run on the
two videos together and kept as it ran (its paths point at `/tmp/claude-0/ap/`, a cloud session's scratchpad). It
adds no frame image or video to the repo.

## Inputs

syakegohan is the LEFT board (p1) throughout; the RIGHT nameplate reads いわしせいじん.

| ids | video | WIN counters at the end (syakegohan first) |
|---|---|---|
| ap00–ap27 | `u6yuJv6hZU4` (Part1) | 15-13 |
| ap28–ap49 | `gk-C0KNZVuY` (Part2) | 15-7 |

syakegohan 30-20 over the 50 games.

- The videos: リプレイVer 3.5 at 854x480 (Part1 fetched at 720p and scaled down, Part2 fetched at 480p), no layout
  rescale.
- Games: `seg/` was run per video (`seg/v_<video>/`); `seg` never closes a video's last game, so `mkgames_ap.py`
  appends it and asserts each game moves one WIN counter by one.

## What differs from chain/ai

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/ap/` |
| `mkgames_ap.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `ap` |
| `corr/dedupe.py` | as in `chain/am`, no NEXT recount decision (`NC = {}`) |
| `corr/dedupe_note.txt` | what `dedupe.py` dropped |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 85 flags: 55 PERFECT CLEAR banner onsets, 13 winner KO pieces, 7
   banner/type disagreements, 5 KO-tail score jumps, 4 T-spins with no banner and 1 bad bag. `check/score/` found 35
   score spots.
2. **PERFECT CLEARs.** 13 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 26 clusters
   (`corr/pcclusters.json`), checked with a lit-cell count of the board after each (`corr/litcount.txt`); 15 left in
   doubt went to a frame check. The set holds 28 PCs (syakegohan 15, いわしせいじん 13).
3. **Frame checks.** `extractor/autosettle` settled 5 items as no change (`corr/out/auto.json`); the other items went
   to groups g0 (16 items), g1 (18) and g2 (15). One agent per group proposed corrections (`corr/out/b*.json`) and
   another tried to refute each (`corr/out/v*.json`). They rejected one: ap31 p1 pieces, where the S locks one frame
   after the game ends. g1's skeptic also noted a likely zero-line T-spin in ap37 near 743.6 s that nothing flagged;
   it was left as the chain has it.
4. **Merge.** g0 and g2 both corrected ap02, ap22 and ap26 in different ways. g2's are kept (its ap22 swap matches g0's
   skeptic's own frame reading, and g0's skeptic amended ap02 to g2's fix); g0's three are rejected in `corr/out/v0.json`
   with a `merge:` note. The g0 skeptic used item numbers as refs; they were remapped to `e<index>` in order.
   `corr/merge_xo.py` wrote the event corrections and `corr/dedupe.py` dropped 9 duplicate retypes (ap33, ap34, ap43,
   ap47) and 7 max_combo cells the chain already gives once the events are corrected, leaving 43 events
   (`corr/dedupe_note.txt`).
5. **Cells.** Four, all syakegohan's pieces: ap16 57 -> 58 and ap27 49 -> 50 (a piece locked on or just before the
   KO frame), ap30 146 -> 143 (three phantom locks), ap49 50 -> 51 (an I locked before the KO).

## NEXT-queue recount

`corr/drive_nc.sh` re-counted all 100 player-games' spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/hand_edits.csv` is the cells without a header): 79 agree,
13 differ by one, one reads two fewer (ap22 p2, 131 against 133) and 7 are lost reads. No piece count was changed from
the recount.
