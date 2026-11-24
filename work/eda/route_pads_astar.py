import json, math, heapq
import numpy as np
G=json.load(open('work/eda/geom300.json'))
tracks,vias,pads=G['tracks'],G['vias'],G['pads']
targets=[('R4','24V_P'),('C77','3V3'),('C7','24V_SENSE'),('C85','24V_SENSE'),('R5','24V_SENSE'),('C8','48V_SENSE'),('R6','48V_SENSE')]
STEP=5.0; OUR=4.0; CLR=6.0
def dseg(px,py,x1,y1,x2,y2):
    dx,dy=x2-x1,y2-y1; L=dx*dx+dy*dy
    t=0 if L==0 else max(0,min(1,((px-x1)*dx+(py-y1)*dy)/L))
    return math.hypot(px-(x1+t*dx),py-(y1+t*dy)),(x1+t*dx,y1+t*dy)
out={}
for comp,net in targets:
    pp=[p for p in pads if p['comp']==comp and p['net']==net]
    if not pp: print('no pad',comp,net); continue
    p=pp[0]; sx,sy=p['x'],p['y']
    best=None
    for t in tracks:
        if t['net']!=net or t['layer']!=1: continue
        d,q=dseg(sx,sy,t['x1'],t['y1'],t['x2'],t['y2'])
        if best is None or d<best[0]: best=(d,q)
    if best is None: print('no target',comp,net); continue
    (d,q)=best; gx,gy=q
    X0,X1=min(sx,gx)-300,max(sx,gx)+300; Y0,Y1=min(sy,gy)-300,max(sy,gy)+300
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
        if t['net'] in (net,'GND') or t['layer']!=1: continue
        if t['x1']>X1 or t['x2']>X1 or t['x1']<X0 and t['x2']<X0: pass
        mark_seg(t['x1'],t['y1'],t['x2'],t['y2'],(t.get('w') or 8)/2+CLR+OUR)
    for v in vias:
        if v['net']==net: continue
        mark_disk(v['x'],v['y'],(v.get('d') or 24)/2+CLR+OUR)
    for q2 in pads:
        if q2['net']==net: continue
        if q2['comp'] in ('U33','U34'): continue
        mark_disk(q2['x'],q2['y'],13+CLR+OUR)
    sc=cell(sx,sy); gc=cell(gx,gy)
    def free(x,y): return 0<=x<NX and 0<=y<NY and not grid[y,x]
    if not free(*sc): print('start blocked',comp); continue
    if not free(*gc):
        # nudge goal to nearest free cell
        found=False
        for rr in range(1,20):
            for dx in range(-rr,rr+1):
                for dy in range(-rr,rr+1):
                    if free(gc[0]+dx,gc[1]+dy): gc=(gc[0]+dx,gc[1]+dy); found=True; break
                if found: break
            if found: break
        if not found: print('goal blocked',comp); continue
    pq=[(0,0,sc[0],sc[1])]; bestd={sc:0}; parent={}
    while pq:
        f,g,x,y=heapq.heappop(pq)
        if (x,y)==gc: break
        if g!=bestd.get((x,y)): continue
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if free(nx,ny):
                ng=bestd[(x,y)]+1
                if ng<bestd.get((nx,ny),1e18):
                    bestd[(nx,ny)]=ng; parent[(nx,ny)]=(x,y)
                    heapq.heappush(pq,(ng+abs(nx-gc[0])+abs(ny-gc[1]),ng,nx,ny))
    if gc not in parent and gc!=sc: print('no path',comp); continue
    path=[gc]; cur=gc
    while cur in parent: cur=parent[cur]; path.append(cur)
    path.reverse()
    pts=[(X0+x*STEP,Y0+y*STEP) for (x,y) in path]
    # simplify collinear
    sm=[pts[0]]
    for q2 in pts[1:]:
        if len(sm)>=2 and abs((sm[-1][0]-sm[-2][0])*(q2[1]-sm[-1][1])-(sm[-1][1]-sm[-2][1])*(q2[0]-sm[-1][0]))<1e-6: sm[-1]=q2
        else: sm.append(q2)
    sm[0]=(sx,sy)
    out[net+'_'+comp]={'net':net,'segs':[[round(sm[i][0],1),round(sm[i][1],1),round(sm[i+1][0],1),round(sm[i+1][1],1)] for i in range(len(sm)-1)]}
    print(comp,net,'path pts',len(sm),'dist %.0f'%d)
json.dump(out,open('work/eda/pad_fix_paths.json','w'))
