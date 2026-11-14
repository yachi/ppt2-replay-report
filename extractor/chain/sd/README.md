# chain/sd: syakegohan's practice stream of 2026-08-16 (「練習【ぷよぷよテトリス２】」)

111 games, ids `v000`–`v110`, dataset `stream-2026-08-16`, video `UKNJ3gWqqkU`. This is the second stream of that
day; `chain/sc` is the first (`n0Kbttgv3sQ`), and both share the dataset. This tree is a copy of `chain/qh`, run on
one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/sd/`, a cloud session's scratchpad).
It adds no frame image or video to the repo.

## Inputs

syakegohan is the LEFT board (p1) throughout. Sets are first to 3, against whoever joined the room; opponent names are
read off a 480p nameplate as they appear there.

| ids | set | opponent | score |
|---|---|---|---|
| v000–v002 | 1 | カワウソ | 3-0 |
| v003–v005 | 2 | カワウソ | 3-0 |
| v006–v008 | 3 | (blank nameplate) | 3-0 |
| v009–v011 | 4 | (blank nameplate) | 3-0 |
| v012–v014 | 5 | ちぃちゃちゃもん | 3-0 |
| v015–v017 | 6 | ちぃちゃちゃもん | 3-0 |
| v018–v020 | 7 | くくすす | 3-0 |
| v021–v024 | 8 | くくすす | 3-1 |
| v025–v027 | 9 | Fumi´∀` | 3-0 |
| v028–v030 | 10 | Fumi´∀` | 3-0 |
| v031–v033 | 11 | アベル | 3-0 |
| v034–v036 | 12 | アベル | 3-0 |
| v037–v039 | 13 | カワウソ | 3-0 |
| v040–v042 | 14 | カワウソ | 3-0 |
| v043–v045 | 15 | ににな | 3-0 |
| v046–v048 | 16 | ににな | 3-0 |
| v049–v051 | 17 | KinoKo | 3-0 |
| v052–v054 | 18 | KinoKo | 3-0 |
| v055–v057 | 19 | 」 | 3-0 |
| v058–v060 | 20 | 」 | 3-0 |
| v061–v063 | 21 | リュウ2サンズ | 3-0 |
| v064–v066 | 22 | リュウ2サンズ | 3-0 |
| v067–v069 | 23 | あおりーん！_！ | 3-0 |
| v070–v072 | 24 | あおりーん！_！ | 3-0 |
| v073–v075 | 25 | Uniあお | 3-0 |
| v076–v078 | 26 | Uniあお | 3-0 |
| v079–v081 | 27 | あちみつ | 3-0 |
| v082–v086 | 28 | あちみつ | 2-3 |
| v087–v091 | 29 | あちみつ | 2-3 |
| v092–v094 | 30 | コルティ | 3-0 |
| v095–v097 | 31 | コルティ | 3-0 |
| v098–v100 | 32 | ヤ | 3-0 |
| v101–v103 | 33 | ヤ | 3-0 |
| v104–v104 | 34 | カワウソ | 1-0 |
| v105–v107 | 35 | コルティ | 3-0 |
| v108–v110 | 36 | コルティ | 3-0 |

syakegohan 104-7 over the 111 games. Set 34 (v104, カワウソ) is one game: the stream leaves the room at 1-0.

- The video: native 854x480 h264, the layout qh's coordinates expect. **No rescale.**
- Games: `seg/` as in qh (144 segments). `mkgames_sd.py` writes `games.json` and `games_all.json` from the WIN
  counters read by eye off the contact sheets, and asserts each set ends on its final score. Left out: five sets
  where the opponent plays puyo (segments 18-24, 38-43, 80-85, 98-103, 117-124), so not tetris vs tetris. When a
  set is won without leaving the room the counter resets to 0-0 on the deciding game's end frame; from 2-0 only
  syakegohan can reach 3, so those deciders are his.
- **Blank nameplate.** Sets 3 and 4 (v006–v011) show '-----' as the opponent's name, so `opponent` is empty and
  the page shows 對手未知. `pool/pool.py` asserts every included game has an opponent name; it now exempts these
  six games by id (`BLANK_NAME`, read from `games.json`).

## What differs from chain/qh

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/sd/`, video `UKNJ3gWqqkU` |
| `mkgames_sd.py` | this stream's games (above) |
| `pool/pool.py` | the blank-nameplate exemption (above) |
| banner, word and score-digit templates, `w/ocr/T.npy` | copied from `chain/qh` (same channel, same native layout). Not committed |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 75 s, a frame of v000 with both NEXT columns at rest |
| `corr/nc_compare.py` | reads this set's chain table and hand edits instead of the analysis games.csv |

As for qh, `pool/pool.py` needs `pool/out/` to exist, `w/tetrio/metrics.py` needs scipy and `witnessed.json`
(`[]` here), and `corr/tools/score.py` needs `check/ocr/reader.py` beside `w/ocr/T.npy`.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 189 flags (`corr/flags.json`): 119 PERFECT CLEAR banner onsets,
   40 winner KO pieces, 17 KO-tail score jumps, 5 banners with no clear, 4 T-spins with no banner,
   3 banner/type disagreements and 1 bad bag. The WIN counter agrees with the csv in 111 of 111 games.
2. **PERFECT CLEARs.** 74 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`). The others make
   16 clusters (`corr/pcclusters.json`). A lit-cell count of the board after each (`corr/litcount.txt`) never fell
   to 40 or less after a rejected one, so there are no hidden PCs and `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 24 spots (`corr/score/spots.json`).
4. **Frame checks.** 73 items in four groups (`corr/groups/g0.json`–`g3.json`). `extractor/autosettle` settled
   12 as no change (the score did not move between the last spawn and the KO), marked 1 for audit and gave 4 hints
   (`corr/out/auto.json`). One agent per group proposed corrections (`corr/out/b*.json`), and one more per group tried
   to refute each (`corr/out/v*.json`). The skeptics rejected 3 proposals: v026's added S and its piece count
   (it locks one frame after the end) and v075's piece count (the T was still soft-dropping). They kept the rest.
5. **Merge.** `corr/merge_xo.py` wrote 10 event corrections (4 retypes, 3 added events, 3 rebuilt windows) and
   10 cell edits. `corr/fixwas.py` ran `w/tetrio/metrics.py` and needed no repair.
6. **Cells.** Of the 10 cell edits, the corrected event list already gives 1 (v043 p2's max B2B), so 9 are hand
   edits, all piece counts (`corr/hand_edits.csv`). Eight add one piece the chain had missed;
   v087 p1 drops from 294 to 292, where the chain had logged two locks twice.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the final table (`corr/nc_compare.json`). Of the 222 player-games, 167 agree
exactly, 29 differ by one piece and 23 are lost reads. Three clean reads differ by more (v009 p1, v071 p1, v101 p1),
and they went to a fifth check (`corr/groups/g4.json`, `corr/out/b4.json`). In each the recount is wrong and the
table stands. nextcount went blind for a short stretch and missed spawns, or started reading after the first lock,
or logged the last two spawns as one late shift after the KO; nc_compare then dropped a last spawn the chain had
already counted. The frames and score steps show every lock the table counts. v071 p1's hand edit (53 → 54) is
confirmed this way. No piece count was changed from the recount.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the streams).
