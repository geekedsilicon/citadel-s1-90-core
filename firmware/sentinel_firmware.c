#include "sentinel_firmware.h"

#define SEG_LOCKED   0xC7u
#define SEG_VERIFIED 0xC1u
#define SEG_OFF      0xFFu

#define GLOW_ON      0xFFu
#define GLOW_OFF     0x00u

static void sentinel_apply_outputs(const sentinel_ctx_t *ctx) {
    switch (ctx->state) {
        case SENTINEL_STATE_VERIFIED:
            sentinel_hal_write_7seg(SEG_VERIFIED);
            sentinel_hal_write_status(GLOW_ON);
            break;
        case SENTINEL_STATE_LOCKOUT:
            sentinel_hal_write_7seg(SEG_OFF);
            sentinel_hal_write_status(GLOW_OFF);
            break;
        case SENTINEL_STATE_BOOT:
        case SENTINEL_STATE_LOCKED:
        default:
            sentinel_hal_write_7seg(SEG_LOCKED);
            sentinel_hal_write_status(GLOW_OFF);
            break;
    }
}

void sentinel_init(sentinel_ctx_t *ctx, const sentinel_config_t *cfg) {
    ctx->cfg = *cfg;
    ctx->state = SENTINEL_STATE_BOOT;
    ctx->failed_attempts = 0u;
    ctx->lockout_deadline_ms = 0u;

    sentinel_hal_init_pins();
    ctx->state = SENTINEL_STATE_LOCKED;
    sentinel_apply_outputs(ctx);
}

void sentinel_tick(sentinel_ctx_t *ctx) {
    if (ctx->state == SENTINEL_STATE_LOCKOUT) {
        const uint32_t now = sentinel_hal_now_ms();
        if (now >= ctx->lockout_deadline_ms) {
            ctx->failed_attempts = 0u;
            ctx->state = SENTINEL_STATE_LOCKED;
            sentinel_apply_outputs(ctx);
        }
    }
}

bool sentinel_submit_candidate(sentinel_ctx_t *ctx, uint8_t candidate) {
    if (ctx->state == SENTINEL_STATE_LOCKOUT) {
        sentinel_apply_outputs(ctx);
        return false;
    }

    if (candidate == ctx->cfg.vaelix_key) {
        ctx->state = SENTINEL_STATE_VERIFIED;
        ctx->failed_attempts = 0u;
        sentinel_apply_outputs(ctx);
        return true;
    }

    ctx->state = SENTINEL_STATE_LOCKED;

    if (ctx->failed_attempts < UINT8_MAX) {
        ctx->failed_attempts++;
    }

    if (ctx->failed_attempts >= ctx->cfg.max_attempts) {
        ctx->state = SENTINEL_STATE_LOCKOUT;
        ctx->lockout_deadline_ms = sentinel_hal_now_ms() + ctx->cfg.lockout_ms;
    }

    sentinel_apply_outputs(ctx);
    return false;
}
