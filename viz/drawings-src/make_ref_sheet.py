# -*- coding: utf-8 -*-
"""P10-A 称重 2.5V 基准 + 比率型激励 方案图（A3）"""
import os
from make_drawings import SVG, arrow, frame, OUT


def blk(svg, x, y, w, h, title, sub="", size=2.1, fill="#f8fafb"):
    svg.rect(x, y, w, h, "med", fill=fill)
    svg.text(x + w / 2, y + h / 2 + (0.8 if not sub else -0.6), title, "txt", size=size)
    if sub:
        svg.text(x + w / 2, y + h - 2.2, sub, "small", size=1.5)


def sheet():
    svg = SVG()
    svg.text(14, 18, "P10-A 称重：2.5 V 基准 + 比率型激励（改板方案）", "viewtitle", size=4.0, anchor="start")
    svg.text(14, 24, "EXC = 2 × VREF，二者同源于 REF5025；5 V 激励保持，VREF = 2.500 V。", "small", size=1.8, anchor="start")

    # 24V -> 6V
    blk(svg, 16, 38, 40, 14, "24V_P", "来自 S1 母线")
    blk(svg, 68, 36, 38, 18, "U51 78L06", "6 V / 100 mA", 1.8)
    svg.line(56, 45, 68, 45, "med"); arrow(svg, 68, 45, "right")
    svg.line(106, 45, 128, 45, "med")
    svg.text(112, 43, "6V", "small", size=1.6, anchor="start")

    # 5V -> REF5025
    blk(svg, 16, 78, 40, 14, "5V", "S1 buck 输出")
    blk(svg, 68, 76, 38, 18, "U50 REF5025", "2.5 V / 3 ppm", 1.8)
    svg.line(56, 85, 68, 85, "med"); arrow(svg, 68, 85, "right")

    # VREF node
    svg.line(106, 85, 150, 85, "med")
    svg.text(120, 82.5, "VREF = 2.500 V", "small", size=1.6, anchor="start")
    svg.circle(150, 85, 1.2, "vis", fill="#1f2933")

    # op-amp triangle (U52A)
    pts = [(150, 55), (150, 75), (168, 65)]
    svg.poly(pts, "med", fill="#f2f6f8", close=True)
    svg.text(155, 59, "+", "txt", size=2.4)
    svg.text(155, 73, "−", "txt", size=2.4)
    svg.line(150, 60, 132, 60, "med")   # + input from VREF? actually + to VREF
    svg.line(132, 60, 132, 85, "med")
    svg.line(132, 85, 150, 85, "med")
    svg.text(176, 66, "U52A OPA2197", "small", size=1.6, anchor="start")
    svg.text(176, 69.5, "（6V 供电）", "small", size=1.4, anchor="start")

    # feedback divider: emitter -> R71 -> -input; R70 to GND
    svg.line(168, 65, 186, 65, "med")
    svg.text(172, 63, "R72 100Ω", "small", size=1.4, anchor="start")
    # Q1
    svg.circle(196, 60, 4.5, "med")
    svg.line(186, 65, 192, 62, "med")
    svg.text(190, 55, "Q1 BC817", "small", size=1.5, anchor="start")
    svg.line(196, 55.5, 196, 45, "med")     # collector to 6V
    svg.line(196, 45, 150, 45, "med")
    svg.line(196, 64.5, 196, 78, "med")     # emitter down
    svg.text(200, 74, "EXC_5V", "small", size=1.7, anchor="start")

    # feedback: emitter node -> R71 -> minus input
    svg.circle(196, 78, 1.2, "vis", fill="#1f2933")
    svg.line(196, 78, 214, 78, "med")
    svg.line(214, 78, 214, 70, "med")
    svg.line(214, 70, 168, 70, "med")
    svg.text(218, 75, "R71 10k 0.1%", "small", size=1.4, anchor="start")
    # R70 to GND from minus node
    svg.line(168, 70, 168, 86, "med")
    svg.line(168, 86, 178, 86, "med")
    svg.text(180, 87.5, "R70 10k 0.1% → GND", "small", size=1.4, anchor="start")
    svg.line(168, 70, 168, 70, "med")

    # EXC output to terminals
    svg.line(196, 78, 260, 78, "med")
    svg.text(222, 76, "EXC_5V（84 mA）", "small", size=1.6, anchor="start")
    svg.line(260, 78, 260, 50, "med")
    svg.line(260, 50, 300, 50, "med")
    blk(svg, 300, 40, 86, 34, "J30–J35 称重端子", "1: EXC_5V  2: EXC_RET(GND)", 1.8)
    arrow(svg, 300, 50, "right")

    # VREF to ADC
    svg.line(150, 85, 300, 85, "med")
    blk(svg, 300, 82, 86, 26, "U40 ADS1256", "VREF pin4；C64 1µF + C65 100nF", 1.7)
    arrow(svg, 300, 85, "right")
    svg.text(150, 89, "C82 1µF + C85 100nF", "small", size=1.4, anchor="start")

    # 6V decoupling and note
    svg.text(128, 40, "C83 10µF + C84 100nF", "small", size=1.4, anchor="start")

    # bottom notes
    svg.text(14, 130, "接线与改板要点", "txt", size=2.2, weight="bold", anchor="start")
    svg.mtext(14, 136, [
        "1. J30–J35 的 1 脚由原 5V 改接 EXC_5V；2 脚（GND）作为 EXC_RET，单点回到 U50 的 GND（星型）。",
        "2. VREF 由 REF5025 直接驱动 ADS1256 pin4，就近放 1µF+100nF；VREF 走线短、包地。",
        "3. EXC_5V = 2 × VREF（R70 = R71 = 10k 0.1%）；5V 激励不变，负载仍为 2 mV/V → 10 mV 满量程。",
        "4. 78L06 从 24V_P 取电（耗散约 0.36 W），给 U52 与 Q1 集电极；U52B 不用时输入接地、输出跟随。",
        "5. 布局：REF/OPA/Q1 靠近 ADS1256 与称重端子，远离继电器、RS485、电机线；模拟地单点连接。",
        "6. 误差预算：REF5025 0.05% + 0.1% 电阻 → 比率误差 <0.25%，可通过五点标定消除；温漂 3 ppm/°C。",
    ], "notetxt", size=1.55, lh=4.4)

    svg.text(14, 170, "器件选型（新增）", "txt", size=2.2, weight="bold", anchor="start")
    rows = [
        ("U50", "REF5025AIDR", "2.5V 基准，3ppm/°C，SOIC-8"),
        ("U51", "78L06", "6V/100mA LDO，SOT-89，24V 输入"),
        ("U52", "OPA2197IDR", "双运放，36V，精密，SOIC-8（6V 供电）"),
        ("Q1", "BC817-40", "NPN 500mA，SOT-23，EXC 缓冲"),
        ("R70/R71", "10k 0.1% 0603", "增益 2，决定 EXC/VREF 比率"),
        ("R72", "100Ω 0603", "Q1 基极限流"),
        ("C80/C83", "10µF/16V 0805", "EXC / 6V 储能"),
        ("C81/C82/C84/C85", "100nF/1µF 0603", "VREF、EXC、6V 去耦"),
    ]
    y = 176
    svg.text(16, y, "位号", "small", size=1.6, anchor="start", weight="bold")
    svg.text(52, y, "型号", "small", size=1.6, anchor="start", weight="bold")
    svg.text(110, y, "说明", "small", size=1.6, anchor="start", weight="bold")
    for i, (a, b, c) in enumerate(rows, 1):
        yy = y + i * 4.6
        svg.text(16, yy, a, "small", size=1.55, anchor="start")
        svg.text(52, yy, b, "small", size=1.55, anchor="start")
        svg.text(110, yy, c, "small", size=1.55, anchor="start")

    frame(svg, 1, 1, "称重基准与比率激励改板", "—", "FC-P10-06",
          note="方案设计 · 待改板验证", project="智能养牛 · 10 头原型验证")
    return svg.render("P10-A 称重基准与比率激励")


if __name__ == "__main__":
    data = sheet()
    path = os.path.join(OUT, "p10-ref-ratiometric.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    print("wrote", path, len(data))
