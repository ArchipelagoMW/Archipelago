from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import CollectionRule, add_rule, allow_self_locking_items
from .constants import NOTES, PHOBEKINS
from .options import MessengerAccessibility

if TYPE_CHECKING:
    from . import MessengerWorld


class MessengerRules:
    player: int
    world: "MessengerWorld"
    connection_rules: dict[str, CollectionRule]
    region_rules: dict[str, CollectionRule]
    location_rules: dict[str, CollectionRule]
    maximum_price: int
    required_seals: int

    def __init__(self, world: "MessengerWorld") -> None:
        self.player = world.player
        self.world = world

        # these locations are at the top of the shop tree, and the entire shop tree needs to be purchased
        maximum_price = (world.multiworld.get_location("The Shop - Demon's Bane", self.player).cost +
                         world.multiworld.get_location("The Shop - Focused Power Sense", self.player).cost)
        self.maximum_price = min(maximum_price, world.total_shards)
        self.required_seals = max(1, world.required_seals)

        # dict of connection names and requirements to traverse the exit
        self.connection_rules = {
            # from ToTHQ
            "Artificer's Portal":
                lambda state: state.has_all({"Demon King Crown", "Magic Firefly"}, self.player),
            "Shrink Down":
                lambda state: state.has_all(NOTES, self.player) or self.has_enough_seals(state),
            # the shop
            "Money Sink":
                lambda state: state.has("Money Wrench", self.player) and self.can_shop(state),
            # Autumn Hills
            "Autumn Hills - Portal -> Autumn Hills - Dimension Climb Shop":
                lambda state: self.has_wingsuit(state) and self.has_dart(state),
            "Autumn Hills - Dimension Climb Shop -> Autumn Hills - Portal":
                self.has_vertical,
            "Autumn Hills - Climbing Claws Shop -> Autumn Hills - Hope Path Shop":
                self.has_dart,
            "Autumn Hills - Climbing Claws Shop -> Autumn Hills - Key of Hope Checkpoint":
                self.false,  # hard logic only
            "Autumn Hills - Hope Path Shop -> Autumn Hills - Hope Latch Checkpoint":
                self.has_dart,
            "Autumn Hills - Hope Path Shop -> Autumn Hills - Climbing Claws Shop":
                lambda state: self.has_dart(state) and self.can_dboost(state),
            "Autumn Hills - Hope Path Shop -> Autumn Hills - Lakeside Checkpoint":
                lambda state: self.has_dart(state) and self.can_dboost(state),
            "Autumn Hills - Hope Latch Checkpoint -> Autumn Hills - Hope Path Shop":
                self.can_dboost,
            "Autumn Hills - Hope Latch Checkpoint -> Autumn Hills - Key of Hope Checkpoint":
                lambda state: self.has_dart(state) and self.has_wingsuit(state),
            # Forlorn Temple
            "Forlorn Temple - Outside Shop -> Forlorn Temple - Entrance Shop":
                lambda state: state.has_all(PHOBEKINS, self.player),
            "Forlorn Temple - Entrance Shop -> Forlorn Temple - Outside Shop":
                lambda state: state.has_all(PHOBEKINS, self.player),
            "Forlorn Temple - Entrance Shop -> Forlorn Temple - Sunny Day Checkpoint":
                lambda state: self.has_vertical(state) and self.can_dboost(state),
            "Forlorn Temple - Sunny Day Checkpoint -> Forlorn Temple - Rocket Maze Checkpoint":
                self.has_vertical,
            "Forlorn Temple - Rocket Sunset Shop -> Forlorn Temple - Descent Shop":
                lambda state: self.has_dart(state) and (self.can_dboost(state) or self.has_wingsuit(state)),
            "Forlorn Temple - Saw Gauntlet Shop -> Forlorn Temple - Demon King Shop":
                self.has_vertical,
            "Forlorn Temple - Demon King Shop -> Forlorn Temple - Saw Gauntlet Shop":
                self.has_vertical,
            # Howling Grotto
            "Howling Grotto - Portal -> Howling Grotto - Crushing Pits Shop":
                self.has_wingsuit,
            "Howling Grotto - Wingsuit Shop -> Howling Grotto - Left":
                self.has_wingsuit,
            "Howling Grotto - Wingsuit Shop -> Howling Grotto - Lost Woods Checkpoint":
                self.has_wingsuit,
            "Howling Grotto - Lost Woods Checkpoint -> Howling Grotto - Bottom":
                lambda state: state.has("Seashell", self.player),
            "Howling Grotto - Crushing Pits Shop -> Howling Grotto - Portal":
                lambda state: self.has_wingsuit(state) or self.can_dboost(state),
            "Howling Grotto - Breezy Crushers Checkpoint -> Howling Grotto - Emerald Golem Shop":
                self.has_wingsuit,
            "Howling Grotto - Breezy Crushers Checkpoint -> Howling Grotto - Crushing Pits Shop":
                lambda state: (self.has_wingsuit(state) or self.can_dboost(
                    state
                ) or self.can_destroy_projectiles(state))
                              and state.multiworld.get_region(
                    "Howling Grotto - Emerald Golem Shop", self.player
                ).can_reach(state),
            "Howling Grotto - Emerald Golem Shop -> Howling Grotto - Right":
                self.has_wingsuit,
            # Searing Crags
            "Searing Crags - Rope Dart Shop -> Searing Crags - Triple Ball Spinner Checkpoint":
                self.has_vertical,
            "Searing Crags - Portal -> Searing Crags - Right":
                self.has_tabi,
            "Searing Crags - Portal -> Searing Crags - Before Final Climb Shop":
                self.has_wingsuit,
            "Searing Crags - Portal -> Searing Crags - Colossuses Shop":
                self.has_wingsuit,
            "Searing Crags - Bottom -> Searing Crags - Portal":
                self.has_wingsuit,
            "Searing Crags - Right -> Searing Crags - Portal":
                lambda state: self.has_tabi(state) and self.has_wingsuit(state),
            "Searing Crags - Colossuses Shop -> Searing Crags - Key of Strength Shop":
                lambda state: state.has("Power Thistle", self.player)
                              and (self.has_dart(state)
                                   or (self.has_wingsuit(state)
                                       and self.can_destroy_projectiles(state))),
            "Searing Crags - Falling Rocks Shop -> Searing Crags - Searing Mega Shard Shop":
                self.has_dart,
            "Searing Crags - Searing Mega Shard Shop -> Searing Crags - Before Final Climb Shop":
                lambda state: self.has_dart(state) or self.can_destroy_projectiles(state),
            "Searing Crags - Searing Mega Shard Shop -> Searing Crags - Falling Rocks Shop":
                self.has_dart,
            "Searing Crags - Searing Mega Shard Shop -> Searing Crags - Key of Strength Shop":
                self.false,
            "Searing Crags - Before Final Climb Shop -> Searing Crags - Colossuses Shop":
                self.has_dart,
            # Glacial Peak
            "Glacial Peak - Portal -> Glacial Peak - Tower Entrance Shop":
                self.has_vertical,
            "Glacial Peak - Left -> Elemental Skylands - Air Shmup":
                lambda state: state.has("Magic Firefly", self.player)
                              and state.multiworld.get_location("Quillshroom Marsh - Queen of Quills", self.player)
                              .can_reach(state),
            "Glacial Peak - Tower Entrance Shop -> Glacial Peak - Top":
                lambda state: state.has("Ruxxtin's Amulet", self.player),
            "Glacial Peak - Projectile Spike Pit Checkpoint -> Glacial Peak - Left":
                lambda state: self.has_dart(state) or (self.can_dboost(state) and self.has_wingsuit(state)),
            # Tower of Time
            "Tower of Time - Left -> Tower of Time - Final Chance Shop":
                self.has_dart,
            "Tower of Time - Second Checkpoint -> Tower of Time - Third Checkpoint":
                lambda state: self.has_wingsuit(state) and (self.has_dart(state) or self.can_dboost(state)),
            "Tower of Time - Third Checkpoint -> Tower of Time - Fourth Checkpoint":
                lambda state: self.has_wingsuit(state) or self.can_dboost(state),
            "Tower of Time - Fourth Checkpoint -> Tower of Time - Fifth Checkpoint":
                lambda state: self.has_wingsuit(state) and self.has_dart(state),
            "Tower of Time - Fifth Checkpoint -> Tower of Time - Sixth Checkpoint":
                self.has_wingsuit,
            # Cloud Ruins
            "Cloud Ruins - Cloud Entrance Shop -> Cloud Ruins - Spike Float Checkpoint":
                self.has_wingsuit,
            "Cloud Ruins - Spike Float Checkpoint -> Cloud Ruins - Cloud Entrance Shop":
                lambda state: self.has_vertical(state) or self.can_dboost(state),
            "Cloud Ruins - Spike Float Checkpoint -> Cloud Ruins - Pillar Glide Shop":
                lambda state: self.has_vertical(state) or self.can_dboost(state),
            "Cloud Ruins - Pillar Glide Shop -> Cloud Ruins - Spike Float Checkpoint":
                lambda state: self.has_vertical(state) and self.can_double_dboost(state),
            "Cloud Ruins - Pillar Glide Shop -> Cloud Ruins - Ghost Pit Checkpoint":
                lambda state: self.has_dart(state) and self.has_wingsuit(state),
            "Cloud Ruins - Pillar Glide Shop -> Cloud Ruins - Crushers' Descent Shop":
                lambda state: self.has_wingsuit(state) and (self.has_dart(state) or self.can_dboost(state)),
            "Cloud Ruins - Toothbrush Alley Checkpoint -> Cloud Ruins - Seeing Spikes Shop":
                self.has_vertical,
            "Cloud Ruins - Seeing Spikes Shop -> Cloud Ruins - Sliding Spikes Shop":
                self.has_wingsuit,
            "Cloud Ruins - Sliding Spikes Shop -> Cloud Ruins - Seeing Spikes Shop":
                self.has_wingsuit,
            "Cloud Ruins - Sliding Spikes Shop -> Cloud Ruins - Saw Pit Checkpoint":
                self.has_vertical,
            "Cloud Ruins - Final Flight Shop -> Cloud Ruins - Manfred's Shop":
                lambda state: self.has_wingsuit(state) and self.has_dart(state),
            "Cloud Ruins - Manfred's Shop -> Cloud Ruins - Final Flight Shop":
                lambda state: self.has_wingsuit(state) and self.can_dboost(state),
            # Underworld
            "Underworld - Left -> Underworld - Left Shop":
                self.has_tabi,
            "Underworld - Left Shop -> Underworld - Left":
                self.has_tabi,
            "Underworld - Hot Dip Checkpoint -> Underworld - Lava Run Checkpoint":
                self.has_tabi,
            "Underworld - Fireball Wave Shop -> Underworld - Long Climb Shop":
                lambda state: self.can_destroy_projectiles(state) or self.has_tabi(state) or self.has_vertical(state),
            "Underworld - Long Climb Shop -> Underworld - Hot Tub Checkpoint":
                lambda state: self.has_tabi(state)
                              and (self.can_destroy_projectiles(state)
                                   or self.has_wingsuit(state))
                              or (self.has_wingsuit(state)
                                  and (self.has_dart(state)
                                       or self.can_dboost(state)
                                       or self.can_destroy_projectiles(state))),
            "Underworld - Hot Tub Checkpoint -> Underworld - Long Climb Shop":
                lambda state: self.has_tabi(state)
                              or self.can_destroy_projectiles(state)
                              or (self.has_dart(state) and self.has_wingsuit(state)),
            # Dark Cave
            "Dark Cave - Right -> Dark Cave - Left":
                lambda state: state.has("Candle", self.player) and self.has_dart(state),
            # Riviere Turquoise
            "Riviere Turquoise - Waterfall Shop -> Riviere Turquoise - Flower Flight Checkpoint":
                lambda state: self.has_dart(state) or (
                            self.has_wingsuit(state) and self.can_destroy_projectiles(state)),
            "Riviere Turquoise - Launch of Faith Shop -> Riviere Turquoise - Flower Flight Checkpoint":
                lambda state: self.has_dart(state) and self.can_dboost(state),
            "Riviere Turquoise - Flower Flight Checkpoint -> Riviere Turquoise - Waterfall Shop":
                lambda state: False,
            # Elemental Skylands
            "Elemental Skylands - Air Intro Shop -> Elemental Skylands - Air Seal Checkpoint":
                self.has_wingsuit,
            "Elemental Skylands - Air Intro Shop -> Elemental Skylands - Air Generator Shop":
                self.has_wingsuit,
            # Sunken Shrine
            "Sunken Shrine - Portal -> Sunken Shrine - Sun Path Shop":
                self.has_tabi,
            "Sunken Shrine - Portal -> Sunken Shrine - Moon Path Shop":
                self.has_tabi,
            "Sunken Shrine - Moon Path Shop -> Sunken Shrine - Waterfall Paradise Checkpoint":
                self.has_tabi,
            "Sunken Shrine - Waterfall Paradise Checkpoint -> Sunken Shrine - Moon Path Shop":
                self.has_tabi,
            "Sunken Shrine - Tabi Gauntlet Shop -> Sunken Shrine - Sun Path Shop":
                lambda state: self.can_dboost(state) or self.has_dart(state),
        }

        self.location_rules = {
            # hq
            "Money Wrench": self.can_shop,
            # ninja village
            "Ninja Village Seal - Tree House":
                self.has_dart,
            "Ninja Village - Candle":
                lambda state: state.multiworld.get_location("Searing Crags - Astral Tea Leaves", self.player).can_reach(
                    state),
            # autumn hills
            "Autumn Hills Seal - Spike Ball Darts":
                self.is_aerobatic,
            "Autumn Hills Seal - Trip Saws":
                self.has_wingsuit,
            "Autumn Hills Seal - Double Swing Saws":
                self.has_vertical,
            # forlorn temple
            "Forlorn Temple Seal - Rocket Maze":
                self.has_vertical,
            # bamboo creek
            "Bamboo Creek - Claustro":
                lambda state: self.has_wingsuit(state) and (self.has_dart(state) or self.can_dboost(state)),
            "Above Entrance Mega Shard":
                lambda state: self.has_dart(state) or self.can_dboost(state),
            "Bamboo Creek Seal - Spike Ball Pits":
                self.has_wingsuit,
            # howling grotto
            "Howling Grotto Seal - Windy Saws and Balls":
                self.has_wingsuit,
            "Howling Grotto Seal - Crushing Pits":
                lambda state: self.has_wingsuit(state) and self.has_dart(state),
            "Howling Grotto - Emerald Golem":
                self.has_wingsuit,
            # searing crags
            "Searing Crags - Astral Tea Leaves":
                lambda state: state.multiworld.get_location("Ninja Village - Astral Seed", self.player).can_reach(state),
            "Searing Crags Seal - Triple Ball Spinner":
                self.can_dboost,
            "Searing Crags - Pyro":
                self.has_tabi,
            # glacial peak
            "Glacial Peak Seal - Ice Climbers":
                self.has_dart,
            "Glacial Peak Seal - Projectile Spike Pit":
                self.can_destroy_projectiles,
            # tower of time
            "Tower of Time Seal - Time Waster":
                self.has_dart,
            # cloud ruins
            "Time Warp Mega Shard":
                lambda state: self.has_vertical(state) or self.can_dboost(state),
            "Cloud Ruins Seal - Ghost Pit":
                self.has_vertical,
            "Cloud Ruins Seal - Toothbrush Alley":
                self.has_dart,
            "Cloud Ruins Seal - Saw Pit":
                self.has_vertical,
            # underworld
            "Underworld Seal - Sharp and Windy Climb":
                self.has_wingsuit,
            "Underworld Seal - Fireball Wave":
                self.is_aerobatic,
            "Underworld Seal - Rising Fanta":
                self.has_dart,
            "Hot Tub Mega Shard":
                lambda state: self.has_tabi(state) or self.has_dart(state),
            # sunken shrine
            "Sunken Shrine - Key of Love":
                lambda state: state.has_all({"Sun Crest", "Moon Crest"}, self.player),
            "Sunken Shrine Seal - Waterfall Paradise":
                self.has_tabi,
            "Sunken Shrine Seal - Tabi Gauntlet":
                self.has_tabi,
            "Mega Shard of the Sun":
                self.has_tabi,
            # riviere turquoise
            "Riviere Turquoise Seal - Bounces and Balls":
                self.can_dboost,
            "Riviere Turquoise Seal - Launch of Faith":
                lambda state: self.has_vertical(state),
            # elemental skylands
            "Elemental Skylands - Key of Symbiosis":
                self.has_dart,
            "Elemental Skylands Seal - Air":
                self.has_wingsuit,
            "Elemental Skylands Seal - Water":
                lambda state: self.has_dart(state) and state.has("Currents Master", self.player),
            "Elemental Skylands Seal - Fire":
                lambda state: self.has_dart(state) and self.can_destroy_projectiles(state) and self.is_aerobatic(state),
            "Earth Mega Shard":
                self.has_dart,
            "Water Mega Shard":
                self.has_dart,
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
        return state.has("Power Seal", self.player, self.required_seals)

    def can_destroy_projectiles(self, state: CollectionState) -> bool:
        return state.has("Strike of the Ninja", self.player)

    def can_dboost(self, state: CollectionState) -> bool:
        return state.has_any({"Path of Resilience", "Meditation"}, self.player) and \
            state.has("Second Wind", self.player)

    def can_double_dboost(self, state: CollectionState) -> bool:
        return state.has_all({"Path of Resilience", "Meditation", "Second Wind"}, self.player)

    def is_aerobatic(self, state: CollectionState) -> bool:
        return self.has_wingsuit(state) and state.has("Aerobatics Warrior", self.player)

    def true(self, state: CollectionState) -> bool:
        """I know this is stupid, but it's easier to read in the dicts."""
        return True

    def false(self, state: CollectionState) -> bool:
        """It's a bit easier to just always create the connections that are only possible in hard or higher logic."""
        return False

    def can_shop(self, state: CollectionState) -> bool:
        return state.has("Shards", self.player, self.maximum_price)

    def set_messenger_rules(self) -> None:
        multiworld = self.world.multiworld

        for entrance_name, rule in self.connection_rules.items():
            entrance = multiworld.get_entrance(entrance_name, self.player)
            entrance.access_rule = rule
        for loc in multiworld.get_locations(self.player):
            if loc.name in self.location_rules:
                loc.access_rule = self.location_rules[loc.name]

        if self.world.options.music_box and not self.world.options.limited_movement:
            add_rule(multiworld.get_entrance("Shrink Down", self.player), self.has_dart)
        multiworld.completion_condition[self.player] = lambda state: state.has("Do the Thing!", self.player)
        if self.world.options.accessibility:  # not locations accessibility
            set_self_locking_items(self.world, self.player)


class MessengerHardRules(MessengerRules):
    def __init__(self, world: "MessengerWorld") -> None:
        super().__init__(world)

        self.connection_rules.update(
            {
                # Autumn Hills
                "Autumn Hills - Portal -> Autumn Hills - Dimension Climb Shop":
                    self.has_dart,
                "Autumn Hills - Climbing Claws Shop -> Autumn Hills - Key of Hope Checkpoint":
                    self.true,  # super easy normal clip - also possible with moderately difficult cloud stepping
                # Howling Grotto
                "Howling Grotto - Portal -> Howling Grotto - Crushing Pits Shop":
                    self.true,
                "Howling Grotto - Lost Woods Checkpoint -> Howling Grotto - Bottom":
                    self.true,  # just memorize the pattern :)
                "Howling Grotto - Crushing Pits Shop -> Howling Grotto - Portal":
                    self.true,
                "Howling Grotto - Breezy Crushers Checkpoint -> Howling Grotto - Emerald Golem Shop":
                    lambda state: self.has_wingsuit(state) or  # there's a very easy normal clip here but it's 16-bit only
                                  "Howling Grotto - Breezy Crushers Checkpoint" in self.world.spoiler_portal_mapping.values(),
                # Searing Crags
                "Searing Crags - Rope Dart Shop -> Searing Crags - Triple Ball Spinner Checkpoint":
                    lambda state: self.has_vertical(state) or self.can_destroy_projectiles(state),
                # it's doable without anything but one jump is pretty hard and time warping is no longer reliable
                "Searing Crags - Falling Rocks Shop -> Searing Crags - Searing Mega Shard Shop":
                    lambda state: self.has_vertical(state) or self.can_destroy_projectiles(state),
                "Searing Crags - Searing Mega Shard Shop -> Searing Crags - Falling Rocks Shop":
                    lambda state: self.has_dart(state) or
                                  (self.can_destroy_projectiles(state) and
                                   (self.has_wingsuit(state) or self.can_dboost(state))),
                "Searing Crags - Searing Mega Shard Shop -> Searing Crags - Key of Strength Shop":
                    lambda state: self.can_leash(state) or self.has_windmill(state),
                "Searing Crags - Before Final Climb Shop -> Searing Crags - Colossuses Shop":
                    self.true,
                # Glacial Peak
                "Glacial Peak - Left -> Elemental Skylands - Air Shmup":
                    lambda state: self.has_windmill(state) or
                                  (state.has("Magic Firefly", self.player) and
                                   state.multiworld.get_location(
                                       "Quillshroom Marsh - Queen of Quills", self.player).can_reach(state)) or
                                  (self.has_dart(state) and self.can_dboost(state)),
                "Glacial Peak - Projectile Spike Pit Checkpoint -> Glacial Peak - Left":
                    lambda state: self.has_vertical(state) or self.has_windmill(state),
                # Cloud Ruins
                "Cloud Ruins - Sliding Spikes Shop -> Cloud Ruins - Saw Pit Checkpoint":
                    self.true,
                # Elemental Skylands
                "Elemental Skylands - Air Intro Shop -> Elemental Skylands - Air Generator Shop":
                    self.true,
                # Riviere Turquoise
                "Riviere Turquoise - Waterfall Shop -> Riviere Turquoise - Flower Flight Checkpoint":
                    self.true,
                "Riviere Turquoise - Launch of Faith Shop -> Riviere Turquoise - Flower Flight Checkpoint":
                    self.can_dboost,
                "Riviere Turquoise - Flower Flight Checkpoint -> Riviere Turquoise - Waterfall Shop":
                    self.can_double_dboost,
            }
        )

        self.location_rules.update(
            {
                "Autumn Hills Seal - Spike Ball Darts":
                    lambda state: self.has_vertical(state) and self.has_windmill(state) or self.is_aerobatic(state),
                "Autumn Hills Seal - Double Swing Saws":
                    lambda state: self.has_vertical(state) or self.can_destroy_projectiles(state),
                "Bamboo Creek - Claustro":
                    self.has_wingsuit,
                "Bamboo Creek Seal - Spike Ball Pits":
                    self.true,
                "Howling Grotto Seal - Windy Saws and Balls":
                    self.true,
                "Searing Crags Seal - Triple Ball Spinner":
                    self.true,
                "Glacial Peak Seal - Ice Climbers":
                    lambda state: self.has_vertical(state) or self.can_dboost(state),
                "Glacial Peak Seal - Projectile Spike Pit":
                    lambda state: self.can_dboost(state) or self.can_destroy_projectiles(state),
                "Glacial Peak Seal - Glacial Air Swag":
                    lambda state: self.has_windmill(state) or self.has_vertical(state),
                "Glacial Peak Mega Shard":
                    lambda state: self.has_windmill(state) or self.has_vertical(state),
                "Cloud Ruins Seal - Ghost Pit":
                    self.true,
                "Cloud Ruins Seal - Toothbrush Alley":
                    self.true,
                "Cloud Ruins Seal - Saw Pit":
                    self.true,
                "Underworld Seal - Fireball Wave":
                    lambda state: self.is_aerobatic(state) or self.has_windmill(state),
                "Riviere Turquoise Seal - Bounces and Balls":
                    self.true,
                "Riviere Turquoise Seal - Launch of Faith":
                    lambda state: self.can_dboost(state) or self.has_vertical(state),
                "Elemental Skylands - Key of Symbiosis":
                    lambda state: self.has_dart(state) or self.can_dboost(state) or self.has_windmill(state),
                "Elemental Skylands Seal - Water":
                    lambda state: self.has_dart(state) or self.can_dboost(state) or self.has_windmill(state),
                "Elemental Skylands Seal - Fire":
                    lambda state: (self.has_dart(state) or self.can_dboost(state) or self.has_windmill(state))
                                  and self.can_destroy_projectiles(state),
                "Earth Mega Shard":
                    lambda state: self.has_dart(state) or self.can_dboost(state) or self.has_windmill(state),
                "Water Mega Shard":
                    lambda state: self.has_dart(state) or self.can_dboost(state) or self.has_windmill(state),
            }
        )

    def has_windmill(self, state: CollectionState) -> bool:
        return state.has("Windmill Shuriken", self.player)

    def can_dboost(self, state: CollectionState) -> bool:
        return state.has("Second Wind", self.player)  # who really needs meditation
    
    def can_destroy_projectiles(self, state: CollectionState) -> bool:
        return super().can_destroy_projectiles(state) or self.has_windmill(state)

    def can_leash(self, state: CollectionState) -> bool:
        return self.has_dart(state) and self.can_dboost(state)


class MessengerOOBRules(MessengerRules):
    def __init__(self, world: "MessengerWorld") -> None:
        self.world = world
        self.player = world.player

        self.required_seals = max(1, world.required_seals)
        self.region_rules = {
            "Elemental Skylands":
                lambda state: state.has_any(
                    {"Windmill Shuriken", "Wingsuit", "Rope Dart", "Magic Firefly"}, self.player
                ),
            "Music Box": lambda state: state.has_all(set(NOTES), self.player) or self.has_enough_seals(state),
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
            "Underworld Seal - Fireball Wave": lambda state: state.has_any(
                {"Wingsuit", "Windmill Shuriken"},
                self.player
            ),
            "Tower of Time Seal - Time Waster": self.has_dart,
        }

    def set_messenger_rules(self) -> None:
        super().set_messenger_rules()
        self.world.options.accessibility.value = MessengerAccessibility.option_minimal


def set_self_locking_items(world: "MessengerWorld", player: int) -> None:
    # locations where these placements are always valid
    allow_self_locking_items(world.get_location("Searing Crags - Key of Strength").parent_region, "Power Thistle")
    allow_self_locking_items(world.get_location("Sunken Shrine - Key of Love"), "Sun Crest", "Moon Crest")
    allow_self_locking_items(world.get_location("Corrupted Future - Key of Courage").parent_region, "Demon King Crown")
    allow_self_locking_items(world.get_location("Elemental Skylands Seal - Water"), "Currents Master")
