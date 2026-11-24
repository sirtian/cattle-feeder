# -*- coding: utf-8 -*-
"""P10 全宽卸料方案对比：现状 / 单带下置 / 后横送"""
import os
from make_drawings import SVG, View, arrow, frame, OUT
from p10 import Z_BOX, GATE_X0, GATE_X1, BELT_X0, BELT_X1, BELT_Z0


def panel(svg, v, mode):
    v.rect(-450, -Z_BOX, 835, Z_BOX, "med")
    if mode == "C":
        v.rect(-450, -Z_BOX, 835, -20, "", fill="#f6ddd5")
    for xx in range(-420, 820, 90):
        v.line(xx, -370, xx, 370, "thin")
    # 链板向 -X
    for zz in (-210, 0, 210):
        v.line(650, zz, 540, zz, "vis")
        arrow(svg, v.X(540), v.Y(zz), "left")

    if mode == "C":
        v.rect(GATE_X0, Z_BOX, GATE_X1, Z_BOX + 15, "med", fill="#f7e6d2")
        v.rect(BELT_X0, BELT_Z0, BELT_X1, 600, "med", fill="#e3f1ef")
        for xx in (-380, -300, -220, -140):
            v.line(xx, 380, xx, 455, "leader")
            arrow(svg, v.X(xx), v.Y(455), "down")
        v.text(-230, -215, "死区 25–40%", "txt", size=1.9)
    elif mode == "A":
        # 带尾在 -Z，带从箱下穿过，全宽后门在 x=-50
        v.rect(BELT_X0, -Z_BOX, BELT_X1, 600, "med", fill="#e3f1ef")
        v.line(-50, -Z_BOX, -50, Z_BOX, "vis")
        v.line(-50, -Z_BOX, -50, Z_BOX, "vis")
        for xx in (-380, -300, -220, -140):
            v.line(xx, -300, xx, 520, "vis")
            arrow(svg, v.X(xx), v.Y(520), "down")
    else:
        # 后横送 400×780，向 +Z，接现有侧门
        v.rect(GATE_X0, -Z_BOX, GATE_X1, Z_BOX, "med", fill="#e3f1ef")
        for xx in (-380, -300, -220, -140):
            v.line(xx, -340, xx, 340, "vis")
            arrow(svg, v.X(xx), v.Y(340), "down")
        v.rect(GATE_X0, Z_BOX, GATE_X1, Z_BOX + 15, "med", fill="#f7e6d2")
        v.rect(BELT_X0, BELT_Z0, BELT_X1, 600, "med", fill="#e3f1ef")


def sheet():
    svg = SVG()
    svg.text(15, 20, "全宽卸料：为什么选 A（单带下置 + 全宽后门）", "viewtitle", size=3.4, anchor="start")
    svg.text(15, 24, "现状是纵向链板 + 侧壁门：链板只沿 -X 推，没有 +Z 分量；远离门的 -Z 侧是死区。", "small", size=1.8, anchor="start")

    s = 1 / 12
    pc = View(svg, s, 55, 80, ysign=-1)
    pa = View(svg, s, 175, 80, ysign=-1)
    pb = View(svg, s, 295, 80, ysign=-1)

    panel(svg, pc, "C")
    panel(svg, pa, "A")
    panel(svg, pb, "B")

    svg.text(17.5, 41, "C 现状：纵向链板 + 侧门", "txt", size=2.1, weight="bold", anchor="start")
    svg.text(137.5, 41, "A 单带下置 + 全宽后门（已选）", "txt", size=2.1, weight="bold", anchor="start")
    svg.text(257.5, 41, "B 后横送 + 现有侧门", "txt", size=2.1, weight="bold", anchor="start")

    svg.text(17.5, 136, "料只沿 X 走，门只开在 +Z 壁", "small", size=1.35, anchor="start")
    svg.text(137.5, 136, "带尾 z=-390；x=-50 全宽门", "small", size=1.35, anchor="start")
    svg.text(257.5, 136, "横送把 -Z 料送到 +Z 门；箱容保留", "small", size=1.35, anchor="start")

    # ---- 说明 ----
    svg.text(15, 150, "为什么 C 不能全出", "txt", size=2.1, weight="bold", anchor="start")
    svg.mtext(15, 156, [
        "1. 链板刮板横跨箱宽、沿 -X 运动，没有 +Z 分量；",
        "   料只能被推到后壁，不能横移到 +Z 侧门。",
        "2. 门是 +Z 壁上的 400×180 洞，只能取 +Z 边界层；",
        "   5 cm 秸秆休止角约 45°，跨 390 宽差要 390 高差，",
        "   箱高 900、门洞 500–680，-Z 侧后角料翻不过去。",
        "3. 估算残留 25–40%，且混入下一车；15 天无人不可接受。",
        "   必须做 1:1 透明试验段实测，不能只靠估算。",
    ], "notetxt", size=1.55, lh=4.6)

    svg.text(200, 150, "A / B 对比", "txt", size=2.1, weight="bold", anchor="start")
    # 表
    x0, y0, rh = 200, 155, 6.2
    widths = [36, 24, 44, 24, 52]
    heads = ["方案", "残留", "箱容", "驱动", "改动"]
    rows = [
        ("C 现状", "25–40%", "保留", "1", "—"),
        ("A 单带下置", "<5%", "后 400 损失", "1", "带加长、门改后"),
        ("B 后横送", "<5%", "保留", "2", "+横送、侧门保留"),
    ]
    W = sum(widths)
    svg.rect(x0, y0, W, rh * 4, "med", fill="none")
    svg.rect(x0, y0, W, rh, "", fill="#e9eff3")
    cx = x0
    for w, h in zip(widths, heads):
        svg.line(cx, y0, cx, y0 + rh * 4, "thin")
        svg.text(cx + 1.2, y0 + rh * 0.7, h, "txt", size=1.45, anchor="start")
        cx += w
    for i, row in enumerate(rows):
        ry = y0 + rh * (i + 1)
        svg.line(x0, ry, x0 + W, ry, "thin")
        cx = x0
        for w, val in zip(widths, row):
            svg.text(cx + 1.2, ry + rh * 0.7, val, "notetxt", size=1.4, anchor="start")
            cx += w

    svg.text(200, 186, "已选 A · 实施要点", "txt", size=2.1, weight="bold", anchor="start")
    svg.mtext(200, 192, [
        "P10 按 A 实施：400 宽带从 z=-390 水平穿到 z=430，",
        "再 33° 抬升；全宽后门 780×180 计量。箱容 0.62 m³",
        "（≈74 kg，10 头 1.6 天）；P50 若用 A，箱体加长",
        "400 保 250 kg。先做 2 m 透明试验段测残留/搭桥。",
    ], "notetxt", size=1.5, lh=4.5)

    frame(svg, 3, 3, "全宽卸料方案（已选 A）", "1:12", "FC-P10-03A",
          note="已选 A · 实施", project="智能养牛 · 10 头原型验证")
    return svg.render("P10 全宽卸料方案对比")


if __name__ == "__main__":
    data = sheet()
    path = os.path.join(OUT, "p10-04-full-discharge.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    print("wrote", path, len(data))
