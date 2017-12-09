#include <stdio.h>
#include <stdlib.h>
#include <thread>
#include "communicate.h"
#include "api_player.h"
#include <unistd.h>
#include <ctime>

using std::pair;
using std::mutex;

int32_t id;

pair<char *, int> data_buffer;
bool receiving;
mutex data_mutex;


void delay(double sec)
{
    clock_t now = clock();
    while ((clock() - now) < sec * CLOCKS_PER_SEC);
}

int player_main(int n)
{
    toggleMaintain(n);
    for (int i = 0; i < 10; ++i)
    {
        switch (rand() % 5)
        {
            case 0:
                sell(rand());
                break;
            case 1:
                construct(Shannon, Position(rand(), rand()), Position(rand(), rand()));
                break;
            case 2:
                toggleMaintain(rand());
                break;
            case 3:
                upgrade(rand());
                break;
            case 4:
                updateAge();
                break;
        }
    }
    double sec = (double) rand() / RAND_MAX / 10 * 5;
    delay(sec);
    return n + (id + 1) * 1000;
}


int main()
{
    Pickle pick;
    std::pair<char *, int> msg;
    RecvSendSocket *sock = create_socket();
    sock->connect_to_server("127.0.0.1", 5838);
    msg = sock->recv_data(true);
    pick.load(msg.first, msg.second);
    delete msg.first;
    if (pick.getType() != IdMsg)
    {
        printf("ERROR data type %d\n", pick.getType());
        exit(1);
    }
    id = pick.getId();
    printf("Id:%d\n", id);
    srand(time(NULL));
    data_buffer.first = NULL;
    receiving = true;
    std::thread recv_thread(&static_recv_data, sock);
    while (true)
    {
        while (!data_buffer.first);
        data_mutex.lock();
        pick.load(data_buffer.first, data_buffer.second);
        delete data_buffer.first;
        data_buffer.first = NULL;
        data_mutex.unlock();
        if (pick.getType() == GameOverMsg)
            break;
        if (pick.getType() == IdMsg)
        {
            int result = pick.getId();
            printf("Num:%d\n", result);
            player_main(result);
            msg = pick.dumpInstr();
            sock->send_data(msg.first, msg.second);
            delete[] msg.first;
        } else
        { ;
            printf("Unknown data type");
        }
    }
    receiving = false;
    recv_thread.join();
    return 0;
}