#ifndef SENTINEL_HAL_H
#define SENTINEL_HAL_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

void sentinel_hal_init_pins(void);
void sentinel_hal_write_7seg(uint8_t value);
void sentinel_hal_write_status(uint8_t value);
uint32_t sentinel_hal_now_ms(void);

#ifdef __cplusplus
}
#endif

#endif
