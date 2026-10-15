# syakegohan vs opponents: pooled metrics, old + new games

Games: 210 found (108 old, 102 new). Included: **191** (98 old, 93 new). Excluded: 19 (listed below).

Every figure is a ratio of sums over included games: e.g. PPS = sum(pieces)/sum(seconds), APM = 60*sum(attack)/sum(s), VS = 100*sum(attack+garbage_cleared)/sum(s), APP = sum(attack)/sum(pieces), DS = garbage_cleared. T-spins = TSS+TSD+TST (Minis not counted). Clears for the % columns = single+double+triple+quad+TSS+TSD+TST+Mini (untyped gap lines are not clears). max REN is the max of `max_combo`. recv/min = garbage rows received per minute. mean s = sum(seconds)/games.

Files: `all_rows.csv` (old + new rows, `opponent` and `source` columns), `pooled.csv`, `pool.py`.

## Pooled table

| scope | player | G | W | PPS | APM | VS | APP | DS/pc | DS/s | LPM | Q/min | TS/min | TSD/min | Q %clr | TS %clr | PC | maxREN | maxB2B | recv/min | mean s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | syakegohan | 191 | 126 | 1.954 | 92.01 | 186.91 | 0.785 | 0.172 | 0.336 | 63.16 | 6.37 | 8.96 | 6.31 | 22.58 | 31.77 | 51 | 13 | 38 | 29.55 | 63.8 |
| all | all opponents | 191 | 65 | 1.863 | 86.75 | 179.33 | 0.776 | 0.187 | 0.347 | 61.06 | 5.81 | 8.32 | 5.71 | 20.89 | 29.90 | 37 | 15 | 31 | 33.89 | 63.8 |
| vs あちみつ | syakegohan | 60 | 35 | 1.986 | 92.87 | 190.96 | 0.779 | 0.182 | 0.362 | 64.90 | 6.24 | 8.98 | 6.41 | 21.12 | 30.41 | 14 | 11 | 14 | 32.59 | 58.7 |
| vs あちみつ | あちみつ | 60 | 25 | 1.998 | 91.64 | 186.42 | 0.765 | 0.169 | 0.337 | 63.21 | 6.27 | 8.95 | 5.93 | 21.98 | 31.36 | 18 | 12 | 17 | 33.05 | 58.7 |
| vs 3000↑ぼ | syakegohan | 44 | 25 | 1.957 | 92.04 | 188.21 | 0.784 | 0.178 | 0.348 | 64.17 | 6.65 | 9.11 | 6.48 | 23.63 | 32.36 | 12 | 12 | 38 | 31.20 | 71.5 |
| vs 3000↑ぼ | 3000↑ぼ | 44 | 19 | 1.878 | 90.94 | 186.58 | 0.807 | 0.187 | 0.350 | 62.11 | 6.04 | 9.38 | 6.83 | 22.12 | 34.33 | 10 | 15 | 20 | 32.28 | 71.5 |
| vs kazu | syakegohan | 23 | 15 | 1.912 | 88.09 | 180.12 | 0.768 | 0.174 | 0.333 | 61.69 | 5.52 | 8.83 | 5.97 | 19.50 | 31.21 | 3 | 10 | 14 | 30.82 | 52.0 |
| vs kazu | kazu | 23 | 8 | 1.883 | 84.68 | 172.01 | 0.749 | 0.164 | 0.309 | 58.18 | 5.97 | 9.09 | 5.42 | 23.56 | 35.84 | 1 | 12 | 21 | 33.63 | 52.0 |
| vs あめみや　はいしん | syakegohan | 21 | 18 | 1.837 | 85.88 | 170.06 | 0.779 | 0.147 | 0.269 | 56.03 | 5.20 | 7.56 | 4.82 | 19.83 | 28.81 | 9 | 13 | 11 | 22.78 | 52.2 |
| vs あめみや　はいしん | あめみや　はいしん | 21 | 3 | 1.576 | 69.78 | 147.24 | 0.738 | 0.196 | 0.309 | 52.36 | 3.07 | 5.31 | 3.61 | 11.07 | 19.17 | 0 | 15 | 7 | 37.63 | 52.2 |
| vs しょうがく6ねんせい | syakegohan | 20 | 17 | 1.964 | 94.91 | 190.99 | 0.805 | 0.167 | 0.328 | 63.54 | 6.95 | 9.30 | 6.47 | 25.16 | 33.67 | 5 | 10 | 26 | 25.01 | 86.7 |
| vs しょうがく6ねんせい | しょうがく6ねんせい | 20 | 3 | 1.783 | 83.33 | 178.13 | 0.779 | 0.220 | 0.393 | 62.50 | 6.64 | 6.99 | 4.60 | 23.73 | 24.97 | 5 | 12 | 12 | 35.11 | 86.7 |
| vs uyeshota | syakegohan | 12 | 8 | 1.991 | 96.16 | 192.85 | 0.805 | 0.164 | 0.326 | 65.16 | 7.20 | 9.52 | 7.08 | 25.51 | 33.71 | 4 | 9 | 18 | 30.42 | 77.7 |
| vs uyeshota | uyeshota | 12 | 4 | 1.834 | 88.83 | 188.57 | 0.807 | 0.221 | 0.405 | 64.06 | 5.66 | 7.85 | 6.11 | 18.41 | 25.52 | 2 | 10 | 31 | 34.28 | 77.7 |
| vs Remakun | syakegohan | 9 | 6 | 1.981 | 90.90 | 177.61 | 0.765 | 0.132 | 0.261 | 58.14 | 6.22 | 9.19 | 6.86 | 24.37 | 36.04 | 4 | 9 | 15 | 23.82 | 51.5 |
| vs Remakun | Remakun | 9 | 3 | 1.737 | 78.86 | 163.80 | 0.757 | 0.186 | 0.324 | 55.42 | 4.66 | 8.42 | 6.09 | 18.00 | 32.50 | 0 | 7 | 8 | 36.13 | 51.5 |
| vs いんたい | syakegohan | 2 | 2 | 1.928 | 90.35 | 185.95 | 0.781 | 0.183 | 0.354 | 63.66 | 8.21 | 8.21 | 4.79 | 31.58 | 31.58 | 0 | 6 | 6 | 26.01 | 43.8 |
| vs いんたい | いんたい | 2 | 0 | 1.745 | 67.76 | 142.60 | 0.647 | 0.170 | 0.297 | 54.76 | 2.74 | 3.42 | 2.05 | 9.30 | 11.63 | 1 | 9 | 1 | 42.44 | 43.8 |

## syakegohan's record per opponent

| opponent | games | syakegohan W-L | win % | syake PPS / APM / VS | opp PPS / APM / VS | APP syake / opp |
|---|---|---|---|---|---|---|
| all opponents | 191 | 126-65 | 66% | 1.954 / 92.01 / 186.91 | 1.863 / 86.75 / 179.33 | 0.785 / 0.776 |
| あちみつ | 60 | 35-25 | 58% | 1.986 / 92.87 / 190.96 | 1.998 / 91.64 / 186.42 | 0.779 / 0.765 |
| 3000↑ぼ | 44 | 25-19 | 57% | 1.957 / 92.04 / 188.21 | 1.878 / 90.94 / 186.58 | 0.784 / 0.807 |
| kazu | 23 | 15-8 | 65% | 1.912 / 88.09 / 180.12 | 1.883 / 84.68 / 172.01 | 0.768 / 0.749 |
| あめみや　はいしん | 21 | 18-3 | 86% | 1.837 / 85.88 / 170.06 | 1.576 / 69.78 / 147.24 | 0.779 / 0.738 |
| しょうがく6ねんせい | 20 | 17-3 | 85% | 1.964 / 94.91 / 190.99 | 1.783 / 83.33 / 178.13 | 0.805 / 0.779 |
| uyeshota | 12 | 8-4 | 67% | 1.991 / 96.16 / 192.85 | 1.834 / 88.83 / 188.57 | 0.805 / 0.807 |
| Remakun | 9 | 6-3 | 67% | 1.981 / 90.90 / 177.61 | 1.737 / 78.86 / 163.80 | 0.765 / 0.757 |
| いんたい | 2 | 2-0 | 100% | 1.928 / 90.35 / 185.95 | 1.745 / 67.76 / 142.60 | 0.781 / 0.647 |

## Sample size: opponents with >= 10 included games

| opponent | included games | >= 10? |
|---|---|---|
| あちみつ | 60 | yes |
| 3000↑ぼ | 44 | yes |
| kazu | 23 | yes |
| あめみや　はいしん | 21 | yes |
| しょうがく6ねんせい | 20 | yes |
| uyeshota | 12 | yes |
| Remakun | 9 | **no** |
| いんたい | 2 | **no** |

6 of 8 opponent names reach 10: あちみつ, 3000↑ぼ, kazu, あめみや　はいしん, しょうがく6ねんせい, uyeshota. Below 10: Remakun (9), いんたい (2). Remakun needs at least 1 more included game (2 of its 11 found games, i002 and i004, are excluded as unresolved lower bounds; resolving either bound is the cheapest route to 10). いんたい has only 2 games and should be read as anecdote, or as part of あめみや　はいしん if that link is confirmed.

## Name variants that may be the same person (NOT merged)

- **しょうがく5ねんせい / しょうがく6ねんせい**: only しょうがく6ねんせい occurs in the included rows (20 games: old + new). The string しょうがく5ねんせい appears nowhere under /private/tmp/claude-501/sk/ (grep of every text file), so nothing to merge here; if a 5ねんせい nameplate turns up in other videos it is probably the same player one school year earlier (unverified).
- **あめみや variants**: `あめみや　はいしん` (full-width space) is the only spelling in the rows (21 games; 3 old + new). Old and new spell it identically (same code points), so pooling them under one name is a string match, not a merge. A grep of every text file under /private/tmp/claude-501/sk/ finds no other あめみや player spelling; the only other hit is the opener name あめみや砲 on the shiwehi page dumps, which is not a player.
- **いんたい** (2 games, i018-i019) appears between two runs of あめみや　はいしん games in the same video (i011-i017, i020-i034). It may be the same account under a temporary name ("引退" = retired); the checker read the nameplate as いんたい in both games. Kept separate.

## Exclusions (every one listed)

| game | player | opponent | source | reason |
|---|---|---|---|---|
| g062 | p1 | (name not read) | old | unresolved lower bound |
| g062 | p2 | (name not read) | old | game excluded (other player) |
| g071 | p1 | (name not read) | old | game excluded (other player) |
| g071 | p2 | (name not read) | old | unresolved lower bound |
| g074 | p1 | (name not read) | old | unresolved lower bound |
| g074 | p2 | (name not read) | old | game excluded (other player) |
| g086 | p1 | (name not read) | old | not-trustworthy verdict game |
| g086 | p2 | (name not read) | old | unresolved lower bound not-trustworthy verdict game |
| g088 | p1 | (name not read) | old | unresolved lower bound |
| g088 | p2 | (name not read) | old | game excluded (other player) |
| g090 | p1 | (name not read) | old | not-trustworthy verdict game |
| g090 | p2 | (name not read) | old | not-trustworthy verdict game |
| g092 | p1 | (name not read) | old | game excluded (other player) |
| g092 | p2 | (name not read) | old | unresolved lower bound |
| g094 | p1 | (name not read) | old | unresolved lower bound |
| g094 | p2 | (name not read) | old | game excluded (other player) |
| g096 | p1 | (name not read) | old | unresolved lower bound |
| g096 | p2 | (name not read) | old | game excluded (other player) |
| g101 | p1 | (name not read) | old | not-trustworthy verdict game |
| g101 | p2 | (name not read) | old | not-trustworthy verdict game |
| h031 | p1 | しょうがく6ねんせい | new | game excluded (other player) |
| h031 | p2 | しょうがく6ねんせい | new | unresolved lower bound |
| i002 | p1 | Remakun | new | unresolved lower bound |
| i002 | p2 | Remakun | new | game excluded (other player) |
| i004 | p1 | Remakun | new | unresolved lower bound |
| i004 | p2 | Remakun | new | game excluded (other player) |
| i014 | p1 | あめみや　はいしん | new | game excluded (other player) |
| i014 | p2 | あめみや　はいしん | new | unresolved lower bound |
| i031 | p1 | あめみや　はいしん | new | unresolved lower bound |
| i031 | p2 | あめみや　はいしん | new | unresolved lower bound |
| i032 | p1 | あめみや　はいしん | new | unresolved lower bound |
| i032 | p2 | あめみや　はいしん | new | game excluded (other player) |
| i033 | p1 | あめみや　はいしん | new | checker: p1 quad count 25 in rows, 26 in video (game-ending Tetris at ~3784.0 s dropped; recorded end falls before the final clear) |
| i033 | p2 | あめみや　はいしん | new | checker: p1 quad count 25 in rows, 26 in video (game-ending Tetris at ~3784.0 s dropped; recorded end falls before the final clear) |
| j008 | p1 | 3000↑ぼ | new | checker: p1 T-spin Triple 3 in rows, 4 in video (game-ending TST at ~1857.85 s dropped; recorded end falls before the final clear) |
| j008 | p2 | 3000↑ぼ | new | checker: p1 T-spin Triple 3 in rows, 4 in video (game-ending TST at ~1857.85 s dropped; recorded end falls before the final clear) |
| j009 | p1 | 3000↑ぼ | new | unresolved lower bound |
| j009 | p2 | 3000↑ぼ | new | game excluded (other player) |

Whole games are excluded when either player's row is excluded, so no game contributes one side only. The 10 old excluded games have no opponent name recorded (opponents.json does not cover them). i033 and j008 were excluded on the checker's findings rather than patched by hand, as instructed.

**Caveat from the checker**: in both i033 and j008 the recorded game end falls just before the final, winning clear, so that clear was dropped. Only 6 of 102 new games were checked; other games may also miss their last clear. Effect, if it is common: a downward bias in the winner's (usually syakegohan's) attack, lines and clear counts. Its size is unmeasured: 2 of the 6 checked games lost exactly one clear each.

No opponent-name corrections were needed: the checker read all 102 new nameplates and found no disagreement.

## Self-check: old-only subset reproduces the original figures

| figure | expected | old-only subset | result |
|---|---|---|---|
| syakegohan PPS | 1.956 | 1.95449 | FAIL |
| syakegohan APM | 91.26 | 92.1677 | FAIL |
| opponents PPS | 1.909 | 1.91135 | FAIL |
| opponents APM | 89.05 | 89.4538 | FAIL |

Overall: **FAIL** (old-only subset = 98 games).
