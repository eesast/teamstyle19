#pragma once
#include <stdint.h>

extern uint8_t const* const pui8LittleEndian;
#define MY_LITTLE_ENDIAN (*pui8LittleEndian)

void EndianConvertOrg(void* pvData,uint8_t ui8Size,uint32_t ui8Length);
void EndianConvertOrg(void const* pvSource,void* pvDest,uint8_t ui8Size,uint32_t ui8Length);

template<typename tType> tType* EndianConvert(tType* ptData,uint32_t ui32Length)
{
	EndianConvertOrg(reinterpret_cast<void*>(ptData),sizeof(tType),ui32Length);
	return ptData;
}

template<typename tType> tType* EndianConvert(tType const* ptSource,tType* ptDest,uint32_t ui32Length)
{
	EndianConvertOrg(reinterpret_cast<void const*>(ptSource),reinterpret_cast<void*>(ptDest),sizeof(tType),ui32Length);
	return ptDest;
}

template<typename tType> void EndianConvertDest(tType* ptDest,tType const& tData)
{
	EndianConvert(&tData,ptDest,1);
}

template<typename tType> tType const EndianConvert(tType const& tData)
{
	tType tNew;
	return *EndianConvert(&tData,&tNew,1);
}
