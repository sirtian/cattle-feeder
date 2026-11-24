import json, math, heapq
import numpy as np
G=json.load(open('work/eda/geom_now2.json'))
tracks,vias,pads=G['tracks'],G['vias'],G['pads']
NET='MCP_P16'
start=(-4129.1,2684.3); goal=(-4771.3,2682.7)
STEP=5.0; OUR=4.0; CLR=6.0; VR=12.0
LAYERS=[1,2,15,16]; LI={l:i for i,l in enumerate(LAYERS)}
X0,X1=min(start[0],goal[0])-500,max(start[0],goal[0])+500
Y0,Y1=min(start[1],goal[1])-500,max(start[1],goal[1])+500
NX=int((X1-X0)/STEP)+1; NY=int((Y1-Y0)/STEP)+1
gT=np.zeros((len(LAYERS),NY,NX),dtype=bool)
gV=np.zeros((len(LAYERS),NY,NX),dtype=bool)
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
def segT(a,x1,y1,x2,y2,r):
    L=math.hypot(x2-x1,y2-y1); n=max(2,int(L/2))
    for i in range(n+1):
        t=i/n; disk(a,x1+(x2-x1)*t,y1+(y2-y1)*t,r)
for t in tracks:
    if t['net']==NET: continue
    lay=t.get('layer'); w=(t.get('w') or 8)/2
    for arr,extra in ((gT,CLR+OUR),(gV,CLR+VR)):
        r=w+extra
        if lay in LI: segT(arr[LI[lay]],t['x1'],t['y1'],t['x2'],t['y2'],r)
        else:
            for l in LAYERS: segT(arr[LI[l]],t['x1'],t['y1'],t['x2'],t['y2'],r)
for v in vias:
    if v['net']==NET: continue
    d=(v.get('d') or 24)/2
    for arr,extra in ((gT,CLR+OUR),(gV,CLR+VR)):
        for l in LAYERS: disk(arr[LI[l]],v['x'],v['y'],d+extra)
for p in pads:
    if p['net']==NET: continue
    for arr,extra in ((gT,CLR+OUR),(gV,CLR+VR)):
        if p['comp'] in ('U33','U34'):
            for l in LAYERS: rect(arr[LI[l]],p['x'],p['y'],8+extra,34+extra)
        else:
            for l in LAYERS: disk(arr[LI[l]],p['x'],p['y'],10+extra)
def astar(start,goal,sl=1,gl=None):
    sx,sy=cell(*start); gx,gy=cell(*goal)
    def fT(l,x,y): return 0<=x<NX and 0<=y<NY and not gT[LI[l],y,x]
    def fV(l,x,y): return 0<=x<NX and 0<=y<NY and not gV[LI[l],y,x]
    if not fT(sl,sx,sy): print('start blocked'); return None
    if not fT(gl or 1,gx,gy): print('goal blocked'); return None
    gl_i=LI[gl] if gl else None
    h=lambda x,y: abs(x-gx)+abs(y-gy)
    pq=[(h(sx,sy),0,sx,sy,LI[sl])]; best={(LI[sl],sx,sy):0}; par={}
    while pq:
        f,g,x,y,l=heapq.heappop(pq); st=(l,x,y)
        if g!=best.get(st): continue
        if (x,y)==(gx,gy) and (gl_i is None or l==gl_i):
            path=[st]
            while st in par: st=par[st]; path.append(st)
            return path[::-1]
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
    return None
p=astar(start,goal)
print('path',len(p) if p else None)
if p:
    pts=[(LAYERS[l],X0+x*STEP,Y0+y*STEP) for (l,x,y) in p]
    pts[0]=(pts[0][0],start[0],start[1]); pts[-1]=(pts[-1][0],goal[0],goal[1])
    sm=[pts[0]]
    for q in pts[1:]:
        if len(sm)>=2 and sm[-1][0]==sm[-2][0]==q[0] and abs((sm[-1][1]-sm[-2][1])*(q[2]-sm[-1][2])-(sm[-1][2]-sm[-2][2])*(q[1]-sm[-1][1]))<1e-6: sm[-1]=q
        else: sm.append(q)
    S=[];V=[]
    for i in range(len(sm)-1):
        a,b=sm[i],sm[i+1]
        if a[0]!=b[0]: V.append((a[1],a[2]))
        else: S.append((a[0],a[1],a[2],b[1],b[2]))
    json.dump({'MCP_P16':{'segs':S,'vias':V}},open('work/eda/p16_path2.json','w'))
    for s in S: print('L%d (%.1f,%.1f)->(%.1f,%.1f)'%s)
    for v in V: print('VIA (%.1f,%.1f)'%v)
