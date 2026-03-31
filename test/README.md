# VAELIX | PROJECT CITADEL — VERIFICATION PROTOCOL

**Version:** 1.3.0  
**Engine:** Cocotb 2.0.1 + Icarus Verilog + GCC harness  
**Target:** S1-90 Sentinel Lock (SaaS bridge protocol)

## Protocol under test

### Inputs
- `ui_in[7:0]`: candidate byte; each change triggers evaluation.
- `rst_n`: reset/lockout clear.
- `ena`: output enable.

### Telemetry (`uio_out`)
- bit7 `AUTHORIZED`
- bit6 `LOCKOUT`
- bit5 `EVENT_TOGGLE`
- bit4 `LAST_RESULT`
- bits3:0 `FAILED_ATTEMPTS`

### Display (`uo_out`)
- `0xC7` locked
- `0xC1` verified
- `0xFF` off when `ena=0`

## Simulation tests

```sh
make -B
```

Cocotb suite now includes:
1. `test_protocol_lockout_and_recovery`
2. `test_lockout_auto_timeout`
3. `test_exhaustive_key_acceptance` (all 256 values)

## Firmware e2e harness

Compile and run the firmware bridge with a mock HAL and protocol model:

```sh
gcc -std=c11 -Wall -Wextra -Werror -pedantic \
  test/firmware_bridge_test.c firmware/sentinel_firmware.c -I firmware \
  -o /tmp/firmware_bridge_test && /tmp/firmware_bridge_test
```
