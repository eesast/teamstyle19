import socket
import threading
import time
from  enum import  Enum
import numpy as np
from unit import Solider
import unit


CommandNum=100

class Command(Enum):
    UpdateAge=0
    Construct=1
    Upgrade=2
    Sell=3
    Maintain=4
    Noupdateage=5

class MainServer(object):
    def __init__(self,addr,post):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((addr, post))
        self.server.listen(2)

    def start_connection(self):
        count=0
        self.sock=[None,None]
        self.addr=[None,None]
        while count<2:
            self.sock[count],self.addr[count]=self.server.accept()
            count=count+1
            print('connect successfully!',self.addr)
        self.sock[0].send(b'0')
        self.sock[1].send(b'1')
        # sock[0]会发送一个map过来
        map1=self.sock[0].recv(200*200)  #size待调整
        map1=map1.decode('utf-8')
        map=[]
        for i in range(200):
            temp=map1[i*200:(i+1)*200]
            row=[]
            for num in temp:
                num=int(num)
                row.append(num)
            map.append(row)
        #对 byte的map处理 将其变成正常的
        self.sock[0].setblocking(0)
        self.sock[0].settimeout(0.01)
        self.sock[1].setblocking(0)
        self.sock[1].settimeout(0.01)
        self.sock[0].send(b'ok')
        self.sock[1].send(b'ok')
        return map

    def change_to_byte(self,status,building,unit):
        state=['','']
        for number in range(0,2):
            #在开头传入时代、资源、和建筑数目  时代、资源、建筑数目之间用,分割 大类之间用 ；分割
            state[number]=str(status[number]['money'])+','+str(status[number]['tech'])+','+str(status[number]['building'])+';'
            #之后传入建筑  Unit_ID Building_Type HP Position Is_Maintain 为所传属性 属性之间用空格分割 不同单位用,分隔
            for key in building[number]:
                for v in building[number][key]:
                    state[number]+=str(v.Unit_ID)+' '+str(v.BuildingType.value)+' '+str(v.HP)+' '+str(v.Position.x)+' '+str(v.Position.y)+' '+str(v.Is_Maintain)+','
            state[number]+=';'
            #再之后传入unit的信息 Unit_ID Solider_Name HP Position
            for v in unit:
                state+=str(v.Unit_ID)+' '+str(v.Solider_Name)+' '+str(v.HP)+' '+str(v.Position.x)+' '+str(v.Position.y)+','
            state+='#'
            state[number]=state[number].encode('utf-8')
        return state

    def send_state(self,status,building,unit):
        #将state0和state1处理成byte形式
        state=change_to_byte(status,building,unit)
        self.sock[0].setblocking(1)
        self.sock[1].setblocking(1)

        self.sock[0].send(state[0])
        self.sock[1].send(state[1])

        self.sock[0].setblocking(0)
        self.sock[0].settimeout(0.01)
        self.sock[1].setblocking(0)
        self.sock[1].settimeout(0.01)


    def recv_command(self):
        def listing_command(sock,command,flag):
            while flag[0]:
                try:
                    data=sock.recv(5)
                    data=data.decode('utf-8')
                    print(data)
                    if data=='start':
                        print('start!')
                        break
                except socket.timeout:
                    pass
            while flag[0]:
                try:
                    data=sock.recv(CommandNum*7+2) #size
                    data=data.decode('utf-8')
                    data=data.split(',')  #将commandid和unitid分离
                    command.append(data)
                    break
                except socket.timeout:
                    pass
            while flag[0]:  #接受传送过多的参数
                try:
                    data=sock.recv(1024)
                except socket.timeout:
                    pass

        command=[[],[]]
        flag=[True]
        th0=threading.Thread(target=listing_command,args=(self.sock[0],command[0],flag))
        th1=threading.Thread(target=listing_command,args=(self.sock[1],command[1],flag))
        th0.start()
        th1.start()
        time.sleep(0.2)
        flag[0]=False
        th0.join()
        th1.join()
        print('time end')
        print(command)
        command[0]=command[0][0]
        command[1]=command[1][0]
        l0=len(command[0])
        max0=51  #最大命令条数+1
        if command[0][0] is Command.UpdateAge.value:
            max0=max0-1
        if l0>max0:
            l0=max0
        for i in range(1,l0):
            v=command[0][i].split(' ')
            if v[0]!=Command.Construct.value:
                command[0][i]={'commandid':v[0],'unitid':v[1]}
            else:
                command[0][i]={'commandid':v[0],'unitid':v[1],'x':v[2],'y':v[3]}
        command[0]=command[0][0:l0]
        l1=len(command[1])
        max1=51  #最大命令条数+1
        if command[1][0] is Command.UpdateAge.value:
            max1=max1-1
        if l1>max1:
            l1=max1
        for i in range(1,l1):
            v=command[1][i].split(' ')
            v=command[1][i].split(' ')
            if v[0]!=str(Command.Construct.value):
                print(v[0])
                command[1][i]={'commandid':int(v[0]),'unitid':int(v[1])}
            else:
                command[1][i]={'commandid':int(v[0]),'unitid':int(v[1]),'x':int(v[2]),'y':int(v[3])}
        command[1]=command[1][0:l1]
        return command

mainserver=MainServer('127.0.0.1',9999)
t=unit.Position(7,7)
unit.Solider(100,t,0,0,1)

UUnit=[[],[]]
Building=[{'produce':[],'defence':[],'resource':[]},{'produce':[],'defence':[],'resource':[]}]
status = [{
    'money': 0,
    'tech': 0,
    'building': 0,
} for i in range(2)]
for i in range(0,2):
    for j in range(10):
        UUnit[i].append(unit.Solider(unit.SoliderName.PACKET.value,100,unit.Position(6,6),i,j))
        Building[i]['produce'].append(unit.Building(unit.BuildingType.Hawkin,unit.Position(7,7),i,j+10,0,unit.Age.NETWORK.value))
        Building[i]['defence'].append(unit.Building(unit.BuildingType.Hawkin,unit.Position(7,7),i,j+20,0,unit.Age.NETWORK.value))
        Building[i]['defence'].append(unit.Building(unit.BuildingType.Hawkin,unit.Position(7,7),i,j+30,0,unit.Age.NETWORK.value))
state=mainserver.change_to_byte(status,Building,UUnit)
print(state[0])
print(state[1])

