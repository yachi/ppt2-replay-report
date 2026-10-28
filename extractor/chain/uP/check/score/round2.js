export const meta = {
  name: 'syakegohan-uP-score-round',
  description: 'Frame-check 26 score-sum spots where the chain predicts more points than the score shows, then verify',
  phases: [{ title: 'Check' }, { title: 'Verify' }],
}
const REPO = '/Users/yachi/codes/ppt2-replay-report'
const U = '/private/tmp/claude-501/uP'
const VID = `${U}/video/uP3FeprmAGI.mp4`
const W = `${U}/w`

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


const EXTRA = `Corrections ALREADY applied (do not duplicate; your 'was' must match the CURRENT cseq.json, which includes them): ${U}/corr/event-corrections.json and ${U}/corr/hand-edits.csv. The spots below come from a score check: the running score total on screen rose LESS than the points the chain's clear list predicts (guideline scoring at level 3: single 300, double 900, triple 1500, quad 2400, TSS 2400, TSD 3600, TST 4800, Mini 600; x1.5 on back-to-back quads and T-spins; +150 per REN step; drop points ignored). A negative 'adjusted' value means a chain clear that did not happen, a wrong type (e.g. a plain double typed TSD, a quad that was a triple), a wrong B2B (a clear between that breaks B2B), or a wrong REN (a lock between clears). It can also be the reader missing a jump while the score was hidden, then the chain is right: say no_change with the evidence.`
const CHECK2 = (i) => `${CONTEXT}\n\n${EXTRA}\n\nTASK. Checker ${i}: settle every spot in ${U}/corr/score_batch${i}.json. Frames under ${U}/corr/fr/s${i}/. Read the score before and after each clear in the window and the banners; find which clear(s) the chain got wrong. Per spot: no_change, corrected (event ops; cell edits only for pieces), or unresolved.`
const VERIFY2 = (i, r) => `${CONTEXT}\n\n${EXTRA}\n\nTASK. Skeptic for score batch ${i}. For each proposed correction, Read your OWN frames (under ${U}/corr/fr/sv${i}/) and try to refute it. keep only if the frames clearly support it; fix numbers via 'amended' (full record). index = position in its list. List in 'missed' any no_change/unresolved you can show is wrong.\n\nPROPOSED:\n${JSON.stringify(r)}`
const results = await pipeline([0, 1],
  (i) => agent(CHECK2(i), { label: `score:b${i}`, phase: 'Check', schema: CORR }),
  (r, i) => r ? agent(VERIFY2(i, r), { label: `verify:s${i}`, phase: 'Verify', schema: VERDICT }).then(v => ({ batch: i, proposed: r, verdict: v })) : null,
)
return { results }
