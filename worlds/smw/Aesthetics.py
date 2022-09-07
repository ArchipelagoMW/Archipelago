
level_music_address_data = [
    0x284DB,
    0x284DC,
    0x284DD,
    0x284DE,
    0x284DF,
    0x284E0,
    0x284E1,
    0x284E2,
]

level_music_value_data = [
    0x02,
    0x06,
    0x01,
    0x08,
    0x07,
    0x03,
    0x05,
    0x12,
]

ow_music_address_data = [
    [0x25BC8, 0x20D8A],
    [0x25BC9, 0x20D8B],
    [0x25BCA, 0x20D8C],
    [0x25BCB, 0x20D8D],
    [0x25BCC, 0x20D8E],
    [0x25BCD, 0x20D8F],
    [0x25BCE, 0x20D90],
    [0x16C7]
]

ow_music_value_data = [
    0x02,
    0x03,
    0x04,
    0x06,
    0x07,
    0x09,
    0x05,
    0x01,
]


def generate_shuffled_level_music(world, player):
    shuffled_level_music = level_music_value_data.copy()

    if world.music_shuffle[player] == "simple_unique":
        world.random.shuffle(shuffled_level_music)
    elif world.music_shuffle[player] == "singularity":
        single_song = world.random.choice(shuffled_level_music)
        shuffled_level_music = [single_song for i in range(len(shuffled_level_music))]

    return shuffled_level_music

def generate_shuffled_ow_music(world, player):
    shuffled_ow_music = ow_music_value_data.copy()

    if world.music_shuffle[player] == "simple_unique":
        world.random.shuffle(shuffled_ow_music)
    elif world.music_shuffle[player] == "singularity":
        single_song = world.random.choice(shuffled_ow_music)
        shuffled_ow_music = [single_song for i in range(len(shuffled_ow_music))]

    return shuffled_ow_music
