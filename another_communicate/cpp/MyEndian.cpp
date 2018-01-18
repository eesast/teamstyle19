#include <memory.h>

#include "MyEndian.h"

uint16_t ui16Data=0x00ffu;

uint8_t const* const pui8LittleEndian=(uint8_t const* const)&ui16Data;

void EndianConvertOrg(void* pvData,uint8_t ui8Size,uint32_t ui8Length)
{
	if (MY_LITTLE_ENDIAN&&ui8Size>1)
	{
		uint8_t *pui8Loop1,*pui8End1,*pui8Loop2,*pui8End2;
		for (
			pui8Loop1=reinterpret_cast<uint8_t*>(pvData),pui8End1=pui8Loop1+ui8Size*ui8Length;
			pui8Loop1<pui8End1;
			pui8Loop1+=ui8Size)
		{
			for (pui8Loop2=pui8Loop1,pui8End2=pui8Loop2+ui8Size-1;pui8Loop2<pui8End2;++pui8Loop2,--pui8End2)
			{
				*pui8Loop2^=*pui8End2;
				*pui8End2^=*pui8Loop2;
				*pui8Loop2^=*pui8End2;
			}
		}
	}
}

void EndianConvertOrg(void const* pvSource,void* pvDest,uint8_t ui8Size,uint32_t ui8Length)
{
	if (pvSource==pvDest)
		EndianConvertOrg(pvDest,ui8Size,ui8Length);
	else if (MY_LITTLE_ENDIAN&&ui8Size>1)
	{
		uint8_t const *pui8SourceLoop1,*pui8SourceLoop2;
		uint8_t *pui8DestLoop1,*pui8DestLoop2;
		for (
			pui8SourceLoop1=reinterpret_cast<uint8_t const*>(pvSource)+ui8Size*(ui8Length-1),pui8DestLoop1=reinterpret_cast<uint8_t*>(pvDest)+ui8Size*(ui8Length-1);
			pui8DestLoop1>=reinterpret_cast<uint8_t*>(pvDest);
			pui8SourceLoop1-=ui8Size,pui8DestLoop1-=ui8Size)
		{
			for (pui8SourceLoop2=pui8SourceLoop1,pui8DestLoop2=pui8DestLoop1+ui8Size-1;pui8DestLoop2>=pui8DestLoop1;++pui8SourceLoop2,--pui8DestLoop2)
				*pui8DestLoop2=*pui8SourceLoop2;
		}
	}
	else
		memcpy(pvDest,pvSource,ui8Size*ui8Length);
}

