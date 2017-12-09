#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <thread>
#include "communicate.h"

using std::mutex;
using std::pair;

extern mutex data_mutex;
extern bool receiving;
extern pair<char *, int> data_buffer;


class UnixSocket : public RecvSendSocket {
public:
    UnixSocket();

    void send_data(const char *msg, int len);

    std::pair<char *, int> recv_data(bool blocked);

    void connect_to_server(const char *ip_address, unsigned short port);

private:
    int sockfd;
};

UnixSocket::UnixSocket()
{
    sockfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sockfd < 0)
    {
        perror("ERROR opening socket\n");
        exit(1);
    }
}

void UnixSocket::connect_to_server(const char *ip_address, unsigned short port)
{
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));

    server_addr.sin_family = AF_INET;

    if (!static_cast<bool>(inet_aton(ip_address, &server_addr.sin_addr)))
    {
        perror("ERROR address\n");
        exit(1);
    }
    server_addr.sin_port = htons(port);

    if (connect(sockfd, reinterpret_cast<struct sockaddr *>(&server_addr), sizeof(server_addr)) < 0)
    {
        perror("ERROR connecting\n");
        exit(1);
    }
    fcntl(sockfd, F_SETFL, O_NONBLOCK);
}

void UnixSocket::send_data(const char *msg, int32_t len)
{
    char *data = new char[len + sizeof(int32_t)];
    memcpy(data, &len, sizeof(int32_t));
    memcpy(data + sizeof(int32_t), msg, len);
    len += sizeof(int32_t);
    while (len > 0)
    {
        len -= send(sockfd, data, len, 0);
    }
    delete[] data;
}

std::pair<char *, int> UnixSocket::recv_data(bool blocked)
{
    int32_t len, received = 0, temp = recv(sockfd, reinterpret_cast<char *>(&len), sizeof(int32_t), 0);
    if (temp <= 0 && !blocked)
        return pair<char *, int>(NULL, 0);
    if (temp > 0)
        received += temp;
    while (received != sizeof(int32_t))
    {
        temp = recv(sockfd, reinterpret_cast<char *>(&len) + received, sizeof(int32_t) - received, 0);
        if (temp > -1)
            received += temp;
    }
    char *buf = new char[len];
    received = 0;
    while (received != len)
    {
        temp = recv(sockfd, buf + received, len - received, 0);
        if (temp > -1)
            received += temp;
    }
    return std::pair<char *, int>(buf, len);
}


RecvSendSocket *create_socket()
{
    return new UnixSocket;
}

void static_recv_data(RecvSendSocket *socket)
{
    pair<char *, int> local_buffer(NULL, 0);
    while (receiving)
    {
        pair<char *, int> temp = socket->recv_data(false);
        if (temp.second > 0)
        {
            local_buffer = temp;
        }
        if (local_buffer.second > 0 && data_mutex.try_lock())
        {
            data_buffer = local_buffer;
            data_mutex.unlock();
            local_buffer.second = 0;
        }
    }
}
