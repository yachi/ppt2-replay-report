You are frame-checker for group G4. Read /tmp/claude-0/c/corr/BRIEF.md first; it is your full instructions.
Your items: /tmp/claude-0/c/corr/groups/g4.json. Write images only under /tmp/claude-0/c/corr/fr/g4/.
For every item, look at the frames (sheet.py, score.py, nextcount.py) and decide whether the chain is wrong.
"No change" is common and fine. Do not guess: propose a correction only when frames show it.
The machine has 4 cores shared with up to 7 other agents: run one tool at a time, keep sheets <= 18 frames.

When done, WRITE /tmp/claude-0/c/corr/out/b4.json with exactly:
{"event_corrections":[...], "cell_edits":[...], "no_change":[{"n":<item n>,"why":"..."}...]}
using the formats in BRIEF.md (each correction also has "n": the item number it answers, and "source").
Every item n of your group must appear in event_corrections, cell_edits or no_change.
Then reply with one line: counts of each list.

Extra for G4: every item is a NEXT-queue recount that disagrees with the table's piece count. Most show 2-3 chain
events within 0.5 s of each other with no NEXT shift, i.e. possible phantom/duplicate locks (often a None lock right
before a clear, both logged at nearly the same t). Check each with score.py (drop points per lock) and nextcount.py /
contact sheets around those times. For a phantom, propose a remove (or replace_window if a clear is involved) AND a
pieces cell edit to the count the frames give. If the recount itself is wrong (e.g. a hold it missed), say no_change.
