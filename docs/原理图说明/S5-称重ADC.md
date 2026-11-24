# S5 · 6 路称重（ADS1256）

> 工程页名：`S5-Weigh-A2`（ADS1256 + 滤波 + J30，19 元件）/ `S5-Weigh-B`（J31–J35 + 母线检测滤波，7 元件），合并说明 23 个元件

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

| 位号 | 值 | 功能块 | 引脚→网络 |
|---|---|---|---|
| U40 | ADS1256 | ADC | 1→5V; 2→GND; 3→GND; 4→VREF; 5→GND; 6→AIN0; 7→AIN1; 8→AIN2; 9→AIN3; 10→24V_SENSE; 11→48V_SENSE; 12→; 13→; 14→3V3; 15→RST_ADC; 16→3V3; 17→GND; 18→; 19→CLK_ADC; 20→SPI_CS_ADC; 21→ADS_DRDY; 22→SPI_MISO; 23→SPI_MOSI; 24→SPI_SCK; 25→; 26→; 27→; 28→ |
| Y1 | 7.68MHz | ADC | 1→3V3; 2→GND; 3→CLK_ADC; 4→3V3 |
| R80 | 1k | Filters | 1→AIN0_F; 2→AIN0 |
| R81 | 1k | Filters | 1→AIN1_F; 2→AIN1 |
| R82 | 1k | Filters | 1→AIN2_F; 2→AIN2 |
| R83 | 1k | Filters | 1→AIN3_F; 2→AIN3 |
| R84 | 10k | ADC | 1→3V3; 2→RST_ADC |
| C60 | 10uF | Filters | 1→5V; 2→GND |
| C61 | 100nF | Filters | 1→5V; 2→GND |
| C62 | 10uF | Filters | 1→3V3; 2→GND |
| C63 | 100nF | Filters | 1→3V3; 2→GND |
| C64 | 1uF | Filters | 1→VREF; 2→GND |
| C65 | 100nF | Filters | 1→VREF; 2→GND |
| C66 | 100nF | Filters | 1→AIN0; 2→GND |
| C67 | 100nF | Filters | 1→AIN1; 2→GND |
| C68 | 100nF | Filters | 1→AIN2; 2→GND |
| C69 | 100nF | Filters | 1→AIN3; 2→GND |
| C70 | 100nF | Filters | 1→RST_ADC; 2→GND |
| C71 | 100nF | Filters | 1→24V_SENSE; 2→GND |
| C72 | 100nF | Filters | 1→48V_SENSE; 2→GND |
| J30 | KF128-4P | Terminals | 1→5V; 2→GND; 3→AIN0_F; 4→AIN1_F |
| J31 | KF128-4P | Terminals | 1→5V; 2→GND; 3→AIN0_F; 4→AIN1_F |
| J32 | KF128-4P | Terminals | 1→5V; 2→GND; 3→AIN0_F; 4→AIN1_F |

## 4. 注意（重要）

- **VREF 目前没有基准源**：网表里 VREF 只接了 `C64 1µF`、`C65 100nF`，没有 2.5 V 基准芯片（原计划的 REF5050 未落位）。ADS1256 必须外接基准，当前状态无法正常转换，需补基准（如 REF5025/ADR4525）或改用带基准的称重变送器。
- 6 只传感器并联后灵敏度下降、偏载分辨变差；若验证阶段发现偏载要求高，建议改 6 路独立输入或数字称重变送器。
- 5V 激励由外部传感器共用，长线时建议每只传感器加屏蔽与 RC。
