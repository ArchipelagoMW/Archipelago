from typing import List
from ...Region import Z3Region, RewardType
from ...Config import Config, GameMode, KeyShuffle
from ...Location import Location, LocationType
from ...Item import Item, Progression, ItemType

class GanonsTower(Z3Region):
    Name = "Ganon's Tower"
    Area = "Ganon's Tower"

    def __init__(self, world, config: Config):
        super().__init__(world, config)
        self.Reward = RewardType.Null
        self.RegionItems = [ ItemType.KeyGT, ItemType.BigKeyGT, ItemType.MapGT , ItemType.CompassGT]
        self.Locations = [
            Location(self, 256+189, 0x308161, LocationType.Regular, "Ganon's Tower - Bob's Torch",
                lambda items: items.Boots),
            Location(self, 256+190, 0x1EAB8, LocationType.Regular, "Ganon's Tower - DMs Room - Top Left",
                lambda items: items.Hammer and items.Hookshot),
            Location(self, 256+191, 0x1EABB, LocationType.Regular, "Ganon's Tower - DMs Room - Top Right",
                lambda items: items.Hammer and items.Hookshot),
            Location(self, 256+192, 0x1EABE, LocationType.Regular, "Ganon's Tower - DMs Room - Bottom Left",
                lambda items: items.Hammer and items.Hookshot),
            Location(self, 256+193, 0x1EAC1, LocationType.Regular, "Ganon's Tower - DMs Room - Bottom Right",
                lambda items: items.Hammer and items.Hookshot),
            Location(self, 256+194, 0x1EAD3, LocationType.Regular, "Ganon's Tower - Map Chest",
                lambda items: items.Hammer and (items.Hookshot or items.Boots) and items.KeyGT >=
                    (3 if any(self.GetLocation("Ganon's Tower - Map Chest").ItemIs(type, self.world) for type in [ItemType.BigKeyGT, ItemType.KeyGT]) else 4))
                .AlwaysAllow(lambda item, items: item.Is(ItemType.KeyGT, self.world) and items.KeyGT >= 3),
            Location(self, 256+195, 0x1EAD0, LocationType.Regular, "Ganon's Tower - Firesnake Room",
                lambda items: items.Hammer and items.Hookshot and items.KeyGT >= (2 if any(l.ItemIs(ItemType.BigKeyGT, self.world) for l in [
                        self.GetLocation("Ganon's Tower - Randomizer Room - Top Right"),
                        self.GetLocation("Ganon's Tower - Randomizer Room - Top Left"),
                        self.GetLocation("Ganon's Tower - Randomizer Room - Bottom Left"),
                        self.GetLocation("Ganon's Tower - Randomizer Room - Bottom Right")
                    ]) or self.GetLocation("Ganon's Tower - Firesnake Room").ItemIs(ItemType.KeyGT, self.world) else 3)),
            Location(self, 256+230, 0x1EAC4, LocationType.Regular, "Ganon's Tower - Randomizer Room - Top Left",
                lambda items: self.LeftSide(items, [
                    self.GetLocation("Ganon's Tower - Randomizer Room - Top Right"),
                    self.GetLocation("Ganon's Tower - Randomizer Room - Bottom Left"),
                    self.GetLocation("Ganon's Tower - Randomizer Room - Bottom Right")
                ])),
            Location(self, 256+231, 0x1EAC7, LocationType.Regular, "Ganon's Tower - Randomizer Room - Top Right",
                lambda items: self.LeftSide(items, [
                    self.GetLocation("Ganon's Tower - Randomizer Room - Top Left"),
                    self.GetLocation("Ganon's Tower - Randomizer Room - Bottom Left"),
                    self.GetLocation("Ganon's Tower - Randomizer Room - Bottom Right")
                ])),
            Location(self, 256+232, 0x1EACA, LocationType.Regular, "Ganon's Tower - Randomizer Room - Bottom Left",
                lambda items: self.LeftSide(items, [
                    self.GetLocation("Ganon's Tower - Randomizer Room - Top Right"),
                    self.GetLocation("Ganon's Tower - Randomizer Room - Top Left"),
                    self.GetLocation("Ganon's Tower - Randomizer Room - Bottom Right")
                ])),
            Location(self, 256+233, 0x1EACD, LocationType.Regular, "Ganon's Tower - Randomizer Room - Bottom Right",
                lambda items: self.LeftSide(items, [
                    self.GetLocation("Ganon's Tower - Randomizer Room - Top Right"),
                    self.GetLocation("Ganon's Tower - Randomizer Room - Top Left"),
                    self.GetLocation("Ganon's Tower - Randomizer Room - Bottom Left")
                ])),
            Location(self, 256+234, 0x1EAD9, LocationType.Regular, "Ganon's Tower - Hope Room - Left"),
            Location(self, 256+235, 0x1EADC, LocationType.Regular, "Ganon's Tower - Hope Room - Right"),
            Location(self, 256+236, 0x1EAE2, LocationType.Regular, "Ganon's Tower - Tile Room",
                lambda items: items.Somaria),
            Location(self, 256+203, 0x1EAE5, LocationType.Regular, "Ganon's Tower - Compass Room - Top Left",
                lambda items: self.RightSide(items, [
                    self.GetLocation("Ganon's Tower - Compass Room - Top Right"),
                    self.GetLocation("Ganon's Tower - Compass Room - Bottom Left"),
                    self.GetLocation("Ganon's Tower - Compass Room - Bottom Right")
                ])),
            Location(self, 256+204, 0x1EAE8, LocationType.Regular, "Ganon's Tower - Compass Room - Top Right",
                lambda items: self.RightSide(items, [
                    self.GetLocation("Ganon's Tower - Compass Room - Top Left"),
                    self.GetLocation("Ganon's Tower - Compass Room - Bottom Left"),
                    self.GetLocation("Ganon's Tower - Compass Room - Bottom Right")
                ])),
            Location(self, 256+205, 0x1EAEB, LocationType.Regular, "Ganon's Tower - Compass Room - Bottom Left",
                lambda items: self.RightSide(items, [
                    self.GetLocation("Ganon's Tower - Compass Room - Top Right"),
                    self.GetLocation("Ganon's Tower - Compass Room - Top Left"),
                    self.GetLocation("Ganon's Tower - Compass Room - Bottom Right")
                ])),
            Location(self, 256+206, 0x1EAEE, LocationType.Regular, "Ganon's Tower - Compass Room - Bottom Right",
                lambda items: self.RightSide(items, [
                    self.GetLocation("Ganon's Tower - Compass Room - Top Right"),
                    self.GetLocation("Ganon's Tower - Compass Room - Top Left"),
                    self.GetLocation("Ganon's Tower - Compass Room - Bottom Left")
                ])),
            Location(self, 256+207, 0x1EADF, LocationType.Regular, "Ganon's Tower - Bob's Chest",
                lambda items: items.KeyGT >= 3 and (
                    items.Hammer and items.Hookshot or
                    items.Somaria and items.Firerod)),
            Location(self, 256+208, 0x1EAD6, LocationType.Regular, "Ganon's Tower - Big Chest",
                lambda items: items.BigKeyGT and items.KeyGT >= 3 and (
                    items.Hammer and items.Hookshot or
                    items.Somaria and items.Firerod))
                .Allow(lambda item, items: item.IsNot(ItemType.BigKeyGT, self.world)),
            Location(self, 256+209, 0x1EAF1, LocationType.Regular, "Ganon's Tower - Big Key Chest", self.BigKeyRoom),
            Location(self, 256+210, 0x1EAF4, LocationType.Regular, "Ganon's Tower - Big Key Room - Left", self.BigKeyRoom),
            Location(self, 256+211, 0x1EAF7, LocationType.Regular, "Ganon's Tower - Big Key Room - Right", self.BigKeyRoom),
            Location(self, 256+212, 0x1EAFD, LocationType.Regular, "Ganon's Tower - Mini Helmasaur Room - Left", self.TowerAscend)
                .Allow(lambda item, items: item.IsNot(ItemType.BigKeyGT, self.world)),
            Location(self, 256+213, 0x1EB00, LocationType.Regular, "Ganon's Tower - Mini Helmasaur Room - Right", self.TowerAscend)
                .Allow(lambda item, items: item.IsNot(ItemType.BigKeyGT, self.world)),
            Location(self, 256+214, 0x1EB03, LocationType.Regular, "Ganon's Tower - Pre-Moldorm Chest", self.TowerAscend)
                .Allow(lambda item, items: item.IsNot(ItemType.BigKeyGT, self.world)),
            Location(self, 256+215, 0x1EB06, LocationType.Regular, "Ganon's Tower - Moldorm Chest",
                lambda items: items.BigKeyGT and items.KeyGT >= 4 and
                    items.Bow and items.CanLightTorches() and
                    self.CanBeatMoldorm(items) and items.Hookshot)
                .Allow(lambda item, items: all(item.IsNot(type, self.world) for type in [ ItemType.KeyGT, ItemType.BigKeyGT ]))
            ]

    def LeftSide(self, items: Progression, locations: List[Location]):
        return items.Hammer and items.Hookshot and items.KeyGT >= (3 if any(l.ItemIs(ItemType.BigKeyGT, self.world) for l in locations) else 4)

    def RightSide(self, items: Progression, locations: List[Location]):
        return items.Somaria and items.Firerod and items.KeyGT >= (3 if any(l.ItemIs(ItemType.BigKeyGT, self.world) for l in locations) else 4)

    def BigKeyRoom(self, items: Progression):
        return items.KeyGT >= 3 and \
            (items.Hammer and items.Hookshot or items.Firerod and items.Somaria) \
            and self.CanBeatArmos(items)

    def TowerAscend(self, items: Progression):
        return items.BigKeyGT and items.KeyGT >= 3 and items.Bow and items.CanLightTorches()
        
    def CanBeatArmos(self, items: Progression):
        return items.Sword or items.Hammer or items.Bow or \
            items.CanExtendMagic(2) and (items.Somaria or items.Byrna) or \
            items.CanExtendMagic(4) and (items.Firerod or items.Icerod)

    def CanBeatMoldorm(self, items: Progression):
        return items.Sword or items.Hammer

    def CanEnter(self, items: Progression):
        return items.MoonPearl and self.world.CanEnter("Dark World Death Mountain East", items) and \
            self.world.CanAcquireAtLeast(self.world.TowerCrystals, items, RewardType.AnyCrystal) and \
            self.world.CanAcquireAtLeast((self.world.TourianBossTokens * self.world.TowerCrystals) / 7, items, RewardType.AnyBossToken)

    # added for AP completion_condition when TowerCrystals is lower than GanonCrystals
    def CanComplete(self, items: Progression):
        return self.world.CanAcquireAtLeast(self.world.GanonCrystals, items, RewardType.AnyCrystal) and \
            self.world.CanAcquireAtLeast(self.world.TourianBossTokens, items, RewardType.AnyBossToken)

    def CanFill(self, item: Item):
        if (self.Config.Multiworld):
            # item.World will be None for item created by create_item for item links
            if (item.World is not None and (item.World != self.world or item.Progression)):
                return False
            if (self.Config.Keysanity and not ((item.Type == ItemType.BigKeyGT or item.Type == ItemType.KeyGT) and item.World == self.world) and (item.IsKey() or item.IsBigKey() or item.IsKeycard())):
                return False
        return super().CanFill(item)

