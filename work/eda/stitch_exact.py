import json, math
G=json.load(open('work/eda/geom_final.json'))
tr,vs=G['tracks'],G['vias']
pads=json.load(open('work/eda/pad_shapes.json'))
def half(p):
    sh=p.get('shape')
    try:
        if sh and len(sh)>=3: w,h=float(sh[1]),float(sh[2])
        elif sh and len(sh)==2: w=h=float(sh[1])
        else: w=h=20.0
    except Exception:
        w=h=20.0
    if int(p.get('rot') or 0)%180==90: w,h=h,w
    return w/2.0,h/2.0
def rdist(px,py,cx,cy,hw,hh):
    dx=max(abs(px-cx)-hw,0); dy=max(abs(py-cy)-hh,0)
    return math.hypot(dx,dy)
jobs=[('U37','3'),('U37','5'),('U37','17'),('C80','2'),('C86','2'),('C8','2'),('U40','22'),('R11','2'),('C13','2'),('U33','10')]
CLR=5.0; OUR=4.0; VR=12.0
def dseg(px,py,x1,y1,x2,y2):
    dx,dy=x2-x1,y2-y1; L=dx*dx+dy*dy
    t=0 if L==0 else max(0,min(1,((px-x1)*dx+(py-y1)*dy)/L))
    return math.hypot(px-(x1+t*dx),py-(y1+t*dy))
def seg_rect(x1,y1,x2,y2,cx,cy,hw,hh,extra):
    L=math.hypot(x2-x1,y2-y1); n=max(2,int(L/2))
    for i in range(n+1):
        t=i/n; x=x1+(x2-x1)*t; y=y1+(y2-y1)*t
        if rdist(x,y,cx,cy,hw,hh) < extra: return True
    return False
def via_ok(x,y):
    for t in tr:
        if t['net']=='GND': continue
        if dseg(x,y,t['x1'],t['y1'],t['x2'],t['y2']) < (t.get('w') or 8)/2+CLR+VR: return False
    for v in vs:
        if math.hypot(x-v['x'],y-v['y']) < 30: return False
    for q in pads:
        hw,hh=half(q)
        if rdist(x,y,q['x'],q['y'],hw,hh) < VR+ (0 if q['net']=='GND' else CLR): return False
    return True
def track_ok(px,py,x,y):
    for t in tr:
        if t['net']=='GND' or t['layer']!=1: continue
        if dseg((px+x)/2,(py+y)/2,t['x1'],t['y1'],t['x2'],t['y2']) < (t.get('w') or 8)/2+CLR+OUR: return False
    for q in pads:
        hw,hh=half(q)
        if q['net']=='GND': continue
        if seg_rect(px,py,x,y,q['x'],q['y'],hw,hh,CLR+OUR): return False
    for v in vs:
        if v['net']=='GND': continue
        if dseg(v['x'],v['y'],px,py,x,y) < CLR+(v.get('d') or 24)/2: return False
    return True
out={}
for comp,num in jobs:
    ps=[p for p in pads if p['comp']==comp and p['num']==num]
    if not ps: print('missing',comp,num); continue
    p=ps[0]; px,py=p['x'],p['y']; found=None
    for rad in range(30,301,5):
        for k in range(72):
            a=2*math.pi*k/72; x=px+rad*math.cos(a); y=py+rad*math.sin(a)
            if via_ok(x,y) and track_ok(px,py,x,y): found=(x,y); break
        if found: break
    if not found: print('no stitch',comp,num); continue
    out[f'{comp}_{num}']={'pad':[px,py],'via':[round(found[0],1),round(found[1],1)]}
    print(comp,num,'via',round(found[0]),round(found[1]),'d',rad)
json.dump(out,open('work/eda/stitch_final.json','w'))
