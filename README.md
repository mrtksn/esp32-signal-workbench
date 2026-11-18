# ESP32 Signal Workbench

A browser-based signal generator, logic analyzer and ADC logger for a dedicated classic **ESP32-WROOM** board.

**[Open the workbench →](https://mrtksn.github.io/esp32-signal-workbench/)**

- Up to eight channels: PWM, digital levels, pulse sequences, UART bytes and DShot generation.
- Digital capture with waveforms and UART, I²C and SPI decoding; 12-bit ADC readings, plots and exports.
- Editable presets with sliders, buttons, sequences and configuration-driven wiring diagrams, component notes and voltage limits.

## Use

Open the link above in **desktop Chrome or Edge**, connect the board by USB, then click **Connect ESP32**. **Try demo** works without hardware. The board needs Signal Workbench firmware v2; from an ESP-IDF **v5.3.2** shell, build and flash it with:

```sh
idf.py -C firmware -p PORT build flash
```

Power the ESP32 by USB, share ground with your target, and keep GPIO signals within **0–3.3 V**. Use **Wiring diagram** for ADC dividers, protection components and preset-specific connections. See the [guide](docs/guide.md) for limits and configuration.

Presets are stored per browser origin. Use **Export presets / Import JSON** to move saved presets from the local UI to the hosted page.

## Develop

```sh
npm test
npm run test:native
npm run serve
```

No npm dependencies are required. The local UI opens at `http://127.0.0.1:8765/`. Changes pushed to `main` are checked and deployed to GitHub Pages automatically.

## Similar projects

- [ESP32 Bit Pirate](https://github.com/geo-tp/ESP32-Bit-Pirate/tree/pioarduino) — protocol sniffing/sending, PWM and scripting; current documented targets focus on ESP32-S3.
- [pfodWeb](https://github.com/drmpf/pfodWeb_src) — configurable browser interfaces with buttons, sliders, charts and drawings.
- [Web Logic Analyzer](https://github.com/hepter/web-logic-analyzer) — ESP32/ESP8266 browser capture and PulseView exports.
- [sigrok / PulseView](https://sigrok.org/wiki/PulseView) — desktop waveform analysis and protocol decoding.
- [Digilent WaveForms](https://digilent.com/shop/waveforms/) — a multi-instrument application for compatible Digilent hardware.
