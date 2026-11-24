import json, math, heapq
import numpy as np

G = json.load(open('work/eda/geom.json'))
tracks, vias, pads = G['tracks'], G['vias'], G['pads']

CX0, CX1 = 600, 3700
CY0, CY1 = -1700, 1500
STEP = 5.0
NX = int((CX1-CX0)/STEP)+1
NY = int((CY1-CY0)/STEP)+1
LAYERS = [1, 2, 15, 16]
LI = {l:i for i,l in enumerate(LAYERS)}
OUR_HALF, CLR = 4.0, 6.0
grid = np.zeros((len(LAYERS), NY, NX), dtype=bool)

def cell(x, y): return int(round((x-CX0)/STEP)), int(round((y-CY0)/STEP))
def mark_disk(arr, cx, cy, r):
    ix, iy = cell(cx, cy); rr = int(r/STEP)+1
    x0,x1 = max(0,ix-rr), min(NX,ix+rr+1); y0,y1 = max(0,iy-rr), min(NY,iy+rr+1)
    if x0>=x1 or y0>=y1: return
    xs = CX0+np.arange(x0,x1)*STEP; ys = CY0+np.arange(y0,y1)*STEP
    mx,my = np.meshgrid(xs,ys); arr[y0:y1,x0:x1] |= (mx-cx)**2+(my-cy)**2 <= r*r
def mark_rect(arr, cx, cy, hw, hh):
    ix,iy = cell(cx,cy); rx=int((hw)/STEP)+1; ry=int((hh)/STEP)+1
    x0,x1=max(0,ix-rx),min(NX,ix+rx+1); y0,y1=max(0,iy-ry),min(NY,iy+ry+1)
    if x0>=x1 or y0>=y1: return
    xs=CX0+np.arange(x0,x1)*STEP; ys=CY0+np.arange(y0,y1)*STEP
    mx,my=np.meshgrid(xs,ys); arr[y0:y1,x0:x1] |= (abs(mx-cx)<=hw)&(abs(my-cy)<=hh)
def mark_seg(arr,x1,y1,x2,y2,r):
    L=math.hypot(x2-x1,y2-y1); n=max(2,int(L/2))
    for i in range(n+1):
        t=i/n; mark_disk(arr,x1+(x2-x1)*t,y1+(y2-y1)*t,r)

for tr in tracks:
    net=tr.get('net') or ''
    if net in ('MCP_P14','MCP_P15'): continue
    w=tr.get('w') or 8.0; r=w/2+CLR+OUR_HALF; lay=tr.get('layer')
    if lay in LI: mark_seg(grid[LI[lay]],tr['x1'],tr['y1'],tr['x2'],tr['y2'],r)
    else:
        for l in LAYERS: mark_seg(grid[LI[l]],tr['x1'],tr['y1'],tr['x2'],tr['y2'],r)
for v in vias:
    net=v.get('net') or ''
    if net in ('MCP_P14','MCP_P15'): continue
    r=(v.get('d') or 24.0)/2+CLR+OUR_HALF
    for l in LAYERS: mark_disk(grid[LI[l]],v['x'],v['y'],r)
for p in pads:
    net=p.get('net') or ''
    if net in ('MCP_P14','MCP_P15') or net=='': continue
    lay = LAYERS if (p.get('comp') or '')[:1] in ('J','K') else [1]
    if p.get('comp') in ('U33','U34'):
        hw,hh = 8+CLR+OUR_HALF, 29.5+CLR+OUR_HALF
        for l in lay: mark_rect(grid[LI[l]],p['x'],p['y'],hw,hh)
    else:
        r=13+CLR+OUR_HALF
        for l in lay: mark_disk(grid[LI[l]],p['x'],p['y'],r)
bx,by=3937.0,1968.0
xs=CX0+np.arange(NX)*STEP; ys=CY0+np.arange(NY)*STEP
for i in range(len(LAYERS)):
    grid[i][:,:] |= (np.abs(xs)[None,:]>bx-60)
    grid[i][:,:] |= (np.abs(ys)[:,None]>by-60)

def astar(start,goal,extra=None,via_cost=80,start_layer=1,goal_layer=None):
    sx,sy=cell(*start); gx,gy=cell(*goal)
    def free(l,x,y):
        return 0<=x<NX and 0<=y<NY and not grid[LI[l],y,x] and not (extra is not None and extra[LI[l],y,x])
    sl=LI[start_layer]; gl=LI[goal_layer] if goal_layer else None
    if not free(start_layer,sx,sy): print(' start blocked'); return None
    if not free(goal_layer or 1,gx,gy): print(' goal blocked'); return None
    h=lambda x,y: abs(x-gx)+abs(y-gy)
    pq=[(h(sx,sy),0,sx,sy,sl)]; best={(sl,sx,sy):0}; parent={}
    while pq:
        f,g,x,y,l=heapq.heappop(pq); st=(l,x,y)
        if g!=best.get(st): continue
        if (x,y)==(gx,gy) and (gl is None or l==gl):
            path=[st]
            while st in parent: st=parent[st]; path.append(st)
            return path[::-1]
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if free(LAYERS[l],nx,ny):
                ns=(l,nx,ny); ng=g+1
                if ng<best.get(ns,1e18):
                    best[ns]=ng; parent[ns]=st; heapq.heappush(pq,(ng+h(nx,ny),ng,nx,ny,l))
        if all(free(LAYERS[k],x,y) for k in range(len(LAYERS))):
            for l2 in range(len(LAYERS)):
                if l2==l: continue
                ns=(l2,x,y); ng=g+via_cost
                if ng<best.get(ns,1e18):
                    best[ns]=ng; parent[ns]=st; heapq.heappush(pq,(ng+h(x,y),ng,x,y,l2))
    return None

def coords(path): return [(LAYERS[l],CX0+x*STEP,CY0+y*STEP) for (l,x,y) in path]
def simplify(pts):
    out=[pts[0]]
    for p in pts[1:]:
        if len(out)>=2 and out[-1][0]==p[0] and out[-2][0]==p[0]:
            x0,y0=out[-2][1],out[-2][2]; x1,y1=out[-1][1],out[-1][2]; x2,y2=p[1],p[2]
            if abs((x1-x0)*(y2-y1)-(y1-y0)*(x2-x1))<1e-6: out[-1]=p; continue
        out.append(p)
    return out
def los(a,b,extra):
    if a[0]!=b[0]: return False
    l=LI[a[0]]; L=math.hypot(b[1]-a[1],b[2]-a[2]); n=max(2,int(L/2))
    for i in range(n+1):
        t=i/n; x=a[1]+(b[1]-a[1])*t; y=a[2]+(b[2]-a[2])*t
        ix,iy=cell(x,y)
        if not(0<=ix<NX and 0<=iy<NY) or grid[l,iy,ix] or (extra is not None and extra[l,iy,ix]): return False
    return True
def smooth(pts,extra):
    out=[pts[0]]; i=0
    while i<len(pts)-1:
        j=len(pts)-1
        while j>i+1 and not los(pts[i],pts[j],extra): j-=1
        out.append(pts[j]); i=j
    return out
def segs(pts):
    S=[];V=[]
    for i in range(len(pts)-1):
        a,b=pts[i],pts[i+1]
        if a[0]!=b[0]: V.append((a[1],a[2]))
        else: S.append((a[0],a[1],a[2],b[1],b[2]))
    return S,V

start14,goal14=(1032.7,403.6),(2946.5,1139.4)
start15,goal15=(1007.1,403.6),(2896.4,1139.4)
print('P15...'); p15a=astar(start15,goal15,start_layer=1,goal_layer=1); print(' path',len(p15a) if p15a else None)
c15a=smooth(simplify(coords(p15a)),None) if p15a else None
s15a,v15a=segs(c15a) if c15a else ([],[])
v14=[]
print('P15 segs',len(s15a),'vias',len(v15a))
extra=None
if p15a:
    extra=np.zeros_like(grid)
    for (_,x1,y1,x2,y2) in s15a:
        for l in LAYERS: mark_seg(extra[LI[l]],x1,y1,x2,y2,OUR_HALF+CLR+OUR_HALF)
    for (x,y) in v15a:
        for l in LAYERS: mark_disk(extra[LI[l]],x,y,12+CLR+12)
print('P14...'); p14=astar(start14,goal14,extra,start_layer=1,goal_layer=1); print(' path',len(p14) if p14 else None)
c14=smooth(simplify(coords(p14)),extra) if p14 else None
s14,v14=segs(c14) if c14 else ([],[])
print('P14 segs',len(s14),'vias',len(v14))
# prepend pad stubs, append pad stubs
out={}
if p14: out['MCP_P14']={'segs':s14,'vias':v14}
if p15a: out['MCP_P15']={'segs':s15a,'vias':v15a}
json.dump(out,open('work/eda/manual_paths.json','w'))
for n,d in out.items():
    print('---',n)
    for s in d['segs']: print('  L%d (%.1f,%.1f)->(%.1f,%.1f)'%s)
    for v in d['vias']: print('  VIA (%.1f,%.1f)'%v)
