def init_map_random(self):
    import random
    #_map_size = 200
    #_map = [[0 for i in range(_map_size)] for i in range(_map_size)]

    # 生成基地，位置定在0,0和199,199处
    for i in range(7):
        for j in range(7):
            _map[i][j] = 2
    for i in range(_map_size - 7, _map_size):
        for j in range(_map_size - 7, _map_size):
            _map[i][j] = 2

    # 生成中路
    i = 7
    j = 7
    _map[i][j] = 1
    while (1):
        if i < _map_size / 2 - 1 and j < _map_size / 2 - 1:
            if random.randint(0, 1) == 0:
                i += 1
            else:
                j += 1
        elif i == _map_size / 2 - 1 and j < _map_size / 2 - 1:
            j += 1
        elif i < _map_size / 2 - 1 and j == _map_size / 2 - 1:
            i += 1
        else:
            break
        _map[i][j] = 1
    for i in range(_map_size):
        for j in range(_map_size):
            if _map[_map_size - i - 1][_map_size - j - 1] == 1:
                _map[i][j] = 1

    # 生成下路
    n = random.randint(1, 3)  # 随机生成3,5或7条路
    for a in range(n):
        i = 7
        x = 5  # 起点从5,3,1顺序选择
        while _map[i][x] == 1 and x >= 1:
            x -= 2
        if x <= 0:
            break
        j = x
        _map[i][j] = 3  # 用3标志暂定路线，最后处理
        while 1:
            if i + j < 200:  # 上下两部分和不同的道路使用两种不同的概率，使道路相对更分散
                if i < _map_size - x - 1 and j < _map_size - 8:
                    if random.uniform(0, 1) >= x / 12:
                        i += 1
                        if _map[i][j - 1] != 1 and _map[i][j + 1] != 1 and _map[i + 1][j] != 1:  # 检查即将延伸的方向有没有其它路，避免交叉
                            pass
                        else:
                            i -= 1
                            j += 1
                            if _map[i - 1][j] != 1 and _map[i + 1][j] != 1 and _map[i][j + 1] != 1:
                                pass
                            else:
                                break
                    else:
                        j += 1
                        if _map[i - 1][j] != 1 and _map[i + 1][j] != 1 and _map[i][j + 1] != 1:
                            pass
                        else:
                            j -= 1
                            i += 1
                            if _map[i][j - 1] != 1 and _map[i][j + 1] != 1 and _map[i + 1][j] != 1:
                                pass
                            else:
                                break
                _map[i][j] = 3
            else:
                if i < _map_size - x - 1 and j < _map_size - 8:
                    if random.uniform(0, 1) < x / 12:
                        i += 1
                        if _map[i][j - 1] != 1 and _map[i][j + 1] != 1 and _map[i + 1][j] != 1:  # 检查即将延伸的方向有没有其它路，避免交叉
                            pass
                        else:
                            i -= 1
                            j += 1
                            if _map[i - 1][j] != 1 and _map[i + 1][j] != 1 and _map[i][j + 1] != 1:
                                pass
                            else:
                                break
                    else:
                        j += 1
                        if _map[i - 1][j] != 1 and _map[i + 1][j] != 1 and _map[i][j + 1] != 1:
                            pass
                        else:
                            j -= 1
                            i += 1
                            if _map[i][j - 1] != 1 and _map[i][j + 1] != 1 and _map[i + 1][j] != 1:
                                pass
                            else:
                                break
                elif i == _map_size - x - 1 and j < _map_size - 8:
                    j += 1
                    if _map[i - 1][j + 1] != 1 and _map[i][j + 1] != 1:
                        pass
                    else:
                        break
                elif i < _map_size - x - 1 and j == _map_size - 8:
                    i += 1
                    if _map[i - 1][j + 1] != 1 and _map[i][j + 1] != 1:
                        pass
                    else:
                        break
                else:
                    break
                _map[i][j] = 3
        if _map_size - 8 <= i < _map_size - 1 and j == _map_size - 8:  # 路最后延伸至另一个基地
            for i in range(_map_size):
                for j in range(_map_size):
                    if _map[i][j] == 3:
                        _map[i][j] = 1
        else:
            for i in range(_map_size):
                for j in range(_map_size):
                    if _map[i][j] == 3:
                        _map[i][j] = 0

    # 利用中心对称生成上路
    for i in range(_map_size):
        for j in range(_map_size):
            if _map[_map_size - i - 1][_map_size - j - 1] == 1:
                _map[i][j] = 1
