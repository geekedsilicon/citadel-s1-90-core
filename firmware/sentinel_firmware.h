#ifndef SENTINEL_FIRMWARE_H
#define SENTINEL_FIRMWARE_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#include "sentinel_hal.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    uint32_t timestamp_ms;
    bool authorized;
    bool lockout;
    bool event_toggle;
    bool last_result;
    uint8_t failed_attempts;
    uint8_t display;
} sentinel_snapshot_t;

void sentinel_bridge_init(void);
void sentinel_bridge_submit(uint8_t candidate);
void sentinel_bridge_clear_lockout(void);
sentinel_snapshot_t sentinel_bridge_snapshot(void);

bool sentinel_bridge_format_json(
    const sentinel_snapshot_t *snapshot,
    char *out,
    size_t out_len
);

#ifdef __cplusplus
}
#endif

#endif
