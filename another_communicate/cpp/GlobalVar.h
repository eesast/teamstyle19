#pragma once
#include <stdint.h>

#define MAX_SOLDIERS 10000
#define MAX_BUILDINGS (2*200*200)

extern uint16_t g_ui16Turn;
extern struct Solider* g_asSoldiers;
extern struct Building* g_abBuildings;

extern uint32_t g_ui32SolidersCount;
extern uint32_t g_ui32BuildingsCount;