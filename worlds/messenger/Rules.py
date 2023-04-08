from typing import Dict, Callable, TYPE_CHECKING

from BaseClasses import CollectionState, MultiWorld
from worlds.generic.Rules import set_rule, allow_self_locking_items, add_rule
from .Options import MessengerAccessibility, Goal
from .Constants import NOTES, PHOBEKINS

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
            "Cloud Ruins Right": self.has_wingsuit,
            "Underworld": self.has_tabi,
            "Forlorn Temple": lambda state: state.has_all({"Wingsuit", *PHOBEKINS}, self.player),
            "Glacial Peak": self.has_vertical,
            "Elemental Skylands": lambda state: state.has("Magic Firefly", self.player),
            "Music Box": lambda state: state.has_all(set(NOTES), self.player) and self.has_vertical(state),
        }

        self.location_rules = {
            # ninja village
            "Ninja Village Seal - Tree House": self.has_dart,
            # autumn hills
            "Autumn Hills - Key of Hope": self.has_dart,
            # howling grotto
            "Howling Grotto Seal - Windy Saws and Balls": self.has_wingsuit,
            "Howling Grotto Seal - Crushing Pits": lambda state: self.has_wingsuit(state) and self.has_dart(state),
            "Howling Grotto - Emerald Golem": self.has_wingsuit,
            # searing crags
            "Searing Crags - Astral Tea Leaves": lambda state: state.can_reach("Ninja Village - Astral Seed", "Location", self.player),
            "Searing Crags - Key of Strength": lambda state: state.has("Power Thistle", self.player),
            # glacial peak
            "Glacial Peak Seal - Ice Climbers": self.has_dart,
            # tower of time
            "Tower of Time Seal - Time Waster Seal": self.has_dart,
            "Tower of Time Seal - Lantern Climb": self.has_wingsuit,
            "Tower of Time Seal - Arcane Orbs": lambda state: self.has_wingsuit(state) and self.has_dart(state),
            # underworld
            "Underworld Seal - Sharp and Windy Climb": self.has_wingsuit,
            "Underworld Seal - Fireball Wave": self.has_wingsuit,
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
            "Riviere Turquoise - Butterfly Matriarch": self.has_vertical,
            "Riviere Turquoise Seal - Bounces and Balls": self.can_dboost,
            "Riviere Turquoise Seal - Launch of Faith": self.can_dboost,
            "Riviere Turquoise Seal - Flower Power": self.has_vertical,
            "Quick Restock Mega Shard 1": self.has_vertical,
            "Quick Restock Mega Shard 2": self.has_vertical,
            # elemental skylands
            "Elemental Skylands - Key of Symbiosis": self.has_dart,
            "Elemental Skylands Seal - Air": self.has_wingsuit,
            "Elemental Skylands Seal - Water": lambda state: self.has_dart(state) and
                                                             state.has("Currents Master", self.player),
            "Elemental Skylands Seal - Fire": self.has_dart,
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
        return state.has_all({"Wingsuit", "Aerobatics Warrior"}, self.player)

    def has_dart(self, state: CollectionState) -> bool:
        return state.has("Rope Dart", self.player)

    def has_tabi(self, state: CollectionState) -> bool:
        return state.has("Lightfoot Tabi", self.player)

    def has_vertical(self, state: CollectionState) -> bool:
        return self.destroys_projectiles(state) and (self.has_wingsuit(state) or self.has_dart(state))

    def has_enough_seals(self, state: CollectionState) -> bool:
        return not self.world.required_seals or state.has("Power Seal", self.player, self.world.required_seals)

    def destroys_projectiles(self, state: CollectionState) -> bool:
        return state.has("Strike of the Ninja", self.player)

    def can_dboost(self, state: CollectionState) -> bool:
        return state.has_any({"Path of Resilience", "Meditation"}, self.player) and \
            state.has("Second Wind", self.player)

    def true(self, state: CollectionState) -> bool:
        """I know this is stupid, but it's easier to read in the dicts."""
        return True

    def can_shop(self, state: CollectionState) -> bool:
        prices = self.world.shop_prices
        most_expensive = 0
        loc = "Demon's Bane"
        for slot, price in prices.items():
            if price > most_expensive:
                most_expensive = price
                loc = slot
        return state.can_reach(f"The Shop - {loc}", "Location", self.player)

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
                from worlds.messenger.SubClasses import MessengerShopLocation
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
            "Forlorn Temple": lambda state: self.has_vertical(state) and state.has_all(set(PHOBEKINS), self.player),
            "Searing Crags Upper": self.true,
            "Glacial Peak": self.true,
            "Elemental Skylands": lambda state: state.has("Fairy Bottle", self.player) or self.has_windmill(state),
        })

        self.location_rules.update({
            "Howling Grotto Seal - Windy Saws and Balls": self.true,
            "Glacial Peak Seal - Projectile Spike Pit": self.true,
            "Bamboo Creek - Claustro": self.has_wingsuit,
            "Elemental Skylands Seal - Water": self.true,
            "Elemental Skylands Seal - Fire": self.true,
            "Earth Mega Shard": self.true,
            "Water Mega Shard": self.true,
        })

        self.extra_rules = {
            "Searing Crags - Key of Strength": lambda state: self.has_dart(state) or self.has_windmill(state),
            "Elemental Skylands - Key of Symbiosis": self.has_windmill,
            "Autumn Hills Seal - Spike Ball Darts": lambda state: (self.has_dart(state) and self.has_windmill(state))
                                                                  or self.has_wingsuit(state),
            "Glacial Peak Seal - Glacial Air Swag": self.has_windmill,
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


class MessengerChallengeRules(MessengerHardRules):
    def __init__(self, world: MessengerWorld) -> None:
        super().__init__(world)

        self.region_rules.update({
            "Forlorn Temple": lambda state: (self.has_vertical(state) and state.has_all(set(PHOBEKINS), self.player))
                                            or state.has_all({"Wingsuit", "Windmill Shuriken"}, self.player),
            "Elemental Skylands": lambda state: self.has_wingsuit(state) or state.has("Fairy Bottle", self.player)
                                                or self.has_windmill(state),
        })

        self.location_rules.update({
            "Riviere Turquoise - Magic Firefly": self.true,
            "Howling Grotto Seal - Crushing Pits": self.true,
            "Underworld Seal - Sharp and Windy Climb": self.true,
            "Riviere Turquoise Seal - Flower Power": self.true,
        })

        self.extra_rules.update({
            "Autumn Hills - Key of Hope": self.has_vertical,
            "Elemental Skylands - Key of Symbiosis": lambda state: self.has_vertical(state) or self.has_windmill(state),
        })


class MessengerOOBRules(MessengerRules):
    def __init__(self, world: MessengerWorld) -> None:
        self.world = world
        self.player = world.player

        self.region_rules = {
            "Elemental Skylands": lambda state: state.has_any({"Wingsuit", "Rope Dart", "Fairy Bottle"}, self.player),
            "Music Box": lambda state: state.has_all(set(NOTES), self.player),
        }

        self.location_rules = {
            "Bamboo Creek - Claustro": self.has_wingsuit,
            "Searing Crags - Key of Strength": lambda state: self.has_vertical(state)
                                                             or state.has("Power Thistle", self.player),
            "Sunken Shrine - Key of Love": lambda state: state.has_all({"Sun Crest", "Moon Crest"}, self.player),
            "Searing Crags - Pyro": self.has_tabi,
            "Underworld - Key of Chaos": self.has_tabi,
            "Corrupted Future - Key of Courage": lambda state: state.has_all({"Demon King Crown", "Magic Firefly"},
                                                                             self.player),
            "Autumn Hills Seal - Spike Ball Darts": self.has_dart,
            "Ninja Village Seal - Tree House": self.has_dart,
            "Underworld Seal - Fireball Wave": lambda state: state.has_any({"Wingsuit", "Windmill Shuriken"},
                                                                           self.player),
            "Tower of Time Seal - Time Waster Seal": self.has_dart,
            "Shop Chest": self.has_enough_seals,
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

    # add these locations when seals aren't shuffled
    if not multiworld.shuffle_seals[player] and not multiworld.shuffle_shards[player]:
        allow_self_locking_items(multiworld.get_region("Cloud Ruins Right", player), "Ruxxtin's Amulet")
        allow_self_locking_items(multiworld.get_region("Forlorn Temple", player), *PHOBEKINS)
