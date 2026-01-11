from typing import Mapping, Any
from worlds.AutoWorld import World, WebWorld
from BaseClasses import MultiWorld, Tutorial, ItemClassification, Region
from .enums import (Spelunky2Goal, VICTORY_STRING, ItemName, JournalName, WorldName, 
                    LocationName, RuleNames, UPGRADE_SUFFIX)
from .Items import (Spelunky2Item, item_data_table, filler_items, traps, filler_weights, trap_weights,
                    characters, upgrade_items_dict, locked_items_dict, permanent_upgrades, world_unlocks, quest_items)
from .Locations import Spelunky2Location, location_data_table
from .Options import Spelunky2Options
from .Regions import region_data_table
from .Rules import set_common_rules, set_sunken_city_rules, set_cosmic_ocean_rules, set_starter_upgrade_rules

obnoxious_locations = frozenset({JournalName.MAGMAR.value, JournalName.LAVAMANDER.value, JournalName.MECH_RIDER.value,
                                 JournalName.SCORPION, JournalName.TRUE_CROWN})


class Spelunky2WebWorld(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        tutorial_name="Setup Guide",
        description="A guide to setting up Spelunky 2",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["Eszenn", "DDRKhat"]
    )
    tutorials = [setup_en]


class Spelunky2World(World):
    """Spelunky 2 is an extremely difficult roguelike platformer where your progression is gated by multiworld unlocks.
    Your ultimate goal is to complete one of the game's various paths. Your primary objective is to complete 'checks' by
    discovering new journal entries, which sends an item from the multiworld into the item pool. The rewards you receive
    can range from simple 'filler' items to world unlocks that allow you to progress, as well as key quest-chain items
    like the Udjat Eye and Hou Yi's Bow. These critical items must be received from the multiworld before you can obtain
    them in-game."""

    game = "Spelunky 2"
    web = Spelunky2WebWorld()
    options: Spelunky2Options
    options_dataclass = Spelunky2Options
    filler_count = 0
    trap_count = 0

    item_data_table = item_data_table

    item_name_to_id = {name: data.code for name, data in locked_items_dict.items()}
    item_name_to_id.update({name: data.code for name, data in upgrade_items_dict.items()})
    item_name_to_id.update({name: data.code for name, data in filler_items.items()})
    item_name_to_id.update({name: data.code for name, data in traps.items()})
    item_name_to_id.update({name: data.code for name, data in characters.items()})
    item_name_to_id.update({name: data.code for name, data in world_unlocks.items()})
    item_name_to_id.update({name: data.code for name, data in permanent_upgrades.items()})
    location_name_to_id = {name: data.address for name, data in location_data_table.items()}

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.filler_weights = filler_weights.copy()
        self.trap_weights = trap_weights.copy()

    def generate_early(self) -> None:
        pass

    def create_regions(self) -> None:
        exclude_regions = []

        if self.options.goal == Spelunky2Goal.EASY:
            exclude_regions.append(WorldName.SUNKEN_CITY)
            exclude_regions.append(WorldName.EGGPLANT)

        if self.options.goal != Spelunky2Goal.CO:
            exclude_regions.append(WorldName.COSMIC_OCEAN)

        for region_name in region_data_table.keys():
            if region_name in exclude_regions:
                continue

            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        for region_name, region_data in region_data_table.items():
            if region_name in exclude_regions:
                continue

            region = self.get_region(region_name)
            if region_data.exits is not None:
                for region_exit in region_data.exits:
                    if region_exit in exclude_regions:
                        continue
                    connecting_region = self.get_region(region_exit)
                    region.connect(connecting_region)

            region.add_locations({
                location_name: self.location_name_to_id[location_name]
                for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.goal <= self.options.goal
                and (location_name not in obnoxious_locations or self.options.include_hard_locations)
            }, Spelunky2Location)

        if self.options.goal == Spelunky2Goal.HARD:
            goal_region = self.get_region(WorldName.SUNKEN_CITY)
        elif self.options.goal == Spelunky2Goal.CO:
            goal_region = self.get_region(WorldName.COSMIC_OCEAN)
        else:
            goal_region = self.get_region(WorldName.NEO_BABYLON)

        goal_location = Spelunky2Location(self.player, VICTORY_STRING, None, goal_region)
        goal_location.place_locked_item(
            Spelunky2Item(VICTORY_STRING, ItemClassification.progression, None, self.player)
        )
        self.multiworld.completion_condition[self.player] = lambda state: state.has(VICTORY_STRING, self.player)
        goal_region.locations.append(goal_location)

    def create_item(self, name: str) -> "Spelunky2Item":
        data = self.item_data_table[name]
        return Spelunky2Item(name, data.classification, data.code, self.player)

    def create_items(self) -> None:
        spelunky2_item_pool = []

        # Handle Progressive Worlds and Goals
        if self.options.progressive_worlds.value:
            unlock_count = 5
            if self.options.goal.value > Spelunky2Goal.EASY:
                unlock_count += 1
            if self.options.goal.value > Spelunky2Goal.HARD:
                unlock_count += 1
            for _ in range(unlock_count):
                spelunky2_item_pool.append(
                    self.create_item(str(WorldName.PROGRESSIVE))
                )
        else:
            individual_worlds = [
                WorldName.JUNGLE.value,
                WorldName.VOLCANA.value,
                WorldName.OLMECS_LAIR.value,
                WorldName.TIDE_POOL.value,
                WorldName.TEMPLE.value,
                WorldName.ICE_CAVES.value,
                WorldName.NEO_BABYLON.value,
            ]
            if self.options.goal.value >= Spelunky2Goal.HARD:
                individual_worlds.append(WorldName.SUNKEN_CITY)
            if self.options.goal.value == Spelunky2Goal.CO:
                individual_worlds.append(WorldName.COSMIC_OCEAN)
            spelunky2_item_pool.extend([
                self.create_item(str(world)) for world in individual_worlds
            ])
        # Add all quest items that match the goal
        if self.options.goal.value == Spelunky2Goal.EASY:
            quest_item_names = quest_items - {ItemName.ARROW_OF_LIGHT.value,
                                              ItemName.HOU_YI_BOW.value,
                                              ItemName.TABLET_OF_DESTINY.value,
                                              ItemName.USHABTI.value}
        elif self.options.goal.value == Spelunky2Goal.HARD:
            quest_item_names = quest_items - {ItemName.ARROW_OF_LIGHT.value,
                                              ItemName.HOU_YI_BOW.value}
        else:
            quest_item_names = quest_items

        # Filter restricted_items so only goal-valid quest items remain
        filtered_restricted = []
        for item_name in self.options.restricted_items.value:
            if item_name not in quest_items or item_name in quest_item_names:
                filtered_restricted.append(item_name)
                spelunky2_item_pool.append(self.create_item(item_name))

        self.options.restricted_items.value = filtered_restricted

        all_upgrades_selected = self.options.waddler_upgrades.value | self.options.item_upgrades.value

        # Add a single "Upgrade" item for each unique item selected. (Except Alien/Compass . Special Rules)
        compasses = 2 if ItemName.ALIEN_COMPASS in all_upgrades_selected else (
                    1 if ItemName.COMPASS in all_upgrades_selected
                    else 0)
        for _ in range(compasses):
            spelunky2_item_pool.append(self.create_item(f"{ItemName.COMPASS}{UPGRADE_SUFFIX}"))
        for item_name in all_upgrades_selected:
            if item_name not in (ItemName.ALIEN_COMPASS, ItemName.COMPASS):
                spelunky2_item_pool.append(self.create_item(f"{item_name}{UPGRADE_SUFFIX}"))

        # Permanent upgrades
        for _ in range(self.options.health_upgrades):
            spelunky2_item_pool.append(
                self.create_item(str(ItemName.HEALTH_UPGRADE))
            )
        for _ in range(self.options.bomb_upgrades):
            spelunky2_item_pool.append(
                self.create_item(str(ItemName.BOMB_UPGRADE))
            )
        for _ in range(self.options.rope_upgrades):
            spelunky2_item_pool.append(
                self.create_item(str(ItemName.ROPE_UPGRADE))
            )

        # Cosmic Ocean checkpoints
        if self.options.goal.value == Spelunky2Goal.CO:
            for _ in range(int(self.options.goal_level.value / 10)):
                spelunky2_item_pool.append(
                    self.create_item(str(ItemName.COSMIC_OCEAN_CP))
                )

        # Characters to add (minus the "Starting" ones, because we begin with them)
        starting_characters = set(self.options.starting_characters or [ItemName.ANA_SPELUNKY.value])
        for char_name in characters:
            if char_name not in starting_characters:
                spelunky2_item_pool.append(self.create_item(char_name))

        # Filler & traps
        locations_count = len(self.multiworld.get_unfilled_locations(self.player))
        self.filler_count = locations_count - len(spelunky2_item_pool)

        self.filler_weights[ItemName.ROPE_PILE.value]   = self.options.rope_pile_weight.value
        self.filler_weights[ItemName.BOMB_BAG.value]    = self.options.bomb_bag_weight.value
        self.filler_weights[ItemName.BOMB_BOX.value]    = self.options.bomb_box_weight.value
        self.filler_weights[ItemName.COOKED_TURKEY.value] = self.options.cooked_turkey_weight.value
        self.filler_weights[ItemName.ROYAL_JELLY.value] = self.options.royal_jelly_weight.value
        self.filler_weights[ItemName.GOLD_BAR.value]    = self.options.gold_bar_weight.value
        self.filler_weights[ItemName.EMERALD_GEM.value] = self.options.emerald_gem_weight.value
        self.filler_weights[ItemName.SAPPHIRE_GEM.value] = self.options.sapphire_gem_weight.value
        self.filler_weights[ItemName.RUBY_GEM.value]    = self.options.ruby_gem_weight.value
        self.filler_weights[ItemName.DIAMOND_GEM.value] = self.options.diamond_gem_weight.value

        if sum(self.filler_weights.values()) <= 0:
            self.filler_weights = {ItemName.GOLD_BAR.value: 1}

        if self.options.enable_traps.value:
            self.trap_count = int(self.filler_count * (self.options.trap_weight.value / 100))
            self.filler_count -= self.trap_count

            self.trap_weights[ItemName.POISON_TRAP.value]      = self.options.poison_weight.value
            self.trap_weights[ItemName.CURSE_TRAP.value]       = self.options.curse_weight.value
            self.trap_weights[ItemName.GHOST_TRAP.value]       = self.options.ghost_weight.value
            self.trap_weights[ItemName.STUN_TRAP.value]        = self.options.stun_weight.value
            self.trap_weights[ItemName.LOOSE_BOMBS_TRAP.value] = self.options.bomb_weight.value
            self.trap_weights[ItemName.BLINDNESS_TRAP.value]   = self.options.blind_weight.value
            self.trap_weights[ItemName.PUNISH_BALL_TRAP.value] = self.options.punish_weight.value

            for _ in range(self.trap_count):
                spelunky2_item_pool.append(self.create_trap())

        for _ in range(self.filler_count):
            spelunky2_item_pool.append(self.create_filler())

        self.multiworld.itempool.extend(spelunky2_item_pool)

    def create_filler(self) -> "Spelunky2Item":
        return self.create_item(
            self.random.choices(list(self.filler_weights.keys()), list(self.filler_weights.values()))[0])

    def create_trap(self) -> "Spelunky2Item":
        return self.create_item(
            self.random.choices(list(self.trap_weights.keys()), list(self.trap_weights.values()))[0])

    def set_rules(self) -> None:
        set_common_rules(self, self.player)

        if self.options.goal != Spelunky2Goal.EASY:
            set_sunken_city_rules(self, self.player)
            self.multiworld.register_indirect_condition(
                self.get_region(LocationName.DUAT), self.get_entrance(RuleNames.NEO_BABYLON_TO_SUNKEN_CITY)
            )
            self.multiworld.register_indirect_condition(
                self.get_region(LocationName.ABZU), self.get_entrance(RuleNames.NEO_BABYLON_TO_SUNKEN_CITY)
            )

        if self.options.goal == Spelunky2Goal.CO:
            set_cosmic_ocean_rules(self, self.player)
            self.multiworld.register_indirect_condition(
                self.get_region(WorldName.SUNKEN_CITY), self.get_entrance(RuleNames.SUNKEN_CITY_TO_COSMIC_OCEAN)
            )

        # Add the rule-setter for starter item upgrades
        set_starter_upgrade_rules(self, self.player)

        self.multiworld.register_indirect_condition(
            self.get_region(LocationName.VLADS_CASTLE), self.get_entrance(RuleNames.ICE_CAVES_TO_MOTHERSHIP)
        )

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = {
            "goal": self.options.goal.value,
            "progressive_worlds": bool(self.options.progressive_worlds),
            "increase_starting_wallet": bool(self.options.starting_wallet),
            "starting_health": self.options.starting_health.value,
            "starting_bombs": self.options.starting_bombs.value,
            "starting_ropes": self.options.starting_ropes.value,
            "starting_characters": [
                self.item_name_to_id[name]
                for name in (self.options.starting_characters or [ItemName.ANA_SPELUNKY.value])
                if name in self.item_name_to_id
            ],
            "health_upgrades": self.options.health_upgrades.value,
            "bomb_upgrades": self.options.bomb_upgrades.value,
            "rope_upgrades": self.options.rope_upgrades.value,
            "restricted_items": list(self.options.restricted_items),
            "item_upgrades": [
                self.item_name_to_id[f"{name}{UPGRADE_SUFFIX}"]
                for name in self.options.item_upgrades.value
                if name not in self.options.waddler_upgrades.value
                and name in self.item_name_to_id
            ],
            "waddler_upgrades": [
                self.item_name_to_id[f"{name}{UPGRADE_SUFFIX}"]
                for name in self.options.waddler_upgrades.value
                if name in self.item_name_to_id
            ],
            "include_hard_locations": bool(self.options.include_hard_locations),
            "journal_entry_required": bool(self.options.journal_entry_required),
            "death_link": self.options.death_link.value > 0,
        }

        if self.options.goal.value == Spelunky2Goal.CO:
            slot_data["goal_level"] = self.options.goal_level.value

        if slot_data["death_link"]:
            slot_data["bypass_ankh"] = bool(self.options.bypass_ankh)

        return slot_data
