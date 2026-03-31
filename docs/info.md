# VAELIX | PROJECT CITADEL: S1-90 CORE
**Version:** 1.2.0-PROT  
**Target Silicon:** IHP 130nm SG13G2 (Tiny Tapeout 06)  
**Security Tier:** TIER 1 Authorization Proof-of-Concept  

---

## How It Works

The **S1-90 Core** is now a stateful Sentinel lock with an explicit command and
telemetry interface designed for SaaS bridge firmware.

### Input Behavior
- `ui_in[7:0]` carries the candidate key byte.
- Each change on `ui_in` is treated as a submission event.
- `rst_n` pulse clears lockout and counters.

### Telemetry Outputs (`uio_out`)
- `uio_out[7]`: `AUTHORIZED`
- `uio_out[6]`: `LOCKOUT`
- `uio_out[5]`: `EVENT_TOGGLE` (toggles each submit)
- `uio_out[4]`: `LAST_RESULT`
- `uio_out[3:0]`: `FAILED_ATTEMPTS`

### Display Output (`uo_out`)
- `0xC7`: Locked
- `0xC1`: Verified
- `0xFF`: Off (`ena=0`)

---

## SaaS Bridge Readiness

The reference firmware in `firmware/` reads this telemetry map and emits stable
JSON snapshots for upstream web APIs.

Example payload:

```json
{"ts":1250031,"authorized":true,"lockout":false,"event":true,"lastResult":true,"failedAttempts":0,"display":"0xC1"}
```

---

## Verification checklist

1. Assert `ena=1`, `rst_n=1`.
2. Submit five incorrect keys by changing `ui_in`; observe `LOCKOUT=1`.
3. Try the correct key during lockout; observe rejection.
4. Pulse `rst_n` low then high; observe counters reset.
5. Change `ui_in` to `0xB6`; observe `AUTHORIZED=1` and `uo_out=0xC1`.
