all_flowers = []


def flower(flower_name: str) -> str:
    all_flowers.append(flower_name)
    return flower_name


class Flower:
    blue_jazz = flower("Blue Jazz")
    fairy_rose = flower("Fairy Rose")
    poppy = flower("Poppy")
    summer_spangle = flower("Summer Spangle")
    sunflower = flower("Sunflower")
    tulip = flower("Tulip")
