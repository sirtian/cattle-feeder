# S4 · 8 路数字输出（DO）

> 工程页名：`S4-DO-A`（MCP23017 + ULN2803 + K1–K4，15 元件）/ `S4-DO-B`（K5–K8 + 端子，6 元件），合并说明 21 个元件

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

| 位号 | 值 | 功能块 | 引脚→网络 |
|---|---|---|---|
| U30 | MCP23017 | IO Expander | 1→MCP_P10; 2→MCP_P11; 3→MCP_P12; 4→MCP_P13; 5→MCP_P14; 6→MCP_P15; 7→MCP_P16; 8→MCP_P17; 9→3V3; 10→GND; 11→; 12→I2C_SCL; 13→I2C_SDA; 14→; 15→GND; 16→GND; 17→GND; 18→RST_MCP; 19→; 20→MCP_INT; 21→MCP_DI7; 22→MCP_DI8; 23→; 24→; 25→; 26→; 27→; 28→ |
| U31 | ULN2803A | Relay Driver | 1→MCP_P10; 2→MCP_P11; 3→MCP_P12; 4→MCP_P13; 5→MCP_P14; 6→MCP_P15; 7→MCP_P16; 8→MCP_P17; 9→GND; 10→24V_P; 11→COIL2_8; 12→COIL2_7; 13→COIL2_6; 14→COIL2_5; 15→COIL2_4; 16→COIL2_3; 17→COIL2_2; 18→COIL2_1 |
| K1 | G5LE-1A4 DC24 | Relays | 5→24V_P; 2→COIL2_1; 1→24V_P; 3→DO1 |
| K2 | G5LE-1A4 DC24 | Relays | 5→24V_P; 2→COIL2_2; 1→24V_P; 3→DO2 |
| K3 | G5LE-1A4 DC24 | Relays | 5→24V_P; 2→COIL2_3; 1→24V_P; 3→DO3 |
| K4 | G5LE-1A4 DC24 | Relays | 5→24V_P; 2→COIL2_4; 1→24V_P; 3→DO4 |
| K5 | G5LE-1A4 DC24 | Relays | 5→24V_P; 2→COIL2_5; 1→24V_P; 3→DO5 |
| K6 | G5LE-1A4 DC24 | Relays | 5→24V_P; 2→COIL2_6; 1→24V_P; 3→DO6 |
| K7 | G5LE-1A4 DC24 | Relays | 5→24V_P; 2→COIL2_7; 1→24V_P; 3→DO7 |
| K8 | G5LE-1A4 DC24 | Relays | 5→24V_P; 2→COIL2_8; 1→24V_P; 3→DO8 |
| R60 | 4.7k | IO Expander | 1→3V3; 2→I2C_SDA |
| R61 | 4.7k | IO Expander | 1→3V3; 2→I2C_SCL |
| R62 | 10k | IO Expander | 1→3V3; 2→RST_MCP |
| R63 | 10k | IO Expander | 1→3V3; 2→MCP_INT |
| C50 | 100nF | IO Expander | 1→3V3; 2→GND |
| C51 | 10uF | IO Expander | 1→3V3; 2→GND |
| C52 | 100nF | IO Expander | 1→RST_MCP; 2→GND |
| J20 | KF128-5P | Connectors | 1→DO1; 2→GND; 3→DO2; 4→GND; 5→24V_P |
| J21 | KF128-5P | Connectors | 1→DO3; 2→GND; 3→DO4; 4→GND; 5→24V_P |
| J22 | KF128-5P | Connectors | 1→DO5; 2→GND; 3→DO6; 4→GND; 5→24V_P |
| J23 | KF128-5P | Connectors | 1→DO7; 2→GND; 3→DO8; 4→GND; 5→24V_P |

## 4. 注意

- ULN2803 是达林顿，饱和压降约 1 V，线圈实际电压约 23 V，属正常。
- 继电器触点容量有限（G5LE 约 10 A/250 VAC、8 A/30 VDC），门推杆等感性负载建议外加续流/RC。
- MCP23017 上电默认输入，固件需先配置为输出并写默认电平，避免上电误动作。
- 抱闸为**失电制动**：继电器失电时抱闸抱住，安全侧失效。
