#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from unit import *


class GameMain:
    _map_size = 200
    _map = [[[0] for i in range(_map_size)] for i in range(_map_size)]
    turn_num = 0
    winner = 3

    units = [{} for i in range(2)]

    main_base = [None] * 2

    buildings = [{
        'produce': [],
        'defence': [],
        'resource': []
    } for i in range(2)]

    status = [{
        'money': 0,
        'tech': 0,
        'building': 0,
    } for i in range(2)]

    # 通信模块将收到的指令写入，各阶段函数从中读取指令，指令格式同api_player.h
    raw_instruments = [{
        'construct': [],  # (BuildingType,(BuildingPos.x,BuildingPos.y),(SoldierPos.x,SoldierPos.y))
        'maintain': [],  # id
        'upgrade': [],  # id
        'sell': [],  # id
        'update_age': False,
    } for i in range(2)]

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
    } for i in range(2)]

    def init_map_random(self):
        import random

        # 生成基地，位置定在0,0和199,199处
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
        while (1):
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
                            if _map[i][j - 1] != 1 and _map[i][j + 1] != 1 and _map[i + 1][
                                j] != 1:  # 检查即将延伸的方向有没有其它路，避免交叉
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
                            if _map[i][j - 1] != 1 and _map[i][j + 1] != 1 and _map[i + 1][
                                j] != 1:  # 检查即将延伸的方向有没有其它路，避免交叉
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
            if _map_size - 8 <= i < _map_size - 1 and j == _map_size - 8:  # 路最后延伸至另一个基地
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

    def init_map_from_bitmap(self):
        from PIL import Image

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
                if (pixdata[j, i] == (0, 0, 0, 255)):
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

    def __init__(self, init_map):
        pass

    def judge_winner(self):
        pass

    def check_legal(self):
        """Remove the repeated instruments, or instruments on the wrong units"""
        pass

    def attack_phase(self):
        """Defence towers attack the units and units attack towers"""
        pass

    def clean_up_phase(self):
        """Remove the destroyed units and towers"""
        pass

    def move_phase(self):
        """Move the units according to their behaviour mode"""
        for current_flag in range(2):
            # Assume player 0's base is at(0,0) temporarily, which can be changed.
            direction = 1 if current_flag == 0 else -1
            can_move = True

            for unit_id, unit in self.units[current_flag].items():
                # Building Musk's skill : AI cannot move in its shot range.
                if unit.Solider_Name == SoliderName.TURNING_MACHINE or SoliderName.ULTRON:
                    for enemy_building in self.buildings[not current_flag]['defence']:
                        if (enemy_building.BuildingType == BuildingType.Musk and
                            abs(enemy_building.Position.x - unit.Position.x) +
                            abs(enemy_building.Position.y - unit.Position.y) <=
                            OriginalBuildingAttribute[enemy_building.BuildingType][BuildingAttribute.ORIGINAL_RANGE]) :
                            can_move = False
                            break
                    if not can_move:
                        continue

                if (OriginalSoliderAttribute[unit.Solider_Name][SoliderAttr.ACTION_MODE] ==
                    ActionMode.BUILDING_ATTACK):
                    for i in range(OriginalSoliderAttribute[unit.Solider_Name][SoliderAttr.SPEED]) :
                        # When solider is moving, if there are buildings in solider's shot range,
                        # stop to attack the building, else continue moving.
                        for building_type, building_array in self.buildings[not current_flag].items():
                            for element in building_array:
                                enemy_building = element[0]
                                if (abs(enemy_building.Position.x - unit.Position.x) +
                                    abs(enemy_building.Position.y - unit.Position.y) <=
                                    OriginalSoliderAttribute[unit.Solider_Name][SoliderAttr.ATTACK_RANGE]) :
                                    can_move = False
                                    break
                            if not can_move:
                                break

                        if can_move:
                            if _map[unit.Position.x + direction][unit.Position.y] == 1:
                                # Position need to be changed.
                                self.units[current_flag][unit_id].Position.x += direction
                            elif _map[unit.Position.x][unit.Position.y + direction] == 1:
                                self.units[current_flag][unit_id].Position.y += direction
                            self.instruments[current_flag]['move'].append((unit_id, self.units[unit_id].Position))
                        else:
                            break

                else:
                    for i in range(OriginalSoliderAttribute[unit.Solider_Name][SoliderAttr.SPEED]) :
                        if _map[unit.Position.x + direction][unit.Position.y] == 1:
                            self.units[current_flag][unit_id].Position.x += direction
                        elif _map[unit.Position.x][unit.Position.y + direction] == 1:
                            self.units[current_flag][unit_id].Position.y += direction
                        self.instruments[current_flag]['move'].append((unit_id, self.units[unit_id].Position))

    def building_phase(self):
        """Deal with the instruments about buildings"""
        pass

        # Lack the legality judgement temporarily.

    def construct_phase(self):
        age_increase_factor = 0.5 * (self.status[current_flag]['tech'] + 2)
        for current_flag in range(2):
            for construct_instrument in self.raw_instruments[current_flag]['construct']:
                building_name = construct_instrument[0]
                building_hp = (OriginalBuildingAttribute[construct_instrument[0]][BuildingAttribute.ORIGINAL_HP] *
                               age_increase_factor)
                building_pos = Position(construct_instrument[1])
                money_cost = (OriginalBuildingAttribute[construct_instrument[0]][BuildingAttribute.ORIGINAL_RESOURCE] *
                              age_increase_factor)
                building_point_cost = (OriginalBuildingAttribute[construct_instrument[0]][BuildingAttribute.ORIGINAL_BUILDING_POINT] *
                                       age_increase_factor)
                produce_pos = Position(construct_instrument[2])

                # Ignore the instruments that spend too much.
                if (self.status[current_flag]['money'] < money_cost and
                    self.status[current_flag]['building'] < building_point_cost) :
                    continue

                if (OriginalBuildingAttribute[construct_instrument[0]][BuildingAttribute.BUILDING_TYPE] ==
                    UnitType.PRODUCTION_BUILDING) :
                    self.buildings[current_flag]['produce'].append((
                        Building(building_name, building_hp, building_pos, current_flag, total_id, False),
                        produce_pos))
                elif (OriginalBuildingAttribute[construct_instrument[0]][BuildingAttribute.BUILDING_TYPE] ==
                      UnitType.DEFENSIVE_BUILDING) :
                    self.buildings[current_flag]['defence'].append((
                        Building(building_name, building_hp, building_pos, current_flag, total_id, False),
                        produce_pos))
                else:
                    self.buildings[current_flag]['resource'].append((
                        Building(building_name, building_hp, building_pos, current_flag, total_id, False),
                        produce_pos))

                total_id += 1
                self.status[current_flag]['money'] -= money_cost
                self.status[current_flag]['building'] -= building_point_cost
                self.instruments[current_flag]['construct'].append(construct_instrument)

    def maintain_phase(self):
        for current_flag in range(2):
            for building_type, building_array in self.buildings[current_flag].items():
                for element in building_array:
                    building = element[0]
                    # Change the status if The building is maintaining.
                    for maintain_instrument in self.raw_instruments[current_flag]['maintain']:
                        if building.Unit_ID == maintain_instrument:
                            # Change the status of the true building, not its copy.
                            building_index = building_array.index(element)
                            self.buildings[current_flag][building_type][building_index][0].Is_Maintain = \
                                not self.buildings[current_flag][building_type][building_index][0].Is_Maintain
                            self.instruments[current_flag]['maintain'].append(maintain_instrument)
                            break

                    # Maintain the buildings.
                    max_HP = (OriginalBuildingAttribute[building.BuildingType][BuildingAttribute.ORIGINAL_HP] *
                              0.5 * (building.level + 2))
                    lost_percent = (max_HP - building.HP) / max_HP # The ratio of lost HP to max HP.
                    construct_money = (OriginalBuildingAttribute[building.BuildingType][BuildingAttribute.ORIGINAL_RESOURCE] *
                                       0.5 * (building.level + 2))
                    if (self.buildings[current_flag][building_type][building_index][0].Is_Maintain and
                        self.status['money'] > lost_percent * construct_money) :
                        self.buildings[current_flag][building_type][building_index][0].HP = max_HP
                        self.status['money'] -= lost_percent * construct_money

    def upgrade_phase(self):
        for current_flag in range(2):
            for building_type, building_array in self.buildings[current_flag].items():
                for element in building_array:
                    building = element[0]
                    for upgrade_instrument in self.raw_instruments[current_flag]['upgrade']:
                        if building.Unit_ID == upgrade_instrument:
                            building_index = building_array.index(element)
                            max_HP = (OriginalBuildingAttribute[building.BuildingType][BuildingAttribute.ORIGINAL_HP] *
                                      0.5 * (building.level + 2))
                            lost_percent = (max_HP - building.HP) / max_HP # The ratio of lost HP to max HP.
                            construct_money = (OriginalBuildingAttribute[building.BuildingType][BuildingAttribute.ORIGINAL_RESOURCE] *
                                               0.5 * (building.level + 2))
                            # The difference of construct money and max HP between old and upgraded towers.
                            upgrade_diff_money = OriginalBuildingAttribute[building.BuildingType][BuildingAttribute.ORIGINAL_RESOURCE]* 0.5
                            upgrade_diff_max_HP = OriginalBuildingAttribute[building.BuildingType][BuildingAttribute.ORIGINAL_HP] * 0.5

                            if (self.status['money'] > lost_percent * construct_money + upgrade_diff_money
                                and self.status['tech'] >= self.buildings[current_flag][building_type][building_index][0].level + 1):
                                self.buildings[current_flag][building_type][building_index][0].level += 1
                                self.buildings[current_flag][building_type][building_index][0].HP = max_HP + upgrade_diff_max_HP
                                self.status['money'] -= upgrade_diff_money + lost_percent * construct_money
                                self.instruments[current_flag]['upgrade'].append(upgrade_instrument)

    def sell_phase(self):
        age_increase_factor = 0.5 * (self.status[current_flag]['tech'] + 2)
        for current_flag in range(2):
            for sell_instrument in self.raw_instruments[current_flag]['sell']:
                have_found = False # Signal if the building to be sold has been found.
                for building_type, building_array in self.buildings[current_flag].items():
                    for element in building_array:
                        building = element[0]
                        if building.Unit_ID == sell_instrument:
                            max_HP = (OriginalBuildingAttribute[building.BuildingType][BuildingAttribute.ORIGINAL_HP] *
                                      0.5 * (building.level + 2))
                            return_percent = 0.5 if building.HP < 0.5 * max_HP else 1 - building.HP / max_HP
                            construct_money = (OriginalBuildingAttribute[building.BuildingType][BuildingAttribute.ORIGINAL_RESOURCE] *
                                               0.5 * (building.level + 2))

                            self.status['money'] += return_percent * construct_money
                            self.buildings[current_flag][building_type].remove(building)
                            have_found = True
                            break
                    if have_found:
                        break
                self.instruments[current_flag]['sell'].append(sell_instrument)

    def produce_phase(self):
        """Unit production by producing building"""
        pass

    def update_age_phase(self):
        """Deal with the update_age instruments"""
        basic_consumption = 0  #基础升级科技消耗，未定
        increased_consumption = 0   #科技每升一级，下次升级科技资源消耗增量
        for flag in range(2):
           if self.raw_instruments[flag]['update_age']:
                consumption = basic_consumption + increased_consumption*self.status[flag]['tech']
                if self.status[flag]['money'] > consumption and self.status[flag]['tech'] < Age.AI:
                    self.status[flag]['money'] -= consumption
                    self.status[flag]['tech'] += 1
                    self.instruments[flag]['update_age'].append(true)
                else:
                    self.instruments[flag]['update_age'].append(false)

    def resource_phase(self):
        """Produce new resource and refresh building force"""
        for flag in range(2):
            basic_resource=50
            resource=0
            for i in self.buildings[flag]['resource']:
                resource += (basic_resource * 0.5 * (self.status[flag]['tech']+2))
            self.status[flag]['money'] += resource
            self.status[flag]['building'] = self.status[flag]['tech'] * 60 + 100
            self.instruments[flag]['resource'].append(true)

    def next_tick(self):
        """回合演算与指令合法性判断"""
        self.attack_phase()
        self.clean_up_phase()
        self.move_phase()

        self.check_legal()

        self.building_phase()
        self.produce_phase()
        self.update_age_phase()
        self.resource_phase()
        # self.update_id()
        self.judge_winner()
