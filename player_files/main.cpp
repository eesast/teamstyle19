#include <stdio.h>
#include <stdlib.h>
#include "communicate.h"
#include <unistd.h>
#include <ctime>

using std::pair;

int32_t id;

void delay(double sec)
{
    clock_t now = clock();
    while ((clock() - now) < sec * CLOCKS_PER_SEC);
}

int player_main(int n)
{
    double sec = (double) rand() / RAND_MAX / 10 * 2;
    delay(sec);
    return n + (id + 1) * 1000;
}


int main()
{
    pickle pick;
    std::pair<char *, int> msg;
    recv_send_socket *sock = create_socket();
    sock->connect_to_server("127.0.0.1", 5818);
    msg = sock->recv_data();
    pick.load(msg.first, msg.second);
    delete msg.first;
    if (pick.getType() != IdType)
    {
        printf("ERROR data type %d\n", pick.getType());
        exit(1);
    }
    id = pick.getId();
    printf("Id:%d\n", id);
    srand(time(NULL));
    while (true)
    {
        msg = sock->recv_data();
        pick.load(msg.first, msg.second);
        delete msg.first;
        if (pick.getType() == GameOverType)
            break;
        if (pick.getType() == IdType)
        {
            int result = pick.getId();
            printf("Num:%d\n", result);
            msg = pick.dumpId(player_main(result));
            sock->send_data(msg.first, msg.second);
            delete msg.first;
        } else
        {
            printf("Unknown data type");
        }
    }
}