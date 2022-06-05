import typing

from Options import Toggle, DefaultOnToggle, Option

item_pool_options = {
    "RandomizeEquipment": ["", True],
    "RandomizeConsumables": ["", True],
    "RandomizeFlaskContainersAndShards": ["", True],
    "RandomizeOfferings": ["", True],
    "RandomizeMoney": ["", True],
    "RandomizeEquipmentSlots": ["", True],
    "RandomizeHexagons": ["", False],
    "RandomizeFairies": ["", False],
    "RandomizeTrophies": ["", False],
}

additional_options = {
    "EnsureEquipmentInEquipmentLocation": ["Equipment such as Sword, Lantern etc. are randomized between each other",
                                           True],
    "ProgressiveStickToSword": ["Swords are swapped out with a stick if you don't have one."
                                "Sticks are swapped out with swords if you already have a stick.", True],
    "BushesOnlyDestructibleBySword": ["You need a sword to cut down bushes", True],
}


class TunicOptions:

    @staticmethod
    def generate_tunic_options():
        _tunic_options = {}
        for item_pool_option in item_pool_options.keys():
            if item_pool_options[item_pool_option][1]:
                _tunic_options[item_pool_option] = DefaultOnToggle
            else:
                _tunic_options[item_pool_option] = Toggle

        for additional_option in additional_options.keys():
            if additional_options[additional_option][1]:
                _tunic_options[additional_option] = DefaultOnToggle
            else:
                _tunic_options[additional_option] = Toggle
        return _tunic_options
