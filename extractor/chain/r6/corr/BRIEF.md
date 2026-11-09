# Frame-check brief: syakegohan live stream of 2026-10-30 (vs ふれあさん 5先あきぬけ), fourteen FT5 sets

Puyo Puyo Tetris 2, Tetris-vs-Tetris, 97 online games n000-n096 from ONE live-stream video,
6rUc3cXsjbo (live play, 360p rescaled to 854x480). p1 is syakegohan (left board), p2 is the opponent ふられ (right board).
Two extractors read the video; a chain fused them
into per-player-game clear events. Your job: look at the actual video frames for each item you are given and
decide whether the chain's events or counts are wrong. Correct ONLY what the frames show. "No change" is a
normal, common answer.

## Files (read-only unless stated)
- Videos: /tmp/claude-0/r6/video/<VIDEO_ID>.mp4, 854x480, 30 fps. Each game's video id is in
  /tmp/claude-0/r6/w/chain/r6/games.json (field `video`). Every time in every file is seconds in THAT game's video.
- Games: /tmp/claude-0/r6/w/chain/r6/w/A/games.jsonl (one JSON per line: id, start_s, end_s = KO frame, winner).
- Chain output per player-game: /tmp/claude-0/r6/out/chain_games.csv.
- Chain event list: /tmp/claude-0/r6/w/chain/r6/w/tetrio/cseq.json, key "n012 p1" -> list of [t, kind, lines, pc, gc].
  kind None = a piece lock with no clear, 'BREAK' = a REN break marker from extractor B, else
  single/double/triple/quad/tss/tsd/tst/tsmini. t is the spawn time of that piece as the chain logged it.
  pc 1 = perfect clear. gc = garbage rows among the cleared lines.
- Full flag list: /tmp/claude-0/r6/out/flags.json; score spots: /tmp/claude-0/r6/corr/score/spots.json.
  Your items: the group file you are given.

## Tools (run them; write images ONLY under /tmp/claude-0/r6/corr/fr/<your group>/)
- `python3 /tmp/claude-0/r6/corr/tools/sheet.py OUT.png T0 T1 STEP p1|p2|both VIDEO_ID` — contact sheet, each frame
  stamped with its time. Read the PNG with the Read tool. Keep sheets small (<= 18 frames).
- `python3 /tmp/claude-0/r6/corr/tools/score.py T0 T1 VIDEO_ID` — both players' on-screen score at every frame where it
  changes (template reader, validated on 12 frames; may show '?' when an effect covers a digit). Every clear raises
  the score a lot (hundreds to thousands, plus REN/B2B bonuses), a plain lock by a few points (drop points).
- `python3 /tmp/claude-0/r6/corr/tools/nextcount.py p1|p2 T0 T1 --video VIDEO_ID` — NEXT-queue shifts (spawns) and
  HOLD changes in the window, i.e. a piece count independent of the chain.
- `ffmpeg -v error -ss T -i /tmp/claude-0/r6/video/VIDEO_ID.mp4 -frames:v 1 x.png` for a full frame.

## Screen geometry (854x480)
- Boards: 10 columns of 15.7 px; p1 board left edge x=142.5, p2 x=553.6; floor y=389. HOLD box left of each board,
  NEXT queue (5 pieces) right of it. Score: y 392-415 under each board (8 digits). Name bars + WIN counter at the bottom.
- Clear banners (T-SPIN Single/Double/Triple, Mini T-SPIN, TETRIS, n REN, BACK to BACK, PERFECT CLEAR) appear left of
  each board near y 320-340 (PERFECT CLEAR over the board).
- KO: the loser's board tilts. end_s is that tilt frame. Locks and clears up to and including the KO frame count; later
  ones do not. The stream overlay may cover parts of the screen edge; boards are clear.

## Correction format (return as JSON in your final answer)
Event corrections (exact t of the chain's event, 2 decimals):
- remove: {"id","side","op":"remove","t","was":[kind,lines,pc]}
- retype: {"id","side","op":"retype","t","was":[kind,lines,pc],"kind","lines"[, "pc", "gc"]}
- add: {"id","side","op":"add","t","kind","lines","pc","gc"} — t must not equal an existing event's t.
- replace_window: {"id","side","op":"replace_window","t","t_end","events":[{t,kind,lines,pc,gc}...],"was_old":[[t,kind,lines],...]}
  replaces every chain event (incl. None locks and BREAKs) with t in [t, t_end]; was_old must list them exactly.
Each needs "source": what you saw, with times and image paths. Pieces are NOT re-counted from these events by every
step, so ALSO give a cell edit for pieces when you are sure the true count differs.
Cell edits: {"id","player","field","was","value","source"} — fields: pieces, garbage_received_rows, max_combo, max_b2b;
"was" = the chain_games.csv value.

## What each item type usually means
- "gap window > 4 s": extractor A could not read the NEXT queue that long; B's estimates were spliced in. Count the real
  locks and clears in the window; fix doubles and misses.
- "score_spot": the on-screen score rose by much more or less than the chain's clears there predict (guideline scoring,
  level 3: single 300, double 900, triple 1500, tetris 2400, TSS 2400, TSD 3600, TST 4800, Mini 600, x1.5 for B2B, +150
  per REN step; a zero-line T-spin is about 1200). Look for a missed clear, a phantom/duplicate clear, or a wrong type.
- "bad bag": spawn order not a 7-bag permutation there: a misread or missed/phantom spawn; check the piece count.
- "T-spin without a banner" / "banner without a clear" / "banner/type disagreement": the banner and chain type disagree.
  A banner lingers ~1.5 s, so it may belong to the previous clear. Use the score jump.
- "winner KO piece not counted": if the winner's last piece locked by the KO frame: +1 piece, and an add if it cleared.
- "PC banner onset": is it a real PERFECT CLEAR (banner and empty board), on which clear? Was it double-logged?
- "KO-tail score jump": a big score jump in the last 1.5 s before the KO with no chain clear there; usually a missed last clear.
- "unresolved lower bound": the chain lost the game partway; say whether it can be repaired by counting, else leave it.

## This capture (360p) — read before starting
- The source is 360p, so digits and the NEXT queue are blurrier than in earlier runs. The score reader still works;
  trust a clean score jump over a blurry banner. nextcount.py loses the queue more often here (bad bags).
- Extractor A misses many clears outright on this capture (mostly the right board). Banners it missed were already
  added as clears by the chain; 215 of those were confirmed by a T-spin-sized score jump and are NOT in your items.
- A also sometimes logs a clear with the wrong line count (e.g. a T-spin Double logged as 3 lines next to a TETRIS
  flash). Decide the kind AND line count from the score jump and the board.
- Score values at level 3 with B2B: TSD 5400, TST 7200, TSS 3600, quad 3600. Without B2B: TSD 3600, TST 4800,
  TSS 2400, quad 2400. TSS+B2B, TSD and quad+B2B are all 3600 — check the board for those.
- Items are sorted by player-game; handle one player-game at a time (one score.py run over the whole game is cheap
  and settles most items). Answer "no change" for an item when the frames show the chain is right.
