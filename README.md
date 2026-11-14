# ppt2-replay-report

Puyo Puyo Tetris 2 match data for syakegohan (しゃけごはん), amemiya (たいようあめみや), uyeshota (ういしょうた), narikura (ナリクラ) and yukun (ゆうくん), read frame by frame
from YouTube video.
Site: <https://yachi.github.io/ppt2-replay-report/>

PPT2 has no replay file, so every figure comes from the video. The figures are not TETR.IO figures:
the PPT2 attack table is different. The TETR.IO reports are in
[tetrio-replay-report](https://github.com/yachi/tetrio-replay-report).

## Layout

| path | what |
|---|---|
| `analysis/ppt2-<slug>/` | one directory for each player: `analysis/ppt2-syakegohan/`, `analysis/ppt2-amemiya/`, `analysis/ppt2-uyeshota/`, `analysis/ppt2-narikura/` and `analysis/ppt2-yukun/` |
| `analysis/ppt2-<slug>/games.csv` | one row for each player in each game: the data that the player's pages render |
| `analysis/ppt2-<slug>/event-corrections.json` | extractor events corrected by eye from the frames, applied before the tally |
| `analysis/ppt2-<slug>/hand-edits.csv` | cell corrections laid over the chain output, each with its source |
| `analysis/piece-pairing/` | the piece-pairing study pages (`lookup/`, `triples/`, `syakegohan/`), wrapped and rendered by `bin/build-docs` as `ppt2-lookup.html`, `ppt2-triples.html` and `ppt2-syakegohan-pairs.html` |
| `pipeline/subjects.py` | one record for each player: name, channel, data paths, page names and the caveats measured on that player's data |
| `pipeline/ppt2_page.py` | the renderer, shared by every player. It uses the Python standard library only |
| `bin/build-docs` | writes `docs/` for every player whose `games.csv` exists, and the index. With `--check`, it re-renders and byte-compares (the CI gate) |
| `docs/` | the GitHub Pages site |
| `extractor/` | the extraction chain, archived as it ran. Read `extractor/README.md` first |
| `extractor/amemiya/` | the amemiya chain, archived as it ran, with its frame-check and score-reader tools; `h3F/` is its run on the second stream |
| `extractor/autosettle/` | settles frame-check items the score OCR already decides (KO piece with an unchanged score), before the checkers run |
| `extractor/banscan-rs/` | the banner scan's NCC series (`R/banscan.py` `series()`) in Rust, parallel over frames and bit-identical to numpy; `run_banscan.py --check` compares every array |
| `extractor/nextcount-fast/` | the NEXT-queue recount (`corr/tools/nextcount.py`) with its four per-frame helpers rewritten, same answers; `run_nextcount.py --check` compares every frame |
| `extractor/pcscan-chunked/` | the PERFECT CLEAR banner scan (`R/pcscan.py`) streamed in chunks, so a long game no longer needs ~5 GB; same output file, `run_pcscan.py --check` compares it |
| `HISTORY.md` | the commit log of this report from its first home, tetrio-replay-report |

## Commands

```bash
bin/build-docs            # render docs/ from every analysis/ppt2-<slug>/games.csv
bin/build-docs --check    # fail if docs/ differs from what those games.csv files render
python3 -m pipeline.ppt2_page --apply syakegohan <chain games.csv>   # games.csv = chain output + hand-edits.csv
python3 -m pipeline.ppt2_page --apply amemiya <chain games.csv>
```

The video copyright belongs to the original authors. The site links to YouTube and copies no frame.
