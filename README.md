# Powston Custom Tasmota Firmware for LilyGO T-Display

Welcome to the Powston Custom Tasmota Firmware repository! This project provides custom firmware for the [LilyGO T-Display](https://www.lilygo.cc/products/lilygo%C2%AE-ttgo-t-display-1-14-inch-lcd-esp32-control-board), designed to support extended MQTT packet handling and JSON parsing for real-time energy management display and control. This firmware is optimized for IoT energy devices, with integrated display commands for user-friendly monitoring on the LilyGO T-Display.

## Features

- **Extended MQTT Packet Handling**: Enhanced support for MQTT, enabling larger payloads to transmit more complex data for energy management.
- **JSON Parsing**: Built-in JSON parser for seamless handling of structured data, allowing easy extraction of key metrics and parameters from the MQTT payload.
- **Display Commands**: Commands to control what is displayed on the LilyGO T-Display, ensuring that essential energy management information, such as battery state, grid power, forecasted prices, and real-time usage, is shown.
- **Real-Time Updates**: Instant display updates in response to changes in data, allowing users to monitor energy usage and grid information at a glance.

## Getting Started

### Requirements

- [LilyGO T-Display](https://www.lilygo.cc/products/lilygo%C2%AE-ttgo-t-display-1-14-inch-lcd-esp32-control-board) (ESP32-based, 240x135 pixel TFT display)
- [Upload Via Tasmota](https://tasmota.github.io/install/) for flashing firmware
- [Powston](https://powston.com) account with your MQTT details

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/powston/powston-custom-firmware
   cd powston-custom-firmware
   ```

2. **Configure MQTT and Device Parameters**
   - After flashing the firmware, enter your powston MQTT details, WiFi credentials, and other device parameters.

3. **Flash the Firmware**
   - Run the script in a loop to keep your display updated as new actions are taken on your inverter.

### Usage

Once the device is connected to the Powston MQTT broker, it will start receiving JSON-encoded MQTT messages containing energy, price and inverter data. The firmware will:
- Parse these messages to display relevant data such as battery state of charge (SOC), grid power, and forecasted prices.
- Update the display with the latest data every time a new packet is received.

### Example MQTT Payload

The following is an example of a JSON MQTT message that the firmware will parse and display:
```json
{
  "battery_soc": 85,
  "grid_power": -500,
  "forecasted_prices": [0.10, 0.12, 0.15],
  "current_usage": 320
...much more...
}
```

### Display Commands

Several commands are supported for customizing the display:

- **`show_power_usage`**: Displays current power usage.
- **`show_forecast_prices`**: Displays the next few forecasted energy prices.
- **`show_battery_state`**: Displays battery state of charge (SOC).

These commands allow flexible display management directly through MQTT messages, making the device suitable for real-time monitoring in energy applications.

## Purchasing the LilyGO T-Display

You can purchase the LilyGO T-Display from the official store or other online retailers:
- [LilyGO T-Display on $8.99](https://www.lilygo.cc/products/lilygo%C2%AE-ttgo-t-display-1-14-inch-lcd-esp32-control-board)
  
> **Note**: Ensure that you purchase the ESP32-S3-based LilyGO T-Display, as this firmware is tailored specifically for that hardware.

## Contributing

We welcome contributions! Please open issues to report bugs or suggest features. Fork the repository, make your changes, and submit a pull request.

1. Fork the repo.
2. Create a branch for your feature or bug fix.
3. Submit a pull request with a description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For further assistance, reach out at service@powston.com.

---

Thank you for using Powston's Custom Firmware for LilyGO T-Display. We hope this firmware enhances your energy monitoring capabilities and brings more efficiency to your energy management system.
