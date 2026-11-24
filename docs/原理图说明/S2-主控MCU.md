# S2 · 主控 ESP32-S3

> 工程页名：`S2-MCU`　元件：14 个

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

| 位号 | 值 | 功能块 | 引脚→网络 |
|---|---|---|---|
| U1 | ESP32-S3-WROOM-1-N16R8 | MCU | 1→GND; 2→3V3; 3→EN; 4→DI1; 5→DI2; 6→DI3; 7→DI4; 8→DI5; 9→DI6; 10→HMI_TX; 11→HMI_RX; 12→WDT_KICK; 13→USB_DM; 14→USB_DP; 15→; 16→MCP_INT; 17→ADS_DRDY; 18→SPI_CS_ADC; 19→SPI_MOSI; 20→SPI_SCK; 21→SPI_MISO; 22→SD_CS; 23→; 24→RS485_TX; 25→RS485_RX; 26→; 27→BOOT; 28→; 29→; 30→; 31→I2C_SDA; 32→I2C_SCL; 33→; 34→; 35→; 36→UART0_RX; 37→UART0_TX; 38→GATE_CURR_L; 39→GATE_CURR_R; 40→GND; 41→GND |
| C1 | 10uF | Decoupling | 1→3V3; 2→GND |
| C2 | 100nF | Decoupling | 1→3V3; 2→GND |
| C3 | 100nF | Decoupling | 1→3V3; 2→GND |
| C4 | 100nF | Decoupling | 1→3V3; 2→GND |
| R1 | 10k | Reset/Boot | 1→3V3; 2→EN |
| C5 | 100nF | Reset/Boot | 1→EN; 2→GND |
| SW1 | RESET | Reset/Boot | 1→EN; 2→EN; 3→GND; 4→GND |
| R2 | 10k | Reset/Boot | 1→3V3; 2→BOOT |
| SW2 | BOOT | Reset/Boot | 1→BOOT; 2→BOOT; 3→GND; 4→GND |
| J1 | USB-C 16P | USB | A1B12→GND; B1A12→GND; A4B9→USB_VBUS; B4A9→USB_VBUS; A5→CC1; B5→CC2; A6→USB_DP; B6→USB_DP; A7→USB_DM; B7→USB_DM; B8→; A8→; 1→GND; 2→GND; 3→GND; 4→GND |
| R3 | 5.1k | USB | 1→CC1; 2→GND |
| R4 | 5.1k | USB | 1→CC2; 2→GND |
| U2 | USBLC6-2SC6 | USB | 1→USB_DM; 2→GND; 3→USB_DP; 4→USB_DP; 5→USB_VBUS; 6→USB_DM |

## 5. 注意

- 天线在模块端部，PCB 上该区域**禁止铺铜/走线**，并尽量靠板边。
- `EN` 的 RC（10k+100nF）不可省，否则上电复位不可靠。
- `GATE_CURR_L/R` 目前只引出到测试点/悬空，固件未使用；若要启用需补采样电路。
