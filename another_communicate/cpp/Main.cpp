#include <WinSock.h>
#include <stdint.h>
#include <limits.h>
#include <stdio.h>
#include <memory.h>
#include <thread>
#include "api_player.h"

#include "CommunicateStruct.h"
#include "MyEndian.h"
#include "MyTime.h"
#include "GlobalVar.h"

#pragma comment(lib,"wsock32.lib")

/*
#define SOCKET int
#define SOCKET_ERROR -1
*/

struct sDataToSend
{
	struct sDataTransfer* pdtData;
	uint16_t ui16Length;
	uint32_t ui32Time;
	struct sDataToSend* pdtsNext;
};

void AddData(struct sDataToSend*** pppdtsLast,struct sDataTransfer* pdt8Data,uint16_t ui16Length)
{
	struct sDataToSend* pdtsNew=(struct sDataToSend*)malloc(sizeof(struct sDataToSend));
	pdtsNew->pdtData=pdt8Data;
	pdtsNew->ui16Length=ui16Length;
	pdtsNew->ui32Time=GetTime()-g_ui32TimeOut;
	pdtsNew->pdtsNext=NULL;

	**pppdtsLast=pdtsNew;
	*pppdtsLast=&pdtsNew->pdtsNext;
}

#define socklen_t int
#define ssize_t int

void Test();

void Call(uint8_t* pui8Finish)
{
	//PlayerMain
	printf("Turn %hu\n",g_ui16Turn);

	Test();
	*pui8Finish=0;
}

static int seed=(int)time(0);

void Test()
{
	for (uint32_t ui32Loop=0;ui32Loop<g_ui32SolidersCount;++ui32Loop)
	{
		printf("s:%u %u %u %u %u\n",
			g_asSoldiers[ui32Loop].solider_name,
			g_asSoldiers[ui32Loop].heal,
			g_asSoldiers[ui32Loop].pos.x,
			g_asSoldiers[ui32Loop].pos.y,
			g_asSoldiers[ui32Loop].flag);
	}

	for (uint32_t ui32Loop=0;ui32Loop<g_ui32BuildingsCount;++ui32Loop)
	{
		printf("b:%u %u %u %u %u %u %u\n",
			g_abBuildings[ui32Loop].building_type,
			g_abBuildings[ui32Loop].flag,
			g_abBuildings[ui32Loop].heal,
			g_abBuildings[ui32Loop].maintain,
			g_abBuildings[ui32Loop].pos.x,
			g_abBuildings[ui32Loop].pos.y,
			g_abBuildings[ui32Loop].unit_id);
	}
	srand(seed);
	{
		int a[2]={rand()%100,rand()%90};
		construct(Shannon,Position(a[0],a[1]),Position(a[0],a[1]+1));
		updateAge();
		printf("construct %d %d\n",a[0],a[1]);
		a[0]=rand()%100;
		a[1]=rand()%100;
		upgrade(a[0]);
		sell(a[1]);
		printf("upgrade %d\n",a[0]);
		printf("sell %d\n",a[1]);
		a[0]=rand()%100;
		toggleMaintain(a[0]);
		printf("toggle Maintain %d\n",a[0]);
	}
	seed=rand();
}

int main(int argc,char* argv[])
{
	uint8_t aui8Buffer[1000];
	uint8_t ui8Team=UINT8_MAX;
	uint8_t aui8Map[5000];
	uint8_t aui8MapReceived[2]={0u};
	uint16_t ui16Round=0;
	struct sDataTransfer* pdtBuffer=(struct sDataTransfer*)aui8Buffer;
	struct sockaddr_in saiServer={AF_INET,htons(g_usServerPort),g_iaServerAddr};
	struct sockaddr_in saiSocket;
	socklen_t slAddrLen;
	fd_set fsReadSet;
	SOCKET sSocket;
	struct timeval tvTimeOut={0u,100u};
	struct Solider* asSoldiers=(struct Solider*)malloc(MAX_SOLDIERS*sizeof(struct Solider));
	struct Building* abBuildings=(struct Building*)malloc(MAX_BUILDINGS*sizeof(struct Building));
	g_asSoldiers=(struct Solider*)malloc(MAX_SOLDIERS*sizeof(struct Solider));
	g_abBuildings=(struct Building*)malloc(MAX_BUILDINGS*sizeof(struct Building));
	memset(asSoldiers,0xff,MAX_SOLDIERS*sizeof(struct Solider));
	memset(abBuildings,0xff,MAX_BUILDINGS*sizeof(struct Building));

	uint32_t aaui32Count[2][2]={{UINT32_MAX,UINT32_MAX},{0,0}};

	struct sDataToSend *pdtsFirst=NULL,**ppdtsLast=&pdtsFirst;
	struct sDataToSend *pdtsMark;

	uint8_t ui8Processing=0u;
	uint8_t ui8Finish=1u;
	ssize_t sSize=0;

	WSADATA dWsaData;
	int iError;

	WSAStartup(MAKEWORD(1,1),&dWsaData);
	sSocket=socket(AF_INET,SOCK_DGRAM,0);
	{
		unsigned long on_windows=1;  
	    ioctlsocket(sSocket, FIONBIO, &on_windows);
	}

	//FirstBeep
	{
		struct sDataTransfer* pdtData=(struct sDataTransfer*)malloc(sizeof(struct sDataTransfer)-sizeof(uint8_t));
		pdtData->ui16Length=0;
		pdtData->ui16Round=0;
		pdtData->ui8Type=dstConnect;
		AddData(&ppdtsLast,pdtData,sizeof(struct sDataTransfer)-sizeof(uint8_t));
	}

	while (true)
	{
		FD_ZERO(&fsReadSet);
		FD_SET(sSocket,&fsReadSet);
		if (select(INT_MAX,&fsReadSet,NULL,NULL,&tvTimeOut)!=SOCKET_ERROR&&FD_ISSET(sSocket,&fsReadSet))
		{
			slAddrLen=sizeof(struct sockaddr_in);
			while (
				(sSize=recvfrom(sSocket,(char*)aui8Buffer,sizeof(aui8Buffer),0,reinterpret_cast<sockaddr*>(&saiSocket),&slAddrLen))!=SOCKET_ERROR
				)
			{
				printf("Receive:%d\n",pdtBuffer->ui8Type);
				if (sSize!=*EndianConvert(&pdtBuffer->ui16Length,1)+sizeof(uint16_t)+sizeof(uint16_t)+sizeof(uint8_t))
				{
					printf("Wrong Size\n");
					break;
				}
				if (EndianConvert(pdtBuffer->ui16Round)>ui16Round)
				{
					printf("New round--------------------------\n");
					EndianConvertDest(&ui16Round,pdtBuffer->ui16Round);
					aaui32Count[0][0]=aaui32Count[0][1]=UINT32_MAX;
					aaui32Count[1][0]=aaui32Count[1][1]=0;
					//Clean Units;
					memset(asSoldiers,0xff,MAX_SOLDIERS*sizeof(struct Solider));
					memset(abBuildings,0xff,MAX_BUILDINGS*sizeof(struct Building));

					//ClearOldCommand
					for (ppdtsLast=&pdtsFirst;*ppdtsLast;)
					{
						if (EndianConvert((*ppdtsLast)->pdtData->ui16Round)<ui16Round)
						{
							struct sDataToSend* pdtsSpace=*ppdtsLast;
							*ppdtsLast=(*ppdtsLast)->pdtsNext;
							free(pdtsSpace->pdtData);
							free(pdtsSpace);
						}
						else
							ppdtsLast=&(*ppdtsLast)->pdtsNext;
					}
					ui8Finish=0u;
				}
				if (EndianConvert(pdtBuffer->ui16Round)<ui16Round&&pdtBuffer->ui8Type!=drtMap)
				{
					printf("OldUnit");
					continue;
				}
				switch (pdtBuffer->ui8Type)
				{
				case drtMap:
					if (pdtBuffer->ui16Length==501*sizeof(uint8_t))
					{
						uint8_t ui8Num=*pdtBuffer->aui8Data>>1;
						ui8Team=*pdtBuffer->aui8Data&0x01;
						memcpy(aui8Map+ui8Num*500,pdtBuffer->aui8Data+1,500*sizeof(uint8_t));
						aui8MapReceived[ui8Num>>3]|=1<<(ui8Num&0x07);
						if (aui8MapReceived[0]==0xff&&aui8MapReceived[1]==0x03)
						{
							//ClearConnectRequest
							for (ppdtsLast=&pdtsFirst;*ppdtsLast;)
							{
								if ((*ppdtsLast)->pdtData->ui8Type==dstConnect)
								{
									struct sDataToSend* pdtsSpace=*ppdtsLast;
									*ppdtsLast=(*ppdtsLast)->pdtsNext;
									free(pdtsSpace->pdtData);
									free(pdtsSpace);
								}
								else
									ppdtsLast=&(*ppdtsLast)->pdtsNext;
							}
							//Confirm
							{
								struct sDataTransfer* pdtData=(struct sDataTransfer*)malloc(sizeof(struct sDataTransfer)-sizeof(uint8_t));
								pdtData->ui16Length=0;
								pdtData->ui16Round=pdtBuffer->ui16Round;
								pdtData->ui8Type=pdtBuffer->ui8Type|dstConfirm;
								AddData(&ppdtsLast,pdtData,sizeof(struct sDataTransfer)-sizeof(uint8_t)+sizeof(uint32_t));
							}
							printf("Map Finish\n");
						}
					}
					else
						printf("dtMap BadSize\n");
					break;
				case drtUnitCount:
					if (pdtBuffer->ui16Length==sizeof(uint32_t)*2)
					{
						EndianConvertOrg(pdtBuffer->aui8Data,aaui32Count[0],sizeof(uint32_t),2);
						printf("Unit Count %u %u\n",aaui32Count[0][0],aaui32Count[0][1]);
						if (aaui32Count[0][0]>MAX_SOLDIERS)
						{
							printf("So many soldiers %u\n",aaui32Count[0][0]);
							aaui32Count[0][0]=MAX_SOLDIERS;
						}
						if (aaui32Count[0][1]>MAX_BUILDINGS)
						{
							printf("So many buildings %u\n",aaui32Count[0][1]);
							aaui32Count[0][1]=MAX_BUILDINGS;
						}
						//Confirm
						{
							struct sDataTransfer* pdtData=(struct sDataTransfer*)malloc(sizeof(struct sDataTransfer)-sizeof(uint8_t));
							pdtData->ui16Length=0;
							pdtData->ui16Round=pdtBuffer->ui16Round;
							pdtData->ui8Type=pdtBuffer->ui8Type|dstConfirm;
							AddData(&ppdtsLast,pdtData,sizeof(struct sDataTransfer)-sizeof(uint8_t)+sizeof(uint32_t));
						}
					}
					break;
				case drtConfirm|dstCommandLength:
					for (ppdtsLast=&pdtsFirst;*ppdtsLast;)
					{
						if ((*ppdtsLast)->pdtData->ui8Type==dstCommandLength)
						{
							struct sDataToSend* pdtsSpace=*ppdtsLast;
							*ppdtsLast=(*ppdtsLast)->pdtsNext;
							free(pdtsSpace->pdtData);
							free(pdtsSpace);
						}
						else
							ppdtsLast=&(*ppdtsLast)->pdtsNext;
					}
					printf("Round Over\n");
					break;
				default:
					if (pdtBuffer->ui16Length>=sizeof(uint32_t))
					{
						uint32_t const ui32Number=EndianConvert(*reinterpret_cast<uint32_t*>(pdtBuffer->aui8Data));
						switch (pdtBuffer->ui8Type-drtUnit)
						{
						case utSoldier:
							if (ui32Number<aaui32Count[0][0]&&pdtBuffer->ui16Length==sizeof(uint32_t)+sizeof(struct sSoldier))
							{
								if (asSoldiers[ui32Number].solider_name==~(SoliderName)0)
								{
									struct sSoldier const& sMySoldier=*reinterpret_cast<struct sSoldier const*>(pdtBuffer->aui8Data+sizeof(uint32_t));
									asSoldiers[ui32Number].solider_name=(SoliderName)sMySoldier.ui8Name;
									asSoldiers[ui32Number].flag=sMySoldier.ui8Flag;
									asSoldiers[ui32Number].pos.x=sMySoldier.aui8Position[0];
									asSoldiers[ui32Number].pos.y=sMySoldier.aui8Position[1];
									asSoldiers[ui32Number].heal=EndianConvert(sMySoldier.ui32Health);
									++aaui32Count[1][0];
									//Confirm
									{
										struct sDataTransfer* pdtData=(struct sDataTransfer*)malloc(sizeof(struct sDataTransfer)-sizeof(uint8_t)+sizeof(uint32_t));
										pdtData->ui16Length=0;
										pdtData->ui16Round=pdtBuffer->ui16Round;
										pdtData->ui8Type=pdtBuffer->ui8Type|dstConfirm;
										EndianConvertDest(reinterpret_cast<uint32_t*>(pdtData->aui8Data),ui32Number);
										AddData(&ppdtsLast,pdtData,sizeof(struct sDataTransfer)-sizeof(uint8_t)+sizeof(uint32_t));
									}
									printf("pass soldier %u\n",ui32Number);
								}
								else
									printf("Re pass soldier %u %u %u\n",ui32Number,asSoldiers[ui32Number].solider_name,~(SoliderName)0);
							}
							else
								printf("Wrong soldier data %u %u %u %u\n",ui32Number,aaui32Count[0][0],pdtBuffer->ui16Length,sizeof(uint32_t)+sizeof(struct sSoldier));
							break;
						case utBuilding:
							if (ui32Number<aaui32Count[0][1]&&pdtBuffer->ui16Length==sizeof(uint32_t)+sizeof(struct sBuilding))
							{
								if (abBuildings[ui32Number].building_type==~(BuildingType)0)
								{
									struct sBuilding const& sMyBuilding=*reinterpret_cast<struct sBuilding const*>(pdtBuffer->aui8Data+sizeof(uint32_t));
									abBuildings[ui32Number].building_type=(BuildingType)sMyBuilding.ui8Type;
									abBuildings[ui32Number].heal=EndianConvert(sMyBuilding.ui32Health);
									abBuildings[ui32Number].pos.x=sMyBuilding.aui8Position[0];
									abBuildings[ui32Number].pos.y=sMyBuilding.aui8Position[1];
									abBuildings[ui32Number].flag=sMyBuilding.ui8Flag;
									abBuildings[ui32Number].unit_id=EndianConvert(sMyBuilding.ui32UnitId);
									abBuildings[ui32Number].maintain=sMyBuilding.ui8Maintain!=0;
									++aaui32Count[1][1];
									//Confirm
									{
										struct sDataTransfer* pdtData=(struct sDataTransfer*)malloc(sizeof(struct sDataTransfer)-sizeof(uint8_t)+sizeof(uint32_t));
										pdtData->ui16Length=0;
										pdtData->ui16Round=pdtBuffer->ui16Round;
										pdtData->ui8Type=pdtBuffer->ui8Type|dstConfirm;
										EndianConvertDest(reinterpret_cast<uint32_t*>(pdtData->aui8Data),ui32Number);
										AddData(&ppdtsLast,pdtData,sizeof(struct sDataTransfer)-sizeof(uint8_t)+sizeof(uint32_t));
									}
								}
								else
									printf("Re pass building %u\n",ui32Number);
							}
							else
								printf("Wrong building data %u %u %u %u\n",ui32Number,aaui32Count[0][1],pdtBuffer->ui16Length,sizeof(uint32_t)+sizeof(struct sBuilding));
							break;
						default:
							if ((pdtBuffer->ui8Type&~drtConfirm)>=dstCommand)
							{
								g_mMutex.lock();
								if (g_mCommands.find(ui32Number)!=g_mCommands.end())
								{
									free(g_mCommands[ui32Number]);
									g_mCommands.erase(ui32Number);
								}
								g_mMutex.unlock();
							}
							else
								printf("Unknown data type\n");
						};
					}
				};
			}
		}
		//Send
		{
			uint32_t ui32Time=GetTime();
			pdtsMark=NULL;
			while (pdtsFirst)
			{
				if (ui32Time-pdtsFirst->ui32Time>g_ui32TimeOut)
				{
					if ((sSize=sendto(sSocket,(char const*)pdtsFirst->pdtData,pdtsFirst->ui16Length,0,(sockaddr const*)&saiServer,sizeof(sockaddr_in)))==pdtsFirst->ui16Length)
					{
						if (pdtsFirst->pdtData->ui8Type&dstConfirm)
						{
							struct sDataToSend* pdtsSpace=pdtsFirst;
							pdtsFirst=pdtsFirst->pdtsNext;
							free(pdtsSpace->pdtData);
							free(pdtsSpace);
						}
						else
						{
							pdtsFirst->ui32Time=ui32Time;
							if (pdtsFirst->pdtsNext)
							{
								*ppdtsLast=pdtsFirst;
								pdtsFirst=pdtsFirst->pdtsNext;
								ppdtsLast=&((*ppdtsLast)->pdtsNext=NULL);
							}
						}
					}
					else
					{
						if ((iError=WSAGetLastError())!=EWOULDBLOCK)
							printf("Error %d\n",iError);
						break;
					}
				}
				else
				{
					if (!pdtsMark)
						pdtsMark=pdtsFirst;
					else if (pdtsFirst==pdtsFirst)
						break;
					if (pdtsFirst->pdtsNext)
					{
						*ppdtsLast=pdtsFirst;
						pdtsFirst=pdtsFirst->pdtsNext;
						ppdtsLast=&((*ppdtsLast)->pdtsNext=NULL);
					}
				}
			}
			if (!pdtsFirst)
			{
				ppdtsLast=&pdtsFirst;
			}
			//SendCommands
			g_mMutex.lock();
			{
				uint16_t ui16Space;
				for (std::map<uint32_t,struct sCommandData*>::iterator imData=g_mCommands.begin();imData!=g_mCommands.end();++imData)
				{
					if (ui32Time-imData->second->ui32Time>g_ui32TimeOut)
					{
						ui16Space=EndianConvert(imData->second->cCommands.ui16Length)+2*sizeof(uint16_t)+sizeof(uint8_t)+sizeof(uint32_t);

						if (sendto(sSocket,(char const*)&imData->second->cCommands,ui16Space,0,(sockaddr const*)&saiServer,sizeof(struct sockaddr_in))==ui16Space)
						{
							imData->second->ui32Time=ui32Time;
						}
						else
							break;
					}
				}
			}
			g_mMutex.unlock();

			if (!ui8Processing)
			{
				if (g_ui16Turn<ui16Round)
				{
					if (!memcmp(aaui32Count[0],aaui32Count[1],2*sizeof(uint32_t)))
					{
						printf("Run %u\n",ui16Round);
						g_ui16Turn=ui16Round;
						g_ui32SolidersCount=aaui32Count[0][0];
						g_ui32BuildingsCount=aaui32Count[0][1];
						ui8Processing=1;
						memcpy(g_asSoldiers,asSoldiers,sizeof(struct Solider)*aaui32Count[0][0]);
						memcpy(g_abBuildings,abBuildings,sizeof(struct Building)*aaui32Count[0][1]);
						g_ui32CommandCount=0;
						std::thread(Call,&ui8Processing).detach();
					}
				}
				else if (!ui8Finish)
				{
					struct sDataTransfer* pdtData=(struct sDataTransfer*)malloc(sizeof(struct sDataTransfer)-sizeof(uint8_t)+sizeof(uint32_t));
					EndianConvertDest(&pdtData->ui16Length,(uint16_t)sizeof(uint32_t));
					EndianConvertDest(&pdtData->ui16Round,ui16Round);
					pdtData->ui8Type=dstCommandLength;
					EndianConvertDest((uint32_t*)pdtData->aui8Data,g_ui32CommandCount);
					AddData(&ppdtsLast,pdtData,sizeof(struct sDataTransfer)-sizeof(uint8_t)+sizeof(uint32_t));

					ui8Finish=1;
				}
			}
		}
	}
	WSACleanup();
	return 0;
}

