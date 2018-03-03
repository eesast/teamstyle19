#include <Windows.h>

#include "MyTime.h"

extern uint32_t const g_ui32TimeOut=50u;

uint32_t GetTime()
{
	return (uint32_t)GetTickCount();
}