import dataclasses
import itertools
import logging
import typing
from collections import defaultdict
from dataclasses import dataclass

from BaseClasses import Region, Location, Item, ItemClassification, CollectionState, Tutorial
from Fill import fill_restrictive, FillError
from settings import Group, Bool, FilePath
from Options import Accessibility, OptionGroup
from worlds.AutoWorld import WebWorld, World
from typing import ClassVar, List, Callable, Dict, Any, Set, Iterable, Type, Tuple, Optional

from . import Constants, Options
from .Constants import AccessRule

from .Data import Items, Locations, Regions, Exits, Events
from .Data.Events import EventData, EventFlags
from .Data.Regions import RegionEnum, Nexus, Red_Cave, Blue, Happy, Forest, Windmill, Bedroom, Street, Hotel, Fields
from .Options import AnodyneGameOptions, SmallKeyShuffle, StartBroom, VictoryCondition, BigKeyShuffle, \
    HealthCicadaShuffle, NexusGatesOpen, RedCaveAccess, PostgameMode, NexusGateShuffle, TrapPercentage, SmallKeyMode, \
    Dustsanity, GateType, gatereq_classes, CardAmount, EndgameRequirement, GateRequirements, MitraHints, gate_lookup, \
    OverworldFieldsGate
from .ut_stuff import UTTrackerData


class AnodyneLocation(Location):
    game = "Anodyne"


class AnodyneItem(Item):
    game = "Anodyne"


class AnodyneSettings(Group):
    class UTTrackerPath(FilePath):
        """Path to the user's Anodyne UT map pack."""
        description = "Anodyne's Universal Tracker zip file"
        required = False

    ut_tracker_path: UTTrackerPath | str = UTTrackerPath()

class AnodyneWebWorld(WebWorld):
    theme = "dirt"
    option_groups = [
        OptionGroup("Key Logic", [
            Options.SmallKeyMode,
            Options.SmallKeyShuffle,
            Options.BigKeyShuffle
        ]),
        OptionGroup("Cards", [
            Options.CardAmount,
            Options.ExtraCardAmount
        ]),
        OptionGroup("Logic Changes", [
            Options.SplitWindmill,
            Options.IncludeBlueAndHappy,
            Options.FieldsSecretPaths,
            Options.RandomizeColorPuzzle,
            Options.NexusGateShuffle,
            Options.RedCaveAccess
        ]),
        OptionGroup("Starting Nexus Gates", [
            Options.NexusGatesOpen,
            Options.RandomNexusGateOpenCount,
            Options.CustomNexusGatesOpen
        ]),
        OptionGroup("Extra Locations", [
            Options.Dustsanity,
            Options.HealthCicadaShuffle,
            Options.IncludeForestBunnyChest
        ]),
        OptionGroup("Filler Items", [
            Options.TrapPercentage
        ]),
        OptionGroup("Big Gate Logic", [option for gatereqs in [
            [gatereq.Gate, gatereq.GateCardReq, gatereq.GateBossReq]
            for gatereq in Options.gatereq_classes] for option in gatereqs]
                    )
    ]
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Anodyne with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["PixieCatSupreme", "SephDB", "hatkirby"]
    )]


class AnodyneWorld(World):
    """
    Anodyne is a unique Zelda-like game, influenced by games such as Yume Nikki and Link's Awakening. 
    In Anodyne, you'll visit areas urban, natural, and bizarre, fighting your way through dungeons 
    and areas in Young's subconscious.
    """
    game = "Anodyne"  # name of the game/world
    web = AnodyneWebWorld()

    options_dataclass = AnodyneGameOptions
    options: AnodyneGameOptions
    settings: ClassVar[AnodyneSettings]
    topology_present = False  # show path to required location checks in spoiler

    ut_can_gen_without_yaml = True
    tracker_world = UTTrackerData
    using_ut: bool
    found_entrances_datastorage_key = "Slot:{player}:EventMap"
    tracked_events: EventFlags

    version = "0.4.0"

    item_name_to_id = Constants.item_name_to_id
    location_name_to_id = Constants.location_name_to_id
    item_name_groups = Items.item_groups
    location_name_groups = Locations.location_groups

    origin_region_name = str(Regions.Nexus.bottom)

    gates_unlocked: List[type[RegionEnum]]
    location_count: int
    dungeon_items: Dict[type[RegionEnum], List[Item]]
    proxy_rules: Dict[str, List[str]]
    shuffled_gates: Set[type[RegionEnum]]

    def generate_early(self):
        self.gates_unlocked = []
        self.location_count = 0
        self.dungeon_items = dict()
        self.proxy_rules = dict()
        self.shuffled_gates = set()
        self.using_ut = False
        self.tracked_events = EventFlags(0)

        nexus_gate_open = self.options.nexus_gates_open

        # Street is always unlocked
        if hasattr(self.multiworld, "re_gen_passthrough") and "Anodyne" in self.multiworld.re_gen_passthrough:
            self.using_ut = True
            # Universal tracker; ignored during normal gen.
            slot_data = self.multiworld.re_gen_passthrough["Anodyne"]

            self.gates_unlocked = [Regions.all_areas[i] for i in slot_data["nexus_gates_unlocked"]]
            self.options.small_key_mode.value = slot_data["small_key_mode"]
            self.options.small_key_shuffle.value = slot_data["shuffle_small_keys"]
            self.options.big_key_shuffle.value = slot_data["shuffle_big_gates"]
            self.options.split_windmill.value = slot_data["split_windmill"]
            self.options.postgame_mode.value = slot_data["postgame_mode"]
            self.options.nexus_gate_shuffle.value = slot_data["nexus_gate_shuffle"]
            self.options.victory_condition.value = slot_data["victory_condition"]
            self.options.forest_bunny_chest.value = slot_data.get("forest_bunny_chest", False)
            self.options.fields_secret_paths.value = slot_data.get("fields_secret_paths", False)
            self.options.dustsanity.value = slot_data.get("dustsanity", False)
            if "endgame_card_requirement" in slot_data:
                EndgameRequirement.cardoption(self.options).value = slot_data["endgame_card_requirement"]
            self.options.include_blue_happy.value = slot_data.get("include_blue_happy", False)
            self.options.red_grotto_access.value = RedCaveAccess.option_vanilla \
                if slot_data.get("vanilla_red_cave", True) \
                else RedCaveAccess.option_progressive
            self.options.randomize_color_puzzle.value = slot_data.get("randomize_color_puzzle", False)

            self.options.card_amount.value = slot_data.get("card_amount", CardAmount.option_vanilla)
            # For universal tracker, slot data already has final value for card amount + extra, extra can be set to 0
            self.options.extra_cards.value = 0
            for c in gatereq_classes:
                option_name: str = slot_data.get(c.typename(), c.shorthand(self.options))
                type_option = c.typeoption(self.options)
                if option_name.startswith("cards"):
                    type_option.value = GateType.CARDS
                    c.cardoption(self.options).value = int(option_name[len("cards_"):])
                elif option_name.startswith("bosses"):
                    type_option.value = GateType.BOSSES
                    c.bossoption(self.options).value = int(option_name[len("bosses_"):])
                else:
                    type_option.value = type_option.from_text(option_name).value
        elif len(self.options.custom_nexus_gates_open.value) > 0:
            self.gates_unlocked.extend(Regions.area_lookup[name] for name in self.options.custom_nexus_gates_open.value)
        elif nexus_gate_open == NexusGatesOpen.option_street_and_fields:
            self.gates_unlocked.append(Fields)
        elif nexus_gate_open == NexusGatesOpen.option_early:
            self.gates_unlocked.extend(Regions.early_nexus_gates)
        elif nexus_gate_open == NexusGatesOpen.option_all:
            for location in Locations.nexus_pad_locations:
                self.gates_unlocked.append(location.region.__class__)
        elif nexus_gate_open in [NexusGatesOpen.option_random_count, NexusGatesOpen.option_random_pre_endgame]:
            random_nexus_gate_count = int(self.options.random_nexus_gate_open_count)

            available_gates = [location.region.__class__ for location in Locations.nexus_pad_locations]
            if nexus_gate_open == NexusGatesOpen.option_random_pre_endgame:
                for gate in Regions.endgame_nexus_gates:
                    available_gates.remove(gate)

            if random_nexus_gate_count > len(available_gates):
                logging.warning(
                    f"Player {self.player_name} requested more random Nexus gates than are available. "
                    f"Adjusting down to {len(available_gates)}")
                random_nexus_gate_count = len(available_gates)

            self.gates_unlocked = self.random.sample(available_gates, random_nexus_gate_count)

        if (self.options.small_key_mode == SmallKeyMode.option_key_rings and
                self.options.small_key_shuffle == SmallKeyShuffle.option_vanilla):
            self.options.small_key_shuffle.value = SmallKeyShuffle.option_original_dungeon
            self.options.small_key_mode.value = SmallKeyMode.option_small_keys
            logging.warning(
                f"Player {self.player_name} requested vanilla small keys with key rings on, "
                f"changing to small key original dungeon")

        if self.options.nexus_gate_shuffle != NexusGateShuffle.option_off:
            self.shuffled_gates = set(item.map for item in Items.Nexus.all()) - set(self.gates_unlocked)

            if self.options.nexus_gate_shuffle == NexusGateShuffle.option_all_except_endgame:
                self.shuffled_gates -= set(Regions.endgame_nexus_gates)

        if (self.options.victory_condition == VictoryCondition.option_final_gate and
                self.options.postgame_mode == PostgameMode.option_disabled):
            logging.warning(
                f"Player {self.player_name} requested the final gate victory condition but turned off postgame. "
                f"Changing goal to Briar")
            self.options.victory_condition.value = VictoryCondition.option_defeat_briar

        if all(gate in Regions.wrong_big_key_early_locked_nexus_gates for gate in self.gates_unlocked) and \
                self.options.nexus_gate_shuffle == NexusGateShuffle.option_off and \
                self.options.big_key_shuffle == BigKeyShuffle.option_vanilla and \
                OverworldFieldsGate.typeoption(self.options) in [GateType.BLUE, GateType.RED]:
            logging.warning(
                f"Player {self.player_name} has locked themselves into the starting area with no escape. "
                f"Reverting Overworld->Fields gate to default")
            OverworldFieldsGate.typeoption(self.options).value = GateType.GREEN

    def create_item(self, name: str) -> Item:
        data = Items.all_items.get(name, None)
        item_class = ItemClassification.filler
        if data is not None:
            item_class = data.classification

        return AnodyneItem(name, item_class, self.item_name_to_id.get(name, None), self.player)

    def create_items(self) -> None:
        item_pool: List[Item] = []
        local_item_pool: set[str] = set()
        non_local_item_pool: set[str] = set()

        small_key_mode: SmallKeyMode = self.options.small_key_mode
        small_key_shuffle: SmallKeyShuffle = self.options.small_key_shuffle
        health_cicada_shuffle = self.options.health_cicada_shuffle
        big_key_shuffle = self.options.big_key_shuffle
        start_broom: StartBroom = self.options.start_broom

        placed_items = 0

        prevent_autoplacement: list[Items.ItemData] = [
            *Items.Keys.all(),
            *Items.BigKey.all(),
            *Items.Cicada.all(),
            *Items.RedCaveUnlock.all(),
            Items.Inventory.Progressive_Swap.item,
            *Items.Nexus.all(),
            *Items.Card.all()
        ]

        if small_key_mode == SmallKeyMode.option_small_keys:
            if small_key_shuffle == SmallKeyShuffle.option_vanilla:
                for location in Locations.all_locations:
                    if location.small_key:
                        item_name = Items.Keys.Small_Key[location.region.__class__].full_name
                        self.multiworld.get_location(location.name, self.player).place_locked_item(
                            self.create_item(item_name))
                        placed_items += 1
            elif small_key_shuffle == SmallKeyShuffle.option_original_dungeon:
                for dungeon, count in Constants.small_key_count.items():
                    small_key_name = Items.Keys.Small_Key[dungeon].full_name
                    items = self.dungeon_items.setdefault(dungeon, [])

                    for _ in range(count):
                        items.append(self.create_item(small_key_name))
                        placed_items += 1
            else:
                for key_item in Items.Keys.Small_Key:
                    count = Constants.small_key_count[key_item.map]
                    placed_items += count

                    for _ in range(count):
                        item_pool.append(self.create_item(key_item.full_name))

                    if small_key_shuffle == SmallKeyShuffle.option_own_world:
                        local_item_pool.add(key_item.full_name)
                    elif small_key_shuffle == SmallKeyShuffle.option_different_world:
                        non_local_item_pool.add(key_item.full_name)
        elif small_key_mode == SmallKeyMode.option_key_rings:
            for dungeon in Constants.small_key_count.keys():
                placed_items += 1
                key_item = Items.Keys.Key_Ring[dungeon].full_name
                item = self.create_item(key_item)

                if small_key_shuffle == SmallKeyShuffle.option_original_dungeon:
                    self.dungeon_items.setdefault(dungeon, []).append(item)
                else:
                    item_pool.append(item)

                    if small_key_shuffle == SmallKeyShuffle.option_own_world:
                        local_item_pool.add(key_item)
                    elif small_key_shuffle == SmallKeyShuffle.option_different_world:
                        non_local_item_pool.add(key_item)

        start_broom_item: Optional[Items.ItemData] = None
        if start_broom == StartBroom.option_normal:
            start_broom_item = Items.Inventory.Broom.item
        elif start_broom == StartBroom.option_wide:
            start_broom_item = Items.Inventory.Widen.item
        elif start_broom == StartBroom.option_long:
            start_broom_item = Items.Inventory.Extend.item
        elif start_broom == StartBroom.option_swap:
            if self.options.postgame_mode == PostgameMode.option_progressive:
                # This is kind of an odd combination of options tbh.
                start_broom_item = Items.Inventory.Progressive_Swap.item
            else:
                start_broom_item = Items.Inventory.Swap.item

        if start_broom_item is not None:
            self.multiworld.push_precollected(self.create_item(start_broom_item.full_name))
            prevent_autoplacement.append(start_broom_item)

        if health_cicada_shuffle != HealthCicadaShuffle.option_vanilla:
            health_cicada_amount = len([location for location in Locations.all_locations if location.health_cicada])
            placed_items += health_cicada_amount
            item_name = Items.Cicada.Health_Cicada.item.full_name

            if health_cicada_shuffle == HealthCicadaShuffle.option_own_world:
                local_item_pool.add(item_name)
            elif health_cicada_shuffle == HealthCicadaShuffle.option_different_world:
                non_local_item_pool.add(item_name)

            for _ in range(health_cicada_amount):
                item_pool.append(self.create_item(item_name))

        if big_key_shuffle not in [BigKeyShuffle.option_vanilla, BigKeyShuffle.option_unlocked]:
            placed_items += len(Items.BigKey.all())

            for big_key in Items.BigKey.all():
                item_pool.append(self.create_item(big_key.full_name))

                if big_key_shuffle == BigKeyShuffle.option_own_world:
                    local_item_pool.add(big_key.full_name)
                elif big_key_shuffle == BigKeyShuffle.option_different_world:
                    non_local_item_pool.add(big_key.full_name)

        if self.options.red_grotto_access != RedCaveAccess.option_vanilla:
            placed_items += 3

            pool: List[Item] = item_pool
            if self.options.red_grotto_access == RedCaveAccess.option_original_dungeon:
                pool = self.dungeon_items.setdefault(Red_Cave, [])

            for _ in range(3):
                pool.append(self.create_item(Items.RedCaveUnlock.names()[0]))

        if not self.options.split_windmill:
            prevent_autoplacement.extend(Items.StatueUnlocks.all())

        if not self.options.include_blue_happy:
            prevent_autoplacement.extend(Items.Dam.all())

        if self.options.postgame_mode == PostgameMode.option_disabled:
            prevent_autoplacement.extend(Items.postgame_cards)

        if self.options.postgame_mode == PostgameMode.option_progressive:
            prog_swap = Items.Inventory.Progressive_Swap.item
            item_pool.append(self.create_item(prog_swap.full_name))
            placed_items += 1

            if start_broom != StartBroom.option_swap:
                item_pool.append(self.create_item(prog_swap.full_name))
                placed_items += 1

            prevent_autoplacement.append(Items.Inventory.Swap.item)

        if self.options.nexus_gate_shuffle != NexusGateShuffle.option_off:
            nexus_gate_items = [Items.Nexus.GATE[loc.region.__class__] for loc in Locations.nexus_pad_locations
                                if loc.region.__class__ in self.shuffled_gates]
            item_pool.extend(self.create_item(item.full_name) for item in nexus_gate_items)
            placed_items += len(nexus_gate_items)

        excluded_items = {item.full_name for item in prevent_autoplacement}

        for name in Items.all_items:
            if name not in excluded_items:
                placed_items += 1
                item_pool.append(self.create_item(name))

        max_cards = self.location_count - placed_items
        card_gates_in_logic = [cls for cls in gatereq_classes
                               if cls.typeoption(self.options) == GateType.CARDS and
                               (
                                       self.options.postgame_mode != PostgameMode.option_disabled
                                       or cls.GateCardReq.default <= 36)]
        requested_cards = max((cls.cardoption(self.options) for cls in card_gates_in_logic), default=0)
        if self.options.extra_cards > max_cards:
            # make sure extra cards can't overflow the game's card list
            self.options.extra_cards.value = max_cards
        if self.options.card_amount == CardAmount.option_vanilla:
            self.options.card_amount.value = 37 if self.options.postgame_mode == PostgameMode.option_disabled else 49
        elif self.options.card_amount == CardAmount.option_auto:
            self.options.card_amount.value = int(requested_cards)
        if self.options.card_amount + self.options.extra_cards > max_cards:
            self.options.card_amount.value = max_cards - self.options.extra_cards

        for cls in card_gates_in_logic:
            if cls.cardoption(self.options) > self.options.card_amount:
                cls.cardoption(self.options).value = self.options.card_amount.value

        for card in Items.Card.all()[:self.options.card_amount + self.options.extra_cards]:
            placed_items += 1
            item_pool.append(self.create_item(card.full_name))

        # If we have space for filler, prioritize adding in the ??? items that would be in-logic. Also add traps,
        # if enabled.
        if placed_items < self.location_count:
            new_items = []

            remaining_items = self.location_count - placed_items
            num_traps = int(self.options.traps_percentage / 100 * remaining_items)
            remaining_items -= num_traps

            for i in range(num_traps):
                new_items.append(self.random.choice(Items.Trap.all()))

            secret_items = Items.early_secret_items if self.options.postgame_mode == PostgameMode.option_disabled \
                else Items.Secret.all()

            if self.options.postgame_mode == PostgameMode.option_disabled and self.options.fields_secret_paths:
                secret_items = [*secret_items, *Items.secret_items_secret_paths]

            if len(secret_items) <= remaining_items:
                new_items.extend(secret_items)
            else:
                new_items.extend(self.random.sample(secret_items, remaining_items))

            item_pool.extend(self.create_item(item.full_name) for item in new_items)
            placed_items += len(new_items)

        # If there's any space left after that, fill the slots with random filler.
        if placed_items < self.location_count:
            item_pool.extend(self.create_filler() for _ in range(self.location_count - placed_items))

        self.multiworld.itempool += item_pool

        self.options.local_items.value |= local_item_pool
        self.options.non_local_items.value |= non_local_item_pool

    def create_regions(self) -> None:
        include_health_cicadas = self.options.health_cicada_shuffle
        include_big_keys = self.options.big_key_shuffle
        include_postgame: bool = (self.options.postgame_mode != PostgameMode.option_disabled)
        dustsanity: bool = bool(self.options.dustsanity.value)

        postgame_regions = Regions.postgame_regions if self.options.fields_secret_paths.value else (
                Regions.postgame_regions + Regions.postgame_without_secret_paths)

        all_regions: Dict[RegionEnum, Region] = {}

        for region_data in (m for area in Regions.all_areas for m in area):
            if not include_postgame and region_data in postgame_regions:
                continue

            region = Region(str(region_data), self.player, self.multiworld)
            if region_data in Locations.locations_by_region:
                for location in Locations.locations_by_region[region_data]:
                    reqs: list[str] = location.reqs.copy()

                    if include_health_cicadas == HealthCicadaShuffle.option_vanilla and location.health_cicada:
                        continue

                    if include_big_keys == BigKeyShuffle.option_vanilla and location.big_key:
                        continue

                    if self.options.red_grotto_access == RedCaveAccess.option_vanilla and location.tentacle:
                        continue

                    if (not self.options.split_windmill and location.region.area_name() == Windmill.area_name()
                            and location.base_name == "Activation"):
                        continue

                    if not include_postgame and location.postgame(bool(self.options.fields_secret_paths.value)):
                        continue

                    if (not self.options.forest_bunny_chest and location.region.area_name() == Forest.area_name()
                            and location.base_name == "Bunny Chest"):
                        continue

                    if (not self.options.include_blue_happy and location.region.__class__
                            in [Blue, Happy] and location.base_name == "Completion Reward"):
                        continue

                    if self.options.victory_condition == VictoryCondition.option_defeat_briar \
                            and location.base_name == "Defeat Briar":
                        continue

                    if location.nexus_gate and location.region.__class__ not in self.shuffled_gates:
                        continue

                    if location.dust:
                        if dustsanity:
                            reqs.append("Combat")
                        else:
                            continue

                    location_id = Constants.location_name_to_id[location.name]

                    new_location = AnodyneLocation(self.player, location.name, location_id, region)
                    new_location.access_rule = Constants.get_access_rule(reqs, str(location.region), self)
                    region.locations.append(new_location)

                    self.location_count += 1

            all_regions[region_data] = region

        for exit_vals in (
                Exits.all_exits if not self.options.fields_secret_paths.value
                else Exits.all_exits + Exits.secret_path_connections):
            exit1: RegionEnum = exit_vals[0]
            exit2: RegionEnum = exit_vals[1]
            requirements: list[str] = exit_vals[2]

            if not include_postgame and (
                    exit1 in postgame_regions or exit2 in postgame_regions
                    or f"{Items.Inventory.Progressive_Swap.item.full_name}:2" in requirements):
                continue

            r1 = all_regions[exit1]
            r2 = all_regions[exit2]

            e = r1.create_exit(f"{exit1} to {exit2} exit")
            e.connect(r2)
            e.access_rule = Constants.get_access_rule(requirements, str(exit1), self)

        for region in self.gates_unlocked:
            all_regions[Nexus.bottom].create_exit(f"{region.area_name()} Nexus Gate").connect(all_regions[{
                location.region.__class__: location.region for location in Locations.nexus_pad_locations}[region]])

        if self.options.nexus_gate_shuffle != NexusGateShuffle.option_off:
            for location in Locations.nexus_pad_locations:
                if location.region.__class__ in self.shuffled_gates:
                    e = all_regions[Nexus.bottom].create_exit(f"{location.region.area_name()} Nexus Gate")
                    e.connect(all_regions[location.region])
                    e.access_rule = Constants.get_access_rule([Items.Nexus.GATE[location.region.__class__].full_name],
                                                              "Nexus bottom", self)

        for event in Events.all_events:
            if not event.is_active(self.options):
                continue

            if self.using_ut and bool(self.multiworld.__getattribute__("enforce_deferred_connections")):
                event_region = Region(f"Event Region: {event.name}",self.player,self.multiworld)
                entry = all_regions[event.region].create_exit(f"Get event: {event.name}")
                entry.access_rule = Constants.get_access_rule(event.reqs,str(event.region),self)
                entry.connect(event_region)

                self.create_event(event_region, event.name, self.ut_event_check(event))

                self.multiworld.regions.append(event_region)
            else:
                self.create_event(all_regions[event.region], event.name, Constants.get_access_rule(event.reqs,
                                                                                         str(event.region), self))

        self.multiworld.regions += all_regions.values()

        if Constants.debug_mode:
            from Utils import visualize_regions

            visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    def ut_event_check(self, event:EventData):
        return lambda _: event.flag in self.tracked_events

    def reconnect_found_entrances(self, key:str, value:Any):
        if key.endswith("EventMap") and isinstance(value,int):
            self.tracked_events = EventFlags(value)

    def create_gate_proxy_rule(self, cls: typing.Type[GateRequirements]):
        rules = []

        gatetype = cls.typeoption(self.options)
        if gatetype == GateType.CARDS:
            rules = [f"Cards:{cls.cardoption(self.options)}"]
        elif gatetype == GateType.BOSSES:
            rules = [f"Bosses:{cls.bossoption(self.options)}"]
        elif gatetype == GateType.UNLOCKED:
            pass
        else:
            rules = [f"{GateType(gatetype).name.title()} Key"]

        self.proxy_rules[cls.typename()] = rules

    def set_rules(self) -> None:
        if not self.options.split_windmill:
            for statue in Items.StatueUnlocks.all():
                self.proxy_rules[statue.full_name] = ["Windmill activated"]

        if self.options.big_key_shuffle == BigKeyShuffle.option_unlocked:
            for big_key in Items.BigKey.all():
                self.proxy_rules[big_key.full_name] = []
        elif self.options.big_key_shuffle == BigKeyShuffle.option_vanilla:
            for big_key in Items.BigKey.all():
                self.proxy_rules[big_key.full_name] = [f"Grab {big_key.full_name}"]

        if self.options.small_key_mode == SmallKeyMode.option_unlocked:
            for dungeon, amount in Constants.small_key_count.items():
                for i in range(amount):
                    self.proxy_rules[f"{Items.Keys.Small_Key[dungeon].full_name}:{i + 1}"] = []
        elif self.options.small_key_mode == SmallKeyMode.option_key_rings:
            for dungeon, amount in Constants.small_key_count.items():
                for i in range(amount):
                    self.proxy_rules[f"{Items.Keys.Small_Key[dungeon].full_name}:{i + 1}"] = [
                        Items.Keys.Key_Ring[dungeon].full_name]
        elif (self.options.small_key_mode == SmallKeyMode.option_small_keys
              and self.options.small_key_shuffle == SmallKeyShuffle.option_vanilla):
            # For vanilla key placement, the regular rules don't quite match up in this dungeon,
            # but the dungeon is still solvable
            for i in range(Constants.small_key_count[Hotel]):
                self.proxy_rules[f"{Items.Keys.Small_Key[Hotel].full_name}:{i + 1}"] = []

        if self.options.red_grotto_access == RedCaveAccess.option_vanilla:
            self.proxy_rules["RedCave-Left"] = ["Center left tentacle hit"]
            self.proxy_rules["RedCave-Right"] = ["Center right tentacle hit"]
            self.proxy_rules["RedCave-Top"] = ["Left tentacle hit", "Right tentacle hit"]
        else:
            item = Items.RedCaveUnlock.names()[0]
            self.proxy_rules["RedCave-Left"] = [item]
            self.proxy_rules["RedCave-Right"] = [f"{item}:2"]
            self.proxy_rules["RedCave-Top"] = [f"{item}:3"]

        if self.options.randomize_color_puzzle:
            self.proxy_rules["GO Color Puzzle"] = ["Defeat Servants", "Defeat Watcher", "Defeat Manager"]
        else:
            self.proxy_rules["GO Color Puzzle"] = []

        if self.options.include_blue_happy:
            self.proxy_rules["Complete Blue"] = [Items.Dam.DAM[Blue].full_name]
            self.proxy_rules["Complete Happy"] = [Items.Dam.DAM[Happy].full_name]
            self.proxy_rules["Happy Open"] = []
        else:
            self.proxy_rules["Complete Blue"] = ["Blue Completion"]
            self.proxy_rules["Complete Happy"] = ["Happy Completion"]
            self.proxy_rules["Happy Open"] = ["Blue Completion"]

        if self.options.postgame_mode != PostgameMode.option_progressive:
            prog_swap = Items.Inventory.Progressive_Swap.item.full_name
            swap = Items.Inventory.Swap.item.full_name
            self.proxy_rules[f"{prog_swap}:1"] = [swap]

            if self.options.postgame_mode == PostgameMode.option_vanilla:
                self.proxy_rules[f"{prog_swap}:2"] = [swap, "Defeat Briar"]
            elif self.options.postgame_mode == PostgameMode.option_unlocked:
                self.proxy_rules[f"{prog_swap}:2"] = [swap]
            else:
                self.proxy_rules[f"{prog_swap}:2"] = [
                    "Impossible"]  # Shouldn't ever be asked for, but gives nice errors if it does

        for cls in gatereq_classes:
            self.create_gate_proxy_rule(cls)

        if self.options.fields_secret_paths.value:
            self.proxy_rules["SwapOrSecret"] = []
        else:
            self.proxy_rules["SwapOrSecret"] = [f"{Items.Inventory.Progressive_Swap.item.full_name}:2"]

        if self.options.nexus_gate_shuffle or \
                any(region in self.gates_unlocked for region in Regions.post_temple_boss_nexus_gates) and \
                self.options.small_key_shuffle != SmallKeyShuffle.option_vanilla:
            # There is one keyblock in Temple of the Seeing One that has conditional logic based on whether it is
            # possible for the player to access the exit of the dungeon early.
            self.proxy_rules["Temple Boss Access"] = [f"{Items.Keys.Small_Key[Bedroom].full_name}:3"]
        else:
            self.proxy_rules["Temple Boss Access"] = [f"{Items.Keys.Small_Key[Bedroom].full_name}:2"]

        victory_condition: VictoryCondition = self.options.victory_condition
        requirements: list[str] = []

        if victory_condition == VictoryCondition.option_defeat_briar:
            requirements.append("Defeat Briar")
        elif victory_condition == VictoryCondition.option_final_gate:
            requirements.append("Open final gate")

        self.multiworld.completion_condition[self.player] = (
            Constants.get_access_rule(requirements, "Event", self))

        if not self.using_ut:
            self.test_gate_requirements()

    def test_gate_requirements(self):
        state = CollectionState(self.multiworld)
        # This function runs before start_inventory gets put in precollected, so need to put them there ourselves
        for item, amount in self.options.start_inventory:
            for _ in range(amount):
                state.collect(self.create_item(item), True)
        state.sweep_for_advancements(self.multiworld.get_locations(self.player))

        # Counter to keep track of how much extra progression items we've placed
        placed_progression = 0

        def finished():
            return self.multiworld.has_beaten_game(state, self.player) and all(
                loc.can_reach(state) for loc in self.multiworld.get_locations(self.player))

        def sort_key(req: AnodyneWorld.LogicRequirement):
            # Reverse order for sorting lexicographically
            return (
                req.is_big_key_locked(),  # Will only ever be true if big keys are fixed events
                req.needed_bosses(),
                req.unlockable_by_num_items(state),
                req.needed_cards(),
                req.name  # Name to ensure unique and consistent sort order across seeds
            )

        gate_max_cards: Dict[Type[GateRequirements], int] = defaultdict(lambda: 49)

        while not finished():
            max_placeable = len(self.multiworld.get_placeable_locations(state, self.player)) - placed_progression

            # Sorting on location and entrance name to have consistent sorting
            requirements = self.get_blocking_rules(state)
            for gate in (gate for r in requirements for gate in r.gates if r.is_gate_locked()):
                gate_max_cards[gate] = min(gate_max_cards[gate],
                                           max_placeable + state.count_group("Cards", self.player))

            requirements.sort(key=sort_key)
            to_fulfill = requirements[0]

            if to_fulfill.is_unlockable_by_items() and to_fulfill.unlockable_by_num_items(state) <= max_placeable:
                logging.debug(f"{len(requirements)},{to_fulfill.unlockable_by_num_items(state)},"
                              f"{to_fulfill._unlock_dict(state)}")
            else:
                unlockable_gates = [r for r in requirements if
                                    r.is_gate_locked() and r.unlockable_by_num_items(state) - r.remaining_cards(
                                        state) <= max_placeable]
                if len(unlockable_gates) == 0:
                    logging.error("No gate to adjust and ran out of locations to put progression!")
                    return
                to_fulfill = unlockable_gates[0]

            if to_fulfill.gates:
                max_cards = (max_placeable - to_fulfill.unlockable_by_num_items(state) +
                             to_fulfill.remaining_cards(state) + state.count_group("Cards", self.player))
                if self.options.accessibility == Accessibility.option_minimal:
                    # Minimal can get itself very easily stuck behind card gates
                    max_cards = min(gate_max_cards[gate] for gate in to_fulfill.gates)
                max_bosses = state.count_from_list(Constants.groups["Bosses"], self.player)
                for cls in to_fulfill.gates:
                    if cls.typeoption(self.options) == GateType.BOSSES:
                        logging.warning(
                            f"Player {self.player_name} requested impossible gate. "
                            f"Adjusting {cls.typename()} down to {max_bosses} Bosses")
                        cls.bossoption(self.options).value = max_bosses
                    elif cls.typeoption(self.options) == GateType.CARDS:
                        opt = cls.cardoption(self.options)
                        if opt.value > max_cards:
                            logging.warning(
                                f"Player {self.player_name} requested impossible gate. "
                                f"Adjusting {cls.typename()} down to {max_cards} Cards")
                        opt.value = min(opt.value, max_cards)
                    else:
                        logging.warning(
                            f"Player {self.player} requested self-locking big key gate. Opening up {cls.typename()}")
                        cls.typeoption(self.options).value = GateType.UNLOCKED
                    self.create_gate_proxy_rule(cls)  # Actually change the rule
                    state.stale[self.player] = True

            placed_progression += to_fulfill.unlockable_by_num_items(state)
            to_fulfill.collect(state)

            state.sweep_for_advancements(self.multiworld.get_locations(self.player))

    class LogicRequirement:
        def __init__(self, reqs: Iterable[str], world: "AnodyneWorld", name: str):
            self.requirements: Dict[str, int] = defaultdict(int)
            self.gates: Set[Type[GateRequirements]] = set()
            self.world = world
            self.name = name
            for item in reqs:
                if item in gate_lookup:
                    self.gates.add(gate_lookup[item])
                    continue
                count = 1
                if ':' in item:
                    item, count = item.split(':')
                    count = int(count)
                if self.requirements[item] < count:
                    self.requirements[item] = count

        def is_event_locked(self):
            return any(req in Events.all_event_names for req in self.requirements)

        def is_gate_locked(self):
            return len(self.gates) > 0

        def is_big_key_locked(self):
            return any(cls.typeoption(self.world.options) in [GateType.BLUE, GateType.RED, GateType.GREEN] for cls in
                       self.gates)

        def is_unlockable_by_items(self):
            return not self.is_event_locked() and all(
                cls.typeoption(self.world.options) != GateType.BOSSES for cls in self.gates)

        def needed_bosses(self):
            return max([0, *[cls.bossoption(self.world.options) for cls in self.gates if
                             cls.typeoption(self.world.options) == GateType.BOSSES]])

        def needed_cards(self):
            return max([0, *[cls.cardoption(self.world.options) for cls in self.gates if
                             cls.typeoption(self.world.options) == GateType.CARDS]])

        def remaining_cards(self, state: CollectionState):
            return max(0, self.needed_cards() - state.count_group("Cards", self.world.player))

        def _unlock_dict(self, state: CollectionState):
            ret: Dict[str, int] = {}
            for item, amount in self.requirements.items():
                ret[item] = max(0, amount - state.count(item, self.world.player))
            for card in itertools.islice((c for c in Items.Card.names() if not state.has(c, self.world.player)),
                                         self.remaining_cards(state)):
                ret[card] = 1
            return ret

        def unlockable_by_num_items(self, state: CollectionState):
            return sum(self._unlock_dict(state).values())

        def collect(self, state: CollectionState):
            for item in itertools.chain.from_iterable(
                    itertools.repeat(i, n) for i, n in self._unlock_dict(state).items()):
                state.collect(self.world.create_item(item), True)

    def get_blocking_rules(self, state: CollectionState):
        blocked_rules: List[Tuple[AccessRule, str]] = [(loc.access_rule, loc.name) for region in
                                                       state.reachable_regions[self.player] for loc in
                                                       region.locations if not loc.access_rule(state)]
        # All our rules are of type AccessRule
        # noinspection PyTypeChecker
        blocked_rules.extend((e.access_rule, e.name) for e in state.blocked_connections[self.player])

        gate_types = [GateType.CARDS, GateType.BOSSES]
        if self.options.big_key_shuffle == BigKeyShuffle.option_vanilla:
            gate_types.extend([GateType.BLUE, GateType.RED, GateType.GREEN])

        def reqs(r: str) -> Iterable[str]:
            if r in self.proxy_rules and not (
                    r in gate_lookup and gate_lookup[r].typeoption(self.options) in gate_types):
                return itertools.chain(*[reqs(sub_r) for sub_r in self.proxy_rules[r]])
            elif not Constants.check_access(state, self, r, "blocking_check"):
                if r in Constants.groups:
                    # If it's a group, return any of them(mostly used for the Combat group)
                    return [Constants.groups[r][0]]
                else:
                    return [r]
            return []

        requirements = [
            AnodyneWorld.LogicRequirement(itertools.chain.from_iterable(reqs(r) for r in rule.reqs), self, name) for
            (rule, name) in blocked_rules]

        return [r for r in requirements if not r.is_event_locked()]

    def get_filler_item_name(self) -> str:
        return self.random.choice(Items.Heal.names())

    def create_event(self, region: Region, event_name: str, access_rule: Callable[[CollectionState], bool]) -> None:
        loc = AnodyneLocation(self.player, event_name, None, region)
        loc.place_locked_item(self.create_event_item(event_name))
        loc.access_rule = access_rule
        region.locations.append(loc)

    def create_event_item(self, name: str) -> Item:
        item = self.create_item(name)
        item.classification = ItemClassification.progression
        return item

    def pre_fill(self):
        for dungeon, confined_dungeon_items in self.dungeon_items.items():
            if len(confined_dungeon_items) == 0:
                continue

            current_items = confined_dungeon_items.copy()
            confined_dungeon_items.clear()  # Prevent the current items from being picked up by all state


            # This will pick up all unplaced dungeon items as well
            collection_state = self.multiworld.get_all_state(allow_partial_entrances=True)

            confined_dungeon_items.extend(current_items)
            del current_items

            dungeon_location_names = [location.name
                                      for region in dungeon
                                      for location in Locations.locations_by_region.get(region, []) if
                                      not location.outside_of_dungeon]

            if dungeon == "Street" and self.options.small_key_shuffle == SmallKeyShuffle.option_original_dungeon and \
                    self.options.nexus_gates_open == NexusGatesOpen.option_street_only and \
                    self.options.start_broom == StartBroom.option_none:
                # This is a degenerate case; we need to prevent pre-fill from putting the Street small key in the Broom
                # chest because if it does, there are no reachable locations at the start of the game.
                dungeon_location_names.remove(f"{Street.area_name()} - Broom Chest")

            dungeon_locations = [location for location in self.multiworld.get_unfilled_locations(self.player)
                                 if location.name in dungeon_location_names]

            for attempts_remaining in range(6, -1, -1):
                self.random.shuffle(dungeon_locations)
                items = confined_dungeon_items.copy()
                locations = dungeon_locations.copy()
                try:
                    fill_restrictive(self.multiworld, collection_state, locations, items,
                                     single_player_placement=True, lock=True)
                    if len(items) == 0:
                        break
                except FillError as exc:
                    if attempts_remaining == 0:
                        raise exc
                    logging.debug(f"Failed to shuffle dungeon items for player {self.player}. Retrying...")
                # Reset locations fill_restrictive tried setting but failed to complete
                for loc in dungeon_locations:
                    if loc.locked and loc.item is not None:
                        loc.locked = False
                        loc.item = None
            confined_dungeon_items.clear()

    def get_pre_fill_items(self) -> List["Item"]:
        return [item for dungeon_items in self.dungeon_items.values() for item in dungeon_items]

    def fill_slot_data(self):
        return {
            "death_link": bool(self.options.death_link.value),
            "small_keys": self.options.small_key_mode.current_key if
            self.options.small_key_mode != SmallKeyMode.option_small_keys else (
                "vanilla" if self.options.small_key_shuffle == SmallKeyShuffle.option_vanilla else "shuffled"),
            "small_key_mode": int(self.options.small_key_mode),
            "shuffle_small_keys": int(self.options.small_key_shuffle),

            "shuffle_big_gates": int(self.options.big_key_shuffle),
            "vanilla_health_cicadas": self.options.health_cicada_shuffle == HealthCicadaShuffle.option_vanilla,
            "nexus_gates_unlocked": [gate.area_id() for gate in self.gates_unlocked],
            "vanilla_red_cave": self.options.red_grotto_access == RedCaveAccess.option_vanilla,
            "split_windmill": bool(self.options.split_windmill),
            "postgame_mode": int(self.options.postgame_mode),
            "nexus_gate_shuffle": int(self.options.nexus_gate_shuffle),
            "victory_condition": int(self.options.victory_condition),
            "forest_bunny_chest": bool(self.options.forest_bunny_chest.value),
            "dustsanity": bool(self.options.dustsanity),
            "seed": self.random.randint(0, 1000000),
            "card_amount": self.options.card_amount + self.options.extra_cards,
            "fields_secret_paths": bool(self.options.fields_secret_paths),
            "shop_items": [dataclasses.asdict(item) for item in self.get_shop_items()],
            "randomize_color_puzzle": bool(self.options.randomize_color_puzzle),
            "mitra_hints": [dataclasses.asdict(hint) for hint in
                            self.get_mitra_hints(0 if self.options.mitra_hints == MitraHints.option_none else 8 + 1)],
            "mitra_hint_type": int(self.options.mitra_hints),
            "include_blue_happy": bool(self.options.include_blue_happy),
            "version": self.version,
            **{c.typename(): c.shorthand(self.options) for c in gatereq_classes}
        }

    @dataclass
    class ShopItem:
        player: int = -1
        item: int = -1

    @dataclass
    class ItemHint:
        item: int = -1
        location: int = -1
        location_player: int = -1

    def get_shop_items(self) -> List[ShopItem]:
        # Do not change shop items if playing solo
        if self.multiworld.players == 1:
            return []
        elif sum(i.classification == ItemClassification.progression and i.player != self.player
                 for i in self.multiworld.itempool) >= 3:
            items = self.random.sample(
                [item for item in self.multiworld.itempool if
                 item.classification == ItemClassification.progression
                 and item.player != self.player],
                3)
            return [AnodyneWorld.ShopItem(item.player, item.code) for item in items]
        else:
            return []

    def get_mitra_hints(self, count: int) -> List[ItemHint]:
        possible_items = [item for item in self.multiworld.itempool if
                          item.classification == ItemClassification.progression
                          and item.player == self.player and item.location is not None]
        items = self.random.sample(
            possible_items,
            min(count, len(possible_items)))

        hints: List[AnodyneWorld.ItemHint] = []

        for item in items:
            location = self.multiworld.find_item(item.name, self.player)
            hints.append(AnodyneWorld.ItemHint(item.code, location.address, location.player))

        return hints

    # for the universal tracker, doesn't get called in standard gen
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        return slot_data
