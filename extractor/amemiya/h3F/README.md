# extractor/amemiya/h3F/ — the amemiya chain run on stream h3FUsPBZmzE (2026-10-28, vs ふられ)

The same chain as `../` (archived for 4xcAmo-s-Tg), run again on a second stream. Nothing here is a new
chain: `diffs.txt` holds every change against `../`, and the working copy ran from `/tmp/claude-0/fr/won/`.
There is no video, frame or feature file here.

| path | what |
|---|---|
| `diffs.txt` | `diff -u` of every text file in `../` against the copy that ran (game ids, banner templates re-cut from this video, `trust.py`'s WIN counter for f026, the checks) |
| `REPORT.md` | the run: games found, what was excluded and why, the frame check |
| `start/` | the board-count grid and start-candidate scripts, the candidates and the rejected ones, for the stream and for the duplicate third segment |
| `games.json` | the 56 games the chain read (start, upper end, opponent, WIN counter at the start) |
| `wc/` | the WIN counter, read by eye off a contact sheet for every game start |
| `chain_games.csv` | the chain's output after the 74 event corrections, before `hand-edits.csv` |
| `check/flags.json`, `check/sanity.txt` | `apply/checks_am.py` on that output |
| `check/ocr/` | the score reader (`tmpl.py` cuts digit templates from 5 hand-read frames) and the KO-tail comparison |
| `check/corr/` | the frame check: `BRIEF.md` (the readers' brief), `items.json` (the 180 items: 146 flags, 34 KO-tail spots), `kept.json` (every verified event fix, cell fix and freeze), `tools/` |
| `check/freezes.json` | lag, stream-skip and rollback windows |

## How the f rows of analysis/ppt2-amemiya/ were made

1. The chain wrote `chain_games.csv` (56 games, 146 flags).
2. The score reader ran over the last 4 s of every game; 34 score jumps before a KO with no chain clear near them
   were added to the 146 flags.
3. A workflow split the 180 items into four groups. One reader per group frame-checked each item and wrote event fixes,
   cell fixes and freeze windows; a second agent per group tried to refute each fix on the frames. Only fixes that
   survived are in `kept.json`.
4. `chain/am/w/tetrio/metrics.py` read the 74 event fixes (now appended to `analysis/ppt2-amemiya/event-corrections.json`)
   and re-tallied; the cell fixes the re-tally did not already reproduce (38) and the two exclusions went into
   `hand-edits.csv`.
5. `analysis/ppt2-amemiya/games.csv` holds both streams, so `--apply` takes both chain outputs in one file:
   the 10-27 rows, then this directory's `chain_games.csv` without its header. Hand edits already applied pass,
   because `--apply` accepts a cell that already holds the edited value.
