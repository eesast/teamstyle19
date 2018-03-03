#pragma once
#include <mutex>

#include "CommunicateStruct.h"

struct sCommands
{
	uint8_t* apui8Command;
};

uint8_t* apui8Commands;

extern std::mutex mMutex;