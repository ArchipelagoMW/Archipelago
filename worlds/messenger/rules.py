from functools import cached_property
from typing import TYPE_CHECKING, TypeAlias

from rule_builder.rules import CanReachLocation, CanReachRegion, False_, Has, HasAll, HasAny, Rule, True_
from worlds.generic.Rules import allow_self_locking_items

from .constants import NOTES, PHOBEKINS
from .options import MessengerAccessibility
from .subclasses import MessengerShopLocation

if TYPE_CHECKING:
    from . import MessengerWorld

MessengerRule: TypeAlias = "Rule[MessengerWorld]"


class MessengerRules:
    player: int
    world: "MessengerWorld"
    connection_rules: dict[str, MessengerRule]
    region_rules: dict[str, MessengerRule]
    location_rules: dict[str, MessengerRule]
    maximum_price: int
    required_seals: int

    def __init__(self, world: "MessengerWorld") -> None:
        self.player = world.player
        self.world = world

        # these locations are at the top of the shop tree, and the entire shop tree needs to be purchased
        maximum_price = (world.multiworld.get_location("The Shop - Demon's Bane", self.player).cost +
                         world.multiworld.get_location("The Shop - Focused Power Sense", self.player).cost)
        self.maximum_price = min(maximum_price, world.total_shards)
        self.required_seals = world.required_seals

        # dict of connection names and requirements to traverse the exit
        # fmt: off
        self.connection_rules = {
            # from ToTHQ
            "Artificer's Portal":
                Has("Demon King Crown"),
            "Shrink Down":
                HasAll(*NOTES),
            # the shop
            "Money Sink":
                Has("Money Wrench") & self.can_shop,
            # Autumn Hills
            "Autumn Hills - Portal -> Autumn Hills - Dimension Climb Shop":
                self.has_wingsuit & self.has_dart,
            "Autumn Hills - Dimension Climb Shop -> Autumn Hills - Portal":
                self.has_vertical,
            "Autumn Hills - Climbing Claws Shop -> Autumn Hills - Hope Path Shop":
                self.has_dart,
            "Autumn Hills - Climbing Claws Shop -> Autumn Hills - Key of Hope Checkpoint":
                self.false,  # hard logic only
            "Autumn Hills - Hope Path Shop -> Autumn Hills - Hope Latch Checkpoint":
                self.has_dart,
            "Autumn Hills - Hope Path Shop -> Autumn Hills - Climbing Claws Shop":
                self.has_dart & self.can_dboost,
            "Autumn Hills - Hope Path Shop -> Autumn Hills - Lakeside Checkpoint":
                self.has_dart & self.can_dboost,
            "Autumn Hills - Hope Latch Checkpoint -> Autumn Hills - Hope Path Shop":
                self.can_dboost,
            "Autumn Hills - Hope Latch Checkpoint -> Autumn Hills - Key of Hope Checkpoint":
                self.has_dart & self.has_wingsuit,
            # Forlorn Temple
            "Forlorn Temple - Outside Shop -> Forlorn Temple - Entrance Shop":
                HasAll(*PHOBEKINS),
            "Forlorn Temple - Entrance Shop -> Forlorn Temple - Outside Shop":
                HasAll(*PHOBEKINS),
            "Forlorn Temple - Entrance Shop -> Forlorn Temple - Sunny Day Checkpoint":
                self.has_vertical & self.can_dboost,
            "Forlorn Temple - Sunny Day Checkpoint -> Forlorn Temple - Rocket Maze Checkpoint":
                self.has_vertical,
            "Forlorn Temple - Rocket Sunset Shop -> Forlorn Temple - Descent Shop":
                self.has_dart & (self.can_dboost | self.has_wingsuit),
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
                Has("Seashell"),
            "Howling Grotto - Crushing Pits Shop -> Howling Grotto - Portal":
                self.has_wingsuit | self.can_dboost,
            "Howling Grotto - Breezy Crushers Checkpoint -> Howling Grotto - Emerald Golem Shop":
                self.has_wingsuit,
            "Howling Grotto - Breezy Crushers Checkpoint -> Howling Grotto - Crushing Pits Shop":
                (self.has_wingsuit | self.can_dboost | self.can_destroy_projectiles)
                & CanReachRegion("Howling Grotto - Emerald Golem Shop"),
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
                self.has_tabi & self.has_wingsuit,
            "Searing Crags - Colossuses Shop -> Searing Crags - Key of Strength Shop":
                Has("Power Thistle"),
            "Searing Crags - Key of Strength Shop -> Searing Crags - Key of Strength Room":
                self.has_dart
                | (self.has_wingsuit
                   & self.can_destroy_projectiles),
            "Searing Crags - Falling Rocks Shop -> Searing Crags - Searing Mega Shard Shop":
                self.has_dart,
            "Searing Crags - Searing Mega Shard Shop -> Searing Crags - Before Final Climb Shop":
                self.has_dart | self.can_destroy_projectiles,
            "Searing Crags - Searing Mega Shard Shop -> Searing Crags - Falling Rocks Shop":
                self.has_dart,
            "Searing Crags - Searing Mega Shard Shop -> Searing Crags - Key of Strength Room":
                self.false,
            "Searing Crags - Before Final Climb Shop -> Searing Crags - Colossuses Shop":
                self.has_dart,
            # Glacial Peak
            "Glacial Peak - Portal -> Glacial Peak - Tower Entrance Shop":
                self.has_vertical,
            "Glacial Peak - Left -> Elemental Skylands - Air Shmup":
                Has("Magic Firefly") & CanReachLocation("Quillshroom Marsh - Queen of Quills"),
            "Glacial Peak - Top -> Cloud Ruins - Left":
                Has("Ruxxtin's Amulet"),
            "Glacial Peak - Projectile Spike Pit Checkpoint -> Glacial Peak - Left":
                self.has_dart | (self.can_dboost & self.has_wingsuit),
            # Tower of Time
            "Tower of Time - Left -> Tower of Time - Final Chance Shop":
                self.has_dart,
            "Tower of Time - Second Checkpoint -> Tower of Time - Third Checkpoint":
                self.has_wingsuit & (self.has_dart | self.can_dboost),
            "Tower of Time - Third Checkpoint -> Tower of Time - Fourth Checkpoint":
                self.has_wingsuit | self.can_dboost,
            "Tower of Time - Fourth Checkpoint -> Tower of Time - Fifth Checkpoint":
                self.has_wingsuit & self.has_dart,
            "Tower of Time - Fifth Checkpoint -> Tower of Time - Sixth Checkpoint":
                self.has_wingsuit,
            # Cloud Ruins
            "Cloud Ruins - Cloud Entrance Shop -> Cloud Ruins - Spike Float Checkpoint":
                self.has_wingsuit,
            "Cloud Ruins - Spike Float Checkpoint -> Cloud Ruins - Cloud Entrance Shop":
                self.has_vertical | self.can_dboost,
            "Cloud Ruins - Spike Float Checkpoint -> Cloud Ruins - Pillar Glide Shop":
                self.has_vertical | self.can_dboost,
            "Cloud Ruins - Pillar Glide Shop -> Cloud Ruins - Spike Float Checkpoint":
                self.has_vertical & self.can_double_dboost,
            "Cloud Ruins - Pillar Glide Shop -> Cloud Ruins - Ghost Pit Checkpoint":
                self.has_dart & self.has_wingsuit,
            "Cloud Ruins - Pillar Glide Shop -> Cloud Ruins - Crushers' Descent Shop":
                self.has_wingsuit & (self.has_dart | self.can_dboost),
            "Cloud Ruins - Toothbrush Alley Checkpoint -> Cloud Ruins - Seeing Spikes Shop":
                self.has_vertical,
            "Cloud Ruins - Seeing Spikes Shop -> Cloud Ruins - Sliding Spikes Shop":
                self.has_wingsuit,
            "Cloud Ruins - Sliding Spikes Shop -> Cloud Ruins - Seeing Spikes Shop":
                self.has_wingsuit,
            "Cloud Ruins - Sliding Spikes Shop -> Cloud Ruins - Saw Pit Checkpoint":
                self.has_vertical,
            "Cloud Ruins - Final Flight Shop -> Cloud Ruins - Manfred's Shop":
                self.has_wingsuit & self.has_dart,
            "Cloud Ruins - Manfred's Shop -> Cloud Ruins - Final Flight Shop":
                self.has_wingsuit & self.can_dboost,
            # Underworld
            "Underworld - Left -> Underworld - Left Shop":
                self.has_tabi | self.has_vertical,
            "Underworld - Left Shop -> Underworld - Left":
                self.has_tabi,
            "Underworld - Hot Dip Checkpoint -> Underworld - Lava Run Checkpoint":
                self.has_tabi,
            "Underworld - Fireball Wave Shop -> Underworld - Long Climb Shop":
                self.can_destroy_projectiles | self.has_tabi | self.has_vertical,
            "Underworld - Long Climb Shop -> Underworld - Hot Tub Checkpoint":
                self.has_tabi
                & (self.can_destroy_projectiles
                   | self.has_wingsuit)
                | (self.has_wingsuit
                   & (self.has_dart
                      | self.can_dboost
                      | self.can_destroy_projectiles)),
            "Underworld - Hot Tub Checkpoint -> Underworld - Long Climb Shop":
                self.has_tabi
                | self.can_destroy_projectiles
                | (self.has_dart & self.has_wingsuit),
            # Dark Cave
            "Dark Cave - Right -> Dark Cave - Left":
                Has("Candle") & self.has_dart & self.has_wingsuit,
            # Riviere Turquoise
            "Riviere Turquoise - Waterfall Shop -> Riviere Turquoise - Flower Flight Checkpoint":
                self.has_dart | (
                        self.has_wingsuit & self.can_destroy_projectiles),
            "Riviere Turquoise - Launch of Faith Shop -> Riviere Turquoise - Flower Flight Checkpoint":
                self.has_dart & self.can_dboost,
            "Riviere Turquoise - Flower Flight Checkpoint -> Riviere Turquoise - Waterfall Shop":
                self.false,
            # Elemental Skylands
            "Elemental Skylands - Air Intro Shop -> Elemental Skylands - Air Seal Checkpoint":
                self.has_wingsuit,
            "Elemental Skylands - Air Intro Shop -> Elemental Skylands - Air Generator Shop":
                self.has_wingsuit,
            "Elemental Skylands - Earth Intro Shop -> Elemental Skylands - Earth Generator Shop":
                self.has_dart,
            "Elemental Skylands - Water Generator Shop -> Elemental Skylands - Water Intro Shop":
                self.can_destroy_projectiles,
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
                self.can_dboost | self.has_dart,
        }
        # fmt: on

        # fmt: off
        self.location_rules = {
            # hq
            "Money Wrench": self.can_shop,
            # ninja village
            "Ninja Village Seal - Tree House":
                self.has_dart,
            "Ninja Village - Candle":
                CanReachLocation("Searing Crags - Astral Tea Leaves"),
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
                self.has_wingsuit & (self.has_dart | self.can_dboost),
            "Above Entrance Mega Shard":
                self.has_dart | self.can_dboost,
            "Bamboo Creek Seal - Spike Ball Pits":
                self.has_wingsuit,
            # howling grotto
            "Howling Grotto Seal - Windy Saws and Balls":
                self.has_wingsuit,
            "Howling Grotto Seal - Crushing Pits":
                self.has_wingsuit & self.has_dart,
            "Howling Grotto - Emerald Golem":
                self.has_wingsuit,
            # searing crags
            "Searing Crags - Astral Tea Leaves":
                CanReachLocation("Ninja Village - Astral Seed"),
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
            # corrupted future
            "Corrupted Future - Key of Courage":
                Has("Magic Firefly"),
            # cloud ruins
            "Time Warp Mega Shard":
                self.has_vertical | self.can_dboost,
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
                self.has_tabi | self.has_dart,
            # sunken shrine
            "Sunken Shrine - Key of Love":
                HasAll("Sun Crest", "Moon Crest"),
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
                self.has_vertical,
            # elemental skylands
            "Elemental Skylands Seal - Air":
                self.has_wingsuit,
            "Elemental Skylands Seal - Water":
                self.has_dart & Has("Currents Master"),
            "Elemental Skylands Seal - Fire":
                self.has_dart & self.can_destroy_projectiles & self.is_aerobatic,
            "Earth Mega Shard":
                self.has_dart,
        }
        # fmt: on

        if self.required_seals:
            self.connection_rules["Shrink Down"] = self.has_enough_seals

    @cached_property
    def has_wingsuit(self) -> MessengerRule:
        return Has("Wingsuit")

    @cached_property
    def has_dart(self) -> MessengerRule:
        return Has("Rope Dart")

    @cached_property
    def has_tabi(self) -> MessengerRule:
        return Has("Lightfoot Tabi")

    @cached_property
    def has_vertical(self) -> MessengerRule:
        return self.has_wingsuit | self.has_dart

    @cached_property
    def has_enough_seals(self) -> MessengerRule:
        return Has("Power Seal", self.required_seals)

    @cached_property
    def can_destroy_projectiles(self) -> MessengerRule:
        return Has("Strike of the Ninja")

    @cached_property
    def can_dboost(self) -> MessengerRule:
        return HasAny("Path of Resilience", "Meditation") & Has("Second Wind")

    @cached_property
    def can_double_dboost(self) -> MessengerRule:
        return HasAll("Path of Resilience", "Meditation", "Second Wind")

    @cached_property
    def is_aerobatic(self) -> MessengerRule:
        return self.has_wingsuit & Has("Aerobatics Warrior")

    @cached_property
    def true(self) -> MessengerRule:
        """I know this is stupid, but it's easier to read in the dicts."""
        return True_()

    @cached_property
    def false(self) -> MessengerRule:
        """It's a bit easier to just always create the connections that are only possible in hard or higher logic."""
        return False_()

    @cached_property
    def can_shop(self) -> MessengerRule:
        return Has("Shards", self.maximum_price)

    def set_messenger_rules(self) -> None:
        if self.world.options.music_box and not self.world.options.limited_movement:
            self.connection_rules["Shrink Down"] &= self.has_dart

        for entrance_name, rule in self.connection_rules.items():
            entrance = self.world.get_entrance(entrance_name)
            self.world.set_rule(entrance, rule)

        for loc in self.world.get_locations():
            if loc.name in self.location_rules:
                self.world.set_rule(loc, self.location_rules[loc.name])

            if isinstance(loc, MessengerShopLocation):
                rule = Has("Shards", min(loc.cost, self.world.total_shards))
                self.world.set_rule(loc, rule)

        self.world.set_completion_rule(Has("Do the Thing!"))
        if self.world.options.accessibility:  # not locations accessibility
            set_self_locking_items(self.world)


class MessengerHardRules(MessengerRules):
    def __init__(self, world: "MessengerWorld") -> None:
        super().__init__(world)

        # fmt: off
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
                    self.has_wingsuit  # there's a very easy normal clip here but it's 16-bit only
                    | (self.true
                       if "Howling Grotto - Breezy Crushers Checkpoint" in self.world.spoiler_portal_mapping.values()
                       else self.false),
                # Searing Crags
                "Searing Crags - Rope Dart Shop -> Searing Crags - Triple Ball Spinner Checkpoint":
                    self.has_vertical | self.can_destroy_projectiles,
                # it's doable without anything but one jump is pretty hard and time warping is no longer reliable
                "Searing Crags - Falling Rocks Shop -> Searing Crags - Searing Mega Shard Shop":
                    self.has_vertical | self.can_destroy_projectiles,
                "Searing Crags - Searing Mega Shard Shop -> Searing Crags - Falling Rocks Shop":
                    self.has_dart
                    | (self.can_destroy_projectiles
                       & (self.has_wingsuit | self.can_dboost)),
                "Searing Crags - Searing Mega Shard Shop -> Searing Crags - Key of Strength Room":
                    self.can_leash | self.has_windmill,
                "Searing Crags - Before Final Climb Shop -> Searing Crags - Colossuses Shop":
                    self.true,
                # Glacial Peak
                "Glacial Peak - Left -> Elemental Skylands - Air Shmup":
                    self.has_windmill
                    | (Has("Magic Firefly")
                       & CanReachLocation("Quillshroom Marsh - Queen of Quills")
                       | (self.has_dart & self.can_dboost)),
                "Glacial Peak - Projectile Spike Pit Checkpoint -> Glacial Peak - Left":
                    self.has_vertical | self.has_windmill,
                # Cloud Ruins
                "Cloud Ruins - Sliding Spikes Shop -> Cloud Ruins - Saw Pit Checkpoint":
                    self.true,
                # Elemental Skylands
                "Elemental Skylands - Air Intro Shop -> Elemental Skylands - Air Generator Shop":
                    self.true,
                "Elemental Skylands - Earth Intro Shop -> Elemental Skylands - Earth Generator Shop":
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
        # fmt: on

        # fmt: off
        self.location_rules.update(
            {
                "Autumn Hills Seal - Spike Ball Darts":
                    (self.has_vertical & self.has_windmill) | self.is_aerobatic,
                "Autumn Hills Seal - Double Swing Saws":
                    self.has_vertical | self.can_destroy_projectiles,
                "Bamboo Creek - Claustro":
                    self.has_wingsuit,
                "Bamboo Creek Seal - Spike Ball Pits":
                    self.true,
                "Above Entrance Mega Shard": # Just reset to the menu and you can get it with full health
                    self.true,
                "Howling Grotto Seal - Windy Saws and Balls":
                    self.true,
                "Howling Grotto Seal - Crushing Pits":
                    self.has_vertical,
                "Searing Crags Seal - Triple Ball Spinner":
                    self.true,
                "Glacial Peak Seal - Ice Climbers":
                    self.has_vertical | self.can_dboost,
                "Glacial Peak Seal - Projectile Spike Pit":
                    self.can_dboost | self.can_destroy_projectiles,
                "Cloud Ruins Seal - Ghost Pit":
                    self.true,
                "Cloud Ruins Seal - Toothbrush Alley":
                    self.true,
                "Cloud Ruins Seal - Saw Pit":
                    self.true,
                "Underworld Seal - Fireball Wave":
                    self.is_aerobatic | self.has_windmill,
                "Riviere Turquoise Seal - Bounces and Balls":
                    self.true,
                "Riviere Turquoise Seal - Launch of Faith":
                    self.can_dboost | self.has_vertical,
                "Elemental Skylands Seal - Water":
                    self.true,
                "Elemental Skylands Seal - Fire":
                    self.can_destroy_projectiles,
                "Earth Mega Shard":
                    self.has_dart | self.can_dboost | self.has_windmill,
            }
        )
        # fmt: on

    @cached_property
    def has_windmill(self) -> MessengerRule:
        return Has("Windmill Shuriken")

    @cached_property
    def can_dboost(self) -> MessengerRule:
        return Has("Second Wind")  # who really needs meditation

    @cached_property
    def can_destroy_projectiles(self) -> MessengerRule:
        return super().can_destroy_projectiles | self.has_windmill

    @cached_property
    def can_leash(self) -> MessengerRule:
        return self.has_dart & self.can_dboost


class MessengerOOBRules(MessengerRules):
    def __init__(self, world: "MessengerWorld") -> None:
        self.world = world
        self.player = world.player

        self.required_seals = max(1, world.required_seals)
        self.region_rules = {
            "Elemental Skylands":
                HasAny("Windmill Shuriken", "Wingsuit", "Rope Dart", "Magic Firefly"),
            "Music Box":
                HasAll(*NOTES) | self.has_enough_seals,
        }

        self.location_rules = {
            "Bamboo Creek - Claustro": self.has_wingsuit,
            "Sunken Shrine - Key of Love": HasAll("Sun Crest", "Moon Crest"),
            "Searing Crags - Pyro": self.has_tabi,
            "Underworld - Key of Chaos": self.has_tabi,
            "Corrupted Future - Key of Courage":
                HasAll("Demon King Crown", "Magic Firefly"),
            "Autumn Hills Seal - Spike Ball Darts": self.has_dart,
            "Ninja Village Seal - Tree House": self.has_dart,
            "Underworld Seal - Fireball Wave":
                HasAny("Wingsuit", "Windmill Shuriken"),
            "Tower of Time Seal - Time Waster": self.has_dart,
        }

    def set_messenger_rules(self) -> None:
        super().set_messenger_rules()
        self.world.options.accessibility.value = MessengerAccessibility.option_minimal


def set_self_locking_items(world: "MessengerWorld") -> None:
    # locations where these placements are always valid
    allow_self_locking_items(world.get_location("Searing Crags - Key of Strength").parent_region, "Power Thistle")
    allow_self_locking_items(world.get_location("Sunken Shrine - Key of Love"), "Sun Crest", "Moon Crest")
    allow_self_locking_items(world.get_location("Elemental Skylands Seal - Water"), "Currents Master")
    if not world.options.shuffle_transitions:
        allow_self_locking_items(world.get_location("Corrupted Future - Key of Courage").parent_region,
                                 "Demon King Crown")
