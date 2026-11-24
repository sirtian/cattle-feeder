# -*- coding: utf-8 -*-
"""FC-04 电气、安全、充电与明细表"""
import os
from make_drawings import SVG, leader, frame, OUT, n


def blk(svg, x, y, w, h, title, sub="", size=1.75, fill="#f8fafb"):
    svg.rect(x, y, w, h, "med", fill=fill)
    lines = title.split("\n")
    base = y + h / 2 - (len(lines) - 1) * 1.9 + 0.7
    for i, ln in enumerate(lines):
        svg.text(x + w / 2, base + i * 3.8, ln, "txt", size=size)
    if sub:
        svg.text(x + w / 2, y + h - 1.8, sub, "small", size=1.5)


def tbl(svg, x, y, cols, rows, rh=5.0, size=1.65):
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
        for (t, w, al), v in zip(cols, row):
            svg.text(cx + 1.2 if al == "start" else cx + w / 2, ry + rh * 0.7,
                     str(v), "notetxt", size=size, anchor=al)
            cx += w


def sheet4():
    svg = SVG()
    svg.text(12, 18, "电气系统框图（48V 平台）", "viewtitle", size=2.9, anchor="start")
    svg.text(12, 21.6, "实线 动力 / 虚线 通信·充电 / 阴影 预留", "small", anchor="start")

    # ---- 电源 ----
    blk(svg, 14, 72, 46, 28, "48V 100Ah\nLiFePO4 + BMS", sub="4.8 kWh")
    blk(svg, 66, 80, 30, 14, "主接触器\n+ 急停回路")
    svg.line(60, 86, 66, 86, "med")
    svg.line(96, 87, 102, 87, "med")
    svg.line(102, 36, 102, 142, "med")
    svg.text(103.6, 34, "48V 母线", "small", size=1.55, anchor="start")

    # ---- 48V 负载 ----
    loads = [
        (36, "行走驱动", "2×0.8 kW / 4 轮"),
        (56, "链板输送", "0.75 kW"),
        (76, "横向侧带", "0.55 kW"),
        (96, "精料绞龙", "0.37 kW"),
        (116, "DC/DC 48→12V", "0.3 kW"),
    ]
    for y, t, sub in loads:
        blk(svg, 110, y, 58, 14, t, sub=sub, size=1.7)
        svg.line(102, y + 7, 110, y + 7, "med")
        svg.circle(102, y + 7, 0.5, "", fill="#2d6b88")

    # ---- 12V 负载 ----
    svg.line(168, 123, 176, 123, "med")
    svg.line(176, 40, 176, 148, "med")
    svg.text(177.5, 38, "12V 控制母线", "small", size=1.55, anchor="start")
    for y, t, sub in [
        (42, "控制器 / 4G", "边缘计算"),
        (62, "相机 ×4", "前/后/侧"),
        (82, "传感器组", "称重/倾角/限位"),
        (102, "灯光 / 警示", "LED+蜂鸣"),
    ]:
        blk(svg, 184, y, 64, 14, t, sub=sub, size=1.7)
        svg.line(176, y + 7, 184, y + 7, "med")
        svg.circle(176, y + 7, 0.5, "", fill="#2d6b88")

    # ---- 远程 ----
    blk(svg, 256, 44, 22, 18, "远程\n平台", size=1.6, fill="#eef2f4")
    svg.line(248, 49, 256, 50, "hid")
    svg.line(248, 55, 256, 56, "hid")

    # ---- 充电 ----
    blk(svg, 14, 112, 46, 16, "充电座 4 芯", sub="48V/20A", size=1.7, fill="#f7edc9")
    svg.line(37, 112, 37, 100, "hid")
    svg.line(60, 120, 102, 120, "hid")
    svg.circle(102, 120, 0.5, "", fill="#2d6b88")

    # ---- 安全/充电说明 ----
    svg.text(12, 152, "安全与联锁", "txt", size=2.2, weight="bold", anchor="start")
    svg.mtext(12, 158.5, [
        "1. 急停 2 处（前后），防撞条 2 条；触发即断",
        "   主接触器，需现场复位后远程确认。",
        "2. 失联 >2 s 自动停车并抱闸；4G 恢复后可",
        "   远程复位，急停回路不参与远程复位。",
        "3. 门限位、仓满、链板过流、电池温度/绝缘",
        "   任一异常 → 停止该动作并上报。",
        "4. 倾角 >8° 禁止行走；侧带工作时禁止行走。",
        "5. 控制箱 IP65；整机 -20～45 ℃；限速 0.6 m/s。",
    ], "notetxt", size=1.7, lh=4.6)

    svg.text(145, 152, "充电与运维", "txt", size=2.2, weight="bold", anchor="start")
    svg.mtext(145, 158.5, [
        "1. 单桩 220V/16A，48V/20A 充电机；4 芯：",
        "   48V+ / 48V- / PE / 联锁信号。",
        "2. 插合后联锁断驱动；充满自动停；反接保护。",
        "3. 当期远程操控回桩插枪；预留自动对接",
        "   触点与引导板，后期升级自动回充。",
        "4. 日耗约 2.2–2.5 kWh（含 4G/相机 30 W）；",
        "   每日回桩 1–2 次，单次 0.8–1 h。",
        "5. 远程监控：电量、位置、料位、故障码；",
        "   支持远程复位与限速。",
        "6. 预留 AI 视觉接口（以太网/PoE）。",
    ], "notetxt", size=1.7, lh=4.6)

    # ---- 明细表 ----
    svg.text(285, 21, "主要零部件明细表", "txt", size=2.2, weight="bold", anchor="start")
    cols = [("序号", 8, "middle"), ("名称", 38, "start"),
            ("规格 / 说明", 50, "start"), ("数量", 10, "middle"), ("备注", 11, "start")]
    rows = [
        ("1", "底盘车架", "40×60×3 方管，2.5×0.7", "1", "焊接"),
        ("2", "驱动轮组", "440×170 实心胎，后 2 轮 0.8 kW", "4", "含轮毂"),
        ("3", "动力电池", "48V 100Ah LiFePO4+BMS", "1", "4.8 kWh"),
        ("4", "粗料箱", "2.0×0.95×1.1，板厚 2.5", "1", "2.09 m³"),
        ("5", "链板输送", "500 宽×2.0 m，0.75 kW", "1", "节距 50"),
        ("6", "侧卸门", "500×200 + 电动推杆", "1", "开度 40–100"),
        ("7", "横向侧带", "500×855，挡边 50，0.55 kW", "1", "隔板 70@105"),
        ("8", "精料仓", "0.6×0.6×0.72，3×100 kg", "1", "0.25 m³"),
        ("9", "精料绞龙", "Φ125×1.0 m，0.37 kW", "1", "出口 z=1320"),
        ("10", "称重模块", "3×500 kg（箱体）", "1 套", "3 点"),
        ("11", "控制器", "4G + 边缘计算 + 存储", "1", "远程复位"),
        ("12", "相机", "200 万，IP67", "4", "预留 AI"),
        ("13", "充电座", "4 芯，48V/20A", "1 套", "单桩"),
        ("14", "急停/防撞", "急停 2 + 防撞条 2", "1 套", "硬线"),
        ("15", "柔性导裙", "门框—带尾，85 间隙", "1 套", "耐磨胶"),
        ("16", "警示灯/蜂鸣", "LED 黄，≥85 dB", "1 套", "行走/故障"),
        ("17", "线束/控制箱", "IP65，防水接头", "1 套", "—"),
        ("18", "天线/定位", "4G + GNSS", "1 套", "—"),
    ]
    tbl(svg, 285, 25, cols, rows, rh=5.15, size=1.55)

    # ---- 质量表 ----
    svg.text(285, 133, "质量汇总", "txt", size=2.1, weight="bold", anchor="start")
    tbl(svg, 285, 137, [
        ("状态", 62, "start"), ("质量 kg", 55, "middle"),
    ], [
        ("空车", "653"),
        ("粗料 190–310 + 精料 150–180", "993–1143"),
        ("设计上限", "1200"),
    ], rh=5.8, size=1.6)

    # ---- IO ----
    svg.text(285, 171, "主要 I/O", "txt", size=2.1, weight="bold", anchor="start")
    svg.mtext(285, 177, [
        "DI  急停×2 / 防撞×2 / 倾角 / 门限位×2",
        "     仓满 / 充电到位 / 钥匙",
        "AI  称重×4 / 电池温度 / 电流",
        "DO  主接触器 / 链板 / 侧带 / 绞龙",
        "     推杆 / 灯 / 蜂鸣 / 抱闸",
        "通信 4G / Wi-Fi 调试 / PoE 相机",
    ], "notetxt", size=1.65, lh=4.5)

    # ---- 故障分级 ----
    svg.text(12, 209, "故障分级与处理", "txt", size=2.1, weight="bold", anchor="start")
    tbl(svg, 12, 213, [
        ("等级", 18, "middle"), ("触发条件", 112, "start"), ("处理", 110, "start"),
    ], [
        ("警告", "料位低 / 电量 <20% / 相机离线", "平台提示，可继续作业"),
        ("停机", "失联 >2 s / 过流 / 门限位异常", "停车抱闸，远程复位"),
        ("锁止", "急停 / 倾角 >8° / 绝缘异常", "现场复位 + 远程确认"),
    ], rh=6.2, size=1.65)

    frame(svg, 4, 4, "电气、安全与明细表", "—", "FC-04")
    return svg.render("FC-04 电气、安全与明细表")


if __name__ == "__main__":
    data = sheet4()
    path = os.path.join(OUT, "04-electrical.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    print("wrote", path, len(data))
