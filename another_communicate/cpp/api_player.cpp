#include "CommunicateStruct.h"
#include "MyEndian.h"
#include "GlobalVar.h"
#include "MyTime.h"

#include "api_player.h"

void updateAge()
{
	struct sCommandData* pcdNewCommand=(struct sCommandData*)malloc(sizeof(uint32_t)+2*sizeof(uint16_t)+sizeof(uint8_t)+sizeof(uint32_t));
	pcdNewCommand->ui32Time=GetTime()-g_ui32TimeOut;
	EndianConvertDest(&pcdNewCommand->cCommands.ui16Length,(uint16_t)0u);
	EndianConvertDest(&pcdNewCommand->cCommands.ui16Round,g_ui16Turn);
	pcdNewCommand->cCommands.ui8Type=dstCommand+ctUpdateAge;

	g_mMutex.lock();
	while (g_mCommands[g_ui32CommandSerial])
		++g_ui32CommandSerial;
	g_mCommands[g_ui32CommandSerial]=pcdNewCommand;
	EndianConvertDest(&pcdNewCommand->cCommands.ui32Number,g_ui32CommandSerial);
	g_mMutex.unlock();
	++g_ui32CommandCount;
}

void construct(BuildingType building_type, Position pos, Position solider_pos)
{
	struct sCommandData* pcdNewCommand=(struct sCommandData*)malloc(sizeof(uint32_t)+2*sizeof(uint16_t)+sizeof(uint8_t)+sizeof(uint32_t)+sizeof(struct sConstruct));
	pcdNewCommand->ui32Time=GetTime()-g_ui32TimeOut;
	EndianConvertDest(&pcdNewCommand->cCommands.ui16Length,(uint16_t)sizeof(struct sConstruct));
	EndianConvertDest(&pcdNewCommand->cCommands.ui16Round,g_ui16Turn);
	pcdNewCommand->cCommands.ui8Type=dstCommand+ctConstruct;
	pcdNewCommand->cCommands.cConstruct.ui8Type=(uint8_t)building_type;
	pcdNewCommand->cCommands.cConstruct.aui8Position[0]=(uint8_t)pos.x;
	pcdNewCommand->cCommands.cConstruct.aui8Position[1]=(uint8_t)pos.y;
	pcdNewCommand->cCommands.cConstruct.aui8SoldierPosition[0]=(uint8_t)solider_pos.x;
	pcdNewCommand->cCommands.cConstruct.aui8SoldierPosition[1]=(uint8_t)solider_pos.y;

	g_mMutex.lock();
	while (g_mCommands[g_ui32CommandSerial])
		++g_ui32CommandSerial;
	g_mCommands[g_ui32CommandSerial]=pcdNewCommand;
	EndianConvertDest(&pcdNewCommand->cCommands.ui32Number,g_ui32CommandSerial);
	g_mMutex.unlock();
	++g_ui32CommandCount;
}

template<uint8_t ui8Type> static inline void Other(int unit_id)
{
	struct sCommandData* pcdNewCommand=(struct sCommandData*)malloc(sizeof(uint32_t)+2*sizeof(uint16_t)+sizeof(uint8_t)+2*sizeof(uint32_t));
	pcdNewCommand->ui32Time=GetTime()-g_ui32TimeOut;
	EndianConvertDest(&pcdNewCommand->cCommands.ui16Length,(uint16_t)sizeof(uint32_t));
	EndianConvertDest(&pcdNewCommand->cCommands.ui16Round,g_ui16Turn);
	pcdNewCommand->cCommands.ui8Type=ui8Type;
	EndianConvertDest(&pcdNewCommand->cCommands.ui32UnitId,(uint32_t)unit_id);

	g_mMutex.lock();
	while (g_mCommands[g_ui32CommandSerial])
		++g_ui32CommandSerial;
	g_mCommands[g_ui32CommandSerial]=pcdNewCommand;
	EndianConvertDest(&pcdNewCommand->cCommands.ui32Number,g_ui32CommandSerial);
	g_mMutex.unlock();
	++g_ui32CommandCount;
}

void upgrade(int unit_id)
{
	Other<dstCommand+ctUpgrade>(unit_id);
}

void sell(int unit_id)
{
	Other<dstCommand+ctSell>(unit_id);
}

void toggleMaintain(int unit_id)
{
	Other<dstCommand+ctToggleMaintain>(unit_id);
}
