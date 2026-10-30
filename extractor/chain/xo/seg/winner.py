import sys, json, subprocess, numpy as np
def frame(path,t):
    b=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.2f}','-i',path,'-frames:v','1','-vf','scale=640:360','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    return np.frombuffer(b,np.uint8).reshape(360,640,3).astype(float)
path, seg = sys.argv[1], sys.argv[2]
g=[q for q in json.load(open(seg)) if max(q['bright'])<100 and q['end']-q['start']>5]
crops=[]
for q in g:
    a=frame(path,q['start']+3.0)
    crops.append((a[324:341,268:292].mean(2), a[324:341,348:372].mean(2)))
a=frame(path,g[-1]['end']-1.0); crops.append((a[324:341,268:292].mean(2), a[324:341,348:372].mean(2)))
for i,q in enumerate(g):
    dL=np.abs(crops[i+1][0]-crops[i][0]).mean(); dR=np.abs(crops[i+1][1]-crops[i][1]).mean()
    q['dL'],q['dR']=round(dL,1),round(dR,1)
    print(q['start'], round(q['end']-q['start'],1), q['dL'], q['dR'])
json.dump(g, open(seg.replace('.json','_games.json'),'w'))
