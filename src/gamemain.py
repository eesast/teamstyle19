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
        pass

    def building_phase(self):
        """Deal with the instruments about buildings"""

        def construct_phase(self):
            pass

        def maintain_phase(self):
            pass

        def upgrade_phase(self):
            pass

        def sell_phase(self):
            pass

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
