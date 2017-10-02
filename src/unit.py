from enum import Enum

'''（请允许我加一段中文注释。。。
为保证基类调用时的安全性 所有属性都设置为了私有 同时为了方便调用 使用了装饰器来提供返回值
但没有设置 set函数的装饰器，因此属性现在处于能读不能取的状态 在以后确定了哪些变量需要在运行期间重新赋值再加入对应的set的装饰器'''

# ***************************The Define of Global Parameters**************************************
Inf=9999999
#**************************************************Enum Value ant Table******************************************
class UnitType(Enum):
    Base = 0

    PRODUCTION_BUILDING = 1
    DEFENSIVE_BUILDING = 2
    RESOURCE_BUILDING = 3

    DATA = 4
    SUBSTANCE = 5
    ALL = 6

class Age(Enum):
    BIT = 0
    CIRCUIT = 1
    PROCESSOR = 2
    ALGORITHM = 3
    NETWORK = 4
    AI = 5

class BuildingType(Enum):
    Base=0

    Shannon=1
    Thevenin=2
    Norton=3
    Von_Neumann=4
    Berners_Lee=5
    Kuen_Kao=6
    Turing=7
    Tony_Stark=8

    Bool=9
    Ohm=10
    Mole=11
    Monte_Carlo=12
    Larry_Roberts=13
    Robert_Kahn=14
    Musk=15
    Hawkin=16

    Programmer=17

class BuildingAttribute(Enum):
    BUILDING_TYPE=0
    ORIGINAL_HP=1
    ORIGINAL_ATTACK=2
    ORIGINAL_RANGE=3
    TRAGET=4
    AGE=5
    ORIGINAL_RESOURCE=6
    ORIGINAL_BUILDING_POINT=7
    AOE=8
    CD=9

class SoliderName(Enum):
    BIT_STREAM=0
    VOLTAGE_SOURCE=1
    CURRENT_SOURCE=2
    ENIAC=3
    PACKET=4
    OPTICAL_FIBER=5
    TURNING_MACHINE=6
    ULTRON=7

class SoliderAttr(Enum):
    SOLIDER_TYPE=0
    ACTION_MODE=1
    SOLIDER_ORIGINAL_HP=2
    SOLIDER_ORIGINAL_ATTACK=3
    ATTACK_RANGE=4
    SPEED=5

class ActionMode(Enum):
    BUILDING_ATTACK=0
    BASE_ATTACK=1
    MOVING_ATTACK=2

OriginalBuildingAttribute={

BuildingType.Base:{BuildingAttribute.BUILDING_TYPE:UnitType.Base,None:None},    #need to complete
BuildingType.Shannon:{ BuildingAttribute.BUILDING_TYPE:UnitType.PRODUCTION_BUILDING , BuildingAttribute.ORIGINAL_HP:100 , BuildingAttribute.ORIGINAL_ATTACK:None, BuildingAttribute.ORIGINAL_RANGE:10 ,BuildingAttribute.TRAGET:SoliderName.BIT_STREAM ,BuildingAttribute.AGE:Age.BIT ,BuildingAttribute.ORIGINAL_RESOURCE:100 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:10 ,BuildingAttribute.AOE:None ,BuildingAttribute.CD: 1},
BuildingType.Thevenin:{ BuildingAttribute.BUILDING_TYPE:UnitType.PRODUCTION_BUILDING , BuildingAttribute.ORIGINAL_HP:120 , BuildingAttribute.ORIGINAL_ATTACK:None, BuildingAttribute.ORIGINAL_RANGE:5 ,BuildingAttribute.TRAGET:SoliderName.VOLTAGE_SOURCE ,BuildingAttribute.AGE:Age.CIRCUIT ,BuildingAttribute.ORIGINAL_RESOURCE:120 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:12 ,BuildingAttribute.AOE:None ,BuildingAttribute.CD: 2},
BuildingType.Norton:{ BuildingAttribute.BUILDING_TYPE:UnitType.PRODUCTION_BUILDING , BuildingAttribute.ORIGINAL_HP:120 , BuildingAttribute.ORIGINAL_ATTACK:None, BuildingAttribute.ORIGINAL_RANGE:5 ,BuildingAttribute.TRAGET:SoliderName.CURRENT_SOURCE ,BuildingAttribute.AGE:Age.CIRCUIT ,BuildingAttribute.ORIGINAL_RESOURCE:120 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:12 ,BuildingAttribute.AOE:None ,BuildingAttribute.CD: 2},
BuildingType.Von_Neumann:{ BuildingAttribute.BUILDING_TYPE:UnitType.PRODUCTION_BUILDING , BuildingAttribute.ORIGINAL_HP:150 , BuildingAttribute.ORIGINAL_ATTACK:None, BuildingAttribute.ORIGINAL_RANGE:15 ,BuildingAttribute.TRAGET:SoliderName.ENIAC ,BuildingAttribute.AGE:Age.PROCESSOR ,BuildingAttribute.ORIGINAL_RESOURCE:150 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:16 ,BuildingAttribute.AOE:None ,BuildingAttribute.CD: 5},
BuildingType.Berners_Lee:{ BuildingAttribute.BUILDING_TYPE:UnitType.PRODUCTION_BUILDING , BuildingAttribute.ORIGINAL_HP:360 , BuildingAttribute.ORIGINAL_ATTACK:None, BuildingAttribute.ORIGINAL_RANGE:30 ,BuildingAttribute.TRAGET:SoliderName.PACKET ,BuildingAttribute.AGE:Age.NETWORK ,BuildingAttribute.ORIGINAL_RESOURCE:360 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:12 ,BuildingAttribute.AOE:None ,BuildingAttribute.CD: 1},
BuildingType.Kuen_Kao:{ BuildingAttribute.BUILDING_TYPE:UnitType.PRODUCTION_BUILDING , BuildingAttribute.ORIGINAL_HP:300 , BuildingAttribute.ORIGINAL_ATTACK:None, BuildingAttribute.ORIGINAL_RANGE:15 ,BuildingAttribute.TRAGET:SoliderName.OPTICAL_FIBER ,BuildingAttribute.AGE:Age.NETWORK ,BuildingAttribute.ORIGINAL_RESOURCE:300 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:30 ,BuildingAttribute.AOE:None ,BuildingAttribute.CD: 3},
BuildingType.Turing:{ BuildingAttribute.BUILDING_TYPE:UnitType.PRODUCTION_BUILDING , BuildingAttribute.ORIGINAL_HP:600 , BuildingAttribute.ORIGINAL_ATTACK:None, BuildingAttribute.ORIGINAL_RANGE:15 ,BuildingAttribute.TRAGET:SoliderName.TURNING_MACHINE ,BuildingAttribute.AGE:Age.AI ,BuildingAttribute.ORIGINAL_RESOURCE:600 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:20 ,BuildingAttribute.AOE:None ,BuildingAttribute.CD: 8},
BuildingType.Tony_Stark:{ BuildingAttribute.BUILDING_TYPE:UnitType.PRODUCTION_BUILDING , BuildingAttribute.ORIGINAL_HP:1000 , BuildingAttribute.ORIGINAL_ATTACK:None, BuildingAttribute.ORIGINAL_RANGE:10 ,BuildingAttribute.TRAGET:SoliderName.TURNING_MACHINE ,BuildingAttribute.AGE:Age.AI ,BuildingAttribute.ORIGINAL_RESOURCE:1000 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:80 ,BuildingAttribute.AOE:None ,BuildingAttribute.CD: 10},

BuildingType.Bool:{ BuildingAttribute.BUILDING_TYPE:UnitType.DEFENSIVE_BUILDING , BuildingAttribute.ORIGINAL_HP:150 , BuildingAttribute.ORIGINAL_ATTACK:16, BuildingAttribute.ORIGINAL_RANGE:20 ,BuildingAttribute.TRAGET:UnitType.DATA ,BuildingAttribute.AGE:Age.BIT ,BuildingAttribute.ORIGINAL_RESOURCE:150 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:15 ,BuildingAttribute.AOE:0 ,BuildingAttribute.CD: 1},
BuildingType.Ohm:{ BuildingAttribute.BUILDING_TYPE:UnitType.DEFENSIVE_BUILDING , BuildingAttribute.ORIGINAL_HP:180 , BuildingAttribute.ORIGINAL_ATTACK:10, BuildingAttribute.ORIGINAL_RANGE:25 ,BuildingAttribute.TRAGET:UnitType.SUBSTANCE ,BuildingAttribute.AGE:Age.CIRCUIT ,BuildingAttribute.ORIGINAL_RESOURCE:180 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:20 ,BuildingAttribute.AOE:3 ,BuildingAttribute.CD: 3},
BuildingType.Mole:{ BuildingAttribute.BUILDING_TYPE:UnitType.DEFENSIVE_BUILDING, BuildingAttribute.ORIGINAL_HP:225 , BuildingAttribute.ORIGINAL_ATTACK:4, BuildingAttribute.ORIGINAL_RANGE:35 ,BuildingAttribute.TRAGET:UnitType.DATA ,BuildingAttribute.AGE:Age.PROCESSOR ,BuildingAttribute.ORIGINAL_RESOURCE:225 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:25 ,BuildingAttribute.AOE:0 ,BuildingAttribute.CD: 1},
BuildingType.Monte_Carlo:{ BuildingAttribute.BUILDING_TYPE:UnitType.DEFENSIVE_BUILDING , BuildingAttribute.ORIGINAL_HP:300 , BuildingAttribute.ORIGINAL_ATTACK:25, BuildingAttribute.ORIGINAL_RANGE:25 ,BuildingAttribute.TRAGET:UnitType.SUBSTANCE ,BuildingAttribute.AGE:Age.ALGORITHM ,BuildingAttribute.ORIGINAL_RESOURCE:300 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:30 ,BuildingAttribute.AOE:0 ,BuildingAttribute.CD: 2},
BuildingType.Larry_Roberts:{ BuildingAttribute.BUILDING_TYPE:UnitType.DEFENSIVE_BUILDING , BuildingAttribute.ORIGINAL_HP:480 , BuildingAttribute.ORIGINAL_ATTACK:5, BuildingAttribute.ORIGINAL_RANGE:25 ,BuildingAttribute.TRAGET:UnitType.ALL ,BuildingAttribute.AGE:Age.NETWORK ,BuildingAttribute.ORIGINAL_RESOURCE:480 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:50 ,BuildingAttribute.AOE:2 ,BuildingAttribute.CD: 1},
BuildingType.Robert_Kahn:{ BuildingAttribute.BUILDING_TYPE:UnitType.DEFENSIVE_BUILDING , BuildingAttribute.ORIGINAL_HP:450 , BuildingAttribute.ORIGINAL_ATTACK:None , BuildingAttribute.ORIGINAL_RANGE:30 ,BuildingAttribute.TRAGET:UnitType.DATA ,BuildingAttribute.AGE:Age.NETWORK ,BuildingAttribute.ORIGINAL_RESOURCE:450 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:45 ,BuildingAttribute.AOE:0 ,BuildingAttribute.CD: 1},
BuildingType.Musk:{ BuildingAttribute.BUILDING_TYPE:UnitType.DEFENSIVE_BUILDING, BuildingAttribute.ORIGINAL_HP:900 , BuildingAttribute.ORIGINAL_ATTACK:0, BuildingAttribute.ORIGINAL_RANGE:10 ,BuildingAttribute.TRAGET:UnitType.ALL ,BuildingAttribute.AGE:Age.AI ,BuildingAttribute.ORIGINAL_RESOURCE:900 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:90 ,BuildingAttribute.AOE:0 ,BuildingAttribute.CD: 1},
BuildingType.Hawkin:{ BuildingAttribute.BUILDING_TYPE:UnitType.DEFENSIVE_BUILDING , BuildingAttribute.ORIGINAL_HP:1500 , BuildingAttribute.ORIGINAL_ATTACK:Inf, BuildingAttribute.ORIGINAL_RANGE:10 ,BuildingAttribute.TRAGET:UnitType.ALL ,BuildingAttribute.AGE:Age.AI ,BuildingAttribute.ORIGINAL_RESOURCE:1500 ,BuildingAttribute.ORIGINAL_BUILDING_POINT:100 ,BuildingAttribute.AOE:1 ,BuildingAttribute.CD: 5},

BuildingType.Programmer:{ BuildingAttribute.BUILDING_TYPE:UnitType.DEFENSIVE_BUILDING , BuildingAttribute.ORIGINAL_HP:100 , BuildingAttribute.ORIGINAL_ATTACK:50},  #use attack stand for the ability of resource building to get resource
}

OriginalSoliderAttribute={
    SoliderName.BIT_STREAM:{SoliderAttr.SOLIDER_TYPE:UnitType.DATA ,SoliderAttr.ACTION_MODE:ActionMode.BUILDING_ATTACK ,SoliderAttr.SOLIDER_ORIGINAL_HP:10 ,SoliderAttr.SOLIDER_ORIGINAL_ATTACK:10 ,SoliderAttr.ATTACK_RANGE:8 ,SoliderAttr.SPEED:8 },
    SoliderName.VOLTAGE_SOURCE:{SoliderAttr.SOLIDER_TYPE: UnitType.SUBSTANCE, SoliderAttr.ACTION_MODE: ActionMode.BUILDING_ATTACK, SoliderAttr.SOLIDER_ORIGINAL_HP: 30,SoliderAttr.SOLIDER_ORIGINAL_ATTACK: 16, SoliderAttr.ATTACK_RANGE: 12,SoliderAttr.SPEED: 6},
    SoliderName.CURRENT_SOURCE:{SoliderAttr.SOLIDER_TYPE: UnitType.SUBSTANCE, SoliderAttr.ACTION_MODE: ActionMode.BASE_ATTACK, SoliderAttr.SOLIDER_ORIGINAL_HP: 30, SoliderAttr.SOLIDER_ORIGINAL_ATTACK: 160, SoliderAttr.ATTACK_RANGE: 1,SoliderAttr.SPEED: 6},
    SoliderName.ENIAC: {SoliderAttr.SOLIDER_TYPE: UnitType.SUBSTANCE,SoliderAttr.ACTION_MODE: ActionMode.MOVING_ATTACK, SoliderAttr.SOLIDER_ORIGINAL_HP: 200,SoliderAttr.SOLIDER_ORIGINAL_ATTACK: 15, SoliderAttr.ATTACK_RANGE: 5,SoliderAttr.SPEED: 3},
    SoliderName.PACKET: {SoliderAttr.SOLIDER_TYPE: UnitType.DATA,SoliderAttr.ACTION_MODE: ActionMode.BASE_ATTACK, SoliderAttr.SOLIDER_ORIGINAL_HP: 30,SoliderAttr.SOLIDER_ORIGINAL_ATTACK: 200, SoliderAttr.ATTACK_RANGE: 1, SoliderAttr.SPEED: 16},
    SoliderName.OPTICAL_FIBER: {SoliderAttr.SOLIDER_TYPE: UnitType.SUBSTANCE,SoliderAttr.ACTION_MODE: ActionMode.BUILDING_ATTACK, SoliderAttr.SOLIDER_ORIGINAL_HP: 40,SoliderAttr.SOLIDER_ORIGINAL_ATTACK: 15, SoliderAttr.ATTACK_RANGE:30, SoliderAttr.SPEED: 10},
    SoliderName.TURNING_MACHINE: {SoliderAttr.SOLIDER_TYPE: UnitType.DATA,SoliderAttr.ACTION_MODE: ActionMode.MOVING_ATTACK, SoliderAttr.SOLIDER_ORIGINAL_HP: 400,SoliderAttr.SOLIDER_ORIGINAL_ATTACK: 10, SoliderAttr.ATTACK_RANGE: 10, SoliderAttr.SPEED: 2},
    SoliderName.ULTRON: {SoliderAttr.SOLIDER_TYPE: UnitType.SUBSTANCE, SoliderAttr.ACTION_MODE: ActionMode.BUILDING_ATTACK,SoliderAttr.SOLIDER_ORIGINAL_HP: 200, SoliderAttr.SOLIDER_ORIGINAL_ATTACK: 1000,SoliderAttr.ATTACK_RANGE: 10, SoliderAttr.SPEED: 8},
}

#****************************************************************************************************************************************************************

#***************************************************************************Basic Class*****************************************************************************
class Resource(obejct):
    def __init__(self,building_point_1,building_point_2,resource_1,resource_2):
        self.__building_point_1=building_point_1
        self.__building_point_2=building_point_2
        self.__resource_1=resource_1
        self.__resource_2=resource_2

    @property
    def building_point_1(self):
        return self.__building_point_1

    @property
    def building_point_2(self):
        return self.__building_point_2

    @property
    def resource_1(self):
        return self.__resource_1

    @property
    def resource_2(self):
        return self.__resource_2

class Position(object):
    def __init__(self,x,y):
        self.__x=x
        self.__y=y

    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y

class Building(object):
    def __init__(self,building_type,hp,pos,flag,unit_id,maintain):
        self.__BuildingType=building_type
        self.__HP=hp
        self.__Position=pos
        self.__Flag=flag
        self.__Unit_ID=unit_id
        self.__Is_Maintain=maintain

    @property
    def HP(self):
        return self.__HP
    @HP.setter
    def HP(self,hp):
        #some condition
        self.__HP=hp
    @property
    def BuildingType(self):
        return self.__BuildingType

    @property
    def Position(self):
        return self.__Position

    @property
    def Flag(self):
        return self.__Flag

    @property
    def Unit_ID(self):
        return self.__Unit_ID

    @property
    def Is_Maintain(self):
        return self.__Is_Maintain

class Solider(object):
    def __init__(self,solider_name,hp,pos,flag):
        self.__Solider_Name=solider_name
        self.__HP=hp
        self.__Position=pos
        self.__Flag=flag

    @property
    def HP(self):
        return self.__HP
    @HP.setter
    def HP(self, hp):
        # some condition
        self.__HP = hp

    @property
    def Solider_Name(self):
        return self.__Solider_Name

    @property
    def Position(self):
        return self.__Position

    @property
    def Flag(self):
        return self.__Flag

#***************************************************************************************************************************************************************************************************