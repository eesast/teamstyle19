import socket
import threading
import queue
import struct
import time
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


class IOHandler(threading.Thread):
    def __init__(self, sock: socket.socket, q: queue.Queue):
        threading.Thread.__init__(self)
        self.socket = sock
        self.socket.settimeout(0)
        self.info_queue = q
        self.wait_for_recv = False
        self.game_going = True
        self.instructions = bytes()
        self.pending_size = 0
        self.mutex = threading.Lock()

    def readable(self):
        return self.wait_for_recv

    def writable(self):
        return not self.info_queue.empty()

    def run(self):
        while self.game_going:
            if self.writable():
                data = self.info_queue.get(block=False)
                data = struct.pack("i", len(data)) + data
                try:
                    while data:
                        send_len = self.socket.send(data)
                        data = data[send_len:]
                except ConnectionResetError:
                    pass

            if self.readable():
                try:
                    instructions = self.socket.recv(4096)
                    if instructions:
                        if not self.pending_size and len(instructions) >= 4:
                            self.pending_size = struct.unpack("i", instructions[:4])[0]
                            instructions = instructions[4:]
                        self.pending_size -= len(instructions)
                        self.mutex.acquire()
                        self.instructions += instructions
                        self.mutex.release()
                        if self.pending_size <= 0:
                            self.wait_for_recv = False
                            self.pending_size = 0
                except ConnectionResetError:
                    self.pending_size = 0
                    self.wait_for_recv = False
                except BlockingIOError:
                    pass

    def dump(self):
        instructions = self.instructions
        self.instructions = bytes()
        return instructions


class MainServer:
    def __init__(self, host_address, port):
        self.threads = []
        self.info_queues = []
        self.socket = socket.socket()
        self.socket.bind((host_address, port))
        self.socket.listen(2)
        self.instructions = []

    def wait_for_connection(self):
        for i in range(2):
            conn, _ = self.socket.accept()
            self.info_queues.append(queue.Queue())
            self.threads.append(IOHandler(conn, self.info_queues[i]))
            self.threads[i].start()
            print("Client {0} connected".format(i))
            self.threads[i].info_queue.put(dump_id(i))
        while not (self.info_queues[0].empty() or self.info_queues[1].empty()):
            pass

    def send_to_players(self, data):
        for q in self.info_queues:
            q.put(data)
        while not (self.info_queues[0].empty() or self.info_queues[1].empty()):
            pass

    def send_to_player(self, data, aim_id):
        self.info_queues[aim_id].put(data)
        while not (self.info_queues[aim_id].empty()):
            pass

    def recv_instructions(self):
        for handler in self.threads:
            handler.wait_for_recv = True
        time.sleep(0.1)
        instructions = []
        for handler in self.threads:
            handler.mutex.acquire()
            handler.wait_for_recv = False
            instructions.append(handler.dump())
            handler.mutex.release()
        return instructions

    def close(self):
        for thread in self.threads:
            thread.game_going = False
        for thread in self.threads:
            thread.join()


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
