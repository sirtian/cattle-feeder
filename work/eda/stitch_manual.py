import json, math
G=json.load(open('work/eda/geom_manual.json'))
TR,VS=G['tracks'],G['vias']
PADS=json.load(open('work/eda/pad_shapes_manual.json'))
jobs=[('U37','3'),('U37','5'),('U37','2'),('R94','2'),('U45','2'),('U40','22'),('U40','9'),
      ('R10','2'),('U4','2'),('U33','17'),('U33','10'),('C37','2'),('C38','2')]
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
CLR=5.9; OUR=4.0; VR=12.0
def via_ok(x,y):
    for t in TR:
        if t['net']=='GND': continue
        if dseg(x,y,t['x1'],t['y1'],t['x2'],t['y2']) < (t.get('w') or 8)/2+CLR+VR: return False
    for v in VS:
        if math.hypot(x-v['x'],y-v['y']) < 30: return False
    for q in PADS:
        hw,hh=half(q)
        if rdist(x,y,q['x'],q['y'],hw,hh) < VR + (0 if q['net']=='GND' else CLR): return False
    return True
def track_ok(px,py,x,y):
    L=math.hypot(x-px,y-py); n=max(2,int(L/2))
    for i in range(n+1):
        t=i/n; sx=px+(x-px)*t; sy=py+(y-py)*t
        for tr in TR:
            if tr['net']=='GND' or tr['layer']!=1: continue
            if dseg(sx,sy,tr['x1'],tr['y1'],tr['x2'],tr['y2']) < (tr.get('w') or 8)/2+CLR+OUR: return False
        for v in VS:
            if v['net']=='GND': continue
            if math.hypot(sx-v['x'],sy-v['y']) < CLR+(v.get('d') or 24)/2+OUR: return False
        for q in PADS:
            if q['net']=='GND': continue
            hw,hh=half(q)
            if rdist(sx,sy,q['x'],q['y'],hw,hh) < CLR+OUR: return False
    return True
out=[]
for comp,num in jobs:
    ps=[p for p in PADS if p['comp']==comp and p['num']==num]
    if not ps: out.append({'ref':f'{comp}.{num}','note':'pad not found'}); continue
    p=ps[0]; px,py=p['x'],p['y']
    found=None
    for rad in range(20,301,5):
        for k in range(72):
            a=2*math.pi*k/72; x=px+rad*math.cos(a); y=py+rad*math.sin(a)
            if via_ok(x,y) and track_ok(px,py,x,y): found=(x,y,rad); break
        if found: break
    rec={'ref':f'{comp}.{num}','pad_mm':[round(px*0.0254,2),round(py*0.0254,2)]}
    if found:
        x,y,rad=found
        rec['via_mm']=[round(x*0.0254,2),round(y*0.0254,2)]
        rec['offset_mm']=[round((x-px)*0.0254,2),round((y-py)*0.0254,2)]
        rec['dist_mm']=round(rad*0.0254,2)
    else:
        # nearest GND via
        best=min([v for v in VS if v['net']=='GND'], key=lambda v: math.hypot(v['x']-px,v['y']-py))
        rec['via_mm']=[round(best['x']*0.0254,2),round(best['y']*0.0254,2)]
        rec['note']='nearest GND via, manual track'
    out.append(rec)
print(json.dumps(out,ensure_ascii=False,indent=1))
json.dump(out,open('work/eda/manual_list.json','w'),ensure_ascii=False)
