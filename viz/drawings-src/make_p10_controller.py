# -*- coding: utf-8 -*-
"""P10-A 控制器架构（ESP32-S3 + 安全继电器）"""
import os
from make_drawings import SVG, arrow, frame, OUT
from p10 import tbl


def blk(svg, x, y, w, h, title, sub="", size=1.55, fill="#f8fafb"):
    svg.rect(x, y, w, h, "med", fill=fill)
    lines = title.split("\n")
    base = y + h / 2 - (len(lines) - 1) * 1.8 + 0.6
    for i, ln in enumerate(lines):
        svg.text(x + w / 2, base + i * 3.6, ln, "txt", size=size)
    if sub:
        svg.text(x + w / 2, y + h - 1.6, sub, "small", size=1.25)


def sheet():
    svg = SVG()
    svg.text(15, 20, "P10-A 控制器架构（ESP32-S3 + 硬线安全链）", "viewtitle", size=3.4, anchor="start")
    svg.text(15, 24, "安全层不进 MCU；主控只管运行使能与监督；4G/视频走独立路由。", "small", size=1.7, anchor="start")

    # ================= A 电源 =================
    svg.text(14, 34, "A 电源与配电", "txt", size=2.1, weight="bold", anchor="start")
    blk(svg, 14, 40, 46, 16, "48V 30Ah", "LiFePO4 + BMS 40A", 1.5)
    blk(svg, 14, 62, 46, 14, "ANL125A + 主接触器", "24V 线圈", 1.35)
    svg.line(66, 48, 66, 176, "med")
    svg.line(60, 48, 66, 48, "med")
    svg.line(60, 69, 66, 69, "med")
    svg.line(66, 80, 74, 80, "med")
    blk(svg, 74, 70, 44, 20, "5× 驱动器供电", "行走 2 / 链板 / 侧带 / 绞龙", 1.3)
    blk(svg, 74, 96, 44, 14, "DC/DC 48→24V 10A", "安全/门/抱闸", 1.3)
    blk(svg, 74, 114, 44, 14, "DC/DC 48→12V 5A", "路由/相机/HMI", 1.3)
    blk(svg, 74, 132, 44, 14, "DC/DC 48→5V 3A", "载板/ADC/传感器", 1.3)
    blk(svg, 74, 150, 44, 14, "预充 50Ω / 充电座", "4 芯 + 联锁", 1.3)
    for yy in (106, 124, 142, 160):
        svg.line(66, yy, 74, yy, "med")

    # ================= B 安全链 =================
    svg.text(128, 34, "B 安全链（硬线，不经 MCU）", "txt", size=2.1, weight="bold", anchor="start")
    blk(svg, 128, 40, 44, 20, "急停×2\n防撞×2 / 倾角", "NC 双通道", 1.3)
    blk(svg, 178, 40, 40, 20, "安全继电器", "PNOZ s4 / 国产", 1.3)
    blk(svg, 224, 40, 44, 20, "主接触器\n+ 失电抱闸", "24V", 1.3)
    svg.line(172, 50, 178, 50, "med"); arrow(svg, 178, 50, "right")
    svg.line(218, 50, 224, 50, "med"); arrow(svg, 224, 50, "right")
    blk(svg, 128, 64, 40, 12, "运行使能", "MCU 监督", 1.3)
    blk(svg, 172, 64, 40, 12, "看门狗", "TPL5010", 1.3)
    blk(svg, 216, 64, 52, 12, "串联 → 接触器/抱闸", "任一断开即停车", 1.3)
    svg.line(168, 70, 172, 70, "med"); arrow(svg, 172, 70, "right")
    svg.line(212, 70, 216, 70, "med"); arrow(svg, 216, 70, "right")
    svg.line(198, 60, 198, 62, "med")
    svg.line(198, 62, 148, 62, "med")
    svg.line(148, 62, 148, 64, "med")
    arrow(svg, 148, 64, "down")
    svg.text(128, 82, "急停复位必须现场手动；远程只复位非安全故障。", "small", size=1.3, anchor="start")

    # ================= C 主控 =================
    svg.text(128, 94, "C 主控：ESP32-S3 载板", "txt", size=2.1, weight="bold", anchor="start")
    svg.rect(128, 99, 140, 98, "med", fill="#fbfcfd")
    blk(svg, 132, 103, 42, 15, "8× DI 24V", "光耦+TVS", 1.35)
    blk(svg, 178, 103, 42, 15, "8× DO 24V", "继电器", 1.35)
    blk(svg, 224, 103, 40, 15, "MCP23017×2", "I2C 扩展", 1.3)
    blk(svg, 132, 122, 42, 15, "ADS1256", "24bit / 8CH", 1.35)
    blk(svg, 178, 122, 42, 15, "RS485 ×2", "隔离", 1.35)
    blk(svg, 224, 122, 40, 15, "I2C", "RTC/扩展", 1.3)
    blk(svg, 132, 141, 42, 15, "Wi-Fi 2.4G", "→ 4G 路由", 1.3)
    blk(svg, 178, 141, 42, 15, "SD / RTC", "日志/计划", 1.3)
    blk(svg, 224, 141, 40, 15, "WDT/电源", "喂狗/监测", 1.3)
    svg.text(132, 165, "固件：safety 10ms / motion 20ms / feed 50ms / weigh 100ms / comm 100ms", "small", size=1.25, anchor="start")
    svg.text(132, 172, "状态机：INIT→IDLE→MANUAL/AUTO→FEED→RETURN→CHARGE；任意态→FAULT/ESTOP", "small", size=1.25, anchor="start")
    svg.text(132, 179, "称重闭环：2.2 kg 粗 + 2.7 kg 精；失重到量→链停→门关→带清 2–3 s", "small", size=1.25, anchor="start")
    svg.text(132, 186, "远程：MQTT/TLS；断网 2 s 停车；OTA 双分区回滚；日志 SD", "small", size=1.25, anchor="start")

    # ================= D 外设 =================
    svg.text(280, 34, "D 外设与连接", "txt", size=2.1, weight="bold", anchor="start")
    blk(svg, 280, 40, 60, 30, "5× 驱动器", "2 行走 + 链板 + 侧带 + 绞龙\nRS485 Modbus", 1.25)
    blk(svg, 280, 74, 60, 18, "全宽门", "2 推杆并联 + 十字轴\nH 桥 + 上下限位", 1.2)
    blk(svg, 280, 96, 60, 24, "6 路称重", "3×150kg + 3×50kg\nADS1256 差分", 1.2)
    blk(svg, 280, 124, 60, 26, "传感器", "急停/防撞/倾角/门限位\n充电/钥匙/料位", 1.2)
    blk(svg, 346, 40, 56, 34, "4G 路由 + 3 相机", "USR-G806s + 交换机\nRTSP / MQTT", 1.2)
    blk(svg, 346, 80, 56, 16, "7\" HMI", "串口 115200", 1.3)
    blk(svg, 346, 100, 56, 16, "充电机 48V 10A", "4 芯 + 联锁", 1.3)
    blk(svg, 346, 120, 56, 16, "云 / 手机", "MQTT / 视频", 1.3)

    # 连线
    svg.line(268, 110, 280, 55, "med")
    svg.text(272, 80, "RS485", "small", size=1.2, anchor="start", rot=90)
    svg.line(268, 130, 280, 132, "med")
    svg.text(290, 164, "Wi-Fi → 4G 路由 → 云", "small", size=1.3, anchor="start")

    # ================= 接口表 =================
    svg.text(12, 204, "主要接口", "txt", size=2.0, weight="bold", anchor="start")
    tbl(svg, 12, 208, [
        ("接口", 26, "start"), ("芯数/电平", 60, "start"), ("用途", 100, "start"),
    ], [
        ("J1", "2+PE / 48V 40A", "电池输入"),
        ("J2", "4 芯 / 48V+ 48V- PE 联锁", "充电座"),
        ("J3", "RS485 A/B + 48V", "5 台驱动器"),
        ("J4", "24V / 门上下 / 限位", "全宽门"),
        ("J5", "6× 4 线 / 5V 激励", "箱/仓称重"),
        ("J6", "24V DI ×8", "急停/防撞/限位/钥匙"),
        ("J7", "RJ45 / 12V", "4G 路由 / 相机"),
        ("J8", "UART 115200", "HMI"),
        ("J9", "USB-C", "烧录/服务"),
    ], rh=3.7, size=1.25)

    # ================= 说明 =================
    svg.text(205, 204, "设计要点", "txt", size=2.0, weight="bold", anchor="start")
    svg.mtext(205, 210, [
        "安全链：急停/防撞/倾角 → 安全继电器 →",
        "运行使能 → 看门狗 → 接触器/抱闸；",
        "急停现场复位，远程只复位非安全故障。",
        "电源：48V 主回路 / 24V 控制 / 12V 通信。",
        "称重：6 路 ADS1256；失重闭环 2.2+2.7 kg。",
        "远程：4G 路由 + 3 相机；MQTT/TLS；",
        "断网 2 s 停车。",
    ], "notetxt", size=1.3, lh=3.8)

    frame(svg, 4, 4, "控制器架构", "—", "FC-P10-05",
          note="方案设计 · 非施工图", project="智能养牛 · 10 头原型验证")
    return svg.render("P10-A 控制器架构")


if __name__ == "__main__":
    data = sheet()
    path = os.path.join(OUT, "p10-05-controller.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    print("wrote", path, len(data))
