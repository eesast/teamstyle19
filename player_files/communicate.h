#ifndef COMMUNICATE_COMMUNICATE_H
#define COMMUNICATE_COMMUNICATE_H

#include <utility>
#include <stdint.h>
#include <vector>
#include "api_player.h"

using std::vector;

enum MsgType {
    NoType = 0,
    IdMsg = 1,
    MapMsg = 2,
    DataMsg = 3,
    InstrMsg = 4,
    GameOverMsg = 5
};

enum InstrType {
    UpdateAge = 1,
    Construct = 2,
    Upgrade = 3,
    Sell = 4,
    Maintain = 5
};

//Interface for communication
class RecvSendSocket {
public:
    virtual void send_data(const char *msg, int32_t len)=0;

    virtual std::pair<char *, int> recv_data(bool blocked)=0;

    virtual void connect_to_server(const char *ip_address, unsigned short port)=0;

};

//Infinite loop for receiving data
void static_recv_data(RecvSendSocket *socket);

//Factory function
RecvSendSocket *create_socket();

//Dump and undamp message
class Pickle {
public:
    Pickle();

    void load(const char *msg, int32_t len);

    std::pair<char *, int> dumpId(int id);

    std::pair<char *, int> dumpInstr();

private:
    MsgType _type;
    bool _gameOver;
    int _id;
public:
    MsgType getType() const;

    int getId() const;
};

union Command_data {
    int unit_id;
    struct BuildingData {
        BuildingType type;
        int pos_x, pos_y, soldier_x, soldier_y;
    } building_data;
};

struct Command {
    InstrType _type;
    Command_data _data;

    Command(InstrType type, int unit_id)
    {
        _type = type;
        _data.unit_id = unit_id;
    }

    Command(InstrType type, BuildingType build_type, Position pos, Position soldier_pos)
    {
        _type = type;
        _data.building_data.type = build_type;
        _data.building_data.pos_x = pos.x;
        _data.building_data.pos_y = pos.y;
        _data.building_data.soldier_x = soldier_pos.x;
        _data.building_data.soldier_y = soldier_pos.y;
    }
};


#endif //COMMUNICATE_COMMUNICATE_H
