# VAELIX | PROJECT CITADEL — VERIFICATION PROTOCOL

**Version:** 1.2.0  
**Engine:** Cocotb 2.0.1 + Icarus Verilog  
**Target:** S1-90 Sentinel Lock (SaaS bridge protocol)

## Protocol under test

### Inputs
- `ui_in[7:0]`: candidate byte; each change triggers evaluation
- `rst_n`: reset/lockout clear

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

## Run

```sh
make -B
```

The cocotb test validates:
1. disabled mode output (`ena=0`)
2. failed-attempt accumulation
3. lockout assertion after threshold
4. lockout-clear via reset pulse
5. successful key submit path (`0xB6`)
