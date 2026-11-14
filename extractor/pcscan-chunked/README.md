# pcscan-chunked: the PERFECT CLEAR banner scan, without the whole game in memory

`R/pcscan.py` decodes a whole game into one float32 array before it computes anything. A long game needs about
5 GB, so a scan with several workers got OOM-killed. `run_pcscan.py` runs the chain's own `R/pcscan.py` unedited.
It executes everything up to the main loop (the paths, `G`, `A`, the crop and `feat()`), then reads the same ffmpeg
command's output 300 frames at a time and applies `feat()` to each chunk.

```
cd chain/<set>/w
python3 ../../../pcscan-chunked/run_pcscan.py [--check] [--chunk N] GID...
```

The output file is the same, byte for byte, and here is why. Every value pcscan writes is the per-frame mean of a
boolean mask, which is a pixel count divided by the pixel total. That is exact in float64 however the frames are
split. `--check` also runs the chain's own loop on the same games and stops unless the two JSON texts are equal.

The runner refuses a `pcscan.py` whose md5 is not in `KNOWN`. Thirty-two of the archived trees hold this exact
file. `lg` holds a different scanner (an NCC of the 'PERFECT' word at 30 fps), and the runner does not cover it.

## Measured

These were measured on 2026-11-14 on a 4-core cloud box, against the te stream's video, using te's `pcscan.py`.

| game | `R/pcscan.py` | `run_pcscan.py` |
|---|---|---|
| 150 s | 1880 MB peak, 12.5 s | 618 MB peak, 11.3 s, same file (md5) |
| 450 s | not run | 631 MB peak, 33.3 s |

The runner's peak memory does not grow with the length of the game. The 450 s figure comes from one run and was
not re-run.

## CI

`check.py` puts a stand-in `ffmpeg` on PATH that writes synthetic frames (noise plus orange and white blocks), so
no video is needed. It runs `--check` at chunk sizes 1, 7, 50 and 1000, and three planted defects must each fail:

- dropping the last partial chunk
- moving the p2 window one column
- reading the white mask as orange
