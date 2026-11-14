# nextcount-fast — the NEXT-queue recount, same answers, faster

`corr/tools/nextcount.py` reads the NEXT queue and hold box on every frame. Per frame, almost all of its time is in
four helpers: `locate()` (an FFT correlation that finds the queue column), `classify2()` (seven colour masks per
slot), `shape_of()` (`np.percentile` on the mask) and `white()`. `fastnc.py` has a drop-in for each that returns
the same values. `run_nextcount.py` runs a chain's own `nextcount.py` with those four swapped and everything else
unchanged: the same command line and the same output.

| helper | what changed | why the answer is the same |
|---|---|---|
| `locate` | `fftconvolve(m, t[::-1,::-1], 'valid')` written out with `scipy.fft`, the template's transform cached | the same `rfftn` / `irfftn` calls on the same padded shapes and the same centred crop, so the same floats; it also skips importing `scipy.signal` (about 7 s) |
| `white`, `classify2` | channel-by-channel min, max and sum instead of reducing a length-3 axis; the seven masks in one array | integer arithmetic; `argmax` takes the first maximum, as the original's strict `>` scan does |
| `shape_of` | `np.percentile` (method `linear`) written out for a sorted array | numpy's own steps: index `(n-1)*q`, floor, `_lerp`'s two-sided form; `np.nonzero` gives the rows sorted and the columns are sorted |

## Use

```bash
cd /tmp/claude-0/<set>/w/chain/<set>         # where corr/tools/nextcount.py is run from
python3 <repo>/extractor/nextcount-fast/run_nextcount.py --check --game GID p1   # first run of a new chain
python3 <repo>/extractor/nextcount-fast/run_nextcount.py --game GID p1           # after that
python3 <repo>/extractor/nextcount-fast/run_nextcount.py p1 T0 T1 --video ID      # the window mode
```

`--check` also reads every frame with the original helpers and stops unless `read_state()` returns the same
queue, hold and `(dx, dy, score)`. `--tool PATH` points at a `nextcount.py` elsewhere. The runner refuses a
`nextcount.py` whose four helpers, `read_state`, `frames` or the constants they read differ from the version
checked here (`fastnc.KNOWN`); every chain's copy under `extractor/chain` and `extractor/amemiya` has that
fingerprint as of 2026-11-14. `--force` runs anyway, and a new fingerprint goes in `KNOWN` after a `--check`
run passes.

`check.py` needs no video. It draws synthetic frames (a white-outlined queue column and hold box, pieces in the
queue's colours and shapes, noise, random offsets, blank and saturated frames), compares `read_state()` with
both sets of helpers, compares `pct()` with `np.percentile` on 40 000 arrays, then plants three defects (one ulp
in the locate score, S read as T, a percentile off by 1e-9) and requires each to be caught. CI runs it.

## Measured (2026-11-14, one core)

uyeshota `10ell5aAJuo` (`te`), p1, 1500–1560 s, 1801 frames, `--check`: every `read_state()` identical, and the
printed output is byte-identical to the chain's own `nextcount.py`. The helpers took 5.3 s against 18.1 s for the
originals (11 s of it without the one-off `scipy.signal` import). What remains is mostly ffmpeg's decode and
the two FFTs.
