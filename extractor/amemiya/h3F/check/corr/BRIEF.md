# Frame-check brief: amemiya vs ふられ, YouTube h3FUsPBZmzE (stream 2026-10-28)

Puyo Puyo Tetris 2, Tetris-vs-Tetris, 56 online games f000-f056 (f027 is absent: it froze on a
disconnect). p1 is amemiya (left board), p2 is ふられ (right board). Two extractors read the video;
a chain fused them into per-player-game clear events. Your job: look at the actual video frames for
each item you are given and decide whether the chain's events or counts are wrong. Correct ONLY what
the frames show. "No change" is a normal, common answer.

## Files (read-only unless stated)
- Video: /tmp/claude-0/fr/video/full.mp4, 854x480, 30 fps. Every time in every file is seconds in this video.
- Games: /tmp/claude-0/fr/won/chain/am/w/A/games.jsonl (one JSON per line: id, start_s, end_s = KO frame, winner, per-player counts).
- Chain output per player-game: /tmp/claude-0/fr/out/chain_games.csv (pieces, lines, garbage, clear counts, max_combo, max_b2b).
- Chain event list: /tmp/claude-0/fr/won/chain/am/w/tetrio/cseq.json, key "f012 p1" -> list of
  [t, kind, lines, pc, gc]. kind None = a piece lock with no clear (one per piece; their count + clears = pieces),
  'BREAK' = a REN break marker from extractor B, else single/double/triple/quad/tss/tsd/tst/tsmini.
  t is the clear-flash (or lock) time the chain logged. pc 1 = perfect clear. gc = garbage rows among the cleared lines.
- Full flag list: /tmp/claude-0/fr/out/flags.json. Your items: the group file you are given.

## Tools (run them; write your images under /tmp/claude-0/fr/corr/fr/<your group>/)
- `python3 /tmp/claude-0/fr/corr/tools/sheet.py OUT.png T0 T1 STEP [p1|p2|both]` — contact sheet, each frame stamped with its time. Read the PNG with the Read tool.
- `python3 /tmp/claude-0/fr/corr/tools/score.py T0 T1` — the on-screen score of both players, every frame where it changes (template reader; occasionally misreads one digit or shows '?'). The score is the most reliable witness: every clear raises it by a lot (single hundreds, tetris / T-spins thousands, plus REN and B2B bonuses), a plain lock by a few points (soft/hard drop).
- `ffmpeg -v error -ss T -i /tmp/claude-0/fr/video/full.mp4 -frames:v 1 x.png` for a single full frame.

## Screen geometry (854x480)
- Boards: 10 columns of 16 px; p1 board left edge x=137, p2 x=556; floor y=391 (rows go up). HOLD box left of each board, NEXT queue (5 pieces) right of it.
- Score: y 397-420 under each board (8 digits). Name bars and the WIN counter at the bottom.
- Clear banners (T-SPIN Single/Double/Triple, Mini, TETRIS, REN n, Back to Back, PERFECT CLEAR) appear beside/over each board.
- KO: the loser's board tilts. end_s is that tilt frame. The winner's locks and clears up to and including the KO frame count; anything after does not. The loser's last piece (the one that tops out) is counted as a piece if it locked.

## Correction format (return these; the coordinator writes the files)
Event corrections (apply to cseq events, exact t of the chain's event, rounded to 0.01):
- remove: {"id","side","op":"remove","t", "was":[kind,lines,pc]}
- retype: {"id","side","op":"retype","t","was":[kind,lines,pc],"kind","lines"[, "pc", "gc"]}
- add: {"id","side","op":"add","t","kind","lines","pc","gc"} — t must not equal an existing event's t; use the clear-flash time.
- replace_window: {"id","side","op":"replace_window","t","t_end","events":[{t,kind,lines,pc,gc}...],"was_old":[[t,kind,lines],...]} — replaces every chain event (including None locks and BREAKs) with t in [t, t_end]; was_old must list them exactly. Use for a mangled stretch.
Each needs "source": what you saw, with times and image paths. Kinds: single double triple quad tss tsd tst tsmini.
Note a plain (non-clearing) lock is a None event; adding/removing a clear does not change the piece count by itself (the coordinator re-tallies pieces from the event list only for clear events) — so ALSO report a cell edit for pieces when the true piece count differs.
Cell edits: {"id","player":"p1|p2","field","was","value","source"} — fields: pieces, garbage_received_rows, garbage_cleared, max_combo, max_b2b. "was" = the chain_games.csv value. Count pieces from NEXT-queue shifts / spawns when a window is in doubt.
Freeze windows: for a game with a long stall, report each window where the game visibly runs in slow motion or freezes because of network lag (both boards stalled, scores frozen): {"id","t0","t1","note"}.

## What each item type usually means
- "gap window > 4 s": extractor A could not read the NEXT queue for that long, and extractor B's estimated pieces/clears were spliced in. Often lag (both players stalled) or a hold-heavy stretch. Check the events in that window against the frames: count the real pieces locked and real clears; fix double counts (B duplicating A) and misses. Report freeze windows when it is lag.
- "PPS outside 0.5..4": the game is mostly lag; measure the freeze windows.
- "bad bag score": spawn order is not a 7-bag permutation at those spawns, i.e. a misread or missed/phantom spawn; check the piece count around there.
- "A T-spin with no banner" / "banner without A clear" / "banner/type disagreement": a T-spin banner and the chain's clear type disagree. A banner lingers ~1.5 s, so a banner can belong to the previous clear. Use the score jump.
- "KO-frame last piece": the winner's last piece may have locked on/before the KO frame and not been counted. If it locked by the KO frame: +1 piece (cell edit), and an add event if it cleared lines.
- "PC banner fix" / "PC count": the chain moved or de-duplicated a PERFECT CLEAR. Confirm the board was really empty after that clear (PERFECT CLEAR banner and empty board), and that the PC was not double-logged.
- kotail: the score reader saw a big score jump in the last 1.5 s before KO and the chain has no clear there. Usually the winner's last clear (or the loser's) that the chain missed. Decide what clear it was (banner, lines, the score size) and whether it happened by the KO frame.

## Earlier examples of good sources (from the 2026-10-27 report)
- remove: "B splice duplicates the 5 REN single of A interval 427.77 (flash 432.97); NEXT shifts only at 427.77/433.63/449.33; score 22005 frozen 433.5-448.6"
- retype: "Z-piece plain double; the T-SPIN Double banner at 289.65 is the lingering one from the 287.87 TSD. Score 56048->57128 (+1080); a TSD would be >= 5400"
- add: "T piece locks ~291.15 and clears garbage row 3 (flash 291.23) with the T-SPIN Single banner + 2 REN, score 57144->59844. The KO tilt is ~291.47, so the lock comes first; the chain had no event for it"
