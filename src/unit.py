# ***************************The Define of Global Parameters**************************************

Inf = 9999999

BYTE = 1
CIRCUIT = 2
CPU = 3
ALGORITHM = 4
NETWORK = 5
AI = 6

DATA = 11
ENTITY = 12
ALL = 13

BYTESTREAM = 21
USOURCE = 22
ISOURCE = 23
ENIAC = 24
DATAPACKAGE = 25
OPTICAL = 26
TURINGMACHINE = 27
ULTRON = 28

ATTACK_TOWER = 31
GO_STRAIGHT = 32
DEFENCE_ATTACK = 33


#******************************************************************************

#************************************Basic Class**************************************

class Building(object):
    def __init__(self, time, basic_hp, unlock_time, basic_source, basic_building_ability):
        self.__HP = basic_hp * (0.5 + 0.5 * time)
        self.__Time = unlock_time
        self.__Source = basic_source * (0.5 + 0.5 * time)
        self.__Building_Ability = basic_building_ability * (0.5 + 0.5 * time)

    @property
    def HP(self):
        return self.__HP

    @HP.setter
    def HP(self, hp):
        # some condition
        self.__HP = hp

    @property
    def Time(self):
        return self.__Time

    @Time.setter
    def Time(self, time):
        # some condition
        self.__Time = time

    @property
    def Source(self):
        return self.__Source

    @Source.setter
    def Source(self, source):
        # some conditon here
        self.__Source = source

    @property
    def Building_Ability(self):
        return self.__Building_Ability

    @Building_Ability.setter
    def Building_Ability(self, b):
        # some condition here
        self.__Building_Ability = b


class Produce_Building(Building):
    def __init__(self, time, basic_hp, unlock_time, basic_source, basic_building_ability, produce_range, produce_cd, produce_unit):
        self.__Produce_Range = produce_range
        self.__Produce_CD = produce_cd
        self.__Produce_Unit = produce_unit
        Building.__init__(self, time, basic_hp, unlock_time,
                          basic_source, basic_building_ability)

    @property
    def Produce_Range(self):
        return self.__Produce_Range

    @Produce_Range.setter
    def Produce_Range(self, range):
        # some condition here
        self.__Produce_Range = range

    @property
    def Produce_CD(self):
        return self.__Produce_CD

    @Produce_CD.setter
    def Produce_CD(self, cd):
        # some condition here
        self.__Produce_CD = cd

    @property
    def Produce_Unit(self):
        return self.__Produce_Unit

    @Produce_Unit.setter
    def Produce_Unit(self, unit):
        # some condition here
        self.__Produce_Unit = unit


class Defence_Building(Building):
    def __init__(self, time, basic_hp, unlock_time, basic_source, basic_building_ability, attack_cd, attack_range, attack_hurt, attack_target, aoe):
        self.__Attack_CD = attack_cd
        self.__Attack_Range = attack_range
        self.__Attack_Target = attack_target
        self.__Attack_Hurt = attack_hurt
        self.__AOE = aoe
        Building.__init__(self, basic_hp, time, unlock_time,
                          basic_source, basic_building_ability)

    @property
    def Attack_CD(self):
        return self.__Attack_CD

    @Attack_CD.setter
    def Attack_CD(self, cd):
        # some condition here
        self.__Attack_CD = cd

    @property
    def Attack_Range(self):
        return self.__Attack_Range

    @Attack_Range.setter
    def Attack_Range(self, range):
        # some condition here
        self.__Attack_Range = range

    @property
    def Attack_Target(self):
        return self.__Attack_Target

    @Attack_Target.setter
    def Attack_Target(self, target):
        # some condition here
        self.__Attack_Target = target

    @property
    def AOE(self):
        return self.AOE

    @AOE.setter
    def AOE(self, aoe):
        # some condition here
        self.__AOE = aoe


class Unit(object):
    def __init__(self, Type, time, behaviour_mode, basic_hp, basic_attack_hurt, attack_range, move_speed):
        self.__Type = Type
        self.__HP = basic_hp * (0.5 * time + 0.5)
        self.__Behaviour_Mode = behaviour_mode
        self.__Attack_Hurt = basic_attack_hurt * (0.5 + 0.5 * basic_hp)
        self.__Attack_Range = attack_range
        self.__Move_Speed = move_speed

    @property
    def HP(self):
        return self.__HP

    @HP.setter
    def HP(self, hp):
        # some condition
        self.__HP = hp

    @property
    def Type(self):
        return self.__Type

    @property
    def Behaviour_Mode(self):
        return self.__Behaviour_Mode

    @property
    def Attack_Hurt(self):
        return self.__Attack_Hurt

    @Attack_Hurt.setter
    def Attack_Hurt(self, hurt):
        # some condition here
        self.__Attack_Hurt = hurt

    @property
    def Attack_Range(self):
        return self.__Attack_Range

    @Attack_Range.setter
    def Attack_Range(self, range):
        # some condition here
        self.__Attack_Range = range

    @property
    def Move_Speed(self):
        return self.__Move_Speed

    @Move_Speed.setter
    def Move_Speed(self, speed):
        # some condition here
        self.Move_Speed = speed


#**********************************************************************************************************

#********************************************Resource Building***********************************

class Resource_Building(object):
    def __init__(self, time):
        self.HP = 100 * (0.5 + time * 0.5)
        self.Get_Resource_Value = 50


#******************************************Produce Building******************************************

class Shannon(Produce_Building):
    def __init__(self, time):
        Produce_Building.__init__(
            self, time, 100, BYTE, 100, 10, 10, 1, BYTESTREAM)


class Thevenin(Produce_Building):
    def __init__(self, time):
        Produce_Building.__init__(
            self, time, 120, CIRCUIT, 120, 12, 5, 2, USOURCE)


class Norton(Produce_Building):
    def __init__(self, time):
        Produce_Building.__init__(
            self, time, 120, CIRCUIT, 120, 12, 5, 2, ISOURCE)


class Von_Neumann(Produce_Building):
    def __init__(self, time):
        Produce_Building.__init__(self, time, 150, CPU, 150, 16, 15, 5, ENIAC)


class Berners_Lee(Produce_Building):
    def __init__(self, time):
        Produce_Building.__init__(
            self, time, 360, NETWORK, 360, 12, 30, 1, DATAPACKAGE)


class Kuen_Kao(Produce_Building):
    def __init__(self, time):
        Produce_Building.__init__(
            self, time, 300, NETWORK, 300, 30, 15, 3, OPTICAL)


class Turning(Produce_Building):
    def __init__(self, time):
        Produce_Building.__init__(
            self, time, 600, AI, 600, 20, 15, 8, TURINGMACHINE)


class Tony_Stark(Produce_Building):
    def __init__(self, time):
        Produce_Building.__init__(
            self, time, 1000, AI, 1000, 80, 10, 10, ULTRON)


#******************************************************************************************************

#*****************************************Defence Building**************************************************

class Bool(Defence_Building):
    def __init__(self, time):
        Defence_Building.__init__(
            self, time, 150, BYTE, 150, 15, 1, 20, 16, DATA, 0)

    def skill(self):
        pass


class Ohm(Defence_Building):
    def __init__(self, time):
        Defence_Building.__init__(
            self, time, 180, CIRCUIT, 180, 20, 3, 25, 10, ENTITY, 3)

    def skill(self):
        pass


class Nole(Defence_Building):
    def __init__(self, time):
        Defence_Building.__init__(
            self, time, 225, DATA, 225, 25, 1, 35, 4, DATA, 0)

    def skill(self):
        pass


class Monte_Carlo(Defence_Building):
    def __init__(self, time):
        Defence_Building.__init__(
            self, time, 300, ALGORITHM, 300, 30, 2, 25, 25, ENTITY, 0)

    def skill(self):
        pass


class Larry_Roberts(Defence_Building):
    def __init__(self, time):
        Defence_Building.__init__(
            self, time, 480, NETWORK, 480, 50, 1, 25, 5, ALL, 2)

    def skill(self):
        pass


class Robert_Kabn(Defence_Building):
    def __init__(self, time):
        Defence_Building.__init__(
            self, time, 450, NETWORK, 450, 45, 1, 30, None, DATA, 0)  # 攻击力暂未设定

    def skill(self):
        pass


class Musk(Defence_Building):
    def __init__(self, time):
        Defence_Building.__init__(
            self, time, 900, AI, 900, 90, 1, 10, 0, ALL, 0)

    def skill(self):
        pass


class Hawkin(Defence_Building):
    def __init__(self, time):
        Defence_Building.__init__(
            self, time, 1500, AI, 1500, 100, 5, 10, Inf, ALL, 1)

    def skill(self):
        pass


#**************************************************************************************************************

#************************************************Unit***************************************

class Bytestream(Unit):
    def __init__(self, time):
        Unit.__init__(self, DATA, time, ATTACK_TOWER, 10, 10, 8, 8)


class Usource(Unit):
    def __init__(self, time):
        Unit.__init__(self, ENTITY, time, ATTACK_TOWER, 30, 16, 12, 6)


class Isource(Unit):
    def __init__(self, time):
        Unit.__init__(self, ENTITY, time, GO_STRAIGHT, 30, 160, 1, 6)


class Eniac(Unit):
    def __init__(self, time):
        Unit.__init__(self, ENTITY, time, DEFENCE_ATTACK, 200, 15, 5, 3)


class DataPackage(Unit):
    def __init__(self, time):
        Unit.__init__(self, DATA, time, GO_STRAIGHT, 30, 200, 1, 16)


class Optical(Unit):
    def __init__(self, time):
        Unit.__init__(self, ENTITY, time, ATTACK_TOWER, 40, 15, 30, 10)


class TurningMachine(Unit):
    def __init__(self, time):
        Unit.__init__(self, DATA, time, DEFENCE_ATTACK, 400, 10, 10, 2)


class Ultron(Unit):
    def __init__(self, time):
        Unit.__init__(self, ENTITY, time, ATTACK_TOWER, 200, 1000, 10, 8)


#**************************************************************************************************************
