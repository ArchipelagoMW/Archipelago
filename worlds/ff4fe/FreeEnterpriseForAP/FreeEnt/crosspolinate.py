def crosspolinate(list1, list2, ratio1, ratio2, rnd):
    low_pool = list(list1)
    high_pool = list(list2)

    rnd.shuffle(low_pool)
    rnd.shuffle(high_pool)

    low_cross_count = int(len(low_pool) * ratio1)
    high_cross_count = int(len(high_pool) * ratio2)

    cross_pool = low_pool[:low_cross_count]
    low_pool = low_pool[low_cross_count:]

    cross_pool.extend(high_pool[:high_cross_count])
    high_pool = high_pool[high_cross_count:]

    rnd.shuffle(cross_pool)

    low_pool.extend(cross_pool[:low_cross_count])
    high_pool.extend(cross_pool[low_cross_count:])

    return (low_pool, high_pool)
