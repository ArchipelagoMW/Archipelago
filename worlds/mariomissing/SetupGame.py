import itertools

def setup_gamevars(world):
    world.city_order = [0x04, 0x0B, 0x08, 0x0C, 0x00, 0x01, 0x0E, 0x06, 0x0D, 0x05, 0x02, 0x0A, 0x07, 0x09, 0x03]
    world.city_list = []
    if world.options.city_shuffle != 0:
        world.random.shuffle(world.city_order)

    city_code = {
        0x00: "Rome",
        0x01: "Paris",
        0x02: "London",
        0x03: "New York",
        0x04: "San Francisco",
        0x05: "Athens",
        0x06: "Sydney",
        0x07: "Tokyo",
        0x08: "Nairobi",
        0x09: "Rio de Janeiro",
        0x0A: "Cairo",
        0x0B: "Moscow",
        0x0C: "Beijing",
        0x0D: "Buenos Aires",
        0x0E: "Mexico City",
    }
    world.city_list = [city_code[world.city_order[i]] for i in range(15)]
    world.city_order = list(itertools.chain.from_iterable((x, 0x00) for x in world.city_order))
