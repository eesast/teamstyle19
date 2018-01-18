#pragma once
#include <stdint.h>
#include <mutex>
#include <map>

#include "MySocket.h"

extern struct  in_addr const g_iaServerAddr;
extern u_short const g_usServerPort;

//Transfer--------------------------------------------
#pragma pack(1)
struct sDataTransfer
{
	uint16_t ui16Length;
	uint16_t ui16Round;
	uint8_t ui8Type;
	uint8_t aui8Data[1];
};
#pragma pack()


//Receive---------------------------------------------
enum eDataReceivedType
{
	drtMap=0,
	drtUnitCount=1,
	drtUnit=2,
	drtStart=3,
	drtConfirm=128
};

enum eUnitType
{
	utSoldier=0,
	utBuilding=1
};

#pragma pack(1)
struct sSoldier
{
	uint8_t ui8Name;
	uint8_t ui8Flag;
	uint8_t aui8Position[2];
	uint32_t ui32Health;
};

struct sBuilding
{
	uint8_t ui8Type;
	uint8_t ui8Flag;
	uint8_t aui8Position[2];
	uint32_t ui32Health;
	uint32_t ui32UnitId;
	uint8_t ui8Maintain;
};
#pragma pack()

//Send------------------------------------------------
enum eDataSendType
{
	dstConnect=0,
	dstCommandLength=1,
	dstCommand=2,
	dstConfirm=128
};

enum eCommandType
{
	ctUpdateAge=0,
	ctConstruct=1,
	ctUpgrade=2,
	ctSell=3,
	ctToggleMaintain=4
};

#pragma pack(1)
struct sConstruct
{
	uint8_t ui8Type;
	uint8_t aui8Position[2];
	uint8_t aui8SoldierPosition[2];
};

struct sCommand
{
	uint16_t ui16Length;
	uint16_t ui16Round;
	uint8_t ui8Type;
	uint32_t ui32Number;
	union
	{
		struct sConstruct cConstruct;
		uint32_t ui32UnitId;
	};
};

struct sCommandData
{
	uint32_t ui32Time;
	sCommand cCommands;
};
#pragma pack()

//200
extern std::map<uint32_t,struct sCommandData*> g_mCommands;
extern uint32_t g_ui32CommandSerial;
extern uint32_t g_ui32CommandCount;
extern std::mutex g_mMutex;