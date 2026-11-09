# extractor/amemiya/xKR/ — the amemiya chain run on stream xKRq6okdeUI (2026-11-02)

The same chain as `../` (archived for 4xcAmo-s-Tg), run on amemiya's stream
「【VS最強格テトラー】uyeshota！ゆうくん！テトリス15先×4回」. Nothing here is a new chain: `diffs.txt` holds every
text change against `../`, and the working copy ran from `/tmp/claude-0/xk/won/` (a cloud session's scratchpad).
There is no video, frame or feature file here.

| path | what |
|---|---|
| `diffs.txt` | `diff -u` of every text file in `../` against the copy that ran (game ids, banner templates re-cut from this video, the checks). Paths `xk-run/` are the run's copy |
| `only_in.txt` | files only in the run's copy (run outputs, logs, feature caches; none committed) |
| `REPORT.md` | the run: games found, sets, the frame check |
| `start/` | board-count grid and start-candidate scripts, the candidates and the rejected ones, and the A/B/R drivers |
| `games.json`, `mkgj.py` | the 128 games the chain read (start, upper end, opponent, WIN counter at the start and after each set's last game); `mkgj.py` writes it from `start/games_auto.json` and the counters read by eye |
| `wc/sheet.py` | the contact-sheet script the WIN counters were read from |
| `chain_games.csv` | the chain's output after the 121 event corrections, before `hand-edits.csv` |
| `check/flags.json`, `check/sanity.txt` | `apply/checks_am.py` on that output |
| `check/ocr/` | the score reader and the KO-tail comparison |
| `check/corr/` | the frame check: `BRIEF.md` (the readers' brief), `items.json` (363 items), `kotail.json`, `results/` (each reader's `g*.json` and each skeptic's `s*.json`), `event-corrections.json` and `cells.json` (what survived), `tools/` (`merge.py`, `score.py`, `sheet.py`, `nextcount.py` and its three recounts) |
| `check/freezes.json` | the lag windows |

## How the x rows of analysis/ppt2-amemiya/ were made

1. The chain wrote 128 games and 272 flags.
2. The score reader ran over the last seconds of every game; 91 score jumps before a KO with no chain clear near
   them joined the flags, 363 items in five groups.
3. One reader per group frame-checked its items and wrote event fixes, cell fixes and freeze windows; one skeptic per
   group re-read the frames of every fix and kept, rejected or amended it. `tools/merge.py` merges the verdicts and
   turns a retype or removal of a None/BREAK into a `replace_window` (the overlay only matches clear events).
4. `chain/am/w/tetrio/metrics.py` read the 121 event fixes (appended to `analysis/ppt2-amemiya/event-corrections.json`)
   and re-tallied; pool and `apply/build_games_csv.py` wrote `chain_games.csv`. Of the 152 cell fixes, 60 were
   reproduced by the re-tally; the other 92 (89 pieces, 2 max REN, 1 garbage received) went into `hand-edits.csv`
   with the re-tallied value as `was`. Pieces come from the A pass's `games.jsonl`, not from the events, so every
   pieces fix is a hand edit.
5. `--apply amemiya` took the existing `games.csv` rows followed by this `chain_games.csv` without its header.
