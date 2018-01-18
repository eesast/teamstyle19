#include "CommunicateStruct.h"

struct in_addr const g_iaServerAddr={0x7f,0x00,0x00,0x01};
u_short const g_usServerPort=48222;

std::map<uint32_t,struct sCommandData*> g_mCommands;
uint32_t g_ui32CommandSerial;
uint32_t g_ui32CommandCount;
std::mutex g_mMutex;