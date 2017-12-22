#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from unit import *


class GameMain:
    _map_size = 200
    _map = []
    for i in range(_map_size):
        _map.append([0 for j in range(_map_size)])
    turn_num = 0
    winner = 2
    total_id = 0

    units = [{} for _ in range(2)]

    main_base = [None] * 2

    buildings = [{
        'produce': [],
        'defence': [],
        'resource': []
    } for _ in range(2)]

    status = [{
        'money': 10000,
        'tech': 3,
        'building': 0,
    } for _ in range(2)]

    # 通信模块将收到的指令写入，各阶段函数从中读取指令，指令格式同api_player.h
    raw_instruments = [{
        'construct': [],  # (BuildingType,(BuildingPos.x,BuildingPos.y),(SoldierPos.x,SoldierPos.y))
        'maintain': [],  # id
        'upgrade': [],  # id
        'sell': [],  # id
        'update_age': False,
    } for _ in range(2)]

    # 各阶段函数处理过raw_instruments后将有效的指令写入，最后将其中的指令写入回放文件
    instruments = [{
        'attack': [],
        'move': [],
        'construct': [],
        'maintain': [],
        'upgrade': [],
        'sell': [],
        'update_age': [],
        'resource': False
    } for _ in range(2)]

    def init_map_random(self):
        import random
        _map = self._map
        _map_size = self._map_size

        # 生成基地，位置定在0,0和199,199处
        self.main_base[0] = Building(BuildingType.Base, Position(0, 0), 0, self.total_id,
                                     False, 0 ,Position(0, 0))
        self.total_id += 1
        self.main_base[1] = Building(BuildingType.Base, Position(199, 199), 1, self.total_id,
                                     False, 0, Position(199, 199))
        self.total_id += 1
        for i in range(7):
            for j in range(7):
                _map[i][j] = 2
        for i in range(_map_size - 7, _map_size):
            for j in range(_map_size - 7, _map_size):
                _map[i][j] = 2

        # 生成中路
        i = 7
        j = 7
        _map[i][j] = 1
        while True:
            if i < _map_size / 2 - 1 and j < _map_size / 2 - 1:
                if random.randint(0, 1) == 0:
                    i += 1
                else:
                    j += 1
            elif i == _map_size / 2 - 1 and j < _map_size / 2 - 1:
                j += 1
            elif i < _map_size / 2 - 1 and j == _map_size / 2 - 1:
                i += 1
            else:
                break
            _map[i][j] = 1
        for i in range(_map_size):
            for j in range(_map_size):
                if _map[_map_size - i - 1][_map_size - j - 1] == 1:
                    _map[i][j] = 1
        _map[int(_map_size / 2) - 1][int(_map_size / 2)] = 1  # 为了让中路连续，把最中心四格都定成路，可改

        # 生成下路
        n = random.randint(1, 3)  # 随机生成3,5或7条路
        for a in range(n):
            i = 7
            x = 5  # 起点从5,3,1顺序选择
            while _map[i][x] == 1 and x >= 1:
                x -= 2
            if x <= 0:
                break
            j = x
            _map[i][j] = 3  # 用3标志暂定路线，最后处理
            while 1:
                if i + j < 200:  # 上下两部分和不同的道路使用两种不同的概率，使道路相对更分散
                    if i < _map_size - x - 1 and j < _map_size - 8:
                        if random.uniform(0, 1) >= x / 12:
                            i += 1
                            if _map[i][j - 1] != 1 and _map[i][j + 1] != 1 and _map[i + 1][j] != 1:
                                # 检查即将延伸的方向有没有其它路，避免交叉
                                pass
                            else:
                                i -= 1
                                j += 1
                                if _map[i - 1][j] != 1 and _map[i + 1][j] != 1 and _map[i][j + 1] != 1:
                                    pass
                                else:
                                    break
                        else:
                            j += 1
                            if _map[i - 1][j] != 1 and _map[i + 1][j] != 1 and _map[i][j + 1] != 1:
                                pass
                            else:
                                j -= 1
                                i += 1
                                if _map[i][j - 1] != 1 and _map[i][j + 1] != 1 and _map[i + 1][j] != 1:
                                    pass
                                else:
                                    break
                    _map[i][j] = 3
                else:
                    if i < _map_size - x - 1 and j < _map_size - 8:
                        if random.uniform(0, 1) < x / 12:
                            i += 1
                            if _map[i][j - 1] != 1 and _map[i][j + 1] != 1 and _map[i + 1][j] != 1:
                                # 检查即将延伸的方向有没有其它路，避免交叉
                                pass
                            else:
                                i -= 1
                                j += 1
                                if _map[i - 1][j] != 1 and _map[i + 1][j] != 1 and _map[i][j + 1] != 1:
                                    pass
                                else:
                                    break
                        else:
                            j += 1
                            if _map[i - 1][j] != 1 and _map[i + 1][j] != 1 and _map[i][j + 1] != 1:
                                pass
                            else:
                                j -= 1
                                i += 1
                                if _map[i][j - 1] != 1 and _map[i][j + 1] != 1 and _map[i + 1][j] != 1:
                                    pass
                                else:
                                    break
                    elif i == _map_size - x - 1 and j < _map_size - 8:
                        j += 1
                        if _map[i - 1][j + 1] != 1 and _map[i][j + 1] != 1:
                            pass
                        else:
                            break
                    elif i < _map_size - x - 1 and j == _map_size - 8:
                        i += 1
                        if _map[i - 1][j + 1] != 1 and _map[i][j + 1] != 1:
                            pass
                        else:
                            break
                    else:
                        break
                    _map[i][j] = 3
            if j == _map_size - 8 <= i < _map_size - 1:  # 路最后延伸至另一个基地
                for i in range(_map_size):
                    for j in range(_map_size):
                        if _map[i][j] == 3:
                            _map[i][j] = 1
            else:
                for i in range(_map_size):
                    for j in range(_map_size):
                        if _map[i][j] == 3:
                            _map[i][j] = 0

        # 利用中心对称生成上路
        for i in range(_map_size):
            for j in range(_map_size):
                if _map[_map_size - i - 1][_map_size - j - 1] == 1:
                    _map[i][j] = 1

    def init_map_from_bitmap(self, path):
        from PIL import Image

        _map_size = self._map_size
        _map = self._map

        img = Image.open(path)
        size = (_map_size, _map_size)
        img = img.resize(size, Image.ANTIALIAS)  # 放缩大小，直接用一个像素对应地图上的一个点

        # 以下二值化代码来自搜索引擎……包括去噪过程
        img = img.convert("RGBA")
        pixdata = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][0] < 90:
                    pixdata[x, y] = (0, 0, 0, 255)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][1] < 136:
                    pixdata[x, y] = (0, 0, 0, 255)
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][2] > 0:
                    pixdata[x, y] = (255, 255, 255, 255)

        # 将二值化后的图片读入_map
        for i in range(_map_size):
            for j in range(_map_size):
                if pixdata[j, i] == (0, 0, 0, 255):
                    _map[i][j] = 1

        # 个人觉得路应该是比非路少的……所以如果1多就反一下，避免底色比道路颜色深的问题
        n = 0
        for i in range(_map_size):
            for j in range(_map_size):
                if _map[i][j] == 1:
                    n += 1
        if n > _map_size * _map_size / 2:
            for i in range(_map_size):
                for j in range(_map_size):
                    if _map[i][j] == 1:
                        _map[i][j] = 0
                    else:
                        _map[i][j] = 1

        # 判断基地，个人想到的一种非常麻烦的判断方法是判断四个角的7*7，全1或者全0判为基地
        x = _map[0][0]
        flag = 0
        for i in range(7):  # 7*7中是不是全是1或0
            for j in range(7):
                if _map[i][j] == x:
                    pass
                else:
                    flag = 1
                    break
        if flag:
            pass
        else:
            for i in range(8):  # 周围一圈有没有1，即路，有路则为基地
                if _map[i][7] == 1:
                    flag = 1
                    break
            for j in range(7):
                if _map[7][j] == 1:
                    flag = 1
                    break
        if flag:  # 如果判为基地
            for i in range(7):
                for j in range(7):
                    _map[i][j] = 2

        x = _map[_map_size - 1][0]
        flag = 0
        for i in range(_map_size - 7, _map_size):
            for j in range(7):
                if _map[i][j] == x:
                    pass
                else:
                    flag = 1
                    break
        if flag:
            pass
        else:
            for i in range(_map_size - 8, _map_size):
                if _map[i][7]:
                    flag = 1
                    break
            for j in range(7):
                if _map[_map_size - 8][j]:
                    flag = 1
                    break
        if flag:  # 如果判为基地
            for i in range(_map_size - 7, _map_size):
                for j in range(7):
                    _map[i][j] = 2

        x = _map[0][_map_size - 1]
        flag = 0
        for i in range(7):
            for j in range(_map_size - 7, _map_size):
                if _map[i][j] == x:
                    pass
                else:
                    flag = 1
                    break
        if flag:
            pass
        else:
            for i in range(8):
                if _map[i][7]:
                    flag = 1
                    break
            for j in range(_map_size - 7, _map_size):
                if _map[7][j]:
                    flag = 1
                    break
        if flag:  # 如果判为基地
            for i in range(7):
                for j in range(_map_size - 7, _map_size):
                    _map[i][j] = 2

        x = _map[_map_size - 1][_map_size - 1]
        flag = 0
        for i in range(_map_size - 7, _map_size):
            for j in range(_map_size - 7, _map_size):
                if _map[i][j] == x:
                    pass
                else:
                    flag = 1
                    break
        if flag:
            pass
        else:
            for i in range(_map_size - 7, _map_size):
                if _map[i][_map_size - 8]:
                    flag = 1
                    break
            for j in range(_map_size - 7, _map_size):
                if _map[_map_size - 8][j]:
                    flag = 1
                    break
        if flag:  # 如果判为基地
            for i in range(_map_size - 7, _map_size):
                for j in range(_map_size - 7, _map_size):
                    _map[i][j] = 2

    def __init__(self):
        self.init_map_random()

    def judge_winnner(self):
        print("judge，回合：",self.turn_num);
        if self.turn_num == Inf:

            if self.main_base[0].HP > self.main_base[1].HP:
                self.winner = 0
            elif self.main_base[0].HP < self.main_base[1].HP:
                self.winner = 1
            elif self.status[0]['tech'] > self.status[1]['tech']:
                self.winner = 0
            elif self.status[0]['tech'] < self.status[1]['tech']:
                self.winner = 1
            elif len(self.units[0]) > len(self.units[1]):
                self.winner = 0
            elif len(self.units[0]) < len(self.units[1]):
                self.winner = 1
            elif self.status[0]['money'] > self.status[1]['money']:
                self.winner = 0
            elif self.status[0]['money'] < self.status[1]['money']:
                self.winner = 1
            else:
                self.winner = 2
        elif self.main_base[0].HP == 0 and self.main_base[1].HP != 0:
            self.winner = 0
        elif self.main_base[1].HP == 0 and self.main_base[0].HP != 0:
            self.winner = 1
        else:
            self.winner = 2

    def check_legal(self):
        """Remove the repeated instruments, or instruments on the wrong units"""
        from functools import reduce
        for current_flag in range(2):
            for instrument_type, instrument_list in self.raw_instruments[current_flag].items():
                if instrument_type == 'update_age':
                    continue
                # 去重，并保持原来指令次序
                new_instrument_list = instrument_list
                del_repeat = lambda x, y: x if y in x else x + [y]
                reduce(del_repeat, [[], ] + new_instrument_list)

                if instrument_type == 'construct':
                    for instrument in new_instrument_list.copy():
                        building_type = instrument[0]
                        new_construct_pos = Position(*instrument[1])
                        new_produce_pos = Position(*instrument[2])
                        # 判断建造时代是否符合要求
                        if (OriginalBuildingAttribute[BuildingType(building_type)][BuildingAttribute.AGE].value >
                                self.status[current_flag]['tech']):
                            new_instrument_list.remove(instrument)
                            continue
                        # 判断建造位置是否符合要求
                        if (self._map[new_construct_pos.x][new_construct_pos.y] == 1 or
                                    self._map[new_construct_pos.x][new_construct_pos.y] == 2):
                            new_instrument_list.remove(instrument)
                            continue
                        building_range = 2  # 建造范围未定，暂设为2
                        can_build = False
                        for building_list in self.buildings[current_flag].values():
                            for building in building_list:
                                if (abs(building.Position.x - new_construct_pos.x) +
                                        abs(building.Position.x - new_construct_pos.x) <=
                                        building_range):
                                    can_build = True
                                    break
                            if can_build:
                                break
                        if not can_build:
                            new_instrument_list.remove(instrument)
                            continue
                        # 判断生产位置是否符合要求
                        if (OriginalBuildingAttribute[building_type][BuildingAttribute.BUILDING_TYPE] ==
                                UnitType.PRODUCTION_BUILDING):
                            if (abs(new_produce_pos.x - new_construct_pos.x) +
                                    abs(new_produce_pos.y - new_construct_pos.y) >
                                    OriginalBuildingAttribute[building_type][BuildingAttribute.ORIGINAL_RANGE]):
                                new_instrument_list.remove(instrument)
                                continue

                else:
                    # 去除指令对象id越界或不符合要求的情况
                    for instrument in new_instrument_list.copy():
                        if instrument > self.total_id or instrument < 0:
                            new_instrument_list.remove(instrument)
                            continue
                        # 去除指令对象不是building的情况
                        is_building = False
                        for building_list in self.buildings[current_flag].values():
                            for building in building_list:
                                if building.Unit_ID == instrument:
                                    is_building = True
                                    break
                            if is_building:
                                break
                        if not is_building:
                            new_instrument_list.remove(instrument)
                            continue
                            # 资源不足，建筑和时代已经到达最高级的情况已经在操作函数中处理
                            # sell指令去重之后不会出现卖空的情况
                            # 其他未考虑到的情况可以继续进行补充

                self.raw_instruments[current_flag][instrument_type] = new_instrument_list

    def attack_phase(self):
        """Defence towers attack the units and units attack towers"""

        for flag in range(2):
            tech_factor = 0.5 * (self.status[flag]['tech'] + 2)

            for building in self.buildings[flag]['defence']:

                # Bool Attack , 1/2 概率无效，攻击最近单位
                if building.BuildingType == BuildingType.Bool:
                    can_attack = random.randint(0, 1)
                    if not can_attack:
                        continue
                    else:
                        pre_dist = OriginalBuildingAttribute[BuildingType.Bool][BuildingAttribute.ORIGINAL_RANGE] + 1
                        target = None
                        for enemy_id, enemy in self.units[1 - flag].items():
                            now_dist = abs(enemy.Position.x - building.Position.x) \
                                       + abs(enemy.Position.y - building.Position.y)
                            if now_dist < pre_dist and enemy.HP > 0:
                                target = enemy
                                target_id = enemy_id
                                pre_dist = now_dist
                        if target is not None:
                            target.HP = (target.HP - (OriginalBuildingAttribute[BuildingType.Bool]
                                                     [BuildingAttribute.ORIGINAL_ATTACK] * tech_factor))
                            self.instruments[flag]['attack'].append((building.Unit_ID, target_id))

                # Ohm Attack , 同时击中V和C伤害加3倍（即乘4倍），攻击最近单位
                if building.BuildingType == BuildingType.Ohm:
                    building.CD -= 1
                    if building.CD <= 0:
                        building.CD = OriginalBuildingAttribute[BuildingType.Ohm][BuildingAttribute.CD]
                        pre_dist = OriginalBuildingAttribute[BuildingType.Ohm][BuildingAttribute.ORIGINAL_RANGE] + 1
                        target = None
                        for enemy_id, enemy in self.units[1 - flag].items():
                            now_dist = (abs(enemy.Position.x - building.Position.x) +
                                        abs(enemy.Position.y - building.Position.y))
                            if now_dist < pre_dist and enemy.HP > 0:
                                target = enemy
                                target_id = enemy_id
                                pre_dist = now_dist
                        if target is not None:
                            target_x = target.Position.x
                            target_y = target.Position.y
                            hit_v = 0
                            hit_c = 0
                            for enemy_id, enemy in self.units[1 - flag].items():
                                if (abs(enemy.Position.x - target_x) + abs(enemy.Position.y - target_y) <
                                        OriginalBuildingAttribute[BuildingType.Ohm][BuildingAttribute.AOE]):
                                    enemy.HP = (enemy.HP - (OriginalBuildingAttribute[BuildingType.Ohm]
                                                           [BuildingAttribute.ORIGINAL_ATTACK] * tech_factor))
                                    if enemy.Solider_Name == SoliderName.VOLTAGE_SOURCE:
                                        hit_v = 1
                                    if enemy.Solider_Name == SoliderName.CURRENT_SOURCE:
                                        hit_c = 1
                                if hit_v and hit_c:
                                    for enemy_id, enemy in self.units[1 - flag].items():
                                        if (abs(enemy.Position.x - target_x) + abs(enemy.Position.y - target_y)
                                                < OriginalBuildingAttribute[BuildingType.Ohm][BuildingAttribute.AOE]):
                                            enemy.HP = (enemy.HP - 3 * (OriginalBuildingAttribute[BuildingType.Ohm][
                                                                    BuildingAttribute.ORIGINAL_ATTACK] * tech_factor))
                            self.instruments[flag]['attack'].append((building.Unit_ID, target_id))
                # Mole Attack，连续攻击同一个目标每次翻倍
                if building.BuildingType == BuildingType.Mole:
                    pre_dist = OriginalBuildingAttribute[BuildingType.Bool][BuildingAttribute.ORIGINAL_RANGE] + 1
                    target = None
                    find_last = False
                    # 查找上一个攻击目标是否还在攻击范围内
                    for enemy_id, enemy in self.units[1 - flag].items():
                        if (enemy.HP > 0 and enemy_id == building.last_target_id and
                                        abs(enemy.Position.x - building.Position.x) +
                                        abs(enemy.Position.y - building.Position.y) < pre_dist):
                            target = enemy
                            building.mult_factor *= 2
                            find_last = True
                            break
                    if not find_last:
                        building.mult_factor = 1
                        for enemy_id, enemy in self.units[1 - flag].items():
                            now_dist = abs(enemy.Position.x - building.Position.x) \
                                       + abs(enemy.Position.y - building.Position.y)
                            if now_dist < pre_dist and enemy.HP > 0:
                                target = enemy
                                target_id = enemy_id
                                pre_dist = now_dist
                    if target is not None:
                        building.last_target_id = target_id
                        target.HP = (target.HP - (OriginalBuildingAttribute[BuildingType.Mole][
                                        BuildingAttribute.ORIGINAL_ATTACK] * tech_factor * building.mult_factor))
                        self.instruments[flag]['attack'].append((building.Unit_ID, target_id))

                # Monte_Carlo Attack,0-2之间随机数
                if building.BuildingType == BuildingType.Monte_Carlo:
                    building.CD -= 1
                    if building.CD <= 0:
                        building.CD = OriginalBuildingAttribute[BuildingType.Monte_Carlo][BuildingAttribute.CD]
                        pre_dist = OriginalBuildingAttribute[BuildingType.Monte_Carlo][
                                       BuildingAttribute.ORIGINAL_RANGE] + 1
                        target = None
                        for enemy_id, enemy in self.units[1 - flag].items():
                            now_dist = abs(enemy.Position.x - building.Position.x) \
                                       + abs(enemy.Position.y - building.Position.y)
                            if now_dist < pre_dist and enemy.HP> 0:
                                target = enemy
                                target_id = enemy_id
                                pre_dist = now_dist
                        if target is not None:
                            rand_factor = random.uniform(0, 2)
                            target.HP = (target.HP - (OriginalBuildingAttribute[BuildingType.Bool]
                                                     [BuildingAttribute.ORIGINAL_ATTACK] * tech_factor * rand_factor))
                            self.instruments[flag]['attack'].append((building.Unit_ID, target_id))

                # Larry_Roberts Attack,优先数据包且对其伤害乘3
                if building.BuildingType == BuildingType.Larry_Roberts:
                    pre_dist = OriginalBuildingAttribute[BuildingType.Larry_Roberts][BuildingAttribute.ORIGINAL_RANGE] \
                               + 1
                    target = None
                    hit_packet = False
                    for enemy_id, enemy in self.units[1 - flag].items():
                        now_dist = abs(enemy.Position.x - building.Position.x) \
                                   + abs(enemy.Position.y - building.Position.y)
                        if now_dist < pre_dist and enemy.HP > 0:
                            if (not hit_packet) or enemy.Solider_Name == SoliderName.PACKET:
                                target = enemy
                                target_id = enemy_id
                                pre_dist = now_dist
                                if enemy.Solider_Name == SoliderName.PACKET:
                                    hit_packet = True
                    if target is not None:
                        target_x = target.Position.x
                        target_y = target.Position.y
                        for enemy_id, enemy in self.units[1 - flag].items():
                            if (abs(enemy.Position.x - target_x) + abs(enemy.Position.y - target_y) <
                                    OriginalBuildingAttribute[BuildingType.Larry_Roberts][BuildingAttribute.AOE]):
                                if enemy.Solider_Name == SoliderName.PACKET:
                                    mult_factor = 3
                                else:
                                    mult_factor = 1
                                enemy.HP = (enemy.HP - (OriginalBuildingAttribute[BuildingType.Larry_Roberts]
                                                       [BuildingAttribute.ORIGINAL_ATTACK] * tech_factor * mult_factor))
                        self.instruments[flag]['attack'].append((building.Unit_ID, target_id))

                # Robert_Kahn Attack,最大生命值10% * tech_factor
                if building.BuildingType == BuildingType.Robert_Kahn:
                    pre_dist = OriginalBuildingAttribute[BuildingType.Robert_Kahn][BuildingAttribute.ORIGINAL_RANGE] + 1
                    target = None
                    for enemy_id, enemy in self.units[1 - flag].items():
                        now_dist = abs(enemy.Position.x - building.Position.x) \
                                   + abs(enemy.Position.y - building.Position.y)
                        if now_dist < pre_dist and enemy.HP > 0:
                            target = enemy
                            target_id = enemy_id
                            pre_dist = now_dist
                    if target is not None:
                        persent = 0.1 * tech_factor
                        target.HP = (target.HP - OriginalSoliderAttribute[target.SoliderName][
                            SoliderAttr.SOLIDER_ORIGINAL_HP] * persent)
                        self.instruments[flag]['attack'].append((building.Unit_ID, target_id))

                # Hawkin Attack,秒杀一格
                if building.BuildingType == BuildingType.Hawkin:
                    building.CD -= 1
                    if building.CD <= 0:
                        building.CD = OriginalBuildingAttribute[BuildingType.Hawkin][BuildingAttribute.CD]
                        pre_dist = OriginalBuildingAttribute[BuildingType.Hawkin][BuildingAttribute.ORIGINAL_RANGE] + 1
                        target = None
                        for enemy_id, enemy in self.units[1 - flag].items():
                            now_dist = abs(enemy.Position.x - building.Position.x) \
                                       + abs(enemy.Position.y - building.Position.y)
                            if now_dist < pre_dist and enemy.HP > 0:
                                target = enemy
                                target_id = enemy_id
                                pre_dist = now_dist
                        if target is not None:
                            target_x = target.Position.x
                            target_y = target.Position.y
                            for enemy_id, enemy in self.units[1 - flag].items():
                                if (abs(enemy.Position.x - target_x) + abs(enemy.Position.y - target_y) <
                                        OriginalBuildingAttribute[BuildingType.Hawkin][BuildingAttribute.AOE]):
                                    enemy.HP = -1
                            self.instruments[flag]['attack'].append((building.Unit_ID, target_id))

            # 兵种对建筑的攻击
            for unit_id, unit in self.units[flag].items():
                action_mode = OriginalSoliderAttribute[unit.Solider_Name][SoliderAttr.ACTION_MODE]
                pre_dist = OriginalSoliderAttribute[unit.Solider_Name][SoliderAttr.ATTACK_RANGE] + 1

                # 推塔式与抗线式兵种的攻击
                if action_mode == ActionMode.BUILDING_ATTACK or action_mode == ActionMode.MOVING_ATTACK:
                    target = None
                    for building_list in self.buildings[1 - flag].values():
                        for enemy_building in building_list:
                            now_dist = (abs(enemy_building.Position.x - unit.Position.x) +
                                        abs(enemy_building.Position.y - unit.Position.y))
                            if now_dist < pre_dist and enemy_building.HP > 0:
                                target = enemy_building
                                pre_dist = now_dist
                    if target is None:
                        # 如果没有找到范围内的建筑，就查找基地是否在其范围内
                        # 假设flag = 0 基地在(0,0)，flag = 1 基地在(199,199)
                        if not flag:
                            now_dist_x = 0 if unit.Position.x >= 193 else 193 - unit.Position.x
                            now_dist_y = 0 if unit.Position.y >= 193 else 193 - unit.Position.y
                        else:
                            now_dist_x = 0 if unit.Position.x <= 6 else unit.Position.x - 6
                            now_dist_y = 0 if unit.Position.y <= 6 else unit.Position.x - 6
                        now_dist = now_dist_x + now_dist_y
                        if now_dist < pre_dist and self.main_base[1 - flag].HP > 0:
                            pass
                            # target = self.main_base[1 - flag]
                    if target is not None:
                        target.HP = (target.HP - OriginalSoliderAttribute[unit.Solider_Name][
                                          SoliderAttr.SOLIDER_ORIGINAL_ATTACK] * tech_factor)
                        self.instruments[flag]['attack'].append((unit_id, target.Unit_ID))

                # 冲锋式兵种的攻击
                else:
                    if flag:
                        now_dist_x = 0 if unit.Position.x >= 193 else 193 - unit.Position.x
                        now_dist_y = 0 if unit.Position.y >= 193 else 193 - unit.Position.x
                    else:
                        now_dist_x = 0 if unit.Position.x <= 6 else unit.Position.x - 6
                        now_dist_y = 0 if unit.Position.y <= 6 else unit.Position.x - 6
                    now_dist = now_dist_x + now_dist_y
                    if now_dist < pre_dist and self.main_base[1 - flag].HP > 0:
                        self.main_base[1 - flag].HP -= (OriginalSoliderAttribute[unit.SoliderName][
                                                            SoliderAttr.SOLIDER_ORIGINAL_ATTACK] * tech_factor)
                        unit.HP = -1
                        self.instruments[flag]['attack'].append((unit_id, self.main_base[1 - flag].Unit_ID))

    def clean_up_phase(self):
        """Remove the destroyed units and towers"""
        for flag in range(2):
            for unit_id in list(self.units[flag].keys()):
                if self.units[flag][unit_id].HP <= 0:
                    self.units[flag].pop(unit_id)
            for building in self.buildings[flag]['produce']:
                if building.HP <= 0:
                    self.buildings[flag]['produce'].remove(building)
            for building in self.buildings[flag]['defence']:
                if building.HP <= 0:
                    self.buildings[flag]['defence'].remove(building)
            for building in self.buildings[flag]['resource']:
                if building.HP <= 0:
                    self.buildings[flag]['resource'].remove(building)

    def move_phase(self):
        """Move the units according to their behaviour mode"""
        _map = self._map
        for current_flag in range(2):
            # Assume player 0's base is at(0,0) temporarily, which can be changed.
            direction = 1 if current_flag == 0 else -1

            for unit_id, unit in self.units[current_flag].items():
                # Building Musk's skill : AI cannot move in its shot range.
                if unit.Solider_Name == SoliderName.TURNING_MACHINE or unit.Solider_Name == SoliderName.ULTRON:
                    can_move = True
                    for enemy_building in self.buildings[1 - current_flag]['defence']:
                        if (enemy_building.BuildingType == BuildingType.Musk and
                            abs(enemy_building.Position.x - unit.Position.x) +
                            abs(enemy_building.Position.y - unit.Position.y) <=
                                    OriginalBuildingAttribute[enemy_building.BuildingType][
                                        BuildingAttribute.ORIGINAL_RANGE]):
                            can_move = False
                            break
                    if not can_move:
                        continue

                if (OriginalSoliderAttribute[unit.Solider_Name][SoliderAttr.ACTION_MODE] ==
                        ActionMode.BUILDING_ATTACK):
                    for i in range(OriginalSoliderAttribute[unit.Solider_Name][SoliderAttr.SPEED]):
                        # When solider is moving, if there are buildings in solider's shot range,
                        # stop to attack the building, else continue moving.
                        can_move = True
                        for building_type, building_array in self.buildings[1 - current_flag].items():
                            for enemy_building in building_array:
                                if (abs(enemy_building.Position.x - unit.Position.x) +
                                        abs(enemy_building.Position.y - unit.Position.y) <=
                                        OriginalSoliderAttribute[unit.Solider_Name][SoliderAttr.ATTACK_RANGE]):
                                    can_move = False
                                    break
                            if not can_move:
                                break

                        if can_move:
                            if _map[unit.Position.x + direction][unit.Position.y] == 1:
                                # position need to be changed.
                                unit.Position = Position(unit.Position.x + direction, unit.Position.y)
                            elif _map[unit.Position.x][unit.Position.y + direction] == 1:
                                unit.Position = Position(unit.Position.x, unit.Position.y + direction)
                        else:
                            break
                    self.instruments[current_flag]['move'].append(
                        (unit_id, unit.Position))

                else:
                    for i in range(OriginalSoliderAttribute[unit.Solider_Name][SoliderAttr.SPEED]):
                        if _map[unit.Position.x + direction][unit.Position.y] == 1:
                            unit.Position = Position(unit.Position.x + direction, unit.Position.y)
                        elif _map[unit.Position.x][unit.Position.y + direction] == 1:
                            unit.Position = Position(unit.Position.x, unit.Position.y + direction)
                    self.instruments[current_flag]['move'].append(
                        (unit_id, unit.Position))

    def building_phase(self):
        """Deal with the instruments about buildings"""

        # Lack the legality judgement temporarily.

        def construct_phase(self):

            total_id = self.total_id
            for current_flag in range(2):
                age_increase_factor = 0.5 * (self.status[current_flag]['tech'] + 2)
                for construct_instrument in self.raw_instruments[current_flag]['construct']:
                    building_name = construct_instrument[0]
                    building_pos = Position(*construct_instrument[1])
                    money_cost = (
                        OriginalBuildingAttribute[construct_instrument[0]][BuildingAttribute.ORIGINAL_RESOURCE] *
                        age_increase_factor)
                    building_point_cost = (
                        OriginalBuildingAttribute[construct_instrument[0]][BuildingAttribute.ORIGINAL_BUILDING_POINT] *
                        age_increase_factor)
                    if building_name < 9 and building_name >0:
                        produce_pos = Position(*construct_instrument[2])

                    # Ignore the instruments that spend too much.
                    if (self.status[current_flag]['money'] < money_cost and
                                self.status[current_flag]['building'] < building_point_cost):
                        continue

                    if (OriginalBuildingAttribute[construct_instrument[0]][BuildingAttribute.BUILDING_TYPE] ==
                            UnitType.PRODUCTION_BUILDING):
                        self.buildings[current_flag]['produce'].append(
                            Building(building_name, building_pos, current_flag, total_id, False,
                                     self.status[current_flag]['tech'],produce_pos)
                            )
                    elif (OriginalBuildingAttribute[construct_instrument[0]][BuildingAttribute.BUILDING_TYPE] ==

                            UnitType.DEFENSIVE_BUILDING):
                        self.buildings[current_flag]['defence'].append(

                            Building(building_name, building_pos, current_flag, total_id, False,
                                     self.status[current_flag]['tech'], produce_pos)
                            )
                    else:
                        self.buildings[current_flag]['resource'].append(
                            Building(building_name, building_pos, current_flag, total_id, False,
                                     self.status[current_flag]['tech'], produce_pos)
                            )

                    total_id += 1
                    self.status[current_flag]['money'] -= money_cost
                    self.status[current_flag]['building'] -= building_point_cost
                    self.instruments[current_flag]['construct'].append(construct_instrument)
        construct_phase(self)

        def maintain_phase(self):
            for current_flag in range(2):
                for building_type, building_array in self.buildings[current_flag].items():
                    for building in building_array:
                        # Change the status if The building is maintaining.
                        for maintain_instrument in self.raw_instruments[current_flag]['maintain']:
                            if building.Unit_ID == maintain_instrument:
                                # Change the status of the true building, not its copy.
                                max_HP = (
                                OriginalBuildingAttribute[building.BuildingType][BuildingAttribute.ORIGINAL_HP] *
                                0.5 * (building.level + 2))
                                lost_percent = (max_HP - building.HP) / max_HP  # The ratio of lost HP to max HP.
                                construct_money = (
                                    OriginalBuildingAttribute[building.BuildingType][
                                        BuildingAttribute.ORIGINAL_RESOURCE] *
                                    0.5 * (building.level + 2))
                                if (self.status[current_flag]['money'] > lost_percent * construct_money):
                                    building.HP = max_HP
                                    self.status[current_flag]['money'] -= lost_percent * construct_money
                                    self.instruments[current_flag]['maintain'].append(building.Unit_ID)
                                break

        maintain_phase(self)

        def upgrade_phase(self):
            for current_flag in range(2):
                for building_type, building_array in self.buildings[current_flag].items():
                    for building in building_array:
                        for upgrade_instrument in self.raw_instruments[current_flag]['upgrade']:
                            if building.Unit_ID == upgrade_instrument:
                                #building_index = building_array.index(element)
                                max_HP = (
                                    OriginalBuildingAttribute[building.BuildingType][BuildingAttribute.ORIGINAL_HP] *
                                    0.5 * (building.level + 2))
                                lost_percent = (max_HP - building.HP) / max_HP  # The ratio of lost HP to max HP.
                                construct_money = (OriginalBuildingAttribute[building.BuildingType][
                                                       BuildingAttribute.ORIGINAL_RESOURCE] *
                                                   0.5 * (building.level + 2))
                                # The difference of construct money and max HP between old and upgraded towers.
                                upgrade_diff_money = OriginalBuildingAttribute[building.BuildingType][
                                                         BuildingAttribute.ORIGINAL_RESOURCE] * 0.5
                                upgrade_diff_max_HP = OriginalBuildingAttribute[building.BuildingType][
                                                          BuildingAttribute.ORIGINAL_HP] * 0.5

                                if (self.status[current_flag]['money'] > lost_percent * construct_money + upgrade_diff_money
                                    and self.status[current_flag]['tech'] >=
                                            building.level + 1):
                                    building.level += 1
                                    building.HP = max_HP + upgrade_diff_max_HP
                                    self.status[current_flag]['money'] -= upgrade_diff_money + lost_percent * construct_money
                                    self.instruments[current_flag]['upgrade'].append(upgrade_instrument)
                                break
        upgrade_phase(self)

        def sell_phase(self):
            # age_increase_factor = 0.5 * (self.status[current_flag]['tech'] + 2)
            for current_flag in range(2):
                for sell_instrument in self.raw_instruments[current_flag]['sell']:
                    have_found = False  # Signal if the building to be sold has been found.
                    for building_type, building_array in self.buildings[current_flag].items():
                        for building in building_array:
                            if building.Unit_ID == sell_instrument:
                                max_HP = (
                                    OriginalBuildingAttribute[building.BuildingType][BuildingAttribute.ORIGINAL_HP] *
                                    0.5 * (building.level + 2))
                                return_percent = 0.5 if building.HP < 0.5 * max_HP else 1 - building.HP / max_HP
                                construct_money = (OriginalBuildingAttribute[building.BuildingType][
                                                       BuildingAttribute.ORIGINAL_RESOURCE] *
                                                   0.5 * (building.level + 2))

                                self.status[current_flag]['money'] += return_percent * construct_money
                                self.buildings[current_flag][building_type].remove(building)
                                have_found = True
                                break
                        if have_found:
                            break
                    self.instruments[current_flag]['sell'].append(sell_instrument)
        sell_phase(self)

    def produce_phase(self):
        """Unit production by producing building"""
        for current_flag in range(2):
            age_increase_factor = 0.5 * (self.status[current_flag]['tech'] + 2)
            for building in self.buildings[current_flag]['produce']:
                if building.CD_left == 0:
                    solider_name = OriginalBuildingAttribute[building.BuildingType][BuildingAttribute.TRAGET]
                    solider_hp = OriginalSoliderAttribute[solider_name][SoliderAttr.SOLIDER_ORIGINAL_HP]
                    solider_pos = building.ProducePos
                    solider_flag = current_flag
                    solider_id = self.total_id
                    cd = OriginalBuildingAttribute[building.BuildingType][BuildingAttribute.CD]
                    self.units[current_flag][solider_id]=\
                        Solider(solider_name, solider_hp, solider_pos, solider_flag, solider_id)
                    building.CD_left = cd  # 重置CD
                    self.total_id += 1
                else:
                    building.CD_left = building.CD_left - 1

    def update_age_phase(self):
        """Deal with the update_age instruments"""
        basic_consumption = 0  # 基础升级科技消耗，未定
        increased_consumption = 0  # 科技每升一级，下次升级科技资源消耗增量
        for flag in range(2):
            if self.raw_instruments[flag]['update_age']:
                consumption = basic_consumption + increased_consumption * self.status[flag]['tech']
                if self.status[flag]['money'] > consumption and self.status[flag]['tech'] < Age.AI.value:
                    self.status[flag]['money'] -= consumption
                    self.status[flag]['tech'] += 1
                    self.instruments[flag]['update_age'].append(True)
                else:
                    self.instruments[flag]['update_age'].append(False)

    def resource_phase(self):
        """Produce new resource and refresh building force"""
        for flag in range(2):
            basic_resource = OriginalBuildingAttribute[BuildingType.Programmer][BuildingAttribute.ORIGINAL_ATTACK]
            resource = (basic_resource * 0.5 * (self.status[flag]['tech'] + 2)) * len(self.buildings[flag]['resource'])
            self.status[flag]['money'] += resource
            self.status[flag]['building'] = self.status[flag]['tech'] * 60 + 100
            self.instruments[flag]['resource'] = True

    def debug_print(self):
        """debug时输出信息"""
        line = "回合:" + str(self.turn_num) + '\n'
        with open("debug.txt", "a", encoding="utf8") as out:
            out.write(line)

        with open("debug.txt", "a", encoding="utf8") as out:
            out.write("输出主基地血量\n")
        for flag in range(2):
            line = "flag:" + str(flag) + " HP:" + str(self.main_base[flag].HP) + '\n'
            with open("debug.txt", "a") as out:
                out.write(line)
        # print('输出status中的信息')
        # for flag in range(2):
        #     print('flag:',flag)
        #     for sta_type, sta_of_type in self.status[flag].items():
        #         print(sta_type, ':', sta_of_type)
        # print('输出raw_ins中的信息')
        # for flag in range(2):
        #     print('flag:', flag)
        #     for ins_type, ins_of_type in self.raw_instruments[flag].items():
        #         print(ins_type, end=':')
        #         if type(ins_of_type) != bool:
        #             for ins in ins_of_type:
        #                 print(ins, end=' ')
        #             print()
        #         else:
        #             print(ins_of_type)
        # print('输出ins中的信息')
        # for flag in range(2):
        #     print('flag:', flag)
        #     for ins_type, ins_of_type in self.instruments[flag].items():
        #         print(ins_type, end=':')
        #         if type(ins_of_type) != bool:
        #             for ins in ins_of_type:
        #                 print(ins, end=' ')
        #             print()
        #         else:
        #             print(ins_of_type)
        with open("debug.txt", "a", encoding="utf8") as out:
            out.write('输出building中的信息\n')
        for flag in range(2):
            line = 'flag:' + str(flag) + '\n'
            with open("debug.txt", "a") as out:
                out.write(line)
            for building_type,buildings_of_type in self.buildings[flag].items():
                for building in buildings_of_type:
                    line = "ID:" + str(building.Unit_ID) + " Type:" + str(int(building.BuildingType)) \
                          + " Position:" + str(building.Position.x) + ' ' + str(building.Position.y) \
                          + " HP:" + str(building.HP) + '\n'
                    with open("debug.txt", "a") as out:
                        out.write(line)

        with open("debug.txt", "a", encoding="utf8") as out:
            out.write('输出unit中的信息\n')
        for flag in range(2):
            line = 'flag:' + str(flag) + '\n'
            with open("debug.txt", "a") as out:
               out.write(line)
            tech_factor = 0.5 * (self.status[flag]['tech'] + 2)
            for unit_id, unit in self.units[flag].items():
                line = "ID:" + str(unit_id) + " Type:" + str(int(unit.Solider_Name)) \
                      + " Position:" + str(unit.Position.x) + ' ' + str(unit.Position.y) \
                      + " Attack" + str(OriginalSoliderAttribute[unit.Solider_Name][
                                SoliderAttr.SOLIDER_ORIGINAL_ATTACK] * tech_factor) + '\n'
                with open("debug.txt", "a") as out:
                    out.write(line)
    def next_tick(self):
        """回合演算与指令合法性判断"""
        self.turn_num += 1
        self.attack_phase()
        self.clean_up_phase()
        self.move_phase()
        # self.check_legal()
        self.building_phase()
        self.produce_phase()
        self.update_age_phase()
        self.resource_phase()
        # self.update_id()
        self.judge_winnner()

        self.debug_print()

def main():
    game = GameMain()
    game.next_tick()


if __name__ == "__main__":
    main()
