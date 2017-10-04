#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "communicate.h"


class unix_socket : public recv_send_socket {
public:
    unix_socket();

    void send_data(const char *msg, int len);

    std::pair<char *, int> recv_data();

    void connect_to_server(const char *ip_address, unsigned short port);

private:
    int sockfd;
};

unix_socket::unix_socket()
{
    sockfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sockfd < 0)
    {
        perror("ERROR opening socket\n");
        exit(1);
    }
}

void unix_socket::connect_to_server(const char *ip_address, unsigned short port)
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
}

void unix_socket::send_data(const char *msg, int32_t len)
{
    char *data = new char[len + sizeof(int32_t)];
    memcpy(data, &len, sizeof(int32_t));
    memcpy(data + sizeof(int32_t), msg, len);
    len += sizeof(int32_t);
    while (len > 0)
    {
        len -= send(sockfd, data, len, 0);
    }
    delete[]data;
}

std::pair<char *, int> unix_socket::recv_data()
{
    int32_t len, received = 0;
    while ((received += recv(sockfd, reinterpret_cast<char *>(&len) + received, sizeof(int32_t) - received, 0)) !=
           sizeof(int32_t));
    char *buf = new char[len];
    received = 0;
    while ((received += recv(sockfd, buf + received, len - received, 0)) != len);
    return std::pair<char *, int>(buf, len);
}


recv_send_socket *create_socket()
{
    return new unix_socket;
}

