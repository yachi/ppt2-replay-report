# amemiya vs opponents: pooled metrics (4xcAmo-s-Tg)

Games: 118 found (0 old, 118 new). Included: **118** (0 old, 118 new). Excluded: 0 (listed below).

Every figure is a ratio of sums over included games: e.g. PPS = sum(pieces)/sum(seconds), APM = 60*sum(attack)/sum(s), VS = 100*sum(attack+garbage_cleared)/sum(s), APP = sum(attack)/sum(pieces), DS = garbage_cleared. T-spins = TSS+TSD+TST (Minis not counted). Clears for the % columns = single+double+triple+quad+TSS+TSD+TST+Mini (untyped gap lines are not clears). max REN is the max of `max_combo`. recv/min = garbage rows received per minute. mean s = sum(seconds)/games.

Files: `all_rows.csv` (old + new rows, `opponent` and `source` columns), `pooled.csv`, `pool.py`.

## Pooled table

| scope | player | G | W | PPS | APM | VS | APP | DS/pc | DS/s | LPM | Q/min | TS/min | TSD/min | Q %clr | TS %clr | PC | maxREN | maxB2B | recv/min | mean s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all | amemiya | 118 | 75 | 1.597 | 82.47 | 165.06 | 0.860 | 0.173 | 0.276 | 50.94 | 3.20 | 5.37 | 3.30 | 11.00 | 18.43 | 0 | 20 | 8 | 28.73 | 53.8 |
| all | all opponents | 118 | 43 | 1.708 | 79.73 | 157.87 | 0.778 | 0.146 | 0.250 | 51.61 | 4.02 | 6.90 | 4.58 | 15.24 | 26.11 | 22 | 21 | 16 | 30.24 | 53.8 |
| vs kazu | amemiya | 50 | 30 | 1.684 | 85.95 | 177.49 | 0.851 | 0.203 | 0.342 | 56.89 | 3.90 | 5.91 | 3.61 | 12.55 | 19.04 | 0 | 17 | 7 | 33.45 | 54.2 |
| vs kazu | kazu | 50 | 20 | 1.881 | 88.67 | 173.28 | 0.785 | 0.135 | 0.255 | 55.96 | 5.49 | 9.56 | 6.91 | 22.14 | 38.57 | 13 | 15 | 16 | 29.66 | 54.2 |
| vs どらえもん | amemiya | 28 | 15 | 1.439 | 73.27 | 147.09 | 0.849 | 0.174 | 0.250 | 45.38 | 2.75 | 5.03 | 3.18 | 10.54 | 19.28 | 0 | 20 | 8 | 27.54 | 59.2 |
| vs どらえもん | どらえもん | 28 | 13 | 1.540 | 74.18 | 148.11 | 0.803 | 0.159 | 0.245 | 47.29 | 3.08 | 5.10 | 2.75 | 11.50 | 19.08 | 6 | 21 | 8 | 27.64 | 59.2 |
| vs あ | amemiya | 22 | 15 | 1.505 | 80.83 | 151.03 | 0.895 | 0.108 | 0.163 | 41.88 | 1.58 | 3.81 | 1.99 | 5.54 | 13.35 | 0 | 19 | 6 | 23.72 | 46.6 |
| vs あ | あ | 22 | 7 | 1.565 | 76.15 | 140.68 | 0.811 | 0.088 | 0.138 | 41.71 | 1.82 | 3.75 | 2.11 | 6.40 | 13.22 | 0 | 21 | 7 | 26.83 | 46.6 |
| vs さむい | amemiya | 18 | 15 | 1.726 | 90.27 | 176.02 | 0.872 | 0.148 | 0.256 | 53.43 | 3.76 | 6.08 | 4.01 | 12.71 | 20.55 | 0 | 16 | 7 | 22.80 | 53.2 |
| vs さむい | さむい | 18 | 3 | 1.661 | 67.84 | 149.50 | 0.681 | 0.219 | 0.364 | 57.38 | 3.88 | 5.83 | 3.82 | 13.69 | 20.53 | 3 | 10 | 6 | 40.03 | 53.2 |

## amemiya's record per opponent

| opponent | games | amemiya W-L | win % | amemiya PPS / APM / VS | opp PPS / APM / VS | APP amemiya / opp |
|---|---|---|---|---|---|---|
| all opponents | 118 | 75-43 | 64% | 1.597 / 82.47 / 165.06 | 1.708 / 79.73 / 157.87 | 0.860 / 0.778 |
| kazu | 50 | 30-20 | 60% | 1.684 / 85.95 / 177.49 | 1.881 / 88.67 / 173.28 | 0.851 / 0.785 |
| どらえもん | 28 | 15-13 | 54% | 1.439 / 73.27 / 147.09 | 1.540 / 74.18 / 148.11 | 0.849 / 0.803 |
| あ | 22 | 15-7 | 68% | 1.505 / 80.83 / 151.03 | 1.565 / 76.15 / 140.68 | 0.895 / 0.811 |
| さむい | 18 | 15-3 | 83% | 1.726 / 90.27 / 176.02 | 1.661 / 67.84 / 149.50 | 0.872 / 0.681 |

## Exclusions (every one listed)

| game | player | opponent | source | reason |
|---|---|---|---|---|

Whole games are excluded when either player's row is excluded, so no game contributes one side only.

