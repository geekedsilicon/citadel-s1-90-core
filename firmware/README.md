# Sentinel SaaS Bridge Firmware

This firmware package bridges Tiny Tapeout Sentinel hardware telemetry to Vaelix SaaS.

## Hardware contract

### Inputs driven by MCU
- `ui_in[7:0]`: candidate key byte.
- Any change to `ui_in` is treated by hardware as a new submission event.
- Lockout reset is performed with a reset pulse (`rst_n`) through HAL.

### Outputs read by MCU
- `uio_out[7]`: `AUTHORIZED`
- `uio_out[6]`: `LOCKOUT`
- `uio_out[5]`: `EVENT_TOGGLE`
- `uio_out[4]`: `LAST_RESULT`
- `uio_out[3:0]`: failed-attempt counter
- `uo_out[7:0]`: display byte (`0xC7` locked, `0xC1` verified, `0xFF` off)

## Firmware API

- `sentinel_bridge_submit(candidate)` updates `ui_in` and waits one cycle.
- `sentinel_bridge_clear_lockout()` pulses reset and re-syncs bridge state.
- `sentinel_bridge_snapshot()` reads telemetry+display into a stable struct.
- `sentinel_bridge_format_json()` emits SaaS-ready JSON payload.

## Example payload

```json
{"ts":1250031,"authorized":true,"lockout":false,"event":true,"lastResult":true,"failedAttempts":0,"display":"0xC1"}
```
