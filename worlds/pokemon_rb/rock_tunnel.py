from .rom_addresses import rom_addresses

disallowed1F = [[2, 2], [3, 2], [1, 8], [2, 8], [7, 7], [8, 7], [10, 4], [11, 4], [11, 12],
              [11, 13], [16, 10], [17, 10], [18, 10], [16, 12], [17, 12], [18, 12]]
disallowed2F = [[16, 2], [17, 2], [18, 2], [15, 5], [15, 6], [10, 10], [11, 10], [12, 10], [7, 14], [8, 14], [1, 15],
                [13, 15], [13, 16], [1, 12], [1, 10], [3, 5], [3, 6], [5, 6], [5, 7], [5, 8], [1, 2], [1, 3], [1, 4],
                [11, 1]]


def randomize_rock_tunnel(data, random):

    seed = random.randint(0, 999999999999999999)
    random.seed(seed)

    map1f = []
    map2f = []

    address = rom_addresses["Map_Rock_Tunnel1F"]
    for y in range(0, 18):
        row = []
        for x in range(0, 20):
            row.append(data[address])
            address += 1
        map1f.append(row)

    address = rom_addresses["Map_Rock_TunnelB1F"]
    for y in range(0, 18):
        row = []
        for x in range(0, 20):
            row.append(data[address])
            address += 1
        map2f.append(row)

    current_map = map1f

    def floor(x, y):
        current_map[y][x] = 1

    def wide(x, y):
        current_map[y][x] = 32
        current_map[y][x + 1] = 34

    def tall(x, y):
        current_map[y][x] = 23
        current_map[y + 1][x] = 31

    def single(x, y):
        current_map[y][x] = 2

    # 0 = top left, 1 = middle, 2 = top right, 3 = bottom right
    entrance_c = random.choice([0, 1, 2])
    exit_c = [0, 1, 3]
    if entrance_c == 2:
        exit_c.remove(1)
    else:
        exit_c.remove(entrance_c)
    exit_c = random.choice(exit_c)
    remaining = [i for i in [0, 1, 2, 3] if i not in [entrance_c, exit_c]]

    if entrance_c == 0:
        floor(6, 3)
        floor(6, 4)
        tall(random.randint(8, 10), 2)
        wide(4, random.randint(5, 7))
        wide(1, random.choice([5, 6, 7, 9]))
    elif entrance_c == 1:
        if remaining == [0, 2] or random.randint(0, 1):
            tall(random.randint(8, 10), 2)
            floor(7, 4)
            floor(8, 4)
        else:
            tall(random.randint(11, 12), 5)
            floor(9, 5)
            floor(9, 6)
    elif entrance_c == 2:
        floor(16, 2)
        floor(16, 3)
        if remaining == [1, 3]:
            wide(17, 4)
        else:
            tall(random.randint(11, 17), random.choice([2, 5]))

    if exit_c == 0:
        r = random.sample([0, 1, 2], 2)
        if 0 in r:
            floor(1, 11)
            floor(2, 11)
        if 1 in r:
            floor(3, 11)
            floor(4, 11)
        if 2 in r:
            floor(5, 11)
            floor(6, 11)
    elif exit_c == 1 or (exit_c == 3 and entrance_c == 0):
        r = random.sample([1, 3, 5, 7], random.randint(1, 2))
        for i in r:
            floor(i, 11)
            floor(i + 1, 11)
    if exit_c != 3:
        tall(random.choice([9, 10, 12]), 12)

    # 0 = top left, 1 = middle, 2 = top right, 3 = bottom right
    # [0, 1] [0, 2] [1, 2] [1, 3], [2, 3]
    if remaining[0] == 1:
        floor(9, 5)
        floor(9, 6)

    if remaining == [0, 2]:
        if random.randint(0, 1):
            tall(9, 4)
            floor(9, 6)
            floor(9, 7)
        else:
            floor(10, 7)
            floor(11, 7)

    if remaining == [1, 2]:
        floor(16, 2)
        floor(16, 3)
        tall(random.randint(11, 17), random.choice([2, 5]))
    if remaining in [[1, 3], [2, 3]]:
        r = round(random.triangular(0, 3, 0))
        floor(12 + (r * 2), 7)
        if r < 3:
            floor(13 + (r * 2), 7)
    if remaining == [1, 3]:
        wide(10, random.choice([3, 5]))

    if remaining != [0, 1] and exit_c != 1:
        wide(7, 6)

    if entrance_c != 0:
        if random.randint(0, 1):
            wide(4, random.randint(4, 7))
        else:
            wide(1, random.choice([5, 6, 7, 9]))

    current_map = map2f

    if 3 in remaining:
        c = random.choice([entrance_c, exit_c])
    else:
        c = random.choice(remaining)

    # 0 = top right, 1 = middle, 2 = bottom right, 3 = top left
    if c in [0, 1]:
        if random.randint(0, 2):
            tall(random.choice([2, 4]), 5)
            r = random.choice([1, 3, 7, 9, 11])
            floor(3 if r < 11 else random.randint(1, 2), r)
            floor(3 if r < 11 else random.randint(1, 2), r + 1)
        if random.randint(0, 2):
            tall(random.randint(6, 7), 7)
            r = random.choice([1, 3, 5, 9])
            floor(6, r)
            floor(6, r + 1)
        if random.randint(0, 2):
            wide(7, 15)
            r = random.randint(0, 4)
            if r == 0:
                floor(9, 14)
                floor(10, 14)
            elif r == 1:
                floor(11, 14)
                floor(12, 14)
            elif r == 2:
                floor(13, 13)
                floor(13, 14)
            elif r == 3:
                floor(13, 11)
                floor(13, 12)
            elif r == 4:
                floor(13, 10)
                floor(14, 10)
    if c == 0:
        tall(random.randint(9, 10), 5)
        if random.randint(0, 1):
            floor(10, 7)
            floor(11, 7)
            if current_map[10][13]==1:
                # (13,10) is floor
                tall(random.randint(14, 16), 8)
            else:
                tall(random.randint(12, 16), 8)
        else:
            floor(12, 5)
            floor(12, 6)
            wide(13, random.randint(4, 5))
            wide(17, random.randint(3, 5))
        r = random.choice([1, 3])
        floor(12, r)
        floor(12, r + 1)
        if current_map[4][12] + current_map[5][12] == 2:
            # (12,4) and (12,5) are floor
            wide(11,4)
    elif c == 2:
        r = random.randint(0, 6)
        if r == 0:
            floor(12, 1)
            floor(12, 2)
        elif r == 1:
            floor(12, 3)
            floor(12, 4)
        elif r == 2:
            floor(12, 5)
            floor(12, 6)
        elif r == 3:
            floor(10, 7)
            floor(11, 7)
        elif r == 4:
            floor(9, 7)
            floor(9, 8)
        elif r == 5:
            floor(9, 9)
            floor(9, 10)
        elif r == 6:
            floor(8, 11)
            floor(9, 11)
        if r < 2 or (r in [2, 3] and random.randint(0, 1)):
            wide(7, random.randint(6, 7))
        elif r in [2, 3]:
            tall(random.randint(9, 10), 5)
        else:
            tall(random.randint(6, 7), 7)
        r = random.randint(r, 6)
        if r == 0:
            #early block
            wide(13, random.randint(2, 5))
            tall(random.randint(14, 15), 1)
            if not 1 in (current_map[1][14],current_map[2][13]):
                # wide(13,2) and tall(14,1) overlap
                single(13,2)
        elif r == 1:
            if random.randint(0, 1):
                tall(16, 5)
                tall(random.choice([14, 15, 17]), 1)
            else:
                wide(16, random.randint(6,8))
                single(18, 7)
        elif r == 2:
            tall(random.randint(12, 16), 8)
        elif r == 3:
            wide(10, 9)
            single(12, 9)
        elif r == 4:
            wide(10, random.randint(11, 12))
            single(12, random.randint(11, 12))
        elif r == 5:
            tall(random.randint(8, 10), 12)
        elif r == 6:
            wide(7, 15)
        r = random.randint(r, 6)
        if r == 6:
            #late open
            if random.randint(0, 1):
                floor(1, 14)
                floor(2, 14)
            else:
                floor(3, 14)
                floor(4, 14)
        elif r == 5:
            if random.randint(0,1):
                floor(6, 12)
                floor(6, 13)
            else:
                floor(5, 14)
                floor(6, 14)
        elif r == 4:
            if random.randint(0, 1):
                floor(6, 11)
                floor(7, 11)
            else:
                floor(8, 11)
                if current_map[12][10]==32:
                    # (10,12) is wide
                    single(9, 11)
                else:
                    floor(9, 11)
            if 31 in (current_map[8][6],current_map[8][7]):
                # (6,7) or (7,7) are tall
                floor(6, 10)
                wide(7, 9)
        elif r == 3:
            floor(9, 9)
            floor(9, 10)
        elif r < 3:
            single(9, 7)
            floor(9, 8)

    def check_addable_block(check_map, disallowed):
        if check_map[y][x] == 1 and [x, y] not in disallowed:
            i = 0
            for xx in range(x-1, x+2):
                for yy in range(y-1, y+2):
                    if check_map[yy][xx] == 1:
                        i += 1
            if i >= 8:
                single(x, y)

    for _ in range(100):
        y = random.randint(1, 16)
        x = random.randint(1, 18)
        current_map = map1f
        check_addable_block(map1f, disallowed1F)
        current_map = map2f
        check_addable_block(map2f, disallowed2F)

    address = rom_addresses["Map_Rock_Tunnel1F"]
    for y in map1f:
        for x in y:
            data[address] = x
            address += 1
    address = rom_addresses["Map_Rock_TunnelB1F"]
    for y in map2f:
        for x in y:
            data[address] = x
            address += 1
    return seed