#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import os
import sys

from gamemain import GameMain
import unit
from unit import BuildingType, Building, Solider, Age, SoliderName


# 以下为两个将building，solider转化为字典函数，便于写入文件（在通信未完成之前）
def building2dict(std):
    return {"flag": std.Flag, "type": str(std.BuildingType),
            "HP": std.HP, "Maintain": std.Is_Maintain,
            "Pos": std.Position, "id": std.Unit_ID}


def unit2dict(std):
    return {"flag": std.Flag, "type": str(std.Solider_Name), "HP": std.HP,
            "Pos": std.Position}


def BuildingType2Str(std):
    return str(std)


def SoliderName2Str(std):
    return str(std)


############################################################################

filename = "ts19" + time.strftime("%m%d%H%M%S") + ".txt"  # 将来改成rpy
if len(sys.argv) > 1:
    filename = sys.argv[1]

read_file = open("test.txt", 'r')
game = GameMain()
game.map_save()
with open('turn_save.txt','w') as f:
    pass    #清空文件
print('start')
file = []
print_count = 0

f = open("debug.txt", 'w')
f.close()
while game.winner == 2:
    # 由于未写通信模块，故每回合指令写入txt中，随后自动逐行读取

    line = read_file.readline()
    if line:
        game.raw_instruments = json.loads(line)
    else:
        game.raw_instruments = [{
        'construct': [],  # (BuildingType,(BuildingPos.x,BuildingPos.y),(SoldierPos.x,SoldierPos.y))
        'maintain': [],  # id
        'upgrade': [],  # id
        'sell': [],  # id
        'update_age': False,
        } for _ in range(2)]

    # 由于通信模块未写，直接将每回合信息写入文件，方便之后调试
    game.next_tick()


