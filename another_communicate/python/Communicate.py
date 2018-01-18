import socket
import struct
import time
from gamemain import *

#parameter
sAddress='127.0.0.1'
iPort=48222
iSendCount=100
iResendTime=10
iRoundTime=1000

#static
drtMap=0
drtUnitCount=1
drtUnit=2
drtStart=3
drtConfirm=128

utSoldier=0
utBuilding=1

dstConnect=0
dstCommandLength=1
dstCommand=2
dstConfirm=128

ctUpdateAge=0
ctConstruct=1
ctUpgrade=2
ctSell=3
ctToggleMaintain=4
#static


gGame=GameMain()

#player address
adPlayers=[0,0];

sSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sSocket.bind((sAddress,iPort))

sHead=struct.Struct('>2HB')
bMap=bytearray(5000)
for iLoop1 in range(gGame._map_size):
    for iLoop2 in range(round(gGame._map_size/8)):
        bMap[iLoop1*round(gGame._map_size/8)+iLoop2]=(0x80 if gGame._map[iLoop1][iLoop2<<3] else 0)|(0x40 if gGame._map[iLoop1][iLoop2<<3|1] else 0)|(0x20 if gGame._map[iLoop1][iLoop2<<3|2] else 0)|(0x10 if gGame._map[iLoop1][iLoop2<<3|3] else 0)|(0x08 if gGame._map[iLoop1][iLoop2<<3|4] else 0)|(0x04 if gGame._map[iLoop1][iLoop2<<3|5] else 0)|(0x02 if gGame._map[iLoop1][iLoop2<<3|6] else 0)|(0x01 if gGame._map[iLoop1][iLoop2<<3|7] else 0)

GetTime=lambda:int(round(time.time()*1000))

def AddData(lPack:list,iCount):
    while lPack[3]<4 and len([gGame.units[lPack[2]],gGame.buildings[lPack[2]]['produce'],gGame.buildings[lPack[2]]['defence'],gGame.buildings[lPack[2]]['resource']][lPack[3]])<=lPack[1]:
        lPack[2]+=1
        lPack[1]=0
        if lPack[2]>=2:
            if not lPack[3]:
                lPack[4]=0
            lPack[2]=0
            lPack[3]+=1
    iLoop2=0
    while lPack[3]<4 and iLoop2<iCount:
        bSpace=[gGame.units[lPack[2]],gGame.buildings[lPack[2]]['produce'],gGame.buildings[lPack[2]]['defence'],gGame.buildings[lPack[2]]['resource']][lPack[3]][lPack[1]]
        if lPack[3]:
            lPack[0][(drtUnit+utBuilding,lPack[4])]=[GetTime(),sHead.pack(17,gGame.turn_num,drtUnit+utBuilding)+struct.Struct('>I4B2IB').pack(lPack[4],bSpace.BuildingType,bSpace.Flag,bSpace.Position.x,bSpace.Position.y,bSpace.HP,bSpace.Unit_ID,1 if bSpace.Is_Maintain else 0)]
        else:
            lPack[0][(drtUnit+utSoldier,lPack[4])]=[GetTime(),sHead.pack(12,gGame.turn_num,drtUnit+utSoldier)+struct.Struct('>I4BI').pack(lPack[4],bSpace.Solider_Name,bSpace.Flag,bSpace.Position.x,bSpace.Position.y,bSpace.HP)]

        lPack[1]+=1
        lPack[4]+=1

        while lPack[3]<4 and len([gGame.units[lPack[2]],gGame.buildings[lPack[2]]['produce'],gGame.buildings[lPack[2]]['defence'],gGame.buildings[lPack[2]]['resource']][lPack[3]])<=lPack[1]:
            lPack[2]+=1
            lPack[1]=0
            if lPack[2]>=2:
                if not lPack[3]:
                    lPack[4]=0
                lPack[2]=0
                lPack[3]+=1
    return iLoop2
sSocket.setblocking(False)

lMessageList=[]

aSendBuffer=[[{},0,0,0,0],[{},0,0,0,0]]
aSendBuffer[0][0][drtUnitCount]=[GetTime(),sHead.pack(8,0,drtUnitCount)+struct.Struct('>2I').pack(len(gGame.units[0])+len(gGame.units[1]),sum(len(b['produce'])+len(b['defence'])+len(b['resource']) for b in gGame.buildings))]
aSendBuffer[1][0][drtUnitCount]=[GetTime(),sHead.pack(8,0,drtUnitCount)+struct.Struct('>2I').pack(len(gGame.units[0])+len(gGame.units[1]),sum(len(b['produce'])+len(b['defence'])+len(b['resource']) for b in gGame.buildings))]

while gGame.turn_num<100:
    #iCurrent iPlayer iClass iLoop1

    bClear=[0,0]
    lCommandLength=[[0xffffff,set()],[0xffffff,set()]]

    AddData(aSendBuffer[0],iSendCount-1)
    AddData(aSendBuffer[1],iSendCount-1)

    iTime=GetTime()+iRoundTime

    while not adPlayers[0] or not adPlayers[1] or ((lCommandLength[0][0]>len(lCommandLength[0][1]) or lCommandLength[1][0]>len(lCommandLength[1][1])) and GetTime()<iTime):
        while True:
            try:
                dData,adAddr=sSocket.recvfrom(2048)
            except BlockingIOError:
                break
            except BaseException:
                break
            if len(dData)<5:
                print("Wrong size1")
                continue
            dHead=list(sHead.unpack(dData[:5]))

            if dHead[1]!=gGame.turn_num:
#                print("Old Data %s"%(str(dHead)))
                continue
            if dHead[2]==dstConnect:
                if adAddr==adPlayers[0] or adAddr==adPlayers[1]:
                    print("Re request")
                    lMessageList+=[(sHead.pack(501,0,drtMap)+struct.pack("B",i<<1|(0 if adAddr==adPlayers[0] else 1))+bMap[i*500:(i+1)*500],adAddr) for i in range(10)]
                elif not adPlayers[0]:
                    adPlayers[0]=adAddr
                    print("Player 0 Joined");
                    lMessageList+=[(sHead.pack(501,0,drtMap)+struct.pack("B",i<<1)+bMap[i*500:(i+1)*500],adAddr) for i in range(10)]
                elif not adPlayers[1]:
                    adPlayers[1]=adAddr
                    print("Player 1 Joined");
                    lMessageList+=[(sHead.pack(501,0,drtMap)+struct.pack("B",i<<1|1)+bMap[i*500:(i+1)*500],adAddr) for i in range(10)]
                    iTime=GetTime()+iRoundTime
                    break;
                else:
                    print("No more space")
            elif adAddr in adPlayers:
                if dHead[2]==dstCommandLength:
                    lMessageList+=[(sHead.pack(0,dHead[1],drtConfirm|dHead[2]),adAddr)]
                    lCommandLength[adPlayers.index(adAddr)][0]=struct.Struct('>I').unpack(dData[5:9])[0];
                elif dHead[2]&dstConfirm:
                    dHead[2]^=dstConfirm
                    if dHead[2]==drtMap:
                        print("Player %d map received"%(adPlayers.index(adAddr)))
                    elif dHead[2]==drtUnitCount:
                        if drtUnitCount in aSendBuffer[adPlayers.index(adAddr)][0].keys():
                            del aSendBuffer[adPlayers.index(adAddr)][0][drtUnitCount]
                            if AddData(aSendBuffer[adPlayers.index(adAddr)],1)<1 and bClear[adPlayers.index(adAddr)]==0:
                                bClear[adPlayers.index(adAddr)]=1
                    else:
                        bSpace=struct.Struct('>I').unpack(dData[5:9])
                        if (dHead[2],bSpace[0]) in aSendBuffer[adPlayers.index(adAddr)][0].keys():
                            del aSendBuffer[adPlayers.index(adAddr)][0][(dHead[2],bSpace[0])]
                            if AddData(aSendBuffer[adPlayers.index(adAddr)],1)<1 and bClear[adPlayers.index(adAddr)]==0:
                                bClear[adPlayers.index(adAddr)]=1
                        else:
                            print("Unknown unit")
                elif dHead[2]>=dstCommand and dHead[2]<=dstCommand+ctToggleMaintain and dHead[1]==gGame.turn_num:
                    #Confirm
                    lMessageList+=[(sHead.pack(4,dHead[1],drtConfirm|dHead[2])+dData[5:9],adAddr)]
                    if not dData[5:9] in lCommandLength[adPlayers.index(adAddr)][1]:
                        lCommandLength[adPlayers.index(adAddr)][1].add(dData[5:9])
                    dHead[2]-=dstCommand
                    if dHead[2]==ctUpdateAge:
                        gGame.raw_instruments[adPlayers.index(adAddr)]['update_age']=True
                    elif dHead[2]==ctConstruct:
                        if len(dData)>=14:
                            bSpace=struct.Struct('5B').unpack(dData[9:14])
                            if not bSpace in gGame.raw_instruments[adPlayers.index(adAddr)]['construct']:
                                gGame.raw_instruments[adPlayers.index(adAddr)]['construct'].append((bSpace[0],bSpace[1:3],bSpace[3:5]))
                    elif len(dData)>=13:
                        bSpace=struct.Struct('>I').unpack(dData[9:13])[0]
                        if not bSpace in gGame.raw_instruments[adPlayers.index(adAddr)][['upgrade','sell','maintain'][dHead[2]-ctUpgrade]]:
                            gGame.raw_instruments[adPlayers.index(adAddr)][['upgrade','sell','maintain'][dHead[2]-ctUpgrade]].append(bSpace)
            else:
                print("Unknown player")

        for iMessage in lMessageList:
            sSocket.sendto(*iMessage)
        lMessageList.clear()
        
        for iPlayer in range(2):
            if adPlayers[iPlayer]:
                for i in aSendBuffer[iPlayer][0].values():
                    if iTime-i[0]>iResendTime:
                        if sSocket.sendto(i[1],adPlayers[iPlayer])==len(i[1]):
                            i[0]=iTime
                        else:
                            break
    print("hi!%d-------------------------------------"%gGame.turn_num)
    print(gGame.raw_instruments)
    gGame.next_tick()
    gGame.turn_num+=1
    print("hj!%d-------------------------------------"%gGame.turn_num)
    aSendBuffer=[[{},0,0,0,0],[{},0,0,0,0]]
    '''
    #
    gGame.units[0]=[Solider(SoliderName.BIT_STREAM.value,10,Position(10,10),0)]
    gGame.buildings[0]['produce']=[Building(BuildingType.Base.value,100,Position(10,10),1,100,False)]
    #
    '''
    aSendBuffer[0][0][drtUnitCount]=[GetTime(),sHead.pack(8,gGame.turn_num,drtUnitCount)+struct.Struct('>2I').pack(len(gGame.units[0])+len(gGame.units[1]),sum(len(b['produce'])+len(b['defence'])+len(b['resource']) for b in gGame.buildings))]
    aSendBuffer[1][0][drtUnitCount]=[GetTime(),sHead.pack(8,gGame.turn_num,drtUnitCount)+struct.Struct('>2I').pack(len(gGame.units[0])+len(gGame.units[1]),sum(len(b['produce'])+len(b['defence'])+len(b['resource']) for b in gGame.buildings))]
