import json, math, heapq
import numpy as np
G=json.load(open('work/eda/geom_2l.json'))
TR,VS,PADS=G['tracks'],G['vias'],G['pads']
PS=json.load(open('work/eda/pad_shapes.json'))
def padinfo(comp,num,net):
    for p in PS:
        if p['comp']==comp and p['num']==num: return p
    return None
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
LAYERS=[1,2]; LI={1:0,2:1}
STEP=4.0; OUR=4.0; CLR=5.9; VR=12.0
def route(net,a,b):
    sx,sy=a; gx,gy=b
    X0,X1=min(sx,gx)-200,max(sx,gx)+200; Y0,Y1=min(sy,gy)-200,max(sy,gy)+200
    NX=int((X1-X0)/STEP)+1; NY=int((Y1-Y0)/STEP)+1
    gT=np.zeros((2,NY,NX),bool); gV=np.zeros((2,NY,NX),bool)
    def cell(x,y): return int(round((x-X0)/STEP)),int(round((y-Y0)/STEP))
    def disk(arr,cx,cy,r):
        ix,iy=cell(cx,cy); rr=int(r/STEP)+1
        x0,x1=max(0,ix-rr),min(NX,ix+rr+1); y0,y1=max(0,iy-rr),min(NY,iy+rr+1)
        if x0>=x1 or y0>=y1: return
        xs=X0+np.arange(x0,x1)*STEP; ys=Y0+np.arange(y0,y1)*STEP
        mx,my=np.meshgrid(xs,ys); arr[y0:y1,x0:x1] |= (mx-cx)**2+(my-cy)**2 <= r*r
    def rect(arr,cx,cy,hw,hh):
        ix,iy=cell(cx,cy); rx=int(hw/STEP)+1; ry=int(hh/STEP)+1
        x0,x1=max(0,ix-rx),min(NX,ix+rx+1); y0,y1=max(0,iy-ry),min(NY,iy+ry+1)
        if x0>=x1 or y0>=y1: return
        xs=X0+np.arange(x0,x1)*STEP; ys=Y0+np.arange(y0,y1)*STEP
        mx,my=np.meshgrid(xs,ys); arr[y0:y1,x0:x1] |= (abs(mx-cx)<=hw)&(abs(my-cy)<=hh)
    for t in TR:
        if t['net']==net or t['net']=='GND': continue
        w=(t.get('w') or 8)/2
        for arr,ex in ((gT,CLR+OUR),(gV,CLR+VR)):
            for l in (1,2): disk(arr[LI[l]],t['x1'],t['y1'],0) if False else None
        lay=t['layer']; w=(t.get('w') or 8)/2
        if lay in LI:
            # rasterize line
            L=math.hypot(t['x2']-t['x1'],t['y2']-t['y1']); n=max(2,int(L/2))
            for i in range(n+1):
                x=t['x1']+(t['x2']-t['x1'])*i/n; y=t['y1']+(t['y2']-t['y1'])*i/n
                disk(gT[LI[lay]],x,y,w+CLR+OUR); disk(gV[LI[lay]],x,y,w+CLR+VR)
        else:
            L=math.hypot(t['x2']-t['x1'],t['y2']-t['y1']); n=max(2,int(L/2))
            for l in (1,2):
                for i in range(n+1):
                    x=t['x1']+(t['x2']-t['x1'])*i/n; y=t['y1']+(t['y2']-t['y1'])*i/n
                    disk(gT[LI[l]],x,y,w+CLR+OUR); disk(gV[LI[l]],x,y,w+CLR+VR)
    for v in VS:
        if v['net'] in (net,'GND'): continue
        d=(v.get('d') or 24)/2
        for l in (1,2): disk(gT[LI[l]],v['x'],v['y'],d+CLR+OUR); disk(gV[LI[l]],v['x'],v['y'],d+CLR+VR)
    for q in PADS:
        if q['net'] in (net,'GND'): continue
        pp=padinfo(q['comp'],q['num'],q['net'])
        hw,hh=half(pp) if pp else (10,10)
        for l in (1,2):
            rect(gT[LI[l]],q['x'],q['y'],hw+CLR+OUR,hh+CLR+OUR)
            rect(gV[LI[l]],q['x'],q['y'],hw+CLR+VR,hh+CLR+VR)
    for v in VS:
        for l in (1,2): disk(gV[LI[l]],v['x'],v['y'],30)
    def fT(l,x,y): return 0<=x<NX and 0<=y<NY and not gT[LI[l],y,x]
    def fV(l,x,y): return 0<=x<NX and 0<=y<NY and not gV[LI[l],y,x]
    sc=cell(sx,sy); gc=cell(gx,gy)
    if not fT(1,*sc): print(net,'start blocked'); return None
    if not fT(1,*gc): print(net,'goal blocked'); return None
    h=lambda x,y: abs(x-gc[0])+abs(y-gc[1])
    pq=[(h(*sc),0,sc[0],sc[1],0)]; best={(0,sc[0],sc[1]):0}; par={}
    while pq:
        f,g,x,y,l=heapq.heappop(pq); st=(l,x,y)
        if f>best.get(st,1e18)+h(x,y)-h(x,y): pass
        if g!=best.get(st): continue
        if (x,y)==gc:
            path=[st]
            while st in par: st=par[st]; path.append(st)
            return path[::-1]
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if fT(LAYERS[l],nx,ny):
                ns=(l,nx,ny); ng=g+1
                if ng<best.get(ns,1e18):
                    best[ns]=ng; par[ns]=st; heapq.heappush(pq,(ng+h(nx,ny),ng,nx,ny,l))
        if all(fV(LAYERS[k],x,y) for k in (1,2)):
            for l2 in (0,1):
                if l2==l: continue
                ns=(l2,x,y); ng=g+80
                if ng<best.get(ns,1e18):
                    best[ns]=ng; par[ns]=st; heapq.heappush(pq,(ng+h(x,y),ng,x,y,l2))
    return None
jobs=[('BMS_TX',('U40','3'),('U41','4')),('CLK_SC',('U40','6'),('Y40','3')),
      ('RST_SC',('C90','1'),('R92','2')),('RST_SC',('R92','2'),('U40','5'))]
out={}
for net,c1,c2 in jobs:
    p1=padinfo(*c1,net); p2=padinfo(*c2,net)
    if not p1 or not p2: print('missing',net,c1,c2); continue
    path=route(net,(p1['x'],p1['y']),(p2['x'],p2['y']))
    if not path: print('no path',net,c1,c2); continue
    pts=[(LAYERS[l],X0:=0,X0) for l,x,y in path] if False else [(LAYERS[l],x,y) for l,x,y in path]
    # rebuild coords with region origin from closure: recompute not available; use stored? Not implemented
    print(net,'path',len(path))
json.dump({},open('work/eda/three.json','w'))
