import time
import socket
import struct
import queue
from enum import Enum

class MsgType(Enum):
    Id = 1
    Map = 2
    Data = 3
    Instr = 4
    GameOver = 5


def dump_id(id_num):
    data = struct.pack("ii", MsgType.Id.value, id_num)
    return data


def wait_for(seconds: float):
    start_time = time.clock()
    while ((time.clock() - start_time) < seconds):
        yield


def sendall(socket: socket.socket, data):
    data = struct.pack("i", len(data)) + data
    while data:
        yield
        try:
            send_len = socket.send(data)
            data = data[send_len:]
        except BlockingIOError:
            pass
        except ConnectionResetError:
            break


def receive(socket: socket.socket):
    pending_size = None
    total_data = b''
    while True:
        yield
        try:
            data = socket.recv(4096)
            if data:
                if pending_size is None and len(data) >= 4:
                    pending_size = struct.unpack("i", data[:4])[0]
                    data = data[4:]
                pending_size -= len(data)
                total_data += data
                if pending_size <= 0:
                    break
        except BlockingIOError:
            pass
        except ConnectionResetError:
            break
    return total_data


def wait_for_connection(socket: socket.socket, connect_num: int):
    socket.listen(connect_num)
    clients = []
    for i in range(connect_num):
        while True:
            try:
                conn, _ = socket.accept()
                clients.append(conn)
                yield Task(sendall(conn, dump_id(i)))
                break
            except BlockingIOError:
                yield
    return clients


class Task:
    def __init__(self, target):
        self.target = target
        self.data = b''

    def run(self):
        try:
            return self.target.send(None)
        except StopIteration as e:
            self.data = e.value
            raise e

    def close(self):
        self.target.close()


def Scheduler(tasks, timeout):
    ready = queue.Queue()
    for task in tasks:
        ready.put(task)
    while not ready.empty():
        try:
            if not timeout is None:
                timeout.send(None)
        except StopIteration:
            break
        task = ready.get(block=False)
        try:
            result = task.run()
            if not result is None:
                ready.put(result)
            ready.put(task)
        except StopIteration:
            pass
    for task in tasks:
        task.close()
    if not timeout is None:
        timeout.close()
    instructions = [task.data for task in tasks]
    return instructions




class MainServer:
    def __init__(self, host_address, port):
        self.clients = []
        self.socket = socket.socket()
        self.socket.settimeout(0)
        self.socket.bind((host_address, port))

    def wait_for_connection(self):
        self.clients = Scheduler([Task(wait_for_connection(self.socket, 2))], timeout=None)[0]

    def send_to_players(self, data):
        Scheduler([Task(sendall(sock, data)) for sock in self.clients], wait_for(0.1))

    def recv_instructions(self):
        return Scheduler([Task(receive(sock)) for sock in self.clients], wait_for(0.1))

    def send_to_player(self, data, aim_id):
        Scheduler([Task(sendall(self.clients[aim_id], data))], wait_for(0.1))

    def close(self):
        for sock in self.clients:
            sock.close()
        self.socket.close()

def main():
    server = MainServer("127.0.0.1", 5818)
    server.wait_for_connection()
    player1, player2 = True, True
    for i in range(100):
        print("Round", i)
        msg = struct.pack("ii", MsgType.Id.value, i)
        if player1 and player2:
            server.send_to_players(msg)
        elif player1:
            server.send_to_player(msg, 0)
        elif player2:
            server.send_to_player(msg, 1)
        data = server.recv_instructions()
        player1, player2 = False, False
        if data[0]:
            playerNum1 = struct.unpack("i", data[0][4:])[0]
            print("Player 1:", playerNum1, end=' ')
            player1 = True
        else:
            print("Player 1 miss", end=' ')
        if data[1]:
            playerNum2 = struct.unpack("i", data[1][4:])[0]
            print("Player 2:", playerNum2)
            player2 = True
        else:
            print("Player 2 miss")
    server.send_to_players(struct.pack("i", MsgType.GameOver.value))
    server.close()

if __name__ == "__main__":
    main()