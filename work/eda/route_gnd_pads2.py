import json, math, heapq
import numpy as np
G=json.load(open('work/eda/geom_now.json'))
tracks,vias,pads=G['tracks'],G['vias'],G['pads']
jobs=[('U37','2',-5280,1516),('U37','3',-5280,1516),('U37','5',-5280,1516),
      ('U4','2',591,2008),('C80','2',1606,1911),('C81','2',1606,1911),
      ('U33','10',-4290,3073),('U33','17',-4331,2281)]
STEP=5.0; OUR=4.0; CLR=5.1
out={}
for comp,num,tx,ty in jobs:
    ps=[p for p in pads if p['comp']==comp and p['num']==num]
    if not ps: print('no pad',comp,num); continue
    p=ps[0]; sx,sy=p['x'],p['y']
    X0,X1=min(sx,tx)-250,max(sx,tx)+250; Y0,Y1=min(sy,ty)-250,max(sy,ty)+250
    NX=int((X1-X0)/STEP)+1; NY=int((Y1-Y0)/STEP)+1
    grid=np.zeros((NY,NX),dtype=bool)
    def cell(x,y): return int(round((x-X0)/STEP)),int(round((y-Y0)/STEP))
    def mark_disk(cx,cy,r):
        ix,iy=cell(cx,cy); rr=int(r/STEP)+1
        x0,x1=max(0,ix-rr),min(NX,ix+rr+1); y0,y1=max(0,iy-rr),min(NY,iy+rr+1)
        if x0>=x1 or y0>=y1: return
        xs=X0+np.arange(x0,x1)*STEP; ys=Y0+np.arange(y0,y1)*STEP
        mx,my=np.meshgrid(xs,ys); grid[y0:y1,x0:x1] |= (mx-cx)**2+(my-cy)**2 <= r*r
    def mark_seg(x1,y1,x2,y2,r):
        L=math.hypot(x2-x1,y2-y1); n=max(2,int(L/2))
        for i in range(n+1):
            t=i/n; mark_disk(x1+(x2-x1)*t,y1+(y2-y1)*t,r)
    for t in tracks:
        if t['net']=='GND' or t['layer']!=1: continue
        mark_seg(t['x1'],t['y1'],t['x2'],t['y2'],(t.get('w') or 8)/2+CLR+OUR)
    for v in vias:
        if v['net']=='GND': continue
        mark_disk(v['x'],v['y'],(v.get('d') or 24)/2+CLR+OUR)
    for q in pads:
        if q['net']=='GND': continue
        mark_disk(q['x'],q['y'],10+CLR+OUR)
    sc=cell(sx,sy); gc=cell(tx,ty)
    def free(x,y): return 0<=x<NX and 0<=y<NY and not grid[y,x]
    if not free(*sc): print('start blocked',comp,num); continue
    gcf=None
    for rr in range(0,30):
        for dx in range(-rr,rr+1):
            for dy in range(-rr,rr+1):
                if free(gc[0]+dx,gc[1]+dy): gcf=(gc[0]+dx,gc[1]+dy); break
            if gcf: break
        if gcf: break
    if not gcf: print('goal blocked',comp,num); continue
    gc=gcf
    pq=[(0,0,sc[0],sc[1])]; best={sc:0}; par={}
    while pq:
        f,g,x,y=heapq.heappop(pq)
        if (x,y)==gc: break
        if g!=best.get((x,y)): continue
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if free(nx,ny):
                ng=g+1
                if ng<best.get((nx,ny),1e18):
                    best[(nx,ny)]=ng; par[(nx,ny)]=(x,y)
                    heapq.heappush(pq,(ng+abs(nx-gc[0])+abs(ny-gc[1]),ng,nx,ny))
    if gc not in par and gc!=sc: print('no path',comp,num); continue
    path=[gc]; cur=gc
    while cur in par: cur=par[cur]; path.append(cur)
    path.reverse()
    pts=[(X0+x*STEP,Y0+y*STEP) for x,y in path]
    sm=[pts[0]]
    for q in pts[1:]:
        if len(sm)>=2 and abs((sm[-1][0]-sm[-2][0])*(q[1]-sm[-1][1])-(sm[-1][1]-sm[-2][1])*(q[0]-sm[-1][0]))<1e-6: sm[-1]=q
        else: sm.append(q)
    sm[0]=(sx,sy)
    sm.append((tx,ty))
    out[comp+'_'+num]={'net':'GND','segs':[[round(sm[i][0],1),round(sm[i][1],1),round(sm[i+1][0],1),round(sm[i+1][1],1)] for i in range(len(sm)-1)]}
    print(comp,num,'pts',len(sm))
json.dump(out,open('work/eda/gnd_pad_paths.json','w'))
