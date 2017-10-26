from gamemain import GameMain
import json
import unit
import time
import os
import sys

from unit import BuildingType,Building,Solider,Age,SoliderName

#以下为两个将building，solider转化为字典函数，便于写入文件（在通信未完成之前）
def building2dict(std):
	return {	"flag":std.Flag,	"type":str(std.BuildingType),
				"HP":std.HP,	"Maintain":std.Is_Maintain,
			 "Pos":std.Position,	"id":std.Unit_ID }

def unit2dict(std):
	return {	"flag":std.Flag,	"type":str(std.Solider_Name),	"HP":std.HP,
			 "Pos":std.Position	}


def BuildingType2Str(std):
	return str(std)
def SoliderName2Str(std):
	return str(std)
############################################################################


filename = "teamstyle19" + time.strftime("%m%d%H%M%S") + ".txt" #将来改成rpy
if (len(sys.argv)>1):
    filename = sys.argv[1]

read_file = open("test.txt",'r')
game = GameMain()
print('start')
file = []


while( game.winner == 3 ):
	#由于未写通信模块，故每回合指令手动输入


	#将指令写入txt文件中，逐行读取
	raw_instrument = json.load(read_file.readline())
	game.raw_instruments = raw_instrument

	#由于通信模块未写，直接将每回合信息写入文件，方便之后调试
	file.append( json.dumps({'turn': game.turn_num }) )
	file.append( json.dumps(game.buildings,default=building2dict ) )
	file.append( json.dumps(game.units, default=unit2dict) )
	file.append( json.dumps(game.status) )
	file.append( json.dumps(game.instruments,default=BuildingType2Str) )

	print("server turns:", game.turn_num)
	game.next_tick()


f = open( filename, 'w' )
for b in file:
	f.write(b)
f.write( game.winner )
f.close()