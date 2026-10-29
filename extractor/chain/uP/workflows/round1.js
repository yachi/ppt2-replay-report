export const meta = {
  name: 'syakegohan-uP3FeprmAGI',
  description: 'Preflight, extract and frame-check the syakegohan 2026-10-28 stream uP3FeprmAGI (vs ふれあさん, FT5 winner-stays)',
  phases: [
    { title: 'Preflight', detail: 'geometry gate, sides, game starts, opponents, WIN counter' },
    { title: 'Extract', detail: 'TJc chain with per-game process pools; KO-tail score reader; flags split into batches' },
    { title: 'Check', detail: 'frame-check each batch of flags' },
    { title: 'Verify', detail: 'one skeptic per batch' },
    { title: 'Audit', detail: 'unflagged sample + lag windows, in parallel with the checks' },
  ],
}

const REPO = '/Users/yachi/codes/ppt2-replay-report'
const U = '/private/tmp/claude-501/uP'
const VID = `${U}/video/uP3FeprmAGI.mp4`
const W = `${U}/w`

const BASE = `You work on the PPT2 video report repo ${REPO} (READ ONLY for you: never edit, add or commit there). Your work tree is ${W} (create it); write ONLY under ${U}/ (never ${U}/video/). No rm (write new files instead). Do not install packages globally; uv run/uvx are fine. Python+numpy+ffmpeg are available. The machine has 11 cores: run every per-game step as a process pool of 9 workers (xargs -P 9, multiprocessing, or shards in background processes); never loop games serially when the step is per-game, and never run two pools at once.
VIDEO: ${VID} (854x480, 30 fps, YouTube uP3FeprmAGI). It may still be downloading (yt-dlp writes ${VID}.part); wait until ${VID} exists (poll with an until-loop, the ETA is a few minutes).
STREAM: syakegohan (しゃけごはん) channel, played 2026-10-28, title "vs ふれあさん 5先あきぬけ" (first-to-5 sets, winner stays, so several opponents may rotate). syakegohan should be the LEFT board = p1, as in every earlier syakegohan video.
OUTPUT FORMAT: rows exactly like ${REPO}/analysis/ppt2-syakegohan/games.csv (same header and column order); ids l000, l001, ... in time order (prefix l is unused); dataset stream-2026-10-28; video uP3FeprmAGI; p1 who=syakegohan; p2 who=opponent nameplate; opponent column = right nameplate text on both rows, Japanese exactly as shown.
TEMPLATE: the most recent syakegohan set is ${REPO}/extractor/chain/TJc (read its README.md first: kofinal.py for the winner's last piece at the KO, pcmap.py for Perfect Clears, seg/ for game starts and WIN-counter winners, drive.sh for the order). Background: ${REPO}/extractor/README.md (defects D1-D6), ${REPO}/HISTORY.md, and the amemiya port ${REPO}/extractor/amemiya/ (README.md, PORT.md: geometry recalibration, a re-cut Mini banner template, the KO-tail score reader in check/ocr and check/ocrall).`

const PREFLIGHT = `${BASE}

TASK: PREFLIGHT ONLY - prove the chain can run before anyone runs it. Do not run extractors A or B over whole games.
1. Copy ${REPO}/extractor/chain/TJc to ${W}/chain/sy (and ${REPO}/extractor/perf/solve_fast.py if needed) and rewrite every /tmp/claude-0/... path to this tree and video. Record every change in ${W}/PORT.md (diffs).
2. GEOMETRY GATE: on 6 frames from at least 3 different games, decode boards (A feat.cells), NEXT, HOLD and frame borders with the TJc constants and compare with the image you Read. If off, recalibrate (the amemiya PORT.md shows how) and re-gate. Also confirm the left nameplate is syakegohan in every game you sample.
3. GAMES: run seg/ (starts, menu filter, WIN-counter winners) over the whole video with a process pool (split the video into time shards). Check each start is GO, not READY (defect D5). Read the right nameplate for every game (one frame per game, Read it). Build ${W}/chain/sy/games.json in the TJc format with ids l000... Count games per opponent and the series score from the WIN counter.
4. Write ${W}/PREFLIGHT.md. Return the structured result; ok=false if the geometry gate fails after recalibration, or the games cannot be segmented.`

const PRE_SCHEMA = { type: 'object', properties: {
  ok: { type: 'boolean' }, games: { type: 'number' }, geometry: { type: 'string' },
  left_is_syakegohan: { type: 'boolean' },
  opponents: { type: 'array', items: { type: 'object', properties: { name: { type: 'string' }, games: { type: 'number' }, syakegohan_won: { type: 'number' } }, required: ['name', 'games', 'syakegohan_won'] } },
  issues: { type: 'array', items: { type: 'string' } },
}, required: ['ok', 'games', 'geometry', 'left_is_syakegohan', 'opponents', 'issues'] }

const EXTRACT = (pre) => `${BASE}

PREFLIGHT RESULT (done; the ported tree is ${W}/chain/sy, games in ${W}/chain/sy/games.json, notes ${W}/PREFLIGHT.md and ${W}/PORT.md):
${JSON.stringify(pre)}

TASK: EXTRACT.
1. Run the chain in drive.sh order, but parallel: A features/analysis per game in a 9-process pool (A/run_all.py uses ThreadPoolExecutor(2): raise it or shard it), B sample.py + runner per game in a 9-process pool, R/evrun, R/banscan and R/pcscan sharded 9 ways. Serial steps (gapchk, bagchk, part, kofinal, fuse, build, seqs, pcmap, metrics) stay serial. Log wall time per step in ${W}/TIMES.md.
2. T-spin Minis: TJc had no Mini banner template, so it counted none. Find a T-SPIN MINI banner in this video (the amemiya port did this: extractor/amemiya/PORT.md) and cut the template, so Minis are detected. If this video has none, say so.
3. Perfect Clears: build PCDEC with pcmap.py as TJc did; put every PC banner onset in flags (do not eyeball them all yourself).
4. Make tetrio/metrics.py load corrections from ${U}/corr/event-corrections.json if that file exists (else []), and dump the exact event list tally() sees, per player-game, to tetrio/cseq.json as {"<id> <p>": [[t, kind, lines, pc, gc], ...]} both before ('<id> <p> pre') and after the overlay. The overlay code and op semantics: ${REPO}/extractor/apply/patch_overlay3.py header (the amemiya tree /private/tmp/claude-501/am/w/chain/am/w/tetrio/metrics.py already has exactly this patch; copy its approach).
5. Build ${U}/out/chain_games.csv (pool.py + build_games_csv.py as the amemiya port did, or TJc's way). Sanity: one p1/p2 row per game, one winner, the winner equals the WIN counter for every game, PPS 0.5-4, APP 0-1.5.
6. KO-TAIL SCORE READER: adapt extractor/amemiya/check/ocr/ocr.py (digit templates C2.npy/samp2.npy are for the amemiya capture: the score box position and scale differ here, so rebuild the templates for this capture and validate the reader against the score you read by eye on 3 games). Run it over every game (9-process pool, window start-1 .. A end+1.5 s). Score jumps >= 60 points within the last 1.5 s before A's end with no chain clear event in cseq.json are KO-tail flags. Do NOT use whole-game score-vs-clear counts as flags: the reader merges clears that are close together.
7. Write ${U}/out/flags.json = list of {id, player, field_or_issue, detail, t_s} for every row a human should frame-check: bad bag, gap windows > 4 s (B splices, D2/D3), banner/type disagreements, banners without a clear, T-spins without a banner, PC onsets, KO-tail score jumps, unresolved lower bounds, outliers, unreadable nameplates.
8. Split the flags into B batch files ${U}/corr/batch0.json ... balanced by flag count, whole games kept together, with B = max(1, min(3, ceil(n_flags/45))). Write ${U}/out/REPORT.md (timings, counts, deviations, what was not done).
Return the structured result. Never fabricate rows; say plainly what was not done.`

const EX_SCHEMA = { type: 'object', properties: {
  csv: { type: 'string' }, games: { type: 'number' }, included: { type: 'number' }, n_flags: { type: 'number' },
  batches: { type: 'number' }, win_counter_agree: { type: 'string' }, tsmini_detected: { type: 'boolean' },
  not_done: { type: 'array', items: { type: 'string' } }, summary: { type: 'string' },
}, required: ['csv', 'games', 'included', 'n_flags', 'batches', 'win_counter_agree', 'tsmini_detected', 'not_done', 'summary'] }

const CONTEXT = `CONTEXT. Video ${VID} (854x480, 30 fps). Left board p1 = syakegohan, right p2 = opponent. Chain output ${U}/out/chain_games.csv; game windows ${W}/chain/sy/games.json; the exact clear-event list per player-game that the tally used is ${W}/chain/sy/w/tetrio/cseq.json: key "<id> <p>" -> [[t, kind, lines, pc, gc], ...]; kind None = a lock with no clear, 'BREAK' = REN break, else single/double/triple/quad/tss/tsd/tst/tsmini; t = spawn time of that piece. Attack, lines, REN, B2B and clear counts are RECOMPUTED from this list, so fix them with EVENT corrections, never cells. Only non-derived fields (pieces, garbage_received_rows, duration_s, start_s, won, opponent) take CELL corrections, with was = the value in chain_games.csv. Event ops and exact semantics: header of ${REPO}/extractor/apply/patch_overlay3.py (remove/retype/setpc need t equal to exactly one non-None non-BREAK event (2 decimals) and was = [kind, lines, pc] of it; add needs no event at t). Examples of earlier corrections: ${REPO}/analysis/ppt2-syakegohan/event-corrections.json and hand-edits.csv, and ${REPO}/analysis/ppt2-amemiya/ (same formats). The KO is the frame where the loser's board starts to tilt; locks at or before it count, later ones do not. Lag slow-motion (the game updates only 2-3 times a second) is not a freeze; pieces still lock in it.
Extract frames with ffmpeg (-ss t -frames:v 1, or 30 fps bursts) and LOOK at them with Read; crop/zoom to read banners, REN counter, score, NEXT queue, WIN counter. Write only under ${U}/corr/. No rm.`

const CORR = { type: 'object', properties: {
  decisions: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, player: { type: 'string' }, issue: { type: 'string' }, verdict: { type: 'string', enum: ['no_change', 'corrected', 'unresolved'] }, note: { type: 'string' } }, required: ['id', 'player', 'issue', 'verdict', 'note'] } },
  event_corrections: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, side: { type: 'string' }, op: { type: 'string' }, t: { type: 'number' }, was: { type: 'array' }, kind: { type: 'string' }, lines: { type: 'number' }, pc: { type: 'number' }, gc: { type: 'number' }, t_end: { type: 'number' }, events: { type: 'array' }, was_old: { type: 'array' }, source: { type: 'string' } }, required: ['id', 'side', 'op', 't', 'source'] } },
  cell_edits: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, player: { type: 'string' }, field: { type: 'string' }, was: { type: 'string' }, value: { type: 'string' }, source: { type: 'string' } }, required: ['id', 'player', 'field', 'was', 'value', 'source'] } },
}, required: ['decisions', 'event_corrections', 'cell_edits'] }

const VERDICT = { type: 'object', properties: {
  reviews: { type: 'array', items: { type: 'object', properties: { kind: { type: 'string', enum: ['event', 'cell'] }, index: { type: 'number' }, keep: { type: 'boolean' }, reason: { type: 'string' }, amended: { type: 'object' } }, required: ['kind', 'index', 'keep', 'reason'] } },
  missed: { type: 'array', items: { type: 'string' } },
}, required: ['reviews', 'missed'] }

const CHECK = (i) => `${CONTEXT}

TASK. Frame-checker ${i}: settle every flag in ${U}/corr/batch${i}.json ({id, player, field_or_issue, detail, t_s}). Save frames under ${U}/corr/fr/b${i}/. Per flag: no_change, corrected (event ops and/or cell edits), or unresolved (say why). Gap windows: decide lag vs a real stall from frames, count real spawns from NEXT shifts, fix B splices. KO-tail score jumps: was there a lock and clear before the tilt that the chain missed (add event + pieces +1)? PC onsets: is it a real PERFECT CLEAR banner, on which clear? Each correction's source names the frames and what they show (banner text, score before/after, NEXT shift). If two flags lead to the same fix, emit it once.`

const VERIFY = (i, r) => `${CONTEXT}

TASK. Skeptic for batch ${i}. For EACH proposed correction below, extract and Read your OWN frames (save under ${U}/corr/fr/v${i}/) and try to refute it: wrong banner reading, wrong t, was not matching cseq.json, an add where an event exists, a lock after the KO tilt, a duplicate, a wrong pieces count. keep only if the frames clearly support it; fix numbers via 'amended' (full record). index = position in its list. List in 'missed' any no_change/unresolved decision you can show is wrong.

PROPOSED:
${JSON.stringify(r)}`

const AUDIT = `${CONTEXT}

TASK. Auditor, in parallel with the checkers. Results in your final text, concise with numbers and frame paths (frames under ${U}/corr/fr/audit/):
1. Pick 3 games with no flag in ${U}/out/flags.json (different opponents if possible). For both players, compare every clear banner + score change on video with the clear events in cseq.json (type and time), the winner, and the duration (first piece to KO). Report each disagreement {id, player, t, chain, video} and what the fix is.
2. Lag: find windows >= 1 s where both boards update on <= 8 of 30 frames (lag slow-motion), per game; write ${U}/corr/lag.json [{id, t0, t1, secs}] and report the total and share of play time.
3. Non-game footage: confirm nothing between the detected games is a Tetris-vs-Tetris game the segmenter missed (sample the gaps).`

phase('Preflight')
const pre = await agent(PREFLIGHT, { label: 'preflight', phase: 'Preflight', schema: PRE_SCHEMA })
if (!pre || !pre.ok) { log('preflight failed: stopping before extraction'); return { pre } }
log(`preflight ok: ${pre.games} games; geometry: ${pre.geometry}`)

phase('Extract')
const ex = await agent(EXTRACT(pre), { label: 'extract', phase: 'Extract', schema: EX_SCHEMA })
if (!ex || !ex.n_flags) return { pre, ex }
log(`extract: ${ex.games} games, ${ex.n_flags} flags in ${ex.batches} batches`)

const ids = Array.from({ length: ex.batches }, (_, i) => i)
const auditP = agent(AUDIT, { label: 'audit', phase: 'Audit' })
const results = await pipeline(ids,
  (i) => agent(CHECK(i), { label: `check:b${i}`, phase: 'Check', schema: CORR }),
  (r, i) => r ? agent(VERIFY(i, r), { label: `verify:b${i}`, phase: 'Verify', schema: VERDICT }).then(v => ({ batch: i, proposed: r, verdict: v })) : null,
)
const audit = await auditP
return { pre, ex, results, audit }
