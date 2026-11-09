# chain/r6: syakegohan's stream of 2026-10-30 (vs ふられさん 5先あきぬけ)

97 games, ids `n000`–`n096`, dataset `stream-2026-10-30`, video `6rUc3cXsjbo`. This tree is a copy of
`chain/xo` run on one live-stream archive, kept as it ran (its paths point at `/tmp/claude-0/r6/`, a cloud
session's scratchpad). It adds no frame image or video to the repo.

## Inputs

| games | set (syakegohan–ふられ) |
|---|---|
| n000–n006 (7) | 4–3, then a disconnect |
| n007–n012 (6) | 5–1 |
| n013–n020 (8) | 5–3 |
| n021–n027 (7) | 5–2 |
| n028–n034 (7) | 5–2 |
| n035–n039 (5) | 2–3, then a disconnect |
| n040–n048 (9) | 5–4 |
| n049–n054 (6) | 5–1 |
| n055–n062 (8) | 3–5 |
| n063–n067 (5) | 5–0 |
| n068–n075 (8) | 3–5 |
| n076–n082 (7) | 5–2 |
| n083–n087 (5) | 5–0 |
| n088–n096 (9) | 4–5 |

- The video is a 640x360 live archive. SnapYT and ytultra could not fetch it from the cloud; youtubetoolkit.com
  could. It was re-encoded to 854x480 (`scale=854:480`, no padding) so the 480p geometry applies.
  syakegohan is the LEFT board.
- Games: `seg/` as in xo. `mkgames_r6.py` writes `games.json` from the WIN-counter strings read by eye off
  contact sheets (`seg/cnt.py`); it asserts the counter rises by one per game. Four segments are not games: three
  menus, and the eighth game of set 1, where the connection dropped about 6 s in with no result. Set 6 also ended
  on a disconnect, after its fifth game finished.
- Winners: A's KO winner agrees with the WIN counter on all 97 games. syakegohan 61–36.

## What differs from chain/xo

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/r6/`; player name `syakegohan` |
| `w/B/extract_b.py` | border end `match < 0.3` for 15 frames. At 360p the border match is noisy (median ~0.75): uP's `< 0.5` for 10 frames cut B short in 63 of 97 games; this rule ends within 0.04 s of A's KO frame in all 97 |
| `w/A/analyze.py` | a T read as clearing four rows (a misread) raised `KeyError` in three games; it is kept as a quad, and the frame checks retyped it |
| `check/ocr/mktpl.py` | score-digit templates from eight frames read by eye |
| `apply/build_games_csv.py` | the opponent comes from `games.json` (metrics.csv has no opponent column) |
| `apply/hand_edits_r6.py` | **new**: `corr/cells.json` to `hand-edits.csv` rows (below) |
| `corr/triage.py`, `corr/scoretype.py` | **new**: settle flags the score already explains (below) |
| `corr/validate.py` | **new**: dry-runs metrics' overlay and lists every failing correction at once |
| `corr/merge_xo.py` | thirteen groups, the big-jump check, and the repairs listed under Merge |
| `corr/drive_nc.sh` | **new**: the NEXT-queue recount, three games at a time |

## Corrections

All 551 event corrections and 10 cell edits are in `analysis/ppt2-syakegohan/` (the cells are the rows whose
ids start with `n`).

1. **Flags.** `apply/checks_xo.py` raised 717 flags (`corr/flags.json`) and the score check (`check/score/`)
   161 spots (`corr/score/spots.json`).
2. **Triage** (`corr/triage.py`). 376 were settled without a frame check: 215 T-SPIN banners with no clear where a
   T-spin-sized score jump (2000 or more) sits next to the banner (`R/build.py` had already added those clears;
   at 360p extractor A misses many clears outright), 25 banner/type disagreements and 4 T-spins with no banner in
   player-games whose score adds up, and 132 PERFECT CLEAR onsets left to the PC pass. 502 items remained
   (`corr/tri/items.json`).
3. **PERFECT CLEARs.** At 360p `pcmap`'s "banner at least 0.9 s" rule rejects most real ones. All 88 short-onset
   clusters (`corr/pcclusters.json`) were drawn with `check/pc/pcstrip.py`: 55 were real, and the 47 the chain
   had not marked are in `corr/hidden_pc.json`. A second pass over score jumps above 8000 (`corr/out/big.json`,
   one reader, no skeptic) found two more, n012 p2 and n041 p1.
4. **Frame checks.** The 502 items made twelve groups of about 42, plus a PC group (`corr/groups/`). One agent per
   group read the frames and proposed corrections (`corr/out/b*.json`); one more agent per group tried to refute
   each (`corr/out/v*.json`). Of 550 proposals the skeptics kept 492, amended 53 and rejected 5, and added 8 the
   checkers missed.
5. **Merge** (`corr/merge_xo.py`). Besides xo's merge, it
   - drops 12 PC-group corrections that another group had already made (inside its rebuilt window, or the same
     clear within 0.15 s);
   - widens 5 one-event windows to every chain event at that time, and folds the retypes that could not
     pick their event (two clears logged at one time) at 4 such times into one window each, and sets one `was`
     to the chain's PC flag (n092 p2);
   - drops 4 piece-count edits that compared NEXT spawns with the event count inside a B-splice window, where
     the chain's piece count already includes B's pieces.
   `corr/validate.py` then reports 0 failing, and `corr/fixwas.py` runs `w/tetrio/metrics.py` cleanly.
6. **Cells** (`apply/hand_edits_r6.py`). Of 13 cell edits, 3 REN or B2B maxima are what the corrected event list
   already gives, so 10 are hand edits: 5 piece counts and 5 REN or B2B maxima. The maxima differ from metrics'
   because a B-splice window (`BREAK`) resets its runs; the checkers read the unbroken runs off the B2B and REN
   score bonuses.

## NEXT-queue recount

`corr/tools/nextcount.py --game` re-counted every player-game's spawns (`corr/nc_compare.py`, ach's rule: the
first hold into an empty box and an unmatched last spawn taken off). At 360p the reader loses the queue often. Of the
194 player-games, 38 agree with the final table exactly, 21 differ by one piece, 123 differ where the reader read bad
bags or lost the queue, and 12 differ by more on a clean read (recount against table): n002 p2 24/31, n027 p1 52/56,
n038 p1 106/103, n043 p1 172/178, n047 p2 38/50, n055 p1 97/100, n069 p1 153/146, n074 p1 164/167, n084 p1 92/82,
n086 p1 54/56, n094 p1 187/193 and n095 p1 210/221. These 12 were not frame-checked. No piece count was changed from
the recount alone; only frame-checked counts were, so the piece counts of these 12 may be wrong.

## Known gaps

- Undetermined, kept as lower bounds: n083 p1 7553–7569 s and n095 p2 8344–8358 s (the checker could not see
  every lock), n022 p2 (a bad bag), n059 p2 (the tail, where an overlay hides the score), n026 p2 (an unexplained
  +980 at about 2145.5 s), n005 p2 (whether 510.83 s is a TSS) and n011 p2 (the piece count after 920.33 s).
- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- The event list is not the lock count (B-splice windows add clears without per-lock events), so event adds and
  removes did not change any piece count; only the cell edits did.
- No opener labels (the `opener` column is empty, as for the streams).
