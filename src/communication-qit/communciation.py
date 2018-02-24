import socket
import threading
import time
from  enum import  Enum
import unit
from unit import Position

CommandNum=100

#API : start connection  send_state recv_state

class Command(Enum):
    UpdateAge=0 #升级时代指令
    Construct=1
    Upgrage=2
    Sell=3
    Maintain=4
    Noupdateage=5   #不升级时代指令

_mapsize=200

class MainServer(object):
    def __init__(self,addr,post):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #创建socket 指定通信类型
        self.server.bind((addr, post))
        self.server.listen(2)

    def change_map(self,map0):  #将map以行为优先进行展开
        map=str()
        for i in range(_mapsize):
            for j in range(_mapsize):
                map+=str(map0[i][j])
        map=map.encode('utf-8')
        return map

    def start_connection(self,map0): #把map传入 传给两个玩家 map为200*200
        count=0
        self.sock=[None,None]   #存放两个玩家的sock
        self.addr=[None,None]   #存放两个玩家的地址
        while count<2:  #循环两次 等待两个玩家全部成功连接
            self.sock[count],self.addr[count]=self.server.accept()
            count=count+1
            print('connect successfully!',self.addr)
        self.sock[0].send(b'0') #给玩家发送消息 告诉他们的编号
        self.sock[1].send(b'1')
        map0=self.change_map(map0)
        print(map0)
        print('the lenght:',len(map0))
        self.sock[0].send(map0)
        self.sock[1].send(map0)
        self.sock[0].setblocking(0)  #将sock都设置成非阻塞模式 为了和之后的记时配合
        self.sock[0].settimeout(0.01)
        self.sock[1].setblocking(0)
        self.sock[1].settimeout(0.01)
        self.sock[0].send(b'ok')
        self.sock[1].send(b'ok')

    def change_to_byte(self,turn,status,building,unit,winner):  #将要发送给玩家的状态变成byte流
        state=['','']
        for number in range(0,2):
            #在开头传入时代、资源、和建筑点数  时代、资源、建筑数目之间用,分割 大类之间用 ；分割
            state[number]=str(status[number]['money'])+','+str(status[number]['tech'])+','+str(status[number]['building'])+';'
            #之后传入建筑  Unit_ID Building_Type HP Position Is_Maintain 为所传属性 属性之间用空格分割 不同单位用,分隔
            for key in building[number]:
                for v in building[number][key]:
                    state[number]+=str(v.Unit_ID)+' '+str(v.BuildingType.value)+' '+str(v.HP)+' '+str(v.Position.x)+' '+str(v.Position.y)+' '+str(v.Is_Maintain)+','
            state[number]+=';'
            #再之后传入unit的信息 Unit_ID Solider_Name HP Position
            for v in unit[number]:
                state[number]+=str(v.Unit_ID)+' '+str(v.Solider_Name)+' '+str(v.HP)+' '+str(v.Position.x)+' '+str(v.Position.y)+','
            state[number]+=';'
            state[number] += '#'
            #state[number]=state[number].encode('utf-8')
        w=turn*10+winner
        states=str(w)+';'
        states += state[0] + state[1]  # 由于信息双方透明 故发送同一个状态即可
        states=states.encode('utf-8')
    #    print('hhhhhhhhhhhhhhhhhhhhh')
     #   print(states)
      #  print(len(states))
        return states

    def send_state(self,turn,status,building,unit,winner=3):  #给外部调用的接口 只要把当前的status传入即可将status发送给C++选手端
        #回合没有结束 没有winner时 不输入该参数或者输入3
        #将state0和state1处理成byte形式
        player_0=1
        player_1=1
        state =self.change_to_byte(turn,status,building,unit,winner)
        self.sock[0].setblocking(1)
        self.sock[1].setblocking(1)
        #发送start 告诉选手端接下来的要发送命令 防治出现通信问题
        try:
            self.sock[0].send(b'start')
        except ConnectionResetError:
            player_0=0
        try:
            self.sock[1].send(b'start')
        except ConnectionResetError:
            player_1=0

        l=str(len(state))
        lene=len(l)
        for i in range(9-lene):
            l+='#'
        l=l.encode('utf-8')
        try:
            self.sock[0].send(l)
        except ConnectionResetError:
            player_0=0
        try:
            self.sock[1].send(l)
        except ConnectionResetError:
            player_1=0
        try:
            self.sock[0].send(state)
        except ConnectionResetError:
            player_0=0
        try:
            self.sock[1].send(state)
        except ConnectionResetError:
            player_1=0
        #将数据长度以byte的形式
        self.sock[0].setblocking(0)
        self.sock[0].settimeout(0.01)
        self.sock[1].setblocking(0)
        self.sock[1].settimeout(0.01)
        return player_0,player_1  # 返回两位玩家的连接状态 决定游戏是否继续进行

    def recv_command(self):
        def listing_command(sock,command,player,flag): #嵌套定义的一个函数 是子线程中分别接受两个玩家发送过来命令的子线程调用的函数,与闭包无关！！
            while flag[0]:  #flag[0]是用来记数的一个死循环 在0.2s后跳出
                try:
                    data=sock.recv(5)   #非阻塞模式
                    data=data.decode('utf-8')
                    print(data)
                    if data=='start':   #接受一个start标记 防止数据混乱
                        print('start!')
                        break
                except socket.timeout:
                    pass
                except ConnectionResetError:
                    player[0]=0
            if flag[0]==True:
                _len=sock.recv(10)
                _len=_len.decode('utf-8')
                _len=_len.split('#')
                _len=_len[0]
                _len=int(_len)
                try:
                    data=sock.recv(_len) #size
                    data=data.decode('utf-8')
                    data=data.split(',')  #将commandid和unitid分离
                    command.append(data)
                except ConnectionResetError:
                    player[0]=0
            '''while flag[0]:  #以上部分应该在正常情况下接受完 这里不应该能够接受东西 如果选手端出错发送了过多信息 在这里进行清空
                try:
                    data=sock.recv(1024)
                except socket.timeout:
                    pass'''
        #嵌套定义的函数结束

        command=[[],[]]
        flag=[True]
        player_0=[1]
        player_1=[1]
        th0=threading.Thread(target=listing_command,args=(self.sock[0],command[0],player_0,flag))
        th1=threading.Thread(target=listing_command,args=(self.sock[1],command[1],player_1,flag))
        th0.start()
        th1.start()
        time.sleep(0.2) #主线程等待0.2s
        flag[0]=False   #将控制循环的flag改为false 子线程中全部跳出循环 子线程结束
        th0.join()
        th1.join()
        player_1=player_1[0]
        player_0=player_0[0]
       # print('time end！！！！！！！！！！！！！！！！！！')
       # print(command)
        try:
            command[0]=command[0][0]
        except IndexError:
            command[0]=[]
        try:
            command[1]=command[1][0]
        except IndexError:
            command[1]=[]
        l0=len(command[0])
        max0=51  #最大命令条数+1
    #    print('here')
     #   print(command[0])
        if l0!=0 and command[0][0] == Command.UpdateAge.value:    #如果发送了升级命令 那么之后允许的其他命令数目-1
            max0=max0-1
        if l0>max0: #超过允许的最大长度时 截断
            l0=max0
        for i in range(1,l0):
            v=command[0][i].split(' ')
            if v[0]!=str(Command.Construct.value):
       #         print(v[0])
                command[0][i]={'commandid':int(v[0]),'unitid':int(v[1])}
            else:
                command[0][i]={'commandid':int(v[0]),'unitid':int(v[1]),'buildp':Position(int(v[2]),int(v[3])),'soliderp':Position(int(v[4]),int(v[5]))}
        command[0]=command[0][0:l0]
        l1=len(command[1])
        max1=51  #最大命令条数+1
        if l1!=0 and command[1][0] == Command.UpdateAge.value:
            max1=max1-1
        if l1>max1:
            l1=max1
        for i in range(1,l1):
            v=command[1][i].split(' ')
            v=command[1][i].split(' ')
            if v[0]!=str(Command.Construct.value):
       #         print(v[0])
                command[1][i]={'commandid':int(v[0]),'unitid':int(v[1])}
            else:
                command[1][i]={'commandid':int(v[0]),'unitid':int(v[1]),'buildp':Position(int(v[2]),int(v[3])),'soliderp':Position(int(v[4]),int(v[5]))}
        command[1]=command[1][0:l1]
        return command,player_0,player_1 #conmmand是返回给服务器的命令集合
        # command[0]为0的命令 command[1]为1的命令
        # command[0][0]为0是否建造的命令 command[0][i] (i>=1) 为一个个字典 command[0][i]['commmandid']为储存的命令编号
        #  command[0][i]['unitid']为执行该命令的id  command['x'] command['y'] 为执行该命令的地点
        #player_0和player_1返回了玩家1,2的连接状态 用以决定是否继续进行游戏

#测试部分
print('memememememme')
map0=[]
for i in range(0,_mapsize):
    map0.append([])
    for j in range(0,_mapsize):
        map0[i].append(0)
#print(len(map0))
mainserver=MainServer('127.0.0.1',9999)
mainserver.start_connection(map0)
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
    for j in range(2):
        UUnit[i].append(unit.Solider(unit.SoliderName.PACKET.value,100,unit.Position(6,6),i,j))
        Building[i]['produce'].append(unit.Building(unit.BuildingType.Hawkin,unit.Position(7,7),i,j+10,0,unit.Age.NETWORK.value))
        Building[i]['defence'].append(unit.Building(unit.BuildingType.Hawkin,unit.Position(7,7),i,j+20,0,unit.Age.NETWORK.value))
        Building[i]['resource'].append(unit.Building(unit.BuildingType.Hawkin,unit.Position(7,7),i,j+30,0,unit.Age.NETWORK.value))
cccc=1
Continue_Game=True
while Continue_Game:
    print('*************',cccc,'*****************')
    player_0,player_1=mainserver.send_state(cccc,status,Building,UUnit)
    if player_0==0 and player_1==1:
        print('########################player_1 win!###########################')
        Continue_Game=False
    if player_1==0 and player_0==1:
        print('###########################player_0 win!##########################')
        Continue_Game=False
    if player_0==0 and player_1==0:
        print('#####################################draw!########################')
        Continue_Game=False

    command_pl = mainserver.recv_command()
    command=command_pl[0]
    player_0=command_pl[1]
    player_1=command_pl[2]
    if player_0==0 and player_1==1:
        print('########################player_1 win!###########################')
        Continue_Game=False
    if player_1==0 and player_1==1:
        print('###########################player_0 win!##########################')
        Continue_Game=False
    if player_0==0 and player_1==0:
        print('#####################################draw!########################')
        Continue_Game=False


    print(command)
    print('player1',len(command[1]))
    for v in command[0]:
        print(v)
    cccc+=1
    print('player2',len(command[1]))
    for v in command[1]:
        print(v)

