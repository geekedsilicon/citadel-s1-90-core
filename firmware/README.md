# Sentinel Firmware Reference

This folder contains a production-ready firmware skeleton for host MCUs that
supervise the **S1-90 Sentinel Lock** on a Tiny Tapeout demo-board setup.

## What this firmware provides

- Deterministic state machine (`LOCKED`, `VERIFIED`, `LOCKOUT`).
- Configurable key (`vaelix_key`), max failed attempts, and lockout window.
- Clean HAL separation so you can port to RP2040, STM32, ESP32, or bare-metal.
- Output behavior aligned to the hardware protocol:
  - `0xC7` on 7-seg for locked.
  - `0xC1` on 7-seg for verified.
  - `0xFF` on 7-seg during lockout.
  - `0xFF`/`0x00` status glow for verified/locked.

## Integration steps

1. Implement the functions declared in `sentinel_hal.h` for your board.
2. Instantiate a `sentinel_ctx_t` and call `sentinel_init` once at boot.
3. Periodically call `sentinel_tick` (for lockout timeout expiry).
4. Call `sentinel_submit_candidate` when a new key candidate is available.

## Minimal usage snippet

```c
sentinel_ctx_t ctx;
const sentinel_config_t cfg = {
    .vaelix_key = 0xB6,
    .max_attempts = 5,
    .lockout_ms = 30000,
};

sentinel_init(&ctx, &cfg);

while (1) {
    sentinel_tick(&ctx);
    uint8_t candidate = read_candidate_switches();
    if (new_candidate_ready()) {
        (void)sentinel_submit_candidate(&ctx, candidate);
    }
}
```
