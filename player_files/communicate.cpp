#include "communicate.h"
#include <string.h>

pickle::pickle() : _type(NoType), _gameOver(false), _id(-1) {}

void pickle::load(const char *msg, int32_t len)
{
    int32_t type = *reinterpret_cast<const int32_t *>(msg);
    msg += sizeof(int32_t);
    len -= sizeof(int32_t);
    switch (type)
    {
        case (int32_t) IdType:
            _type = IdType;
            _id = *reinterpret_cast<const int32_t *>(msg);
            break;
        case (int32_t) GameOverType:
            _type = GameOverType;
            _gameOver = true;
            break;
        default:
            _type = NoType;
    }
}

MsgType pickle::getType() const
{
    return _type;
}

int pickle::getId() const
{
    return _id;
}

std::pair<char *, int> pickle::dumpId(int id)
{
    int size = 2 * sizeof(int32_t);
    char *data = new char[size];
    int32_t temp = IdType;
    memcpy(data, &temp, sizeof(int32_t));
    temp = id;
    memcpy(data + sizeof(int32_t), &temp, sizeof(int32_t));
    return std::pair<char *, int>(data, size);
}

