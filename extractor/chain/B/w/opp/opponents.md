# Opponent metrics (pooled, ratio of sums, non-excluded games)

sk = syakegohan (p1). Rates are sums over the opponent's games: PPS = pieces/s, APM = 60·attack/s, VS = 100·(attack+garbage_cleared)/s, APP = attack/pieces, DS/piece = garbage_cleared/pieces, LPM = 60·lines/s.
Opponents with fewer than 3 games are flagged "small n, do not compare". Every stream name was read by two independent readers, all at high confidence, so no name is flagged low-confidence.

| opponent | source | games | opp wins | opp PPS | opp APM | opp VS | opp APP | opp DS/piece | opp LPM | sk PPS | sk APM | sk VS | sk APP | sk DS/piece | sk LPM | flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| あちみつ | upload-2026-08-20, upload-2026-09-13 | 39 | 18 | 2.005 | 93.15 | 191.22 | 0.774 | 0.179 | 64.99 | 1.976 | 93.59 | 192.90 | 0.789 | 0.187 | 65.58 |  |
| kazu | stream-2026-10-12 | 23 | 8 | 1.883 | 84.68 | 172.01 | 0.749 | 0.164 | 58.18 | 1.912 | 88.09 | 180.12 | 0.768 | 0.174 | 61.69 |  |
| uyeshota | upload-2026-07-14 | 12 | 4 | 1.834 | 88.83 | 188.57 | 0.807 | 0.221 | 64.06 | 1.991 | 96.16 | 192.85 | 0.805 | 0.164 | 65.16 |  |
| 3000↑ぼ | stream-2026-10-12 | 12 | 7 | 1.877 | 93.48 | 191.09 | 0.830 | 0.188 | 62.88 | 1.918 | 88.45 | 186.10 | 0.768 | 0.202 | 65.23 |  |
| しょうがく6ねんせい | stream-2026-10-12 | 9 | 1 | 1.800 | 80.87 | 167.07 | 0.749 | 0.179 | 59.01 | 1.931 | 94.48 | 189.59 | 0.816 | 0.166 | 62.29 |  |
| あめみや　はいしん | stream-2026-10-12 | 3 | 1 | 1.690 | 77.16 | 162.40 | 0.761 | 0.200 | 54.07 | 2.075 | 90.12 | 168.03 | 0.724 | 0.086 | 58.58 |  |
| **stream (all)** | stream-2026-10-12 | 47 | 17 | 1.856 | 86.50 | 176.91 | 0.777 | 0.176 | 59.75 | 1.924 | 89.64 | 183.65 | 0.777 | 0.178 | 62.87 |  |
| **all opponents** | stream-2026-10-12, upload-2026-07-14, upload-2026-08-20, upload-2026-09-13 | 98 | 39 | 1.911 | 89.45 | 184.26 | 0.780 | 0.184 | 62.45 | 1.954 | 92.17 | 188.66 | 0.786 | 0.179 | 64.27 |  |

Distinct stream opponents: 4

## Checks

- per-opponent games sum = 98 (expect 98): PASS
- all-opponents PPS = 1.911348 -> 1.911 (expect 1.909): FAIL
- all-opponents APM = 89.453783 -> 89.45 (expect 89.05): FAIL
- all-opponents VS = 184.261401 -> 184.26 (expect 183.54): FAIL
- all-opponents APP = 0.780024 -> 0.78 (expect 0.778): FAIL
