//! The NCC series of a chain's R/banscan.py `series(F,t,x,y)`, bit for bit, in parallel over frames.
//! The caller passes the mean-subtracted template `tt` (h,w,3) and its norm `tn`, both computed by numpy
//! exactly as banscan.py does; this computes, per frame, the 7x9 window of scores and returns the max and the
//! first argmax, as `flat.max(1)` and `flat.argmax(1)` do.
//!
//! Summation order is numpy's float32 pairwise sum (loops_utils.h.src, PW_BLOCKSIZE 128) over each window row
//! of w*3 floats, accumulated row by row from 0.0, which is how numpy reduces axes (3,4,5) of the strided view.

// numpy's pairwise summation for float32
fn pw(a: &[f32]) -> f32 {
    let n = a.len();
    if n < 8 {
        let mut r = -0.0f32;
        for &x in a {
            r += x;
        }
        r
    } else if n <= 128 {
        let mut r = [0f32; 8];
        r.copy_from_slice(&a[0..8]);
        let mut i = 8;
        while i < n - (n % 8) {
            for j in 0..8 {
                r[j] += a[i + j];
            }
            i += 8;
        }
        let mut res = ((r[0] + r[1]) + (r[2] + r[3])) + ((r[4] + r[5]) + (r[6] + r[7]));
        while i < n {
            res += a[i];
            i += 1;
        }
        res
    } else {
        let mut n2 = n / 2;
        n2 -= n2 % 8;
        pw(&a[..n2]) + pw(&a[n2..])
    }
}

const OY: usize = 7; // y-3 .. y+3
const OX: usize = 9; // x-4 .. x+4

fn frame(fr: &[f32], rs: usize, tt: &[f32], tn: f32, h: usize, w: usize, y0: usize, x0: usize, p: &mut [f32], q: &mut [f32]) -> (f32, i64) {
    let n = h * w * 3;
    let rl = w * 3;
    let mut best = 0f32;
    let mut bk = -1i64;
    for oy in 0..OY {
        for ox in 0..OX {
            let by = y0 + oy;
            let bx = x0 + ox;
            let mut acc = 0f32;
            for a in 0..h {
                let s = (by + a) * rs + bx * 3;
                acc += pw(&fr[s..s + rl]);
            }
            let m = acc / n as f32;
            let mut num = 0f32;
            let mut dsq = 0f32;
            for a in 0..h {
                let s0 = (by + a) * rs + bx * 3;
                for k in 0..rl {
                    let v = fr[s0 + k] - m;
                    p[k] = v * tt[a * rl + k];
                    q[k] = v * v;
                }
                num += pw(&p[..rl]);
                dsq += pw(&q[..rl]);
            }
            let den = dsq.sqrt() * tn + 1e-6f32;
            let s = num / den;
            let k = (oy * OX + ox) as i64;
            // numpy argmax: first maximum; a NaN is the maximum and the first NaN wins
            if bk < 0 || (!best.is_nan() && (s > best || s.is_nan())) {
                best = s;
                bk = k;
            }
        }
    }
    (best, bk)
}

/// Returns 0 on success, 1 on a window outside the frame, 2 on bad arguments.
/// f: nf frames of (fh, fw, 3) float32, C order. tt: (h, w, 3). y0, x0: the window's top-left in the frame
/// (banscan's y-3-Y0 and x-4). out_max: nf float32, out_k: nf int64.
#[no_mangle]
pub unsafe extern "C" fn ncc_series(
    f: *const f32, nf: usize, fh: usize, fw: usize,
    tt: *const f32, h: usize, w: usize, tn: f32,
    y0: i64, x0: i64,
    out_max: *mut f32, out_k: *mut i64, threads: usize,
) -> i32 {
    if h == 0 || w == 0 || fw == 0 || fh == 0 {
        return 2;
    }
    if y0 < 0 || x0 < 0 || y0 as usize + OY - 1 + h > fh || x0 as usize + OX - 1 + w > fw {
        return 1;
    }
    if nf == 0 {
        return 0;
    }
    let fs = fh * fw * 3;
    let fall = std::slice::from_raw_parts(f, nf * fs);
    let tt = std::slice::from_raw_parts(tt, h * w * 3);
    let om = std::slice::from_raw_parts_mut(out_max, nf);
    let ok = std::slice::from_raw_parts_mut(out_k, nf);
    let (y0, x0) = (y0 as usize, x0 as usize);
    let nt = threads.max(1).min(nf);
    let per = (nf + nt - 1) / nt;
    std::thread::scope(|sc| {
        for ((fc, mc), kc) in fall.chunks(per * fs).zip(om.chunks_mut(per)).zip(ok.chunks_mut(per)) {
            sc.spawn(move || {
                let mut p = vec![0f32; w * 3];
                let mut q = vec![0f32; w * 3];
                for (i, fr) in fc.chunks(fs).enumerate() {
                    let (m, k) = frame(fr, fw * 3, tt, tn, h, w, y0, x0, &mut p, &mut q);
                    mc[i] = m;
                    kc[i] = k;
                }
            });
        }
    });
    0
}
