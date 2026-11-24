# -*- coding: utf-8 -*-
"""P10-A 卸料原理：全宽后门 + 箱底接料带"""
import os
from make_drawings import SVG, View, dim_h, dim_v, leader, frame, arrow, OUT
from p10 import (
    Z_BOX, GATE_X, GATE_Y0, GATE_Y1, TROUGH_X0, TROUGH_X1,
    BELT_X0, BELT_X1, BELT_TAIL_Z, BELT_KNEE_Z, BELT_TIP_Z,
    BELT_Y, BELT_TIP_Y, TROUGH_Z0, TROUGH_Z1, TROUGH_RIM, FEED_Y,
)


def sheet():
    svg = SVG()
    svg.text(15, 20, "全宽后门怎么把整箱粗料卸干净？", "viewtitle", size=3.4, anchor="start")
    svg.text(15, 24, "A 方案：链板推到 x=-50 全宽门 → 料落进箱底接料带 → 带水平收集全宽 → 33° 抬升越槽沿。", "small", size=1.75, anchor="start")

    # ================= 平面 =================
    s = 1 / 12
    v = View(svg, s, 70, 95, ysign=-1)
    svg.text(30, 36, "A 平面：全宽落料（1:12）", "txt", size=2.1, weight="bold", anchor="start")

    v.rect(-450, -Z_BOX, 835, Z_BOX, "med")
    v.rect(GATE_X, -370, 815, 370, "thin", fill="url(#straw)")
    for xx in range(-20, 820, 90):
        v.line(xx, -360, xx, 360, "thin")
    for zz in (-300, -100, 100, 300):
        v.line(720, zz, 620, zz, "vis")
        arrow(svg, v.X(620), v.Y(zz), "left")
    v.rect(TROUGH_X0, -370, TROUGH_X1, 370, "thin", fill="#dfe7eb")
    v.rect(BELT_X0, BELT_TAIL_Z, BELT_X1, 700, "med", fill="#e3f1ef")
    for zz in range(-340, 680, 90):
        v.line(BELT_X0 + 8, zz, BELT_X1 - 8, zz, "thin")
    for zz in (-280, -80, 120, 320):
        v.line(-250, zz, -250, zz + 70, "vis")
        arrow(svg, v.X(-250), v.Y(zz + 70), "down")
    v.line(GATE_X, -Z_BOX, GATE_X, Z_BOX, "vis")
    v.rect(GATE_X - 12, -Z_BOX, GATE_X, Z_BOX, "med", fill="#f7e6d2")
    v.line(-450, 700, -50, 700, "thin")
    svg.text(v.X(-250), 158, "至 z=1050（断）", "small", size=1.3)

    v.text(390, 0, "链板 → -X", "small", size=1.4, rot=-90)
    v.text(-250, 470, "带 → +Z", "small", size=1.4, rot=-90)
    svg.text(30, 150, "门宽 780，覆盖整个箱宽；-Z 侧不再有死区", "small", size=1.4, anchor="start")

    # ================= 门/槽剖面 =================
    g = View(svg, 1 / 7, 175, 150)
    svg.text(150, 18, "B 门/槽剖面（1:7）", "txt", size=2.1, weight="bold", anchor="start")
    g.rect(-50, 530, 100, 565, "med", fill="#dfe7eb")
    g.poly([(-50, 565), (100, 565), (100, 800), (-50, 800)], "thin", fill="url(#straw)", close=True)
    g.rect(-150, 400, -50, 530, "thin", fill="#e3f1ef")
    g.line(-150, 400, -50, 400, "med")
    g.rect(-50, 530, -35, 710, "med", fill="#e7edf0")
    g.line(-42, 710, -42, 820, "med")
    g.rect(-52, 820, -32, 900, "med", fill="#dfe7eb")
    g.line(-80, 540, -100, 470, "leader")
    arrow(svg, g.X(-100), g.Y(470), "down")

    dim_v(svg, g.Y(530), g.Y(710), 192, "180")
    dim_v(svg, g.Y(710), g.Y(820), 198, "推杆")
    dim_h(svg, g.X(-50), g.X(-20), 100, "30–80", ref1=g.Y(530), ref2=g.Y(560))
    leader(svg, g.X(-60), g.Y(480), 192, 62, "落差 105", anchor="start", size=1.4)
    leader(svg, g.X(-110), g.Y(430), 192, 75, "带面 425", anchor="start", size=1.4)

    # ================= 配速 =================
    svg.text(250, 36, "配速（P10-A）", "txt", size=2.1, weight="bold", anchor="start")
    svg.mtext(250, 42, [
        "Q门 = 0.78×0.06×0.07×0.4",
        "     ≈ 1.3 L/s ≈ 0.16 kg/s",
        "2.2 kg 粗料 ≈ 14 s/头",
        "Q带 = 0.58 kg/s ≈ 3.6×Q门",
        "→ 带不会堵，门不会憋",
    ], "notetxt", size=1.45, lh=4.6)

    svg.text(250, 70, "为什么能全出", "txt", size=2.1, weight="bold", anchor="start")
    svg.mtext(250, 76, [
        "1. 门在箱后、横跨 780 全宽；链板把每一",
        "   条 Z 截面的料都推到门唇，没有侧向死区。",
        "2. 门后 400 是落料槽，槽底就是带面；",
        "   料靠重力落下 105，不靠“爬坡”。",
        "3. 带在箱底水平段 820 全宽接料，再 33°",
        "   抬升；带速 ≥3×门出料，不会积料。",
        "4. 门板下缘 30–80 定切片；失重计量到量",
        "   即停链、关门，带再清 2–3 s。",
    ], "notetxt", size=1.45, lh=4.5)

    # ================= 时序 =================
    svg.text(15, 170, "一个停靠点的动作顺序", "txt", size=2.1, weight="bold", anchor="start")
    y = 186
    svg.line(25, y, 395, y, "med")
    nodes = [
        (35, "① 到位", "停稳/抱闸", True),
        (95, "② 带启动", "先转 0.5 s", False),
        (155, "③ 门开", "30–80", True),
        (215, "④ 链板", "慢速", False),
        (275, "⑤ 失重", "3 点称重", True),
        (335, "⑥ 达标", "链停→门关", False),
        (388, "⑦ 带清", "2–3 s", True),
    ]
    for x, t1, t2, up in nodes:
        svg.circle(x, y, 1.8, "med", fill="#ffffff")
        if up:
            svg.text(x, y - 6.5, t1, "txt", size=1.5)
            svg.text(x, y - 3, t2, "small", size=1.2)
        else:
            svg.text(x, y + 6.5, t1, "txt", size=1.5)
            svg.text(x, y + 10, t2, "small", size=1.2)

    svg.text(15, 205, "动作 / 保护", "txt", size=2.1, weight="bold", anchor="start")
    svg.mtext(15, 211, [
        "1. 先带后链：带先转 0.5 s，门再开，链板最后启动；停机顺序相反。",
        "2. 带停时链板不能长时间转，否则门区积压、下次启动过载。",
        "3. 5 s 无失重 → 链板反转 1 s、门再开 +10 mm；3 次仍不下 → 报警。",
        "4. 仍搭桥：门内加 Ø200 拨料星轮（0.18 kW，6 指）或门唇加振动器。",
        "5. 箱容 0.62 m³（74 kg，10 头 1.6 天）；试验按 2 天装，留 30% 余量。",
    ], "notetxt", size=1.55, lh=4.6)

    frame(svg, 3, 3, "全宽卸料原理", "1:12 / 1:7", "FC-P10-03A",
          project="智能养牛 · 10 头原型验证")
    return svg.render("P10-A 全宽卸料原理")


if __name__ == "__main__":
    data = sheet()
    path = os.path.join(OUT, "p10-03a-principle.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    print("wrote", path, len(data))
