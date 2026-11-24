# -*- coding: utf-8 -*-
"""FC-03 精料仓、底盘与轴荷"""
import os
from make_drawings import (
    SVG, View, ground, dim_h, dim_v, leader, balloon, frame, arrow,
    center_mark, OUT,
    AXLE_X, TRACK_Z, WHEEL_R, WHEEL_W,
    BELT_Z0, BELT_Z1, TROUGH_RIM,
)


def tbl(svg, x, y, cols, rows, rh=5.2, size=1.75):
    """cols: [(title, width, anchor)]; rows: [[...]]"""
    W = sum(c[1] for c in cols)
    H = rh * (len(rows) + 1)
    svg.rect(x, y, W, H, "med", fill="none")
    svg.rect(x, y, W, rh, "", fill="#e9eff3")
    cx = x
    for t, w, al in cols:
        svg.line(cx, y, cx, y + H, "thin")
        svg.text(cx + 1.4 if al == "start" else cx + w / 2, y + rh * 0.68,
                 t, "txt", size=size, anchor=al)
        cx += w
    for i, row in enumerate(rows):
        ry = y + rh * (i + 1)
        svg.line(x, ry, x + W, ry, "thin")
        cx = x
        for (t, w, al), v in zip(cols, row):
            svg.text(cx + 1.4 if al == "start" else cx + w / 2, ry + rh * 0.68,
                     str(v), "notetxt", size=size, anchor=al)
            cx += w


def sheet3():
    svg = SVG()

    # ============ 顶部：轴荷示意（1:50） ============
    s = 1 / 60
    ld = View(svg, s, 75, 40)
    ground(svg, 50, 100, 40)
    for wx in (-AXLE_X, AXLE_X):
        ld.circle(wx, WHEEL_R, WHEEL_R, "vis", fill="#e6ebee")
        ld.circle(wx, WHEEL_R, 70, "thin")
        svg.line(ld.X(wx), 43.2, ld.X(wx), 40.6, "dim")
        arrow(svg, ld.X(wx), 40.6, "up")
        svg.text(ld.X(wx), 46.0, "521" if wx > 0 else "622", "dimtxt", size=1.9)
    ld.rect(-1250, 300, 1250, 460, "med", fill="url(#hatch2)")
    ld.rect(-700, 460, 1300, 1560, "med", fill="#f8fafb")
    ld.rect(-1300, 290, -700, 1260, "med", fill="#fbfcfc")
    ld.poly([(-1300, 500), (-1220, 290), (-780, 290), (-700, 500)], "med", close=True)
    gx, gy = -70, 900
    ld.circle(gx, gy, 55, "cen")
    ld.line(gx - 55, gy, gx + 55, gy, "cen")
    ld.line(gx, gy - 55, gx, gy + 55, "cen")
    ld.text(gx, gy - 3, "G", "txt", size=2.0, weight="bold")
    svg.text(ld.X(AXLE_X), 49.0, "前轴", "small", size=1.6)
    svg.text(ld.X(-AXLE_X), 49.0, "后轴", "small", size=1.6)
    svg.text(108, 13.5, "满载轴荷（310+180 kg）", "txt", size=2.1, weight="bold", anchor="start")
    svg.mtext(108, 19, [
        "空车 653 kg：344 / 309",
        "满载 250+180：495 / 588",
        "满载 310+180：521 / 622",
        "后轴 >600 时：电池前移",
        "150–250，或精料仓前移 100",
    ], "notetxt", size=1.75, lh=5.2)

    # ============ D-D 俯视（1:25） ============
    s = 0.04
    top = View(svg, s, 75, 84, ysign=-1)

    # 料槽内沿（现场）
    top.line(-1500, 1230, 1500, 1230, "phantom")
    svg.text(top.X(1420), top.Y(1180), "料槽内沿 z=1230", "small", size=1.6, anchor="end", rot=-90)

    # 底盘 / 电池 / 电控
    top.rect(-1250, -350, 1250, 350, "med", fill="url(#hatch2)")
    top.rect(-700, -475, 1300, 475, "phantom")
    top.rect(-400, -300, 600, 300, "hid")
    top.rect(650, -175, 1150, 175, "hid")
    svg.text(top.X(1000), top.Y(0), "电控箱", "small", size=1.7)

    # 车轮与车轴
    for wx in (-AXLE_X, AXLE_X):
        for wz in (-TRACK_Z, TRACK_Z):
            top.rect(wx - WHEEL_R, wz - WHEEL_W / 2, wx + WHEEL_R, wz + WHEEL_W / 2,
                     "thin", fill="#e6ebee", rx=1.0)
        top.line(wx, -TRACK_Z, wx, TRACK_Z, "cen")
        center_mark(svg, top.X(wx), top.Y(-TRACK_Z), 2.2)
        center_mark(svg, top.X(wx), top.Y(TRACK_Z), 2.2)

    # 精料仓 + 称重
    top.rect(-1300, -300, -700, 300, "vis", fill="url(#conc)")
    top.rect(-1240, -240, -760, 240, "thin")
    for cx, cz in ((-1260, -260), (-1260, 260), (-740, 0)):
        top.circle(cx, cz, 30, "med", fill="#f0c07a")
    # 绞龙
    top.line(-1000, 0, -820, 420, "med")
    top.line(-820, 420, -820, BELT_Z1, "med")
    top.line(-870, 420, -770, 420, "thin")
    top.circle(-820, BELT_Z1, 75, "med", fill="#f7edc9")

    # 侧带
    top.rect(-620, BELT_Z0, -120, BELT_Z1, "med", fill="#e3f1ef")
    for k in range(8):
        zz = BELT_Z0 + 45 + k * 105
        if zz < BELT_Z1 - 25:
            top.line(-610, zz, -130, zz, "thin")
    # 名称
    svg.text(top.X(-370), top.Y(960), "侧带", "small", size=1.7, rot=-90)
    svg.text(top.X(-880), top.Y(820), "绞龙 Φ125", "small", size=1.7, rot=-90)

    # 重心
    top.circle(-70, 0, 55, "cen")
    top.line(-125, 0, -15, 0, "cen")
    top.line(-70, -55, -70, 55, "cen")
    top.text(-70, -3, "G", "txt", size=2.0, weight="bold")

    svg.text(75, 53.0, "D-D 底盘 / 精料仓俯视（箱体双点划线）", "viewtitle", size=2.9)
    svg.text(75, 57.0, "1:25 · 轴距 1640 · 轮距 940 · 底盘宽 700", "small")

    dim_h(svg, top.X(-700), top.X(1300), 143, "2000", ref1=top.Y(475), ref2=top.Y(475))
    dim_h(svg, top.X(-AXLE_X), top.X(AXLE_X), 149, "1640", ref1=top.Y(470), ref2=top.Y(470))
    dim_h(svg, top.X(-1355), top.X(1355), 155, "2710", ref1=top.Y(555), ref2=top.Y(555))
    dim_v(svg, top.Y(-470), top.Y(470), 135, "940", ref1=top.X(820), ref2=top.X(820))
    dim_v(svg, top.Y(-555), top.Y(555), 141, "1110", ref1=top.X(1300), ref2=top.X(1300))
    dim_v(svg, top.Y(-350), top.Y(350), 147, "700", ref1=top.X(1250), ref2=top.X(1250))

    balloon(svg, 8, top.X(-1000), top.Y(-240), 17, 69)
    balloon(svg, 9, top.X(-820), top.Y(420), 27, 96)
    balloon(svg, 14, top.X(-740), top.Y(0), 17, 80)

    # ============ E-E 精料仓横剖（1:10） ============
    s = 0.1
    ee = View(svg, s, 318, 160)

    # 地面 / 车架
    ground(svg, 278, 358, 160)
    ee.rect(-350, 300, 350, 460, "med", fill="url(#hatch2)")
    # 锥斗穿底盘开孔（孔 z=-250..250）
    ee.rect(-260, 300, 260, 460, "", fill="#ffffff")
    ee.line(-260, 300, -260, 460, "thin")
    ee.line(260, 300, 260, 460, "thin")

    # 仓体
    ee.rect(-300, 500, -275, 1220, "med", fill="url(#hatch)")
    ee.rect(275, 500, 300, 1220, "med", fill="url(#hatch)")
    ee.rect(-275, 500, 275, 1220, "", fill="url(#conc)")
    # 锥斗
    ee.poly([(-275, 500), (275, 500), (75, 300), (-75, 300)], "", fill="url(#conc)", close=True)
    ee.line(-300, 500, -75, 300, "med")
    ee.line(300, 500, 75, 300, "med")
    ee.line(-275, 500, -75, 300, "thin")
    ee.line(275, 500, 75, 300, "thin")
    ee.line(-75, 300, 75, 300, "med")
    # 绞龙
    ee.circle(0, 360, 62.5, "med", fill="#dfe7eb")
    ee.circle(0, 360, 40, "thin")
    # 称重模块
    for cz in (-290, 290):
        ee.rect(cz - 30, 460, cz + 30, 500, "med", fill="#f0c07a")
    # 仓盖
    ee.rect(-310, 1220, 310, 1260, "med", fill="#eef2f4")
    ee.line(-150, 1240, 150, 1240, "thin")

    svg.text(318, 27, "E-E 精料仓横剖（x=-1000，向 -X 看）", "viewtitle", size=2.9)
    svg.text(318, 31, "1:10 · 3 点称重 · 锥斗穿底盘", "small")

    dim_v(svg, ee.Y(0), ee.Y(1220), 376, "1220", ref1=ee.X(300), ref2=ee.X(300))
    dim_h(svg, ee.X(-300), ee.X(300), 166, "600", ref1=ee.Y(500), ref2=ee.Y(500))
    dim_h(svg, ee.X(-350), ee.X(350), 172, "700", ref1=ee.Y(300), ref2=ee.Y(300))
    leader(svg, ee.X(0), ee.Y(360), 356, 150, "Φ125 绞龙", anchor="start", size=1.75)
    leader(svg, ee.X(290), ee.Y(480), 356, 140, "3×100 kg 称重", anchor="start", size=1.75)

    # ============ 轴荷表 ============
    tbl(svg, 12, 182, [
        ("工况", 46, "start"), ("总重 kg", 30, "middle"),
        ("前轴 kg", 30, "middle"), ("后轴 kg", 30, "middle"),
    ], [
        ("空车", "653", "344", "309"),
        ("满载 250+180", "1083", "495", "588"),
        ("满载 310+180", "1143", "521", "622"),
        ("设计上限", "1200", "≤560", "≤600"),
    ], rh=6.2, size=1.8)
    svg.text(12, 178, "轴荷（G x≈-70，y≈900）", "txt", size=2.2, weight="bold", anchor="start")

    # ============ 说明 ============
    svg.text(178, 182, "底盘与行走", "txt", size=2.2, weight="bold", anchor="start")
    svg.mtext(178, 188, [
        "1. 车架 40×60×3 方管焊接，2.5×0.7；",
        "   电池 48V/100Ah 居中偏后。",
        "2. 4×440×170 实心胎，额定 ≥600 kg/轮；",
        "   轴距 1640，轮距 940，最小离地 120。",
        "3. 后轮 2×0.8 kW 轮毂减速电机，",
        "   电磁失电制动 + 再生制动，0.6 m/s。",
        "4. 精料仓 3 点称重（后 2 + 前 1），",
        "   锥斗穿底盘开孔，孔边 40×40 补强。",
        "5. 后轴 622 > 600：量产前电池前移 200",
        "   或精料仓前移 100，复称轴荷。",
        "6. 绞龙 Φ125，仓底→z=1320 下料口，",
        "   出口与侧带错开 450，同落入料槽。",
    ], "notetxt", size=1.75, lh=4.55)

    frame(svg, 3, 4, "精料仓、底盘与轴荷", "1:25 / 1:10 / 1:50", "FC-03")
    return svg.render("FC-03 精料仓、底盘与轴荷")


if __name__ == "__main__":
    data = sheet3()
    path = os.path.join(OUT, "03-chassis.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    print("wrote", path, len(data))
