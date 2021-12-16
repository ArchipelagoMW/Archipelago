from typing import List
from Region import Z3Region, RewardType, IReward, IMedallionAccess
from Config import Config
from World import World
from Location import Location, LocationType
from Item import Progression, ItemType
from worlds.smz3.Config import GameMode, KeyShuffle
from worlds.smz3.Item import Item

class TurtleRock(Z3Region, IReward, IMedallionAccess):
    Name = "Turtle Rock"

    def __init__(self, world: World, config: Config):
        super().__init__(world, config)
        self.RegionItems = [ ItemType.KeyTR, ItemType.BigKeyTR, ItemType.MapTR, ItemType.CompassTR]
        self.Reward = RewardType.Null
        self.Medallion = ItemType.Nothing
        self.Locations = [
            Location(self, 256+177, 0x1EA22, LocationType.Regular, "Turtle Rock - Compass Chest"),
            Location(self, 256+178, 0x1EA1C, LocationType.Regular, "Turtle Rock - Roller Room - Left",
                lambda items: items.Firerod),
            Location(self, 256+179, 0x1EA1F, LocationType.Regular, "Turtle Rock - Roller Room - Right",
                lambda items: items.Firerod),
            Location(self, 256+180, 0x1EA16, LocationType.Regular, "Turtle Rock - Chain Chomps",
                lambda items: items.KeyTR >= 1),
            Location(self, 256+181, 0x1EA25, LocationType.Regular, "Turtle Rock - Big Key Chest",
                lambda items: items.KeyTR >=
                    (2 if not Config.Keysanity or self.GetLocation("Turtle Rock - Big Key Chest").ItemIs(ItemType.BigKeyTR, World) else
                        3 if self.GetLocation("Turtle Rock - Big Key Chest").ItemIs(ItemType.KeyTR, World) else 4))
                .AlwaysAllow(lambda item, items: item.Is(ItemType.KeyTR, World) and items.KeyTR >= 3),
            Location(self, 256+182, 0x1EA19, LocationType.Regular, "Turtle Rock - Big Chest",
                lambda items: items.BigKeyTR and items.KeyTR >= 2)
                .Allow(lambda item, items: item.IsNot(ItemType.BigKeyTR, World)),
            Location(self, 256+183, 0x1EA34, LocationType.Regular, "Turtle Rock - Crystaroller Room",
                lambda items: items.BigKeyTR and items.KeyTR >= 2),
            Location(self, 256+184, 0x1EA28, LocationType.Regular, "Turtle Rock - Eye Bridge - Top Right", self.LaserBridge),
            Location(self, 256+185, 0x1EA2B, LocationType.Regular, "Turtle Rock - Eye Bridge - Top Left", self.LaserBridge),
            Location(self, 256+186, 0x1EA2E, LocationType.Regular, "Turtle Rock - Eye Bridge - Bottom Right", self.LaserBridge),
            Location(self, 256+187, 0x1EA31, LocationType.Regular, "Turtle Rock - Eye Bridge - Bottom Left", self.LaserBridge),
            Location(self, 256+188, 0x308159, LocationType.Regular, "Turtle Rock - Trinexx",
                lambda items: items.BigKeyTR and items.KeyTR >= 4 and items.Lamp and self.CanBeatBoss(items)),
            ]

    def LaserBridge(self, items: Progression):
        return items.BigKeyTR and items.KeyTR >= 3 and items.Lamp and (items.Cape or items.Byrna or items.CanBlockLasers)

    def CanBeatBoss(self, items: Progression):
        return items.Firerod and items.Icerod

    def CanEnter(self, items: Progression):
        return (items.Bombos if self.Medallion == ItemType.Bombos else (
                    items.Ether if self.Medallion == ItemType.Ether else items.Quake)) and items.Sword and \
            items.MoonPearl and items.CanLiftHeavy() and items.Hammer and items.Somaria and \
            World.CanEnter("Light World Death Mountain East", items)

    def CanComplete(self, items: Progression):
        return self.GetLocation("Turtle Rock - Trinexx").Available(items)
