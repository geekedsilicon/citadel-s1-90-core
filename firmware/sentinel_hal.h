#ifndef SENTINEL_HAL_H
#define SENTINEL_HAL_H

#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

void sentinel_hal_init(void);
void sentinel_hal_set_candidate(uint8_t candidate);
void sentinel_hal_wait_cycles(uint32_t cycles);
void sentinel_hal_pulse_reset(void);
uint8_t sentinel_hal_read_telemetry(void);
uint8_t sentinel_hal_read_display(void);
uint32_t sentinel_hal_now_ms(void);

#ifdef __cplusplus
}
#endif

#endif
