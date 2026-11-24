# S3 · 8 路数字输入（DI）

> 工程页名：`S3-DI-A`（DI1–4，19 元件）/ `S3-DI-B`（DI5–8，17 元件），合并说明 36 个元件

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

| 位号 | 值 | 功能块 | 引脚→网络 |
|---|---|---|---|
| U10 | EL357N | Input1-4 | 1→OPTO_A1; 2→GND; 3→GND; 4→DI1 |
| R10 | 2.2k | Input1-4 | 1→IN1; 2→OPTO_A1 |
| R18 | 10k | Input1-4 | 1→3V3; 2→DI1 |
| C10 | 100nF | Input1-4 | 1→DI1; 2→GND |
| U11 | EL357N | Input1-4 | 1→OPTO_A2; 2→GND; 3→GND; 4→DI2 |
| R11 | 2.2k | Input1-4 | 1→IN2; 2→OPTO_A2 |
| R19 | 10k | Input1-4 | 1→3V3; 2→DI2 |
| C11 | 100nF | Input1-4 | 1→DI2; 2→GND |
| U12 | EL357N | Input1-4 | 1→OPTO_A3; 2→GND; 3→GND; 4→DI3 |
| R12 | 2.2k | Input1-4 | 1→IN3; 2→OPTO_A3 |
| R20 | 10k | Input1-4 | 1→3V3; 2→DI3 |
| C12 | 100nF | Input1-4 | 1→DI3; 2→GND |
| U13 | EL357N | Input1-4 | 1→OPTO_A4; 2→GND; 3→GND; 4→DI4 |
| R13 | 2.2k | Input1-4 | 1→IN4; 2→OPTO_A4 |
| R21 | 10k | Input1-4 | 1→3V3; 2→DI4 |
| C13 | 100nF | Input1-4 | 1→DI4; 2→GND |
| U14 | EL357N | Input5-8 | 1→OPTO_A5; 2→GND; 3→GND; 4→DI5 |
| R14 | 2.2k | Input5-8 | 1→IN5; 2→OPTO_A5 |
| R22 | 10k | Input5-8 | 1→3V3; 2→DI5 |
| C14 | 100nF | Input5-8 | 1→DI5; 2→GND |
| U15 | EL357N | Input5-8 | 1→OPTO_A6; 2→GND; 3→GND; 4→DI6 |
| R15 | 2.2k | Input5-8 | 1→IN6; 2→OPTO_A6 |
| R23 | 10k | Input5-8 | 1→3V3; 2→DI6 |
| C15 | 100nF | Input5-8 | 1→DI6; 2→GND |
| U16 | EL357N | Input5-8 | 1→OPTO_A7; 2→GND; 3→GND; 4→MCP_DI7 |
| R16 | 2.2k | Input5-8 | 1→IN7; 2→OPTO_A7 |
| R24 | 10k | Input5-8 | 1→3V3; 2→MCP_DI7 |
| C16 | 100nF | Input5-8 | 1→MCP_DI7; 2→GND |
| U17 | EL357N | Input5-8 | 1→OPTO_A8; 2→GND; 3→GND; 4→MCP_DI8 |
| R17 | 2.2k | Input5-8 | 1→IN8; 2→OPTO_A8 |
| R25 | 10k | Input5-8 | 1→3V3; 2→MCP_DI8 |
| C17 | 100nF | Input5-8 | 1→MCP_DI8; 2→GND |
| J10 | KF128-5P | Input1-4 | 1→IN1; 2→IN2; 3→IN3; 4→IN4; 5→GND |
| J11 | KF128-5P | Input5-8 | 1→IN5; 2→IN6; 3→IN7; 4→IN8; 5→24V_P |
| D10 | SMBJ33A | Field Power | 1→24V_P; 2→GND |
| C18 | 10uF/50V | Field Power | 1→24V_P; 2→GND |

## 5. 注意

- **非电气隔离**：光耦输入侧与输出侧都接同一个 GND，只做电平转换/抗干扰；需要真隔离时应改为独立 `GND_F` + 隔离电源。
- **无每路反接/浪涌器件**：目前只有 D10 在 24 V 母线；长线或可能反接时建议每路加反并二极管/小 TVS。
- 导通阈值约 3–4 V，不是严格 24 V 判定；需要区分 12/24 V 时可加稳压管抬阈值。
- D10 `SMBJ33A` + `C18 10µF` 为现场电源浪涌/储能。
