import logging
import re
import string
from logging import Logger
from typing import Optional, List, Set, Any

from BaseClasses import Item, ItemClassification, Location, MultiWorld, Region, Tutorial
from Options import OptionError
from .Characters import character_list, CharacterConfig, character_offset_map, NUM_CUSTOM
from .Items import event_item_pairs, item_table, ItemType, chars_to_items, base_event_item_pairs, item_groups
from .Locations import location_table, loc_ids_to_data, LocationData, LocationType, CARD_REWARD_COUNT, location_groups, \
    CHAR_OFFSET
from .Options import SpireOptions, option_groups
from .Regions import create_regions
from .Rules import set_rules
from ..AutoWorld import WebWorld, World


class SpireWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Slay the Spire for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "slay-the-spire_en.md",
        "slay-the-spire/en",
        ["Phar"]
    )]
    option_groups = option_groups

class SpireWorld(World):
    """
    A deck-building roguelike where you must craft a unique deck, encounter bizarre creatures, discover relics of
    immense power, and Slay the Spire!
    """

    options_dataclass = SpireOptions
    options: SpireOptions
    game = "Slay the Spire"
    topology_present = False
    web = SpireWeb()
    required_client_version = (0, 6, 1)
    mod_version = 2
    location_name_groups = location_groups
    item_name_groups = item_groups

    ut_can_gen_without_yaml = True

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table
    logger = logging.getLogger("SlayTheSpire")

    def __init__(self, mw: MultiWorld, player: int):
        super().__init__(mw, player)
        self.characters: List[CharacterConfig] = []
        self.modded_num = 0
        self.modded_chars: List[CharacterConfig] = []
        self.total_shop_locations = 0
        self.total_shop_items = 0

    def generate_early(self):
        if hasattr(self.multiworld, 're_gen_passthrough'):
            self._setup_ut(self.multiworld.re_gen_passthrough[self.game])
            return
        if self.options.use_advanced_characters.value == 0:
            self._handle_basic_chars()
        else:
            self._handle_advanced_chars()

        if not self.characters:
            raise OptionError("At least one character must be configured")
        names = set()
        for config in self.characters:
            self.logger.info("StS: Got character configuration" + str(config))
            names.add(config.official_name)
        if len(names) != len(self.characters):
            raise OptionError(f"Found duplicate characters: {[x.official_name for x in self.characters]}")
        for config in self.characters:
            if not config.locked:
                break
        else:
            raise OptionError("No character started unlocked!")
        self.total_shop_items = (self.options.shop_card_slots.value + self.options.shop_neutral_card_slots.value +
                                     self.options.shop_relic_slots.value + self.options.shop_potion_slots.value)
        self.total_shop_locations = self.total_shop_items + (3 if self.options.shop_remove_slots else 0)
        if self.total_shop_locations <= 0:
            self.options.shop_sanity.value = 0
        if len(self.modded_chars) > NUM_CUSTOM:
            raise OptionError(f"StS only supports {NUM_CUSTOM} modded characters; got {len(self.modded_chars)}: {[x.option_name for x in self.modded_chars]}")
        num_chars_goal = self.options.num_chars_goal.value
        if num_chars_goal != 0:
            if num_chars_goal > len(self.characters):
                self.options.num_chars_goal.value = 0
        for weight in self.options.trap_weights.values():
            if weight > 0:
                break
        else:
            self.options.trap_chance.value = 0

    def _get_unlocked_char(self, characters: List[str]) -> Optional[str]:
        if len(characters) <= 0:
            raise OptionError("At least one character must be selected.")
        locked_opt = self.options.lock_characters.value
        unlocked_char = None
        if locked_opt == 1:
            unlocked_char = self.random.choice([x for x in characters])
        elif locked_opt == 2:
            unlocked_char = self.options.unlocked_character.value
            if type(unlocked_char) == int:
                unlocked_char = character_list[unlocked_char]

            for char in characters:
                if char.lower() == unlocked_char.lower():
                    return char
            else:
                raise OptionError(
                    f"Configured {unlocked_char} as the first unlocked character, but was not one of: {characters}")
        return unlocked_char

    def _handle_basic_chars(self) -> None:
        if len(self.options.character.value) > 0:
            self.logger.warning("The 'character' option has been renamed to 'characters'; please update your yaml")
            self.options.characters.value = self.options.character.value
        selected_chars = sorted(self.options.characters.value)
        num_rand_chars = self.options.pick_num_characters.value
        unlocked_char = self._get_unlocked_char(selected_chars)
        if self.options.lock_characters.value != 0 and num_rand_chars != 0 and num_rand_chars < len(selected_chars):
            selected_chars.remove(unlocked_char)
            selected_chars = [unlocked_char] + self.random.sample(selected_chars, k=num_rand_chars - 1)
        self.logger.info("Generating with characters %s", selected_chars)
        ascension_down = self.options.ascension_down.value
        if self.options.include_floor_checks.value == 0:
            ascension_down = 0
        for char_val in selected_chars:
            option_name = char_val
            char_offset = character_offset_map[option_name.lower()]
            name = character_list[char_offset]
            if self.options.seeded:
                seed = "".join(self.random.choice(string.ascii_letters) for i in range(16))
            else:
                seed = ""
            locked = False if unlocked_char is None or unlocked_char.lower() == option_name.lower() else True
            config = CharacterConfig(name,
                                     option_name,
                                     char_offset,
                                     0,
                                     seed,
                                     locked,
                                     ascension=self.options.ascension.value,
                                     final_act=self.options.final_act.value == 1,
                                     downfall=self.options.downfall.value == 1,
                                     ascension_down=ascension_down)
            self.characters.append(config)

    def _handle_advanced_chars(self) -> None:
        advanced_chars = self.options.advanced_characters.keys()
        char_options = sorted(advanced_chars)
        num_rand_chars = self.options.pick_num_characters.value
        unlocked_char = self._get_unlocked_char(char_options)
        include_ascension_down = self.options.include_floor_checks.value != 0
        if self.options.lock_characters.value != 0 and num_rand_chars != 0 and num_rand_chars < len(char_options):
            selected_chars = list(char_options)
            if unlocked_char in selected_chars:
                selected_chars.remove(unlocked_char)
            selected_chars = [unlocked_char] + self.random.sample(selected_chars, k=num_rand_chars - 1)
            modded_num = 0
            for char in selected_chars:
                if character_offset_map.get(char.lower(), None) is None:
                    modded_num += 1
            if modded_num > NUM_CUSTOM:
                supported_chars = sorted({x for x in char_options if x.lower() in character_offset_map})
                replace_num = modded_num - NUM_CUSTOM
                remove_me = self.random.sample(selected_chars, k=replace_num)
                for remove in remove_me:
                    selected_chars.remove(remove)
                selected_chars += self.random.sample(supported_chars, k=min(replace_num, len(supported_chars)))
        else:
            selected_chars = char_options

        self.logger.info("Generating with characters %s", selected_chars)
        for option_name in selected_chars:
            options = self.options.advanced_characters[option_name]
            mod_num = 0
            char_offset = character_offset_map.get(option_name.lower(), None)
            if char_offset is None:
                self.modded_num += 1
                mod_num = self.modded_num
                char_offset = mod_num + len(character_list) - 1
                name = f"Custom Character {mod_num}"
            else:
                name = character_list[char_offset]
            if self.options.seeded:
                seed = "".join(self.random.choice(string.ascii_letters) for i in range(16))
            else:
                seed = ""
            locked = False if unlocked_char is None or unlocked_char.lower() == option_name.lower() else True
            config = CharacterConfig(name,
                                     option_name,
                                     char_offset,
                                     mod_num,
                                     seed,
                                     locked,
                                     **options)
            if not include_ascension_down:
                config.ascension_down = 0
            self.characters.append(config)
            if config.mod_num > 0:
                self.modded_chars.append(config)

    def create_items(self):
        # Fill out our pool with our items from item_pool, assuming 1 item if not present in item_pool
        pool = []
        for config in self.characters:
            char_lookup = config.name if config.mod_num == 0 else config.mod_num
            ascension_downs = min(config.ascension_down, config.ascension)
            for name, data in chars_to_items[char_lookup].items():
                amount = 0
                if ItemType.CARD_REWARD == data.type:
                    amount = CARD_REWARD_COUNT
                elif ItemType.RARE_CARD_REWARD == data.type or ItemType.BOSS_RELIC == data.type:
                    amount = 2
                elif ItemType.RELIC == data.type:
                    amount = 10
                elif ItemType.CAMPFIRE == data.type and self.options.campfire_sanity.value != 0:
                    amount = 3
                elif ItemType.CHAR_UNLOCK == data.type and self.options.lock_characters.value != 0 and config.locked:
                    amount = 1
                elif ItemType.GOLD == data.type and self.options.gold_sanity.value != 0:
                    if '15 Gold' in name:
                        amount = 18
                    elif '30 Gold' in name:
                        amount = 7
                    elif 'Boss Gold' in name:
                        amount = 2
                elif ItemType.POTION == data.type and self.options.potion_sanity:
                    amount = 9
                elif ItemType.ASCENSION_DOWN == data.type and self.options.include_floor_checks.value != 0:
                    amount = ascension_downs
                elif self.options.shop_sanity.value != 0:
                    if ItemType.SHOP_CARD == data.type:
                        amount = self.options.shop_card_slots.value
                    elif ItemType.SHOP_NEUTRAL == data.type:
                        amount = self.options.shop_neutral_card_slots.value
                    elif ItemType.SHOP_RELIC == data.type:
                        amount = self.options.shop_relic_slots.value
                    elif ItemType.SHOP_POTION == data.type:
                        amount = self.options.shop_potion_slots.value
                    elif ItemType.SHOP_REMOVE == data.type and self.options.shop_remove_slots.value != 0:
                        amount = 3
                for _ in range(amount):
                    pool.append(SpireItem(name, self.player))

            if self.options.include_floor_checks.value:

                remaining_checks = 51 - ascension_downs

                if config.final_act:
                    remaining_checks += 4
                if config.ascension >= 20:
                    remaining_checks += 1

                traps: list[bool] = [self.random.randint(0, 100) < self.options.trap_chance for _ in range(remaining_checks)]
                trap_num = traps.count(True)
                filler_num = len(traps) - trap_num
                for name in self.random.choices(list(self.options.trap_weights.keys()), weights=list(self.options.trap_weights.values()),k=trap_num):
                    pool.append(SpireItem(name, self.player))
                for name in self.random.choices([key for key, val in chars_to_items[char_lookup].items()
                                                 if ItemType.GOLD == val.type and ItemClassification.filler == val.classification], weights=[40,60],k=filler_num):
                    pool.append(SpireItem(name, self.player))
            # Pair up our event locations with our event items
            for base_event, base_item in base_event_item_pairs.items():
                event = f"{config.name} {base_event}"
                item = f"{config.name} {base_item}"
                event_item = SpireItem(item, self.player)
                self.multiworld.get_location(event, self.player).place_locked_item(event_item)

        self.multiworld.itempool += pool

    def set_rules(self):
        set_rules(self, self.player)

    def create_item(self, name: str) -> Item:
        return SpireItem(name, self.player)

    def create_regions(self):
        create_regions(self, self.player)

    def fill_slot_data(self) -> dict:
        slot_data = {
            'characters': [
                c.to_dict() for c in self.characters
            ],
            'shop_sanity_options': {
                "card_slots": self.options.shop_card_slots.value,
                "neutral_slots": self.options.shop_neutral_card_slots.value,
                "relic_slots": self.options.shop_relic_slots.value,
                "potion_slots": self.options.shop_potion_slots.value,
                "card_remove": self.options.shop_remove_slots != 0,
                "costs": self.options.shop_sanity_costs.value,
            },
            "mod_version": self.mod_version,
        }
        slot_data.update(self.options.as_dict(
            "ascension",
            "final_act",
            "downfall",
            "death_link",
            "include_floor_checks",
            "campfire_sanity",
            "shop_sanity",
            "gold_sanity",
            "potion_sanity",
            "chatty_mc",
            "num_chars_goal",
        ))
        return slot_data

    def get_filler_item_name(self) -> str:
        if not self.characters:
            return "CAW CAW"
        config = self.random.choice(self.characters)
        return self.random.choice([f"{config.name} One Gold", f"{config.name} Five Gold"])

    def create_region(self, player: int, prefix: Optional[str], name: str, config: CharacterConfig, locations: List[str] = None, exits: List[str] =None):
        ret = Region(f"{prefix} {name}" if prefix is not None else name, player, self.multiworld)
        if locations:
            locs: dict[str, Optional[int]] = dict()
            for location in locations:
                loc_name = f"{prefix} {location}" if prefix is not None else location
                loc_id = location_table.get(loc_name, 0)
                loc_data = loc_ids_to_data.get(loc_id, None)
                if self._should_include_location(loc_data, config):
                    locs[loc_name] = loc_id
            ret.add_locations(locs, SpireLocation)
        if exits:
            for exit in exits:
                exit_name = f"{prefix} {exit}" if prefix is not None else exit
                ret.create_exit(exit_name)
        return ret

    def _should_include_location(self, data: LocationData, config: CharacterConfig) -> bool:
        if data is None:
            return True
        if data.type == LocationType.Floor and self.options.include_floor_checks == 0:
            return False
        elif data.type == LocationType.Campfire and self.options.campfire_sanity == 0:
            return False
        elif data.type == LocationType.Shop:
            if self.options.shop_sanity.value == 0:
                return False
            total_shop = self.total_shop_locations
            return total_shop >= data.id - 163
        elif data.type == LocationType.Start and (self.options.lock_characters == 0 or not config.locked):
            return False
        elif data.type == LocationType.Gold and self.options.gold_sanity.value == 0:
            return False
        elif data.type == LocationType.Potion and self.options.potion_sanity.value == 0:
            return False
        return True

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> Any:
        return slot_data

    def _setup_ut(self, slot_data: dict[str, Any]) -> None:
        self.options.shop_remove_slots.value = slot_data["shop_sanity_options"]["card_remove"]
        self.options.shop_neutral_card_slots.value = slot_data["shop_sanity_options"]["neutral_slots"]
        self.options.shop_relic_slots.value = slot_data["shop_sanity_options"]["relic_slots"]
        self.options.shop_potion_slots.value = slot_data["shop_sanity_options"]["potion_slots"]
        for char_dict in slot_data['characters']:
            config = CharacterConfig(
                char_dict['name'],
                char_dict['option_name'],
                char_dict['char_offset'],
                char_dict['mod_num'],
                char_dict['seed'],
                char_dict['locked'],
                ascension=char_dict['ascension'],
                final_act=char_dict['final_act'],
                downfall=char_dict['downfall'],
                ascension_down=char_dict['ascension_down'],
            )
            self.characters.append(config)
            if char_dict['mod_num'] > 0:
                self.modded_chars.append(config)
        self.total_shop_items = (self.options.shop_card_slots.value + self.options.shop_neutral_card_slots.value +
                                 self.options.shop_relic_slots.value + self.options.shop_potion_slots.value)
        self.total_shop_locations = self.total_shop_items + (3 if self.options.shop_remove_slots else 0)
        if self.total_shop_locations <= 0:
            self.options.shop_sanity.value = 0
        self.options.include_floor_checks.value = slot_data['include_floor_checks']
        self.options.campfire_sanity.value = slot_data['campfire_sanity']
        self.options.shop_sanity.value = slot_data['shop_sanity']
        self.options.gold_sanity.value = slot_data['gold_sanity']
        self.options.potion_sanity.value = slot_data['potion_sanity']
        self.options.num_chars_goal.value = slot_data['num_chars_goal']
        self.location_id_to_alias: dict[int, str] = dict()
        pattern = re.compile("Custom Character [0-9]+ (?P<location_name>.*?)$")
        # for i in range(1, len(self.modded_chars) + 1):
        for key, value in SpireWorld.location_id_to_name.items():
            if key < (len(character_list)) * CHAR_OFFSET:
                continue
            modded_index = (key // CHAR_OFFSET) - len(character_list)
            self.logger.info(f"Modded index: {modded_index}")
            self.logger.info(f"modded_chars index: {self.modded_chars}")
            if modded_index >= len(self.modded_chars):
                continue
            match = pattern.match(value)
            if match is None:
                raise Exception("Failed to match " + value)
            name = self.modded_chars[modded_index].official_name
            self.logger.info(name)
            self.location_id_to_alias[key] = name + " " + match.group("location_name")


class SpireLocation(Location):
    game: str = "Slay the Spire"


class SpireItem(Item):
    game = "Slay the Spire"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(SpireItem, self).__init__(
            name,
            item_data.classification,
            item_data.code, player
        )
