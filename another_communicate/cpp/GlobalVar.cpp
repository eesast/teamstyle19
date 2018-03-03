#include "GlobalVar.h"
#include "api_player.h"
#include <stdlib.h>

uint16_t g_ui16Turn=0;
struct Solider* g_asSoldiers=(struct Solider*)malloc(MAX_SOLDIERS*sizeof(struct Solider));
struct Building* g_abBuildings=(struct Building*)malloc(MAX_BUILDINGS*sizeof(struct Building));

uint32_t g_ui32SolidersCount;
uint32_t g_ui32BuildingsCount;