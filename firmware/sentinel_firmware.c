#include "sentinel_firmware.h"

#include <stdio.h>

static uint8_t g_last_candidate;

void sentinel_bridge_init(void) {
    sentinel_hal_init();
    g_last_candidate = 0x00u;
}

void sentinel_bridge_submit(uint8_t candidate) {
    if (candidate == g_last_candidate) {
        sentinel_hal_set_candidate((uint8_t)~candidate);
        sentinel_hal_wait_cycles(1);
    }

    sentinel_hal_set_candidate(candidate);
    sentinel_hal_wait_cycles(1);
    g_last_candidate = candidate;
}

void sentinel_bridge_clear_lockout(void) {
    sentinel_hal_pulse_reset();
    g_last_candidate = 0x00u;
}

sentinel_snapshot_t sentinel_bridge_snapshot(void) {
    const uint8_t telemetry = sentinel_hal_read_telemetry();

    sentinel_snapshot_t snapshot;
    snapshot.timestamp_ms  = sentinel_hal_now_ms();
    snapshot.authorized    = ((telemetry >> 7) & 0x1u) != 0u;
    snapshot.lockout       = ((telemetry >> 6) & 0x1u) != 0u;
    snapshot.event_toggle  = ((telemetry >> 5) & 0x1u) != 0u;
    snapshot.last_result   = ((telemetry >> 4) & 0x1u) != 0u;
    snapshot.failed_attempts = telemetry & 0x0Fu;
    snapshot.display       = sentinel_hal_read_display();
    return snapshot;
}

bool sentinel_bridge_format_json(
    const sentinel_snapshot_t *snapshot,
    char *out,
    size_t out_len
) {
    if (snapshot == NULL || out == NULL || out_len == 0u) {
        return false;
    }

    const int written = snprintf(
        out,
        out_len,
        "{\"ts\":%lu,\"authorized\":%s,\"lockout\":%s,\"event\":%s,\"lastResult\":%s,\"failedAttempts\":%u,\"display\":\"0x%02X\"}",
        (unsigned long)snapshot->timestamp_ms,
        snapshot->authorized ? "true" : "false",
        snapshot->lockout ? "true" : "false",
        snapshot->event_toggle ? "true" : "false",
        snapshot->last_result ? "true" : "false",
        snapshot->failed_attempts,
        snapshot->display
    );

    return written > 0 && (size_t)written < out_len;
}
