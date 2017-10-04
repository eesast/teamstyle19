from unit import *
from unit import Age

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
        pass

    def init_map_from_bitmap(self):
        pass

    def __init__(self, init_map):
        pass

    def judge_winnner(self):
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

        if  self.instruments[0]['update_age']:
            consumption = basic_consumption + increased_consumption*self.status[0]['tech']
            if  self.status[0]['money'] > consumption and self.status[0]['tech'] < Age.AI:
                self.status[0]['money'] -= consumption
                self.status[0]['tech'] += 1
            else:
                pass
        if self.instruments[1]['update_age']:
            consumption = basic_consumption + increased_consumption * self.status[1]['tech']
            if self.status[1]['money'] > consumption and self.status[1]['tech'] < Age.AI:
                self.status[1]['money'] -= consumption
                self.status[1]['tech'] += 1
            else:
                pass

    def resource_phase(self):
        """Produce new resource and refresh building force"""

        basic_resource=50
        resource0=0
        resource1=0

        for i in self.buildings[0]['resource']:
            resource0 += (basic_resource * 0.5 * (self.status[0]['tech']+2))
        for i in self.buildings[1]['resource']:
            resource1 += (basic_resource * 0.5 * (self.status[1]['tech']+2))

        self.status[0]['money'] += resource0
        self.status[1]['money'] += resource1

        self.status[0]['building'] = self.status[0]['tech'] * 60 + 100
        self.status[1]['building'] = self.status[1]['tech'] * 60 + 100

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
        self.judge_winnner()
