#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "../firmware/sentinel_firmware.h"

static uint8_t g_candidate;
static uint8_t g_telemetry;
static uint8_t g_display;
static uint32_t g_now_ms;
static uint8_t g_failed_attempts;
static bool g_lockout;
static bool g_authorized;
static bool g_event;
static bool g_last_result;

static void update_telemetry(void) {
    g_telemetry = 0;
    g_telemetry |= (uint8_t)(g_authorized ? 0x80 : 0x00);
    g_telemetry |= (uint8_t)(g_lockout ? 0x40 : 0x00);
    g_telemetry |= (uint8_t)(g_event ? 0x20 : 0x00);
    g_telemetry |= (uint8_t)(g_last_result ? 0x10 : 0x00);
    g_telemetry |= (uint8_t)(g_failed_attempts & 0x0F);
}

void sentinel_hal_init(void) {
    g_candidate = 0;
    g_telemetry = 0;
    g_display = 0xC7;
    g_now_ms = 1000;
    g_failed_attempts = 0;
    g_lockout = false;
    g_authorized = false;
    g_event = false;
    g_last_result = false;
    update_telemetry();
}

void sentinel_hal_set_candidate(uint8_t candidate) {
    g_candidate = candidate;
}

void sentinel_hal_wait_cycles(uint32_t cycles) {
    (void)cycles;
    g_now_ms += 1;

    if (g_candidate == 0xB6) {
        if (!g_lockout) {
            g_authorized = true;
            g_last_result = true;
            g_failed_attempts = 0;
            g_display = 0xC1;
        }
    } else {
        g_authorized = false;
        g_last_result = false;
        if (!g_lockout && g_failed_attempts < 15) {
            g_failed_attempts++;
            if (g_failed_attempts >= 5) {
                g_lockout = true;
            }
        }
        g_display = 0xC7;
    }
    g_event = !g_event;
    update_telemetry();
}

void sentinel_hal_pulse_reset(void) {
    g_failed_attempts = 0;
    g_lockout = false;
    g_authorized = false;
    g_last_result = false;
    g_display = 0xC7;
    update_telemetry();
}

uint8_t sentinel_hal_read_telemetry(void) {
    return g_telemetry;
}

uint8_t sentinel_hal_read_display(void) {
    return g_display;
}

uint32_t sentinel_hal_now_ms(void) {
    return g_now_ms;
}

int main(void) {
    char json[200];

    sentinel_bridge_init();

    // Trigger lockout with bad attempts
    for (int i = 0; i < 5; ++i) {
        sentinel_bridge_submit((uint8_t)i);
    }

    sentinel_snapshot_t s = sentinel_bridge_snapshot();
    assert(s.lockout == true);
    assert(s.authorized == false);
    assert(s.failed_attempts == 5);
    assert(s.display == 0xC7);

    bool ok = sentinel_bridge_format_json(&s, json, sizeof(json));
    assert(ok);
    assert(strstr(json, "\"lockout\":true") != NULL);
    assert(strstr(json, "\"display\":\"0xC7\"") != NULL);

    // Clear lockout, then authorize
    sentinel_bridge_clear_lockout();
    sentinel_bridge_submit(0xB6);

    s = sentinel_bridge_snapshot();
    assert(s.lockout == false);
    assert(s.authorized == true);
    assert(s.failed_attempts == 0);
    assert(s.display == 0xC1);

    ok = sentinel_bridge_format_json(&s, json, sizeof(json));
    assert(ok);
    assert(strstr(json, "\"authorized\":true") != NULL);
    assert(strstr(json, "\"failedAttempts\":0") != NULL);
    assert(strstr(json, "\"display\":\"0xC1\"") != NULL);

    printf("firmware_bridge_test: PASS\n");
    return 0;
}
