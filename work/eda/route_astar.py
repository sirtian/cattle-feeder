import json, math, heapq, sys
import numpy as np

G = json.load(open('work/eda/geom.json'))
tracks, vias, pads = G['tracks'], G['vias'], G['pads']

CX0, CX1 = 600, 3700      # mil region
CY0, CY1 = -1700, 1400
STEP = 5.0
NX = int((CX1-CX0)/STEP)+1
NY = int((CY1-CY0)/STEP)+1
LAYERS = [1, 2, 15, 16]
LI = {l:i for i,l in enumerate(LAYERS)}
OUR_HALF, CLR = 4.0, 6.0

def cell(x, y):
    return int(round((x-CX0)/STEP)), int(round((y-CY0)/STEP))

grid = np.zeros((len(LAYERS), NY, NX), dtype=bool)  # True = blocked

def mark_disk(arr, cx, cy, r):
    ix, iy = cell(cx, cy)
    rr = int(r/STEP)+1
    x0, x1 = max(0, ix-rr), min(NX, ix+rr+1)
    y0, y1 = max(0, iy-rr), min(NY, iy+rr+1)
    if x0 >= x1 or y0 >= y1: return
    xs = CX0 + np.arange(x0, x1)*STEP
    ys = CY0 + np.arange(y0, y1)*STEP
    mx, my = np.meshgrid(xs, ys)
    m = (mx-cx)**2 + (my-cy)**2 <= r*r
    arr[y0:y1, x0:x1] |= m

def mark_seg(arr, x1, y1, x2, y2, r):
    L = math.hypot(x2-x1, y2-y1)
    n = max(2, int(L/2))
    for i in range(n+1):
        t = i/n
        mark_disk(arr, x1+(x2-x1)*t, y1+(y2-y1)*t, r)

def pad_radius(p):
    # TH connector pads larger; approximate by pad net/comp prefixes
    return 11.0

for tr in tracks:
    net = tr.get('net') or ''
    if net in ('MCP_P14', 'MCP_P15'):
        continue
    w = tr.get('w') or 8.0
    r = w/2.0 + CLR + OUR_HALF
    lay = tr.get('layer')
    if lay in LI:
        mark_seg(grid[LI[lay]], tr['x1'], tr['y1'], tr['x2'], tr['y2'], r)
    else:
        for l in LAYERS:
            mark_seg(grid[LI[l]], tr['x1'], tr['y1'], tr['x2'], tr['y2'], r)

for v in vias:
    net = v.get('net') or ''
    if net in ('MCP_P14','MCP_P15'): continue
    d = v.get('d') or 24.0
    r = d/2.0 + CLR + OUR_HALF
    for l in LAYERS:
        mark_disk(grid[LI[l]], v['x'], v['y'], r)

for p in pads:
    net = p.get('net') or ''
    if net in ('MCP_P14','MCP_P15') or net == '':
        continue
    r = pad_radius(p) + CLR + OUR_HALF
    for l in LAYERS:
        mark_disk(grid[LI[l]], p['x'], p['y'], r)

# block outside board
board_x, board_y = 3937.0, 1968.0
for i in range(len(LAYERS)):
    g = grid[i]
    xs = CX0 + np.arange(NX)*STEP
    ys = CY0 + np.arange(NY)*STEP
    g[:, :] |= (np.abs(xs)[None, :] > board_x-60)
    g[:, :] |= (np.abs(ys)[:, None] > board_y-60)

def astar(start, goal, extra_block=None, via_cost=80):
    sx, sy = cell(*start); gx, gy = cell(*goal)
    def free(l, x, y):
        return 0 <= x < NX and 0 <= y < NY and not grid[LI[l], y, x] and not (extra_block is not None and extra_block[LI[l], y, x])
    if not free(1, sx, sy): print('start blocked', start); return None
    if not free(1, gx, gy): print('goal blocked', goal); return None
    start_state = (0, sx, sy)
    goal_state = (LI[LAYERS[0]], gx, gy)
    h = lambda x, y: (abs(x-gx)+abs(y-gy))
    pq = [(h(sx, sy), 0, sx, sy, 0)]
    best = {(0, sx, sy): 0}
    parent = {}
    moves = [(1,0,1),(-1,0,1),(0,1,1),(0,-1,1)]
    while pq:
        f, g, x, y, l = heapq.heappop(pq)
        st = (l, x, y)
        if g != best.get(st): continue
        if (x, y) == (gx, gy):
            path = [st]
            while st in parent:
                st = parent[st]; path.append(st)
            return path[::-1]
        # moves same layer
        for dx, dy, c in moves:
            nx, ny = x+dx, y+dy
            if free(LAYERS[l], nx, ny):
                ns = (l, nx, ny); ng = g+c
                if ng < best.get(ns, 1e18):
                    best[ns] = ng; parent[ns] = st
                    heapq.heappush(pq, (ng+h(nx, ny), ng, nx, ny, l))
        # via
        for l2 in range(len(LAYERS)):
            if l2 == l: continue
            if all(free(LAYERS[k], x, y) for k in range(len(LAYERS))):
                ns = (l2, x, y); ng = g+via_cost
                if ng < best.get(ns, 1e18):
                    best[ns] = ng; parent[ns] = st
                    heapq.heappush(pq, (ng+h(x, y), ng, x, y, l2))
    return None

def to_coords(path):
    return [(LAYERS[l], CX0+x*STEP, CY0+y*STEP) for (l, x, y) in path]

def simplify(pts):
    out = [pts[0]]
    for p in pts[1:]:
        if len(out) >= 2 and out[-1][0] == p[0] and out[-2][0] == p[0]:
            (_, x0, y0), (_, x1, y1), (_, x2, y2) = out[-2], out[-1], p
            if (abs((x1-x0)*(y2-y1) - (y1-y0)*(x2-x1)) < 1e-6):
                out[-1] = p; continue
        out.append(p)
    return out

def los(a, b):
    if a[0] != b[0]:
        return False
    l = LI[a[0]]
    x1, y1, x2, y2 = a[1], a[2], b[1], b[2]
    L = math.hypot(x2-x1, y2-y1)
    n = max(2, int(L/2))
    for i in range(n+1):
        t = i/n
        x, y = x1+(x2-x1)*t, y1+(y2-y1)*t
        ix, iy = cell(x, y)
        if not (0 <= ix < NX and 0 <= iy < NY) or grid[l, iy, ix]:
            return False
    return True

def smooth(pts):
    out = [pts[0]]
    i = 0
    while i < len(pts)-1:
        j = len(pts)-1
        while j > i+1 and not los(pts[i], pts[j]):
            j -= 1
        out.append(pts[j])
        i = j
    return out

def to_segments(pts):
    segs, vias_out = [], []
    for i in range(len(pts)-1):
        a, b = pts[i], pts[i+1]
        if a[0] != b[0]:
            vias_out.append((a[1], a[2]))
        else:
            segs.append((a[0], a[1], a[2], b[1], b[2]))
    return segs, vias_out

start14, goal14 = (1032.7, 403.6), (2946.5, 1180.0)
start15, goal15 = (1007.1, 403.6), (2896.4, 1180.0)

print('routing P14...')
p14 = astar(start14, goal14)
print('P14 path', len(p14) if p14 else None)
if p14:
    c14 = smooth(simplify(to_coords(p14)))
    s14, v14 = to_segments(c14)
    print('P14 segs', len(s14), 'vias', len(v14))
print('routing P15...')
extra = None
if p14:
    extra = np.zeros_like(grid)
    # add P14 route as obstacle for P15
    for (_, x1, y1, x2, y2) in s14:
        pass
    # approximate: mark path cells with radius
    for (_, x1, y1, x2, y2) in s14:
        for l in LAYERS:
            mark_seg(extra[LI[l]], x1, y1, x2, y2, OUR_HALF+CLR+OUR_HALF)
    for (x, y) in v14:
        for l in LAYERS:
            mark_disk(extra[LI[l]], x, y, 12+CLR+OUR_HALF)
p15 = astar(start15, goal15, extra_block=extra)
print('P15 path', len(p15) if p15 else None)
if p15:
    c15 = smooth(simplify(to_coords(p15)))
    s15, v15 = to_segments(c15)
    print('P15 segs', len(s15), 'vias', len(v15))

def emit(name, segs, vias_out):
    print(f'--- {name}')
    for (l, x1, y1, x2, y2) in segs:
        print(f'  L{l}: ({x1:.1f},{y1:.1f}) -> ({x2:.1f},{y2:.1f})')
    for (x, y) in vias_out:
        print(f'  VIA ({x:.1f},{y:.1f})')

out = {}
if p14:
    s14.append((1, 2946.5, 1180.0, 2946.5, 1139.4))
    out['MCP_P14'] = {'segs': s14, 'vias': v14}
    emit('MCP_P14', s14, v14)
if p15:
    s15.append((1, 2896.4, 1180.0, 2896.4, 1139.4))
    out['MCP_P15'] = {'segs': s15, 'vias': v15}
    emit('MCP_P15', s15, v15)
json.dump(out, open('work/eda/manual_paths.json','w'))
