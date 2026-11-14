# chain/sa: syakegohan's eight short uploads of July 2026

30 games, ids `r000`–`r029`, over eight videos and three datasets. This tree is a copy of `chain/ms`, run on the
eight videos together and kept as it ran (its paths point at `/tmp/claude-0/sa/`, a cloud session's scratchpad).
It adds no frame image or video to the repo.

## Inputs

Each video is one set, first to 3. syakegohan is the LEFT board (p1) throughout.

| ids | video | dataset | opponent | score |
|---|---|---|---|---|
| r000–r004 | `3ZIHXsEMglM` | `upload-2026-07-07` | あちみつ | 3-2 |
| r005–r007 | `DiFaYIsoP2Q` | `upload-2026-07-07` | あちみつ | 3-0 |
| r008–r012 | `Llprnzb5HyE` | `upload-2026-07-07` | あちみつ | 2-3 |
| r013–r016 | `1H-Nb8dueHI` | `upload-2026-07-07` | あちみつ | 3-1 |
| r017–r019 | `P-AdNKkIJZg` | `upload-2026-07-17` | あちみつ | 3-0 |
| r020–r023 | `JeHOgt5ZD00` | `upload-2026-07-17` | あちみつ | 3-1 |
| r024–r026 | `ef8WfxqLWGE` | `upload-2026-07-17` | あちみつ | 3-0 |
| r027–r029 | `lenoq_l7Egw` | `upload-2026-07-28` | uyeshota | 3-0 |

syakegohan 23-7 over the 30 games, seven sets to one.

- The videos: native 854x480 h264, the layout ms's coordinates expect. **No rescale.**
- Games: `seg/` was run per video (`seg/v_<video>/`). seg never closes a video's last game, so `mkgames_sa.py`
  appends it: start 1.2 s after the previous end, `end_upper_s` 9 s after the WIN counter's last change (read by
  eye off the contact sheets), capped at the video's length. It asserts each game moves one counter by one and each
  video ends on a set score.

## What differs from chain/ms

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/sa/`; `games.json` carries each game's own video `path` |
| `mkgames_sa.py` | this run's games (above); `drive_s1.sh`, `drive_s2.sh` are ms's stage drivers |
| banner, word and score-digit templates, `w/ocr/T.npy` | copied from `chain/ms` (same font, same native layout). Not committed |
| `corr/tools/nextcount.py` | the reference frame is 15 s into the first game of the game's own video (ms's fixed 220 s is past the end of `ef8WfxqLWGE`) |
| `corr/merge_xo.py` | three groups (`range(3)`) |
| `apply/hand_edits_sa.py` | the hand-edit writer, paths to this run |

As for ms, `pool/pool.py` needs `pool/out/` to exist, `w/tetrio/metrics.py` needs scipy and `witnessed.json`
(`[]` here), `check/score/steps.py` needs `corr/score/`, and `corr/tools/score.py` needs `check/ocr/reader.py`
beside `w/ocr/T.npy`.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 62 flags (`corr/flags.json`): 35 PERFECT CLEAR banner onsets, 9 winner
   KO pieces, 7 banner/type disagreements, 3 bad bags, 3 T-spins with no banner, 3 KO-tail score jumps and
   2 banners with no clear.
2. **PERFECT CLEARs.** 1 onset carries `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). The others make
   21 clusters (`corr/pcclusters.json`). A lit-cell count of the board after each rejected onset
   (`corr/litcount.txt`) reads a stack after most; the 11 whose board read low went to the checkers as frame-check
   items rather than straight into `corr/hidden_pc.json`, which is therefore empty.
3. **Score spots.** `check/score/` found 44 spots (`corr/score/spots.json`); 13 with an unexplained change of 900 or
   more were kept as items.
4. **Frame checks.** 24 non-PC flags, the 11 PC onsets and the 13 spots made 48 items in three groups
   (`corr/groups/`). One agent per group proposed corrections (`corr/out/b*.json`), one more per group tried to
   refute each (`corr/out/v*.json`). The skeptics kept 46 proposals and rejected one (r001 p1's piece count 46 → 47).
   `corr/out/auto.json` (autosettle) holds only no-change verdicts and hints, so nothing from it was merged.
5. **Merge.** `corr/merge_xo.py` wrote 43 event corrections; two groups had read the same r020 p2 PERFECT CLEAR,
   so two duplicates were dropped (the later group's kept), leaving 41 (29 retypes, 12 rebuilt windows; 12 corrected clears in them
   are PERFECT CLEARs the chain had missed) and 3 cell edits. `corr/fixwas.py` ran
   `w/tetrio/metrics.py` and needed no repair.
6. **Cells.** The 3 cell edits are all piece counts and all hand edits: r004 p1 60 → 59, r015 p1 76 → 70,
   r026 p1 63 → 70. The NEXT-queue check below adds a fourth (r009 p2 30 → 29) and a 42nd correction.

## NEXT-queue recount

`corr/drive_nc.sh` recounts every player-game's pieces from the NEXT queue (`corr/nc/`, summary
`corr/nc_compare.json`). Every game's reference frame is taken from `JeHOgt5ZD00` (`NC_REFVID`): with each video's own
reference frame the queue read poorly on every video but that one. Against the table (with the hand edits):
45 same, 9 off by one (mostly the KO piece), 5 lost (the queue unreadable for a stretch), 1 off by more.

That one, r026 p1 (recount 67, table 70), was checked on the frames and the table stands: the queue is unreadable
until 135.30 and the recount misses three spawns before it. A second check (r009 p2, recount 28, table then 30) found
29: the chain logged the J that went straight into the empty hold at 85.67 as a lock, and typed the TSD at 97.57 as a
double. Both are fixed (a hand edit 30 -> 29 and a retype), so the corrections are 42 and the hand edits 4
(`corr/out/x.json`, `corr/fr/x/` is not committed).

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the other videos).
- uyeshota's three games (r027–r029, p2) are not added to uyeshota's own page.
