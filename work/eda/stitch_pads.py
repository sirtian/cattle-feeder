import json, math
G=json.load(open('work/eda/geom_now.json'))
tracks,vias,pads=G['tracks'],G['vias'],G['pads']
jobs=[('U37','2'),('U37','3'),('U37','5'),('U4','2'),('C80','2'),('C81','2'),('U33','10'),('U33','17')]
CLR=5.1; OUR=4.0; VR=12.0
def dseg(px,py,x1,y1,x2,y2):
    dx,dy=x2-x1,y2-y1; L=dx*dx+dy*dy
    t=0 if L==0 else max(0,min(1,((px-x1)*dx+(py-y1)*dy)/L))
    return math.hypot(px-(x1+t*dx),py-(y1+t*dy))
def via_ok(x,y,own_pad):
    for t in tracks:
        if t['net']=='GND': continue
        r=(t.get('w') or 8)/2+CLR+VR
        # only same-layer? via passes all layers; check all tracks
        if dseg(x,y,t['x1'],t['y1'],t['x2'],t['y2'])<r: return False
    for v in vias:
        if v['net']=='GND': continue
        if math.hypot(x-v['x'],y-v['y'])<VR+CLR+(v.get('d') or 24)/2: return False
    for q in pads:
        if q['net']=='GND': continue
        if math.hypot(x-q['x'],y-q['y'])<VR+CLR+10: return False
    return True
def track_ok(px,py,x,y):
    for t in tracks:
        if t['net']=='GND' or t['layer']!=1: continue
        r=(t.get('w') or 8)/2+CLR+OUR
        if dseg((px+x)/2,(py+y)/2,t['x1'],t['y1'],t['x2'],t['y2'])<r-0: return False
    for q in pads:
        if q['net']=='GND': continue
        # distance from segment to pad center
        if dseg(q['x'],q['y'],px,py,x,y)<CLR+10: return False
    for v in vias:
        if v['net']=='GND': continue
        if dseg(v['x'],v['y'],px,py,x,y)<CLR+(v.get('d') or 24)/2: return False
    return True
out={}
for comp,num in jobs:
    ps=[p for p in pads if p['comp']==comp and p['num']==num]
    if not ps: print('missing',comp,num); continue
    p=ps[0]; px,py=p['x'],p['y']
    found=None
    for rad in range(35,161,5):
        for k in range(0,72):
            a=2*math.pi*k/72
            x=px+rad*math.cos(a); y=py+rad*math.sin(a)
            if via_ok(x,y,p) and track_ok(px,py,x,y): found=(x,y); break
        if found: break
    if not found: print('no stitch',comp,num); continue
    out[comp+'_'+num]={'net':'GND','pad':[px,py],'via':[round(found[0],1),round(found[1],1)]}
    print(comp,num,'via at',round(found[0]),round(found[1]),'d',rad)
json.dump(out,open('work/eda/gnd_stitch.json','w'))
