from unit import *


class GameMain:
    _map_size = 200
    _map = [[0] * _map_size] * _map_size
    turn_num = 0
    winner = 3

    units = [{}] * 2

    main_base = [None] * 2

    buildings = [{
        'produce': [],
        'defence': [],
        'resource': []
    }] * 2

    status = [{
        'money': 0,
        'tech': 0,
        'building': 0,
    }] * 2

    # 通信模块将收到的指令写入，各阶段函数从中读取指令，指令格式同api_player.h
    raw_instruments = [{
        'construct': [],  # (BuildingType,(BuildingPos.x,BuildingPos.y),(SoldierPos.x,SoldierPos.y))
        'maintain': [],  # id
        'upgrade': [],  # id
        'sell': [],  # id
        'update_age': False,
    }] * 2

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
    }] * 2

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
        pass

    def resource_phase(self):
        """Produce new resource"""
        pass

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
