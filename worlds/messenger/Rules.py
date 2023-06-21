from typing import Dict, Callable, TYPE_CHECKING

from BaseClasses import CollectionState, MultiWorld
from worlds.generic.Rules import set_rule, allow_self_locking_items, add_rule
from .Options import MessengerAccessibility, Goal
from .Constants import NOTES, PHOBEKINS
from .SubClasses import MessengerShopLocation

if TYPE_CHECKING:
    from . import MessengerWorld
else:
    MessengerWorld = object


class MessengerRules:
    player: int
    world: MessengerWorld
    region_rules: Dict[str, Callable[[CollectionState], bool]]
    location_rules: Dict[str, Callable[[CollectionState], bool]]

    def __init__(self, world: MessengerWorld) -> None:
        self.player = world.player
        self.world = world

        self.region_rules = {
            "Ninja Village": self.has_wingsuit,
            "Autumn Hills": self.has_wingsuit,
            "Catacombs": self.has_wingsuit,
            "Bamboo Creek": self.has_wingsuit,
            "Searing Crags Upper": self.has_vertical,
            "Cloud Ruins": lambda state: self.has_vertical(state) and state.has("Ruxxtin's Amulet", self.player),
            "Cloud Ruins Right": lambda state: self.has_wingsuit(state) and
                                               (self.has_dart(state) or self.can_dboost(state)),
            "Underworld": self.has_tabi,
            "Riviere Turquoise": lambda state: self.has_dart(state) or
                                               (self.has_wingsuit(state) and self.can_destroy_projectiles(state)),
            "Forlorn Temple": lambda state: state.has_all({"Wingsuit", *PHOBEKINS}, self.player) and self.can_dboost(state),
            "Glacial Peak": self.has_vertical,
            "Elemental Skylands": lambda state: state.has("Magic Firefly", self.player) and self.has_wingsuit(state),
            "Music Box": lambda state: state.has_all(set(NOTES), self.player) and self.has_dart(state),
        }

        self.location_rules = {
            # ninja village
            "Ninja Village Seal - Tree House": self.has_dart,
            # autumn hills
            "Autumn Hills - Key of Hope": self.has_dart,
            "Autumn Hills Seal - Spike Ball Darts": self.is_aerobatic,
            # bamboo creek
            "Bamboo Creek - Claustro": lambda state: self.has_dart(state) or self.can_dboost(state),
            # howling grotto
            "Howling Grotto Seal - Windy Saws and Balls": self.has_wingsuit,
            "Howling Grotto Seal - Crushing Pits": lambda state: self.has_wingsuit(state) and self.has_dart(state),
            "Howling Grotto - Emerald Golem": self.has_wingsuit,
            # searing crags
            "Searing Crags Seal - Triple Ball Spinner": self.has_vertical,
            "Searing Crags - Astral Tea Leaves":
                lambda state: state.can_reach("Ninja Village - Astral Seed", "Location", self.player),
            "Searing Crags - Key of Strength": lambda state: state.has("Power Thistle", self.player),
            # glacial peak
            "Glacial Peak Seal - Ice Climbers": self.has_dart,
            "Glacial Peak Seal - Projectile Spike Pit": self.can_destroy_projectiles,
            # cloud ruins
            "Cloud Ruins Seal - Ghost Pit": self.has_dart,
            # tower of time
            "Tower of Time Seal - Time Waster": self.has_dart,
            "Tower of Time Seal - Lantern Climb": lambda state: self.has_wingsuit(state) and self.has_dart(state),
            "Tower of Time Seal - Arcane Orbs": lambda state: self.has_wingsuit(state) and self.has_dart(state),
            # underworld
            "Underworld Seal - Sharp and Windy Climb": self.has_wingsuit,
            "Underworld Seal - Fireball Wave": self.is_aerobatic,
            "Underworld Seal - Rising Fanta": self.has_dart,
            # sunken shrine
            "Sunken Shrine - Sun Crest": self.has_tabi,
            "Sunken Shrine - Moon Crest": self.has_tabi,
            "Sunken Shrine - Key of Love": lambda state: state.has_all({"Sun Crest", "Moon Crest"}, self.player),
            "Sunken Shrine Seal - Waterfall Paradise": self.has_tabi,
            "Sunken Shrine Seal - Tabi Gauntlet": self.has_tabi,
            "Mega Shard of the Moon": self.has_tabi,
            "Mega Shard of the Sun": self.has_tabi,
            # riviere turquoise
            "Riviere Turquoise Seal - Bounces and Balls": self.can_dboost,
            "Riviere Turquoise Seal - Launch of Faith": lambda state: self.can_dboost(state) or self.has_dart(state),
            # elemental skylands
            "Elemental Skylands - Key of Symbiosis": self.has_dart,
            "Elemental Skylands Seal - Air": self.has_wingsuit,
            "Elemental Skylands Seal - Water": lambda state: self.has_dart(state) and
                                                             state.has("Currents Master", self.player),
            "Elemental Skylands Seal - Fire": lambda state: self.has_dart(state) and self.can_destroy_projectiles(state),
            "Earth Mega Shard": self.has_dart,
            "Water Mega Shard": self.has_dart,
            # corrupted future
            "Corrupted Future - Key of Courage": lambda state: state.has_all({"Demon King Crown", "Magic Firefly"},
                                                                             self.player),
            # the shop
            "Shop Chest": self.has_enough_seals,
            # tower hq
            "Money Wrench": self.can_shop,
        }

    def has_wingsuit(self, state: CollectionState) -> bool:
        return state.has("Wingsuit", self.player)

    def has_dart(self, state: CollectionState) -> bool:
        return state.has("Rope Dart", self.player)

    def has_tabi(self, state: CollectionState) -> bool:
        return state.has("Lightfoot Tabi", self.player)

    def has_vertical(self, state: CollectionState) -> bool:
        return self.has_wingsuit(state) or self.has_dart(state)

    def has_enough_seals(self, state: CollectionState) -> bool:
        return not self.world.required_seals or state.has("Power Seal", self.player, self.world.required_seals)

    def can_destroy_projectiles(self, state: CollectionState) -> bool:
        return state.has("Strike of the Ninja", self.player)

    def can_dboost(self, state: CollectionState) -> bool:
        return state.has_any({"Path of Resilience", "Meditation"}, self.player) and \
            state.has("Second Wind", self.player)
    
    def is_aerobatic(self, state: CollectionState) -> bool:
        return self.has_wingsuit(state) and state.has("Aerobatics Warrior", self.player)

    def true(self, state: CollectionState) -> bool:
        """I know this is stupid, but it's easier to read in the dicts."""
        return True

    def can_shop(self, state: CollectionState) -> bool:
        prices = self.world.shop_prices
        most_expensive_loc = max(prices, key=prices.get)
        return state.can_reach(f"The Shop - {most_expensive_loc}", "Location", self.player)

    def set_messenger_rules(self) -> None:
        multiworld = self.world.multiworld

        for region in multiworld.get_regions(self.player):
            if region.name in self.region_rules:
                for entrance in region.entrances:
                    entrance.access_rule = self.region_rules[region.name]
            for loc in region.locations:
                if loc.name in self.location_rules:
                    loc.access_rule = self.location_rules[loc.name]
            if region.name == "The Shop":
                for loc in [location for location in region.locations if isinstance(location, MessengerShopLocation)]:
                    loc.access_rule = loc.can_afford
        if multiworld.goal[self.player] == Goal.option_power_seal_hunt:
            set_rule(multiworld.get_entrance("Tower HQ -> Music Box", self.player),
                     lambda state: state.has("Shop Chest", self.player))

        multiworld.completion_condition[self.player] = lambda state: state.has("Rescue Phantom", self.player)
        if multiworld.accessibility[self.player] > MessengerAccessibility.option_locations:
            set_self_locking_items(multiworld, self.player)


class MessengerHardRules(MessengerRules):
    extra_rules: Dict[str, Callable[[CollectionState], bool]]

    def __init__(self, world: MessengerWorld) -> None:
        super().__init__(world)

        self.region_rules.update({
            "Ninja Village": self.has_vertical,
            "Autumn Hills": self.has_vertical,
            "Catacombs": self.has_vertical,
            "Bamboo Creek": self.has_vertical,
            "Riviere Turquoise": self.true,
            "Forlorn Temple": lambda state: self.has_vertical(state) and state.has_all(set(PHOBEKINS), self.player),
            "Searing Crags Upper": lambda state: self.can_destroy_projectiles(state) or self.has_windmill(state)
                                                 or self.has_vertical(state),
            "Glacial Peak": lambda state: self.can_destroy_projectiles(state) or self.has_windmill(state)
                                          or self.has_vertical(state),
            "Elemental Skylands": lambda state: state.has("Magic Firefly", self.player) or
                                                self.has_windmill(state) or
                                                self.has_dart(state),
        })

        self.location_rules.update({
            "Howling Grotto Seal - Windy Saws and Balls": self.true,
            "Searing Crags Seal - Triple Ball Spinner": self.true,
            "Searing Crags Seal - Raining Rocks": lambda state: self.has_vertical(state) or self.can_destroy_projectiles(state),
            "Searing Crags Seal - Rhythm Rocks": lambda state: self.has_vertical(state) or self.can_destroy_projectiles(state),
            "Searing Crags - Power Thistle": lambda state: self.has_vertical(state) or self.can_destroy_projectiles(state),
            "Glacial Peak Seal - Ice Climbers": self.has_vertical,
            "Glacial Peak Seal - Projectile Spike Pit": self.true,
            "Cloud Ruins Seal - Ghost Pit": self.true,
            "Bamboo Creek - Claustro": self.has_wingsuit,
            "Tower of Time Seal - Lantern Climb": self.has_wingsuit,
            "Elemental Skylands Seal - Water": lambda state: self.has_dart(state) or self.can_dboost(state)
                                                             or self.has_windmill(state),
            "Elemental Skylands Seal - Fire": lambda state: (self.has_dart(state) or self.can_dboost(state)
                                                             or self.has_windmill(state)) and
                                                            self.can_destroy_projectiles(state),
            "Earth Mega Shard": lambda state: self.has_dart(state) or self.can_dboost(state) or self.has_windmill(state),
            "Water Mega Shard": lambda state: self.has_dart(state) or self.can_dboost(state) or self.has_windmill(state),
        })

        self.extra_rules = {
            "Searing Crags - Key of Strength": lambda state: self.has_dart(state) or self.has_windmill(state),
            "Elemental Skylands - Key of Symbiosis": lambda state: self.has_windmill(state) or self.can_dboost(state),
            "Autumn Hills Seal - Spike Ball Darts": lambda state: (self.has_dart(state) and self.has_windmill(state))
                                                                  or self.has_wingsuit(state),
            "Glacial Peak Seal - Glacial Air Swag": self.has_windmill,
            "Glacial Peak Seal - Ice Climbers": lambda state: self.has_wingsuit(state) or self.can_dboost(state),
            "Underworld Seal - Fireball Wave": lambda state: state.has_all({"Lightfoot Tabi", "Windmill Shuriken"},
                                                                           self.player),
        }

    def has_windmill(self, state: CollectionState) -> bool:
        return state.has("Windmill Shuriken", self.player)

    def set_messenger_rules(self) -> None:
        super().set_messenger_rules()
        for loc, rule in self.extra_rules.items():
            if not self.world.multiworld.shuffle_seals[self.player] and "Seal" in loc:
                continue
            if not self.world.multiworld.shuffle_shards[self.player] and "Shard" in loc:
                continue
            add_rule(self.world.multiworld.get_location(loc, self.player), rule, "or")


class MessengerOOBRules(MessengerRules):
    def __init__(self, world: MessengerWorld) -> None:
        self.world = world
        self.player = world.player

        self.region_rules = {
            "Elemental Skylands":
                lambda state: state.has_any({"Windmill Shuriken", "Wingsuit", "Rope Dart", "Magic Firefly"}, self.player),
            "Music Box": lambda state: state.has_all(set(NOTES), self.player)
        }

        self.location_rules = {
            "Bamboo Creek - Claustro": self.has_wingsuit,
            "Searing Crags - Key of Strength": self.has_wingsuit,
            "Sunken Shrine - Key of Love": lambda state: state.has_all({"Sun Crest", "Moon Crest"}, self.player),
            "Searing Crags - Pyro": self.has_tabi,
            "Underworld - Key of Chaos": self.has_tabi,
            "Corrupted Future - Key of Courage":
                lambda state: state.has_all({"Demon King Crown", "Magic Firefly"}, self.player),
            "Autumn Hills Seal - Spike Ball Darts": self.has_dart,
            "Ninja Village Seal - Tree House": self.has_dart,
            "Underworld Seal - Fireball Wave": lambda state: state.has_any({"Wingsuit", "Windmill Shuriken"},
                                                                           self.player),
            "Tower of Time Seal - Time Waster": self.has_dart,
            "Shop Chest": self.has_enough_seals
        }

    def set_messenger_rules(self) -> None:
        super().set_messenger_rules()
        self.world.multiworld.completion_condition[self.player] = lambda state: True
        self.world.multiworld.accessibility[self.player].value = MessengerAccessibility.option_minimal


def set_self_locking_items(multiworld: MultiWorld, player: int) -> None:
    # do the ones for seal shuffle on and off first
    allow_self_locking_items(multiworld.get_location("Searing Crags - Key of Strength", player), "Power Thistle")
    allow_self_locking_items(multiworld.get_location("Sunken Shrine - Key of Love", player), "Sun Crest", "Moon Crest")
    allow_self_locking_items(multiworld.get_location("Corrupted Future - Key of Courage", player), "Demon King Crown")

    # add these locations when seals are shuffled
    if multiworld.shuffle_seals[player]:
        allow_self_locking_items(multiworld.get_location("Elemental Skylands Seal - Water", player), "Currents Master")
    # add these locations when seals and shards aren't shuffled
    elif not multiworld.shuffle_shards[player]:
        allow_self_locking_items(multiworld.get_region("Cloud Ruins Right", player), "Ruxxtin's Amulet")
        allow_self_locking_items(multiworld.get_region("Forlorn Temple", player), *PHOBEKINS)
