# -*- coding: utf-8 -*-
"""P10 十头原型车（A 方案）· 总图"""
import os
from make_drawings import SVG, View, ground, dim_h, dim_v, leader, balloon, frame, arrow, OUT
from p10 import (
    wheel10, tbl, belt_y,
    X_MIN, X_MAX, Y_ANT, Y_BOX, Y_FLOOR_BOT, Y_FLOOR, Y_SLAT,
    X_BOX0, X_BOX1, Z_BOX, TROUGH_X0, TROUGH_X1, GATE_X, GATE_Y0, GATE_Y1,
    BELT_X0, BELT_X1, BELT_TAIL_Z, BELT_KNEE_Z, BELT_TIP_Z,
    BELT_Y, BELT_TIP_Y, BELT_ANG,
    CONC_X0, CONC_X1, CONC_Z, CONC_TOP, TROUGH_Z0, TROUGH_Z1,
    TROUGH_RIM, FEED_Y, WHEEL_R, WHEEL_W, AXLE_X, TRACK_Z, CHASSIS_Z,
    BAT_X0, BAT_X1, AUGER_X,
)


def sheet1():
    svg = SVG()
    s = 1 / 15
    side = View(svg, s, 85, 125)
    top = View(svg, s, 85, 180, ysign=-1)
    front = View(svg, s, 330, 125, xsign=-1)

    # ================= 侧视 =================
    ground(svg, 12, 160, 125)
    wheel10(side, -AXLE_X)
    wheel10(side, AXLE_X)

    side.rect(-835, 260, 835, 380, "med", fill="url(#hatch2)")
    side.rect(BAT_X0, 100, BAT_X1, 300, "hid")
    side.rect(X_BOX0, Y_FLOOR_BOT, X_BOX1, Y_BOX, "vis", fill="#f8fafb")
    side.rect(X_BOX0, 1310, X_BOX1, Y_BOX, "thin")
    side.rect(X_BOX0, Y_FLOOR_BOT, X_BOX1, Y_FLOOR, "thin")
    side.rect(TROUGH_X0 + 20, Y_FLOOR, TROUGH_X1 - 20, Y_SLAT, "thin", fill="#dfe7eb")
    side.line(TROUGH_X0 + 20, 548, TROUGH_X1 - 20, 548, "thin")
    for xx in (0, 350, 650):
        side.line(xx, Y_SLAT, xx, 1308, "thin")
    # 后落料槽 / 全宽门（隐藏）
    side.rect(TROUGH_X0, 400, TROUGH_X1, Y_FLOOR_BOT, "hid")
    side.line(GATE_X, GATE_Y0, GATE_X, GATE_Y1, "hid")
    side.line(-150, 400, 790, 400, "hid")
    # 精料仓
    side.rect(CONC_X0, 420, CONC_X1, CONC_TOP, "vis", fill="#fbfcfc")
    side.poly([(CONC_X0, 420), (CONC_X0 + 80, 260), (CONC_X1 - 80, 260), (CONC_X1, 420)],
              "med", fill="#fbfcfc", close=True)
    side.rect(CONC_X0 + 10, CONC_TOP, CONC_X1 - 10, CONC_TOP + 30, "med", fill="#eef2f4")
    for lx in (CONC_X0 + 10, CONC_X1 - 40):
        side.rect(lx, 380, lx + 30, 420, "med", fill="#f0c07a")
    # 箱体称重
    for lx in (-250, 500):
        side.rect(lx - 30, 380, lx + 30, 440, "med", fill="#dfe7eb")
        side.rect(lx - 30, 440, lx + 30, 480, "med", fill="#f0c07a")
    # 保险杠
    for bx in (-925, 835):
        side.rect(bx, 280, bx + 90, 460, "vis", fill="#e8edf0")
        side.line(bx + 45, 300, bx + 45, 440, "thin")
    # 桅杆 / 相机 / 灯 / 天线
    side.rect(800, 1380, 826, 1600, "med")
    side.rect(770, 1540, 880, 1620, "med", fill="#eef2f4")
    side.rect(600, 1390, 700, 1470, "med", fill="#f3e6d8")
    side.line(-900, 1050, -900, 1640, "med")
    side.circle(-900, 1640, 16, "med", fill="#e3f1ef")
    # 重心
    side.circle(-40, 780, 42, "cen")
    side.line(-82, 780, 2, 780, "cen")
    side.line(-40, 738, -40, 822, "cen")
    side.text(-40, 777, "G", "txt", size=2.0, weight="bold")

    svg.text(85, 11.5, "侧视图（非卸料侧，-Z）", "viewtitle", size=2.9)
    svg.text(85, 14.6, "1:15", "small")

    dim_v(svg, 125, side.Y(Y_ANT), 12, "1640", ref1=side.X(-900), ref2=side.X(-900))
    dim_v(svg, 125, side.Y(Y_BOX), 18, "1380", ref1=side.X(835), ref2=side.X(835))
    dim_h(svg, side.X(-AXLE_X), side.X(AXLE_X), 131, "1200", ref1=125, ref2=125)
    dim_h(svg, side.X(X_BOX0), side.X(X_BOX1), 136, "1285", ref1=125, ref2=125)
    dim_h(svg, side.X(-925), side.X(925), 141, "1850", ref1=125, ref2=125)

    side.text(230, 900, "粗料箱 有效 0.62 m³", "small", size=1.6)
    side.text(230, 980, "1.285×0.78×0.90", "small", size=1.4)
    side.text(-642, 760, "精料仓 0.116 m³", "small", size=1.5, rot=-90)

    # ================= 俯视 =================
    top.rect(-1000, TROUGH_Z0, 1000, TROUGH_Z1, "phantom")
    top.line(-1000, TROUGH_Z0, 1000, TROUGH_Z0, "phantom")
    svg.text(top.X(-250), top.Y(1260), "试验槽内沿 z=950 / 沿高 600（10 位×0.75 m）", "small", size=1.55, anchor="start")

    top.rect(-835, -CHASSIS_Z, 835, CHASSIS_Z, "med", fill="url(#hatch2)")
    for wx in (-AXLE_X, AXLE_X):
        for wz in (-TRACK_Z, TRACK_Z):
            top.rect(wx - WHEEL_R, wz - WHEEL_W / 2, wx + WHEEL_R, wz + WHEEL_W / 2,
                     "thin", fill="#e6ebee", rx=1.0)
        top.line(wx, -TRACK_Z, wx, TRACK_Z, "cen")
    top.rect(X_BOX0, -Z_BOX, X_BOX1, Z_BOX, "phantom")
    top.rect(X_BOX0, -Z_BOX, X_BOX1, -370, "thin", fill="#f8fafb")
    top.rect(X_BOX0, 370, X_BOX1, Z_BOX, "thin", fill="#f8fafb")
    top.rect(X_BOX0, -Z_BOX, X_BOX0 + 20, Z_BOX, "thin", fill="#f8fafb")
    top.rect(X_BOX1 - 20, -Z_BOX, X_BOX1, Z_BOX, "thin", fill="#f8fafb")
    # 链板区（x -50..835）
    top.rect(GATE_X, -370, 815, 370, "thin", fill="url(#straw)")
    for xx in range(-20, 820, 90):
        top.line(xx, -360, xx, 360, "thin")
    for zz in (-330, 0, 330):
        top.line(GATE_X + 650, zz, GATE_X + 560, zz, "vis")
        arrow(svg, top.X(GATE_X + 560), top.Y(zz), "left")
    # 后落料槽 + 带（x -450..-50）
    top.rect(TROUGH_X0, -370, TROUGH_X1, 370, "thin", fill="#dfe7eb")
    top.rect(BELT_X0, BELT_TAIL_Z, BELT_X1, BELT_TIP_Z, "med", fill="#e3f1ef")
    for zz in range(-340, 1040, 90):
        top.line(BELT_X0 + 8, zz, BELT_X1 - 8, zz, "thin")
    for zz in (-300, -100, 100, 300):
        top.line(-250, zz, -250, zz + 80, "vis")
        arrow(svg, top.X(-250), top.Y(zz + 80), "down")
    # 全宽门
    top.line(GATE_X, -Z_BOX, GATE_X, Z_BOX, "vis")
    top.rect(GATE_X - 12, -Z_BOX, GATE_X, Z_BOX, "med", fill="#f7e6d2")
    leader(svg, top.X(GATE_X), top.Y(300), 112, 166, "全宽门 780×180", anchor="start", size=1.5)
    # 精料仓/绞龙
    top.rect(CONC_X0, -CONC_Z, CONC_X1, CONC_Z, "vis", fill="url(#conc)")
    for cxx, czz in ((CONC_X0 + 40, -220), (CONC_X0 + 40, 220), (CONC_X1 - 40, 0)):
        top.circle(cxx, czz, 24, "med", fill="#f0c07a")
    top.line(-642, 0, AUGER_X, 250, "med")
    top.line(AUGER_X, 250, AUGER_X, BELT_TIP_Z, "med")
    top.circle(AUGER_X, BELT_TIP_Z, 60, "med", fill="#f7edc9")
    # 电池/电控/轮
    top.rect(BAT_X0, -250, BAT_X1, 250, "hid")
    top.rect(450, -175, 750, 175, "hid")
    for bx in (-925, 835):
        top.rect(bx, -475, bx + 90, 475, "thin", fill="#e8edf0")
    top.circle(-40, 0, 42, "cen")
    top.line(-82, 0, 2, 0, "cen")
    top.line(-40, -42, -40, 42, "cen")
    top.text(-40, -3, "G", "txt", size=2.0, weight="bold")

    svg.text(85, 144.5, "俯视图（工作状态，含侧带）", "viewtitle", size=2.9)
    svg.text(85, 147.8, "1:15 · 全宽后门 + 箱底接料带", "small")

    dim_v(svg, top.Y(-475), top.Y(1350), 12, "1825")
    dim_v(svg, top.Y(-475), top.Y(475), 17, "950")
    dim_v(svg, top.Y(-390), top.Y(390), 22, "780")
    dim_h(svg, top.X(X_BOX0), top.X(X_BOX1), 275, "1285")
    dim_h(svg, top.X(-925), top.X(925), 281, "1850")

    # 剖切 A-A / B-B
    svg.line(20, top.Y(0), 148, top.Y(0), "cen")
    arrow(svg, 20, top.Y(0), "down")
    arrow(svg, 148, top.Y(0), "down")
    svg.text(23, top.Y(0) - 2, "A", "txt", size=2.4, weight="bold")
    svg.text(143, top.Y(0) - 2, "A", "txt", size=2.4, weight="bold")
    svg.line(side.X(-250), 24, side.X(-250), 126, "cen")
    arrow(svg, side.X(-250), 24, "right")
    arrow(svg, side.X(-250), 126, "right")
    svg.text(side.X(-250) + 3, 22, "B", "txt", size=2.4, weight="bold")
    svg.text(side.X(-250) + 3, 129, "B", "txt", size=2.4, weight="bold")

    # ================= 前视 =================
    ground(svg, 232, 400, 125)
    for wz in (-TRACK_Z, TRACK_Z):
        front.rect(wz - WHEEL_W / 2, 0, wz + WHEEL_W / 2, 2 * WHEEL_R, "vis", fill="#e6ebee", rx=1.2)
    front.rect(-CHASSIS_Z, 260, CHASSIS_Z, 380, "med", fill="url(#hatch2)")
    front.rect(-250, 100, 250, 300, "hid")
    front.rect(-Z_BOX, Y_FLOOR_BOT, Z_BOX, Y_BOX, "vis", fill="#f8fafb")
    front.rect(-Z_BOX, 1310, Z_BOX, Y_BOX, "thin")
    # 全宽门（x=-50，正视可见）
    front.rect(-Z_BOX, GATE_Y0, Z_BOX, GATE_Y1, "hid")
    front.line(-Z_BOX, Y_FLOOR, Z_BOX, Y_FLOOR, "hid")
    front.line(-Z_BOX, Y_SLAT, Z_BOX, Y_SLAT, "hid")
    for zz in (-250, 0, 250):
        front.rect(zz - 40, 380, zz + 40, 440, "med", fill="#dfe7eb")
        front.rect(zz - 30, 440, zz + 30, 480, "med", fill="#f0c07a")
    svg.text(246, 120, "全宽门见 A-A / B-B", "small", size=1.35, anchor="start")
    # 箱底水平带（隐藏）+ 外侧倾斜段
    front.line(BELT_TAIL_Z, BELT_Y, BELT_KNEE_Z, BELT_Y, "hid")
    front.line(BELT_TAIL_Z, BELT_Y + 25, BELT_KNEE_Z, BELT_Y + 25, "hid")
    front.line(BELT_KNEE_Z, BELT_Y, BELT_TIP_Z, BELT_TIP_Y, "med")
    front.line(BELT_KNEE_Z, BELT_Y + 25, BELT_TIP_Z, BELT_TIP_Y + 25, "med")
    front.line(BELT_KNEE_Z, BELT_Y - 25, BELT_TIP_Z, BELT_TIP_Y - 25, "med")
    front.circle(BELT_KNEE_Z, BELT_Y, 40, "med", fill="#dfe7eb")
    front.circle(BELT_TIP_Z, BELT_TIP_Y, 40, "med", fill="#dfe7eb")
    # 试验槽
    front.rect(TROUGH_Z0, 0, TROUGH_Z1, TROUGH_RIM, "phantom")
    front.line(TROUGH_Z0, FEED_Y, TROUGH_Z1, FEED_Y, "phantom")
    # 桅杆
    front.rect(-13, 1380, 13, 1600, "med")

    svg.text(246, 11.5, "前视图（+X，车头方向）", "viewtitle", size=2.9)
    svg.text(246, 14.6, "1:15 · 工作宽 1825", "small")

    dim_h(svg, front.X(-TRACK_Z), front.X(TRACK_Z), 131, "760", ref1=125, ref2=125)
    dim_h(svg, front.X(-475), front.X(475), 137, "950", ref1=125, ref2=125)
    dim_v(svg, 125, front.Y(BELT_TIP_Y), 368, "820", ref1=front.X(BELT_TIP_Z), ref2=front.X(BELT_TIP_Z))
    dim_v(svg, 125, front.Y(TROUGH_RIM), 374, "600", ref1=front.X(TROUGH_Z1), ref2=front.X(TROUGH_Z1))

    # ================= 对比表 =================
    svg.text(155, 21, "P10（A）与 P50 主要差异", "txt", size=2.0, weight="bold", anchor="start")
    tbl(svg, 155, 25, [
        ("项目", 31, "start"), ("P10", 25, "middle"), ("P50", 24, "middle"),
    ], [
        ("外形 mm", "1850×950", "2710×1110"),
        ("箱体", "1.285×0.78×0.9", "2.0×0.95×1.1"),
        ("粗料 kg", "56–93", "190–310"),
        ("精料 kg", "92", "150–180"),
        ("整备 kg", "340", "653"),
        ("满载 kg", "~506", "~1140"),
        ("电池", "48V 30Ah", "48V 100Ah"),
        ("驱动", "2×0.4 kW", "2×0.8 kW"),
        ("轮", "350×130", "440×170"),
        ("轴距 mm", "1200", "1640"),
        ("带", "400×1555", "500×855"),
        ("后轴 kg", "272", "622"),
    ], rh=5.0, size=1.5)

    svg.text(155, 96, "降本要点", "txt", size=2.0, weight="bold", anchor="start")
    svg.mtext(155, 101, [
        "1. 箱体/车架按 0.65 长度缩，材料减 45%；",
        "2. 电池 100→30Ah，功率 3.3→1.6 kW；",
        "3. 轮 440→350，标准件，单价降 40%；",
        "4. 一条带完成全宽收集 + 抬升；",
        "5. 试验槽 7.5 m 可拆，复用棚舍。",
    ], "notetxt", size=1.55, lh=4.3)

    svg.text(155, 126, "原型边界", "txt", size=2.0, weight="bold", anchor="start")
    svg.mtext(155, 131, [
        "1. 验证：远程驾驶、装料对接、全宽后门、",
        "   箱底接料带、断链停车、充电对接。",
        "2. 不验证：15 天无人、AI 视觉、2 m 通道",
        "   90° 转弯；这批留给 50 头产品。",
        "3. 后 400 做落料槽，有效箱容 0.62 m³；",
        "   10 头 1.6 天，试验按 2 天装留余量。",
        "4. 全宽门 780×180，开度 30–80；",
        "   门区无 -Z 死区。",
        "5. 投料精度 ±5%/站（2–5 kg），",
        "   称重 3×150 kg + 3×50 kg。",
    ], "notetxt", size=1.55, lh=4.3)

    # ================= 参数表 =================
    svg.text(240, 143, "主要技术参数（P10-A）", "txt", size=2.0, weight="bold", anchor="start")
    tbl(svg, 240, 147, [
        ("项目", 40, "start"), ("参数", 78, "start"), ("备注", 45, "start"),
    ], [
        ("外形（长×宽×高）", "1850×950×1640", "含天线"),
        ("箱体 / 容积", "1285×780×900 / 0.90 m³", "有效 0.62"),
        ("粗料容量", "56–93 kg", "容重 90–150"),
        ("精料仓 / 容积", "385×500×600 / 0.116 m³", "92 kg"),
        ("整备 / 满载", "340 / 506 kg", "—"),
        ("轴距 / 轮距", "1200 / 760", "车架宽 560"),
        ("轮胎", "4×350×130 实心", "≥400 kg/轮"),
        ("电池", "48V 30Ah LiFePO4", "1.44 kWh"),
        ("行走", "2×0.4 kW，0.5 m/s", "电磁抱闸"),
        ("链板", "0.37 kW，885 长", "节距 90"),
        ("侧带", "400×1555，水平+33°", "0.37 kW"),
        ("全宽门", "780×180，开度 30–80", "2×推杆"),
        ("精料绞龙", "Φ90，0.18 kW", "出口 z=1050"),
        ("最小离地", "100（电池）/ 260（车架）", "—"),
        ("轴荷（空/满）", "176/164；234/272", "后轴 ≤350"),
    ], rh=6.1, size=1.5)

    frame(svg, 1, 3, "10 头原型车（A）· 总图", "1:15", "FC-P10-01A",
          project="智能养牛 · 10 头原型验证")
    return svg.render("P10-A 十头原型车 总图")


if __name__ == "__main__":
    data = sheet1()
    path = os.path.join(OUT, "p10-01a-general.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    print("wrote", path, len(data))
