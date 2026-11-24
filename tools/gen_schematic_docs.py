# -*- coding: utf-8 -*-
"""Generate docs/原理图说明 from work/eda page JSON."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "原理图说明")
os.makedirs(OUT, exist_ok=True)


def comps(name):
    path = os.path.join(ROOT, "work", "eda", name)
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("add_components", [])


def table(cs):
    lines = ["| 位号 | 值 | 功能块 | 引脚→网络 |", "|---|---|---|---|"]
    for c in cs:
        pins = "; ".join(f"{p['pin_number']}→{p.get('signal_name')}" for p in c.get("pins", []))
        lines.append(f"| {c['designator']} | {c.get('value','')} | {c.get('block_name','')} | {pins} |")
    return "\n".join(lines)


def write(name, text):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", path)


s1 = comps("s1_power.json")
s2 = comps("s2_mcu.json")
s3 = comps("s3_di.json")
s4 = comps("s4_do.json")
s5 = comps("s5_weigh.json")
s6 = comps("s6_comm_a.json") + comps("s6_comm_b.json")
s7 = comps("s7_conn.json")

write("S1-电源.md", f"""# S1 · 电源与母线检测

> 工程页名：`S1-Power`　元件：{len(s1)} 个

## 1. 作用

把现场 24 V 转换成控制板需要的 **5 V / 3.3 V**，并对 24 V、48 V 母线做分压检测，供 ADC 监测。

## 2. 电源树

```
J1 24V_IN ─ F1 5A ─ D2 SS54 ─ 24V_P ─┬─ XL4015 Buck ─ L1 ─ 5V ─ AMS1117 ─ 3V3
                                     ├─ 继电器/门推杆/抱闸（24V）
                                     ├─ J51 辅助 24V 输出
                                     └─ R4/R5 分压 → 24V_SENSE
J2 48V_IN ─ R6/R7 分压 → 48V_SENSE
D1 SMBJ33A 24V 母线浪涌吸收；C1/C2 母线储能
```

## 3. 关键计算

| 项 | 公式 | 结果 |
|---|---|---|
| 5V 输出 | (1+30k/10k)×1.25 V | **5.0 V** |
| 24V 检测 | 24×15/(100+15) | **3.13 V** |
| 48V 检测 | 48×6.8/(100+6.8) | **3.06 V** |

## 4. 元件表

{table(s1)}

## 5. 说明与注意

- `D2 SS54` 为防反接串联二极管，正常压降约 0.5 V，24 V 母线实际约 23.5 V。
- `F1 5A` 为整板总保险；后续 24 V 分支（继电器、门、抱闸）在各自回路另有保护。
- `XL4015` 标称 5 A，实际建议长期 ≤3 A；5 V 主要供 3.3 V LDO、HMI、传感器。
- `AMS1117-3.3` 压差约 1.1 V，5 V 输入时功耗 (5−3.3)×I；3.3 V 负载大时需注意温升。
- `24V_SENSE / 48V_SENSE` 送 ADS1256 的 AIN4/AIN5（见 S5），软件需按分压比还原。
- **VREF 基准源不在本页**：ADS1256 的 VREF 目前只有滤波电容（见 S5 说明），需补 2.5 V 基准。
""")

write("S2-主控MCU.md", f"""# S2 · 主控 ESP32-S3

> 工程页名：`S2-MCU`　元件：{len(s2)} 个

## 1. 作用

系统主控：Wi-Fi 上云、远程驾驶/投喂状态机、DI/DO、RS485、ADS1256 称重、SD 日志、HMI 串口。

## 2. 最小系统

- `U1 ESP32-S3-WROOM-1-N16R8`：16 MB Flash / 8 MB PSRAM，2.4 G Wi-Fi + BLE。
- 复位：`R1 10k` 上拉 + `C5 100nF` + `SW1 RESET`。
- 下载：`R2 10k` 上拉 + `SW2 BOOT`。
- USB：`J1 USB-C`，`R3/R4 5.1k` CC 下拉，`U2 USBLC6-2SC6` ESD 保护；USB 仅用于烧录/服务，不作为主供电。
- 去耦：`C1 10µF + C2–C4 100nF`。

## 3. 引脚分配（按网表）

| 功能 | 网络 | 模块引脚 |
|---|---|---|
| 8 路 DI | DI1–DI6（DI7/8 经 MCP23017） | 4–9 |
| HMI | HMI_TX / HMI_RX | 10 / 11 |
| 看门狗喂狗 | WDT_KICK | 12 |
| USB | USB_DM / USB_DP | 13 / 14 |
| 中断 | MCP_INT / ADS_DRDY | 16 / 17 |
| SPI（ADC/SD） | CS/MOSI/SCK/MISO | 18–21 |
| SD 片选 | SD_CS | 22 |
| RS485 驱动器 | RS485_TX / RS485_RX | 24 / 25 |
| I2C | I2C_SDA / I2C_SCL | 31 / 32 |
| 服务串口 | UART0_RX / UART0_TX | 36 / 37 |
| 栅极电流采样 | GATE_CURR_L / R | 38 / 39（当前悬空，已 NC） |

## 4. 元件表

{table(s2)}

## 5. 注意

- 天线在模块端部，PCB 上该区域**禁止铺铜/走线**，并尽量靠板边。
- `EN` 的 RC（10k+100nF）不可省，否则上电复位不可靠。
- `GATE_CURR_L/R` 目前只引出到测试点/悬空，固件未使用；若要启用需补采样电路。
""")

write("S3-数字输入DI.md", f"""# S3 · 8 路数字输入（DI）

> 工程页名：`S3-DI-A`（DI1–4，19 元件）/ `S3-DI-B`（DI5–8，17 元件），合并说明 {len(s3)} 个元件

## 1. 作用

把现场 24 V 开关量（急停、防撞、门限位、钥匙、接近开关等）转换成 3.3 V GPIO 电平，并做 RC 滤波与母线浪涌保护。

## 2. 单路原理

```
现场 24V ─ INx ─ R 2.2k ─ EL357N ①(LED+) ─ ② ─ GND
                              │
                        ④ 集电极 ─ DIx ─ ESP32 / MCP23017
                              │
                        ③ 发射极 ─ GND
DIx 经 10k 上拉 3V3，100nF 到 GND
```

- 输入 24 V：LED 电流 (24−1.2)/2.2k ≈ **10.4 mA**，光敏管导通，DIx 被拉低 → **低有效**。
- 输入 0 V：LED 灭，DIx 由 10k 上拉到 3V3 → 高。
- RC：10k×100nF = **1 ms**（约 160 Hz），软件再加 10–20 ms 去抖。
- EL357N CTR ≥50%，10 mA 输入可驱动 ≥5 mA，10k 上拉仅需 0.33 mA，饱和余量大。

## 3. 接线

| 端子 | 定义 |
|---|---|
| J10-1…4 | IN1–IN4 |
| J10-5 | 现场 GND |
| J11-1…4 | IN5–IN8 |
| J11-5 | 24V_P（给现场传感器供电） |

DI1–DI6 进 ESP32 GPIO；**DI7/DI8 进 MCP23017**（`MCP_DI7/8`）。

## 4. 元件表

{table(s3)}

## 5. 注意

- **非电气隔离**：光耦输入侧与输出侧都接同一个 GND，只做电平转换/抗干扰；需要真隔离时应改为独立 `GND_F` + 隔离电源。
- **无每路反接/浪涌器件**：目前只有 D10 在 24 V 母线；长线或可能反接时建议每路加反并二极管/小 TVS。
- 导通阈值约 3–4 V，不是严格 24 V 判定；需要区分 12/24 V 时可加稳压管抬阈值。
- D10 `SMBJ33A` + `C18 10µF` 为现场电源浪涌/储能。
""")

write("S4-数字输出DO.md", f"""# S4 · 8 路数字输出（DO）

> 工程页名：`S4-DO-A`（MCP23017 + ULN2803 + K1–K4，15 元件）/ `S4-DO-B`（K5–K8 + 端子，6 元件），合并说明 {len(s4)} 个元件

## 1. 作用

8 路 24 V 继电器输出：链板/侧带/绞龙使能、门上下、警示灯、抱闸等。

## 2. 信号链

```
ESP32 ─ I2C ─ MCP23017（8 路输出 P10–P17）
                 │
             ULN2803A（达林顿阵列，内部续流二极管）
                 │
          G5LE-1A4 DC24 继电器线圈（COIL2_1…8）
                 │
         DO1…DO8 干接点 → J20–J23（每端子 2 路 + GND + 24V）
```

- MCP23017：I2C 地址由硬件固定，`R60/R61 4.7k` 上拉，`RST_MCP` 10k 上拉，`MCP_INT` 10k 上拉 + 中断到 ESP32。
- ULN2803A：8 路达林顿，COM 脚接 24V_P，线圈续流由内部二极管完成。
- 继电器：G5LE-1A4 DC24，单线圈约 0.53 W（≈22 mA），8 路同时约 **176 mA**，ULN2803 余量充足。
- 输出端子：J20–J23，每路 `DOx / GND / 24V_P`。

## 3. 元件表

{table(s4)}

## 4. 注意

- ULN2803 是达林顿，饱和压降约 1 V，线圈实际电压约 23 V，属正常。
- 继电器触点容量有限（G5LE 约 10 A/250 VAC、8 A/30 VDC），门推杆等感性负载建议外加续流/RC。
- MCP23017 上电默认输入，固件需先配置为输出并写默认电平，避免上电误动作。
- 抱闸为**失电制动**：继电器失电时抱闸抱住，安全侧失效。
""")

write("S5-称重ADC.md", f"""# S5 · 6 路称重（ADS1256）

> 工程页名：`S5-Weigh-A2`（ADS1256 + 滤波 + J30，19 元件）/ `S5-Weigh-B`（J31–J35 + 母线检测滤波，7 元件），合并说明 {len(s5)} 个元件

## 1. 作用

用 24 位 ADC 采集料仓（3×150 kg）与精料仓（3×50 kg）称重传感器，以及 24 V/48 V 母线电压。

## 2. 通道分配

| ADS1256 通道 | 网络 | 用途 |
|---|---|---|
| AIN0/AIN1 | AIN0_F / AIN1_F | 料仓 3 只传感器并联（J30–J32） |
| AIN2/AIN3 | AIN2_F / AIN3_F | 精料仓 3 只传感器并联（J33–J35） |
| AIN4 | 24V_SENSE | 24 V 母线检测 |
| AIN5 | 48V_SENSE | 48 V 母线检测 |

- 每只传感器 4 线：5V 激励、GND、信号+、信号−；同组 3 只并联后进同一对 AIN。
- 每路串 `1k` + `100nF` 到地，构成约 **1.6 kHz** 低通，抑制皮带/电机干扰。
- 晶振 `Y1 7.68 MHz`；SPI 与 ESP32 直连；`R84 10k` 复位上拉。

## 3. 元件表

{table(s5)}

## 4. 注意（重要）

- **VREF 目前没有基准源**：网表里 VREF 只接了 `C64 1µF`、`C65 100nF`，没有 2.5 V 基准芯片（原计划的 REF5050 未落位）。ADS1256 必须外接基准，当前状态无法正常转换，需补基准（如 REF5025/ADR4525）或改用带基准的称重变送器。
- 6 只传感器并联后灵敏度下降、偏载分辨变差；若验证阶段发现偏载要求高，建议改 6 路独立输入或数字称重变送器。
- 5V 激励由外部传感器共用，长线时建议每只传感器加屏蔽与 RC。
""")

write("S6-通信与存储.md", f"""# S6 · 通信、RTC、看门狗、SD

> 工程页名：`S6-Comm-A`（14 元件）/ `S6-Comm-B`（12 元件），合并说明 {len(s6)} 个元件

## 1. 内容

| 功能 | 器件 | 说明 |
|---|---|---|
| 双 UART 扩展 | `U40 SC16IS752` + `Y40 1.8432 MHz` | I2C 转 2 路 UART：BMS、充电机 |
| BMS RS485 | `U41 MAX13487E` + `J40` + `R90 120R` + `D40 SMBJ6.5CA` | 自动收发，A/B 差分 |
| 充电机 RS485 | `U42 MAX13487E` + `J41` + `R91 120R` + `D41` | 同上 |
| 驱动器 RS485 | `U43 MAX13487E` + `J42` + `R93 120R` + `D42` | 接 5 台驱动器（链板/侧带/绞龙/左/右） |
| RTC | `U44 DS3231MZ` | I2C，掉电走时（需纽扣电池/超级电容） |
| 看门狗 | `U45 TPL5010` + `R94 100k` | 1 Hz 喂狗，超时输出复位 |
| SD 卡 | `J43 TF-01A` | SPI：CS/MOSI/SCK/MISO |
| HMI | `J44 KF128-4P` | 5V/GND/HMI_TX/HMI_RX |

## 2. 元件表

{table(s6)}

## 3. 注意

- **看门狗输出接的是 `RST_MCP`（MCP23017 复位），不是运行使能/ESP32 EN**。按安全设计，MCU 死机应断开“运行使能”并抱闸；当前网表与这一目标不一致，需改板或确认由固件/外部逻辑实现。
- RS485 终端电阻 120 Ω 已固定在板上；总线两端各一个，中间节点应去掉（可用跳线/贴片选择）。
- MAX13487 为自动方向控制，无需 DE 引脚；A/B 有 TVS，但长线建议再加共模电感。
- SC16IS752 的 I2C 地址、晶振 1.8432 MHz 对应标准波特率；BMS/充电机协议需按厂家确认。
- SD 卡走线与 SPI 共用，注意 CS 独立、上电时序。
""")

write("S7-连接器与充电.md", f"""# S7 · 充电、辅助电源与调试口

> 工程页名：`S7-Conn`　元件：{len(s7)} 个

## 1. 内容

| 端子 | 定义 | 说明 |
|---|---|---|
| J50 KF301-2P | 1: CHARGE_INT，2: GND | 充电到位/中断输入（当前未接线，引脚已 NC） |
| J51 KF301-2P | 1: 24V_P，2: GND | 辅助 24 V 输出（传感器/指示灯） |
| J52 KF128-4P | 3V3 / GND / UART0_TX / UART0_RX | 服务/调试串口 |

## 2. 元件表

{table(s7)}

## 3. 注意

- `CHARGE_INT` 目前是空置网络（原设计用于充电检测），如需使用应接到 ESP32 的可用 GPIO 并在固件中处理。
- 调试口为 3.3 V 电平，接 USB-TTL 时注意电平匹配。
- 充电主回路（48 V）不经过本页，直接由电池/充电座与 BMS 管理；本页只做状态信号。
""")

print("done")
