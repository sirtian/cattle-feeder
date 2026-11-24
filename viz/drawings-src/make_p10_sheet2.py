# -*- coding: utf-8 -*-
"""P10-A 卸料与底盘：A-A 纵剖 / B-B 带路径"""
import os
import math
from make_drawings import SVG, View, ground, dim_h, dim_v, leader, balloon, frame, arrow, OUT
from p10 import (
    tbl,
    X_BOX0, X_BOX1, Y_BOX, Y_FLOOR_BOT, Y_FLOOR, Y_SLAT, Z_BOX,
    TROUGH_X0, TROUGH_X1, GATE_X, GATE_Y0, GATE_Y1,
    BELT_X0, BELT_X1, BELT_TAIL_Z, BELT_KNEE_Z, BELT_TIP_Z,
    BELT_Y, BELT_TIP_Y, BELT_ANG,
    CONC_X0, CONC_X1, CONC_Z, CONC_TOP,
    TROUGH_Z0, TROUGH_Z1, TROUGH_RIM, FEED_Y,
    WHEEL_R, WHEEL_W, AXLE_X, TRACK_Z, CHASSIS_Z, BAT_X0, BAT_X1, AUGER_X,
)


def sheet2():
    svg = SVG()

    # ================= 成本 =================
    svg.text(264, 11, "原型成本（元，±30%）", "txt", size=2.0, weight="bold", anchor="start")
    tbl(svg, 264, 15, [
        ("系统", 55, "start"), ("P10-A", 30, "middle"), ("说明", 55, "start"),
    ], [
        ("车架 / 箱体 / 钣金", "4,300", "含落料槽"),
        ("行走", "3,200", "350 胎"),
        ("卸料机构", "5,900", "带/门"),
        ("电池 / 充电", "2,800", "48V 30Ah"),
        ("电控 / 4G / 相机", "8,000", "3 路"),
        ("线束 / 辅材", "2,000", "—"),
        ("整车合计", "26,200", "不含人工"),
    ], rh=5.4, size=1.4)

    # ================= B-B 1:10 =================
    s = 1 / 10
    bb = View(svg, s, 70, 200)
    ground(svg, 55, 250, 200)
    svg.text(60, 56, "B-B 带路径（x=-250，向 +X 看）", "viewtitle", size=2.5)
    svg.text(60, 59.5, "1:10 · 水平段 + 33° 抬升", "small")

    # 箱体 / 落料槽
    bb.rect(-Z_BOX, 400, -Z_BOX + 20, 530, "med", fill="url(#hatch)")
    bb.rect(Z_BOX - 20, 400, Z_BOX, 530, "med", fill="url(#hatch)")
    bb.rect(-Z_BOX, 530, -Z_BOX + 20, Y_BOX, "med", fill="url(#hatch)")
    bb.rect(Z_BOX - 20, 530, Z_BOX, Y_BOX, "med", fill="url(#hatch)")
    bb.line(-Z_BOX, Y_BOX, Z_BOX, Y_BOX, "med")
    bb.text(0, 1080, "后 400 落料槽 / 上部不存料", "small", size=1.3)
    bb.rect(-Z_BOX, 400, Z_BOX, 425, "thin")
    # 带水平段
    bb.poly([(-390, 450), (430, 450), (430, 400), (-390, 400)], "med", fill="#e3f1ef", close=True)
    # 带倾斜段
    dz, dy = BELT_TIP_Z - BELT_KNEE_Z, BELT_TIP_Y - BELT_Y
    L = math.hypot(dz, dy)
    ux, uy = dz / L, dy / L
    nx, ny = -uy, ux
    pts = [(BELT_KNEE_Z + nx * 25, BELT_Y + ny * 25),
           (BELT_TIP_Z + nx * 25, BELT_TIP_Y + ny * 25),
           (BELT_TIP_Z - nx * 25, BELT_TIP_Y - ny * 25),
           (BELT_KNEE_Z - nx * 25, BELT_Y - ny * 25)]
    bb.poly(pts, "med", fill="#e3f1ef", close=True)
    bb.circle(BELT_TAIL_Z, BELT_Y, 40, "med", fill="#dfe7eb")
    bb.circle(BELT_KNEE_Z, BELT_Y, 40, "med", fill="#dfe7eb")
    bb.circle(BELT_TIP_Z, BELT_TIP_Y, 40, "med", fill="#dfe7eb")
    # 水平段隔板
    for k in range(9):
        zz = -350 + k * 90
        if zz < 410:
            bb.line(zz, 450, zz, 510, "med")
    # 倾斜段隔板
    for k in range(6):
        t = (30 + k * 90) / L
        cz, cy = BELT_KNEE_Z + ux * L * t, BELT_Y + uy * L * t
        p1 = (cz - ux * 16 + nx * 25, cy - uy * 16 + ny * 25)
        p2 = (cz + ux * 16 + nx * 25, cy + uy * 16 + ny * 25)
        p3 = (cz + ux * 16 + nx * 85, cy + uy * 16 + ny * 85)
        p4 = (cz - ux * 16 + nx * 85, cy - uy * 16 + ny * 85)
        bb.poly([p1, p2, p3, p4], "med", fill="#9fb3bf", close=True)
    # 料
    bb.poly([(-350, 450), (400, 450), (400, 490), (-350, 490)], "thin", fill="url(#straw)", close=True)
    # 试验槽
    bb.rect(TROUGH_Z0, 0, TROUGH_Z1, TROUGH_RIM, "phantom")
    bb.line(TROUGH_Z0, FEED_Y, TROUGH_Z1, FEED_Y, "phantom")
    bb.line(BELT_TIP_Z, BELT_TIP_Y - 20, BELT_TIP_Z, TROUGH_RIM + 20, "vis")
    arrow(svg, bb.X(BELT_TIP_Z), bb.Y(TROUGH_RIM + 20), "down")

    dim_h(svg, bb.X(-Z_BOX), bb.X(Z_BOX), 58, "780", ref1=bb.Y(400), ref2=bb.Y(400))
    dim_v(svg, 200, bb.Y(Y_BOX), 215, "1380", ref1=bb.X(Z_BOX), ref2=bb.X(Z_BOX))
    bb.text(1050, 770, "越沿 100", "small", size=1.3)
    ax, ay = bb.X(BELT_TIP_Z), bb.Y(BELT_TIP_Y)
    svg.path("M %.2f %.2f A 12 12 0 0 0 %.2f %.2f" % (ax - 12, ay, ax - 11, ay - 4.8), "dim")
    svg.text(ax - 10, ay - 6, "33°", "dimtxt", size=2.0)
    bb.text(-100, 425, "水平段 820", "small", size=1.3)
    bb.text(700, 655, "33° 抬升", "small", size=1.3, rot=-33)
    bb.text(1120, 615, "槽沿 600", "small", size=1.3)

    # ================= A-A 1:14 =================
    aa = View(svg, 1 / 14, 330, 200)
    ground(svg, 250, 400, 200)
    svg.text(264, 95, "A-A 纵剖（z=0，向 +Z 看）", "viewtitle", size=2.5)
    svg.text(264, 98.5, "1:14 · 链板 / 全宽门 / 落料槽", "small")

    for wx in (-AXLE_X, AXLE_X):
        aa.circle(wx, WHEEL_R, WHEEL_R, "hid")
    aa.rect(-835, 260, 835, 380, "med", fill="url(#hatch2)")
    aa.rect(BAT_X0, 100, BAT_X1, 300, "hid")
    # 箱体
    aa.rect(X_BOX0, Y_FLOOR_BOT, X_BOX0 + 20, Y_BOX, "med", fill="url(#hatch)")
    aa.rect(X_BOX1 - 20, Y_FLOOR_BOT, X_BOX1, Y_BOX, "med", fill="url(#hatch)")
    aa.rect(X_BOX0, Y_FLOOR_BOT, X_BOX1, 530, "med", fill="url(#hatch)")
    aa.rect(-50, 530, 815, Y_SLAT, "med", fill="#dfe7eb")
    aa.poly([(-50, Y_SLAT), (815, Y_SLAT), (815, 1240), (-50, 1240)],
            "thin", fill="url(#straw)", close=True)
    # 后落料槽 + 带截面
    aa.rect(TROUGH_X0, 400, TROUGH_X1, Y_FLOOR_BOT, "thin", fill="#dfe7eb")
    aa.rect(BELT_X0, 400, BELT_X1, 450, "med", fill="#e3f1ef")
    # 全宽门
    aa.rect(GATE_X - 14, GATE_Y0, GATE_X, GATE_Y1, "med", fill="#e7edf0")
    aa.line(GATE_X - 7, GATE_Y1, GATE_X - 7, 900, "med")
    aa.rect(GATE_X - 22, 900, GATE_X - 2, 980, "med", fill="#dfe7eb")
    # 精料仓
    aa.rect(CONC_X0, 420, CONC_X1, CONC_TOP, "vis", fill="#fbfcfc")
    aa.rect(CONC_X0 + 20, 440, CONC_X1 - 20, CONC_TOP - 20, "", fill="url(#conc)")
    aa.poly([(CONC_X0, 420), (CONC_X0 + 80, 260), (CONC_X1 - 80, 260), (CONC_X1, 420)],
            "med", fill="#fbfcfc", close=True)
    aa.rect(CONC_X0 + 10, CONC_TOP, CONC_X1 - 10, CONC_TOP + 30, "med", fill="#eef2f4")
    for lx in (CONC_X0 + 10, CONC_X1 - 40):
        aa.rect(lx, 380, lx + 30, 420, "med", fill="#f0c07a")
    for lx in (-250, 500):
        aa.rect(lx - 30, 380, lx + 30, 440, "med", fill="#dfe7eb")
        aa.rect(lx - 30, 440, lx + 30, 480, "med", fill="#f0c07a")
    aa.circle(-642, 360, 45, "med", fill="#dfe7eb")

    dim_h(svg, aa.X(-925), aa.X(925), 206, "1850", ref1=200, ref2=200)
    dim_h(svg, aa.X(X_BOX0), aa.X(X_BOX1), 211, "1285", ref1=200, ref2=200)
    dim_h(svg, aa.X(-AXLE_X), aa.X(AXLE_X), 216, "1200", ref1=200, ref2=200)
    dim_v(svg, 200, aa.Y(Y_BOX), 257, "1380", ref1=aa.X(X_BOX1), ref2=aa.X(X_BOX1))
    svg.text(264, 222, "全宽门 780×180（开度 30–80）；带 400×1555，水平 820 + 33°", "small", size=1.4, anchor="start")
    balloon(svg, 4, aa.X(400), aa.Y(1200), 380, 116)
    balloon(svg, 5, aa.X(-642), aa.Y(800), 300, 128)

    # ================= 轴荷 / 说明 =================
    svg.text(12, 204, "轴荷（P10-A）", "txt", size=2.0, weight="bold", anchor="start")
    tbl(svg, 12, 208, [
        ("工况", 42, "start"), ("总重 kg", 32, "middle"),
        ("前轴 kg", 32, "middle"), ("后轴 kg", 32, "middle"),
    ], [
        ("空车", "340", "176", "164"),
        ("满载 74+92", "506", "234", "272"),
        ("设计上限", "600", "280", "320"),
    ], rh=6.0, size=1.7)

    svg.text(160, 204, "A 方案要点", "txt", size=2.0, weight="bold", anchor="start")
    svg.mtext(160, 209, [
        "1. 链板 885 长，把料推到 x=-50 全宽门；",
        "2. 门后 400 为落料槽，无 -Z 侧死区；",
        "3. 带 400 宽，水平穿箱底 820，再 33° 抬升；",
        "4. 带速 0.3–0.5，Q带 0.58 kg/s ≥ 2×Q门；",
        "5. 箱容 0.62 m³（74 kg），10 头 1.6 天。",
    ], "notetxt", size=1.5, lh=4.5)

    frame(svg, 2, 3, "原型车（A）· 卸料与底盘", "1:10 / 1:14", "FC-P10-02A",
          project="智能养牛 · 10 头原型验证")
    return svg.render("P10-A 卸料与底盘")


if __name__ == "__main__":
    data = sheet2()
    path = os.path.join(OUT, "p10-02a-chassis.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    print("wrote", path, len(data))
