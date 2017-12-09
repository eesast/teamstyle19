#include "communicate.h"
#include <vector>
#include <string.h>

using std::vector;

extern vector<Command> command_queue;
extern bool askUpdateAge;

Pickle::Pickle() : _type(NoType), _gameOver(false), _id(-1) {}

void Pickle::load(const char *msg, int32_t len)
{
    int32_t type = *reinterpret_cast<const int32_t *>(msg);
    msg += sizeof(int32_t);
    len -= sizeof(int32_t);
    switch (type)
    {
        case (int32_t) IdMsg:
            _type = IdMsg;
            _id = *reinterpret_cast<const int32_t *>(msg);
            break;
        case (int32_t) GameOverMsg:
            _type = GameOverMsg;
            _gameOver = true;
            break;
        case (int32_t) DataMsg:
            _type = DataMsg;
            break;
        default:
            _type = NoType;
    }
}

MsgType Pickle::getType() const
{
    return _type;
}

int Pickle::getId() const
{
    return _id;
}

std::pair<char *, int> Pickle::dumpId(int id)
{
    int size = 2 * sizeof(int32_t);
    char *data = new char[size];
    int32_t temp = IdMsg;
    memcpy(data, &temp, sizeof(int32_t));
    temp = id;
    memcpy(data + sizeof(int32_t), &temp, sizeof(int32_t));
    return std::pair<char *, int>(data, size);
}

std::pair<char *, int> Pickle::dumpInstr()
{
    vector<int32_t> data;
    data.push_back(InstrMsg);
    for (vector<Command>::iterator it = command_queue.begin(); it != command_queue.end(); ++it)
    {
        data.push_back(it->_type);
        if (it->_type == Construct)
        {
            data.push_back(it->_data.building_data.type);
            data.push_back(it->_data.building_data.pos_x);
            data.push_back(it->_data.building_data.pos_y);
            data.push_back(it->_data.building_data.soldier_x);
            data.push_back(it->_data.building_data.soldier_y);
        } else
        {
            data.push_back(it->_data.unit_id);
        }
    }
    if (askUpdateAge)
        data.push_back(UpdateAge);
    askUpdateAge = false;
    command_queue.clear();
    char *buffer = new char[data.size() * sizeof(int32_t)];
    memcpy(buffer, data.data(), data.size() * sizeof(int32_t));
    return std::pair<char *, int>(buffer, data.size() * sizeof(int32_t));
}

