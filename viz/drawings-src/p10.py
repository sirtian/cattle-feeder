# -*- coding: utf-8 -*-
"""P10 十头原型车（A 方案）—— 共用几何与表格

A 方案：箱后 400 做落料槽，x=-50 全宽后门（780×180）计量；
400 宽带从 z=-390 水平穿到 z=430，再 33° 抬升到 z=1050；
链板只把料推到后门，全宽落料，无侧向死区。
"""
import math
from make_drawings import (
    SVG, View, ground, dim_h, dim_v, leader, balloon, frame, arrow,
    center_mark, OUT,
)

# ---------------- 总体（mm） ----------------
X_MIN, X_MAX = -925, 925          # 1850，含保险杠
Y_ANT, Y_BOX = 1640, 1380         # 天线 / 箱顶（箱体抬高 60 让带）
X_BOX0, X_BOX1 = -450, 835        # 箱长 1285
Z_BOX = 390                       # 箱宽 780
Y_FLOOR_BOT, Y_FLOOR = 480, 530   # 箱底 / 底板顶
Y_SLAT = 565                      # 链板面

# 箱后落料槽 / 全宽门
TROUGH_X0, TROUGH_X1 = -450, -50
GATE_X = -50
GATE_Y0, GATE_Y1 = 530, 710       # 门洞 180 高
GATE_GAP = (30, 80)

# 侧带（箱底水平段 + 外侧倾斜段）
BELT_X0, BELT_X1 = -450, -50      # 带宽 400
BELT_TAIL_Z = -390
BELT_KNEE_Z = 430
BELT_TIP_Z = 1050
BELT_Y = 425                      # 水平段带面中心
BELT_TIP_Y = 820
BELT_RUN = BELT_TIP_Z - BELT_KNEE_Z     # 620
BELT_RISE = BELT_TIP_Y - BELT_Y         # 395
BELT_ANG = math.degrees(math.atan2(BELT_RISE, BELT_RUN))   # 32.5°
BELT_LEN = (BELT_KNEE_Z - BELT_TAIL_Z) + math.hypot(BELT_RUN, BELT_RISE)

CONC_X0, CONC_X1, CONC_Z = -835, -450, 250
CONC_TOP = 1020                   # 0.116 m³
TROUGH_Z0, TROUGH_Z1 = 950, 1350  # 试验槽
TROUGH_RIM, FEED_Y = 600, 430
WHEEL_R, WHEEL_W = 175, 130
AXLE_X, TRACK_Z = 600, 380
CHASSIS_Z = 280                   # 车架宽 560
BAT_X0, BAT_X1 = -100, 400
AUGER_X = -560

# 兼容旧图（方案对比图）
GATE_X0, GATE_X1 = -450, -50
BELT_Z0, BELT_Z1 = 430, 1050
BELT_Y0, BELT_Y1 = 390, 820


def belt_y(z):
    """带面中心高度：z<=430 水平，之后按 33° 抬升"""
    if z <= BELT_KNEE_Z:
        return BELT_Y
    return BELT_Y + (z - BELT_KNEE_Z) * BELT_RISE / BELT_RUN


def wheel10(v, cx, r=WHEEL_R):
    v.circle(cx, r, r, "vis")
    v.circle(cx, r, r * 0.66, "thin")
    v.circle(cx, r, 42, "thin")
    v.circle(cx, r, 16, "thin")
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        v.line(cx + 20 * math.cos(a), r + 20 * math.sin(a),
               cx + 60 * math.cos(a), r + 60 * math.sin(a), "thin")


def tbl(svg, x, y, cols, rows, rh=5.2, size=1.7):
    W = sum(c[1] for c in cols)
    H = rh * (len(rows) + 1)
    svg.rect(x, y, W, H, "med", fill="none")
    svg.rect(x, y, W, rh, "", fill="#e9eff3")
    cx = x
    for t, w, al in cols:
        svg.line(cx, y, cx, y + H, "thin")
        svg.text(cx + 1.2 if al == "start" else cx + w / 2, y + rh * 0.7,
                 t, "txt", size=size, anchor=al)
        cx += w
    for i, row in enumerate(rows):
        ry = y + rh * (i + 1)
        svg.line(x, ry, x + W, ry, "thin")
        cx = x
        for (t, w, al), val in zip(cols, row):
            svg.text(cx + 1.2 if al == "start" else cx + w / 2, ry + rh * 0.7,
                     str(val), "notetxt", size=size, anchor=al)
            cx += w
