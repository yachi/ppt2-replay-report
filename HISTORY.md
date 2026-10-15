# History

These commits are from tetrio-replay-report, where this report lived until 2026-10-15.
The commit IDs refer to that repo.


## e5279b6 2026-10-15 fix(ppt2): frame-check pieces, garbage cleared and start times

Close the three items left open by a719717, each settled on video
frames and re-checked by an independent verify pass.

- pieces: the suspect hold-swap events are interval starts with a real
  lock inside, so g024, g042, j018 and g035 keep their counts. Two real
  defects instead: extractor A counts a first-piece hold made before
  the second spawn (g018 p2, h011 p1, -1 each; the only two in 420
  player-games), and in gap windows B's pace-estimated pieces are added
  on top of A's own count (i015 p1 86->69, i017 p1 239->233).
- garbage cleared: every frame-added or retyped clear now has its gc
  read on frames. h017 p1 +1, i015 p2 +1, g070 p1 -1; j027 p1 and
  j033 p2 were already right.
- start_s: six games started on the READY overlay. They now start on
  GO like the other 204 (+1.2 to 1.4 s). Durations do not change.
- The 點樣讀呢版 box says garbage cleared is read on frames (i016 p1 is
  the one lower bound), and names the start fix and the nine gap-window
  player-games that are not frame-checked yet.

The chain rules behind the pieces defects are deferred: they rerun the
extractors and move rows that hand corrections were written against.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KjuKsoGthP9SP5XFMFji7r

## a719717 2026-10-15 fix(ppt2): correct clears and KO-frame pieces from frame checks

Two frame-check rounds re-read every disputed row of syakegohan's
games.csv against the video.

- 30 event corrections (event-corrections.json) fix 16 player-games:
  hold swaps and spawns read as locks, missed Perfect Clears, zero-line
  T-spin Minis, untyped BREAK gaps, a TETRIS typed as a Mini, and the
  i015 p2 1605-1634 window (11 singles, REN 3 to 13). Attack, lines and
  the maxes are tallied again from the corrected events.
- hand-edits.csv grows from 31 to 58 rows: 25 pieces cells where the
  winner's last piece locks on the KO frame (or never locks), i015 p2
  pieces 62, and i015 p1 max_combo 5 (an eye lower bound).
- The 點樣讀呢版 box no longer says only two games were fixed, and now
  says that garbage cleared, DS and max REN on corrected rows are lower
  bounds.

games.csv equals the corrected chain plus the overlay, byte for byte
(md5 bdd89d7b). An independent re-tally reproduces every changed cell.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KjuKsoGthP9SP5XFMFji7r

## 5ecec57 2026-10-15 fix(ppt2): end each game on the board tilt; keep the hand edits as an overlay

Two extractor A fixes, rebuilt over all 210 games (68 rows change):
- find_end fired on an attack flash or a grey top-out dip before the KO.
  It now walks forward to the first frame where the loser's border stays
  dark for 30 frames. 18 games move. Every included duration is now within
  0.11 s of the eye-measured first-piece-to-KO time (178 of 191 within
  0.07 s), and 9 winners gain the pieces that locked before the real KO.
- A J or T in the fifth NEXT slot read as I for 3 frames, and A lost sync
  until the KO. The slot is now re-read by vote. 37 player-games change.
  g018, g042 and i002 regain the winner's final clear. The other games
  the flash reader flagged were not misses.

The FIX2 rows that replace B-spliced windows are consistent (bag score
1.0, board-cell bound holds) but were not recounted frame by frame,
including large lines drops on losers (j009, j020, g049, g068, j016,
j027). No exclusion changes. i031 p1 is still wrong and stays excluded.

The 24 hand-edited cells from a67711b existed only in games.csv, so the
rebuild dropped them. They are now hand-edits.csv (with the chain value
each one replaced), applied by `python3 -m pipeline.ppt2_page --apply`,
and load() refuses a games.csv that lacks one. h002's edit is gone: the
chain now gives its 247 / 5. g028 p1 and i026 p1 gain the last piece
that locks on the KO frame itself, which A cannot see.

The defects note now says what the KO is and what is still missing.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KjuKsoGthP9SP5XFMFji7r

## a67711b 2026-10-14 feat(docs): PPT2 cards per date and opponent; count the winner's game-ending clear

- One page per (date, opponent), like the TETR.IO session cards, with a
  card grid and an APP/PPS trend on the overview. bin/build-docs renders
  every card and treats a stale or orphan card page as drift.
- Extractors A and B stopped counting before the KO frame, so the
  winner's last clear was lost. Both now count the piece locked at or
  before the KO. 113 winner rows changed; loser rows, results,
  exclusions and durations did not.
- 15 rows corrected from video frames (banner text and score change):
  j008, h002, i016 and 12 final T-spins that the KO screen hid.
- Named the opponent of 10 excluded games from the nameplate.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KjuKsoGthP9SP5XFMFji7r

## 4c71c2b 2026-10-14 feat(docs): syakegohan PPT2 video-measured metrics page, linked from the index

210 Puyo Puyo Tetris 2 games (191 included) read off syakegohan's YouTube
videos by two independent extractors, reconciled and spot-checked. The page
pools PPS/APM/VS/APP per player and per opponent and links every game to its
video timestamp. Rendered by bin/build-docs from the committed CSV, so --check
recomputes every figure. Outside the proof chain and not TETR.IO numbers; the
page says so, and names the known final-clear undercount.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KjuKsoGthP9SP5XFMFji7r

