import json, math, heapq
import numpy as np
G=json.load(open('work/eda/geom_g.json'))
TR,VS=G['tracks'],G['vias']
PADS=json.load(open('work/eda/pad_shapes.json'))
jobs=[('U44','5'),('U44','6'),('C82','2'),('C80','2'),('C81','2'),('R11','2'),('U40','9'),('U40','22'),('C13','2'),('U37','17')]
STEP=5.0; OUR=4.0; CLR=5.9; VR=12.0
LAYERS=[1,2,15,16]; LI={l:i for i,l in enumerate(LAYERS)}
def half(p):
    sh=p.get('shape')
    try:
        if sh and len(sh)>=3: w,h=float(sh[1]),float(sh[2])
        elif sh and len(sh)==2: w=h=float(sh[1])
        else: w=h=20.0
    except: w=h=20.0
    if int(p.get('rot') or 0)%180==90: w,h=h,w
    return w/2,h/2
def rdist(px,py,cx,cy,hw,hh): return math.hypot(max(abs(px-cx)-hw,0),max(abs(py-cy)-hh,0))
def dseg(px,py,x1,y1,x2,y2):
    dx,dy=x2-x1,y2-y1; L=dx*dx+dy*dy
    t=0 if L==0 else max(0,min(1,((px-x1)*dx+(py-y1)*dy)/L))
    return math.hypot(px-(x1+t*dx),py-(y1+t*dy))
out={}
for comp,num in jobs:
    ps=[p for p in PADS if p['comp']==comp and p['num']==num]
    if not ps: print('missing',comp,num); continue
    p=ps[0]; sx,sy=p['x'],p['y']
    cand=[v for v in VS if v['net']=='GND' and math.hypot(v['x']-sx,v['y']-sy)<1200]
    cand.sort(key=lambda v:math.hypot(v['x']-sx,v['y']-sy))
    if not cand: print('no target',comp,num); continue
    tg=cand[0]; gx,gy=tg['x'],tg['y']
    X0,X1=min(sx,gx)-450,max(sx,gx)+450; Y0,Y1=min(sy,gy)-450,max(sy,gy)+450
    NX=int((X1-X0)/STEP)+1; NY=int((Y1-Y0)/STEP)+1
    gT=np.zeros((len(LAYERS),NY,NX),dtype=bool); gV=np.zeros_like(gT)
    def cell(x,y): return int(round((x-X0)/STEP)),int(round((y-Y0)/STEP))
    def disk(a,cx,cy,r):
        ix,iy=cell(cx,cy); rr=int(r/STEP)+1
        x0,x1=max(0,ix-rr),min(NX,ix+rr+1); y0,y1=max(0,iy-rr),min(NY,iy+rr+1)
        if x0>=x1 or y0>=y1: return
        xs=X0+np.arange(x0,x1)*STEP; ys=Y0+np.arange(y0,y1)*STEP
        mx,my=np.meshgrid(xs,ys); a[y0:y1,x0:x1] |= (mx-cx)**2+(my-cy)**2 <= r*r
    def rect(a,cx,cy,hw,hh):
        ix,iy=cell(cx,cy); rx=int(hw/STEP)+1; ry=int(hh/STEP)+1
        x0,x1=max(0,ix-rx),min(NX,ix+rx+1); y0,y1=max(0,iy-ry),min(NY,iy+ry+1)
        if x0>=x1 or y0>=y1: return
        xs=X0+np.arange(x0,x1)*STEP; ys=Y0+np.arange(y0,y1)*STEP
        mx,my=np.meshgrid(xs,ys); a[y0:y1,x0:x1] |= (abs(mx-cx)<=hw)&(abs(my-cy)<=hh)
    def segmk(a,x1,y1,x2,y2,r):
        L=math.hypot(x2-x1,y2-y1); n=max(2,int(L/2))
        for i in range(n+1):
            t=i/n; disk(a,x1+(x2-x1)*t,y1+(y2-y1)*t,r)
    for t in TR:
        if t['net']=='GND': continue
        lay=t.get('layer'); w=(t.get('w') or 8)/2
        for arr,ex in ((gT,CLR+OUR),(gV,CLR+VR)):
            if lay in LI: segmk(arr[LI[lay]],t['x1'],t['y1'],t['x2'],t['y2'],w+ex)
            else:
                for l in LAYERS: segmk(arr[LI[l]],t['x1'],t['y1'],t['x2'],t['y2'],w+ex)
    for v in VS:
        if v['net']=='GND': continue
        d=(v.get('d') or 24)/2
        for arr,ex in ((gT,CLR+OUR),(gV,CLR+VR)):
            for l in LAYERS: disk(arr[LI[l]],v['x'],v['y'],d+ex)
    for q in PADS:
        if q['net']=='GND' or (q['comp'],q['num'])==(comp,num): continue
        hw,hh=half(q)
        for l in LAYERS:
            rect(gT[LI[l]],q['x'],q['y'],hw+CLR+OUR,hh+CLR+OUR)
            rect(gV[LI[l]],q['x'],q['y'],hw+CLR+VR,hh+CLR+VR)
    # avoid holes/vias for new vias
    for v in VS:
        for l in LAYERS: disk(gV[LI[l]],v['x'],v['y'],30)
    def fT(l,x,y): return 0<=x<NX and 0<=y<NY and not gT[LI[l],y,x]
    def fV(l,x,y): return 0<=x<NX and 0<=y<NY and not gV[LI[l],y,x]
    sc=cell(sx,sy); gc=cell(gx,gy)
    if not fT(1,sc[0],sc[1]): print('start blocked',comp,num); continue
    if not fT(1,gc[0],gc[1]): print('goal blocked',comp,num); continue
    h=lambda x,y: abs(x-gc[0])+abs(y-gc[1])
    pq=[(h(sc[0],sc[1]),0,sc[0],sc[1],LI[1])]; best={(LI[1],sc[0],sc[1]):0}; par={}
    found=None
    while pq:
        f,g,x,y,l=heapq.heappop(pq); st=(l,x,y)
        if g!=best.get(st): continue
        if (x,y)==gc: found=st; break
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if fT(LAYERS[l],nx,ny):
                ns=(l,nx,ny); ng=g+1
                if ng<best.get(ns,1e18):
                    best[ns]=ng; par[ns]=st; heapq.heappush(pq,(ng+h(nx,ny),ng,nx,ny,l))
        if all(fV(LAYERS[k],x,y) for k in range(len(LAYERS))):
            for l2 in range(len(LAYERS)):
                if l2==l: continue
                ns=(l2,x,y); ng=g+80
                if ng<best.get(ns,1e18):
                    best[ns]=ng; par[ns]=st; heapq.heappush(pq,(ng+h(x,y),ng,x,y,l2))
    if not found: print('no path',comp,num); continue
    path=[found]
    while path[-1] in par: path.append(par[path[-1]])
    path.reverse()
    pts=[(LAYERS[l],X0+x*STEP,Y0+y*STEP) for (l,x,y) in path]
    pts[0]=(pts[0][0],sx,sy); pts[-1]=(pts[-1][0],gx,gy)
    sm=[pts[0]]
    for q in pts[1:]:
        if len(sm)>=2 and sm[-1][0]==sm[-2][0]==q[0] and abs((sm[-1][1]-sm[-2][1])*(q[2]-sm[-1][2])-(sm[-1][2]-sm[-2][2])*(q[1]-sm[-1][1]))<1e-6: sm[-1]=q
        else: sm.append(q)
    S=[];V=[]
    for i in range(len(sm)-1):
        a,b=sm[i],sm[i+1]
        if a[0]!=b[0]: V.append((a[1],a[2]))
        else: S.append((a[0],a[1],a[2],b[1],b[2]))
    out[f'{comp}_{num}']={'segs':S,'vias':V,'target':[gx,gy]}
    print(comp,num,'path pts',len(sm),'vias',len(V),'target',round(gx),round(gy))
json.dump(out,open('work/eda/gnd_paths3.json','w'))
