You are the skeptic for group G{K}. Read /tmp/claude-0/xo/corr/BRIEF.md (same tools, same files).
A checker read the frames for the items in /tmp/claude-0/xo/corr/groups/g{K}.json and proposed corrections in
/tmp/claude-0/xo/corr/out/b{K}.json. Your job is to try to REFUTE each proposal by looking at the frames
yourself (score.py jumps, nextcount.py spawns, contact sheets). Write images only under /tmp/claude-0/xo/corr/fr/v{K}/.
The machine has 4 cores shared with other agents: run one tool at a time.

For event_corrections[i] use ref "e<i>", for cell_edits[i] ref "c<i>". Verdicts:
- "keep": the frames confirm it.
- "amend": partly right; give "amended": an object of the fields to replace (same format), e.g. {"value": 112} or {"gc": 1}.
- "reject": the frames do not support it (say what you saw).
Also skim no_change: if one of them is clearly wrong, add {"ref":"n<item n>","verdict":"missed","why":...,"proposal":{...full correction...}}.

WRITE /tmp/claude-0/xo/corr/out/v{K}.json as a JSON list of {"ref","verdict","why"[,"amended"|"proposal"]},
one entry per e*/c* ref. Then reply with one line: counts of keep/amend/reject/missed.
