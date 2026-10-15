import sys,subprocess
from PIL import Image
# timer.py VIDEO t1 t2 ... -> stacks crops of timer + both boards' top-half small
v=sys.argv[1]; ts=[float(x) for x in sys.argv[3:]]; out=sys.argv[2]
ims=[]
for t in ts:
  subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(t),'-i',f'/private/tmp/claude-501/sk/vid/{v}.mp4','-frames:v','1','/private/tmp/claude-501/sk/metrics/R/fr/_t.png'])
  im=Image.open('/private/tmp/claude-501/sk/metrics/R/fr/_t.png').convert('RGB')
  row=Image.new('RGB',(854,60)); row.paste(im.crop((0,420,854,480)),(0,0))
  from PIL import ImageDraw; ImageDraw.Draw(row).text((5,5),'%.2f'%t,fill=(255,0,0))
  ims.append(row)
S=Image.new('RGB',(854,60*len(ims)))
for i,r in enumerate(ims): S.paste(r,(0,60*i))
S.save(out)
