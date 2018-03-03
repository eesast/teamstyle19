#pragma once

#define _NULL -1
#define MY_INT_MAX 1000000000

//definition of enumeration
enum UnitType {
    Base,

    PRODUCTION_BUILDING,
    DEFENSIVE_BUILDING,
    RESOURCE_BUILDING,

    DATA,
    SUBSTANCE,
    ALL
};

enum Age {
    BIT,
    CIRCUIT,
    PROCESSOR,
    ALGORITHM,
    NETWORK,
    AI
};

enum BuildingType{
    //base
    __Base,

    //buidings for producing
    Shannon,
    Thevenin,
    Norton,
    Von_Neumann,
    Berners_Lee,
    Kuen_Kao,
    Turing,
    Tony_Stark,

    //buildings for defending
    Bool,
    Ohm,
    Mole,
    Monte_Carlo,
    Larry_Roberts,
    Robert_Kahn,
    Musk,
    Hawkin,

    //building for resource
    Programmer,
    Building_Type
};

enum BuildingAttribute {
    BUILDING_TYPE,
    ORIGINAL_HEAL,
    ORIGINAL_ATTACK,  //For defensive buildings, it stands for the level of attack.
                      //For resources buildings, it stands for Collective_Value
                      //For production buildings, it means nothing set as _NULL

    ORGINAL_RANGE,    //FOr production buildings, it stands for the range of production,
                      //For defensive buildings, it stands for the range of attacking
                      //For resource buildings, it means nothing

    TARGET,           //For production buildings, it stands for the type of units it produce,
                      //For defensive buildings, it stands for the type of units it attack.
    AGE,
    ORIGINAL_RESOURCE,
    ORIGINAL_BUILDING_POINT,
    AOE,              //Only works for defensive buildings
    CD,
    Attr_Num          //For the definition of Array
};

enum SoliderName {
    BIT_STREAM,
    VOLTAGE_SOURCE,
    CURRENT_SOURCE,
    ENIAC,
    PACKET,
    OPTICAL_FIBER,
    TURING_MACHINE,
    ULTRON,
    Solider_Type
};

enum SoliderAttr {
    SOLIDER_TYPE,
    ACTION_MODE,
    SOLIDER_ORIGINAL_HEAL,
    SOLIDER_ORIGINAL_ATTACK,
    ATTACK_RANGE,
    SPEED,
    Solider_Attr_Num  //For the definition of Array
};

enum ActionMode {
    BUILDING_ATTACK, //推塔
    BASE_ATTACK,     //冲锋
    MOVING_ATTACK    //抗线
};

const int OriginalBuildingAttribute[Building_Type][Attr_Num] = {
    /*TODO
    {Base,                          },
    */

    {PRODUCTION_BUILDING, 100,  _NULL,  10,   BIT_STREAM,      BIT,       100,    10,    _NULL,  1},
    {PRODUCTION_BUILDING, 120,  _NULL,  5,    VOLTAGE_SOURCE,  CIRCUIT,   120,    12,    _NULL,  2},
    {PRODUCTION_BUILDING, 120,  _NULL,  5,    CURRENT_SOURCE,  CIRCUIT,   120,    12,    _NULL,  2},
    {PRODUCTION_BUILDING, 150,  _NULL,  15,   ENIAC,           PROCESSOR, 150,    16,    _NULL,  5},
    {PRODUCTION_BUILDING, 360,  _NULL,  30,   PACKET,          NETWORK,   360,    12,    _NULL,  1},
    {PRODUCTION_BUILDING, 300,  _NULL,  15,   OPTICAL_FIBER,   NETWORK,   300,    30,    _NULL,  3},
    {PRODUCTION_BUILDING, 600,  _NULL,  15,   TURING_MACHINE,  AI,        600,    20,    _NULL,  8},
    {PRODUCTION_BUILDING, 1000, _NULL,  10,   ULTRON,          AI,        1000,   80,    _NULL,  10},

    {DEFENSIVE_BUILDING,  150,  16,     20,   DATA,            BIT,       150,    15,    0,      1},
    {DEFENSIVE_BUILDING,  180,  10,     25,   SUBSTANCE,       CIRCUIT,   180,    20,    3,      3},
    {DEFENSIVE_BUILDING,  225,  4,      35,   DATA,            PROCESSOR, 225,    25,    0,      1},
    {DEFENSIVE_BUILDING,  300,  25,     25,   SUBSTANCE,       ALGORITHM, 300,    30,    0,      2},
    {DEFENSIVE_BUILDING,  480,  5,      25,   ALL,             NETWORK,   480,    50,    2,      1},
    {DEFENSIVE_BUILDING,  450,30,   DATA,            NETWORK,   450,    45,    0,      1},
    {DEFENSIVE_BUILDING,  900,  0,      10,   ALL,             AI,        900,    90,    0,      1},
    {DEFENSIVE_BUILDING,  1500, MY_INT_MAX,10,   ALL,             AI,        1500,   100,   1,      5},

    {RESOURCE_BUILDING,            100,  50,     _NULL,_NULL,          _NULL,      _NULL,  _NULL, _NULL,  _NULL}
};

const int OriginalSoliderAttribute[Solider_Type][Solider_Attr_Num] = {
    {DATA,      BUILDING_ATTACK,        10,     10,     8,      8},
    {SUBSTANCE, BUILDING_ATTACK,        30,     16,     12,     6},
    {SUBSTANCE, BASE_ATTACK,            30,     160,    1,      6},
    {SUBSTANCE, MOVING_ATTACK,          200,    15,     5,      3},
    {DATA,      BASE_ATTACK,            30,     200,    1,      16},
    {SUBSTANCE, BUILDING_ATTACK,        40,     15,     30,     10},
    {DATA,      MOVING_ATTACK,          400,    10,     10,     2},
    {SUBSTANCE, BUILDING_ATTACK,        200,    1000,   10,     8}
};


//struct

//The global variables of both sides
struct Resource {
    int building_point_1;
    int building_point_2;

    int resource_1;
    int resource_2;
    Resource(int building_point_1=0, int building_point_2=0, int resource_1=0, int resource_2=0):
        building_point_1(building_point_1), building_point_2(building_point_2), resource_1(resource_1), resource_2(resource_2) {}
};

struct Position {
    int x;
    int y;
    Position(int x = -1, int y = -1): x(x), y(y) {}
};

struct Solider {
    SoliderName solider_name;
    int heal;
    Position pos;
    int flag;

    Solider();
    Solider(SoliderName solider_name, int heal, Position pos, int flag);
};

struct Building {
    BuildingType building_type;
    int heal;
    Position pos;
    int flag;
    int unit_id;
    bool maintain;

    Building();
    Building(BuildingType building_type, int heal, Position pos, int flag, int unit_id, bool maintain);
};

//API for players
void updateAge();
void construct(BuildingType building_type, Position pos, Position solider_pos); //The solier position is not set now
void upgrade(int unit_id);
void sell(int unit_id);
void toggleMaintain(int unit_id);
