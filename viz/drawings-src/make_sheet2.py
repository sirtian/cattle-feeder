# -*- coding: utf-8 -*-
"""FC-02 粗料箱与卸料机构"""
import os
from make_drawings import (
    SVG, View, n, ground, dim_h, dim_v, leader, balloon, frame,
    BELT_Z0, BELT_Z1, BELT_Y0, BELT_Y1,
    TROUGH_Z0, TROUGH_Z1, TROUGH_RIM, FEED_Y,
    AXLE_X, WHEEL_R, OUT,
)


def belt_geom():
    dz, dy = BELT_Z1 - BELT_Z0, BELT_Y1 - BELT_Y0
    L = (dz * dz + dy * dy) ** 0.5
    return (dz / L, dy / L), (-dy / L, dz / L), L


def sheet2():
    svg = SVG()
    bb = View(svg, 0.1, 62, 182)

    # ---- 地面 / 料槽（现场） ----
    ground(svg, 5, 248, 182)
    for z1, z2 in ((TROUGH_Z0, 1230), (1670, TROUGH_Z1)):
        bb.rect(z1, 0, z2, TROUGH_RIM, "phantom")
    bb.rect(1230, 200, 1670, 250, "phantom")
    bb.line(1230, FEED_Y, 1670, FEED_Y, "phantom")
    svg.text(bb.X(1450), bb.Y(330), "料槽（现场条件）", "small", size=1.9, rot=-90)

    # ---- 底盘 / 电池 ----
    bb.rect(-350, 300, 350, 460, "med", fill="url(#hatch2)")
    bb.rect(-300, 120, 300, 360, "hid")
    svg.text(bb.X(0), bb.Y(250), "48V 电池（藏于底盘）", "small", size=1.8)

    # ---- 箱体截面 ----
    bb.rect(-475, 460, -430, 1560, "med", fill="url(#hatch)")
    bb.rect(430, 800, 475, 1560, "med", fill="url(#hatch)")
    bb.rect(430, 460, 475, 600, "med", fill="url(#hatch)")
    bb.rect(-475, 460, 475, 520, "med", fill="url(#hatch)")
    bb.rect(-430, 520, 430, 565, "med", fill="#dfe7eb")
    bb.line(-430, 542, 430, 542, "thin")
    bb.poly([(-430, 565), (430, 565), (430, 1300), (300, 1540), (-430, 1540)],
            "thin", fill="url(#straw)", close=True)

    # ---- 侧卸门 ----
    bb.rect(475, 585, 535, 815, "med", fill="#f7e6d2")
    bb.rect(475, 600, 535, 800, "vis", fill="#ffffff")
    bb.rect(505, 580, 530, 820, "med", fill="#e8edf0")
    bb.rect(505, 680, 530, 920, "hid")
    bb.line(505, 580, 505, 820, "thin")
    bb.line(530, 580, 530, 820, "thin")
    bb.line(535, 585, 535, 815, "thin")
    bb.rect(528, 900, 552, 1140, "med", fill="#dfe7eb")
    bb.line(540, 900, 540, 820, "med")
    bb.line(535, 600, 560, 655, "vis")
    bb.line(535, 612, 560, 667, "thin")

    # ---- 横向挡边皮带 ----
    d, nrm, L = belt_geom()
    z0, y0, z1, y1 = BELT_Z0, BELT_Y0, BELT_Z1, BELT_Y1
    top0 = (z0 + nrm[0] * 25, y0 + nrm[1] * 25)
    bot0 = (z0 - nrm[0] * 25, y0 - nrm[1] * 25)
    top1 = (z1 + nrm[0] * 25, y1 + nrm[1] * 25)
    bot1 = (z1 - nrm[0] * 25, y1 - nrm[1] * 25)
    bb.poly([top0, top1, bot1, bot0], "med", fill="#e3f1ef", close=True)
    bb.circle(z0, y0, 45, "med", fill="#dfe7eb")
    bb.circle(z1, y1, 45, "med", fill="#dfe7eb")
    for k in range(1, 8):
        t = (40 + k * 105) / L
        if t >= 0.97:
            continue
        cz, cy = z0 + d[0] * L * t, y0 + d[1] * L * t
        pts = []
        for sgn in (-1, 1):
            for h in (25, 95):
                pts.append((cz + sgn * d[0] * 22.5 + nrm[0] * h,
                            cy + sgn * d[1] * 22.5 + nrm[1] * h))
        pts = [pts[0], pts[1], pts[3], pts[2]]
        bb.poly(pts, "med", fill="#9fb3bf", close=True)
    lip_end = (z1 + 150, y1 - 75)
    bb.line(z1, y1, lip_end[0], lip_end[1], "vis")
    bb.line(z1, y1 - 30, lip_end[0], lip_end[1] - 30, "thin")
    bb.line(600, 600, 980, 750, "thin")
    bb.rect(560, 455, 660, 555, "hid")
    svg.text(bb.X(610), bb.Y(505), "侧带电机", "small", size=1.7, rot=-90)

    # ---- 标注 ----
    svg.text(bb.X(-250), 19, "B-B 剖视（x=-370，向 +X 看）", "viewtitle")
    svg.text(bb.X(-250), 23.2, "1:10 · 侧卸门 / 横向挡边皮带 / 料槽", "small")

    dim_h(svg, bb.X(1230), bb.X(BELT_Z1), 100, "100", ref1=bb.Y(700), ref2=bb.Y(BELT_Y1))
    dim_v(svg, bb.Y(0), bb.Y(1560), 243, "1560", ref1=bb.X(475), ref2=bb.X(475))

    ax, ay = bb.X(BELT_Z1), bb.Y(BELT_Y1)
    svg.line(ax - 18, ay, ax, ay, "dim")
    svg.path("M %.2f %.2f A 12 12 0 0 0 %.2f %.2f" % (ax - 12, ay, ax - 11.1, ay - 4.6), "dim")
    svg.text(ax - 10, ay - 5.5, "23°", "dimtxt", size=2.2)

    leader(svg, bb.X(520), bb.Y(700), 150, 38, "侧卸门 500×200 · 开度 40–100", anchor="start", size=1.75)
    leader(svg, bb.X(1060), bb.Y(870), 150, 48, "横向挡边带 500 · 挡边 50 · 隔板 70@105", anchor="start", size=1.75)
    leader(svg, bb.X(BELT_Z0), bb.Y(BELT_Y0), 150, 58, "带尾距箱壁 85 · 柔性导裙密封", anchor="start", size=1.75)
    svg.text(bb.X(1420), bb.Y(760), "料槽（现场条件）", "small", size=1.7, rot=-90)

    # ---- A-A 剖视 ----
    aa = View(svg, 0.05, 330, 120)
    ground(svg, 258, 404, 120)
    for wx in (-AXLE_X, AXLE_X):
        aa.circle(wx, WHEEL_R, WHEEL_R, "hid")
    aa.rect(-1250, 300, 1250, 460, "med", fill="url(#hatch2)")
    aa.rect(-400, 120, 600, 360, "hid")
    aa.rect(1250, 460, 1300, 1560, "med", fill="url(#hatch)")
    aa.rect(-700, 460, -650, 1560, "med", fill="url(#hatch)")
    aa.rect(-700, 460, 1300, 520, "med", fill="url(#hatch)")
    aa.rect(-650, 520, 1250, 565, "med", fill="#dfe7eb")
    aa.line(-650, 542, 1250, 542, "thin")
    aa.poly([(-650, 565), (1250, 565), (1250, 1540), (-650, 1540)],
            "thin", fill="url(#straw)", close=True)
    aa.rect(-1300, 500, -700, 1220, "vis", fill="#fbfcfc")
    aa.poly([(-1280, 520), (-720, 520), (-720, 1195), (-1280, 1195)], "thin", fill="url(#conc)", close=True)
    aa.poly([(-1300, 500), (-1220, 290), (-780, 290), (-700, 500)], "vis", fill="#fbfcfc", close=True)
    aa.poly([(-1250, 500), (-1200, 380), (-800, 380), (-750, 500)], "thin", fill="url(#conc)", close=True)
    aa.rect(-1290, 1220, -710, 1260, "med", fill="#eef2f4")
    for lx in (-1260, -740):
        aa.rect(lx, 460, lx + 34, 500, "med", fill="#dfe7eb")
    for lx in (-500, 1000):
        aa.rect(lx - 35, 448, lx + 35, 462, "med", fill="#f0c07a")
    aa.rect(-1000, 480, -970, 505, "med", fill="#f0c07a")
    aa.circle(-1000, 500, 55, "med", fill="#dfe7eb")

    svg.text(330, 18, "A-A 剖视（z=0，向 +Z 看）", "viewtitle")
    svg.text(330, 22.2, "1:20 · 箱体 / 精料仓 / 称重", "small")

    dim_h(svg, aa.X(-1355), aa.X(1355), 140, "2710", ref1=120, ref2=120)
    dim_h(svg, aa.X(-700), aa.X(1300), 135, "2000", ref1=120, ref2=120)
    dim_h(svg, aa.X(-1300), aa.X(-700), 130, "600", ref1=120, ref2=120)
    dim_h(svg, aa.X(-820), aa.X(820), 146, "1640", ref1=120, ref2=120)
    dim_v(svg, 120, aa.Y(1560), 258, "1560", ref1=aa.X(1300), ref2=aa.X(1300))

    balloon(svg, 4, aa.X(300), aa.Y(1450), 350, 35)
    balloon(svg, 5, aa.X(800), aa.Y(542), 385, 88)
    balloon(svg, 8, aa.X(-1000), aa.Y(1100), 270, 58)
    balloon(svg, 9, aa.X(-1000), aa.Y(500), 270, 100)
    balloon(svg, 14, aa.X(1000), aa.Y(455), 392, 96)

    # ---- C 详图 ----
    s = 1 / 6
    det = View(svg, s, 22 - 440 * s, 200 + 1000 * s)
    det.rect(440, 540, 475, 1000, "med", fill="url(#hatch)")
    det.rect(475, 585, 535, 815, "med", fill="#f7e6d2")
    det.rect(475, 600, 535, 800, "vis", fill="#ffffff")
    det.rect(505, 580, 530, 820, "med", fill="#e8edf0")
    det.rect(505, 680, 530, 920, "hid")
    det.line(535, 585, 535, 815, "thin")
    det.rect(528, 900, 552, 1000, "med", fill="#dfe7eb")
    det.line(540, 900, 540, 820, "med")
    det.line(535, 600, 560, 655, "vis")
    det.line(535, 612, 560, 667, "thin")
    d, nrm, L = belt_geom()
    y720 = BELT_Y0 + (720 - BELT_Z0) * (BELT_Y1 - BELT_Y0) / (BELT_Z1 - BELT_Z0)
    det.poly([(BELT_Z0 + nrm[0] * 25, BELT_Y0 + nrm[1] * 25),
              (720 + nrm[0] * 25, y720 + nrm[1] * 25),
              (720 - nrm[0] * 25, y720 - nrm[1] * 25),
              (BELT_Z0 - nrm[0] * 25, BELT_Y0 - nrm[1] * 25)],
             "med", fill="#e3f1ef", close=True)
    det.circle(BELT_Z0, BELT_Y0, 45, "med", fill="#dfe7eb")
    for k in range(2):
        tz = 600 + k * 105
        ty = BELT_Y0 + (tz - BELT_Z0) * (BELT_Y1 - BELT_Y0) / (BELT_Z1 - BELT_Z0)
        det.poly([(tz - 22, ty + 25), (tz + 22, ty + 25), (tz + 22, ty + 95), (tz - 22, ty + 95)],
                 "med", fill="#9fb3bf", close=True)

    svg.text(22, 193, "C 详图（侧卸门 / 带尾）", "viewtitle")
    svg.text(22, 197.2, "1:6", "small")
    dim_v(svg, det.Y(600), det.Y(800), det.X(545), "200")
    dim_h(svg, det.X(475), det.X(BELT_Z0), det.Y(830), "85")
    leader(svg, det.X(517), det.Y(760), 74, 218, "门板 520×240", anchor="start", size=1.8)
    leader(svg, det.X(517), det.Y(900), 74, 228, "开度 40–100", anchor="start", size=1.8)
    leader(svg, det.X(560), det.Y(600), 74, 238, "柔性导裙 / 带尾滚筒 Φ90", anchor="start", size=1.8)
    leader(svg, det.X(650), det.Y(680), 74, 248, "横隔板 70 @ 105", anchor="start", size=1.8)
    leader(svg, det.X(620), det.Y(640), 74, 258, "带面 50 / 挡边 50", anchor="start", size=1.8)

    # ---- 说明 ----
    nx, ny = 120, 205
    svg.text(nx, ny, "卸料顺序与要点", "txt", size=2.4, weight="bold", anchor="start")
    notes = [
        "1. 链板把粗料推向后端，侧卸门开度 40–100 粗调流量；",
        "   门洞 500×200（宽×高），门板电动推杆升降。",
        "2. 带尾置于门洞下方，门框与带尾间柔性导裙密封；",
        "   门板与皮带不干涉（带尾距箱壁 85）。",
        "3. 横向挡边带 500 宽，带长 855（投影 770），仰角 23°；",
        "   挡边 50，横隔板 70@105，带速 0.3–0.5 m/s。",
        "4. 带端越过料槽内沿 100，落料高差 250–350；",
        "   槽内料面低于槽沿约 150。",
        "5. 每站先粗 10–15 kg（3 点称重），关门后侧带空转",
        "   2–3 s 清料；再下精料 10–12 kg。",
        "6. 槽沿/槽宽为现场条件；实测后冻结带长/仰角。",
        "7. 精料仓锥斗坐入底盘开孔，四周 40×40 方管补强；",
        "   三维演示未示开孔。",
        "8. 3 点称重传感器嵌入底盘安装座，箱底与底盘间隙",
        "   10–15；本图按贴合示意。",
    ]
    svg.mtext(nx, ny + 5.5, notes, "notetxt", size=1.85, lh=4.1)

    frame(svg, 2, 4, "粗料箱与卸料机构", "1:10 / 1:20 / 1:6", "FC-02")
    return svg.render("FC-02 粗料箱与卸料机构")


if __name__ == "__main__":
    data = sheet2()
    path = os.path.join(OUT, "02-discharge.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    print("wrote", path, len(data))
