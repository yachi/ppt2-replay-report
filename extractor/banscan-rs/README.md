# banscan-rs — the banner scan's NCC series in Rust

`R/banscan.py` spends its compute in `series(F,t,x,y)`: for every frame, normalised cross-correlation of a
banner template over a 7×9 window of offsets, keeping the best score and its offset. This crate computes the
same two arrays in Rust, split over threads by frame, **bit for bit**: the max scores compare equal as float32
bits and the argmax indices exactly.

It gets there by doing the float32 arithmetic in numpy's order rather than by being close: numpy's pairwise sum
(blocks of 128, eight accumulators) over each window row of `w*3` floats, rows accumulated from 0. The
template's mean and norm are still computed by numpy, in the wrapper, with banscan's own expressions. Frames
from ffmpeg are integers, so the window mean is exact in any order; the products are not, which is why the
order matters.

## Use

```bash
cd /tmp/claude-0/<set>/w                      # a chain's work dir, as for R/banscan.py
python3 <repo>/extractor/banscan-rs/run_banscan.py --check GID...   # first run of a new chain
python3 <repo>/extractor/banscan-rs/run_banscan.py GID...           # after that
```

`run_banscan.py` reads the chain's own `R/banscan.py`, swaps its `series()` for the Rust one and runs the rest
unchanged, so it writes the same `R/ban/GID.npz`. No chain file is edited, and archived chains are not re-run.
`--check` also runs the numpy `series()` on every call and stops at the first array that differs. The library
builds itself with `cargo build --release` on first use. `BANSCAN_THREADS` sets the thread count (default: all
cores).

`check.py` needs no video: synthetic integer frames, five templates of banscan's sizes, constant frames (every
score 0, so the argmax must be the first offset) and period-2 frames (tied offsets), then a 1-ulp change to one
output and a one-cell change to a template, each of which the comparison must catch. CI runs it.

## Measured (2026-11-14, 4 cores)

| stream | game window | series calls | frames scanned | numpy | Rust | arrays |
|---|---|---|---|---|---|---|
| uyeshota `10ell5aAJuo` (`te`), 480p | 1500–1590 s | 50 | 27 300 | 15.7 s | 1.2 s | all identical |
| uyeshota `XoaWLJowuCQ` (`xo`), 480p | 4000–4060 s | 40 | 18 300 | 13.7 s | 0.9 s | all identical |

Templates for these runs were cut from frames of the same videos (the chains' `R/fr/*.png` are not committed);
the comparison does not depend on what the template shows. With the series this fast, the ffmpeg decode of the
strips is most of banscan's wall time.
