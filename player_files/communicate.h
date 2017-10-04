#ifndef COMMUNICATE_COMMUNICATE_H
#define COMMUNICATE_COMMUNICATE_H

#include <utility>
#include <stdint.h>

enum MsgType {
    NoType = 0,
    IdType = 1,
    MapType = 2,
    DataType = 3,
    InstrType = 4,
    GameOverType = 5
};

class recv_send_socket {
public:
    virtual void send_data(const char *msg, int32_t len)=0;

    virtual std::pair<char *, int> recv_data()=0;

    virtual void connect_to_server(const char *ip_address, unsigned short port)=0;
};

recv_send_socket *create_socket();

class pickle {
public:
    pickle();

    void load(const char *msg, int32_t len);

    std::pair<char *, int> dumpId(int id);

private:
    MsgType _type;
    bool _gameOver;
    int _id;
public:
    MsgType getType() const;

    int getId() const;
};


#endif //COMMUNICATE_COMMUNICATE_H
