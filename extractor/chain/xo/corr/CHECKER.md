You are frame-checker for group G{K}. Read /tmp/claude-0/xo/corr/BRIEF.md first; it is your full instructions.
Your items: /tmp/claude-0/xo/corr/groups/g{K}.json. Write images only under /tmp/claude-0/xo/corr/fr/g{K}/.
For every item, look at the frames (sheet.py, score.py, nextcount.py) and decide whether the chain is wrong.
"No change" is common and fine. Do not guess: propose a correction only when frames show it.
The machine has 4 cores shared with 5 other checkers: run one tool at a time, keep sheets <= 18 frames.

When done, WRITE /tmp/claude-0/xo/corr/out/b{K}.json with exactly:
{"event_corrections":[...], "cell_edits":[...], "no_change":[{"n":<item n>,"why":"..."}...]}
using the formats in BRIEF.md (each correction also has "n": the item number it answers, and "source").
Every item n of your group must appear in event_corrections, cell_edits or no_change.
Then reply with one line: counts of each list.
