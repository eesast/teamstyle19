import socket
import threading
import queue
import struct
import time


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
        while (self.game_going):
            if self.writable():
                data = self.info_queue.get(block=False)
                try:
                    while data:
                        send_len = self.socket.send(data)
                        data = data[send_len:]
                except ConnectionResetError:
                    pass

            if self.readable():
                try:
                    instructions = self.socket.recv(4096)
                except ConnectionResetError:
                    self.pending_size = 0
                    self.wait_for_read = False
                except BlockingIOError:
                    continue
                if instructions:
                    if not self.pending_size:
                        self.pending_size = struct.unpack("i", instructions[:4])[0]
                        instructions = instructions[4:]
                    self.pending_size -= len(instructions)
                    self.mutex.acquire()
                    self.instructions += instructions
                    self.mutex.release()
                    if self.pending_size <= 0:
                        self.wait_for_read = False
                        self.pending_size = 0

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
            print("Client {0} connected".format(i + 1))
            ai_id = struct.pack("i", i)
            self.threads[i].info_queue.put(ai_id)
        while not (self.info_queues[0].empty() or self.info_queues[1].empty()):
            pass

    def send_to_player(self, data):
        for q in self.info_queues:
            q.put(data)
        while not (self.info_queues[0].empty() or self.info_queues[1].empty()):
            time.sleep(0.1)

    def recv_instructions(self):
        for handler in self.threads:
            handler.wait_for_recv = True
        time.sleep(5)
        instructions = []
        for handler in self.threads:
            handler.mutex.acquire()
            handler.wait_for_recv = False
            instructions.append(handler.dump())
            handler.mutex.release()
        return instructions


def main():
    server = MainServer("127.0.0.1", 5708)
    server.wait_for_connection()
    while True:
        texts = server.recv_instructions()
        print(texts[0])
        print(texts[1])
        server.send_to_player("Received".encode("utf-8"))


if __name__ == "__main__":
    main()
