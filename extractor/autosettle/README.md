# autosettle — settle frame-check items the score OCR already decides

Most frame-check time goes to agents re-reading items whose answer is "no change". `autosettle.py` runs after a
chain's grouping step (`corr/groups/g*.json`) and before the checkers. It reads the chain's per-game score OCR
(`SET/w/ocrall/GID.json`, written by `ocr_all.sh`), takes settled items out of the groups and records them in an
`auto.json` beside the checkers' `b*.json`.

```bash
python3 extractor/autosettle/autosettle.py /tmp/claude-0/<set>/w/ocrall corr/groups corr/out/auto.json
```

`merge_xo.py` reads only event corrections and cell edits, so a settled item changes no output. It only skips
the frame check. No archived chain was re-run; this is for the next runs.

## Rules

| rule | item | what it does |
|---|---|---|
| `ko-flat-v1` | winner KO piece not counted | **settles as no change** when the player's stable score at the last spawn equals the last stable score after KO + 0.2 s. A piece that locked on the KO frame scores at least its drop points. A rise is left to the checker. |
| `tsb-hint-v1` | T-spin without a banner | **settles nothing**. The one score jump near the clear is matched against the T-spin and plain values (level 3, B2B ×1.5, REN 0–30, drop 0–80) and the verdict is appended to the item's detail as evidence. |

Every tenth settled item (by a stable hash of id, player and time) stays in its group with the evidence appended,
as an audit sample. A disagreement there means the rule is wrong: stop using it and look.

## Backtest (2026-11-14)

The committed groups of two chains with checker labels, `xo` (uyeshota 2026-10-30) and `te` (uyeshota 10ell5aAJuo),
with score OCR re-read from the videos (480p download, its own digit templates, not the chain's rescaled reader):

| chain | items | settled by `ko-flat-v1` | audit sample | settled items the checkers changed | `tsb-hint-v1` verdicts (label) |
|---|---|---|---|---|---|
| te | 76 | 23 | 1 | 0 | plain 2 (no change 2), undecided 2 |
| xo | 176 | 22 | 3 | 0 | plain 5 (no change 5), T-spin 3 (change 3), undecided 3 |

So 49 of the 252 items (19%) would have gone to `ko-flat-v1`, and every one of them the checkers had marked
"no change". `tsb-hint-v1`'s 10 decided verdicts all match the checkers' outcome; that is why it is only a hint.

Labels come from `corr/out/b*.json`: an item is "change" when a correction or cell edit carries its `n`.
Two streams of one player is a small sample; the audit sample is what keeps the rule honest on the next runs.

## Rules tried and not shipped (2026-11-14)

The 2773 labelled frame-check items of 28 chains (`corr/groups` against `corr/out/b*.json`) were searched for a
rule that the item's own detail text decides, without score OCR. None settles with zero false "no change":

| item | feature tried | no change | change | why not |
|---|---|---|---|---|
| NEXT-queue recount differs from pieces | shifts equal the table's pieces and at least one unmatched event | 20 | 1 | one change on the same features (0 shifts off, 2 and 2 unmatched) |
| KO-tail score jump | the jump's size (300, 1200 …) and its time from KO | 74 | 77 | sizes 71–76 and 300 occur on both sides |
| winner KO piece not counted | anything but the score | 736 | 106 | only the score after KO separates them, which is `ko-flat-v1` |

The other categories (gap windows, score_spot, banner/type) are mostly "change" and are not candidates. A further
rule needs score OCR on more chains than `te` and `xo`, which means downloading their videos; it should be developed
on some chains and checked on held-out ones the way `ko-flat-v1` was.
