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


class InstrType(Enum):
    UpdateAge = 1
    Construct = 2
    Upgrade = 3
    Sell = 4
    Maintain = 5


def dump_id(id_num):
    """dump the info for the player id"""
    data = struct.pack("ii", MsgType.Id.value, id_num)
    return data


def dump_data(units, buildings, status, turn_num):
    """dump the data to send at every turn"""
    data = struct.pack("ii", MsgType.Data.value, turn_num)
    for flag in range(2):
        data += struct.pack("i", status[flag]['money'])
        data += struct.pack("i", status[flag]['tech'])
        data += struct.pack("i", status[flag]['building'])
    typed_list = ['produce', 'defense', 'resource']
    for flag in range(2):
        for type_name in typed_list:
            data += struct.pack("i", len(buildings[flag][type_name]))
            for building in buildings[flag][type_name]:
                data += struct.pack("iiiiii", building.Unit_ID, building.BuildingType, building.HP,
                                    building.Position.x, building.Position.y, building.Is_Maintain)
    for flag in range(2):
        for unit_id, unit in units[flag].items():
            data += struct.pack("iiiii", unit_id, unit.Solider_name, unit.HP, unit.Position.x, unit.Position.y,
                                )
    return data


def dump_map(map):
    """dump the map info"""
    # 数据顺序为基地位置数+基地位置+道路位置数+道路位置
    data = struct.pack("i", MsgType.Map.value)
    base_positions = []
    road_positions = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 2:
                base_positions.append((i, j))
            elif map[i][j] == 1:
                road_positions.append((i, j))
    data += struct.pack("i", len(base_positions))
    for x, y in base_positions:
        data += struct.pack("ii", x, y)
    data += struct.pack("i", len(road_positions))
    for x, y in road_positions:
        data += struct.pack("ii", x, y)
    return data


def undump_instr(instructions):
    pass


def wait_for(seconds: float):
    """wait for given seconds and stop"""
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


def Scheduler(tasks: list, timeout):
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
    def __init__(self, host_address: str, port: int):
        self.clients = []
        self.socket = socket.socket()
        self.socket.settimeout(0)
        self.socket.bind((host_address, port))

    def wait_for_connection(self):
        """wait for two clients to connect"""
        self.clients = Scheduler([Task(wait_for_connection(self.socket, 2))], timeout=None)[0]

    def send_to_players(self, data: bytes):
        """send the data to two clients"""
        Scheduler([Task(sendall(sock, data)) for sock in self.clients], wait_for(0.1))

    def recv_instructions(self):
        """receive the instructions from two clients, return in at most 1 second"""
        return Scheduler([Task(receive(sock)) for sock in self.clients], wait_for(0.1))

    def send_to_player(self, data: bytes, aim_id: int):
        """send the data to one client"""
        Scheduler([Task(sendall(self.clients[aim_id], data))], wait_for(0.1))

    def close(self):
        """close the server and disconnect"""
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
