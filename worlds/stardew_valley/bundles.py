from random import Random
from typing import List, Dict, Union

from .data.bundle_data import *
from .logic import StardewLogic
from .options import BundleRandomization, BundlePrice

vanilla_bundles = {
    "Pantry/0": "Spring Crops/O 465 20/24 1 0 188 1 0 190 1 0 192 1 0/0",
    "Pantry/1": "Summer Crops/O 621 1/256 1 0 260 1 0 258 1 0 254 1 0/3",
    "Pantry/2": "Fall Crops/BO 10 1/270 1 0 272 1 0 276 1 0 280 1 0/2",
    "Pantry/3": "Quality Crops/BO 15 1/24 5 2 254 5 2 276 5 2 270 5 2/6/3",
    "Pantry/4": "Animal/BO 16 1/186 1 0 182 1 0 174 1 0 438 1 0 440 1 0 442 1 0/4/5",
    # 639 1 0 640 1 0 641 1 0 642 1 0 643 1 0
    "Pantry/5": "Artisan/BO 12 1/432 1 0 428 1 0 426 1 0 424 1 0 340 1 0 344 1 0 613 1 0 634 1 0 635 1 0 636 1 0 637 1 0 638 1 0/1/6",
    "Crafts Room/13": "Spring Foraging/O 495 30/16 1 0 18 1 0 20 1 0 22 1 0/0",
    "Crafts Room/14": "Summer Foraging/O 496 30/396 1 0 398 1 0 402 1 0/3",
    "Crafts Room/15": "Fall Foraging/O 497 30/404 1 0 406 1 0 408 1 0 410 1 0/2",
    "Crafts Room/16": "Winter Foraging/O 498 30/412 1 0 414 1 0 416 1 0 418 1 0/6",
    "Crafts Room/17": "Construction/BO 114 1/388 99 0 388 99 0 390 99 0 709 10 0/4",
    "Crafts Room/19": "Exotic Foraging/O 235 5/88 1 0 90 1 0 78 1 0 420 1 0 422 1 0 724 1 0 725 1 0 726 1 0 257 1 0/1/5",
    "Fish Tank/6": "River Fish/O 685 30/145 1 0 143 1 0 706 1 0 699 1 0/6",
    "Fish Tank/7": "Lake Fish/O 687 1/136 1 0 142 1 0 700 1 0 698 1 0/0",
    "Fish Tank/8": "Ocean Fish/O 690 5/131 1 0 130 1 0 150 1 0 701 1 0/5",
    "Fish Tank/9": "Night Fishing/R 516 1/140 1 0 132 1 0 148 1 0/1",
    "Fish Tank/10": "Specialty Fish/O 242 5/128 1 0 156 1 0 164 1 0 734 1 0/4",
    "Fish Tank/11": "Crab Pot/O 710 3/715 1 0 716 1 0 717 1 0 718 1 0 719 1 0 720 1 0 721 1 0 722 1 0 723 1 0 372 1 0/1/5",
    "Boiler Room/20": "Blacksmith's/BO 13 1/334 1 0 335 1 0 336 1 0/2",
    "Boiler Room/21": "Geologist's/O 749 5/80 1 0 86 1 0 84 1 0 82 1 0/1",
    "Boiler Room/22": "Adventurer's/R 518 1/766 99 0 767 10 0 768 1 0 769 1 0/1/2",
    "Vault/23": "2,500g/O 220 3/-1 2500 2500/4",
    "Vault/24": "5,000g/O 369 30/-1 5000 5000/2",
    "Vault/25": "10,000g/BO 9 1/-1 10000 10000/3",
    "Vault/26": "25,000g/BO 21 1/-1 25000 25000/1",
    "Bulletin Board/31": "Chef's/O 221 3/724 1 0 259 1 0 430 1 0 376 1 0 228 1 0 194 1 0/4",
    "Bulletin Board/32": "Field Research/BO 20 1/422 1 0 392 1 0 702 1 0 536 1 0/5",
    "Bulletin Board/33": "Enchanter's/O 336 5/725 1 0 348 1 0 446 1 0 637 1 0/1",
    "Bulletin Board/34": "Dye/BO 25 1/420 1 0 397 1 0 421 1 0 444 1 0 62 1 0 266 1 0/6",
    "Bulletin Board/35": "Fodder/BO 104 1/262 10 0 178 10 0 613 3 0/3",
    # "Abandoned Joja Mart/36": "The Missing//348 1 1 807 1 0 74 1 0 454 5 2 795 1 2 445 1 0/1/5"
}


class Bundle:
    room: str
    sprite: str
    original_name: str
    name: str
    rewards: List[str]
    requirements: List[BundleItem]
    color: str
    number_required: int

    def __init__(self, key: str, value: str):
        key_parts = key.split("/")
        self.room = key_parts[0]
        self.sprite = key_parts[1]

        value_parts = value.split("/")
        self.original_name = value_parts[0]
        self.name = value_parts[0]
        self.rewards = self.parse_stardew_objects(value_parts[1])
        self.requirements = self.parse_stardew_bundle_items(value_parts[2])
        self.color = value_parts[3]
        if len(value_parts) > 4:
            self.number_required = int(value_parts[4])
        else:
            self.number_required = len(self.requirements)

    def __repr__(self):
        return f"{self.original_name} -> {repr(self.requirements)}"

    def get_name_with_bundle(self) -> str:
        return f"{self.original_name} Bundle"

    def to_pair(self) -> (str, str):
        key = f"{self.room}/{self.sprite}"
        str_rewards = ""
        for reward in self.rewards:
            str_rewards += f" {reward}"
        str_rewards = str_rewards.strip()
        str_requirements = ""
        for requirement in self.requirements:
            str_requirements += f" {requirement.item.item_id} {requirement.amount} {requirement.quality}"
        str_requirements = str_requirements.strip()
        value = f"{self.name}/{str_rewards}/{str_requirements}/{self.color}/{self.number_required}"
        return key, value

    def remove_rewards(self):
        self.rewards = []

    def change_number_required(self, difference: int):
        self.number_required = min(len(self.requirements), max(1, self.number_required + difference))
        if len(self.requirements) == 1 and self.requirements[0].item.item_id == -1:
            one_fifth = self.requirements[0].amount / 5
            new_amount = int(self.requirements[0].amount + (difference * one_fifth))
            self.requirements[0] = BundleItem.money_bundle(new_amount)
            thousand_amount = int(new_amount / 1000)
            dollar_amount = str(new_amount % 1000)
            while len(dollar_amount) < 3:
                dollar_amount = f"0{dollar_amount}"
            self.name = f"{thousand_amount},{dollar_amount}g"

    def randomize_requirements(self, random: Random,
                               potential_requirements: Union[List[BundleItem], List[List[BundleItem]]]):
        if not potential_requirements:
            return

        number_to_generate = len(self.requirements)
        self.requirements.clear()
        if number_to_generate > len(potential_requirements):
            choices: Union[BundleItem, List[BundleItem]] = random.choices(potential_requirements, k=number_to_generate)
        else:
            choices: Union[BundleItem, List[BundleItem]] = random.sample(potential_requirements, number_to_generate)
        for choice in choices:
            if isinstance(choice, BundleItem):
                self.requirements.append(choice)
            else:
                self.requirements.append(random.choice(choice))

    def assign_requirements(self, new_requirements: List[BundleItem]) -> List[BundleItem]:
        number_to_generate = len(self.requirements)
        self.requirements.clear()
        for requirement in new_requirements:
            self.requirements.append(requirement)
            if len(self.requirements) >= number_to_generate:
                return new_requirements[number_to_generate:]

    @staticmethod
    def parse_stardew_objects(string_objects: str) -> List[str]:
        objects = []
        if len(string_objects) < 5:
            return objects
        rewards_parts = string_objects.split(" ")
        for index in range(0, len(rewards_parts), 3):
            objects.append(f"{rewards_parts[index]} {rewards_parts[index + 1]} {rewards_parts[index + 2]}")
        return objects

    @staticmethod
    def parse_stardew_bundle_items(string_objects: str) -> List[BundleItem]:
        bundle_items = []
        parts = string_objects.split(" ")
        for index in range(0, len(parts), 3):
            item_id = int(parts[index])
            bundle_item = BundleItem(all_bundle_items_by_id[item_id].item,
                                     int(parts[index + 1]),
                                     int(parts[index + 2]))
            bundle_items.append(bundle_item)
        return bundle_items

    # Shuffling the Vault doesn't really work with the stardew system in place
    # shuffle_vault_amongst_themselves(random, bundles)


def get_all_bundles(random: Random, logic: StardewLogic, randomization: BundleRandomization, price: BundlePrice) -> Dict[str, Bundle]:
    bundles = {}
    for bundle_key in vanilla_bundles:
        bundle_value = vanilla_bundles[bundle_key]
        bundle = Bundle(bundle_key, bundle_value)
        bundles[bundle.get_name_with_bundle()] = bundle

    if randomization == BundleRandomization.option_thematic:
        shuffle_bundles_thematically(random, bundles)
    elif randomization == BundleRandomization.option_shuffled:
        shuffle_bundles_completely(random, logic, bundles)

    price_difference = 0
    if price == BundlePrice.option_very_cheap:
        price_difference = -2
    elif price == BundlePrice.option_cheap:
        price_difference = -1
    elif price == BundlePrice.option_expensive:
        price_difference = 1

    for bundle_key in bundles:
        bundles[bundle_key].remove_rewards()
        bundles[bundle_key].change_number_required(price_difference)

    return bundles


def shuffle_bundles_completely(random: Random, logic: StardewLogic, bundles: Dict[str, Bundle]):
    total_required_item_number = sum(len(bundle.requirements) for bundle in bundles.values())
    quality_crops_items_set = set(quality_crops_items)
    all_bundle_items_without_quality_and_money = [item
                                                  for item in all_bundle_items_except_money
                                                  if item not in quality_crops_items_set] + \
                                                 random.sample(quality_crops_items, 10)
    choices = random.sample(all_bundle_items_without_quality_and_money, total_required_item_number - 4)

    items_sorted = sorted(choices, key=lambda x: logic.item_rules[x.item.name].get_difficulty())

    keys = sorted(bundles.keys())
    random.shuffle(keys)

    for key in keys:
        if not bundles[key].original_name.endswith("00g"):
            items_sorted = bundles[key].assign_requirements(items_sorted)


def shuffle_bundles_thematically(random: Random, bundles: Dict[str, Bundle]):
    shuffle_crafts_room_bundle_thematically(random, bundles)
    shuffle_pantry_bundle_thematically(random, bundles)
    shuffle_fish_tank_thematically(random, bundles)
    shuffle_boiler_room_thematically(random, bundles)
    shuffle_bulletin_board_thematically(random, bundles)


def shuffle_crafts_room_bundle_thematically(random: Random, bundles: Dict[str, Bundle]):
    bundles["Spring Foraging Bundle"].randomize_requirements(random, spring_foraging_items)
    bundles["Summer Foraging Bundle"].randomize_requirements(random, summer_foraging_items)
    bundles["Fall Foraging Bundle"].randomize_requirements(random, fall_foraging_items)
    bundles["Winter Foraging Bundle"].randomize_requirements(random, winter_foraging_items)
    bundles["Exotic Foraging Bundle"].randomize_requirements(random, exotic_foraging_items)
    bundles["Construction Bundle"].randomize_requirements(random, construction_items)


def shuffle_pantry_bundle_thematically(random: Random, bundles: Dict[str, Bundle]):
    bundles["Spring Crops Bundle"].randomize_requirements(random, spring_crop_items)
    bundles["Summer Crops Bundle"].randomize_requirements(random, summer_crops_items)
    bundles["Fall Crops Bundle"].randomize_requirements(random, fall_crops_items)
    bundles["Quality Crops Bundle"].randomize_requirements(random, quality_crops_items)
    bundles["Animal Bundle"].randomize_requirements(random, animal_product_items)
    bundles["Artisan Bundle"].randomize_requirements(random, artisan_goods_items)


def shuffle_fish_tank_thematically(random: Random, bundles: Dict[str, Bundle]):
    bundles["River Fish Bundle"].randomize_requirements(random, river_fish_items)
    bundles["Lake Fish Bundle"].randomize_requirements(random, lake_fish_items)
    bundles["Ocean Fish Bundle"].randomize_requirements(random, ocean_fish_items)
    bundles["Night Fishing Bundle"].randomize_requirements(random, night_fish_items)
    bundles["Crab Pot Bundle"].randomize_requirements(random, crab_pot_items)
    bundles["Specialty Fish Bundle"].randomize_requirements(random, specialty_fish_items)


def shuffle_boiler_room_thematically(random: Random, bundles: Dict[str, Bundle]):
    bundles["Blacksmith's Bundle"].randomize_requirements(random, blacksmith_items)
    bundles["Geologist's Bundle"].randomize_requirements(random, geologist_items)
    bundles["Adventurer's Bundle"].randomize_requirements(random, adventurer_items)


def shuffle_bulletin_board_thematically(random: Random, bundles: Dict[str, Bundle]):
    bundles["Chef's Bundle"].randomize_requirements(random, chef_items)
    bundles["Dye Bundle"].randomize_requirements(random, dye_items)
    bundles["Field Research Bundle"].randomize_requirements(random, field_research_items)
    bundles["Fodder Bundle"].randomize_requirements(random, fodder_items)
    bundles["Enchanter's Bundle"].randomize_requirements(random, enchanter_items)


def shuffle_vault_amongst_themselves(random: Random, bundles: Dict[str, Bundle]):
    bundles["2,500g Bundle"].randomize_requirements(random, vault_bundle_items)
    bundles["5,000g Bundle"].randomize_requirements(random, vault_bundle_items)
    bundles["10,000g Bundle"].randomize_requirements(random, vault_bundle_items)
    bundles["25,000g Bundle"].randomize_requirements(random, vault_bundle_items)
