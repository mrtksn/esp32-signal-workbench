# Workbench guide

## Hardware and connection

This firmware targets the classic ESP32-WROOM (ESP32-D0WD), not ESP32-S3/C3. The supplied board profile matches a 30-pin board viewed from the component side, USB connector at the top. Read GPIO labels rather than counting header positions; RX2/TX2 are GPIO16/17 and VP/VN are GPIO36/39.

Use USB for board power and host communication. The browser uses Web Serial at 921600 baud and requires firmware protocol 2. Opening the USB serial port may reset the board; the handshake retries while it boots. Use desktop Chrome or Edge. The hosted HTTPS page communicates directly with your selected serial device; there is no server-side device connection.

| Role | Supported GPIOs |
| --- | --- |
| Input/output | 4, 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33 |
| Extra input-only | 34, 35, 36/VP, 39/VN; no internal pull resistors |
| ADC1 | 32, 33, 34, 35, 36, 39 |
| ADC2 | 4, 13, 14, 25, 26, 27; Wi-Fi stays off |

Boot-strapping, flash and USB-serial pins are reserved. Share ground with the target. GPIOs use 3.3 V logic and are not 5 V tolerant. A series resistor alone is not a level shifter. Never connect a battery directly to a GPIO or the 3V3 rail. Disconnect target signals before removing board power to avoid back-powering.

**Wiring diagram** shows the selected preset's pin assignments, grounds, power, components and voltage limits. **Edit wiring** opens the configuration editor. The supplied examples cover loopback, a protected digital probe using an SN74LVC125A with a 100 nF bypass capacitor, ADC dividers and a separately powered toy ESC. Sources and package-specific pin details are included in each diagram. Documentation settings do not alter physical electrical limits.

## Instruments and limits

A preset configures up to eight logical channels in total, mixing digital inputs, analog inputs and outputs. GPIOs must be unique. Eight PWM outputs have independent timers; they are not phase-synchronized.

- **Generation:** pulse-width/duty PWM, digital levels and finite pulses, raw level/duration sequences, UART 8N1, and DShot150/300/600. PWM requests accept integer 1–1,000,000 Hz subject to hardware quantization. Pulse width must fit the period.
- **RMT signals:** at most 126 half-segments / 63 symbols per channel. UART payloads are 1–12 bytes. Long intervals or low baud rates may consume extra segments and be rejected. UART/raw repeat intervals include waveform duration. DShot repeat frames have a minimum 50 µs gap.
- **Digital capture:** UI windows 5–100 ms, up to 12,000 shared changes. Triggers wait up to 100 ms and report timeout explicitly. Inputs can be combined with output-pad readback. Polling interval is measured per capture, not a guaranteed worst-case sampling rate. Short pulses can be missed or aliased.
- **Decoding:** automatic timing/protocol candidates plus explicit UART 8N1, I²C and eight-bit MSB-first SPI modes 0–3. I²C/SPI are passive decoders, not active bus masters. UART display supports escaped UTF-8 text, typed integers/floats, endian selection and a starting offset; application message boundaries are not inferred.
- **Analog:** 12-bit readings, 1–1000 requested samples/s, 10–10,000 ms windows, at most 1024 points per channel. Channels convert sequentially. Live views consist of separate acquisitions with transfer gaps; this is a slow logger, not a high-speed analog oscilloscope.

| ADC attenuation | Approximate characterized pin-voltage range |
| --- | --- |
| 0 dB | 0.10–0.95 V |
| 2.5 dB | 0.10–1.25 V |
| 6 dB | 0.15–1.75 V |
| 12 dB | 0.15–2.45 V |

Voltage estimates use factory eFuse calibration when present, otherwise a nominal reference. Accuracy near zero, source impedance, noise and saturation still matter; compare against a reference before relying on absolute voltage. A physical divider is required for higher voltages. The example 20 kΩ / 10 kΩ divider divides by three; software display scale does not protect the pin. Its optional 100 nF ADC-to-GND capacitor filters faster changes. Do not add filter capacitors to digital data lines.

## Presets and output behavior

Controls support continuous on/off, hold, once, press/release edge signals, alternating signals, sequences and a stop action. Placement, colors and labels are editable. Sliders update running numeric outputs. UART payloads can be edited as hex, text or binary integers/floats; the wire-byte preview stays visible.

Sequences contain 1–32 signal/wait/idle/stop steps, with up to 120 seconds of total waits. Waveforms run in hardware; waits are browser-timed. A signal step starts its waveform: add a wait if it must finish before another step. Cancellation prevents later queued signals; competing controls take channel ownership.

Boot/connect/configuration leave outputs high impedance. The internal enable command sends no waveform. Explicit preset actions drive outputs. Stop restores configured idle on previously driven channels and disables further output actions. A motor's idle can be a continuing stop pulse, so software stop does not disconnect motor power. Focus loss, tab hiding and disconnect stop continuous outputs. The firmware also stops after 900 ms without host heartbeats; no automatic restart occurs.

Presets live in browser local storage. Export them before changing browser/origin or clearing storage. Captures/history are session data and have JSON/CSV export; logs can also be exported. Try demo labels all generated data as simulated.

## Configuration

`web/config/manifest.json` loads the JSON resources before the application:

- `presets.json`: shipped examples, with complete wiring documents and editable controls.
- `board.json`: physical pin positions/labels, supported roles, voltage/ADC metadata and presentation.
- `wiring-templates.json`: diagram configurations available to copy from the library.
- `defaults.json`: generic new-preset/control defaults and legacy migration data.

Every preset owns its board drawing, diagram elements, limits, component notes, parameters and calculations. The renderer has no device-name or preset-ID special cases. Duplicating/exporting/importing preserves the document. Deleted controls and diagrams stay deleted. Changes to shipped seed files do not overwrite existing saved presets; edit or import that saved copy.

The editor exposes ordinary text fields and advanced JSON for drawings/calculations. Bindings can reference `channel`, `board`, `adc`, `params` and `calc`. Expressions use declarative arrays, for example `["divide", {"ref":"params.sourceV"}, {"ref":"calc.ratio"}]`. Scripts, event attributes and external drawing resources are rejected. Missing references, invalid numeric values, division by zero and cyclic calculations report errors. Preview parameter edits in the wiring view are temporary; edit parameter defaults to save them.

## Firmware and tests

Install/export ESP-IDF v5.3.2, then run `idf.py -C firmware -p PORT build flash`. This repository includes the analysis core alongside the firmware, with no dependency on another checkout. Third-party SDK components retain their upstream licenses.

`npm test` runs the browser model/codec/transport/configuration tests. `npm run test:native` compiles synthetic capture tests with a C compiler and undefined-behavior sanitizer. Hardware checks require Python/pyserial (`python3 -m pip install -r tools/requirements.txt`). They deliberately drive otherwise unloaded pins:

```sh
python3 tools/hardware_check.py --port PORT --unloaded --output-dir /tmp/signal-workbench-check
```

Digital pad-readback tests previously covered independent PWM, live updates, idle behavior, UART, DShot, one-shots and heartbeat stopping. ADC transport was exercised across eight channels with floating inputs; that does not establish absolute measurement accuracy.

## Toy ESC example

This is an editable example for one salvaged 1S ESC, not a universal ESC profile: 490 Hz PWM, 550 µs stop, motor starting near 1070 µs, and a provisional 2000 µs upper command. Its initialization sequence explicitly sends the stop waveform and waits one second; that delay is an example, not an independently established requirement.

In a bench test, this specimen worked through 5.1 V supply, showed arming faults above 5.1 V and resets above 5.5 V. These are observations, not manufacturer ratings or validated continuous operating limits. They describe the ESC power input, never the ESP32 GPIO voltage. Supply + goes only to ESC power; supply −, ESC − and ESP32 GND share a common point. Motor current must not return through the ESP32 board.
