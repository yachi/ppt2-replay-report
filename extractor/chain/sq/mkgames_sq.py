# [sq] games.json for syakegohan vs あてん, 深夜の対戦で (one upload of 2025-08-17, native 854x480 replay Ver 3.5, no
# rescale): one game of a set whose earlier games were not uploaded (WIN counter 2-0 at the start, 3-0 after), id ab00
# (two letters and two digits, see chain/sp). seg found no game in this video (a single 9.5-minute game), so the game
# is written by hand: ゴー！ shows at 2.0 s, the in-game clock reads 00:00.13 at 2.4 s and the first pieces drop
# then; start_s = 1.8, end_upper_s = the video's end less 0.2 s. (A first run used start_s = 5.3, read off a misread
# clock, and lost each player's first pieces; the NEXT recount's bag offset showed it.)
# syakegohan is the LEFT board (p1).
import json, subprocess
K = '/tmp/claude-0/sq/'; V = 'JCJkunwkkxw'; p = K + f'video/{V}.mp4'
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
out = [dict(id='ab00', video=V, path=p, start_s=1.8, end_upper_s=round(dur - 0.2, 1), dataset='upload-2025-08-17',
            opener='', opponent='あてん', win_counter_at_start='2-0', counter_winner=1, win_counter_after='3-0')]
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
print(out)
