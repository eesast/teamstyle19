def init_map_from_bitmap(self,path):
    from PIL import Image
    #_map_size = 200
    #_map = [[0 for i in range(_map_size)] for i in range(_map_size)]

    img = Image.open(path)
    _map = [[0] * _map_size for i in range(_map_size)]
    size = (_map_size, _map_size)
    img = img.resize(size, Image.ANTIALIAS)  # 放缩大小，直接用一个像素对应地图上的一个点

    # 以下二值化代码来自搜索引擎……包括去噪过程
    img = img.convert("RGBA")
    pixdata = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][0] < 90:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][1] < 136:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][2] > 0:
                pixdata[x, y] = (255, 255, 255, 255)

    # 将二值化后的图片读入_map
    for i in range(_map_size):
        for j in range(_map_size):
            if (pixdata[j, i] == (0, 0, 0, 255)):
                _map[i][j] = 1

    # 个人觉得路应该是比非路少的……所以如果1多就反一下，避免底色比道路颜色深的问题
    n = 0
    for i in range(_map_size):
        for j in range(_map_size):
            if _map[i][j] == 1:
                n += 1
    if n > _map_size * _map_size / 2:
        for i in range(_map_size):
            for j in range(_map_size):
                if _map[i][j] == 1:
                    _map[i][j] = 0
                else:
                    _map[i][j] = 1

    # 判断基地，个人想到的一种非常麻烦的判断方法是判断四个角的7*7，全1或者全0判为基地
    x = _map[0][0]
    flag = 0
    for i in range(7):  # 7*7中是不是全是1或0
        for j in range(7):
            if _map[i][j] == x:
                pass
            else:
                flag = 1
                break
    if flag:
        pass
    else:
        for i in range(8):  # 周围一圈有没有1，即路，有路则为基地
            if _map[i][7] == 1:
                flag = 1
                break
        for j in range(7):
            if _map[7][j] == 1:
                flag = 1
                break
    if flag:  # 如果判为基地
        for i in range(7):
            for j in range(7):
                _map[i][j] = 2

    x = _map[_map_size - 1][0]
    flag = 0
    for i in range(_map_size - 7, _map_size):
        for j in range(7):
            if _map[i][j] == x:
                pass
            else:
                flag = 1
                break
    if flag:
        pass
    else:
        for i in range(_map_size - 8, _map_size):
            if _map[i][7]:
                flag = 1
                break
        for j in range(7):
            if _map[_map_size - 8][j]:
                flag = 1
                break
    if flag:  # 如果判为基地
        for i in range(_map_size - 7, _map_size):
            for j in range(7):
                _map[i][j] = 2

    x = _map[0][_map_size - 1]
    flag = 0
    for i in range(7):
        for j in range(_map_size - 7, _map_size):
            if _map[i][j] == x:
                pass
            else:
                flag = 1
                break
    if flag:
        pass
    else:
        for i in range(8):
            if _map[i][7]:
                flag = 1
                break
        for j in range(_map_size - 7, _map_size):
            if _map[7][j]:
                flag = 1
                break
    if flag:  # 如果判为基地
        for i in range(7):
            for j in range(_map_size - 7, _map_size):
                _map[i][j] = 2

    x = _map[_map_size - 1][_map_size - 1]
    flag = 0
    for i in range(_map_size - 7, _map_size):
        for j in range(_map_size - 7, _map_size):
            if _map[i][j] == x:
                pass
            else:
                flag = 1
                break
    if flag:
        pass
    else:
        for i in range(_map_size - 7, _map_size):
            if _map[i][_map_size - 8]:
                flag = 1
                break
        for j in range(_map_size - 7, _map_size):
            if _map[_map_size - 8][j]:
                flag = 1
                break
    if flag:  # 如果判为基地
        for i in range(_map_size - 7, _map_size):
            for j in range(_map_size - 7, _map_size):
                _map[i][j] = 2