#ifndef SENTINEL_FIRMWARE_H
#define SENTINEL_FIRMWARE_H

#include <stdbool.h>
#include <stdint.h>

#include "sentinel_hal.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    SENTINEL_STATE_BOOT = 0,
    SENTINEL_STATE_LOCKED,
    SENTINEL_STATE_VERIFIED,
    SENTINEL_STATE_LOCKOUT,
} sentinel_state_t;

typedef struct {
    uint8_t  vaelix_key;
    uint8_t  max_attempts;
    uint32_t lockout_ms;
} sentinel_config_t;

typedef struct {
    sentinel_config_t cfg;
    sentinel_state_t  state;
    uint8_t           failed_attempts;
    uint32_t          lockout_deadline_ms;
} sentinel_ctx_t;

void sentinel_init(sentinel_ctx_t *ctx, const sentinel_config_t *cfg);
void sentinel_tick(sentinel_ctx_t *ctx);
bool sentinel_submit_candidate(sentinel_ctx_t *ctx, uint8_t candidate);

#ifdef __cplusplus
}
#endif

#endif
