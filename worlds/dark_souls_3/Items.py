from dataclasses import dataclass
import dataclasses
from enum import IntEnum
from typing import Any, cast, ClassVar, Dict, Generator, List, Optional, Set

from BaseClasses import Item, ItemClassification


class DS3ItemCategory(IntEnum):
    WEAPON_UPGRADE_5 = 0
    WEAPON_UPGRADE_10 = 1
    WEAPON_UPGRADE_10_INFUSIBLE = 2
    SHIELD = 3
    SHIELD_INFUSIBLE = 4
    ARMOR = 5
    RING = 6
    SPELL = 7
    MISC = 8
    UNIQUE = 9
    BOSS = 10
    SOUL = 11
    UPGRADE = 12
    HEALING = 13

    @property
    def is_infusible(self) -> bool:
        """Returns whether this category can be infused."""
        return self in [
            DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE,
            DS3ItemCategory.SHIELD_INFUSIBLE
        ]

    @property
    def upgrade_level(self) -> Optional[int]:
        """The maximum upgrade level for this category, or None if it's not upgradable."""
        if self == DS3ItemCategory.WEAPON_UPGRADE_5: return 5
        if self in [
            DS3ItemCategory.WEAPON_UPGRADE_10,
            DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE
        ]: return 10
        return None


@dataclass
class Infusion(IntEnum):
    """Infusions supported by Dark Souls III.

    The value of each infusion is the number added to the base weapon's ID to get the infused ID.
    """

    HEAVY = 100
    SHARP = 200
    REFINED = 300
    SIMPLE = 400
    CRYSTAL = 500
    FIRE = 600
    CHAOS = 700
    LIGHTNING = 800
    DEEP = 900
    DARK = 1000
    POISON = 1100
    BLOOD = 1200
    RAW = 1300
    BLESSED = 1400
    HOLLOW = 1500

    @property
    def prefix(self):
        """The prefix to add to a weapon name with this infusion."""
        return self.name.title()


class UsefulIf(IntEnum):
    """An enum that indicates when an item should be upgraded to ItemClassification.useful.

    This is used for rings with +x variants that may or may not be the best in class depending on
    the player's settings.
    """

    DEFAULT = 0
    """Follows DS3ItemData.classification as written."""

    BASE = 1
    """Useful only if the DLC and NG+ locations are disabled."""

    NO_DLC = 2
    """Useful if the DLC is disabled, whether or not NG+ locations are."""

    NO_NGP = 3
    """Useful if NG+ locations is disabled, whether or not the DLC is."""


@dataclass
class DS3ItemData:
    __item_id: ClassVar[int] = 100000
    """The next item ID to use when creating item data."""

    name: str
    ds3_code: Optional[int]
    category: DS3ItemCategory

    base_ds3_code: Optional[int] = None
    """If this is an upgradable weapon, the base ID of the weapon it upgrades from.

    Otherwise, or if the weapon isn't upgraded, this is the same as ds3_code.
    """

    base_name: Optional[str] = None
    """The name of the individual item, if this is a multi-item group."""

    classification: ItemClassification = ItemClassification.filler
    """How important this item is to the game progression."""

    ap_code: Optional[int] = None
    """The Archipelago ID for this item."""

    is_dlc: bool = False
    """Whether this item is only found in one of the two DLC packs."""

    count: int = 1
    """The number of copies of this item included in each drop."""

    inject: bool = False
    """If this is set, the randomizer will try to inject this item into the game.

    This is used for items such as covenant rewards that aren't realistically reachable in a
    randomizer run, but are still fun to have available to the player. If there are more locations
    available than there are items in the item pool, these items will be used to help make up the
    difference.
    """

    souls: Optional[int] = None
    """If this is a consumable item that gives souls, the number of souls it gives."""

    useful_if: UsefulIf = UsefulIf.DEFAULT
    """Whether and when this item should be marked as "useful"."""

    filler: bool = False
    """Whether this is a candidate for a filler item to be added to fill out extra locations."""

    skip: bool = False
    """Whether to omit this item from randomization and replace it with filler or unique items."""

    @property
    def unique(self):
        """Whether this item should be unique, appearing only once in the randomizer."""
        return self.category not in {
            DS3ItemCategory.MISC, DS3ItemCategory.SOUL, DS3ItemCategory.UPGRADE,
            DS3ItemCategory.HEALING,
        }

    def __post_init__(self):
        self.ap_code = self.ap_code or DS3ItemData.__item_id
        if not self.base_name: self.base_name = self.name
        if not self.base_ds3_code: self.base_ds3_code = self.ds3_code
        DS3ItemData.__item_id += 1

    def item_groups(self) -> List[str]:
        """The names of item groups this item should appear in.

        This is computed from the properties assigned to this item."""
        names = []
        if self.classification == ItemClassification.progression: names.append("Progression")
        if self.name.startswith("Cinders of a Lord -"): names.append("Cinders")

        names.append({
            DS3ItemCategory.WEAPON_UPGRADE_5: "Weapons",
            DS3ItemCategory.WEAPON_UPGRADE_10: "Weapons",
            DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE: "Weapons",
            DS3ItemCategory.SHIELD: "Shields",
            DS3ItemCategory.SHIELD_INFUSIBLE: "Shields",
            DS3ItemCategory.ARMOR: "Armor",
            DS3ItemCategory.RING: "Rings",
            DS3ItemCategory.SPELL: "Spells",
            DS3ItemCategory.MISC: "Miscellaneous",
            DS3ItemCategory.UNIQUE: "Unique",
            DS3ItemCategory.BOSS: "Boss Souls",
            DS3ItemCategory.SOUL: "Small Souls",
            DS3ItemCategory.UPGRADE: "Upgrade",
            DS3ItemCategory.HEALING: "Healing",
        }[self.category])

        return names

    def counts(self, counts: List[int]) -> Generator["DS3ItemData", None, None]:
        """Returns an iterable of copies of this item with the given counts."""
        yield self
        for count in counts:
            yield dataclasses.replace(
                self,
                ap_code = None,
                name = "{} x{}".format(self.base_name, count),
                base_name = self.base_name,
                count = count,
                filler = False, # Don't count multiples as filler by default
            )

    @property
    def is_infused(self) -> bool:
        """Returns whether this item is an infused weapon."""
        return cast(int, self.ds3_code) - cast(int, self.base_ds3_code) >= 100

    def infuse(self, infusion: Infusion) -> "DS3ItemData":
        """Returns this item with the given infusion applied."""
        if not self.category.is_infusible: raise RuntimeError(f"{self.name} is not infusible.")
        if self.is_infused:
            raise RuntimeError(f"{self.name} is already infused.")

        # We can't change the name or AP code when infusing/upgrading weapons, because they both
        # need to match what's in item_name_to_id. We don't want to add every possible
        # infusion/upgrade combination to that map because it's way too many items.
        return dataclasses.replace(
            self,
            name = self.name,
            ds3_code = cast(int, self.ds3_code) + infusion.value,
            filler = False,
        )

    @property
    def is_upgraded(self) -> bool:
        """Returns whether this item is a weapon that's upgraded beyond level 0."""
        return (cast(int, self.ds3_code) - cast(int, self.base_ds3_code)) % 100 != 0

    def upgrade(self, level: int) -> "DS3ItemData":
        """Upgrades this item to the given level."""
        if not self.category.upgrade_level: raise RuntimeError(f"{self.name} is not upgradable.")
        if level > self.category.upgrade_level:
            raise RuntimeError(f"{self.name} can't be upgraded to +{level}.")
        if self.is_upgraded:
            raise RuntimeError(f"{self.name} is already upgraded.")

        # We can't change the name or AP code when infusing/upgrading weapons, because they both
        # need to match what's in item_name_to_id. We don't want to add every possible
        # infusion/upgrade combination to that map because it's way too many items.
        return dataclasses.replace(
            self,
            name = self.name,
            ds3_code = cast(int, self.ds3_code) + level,
            filler = False,
        )


class DarkSouls3Item(Item):
    game: str = "Dark Souls III"
    data: DS3ItemData

    @property
    def level(self) -> Optional[int]:
        """This item's upgrade level, if it's a weapon."""
        return cast(int, self.data.ds3_code) % 100 if self.data.category.upgrade_level else None

    def __init__(
            self,
            player: int,
            data: DS3ItemData,
            classification = None):
        super().__init__(data.name, classification or data.classification, data.ap_code, player)
        self.data = data

    @staticmethod
    def event(name: str, player: int) -> "DarkSouls3Item":
        data = DS3ItemData(name, None, DS3ItemCategory.MISC,
                           skip = True, classification = ItemClassification.progression)
        data.ap_code = None
        return DarkSouls3Item(player, data)


_vanilla_items = [
    # Ammunition
    *DS3ItemData("Standard Arrow",                      0x00061A80, DS3ItemCategory.MISC).counts([12]),
    DS3ItemData("Standard Arrow x8",                   0x00061A80, DS3ItemCategory.MISC, count = 8, filler = True),
    DS3ItemData("Fire Arrow",                          0x00061AE4, DS3ItemCategory.MISC),
    DS3ItemData("Fire Arrow x8",                       0x00061AE4, DS3ItemCategory.MISC, count = 8, filler = True),
    *DS3ItemData("Poison Arrow",                        0x00061B48, DS3ItemCategory.MISC).counts([18]),
    DS3ItemData("Poison Arrow x8",                     0x00061B48, DS3ItemCategory.MISC, count = 8, filler = True),
    DS3ItemData("Large Arrow",                         0x00061BAC, DS3ItemCategory.MISC),
    DS3ItemData("Feather Arrow",                       0x00061C10, DS3ItemCategory.MISC),
    *DS3ItemData("Moonlight Arrow",                     0x00061C74, DS3ItemCategory.MISC).counts([6]),
    DS3ItemData("Wood Arrow",                          0x00061CD8, DS3ItemCategory.MISC),
    DS3ItemData("Dark Arrow",                          0x00061D3C, DS3ItemCategory.MISC),
    *DS3ItemData("Dragonslayer Greatarrow",             0x00062250, DS3ItemCategory.MISC).counts([5]),
    *DS3ItemData("Dragonslayer Lightning Arrow",        0x00062318, DS3ItemCategory.MISC).counts([10]),
    *DS3ItemData("Onislayer Greatarrow",                0x0006237C, DS3ItemCategory.MISC).counts([8]),
    DS3ItemData("Standard Bolt",                       0x00062A20, DS3ItemCategory.MISC),
    DS3ItemData("Heavy Bolt",                          0x00062A84, DS3ItemCategory.MISC),
    *DS3ItemData("Sniper Bolt",                         0x00062AE8, DS3ItemCategory.MISC).counts([11]),
    DS3ItemData("Wood Bolt",                           0x00062B4C, DS3ItemCategory.MISC),
    *DS3ItemData("Lightning Bolt",                      0x00062BB0, DS3ItemCategory.MISC).counts([9]),
    *DS3ItemData("Lightning Bolt",                      0x00062BB0, DS3ItemCategory.MISC).counts([12]),
    DS3ItemData("Splintering Bolt",                    0x00062C14, DS3ItemCategory.MISC),
    *DS3ItemData("Exploding Bolt",                      0x00062C78, DS3ItemCategory.MISC).counts([6]),

    # Weapons
    DS3ItemData("Dagger",                              0x000F4240, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Bandit's Knife",                      0x000F6950, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Parrying Dagger",                     0x000F9060, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Rotten Ghru Dagger",                  0x000FDE80, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Harpe",                               0x00102CA0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Scholar's Candlestick",               0x001053B0, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Tailbone Short Sword",                0x00107AC0, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Corvian Greatknife",                  0x0010A1D0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Handmaid's Dagger",                   0x00111700, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Shortsword",                          0x001E8480, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Longsword",                           0x001EAB90, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Broadsword",                          0x001ED2A0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Broken Straight Sword",               0x001EF9B0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Lothric Knight Sword",                0x001F6EE0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Sunlight Straight Sword",             0x00203230, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Rotten Ghru Curved Sword",            0x00205940, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Irithyll Straight Sword",             0x0020A760, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Cleric's Candlestick",                0x0020F580, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Morion Blade",                        0x002143A0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Astora Straight Sword",               0x002191C0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Barbed Straight Sword",               0x0021B8D0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Executioner's Greatsword",            0x0021DFE0, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Anri's Straight Sword",               0x002206F0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Estoc",                               0x002DC6C0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Mail Breaker",                        0x002DEDD0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Rapier",                              0x002E14E0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Ricard's Rapier",                     0x002E3BF0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Crystal Sage's Rapier",               0x002E6300, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Irithyll Rapier",                     0x002E8A10, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Shotel",                              0x003D3010, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Scimitar",                            0x003D7E30, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Falchion",                            0x003DA540, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Carthus Curved Sword",                0x003DCC50, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Carthus Curved Greatsword",           0x003DF360, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Pontiff Knight Curved Sword",         0x003E1A70, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Storm Curved Sword",                  0x003E4180, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Painting Guardian's Curved Sword",    0x003E6890, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Crescent Moon Sword",                 0x003E8FA0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Carthus Shotel",                      0x003EB6B0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Uchigatana",                          0x004C4B40, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Washing Pole",                        0x004C7250, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Chaos Blade",                         0x004C9960, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Black Blade",                         0x004CC070, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Bloodlust",                           0x004CE780, DS3ItemCategory.WEAPON_UPGRADE_5,
                inject = True), # Covenant reward
    DS3ItemData("Darkdrift",                           0x004D0E90, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Bastard Sword",                       0x005B8D80, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Claymore",                            0x005BDBA0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Zweihander",                          0x005C29C0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Greatsword",                          0x005C50D0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Astora Greatsword",                   0x005C9EF0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Murakumo",                            0x005CC600, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Lothric Knight Greatsword",           0x005D1420, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Flamberge",                           0x005DB060, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Exile Greatsword",                    0x005DD770, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Greatsword of Judgment",              0x005E2590, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Profaned Greatsword",                 0x005E4CA0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Cathedral Knight Greatsword",         0x005E73B0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Farron Greatsword",                   0x005E9AC0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Yhorm's Great Machete",               0x005F0FF0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Dark Sword",                          0x005F3700, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Black Knight Sword",                  0x005F5E10, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Lorian's Greatsword",                 0x005F8520, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Twin Princes' Greatsword",            0x005FAC30, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Lothric's Holy Sword",                0x005FD340, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Wolnir's Holy Sword",                 0x005FFA50, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Wolf Knight's Greatsword",            0x00602160, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Greatsword of Artorias",              0x0060216A, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Hollowslayer Greatsword",             0x00604870, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Moonlight Greatsword",                0x00606F80, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Drakeblood Greatsword",               0x00609690, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Firelink Greatsword",                 0x0060BDA0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Fume Ultra Greatsword",               0x0060E4B0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Old Wolf Curved Sword",               0x00610BC0, DS3ItemCategory.WEAPON_UPGRADE_5,
                inject = True), # Covenant reward
    DS3ItemData("Storm Ruler",                         0x006132D0, DS3ItemCategory.WEAPON_UPGRADE_5,
                classification = ItemClassification.progression),
    DS3ItemData("Hand Axe",                            0x006ACFC0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Battle Axe",                          0x006AF6D0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Deep Battle Axe",                     0x006AFA54, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Brigand Axe",                         0x006B1DE0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Crescent Axe",                        0x006B6C00, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Greataxe",                            0x006B9310, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Butcher Knife",                       0x006BE130, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Dragonslayer's Axe",                  0x006C0840, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Thrall Axe",                          0x006C5660, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Dragonslayer Greataxe",               0x006C7D70, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Demon's Greataxe",                    0x006CA480, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Eleonora",                            0x006CCB90, DS3ItemCategory.WEAPON_UPGRADE_5,
                classification = ItemClassification.progression), # Crow trade
    DS3ItemData("Man Serpent Hatchet",                 0x006D19B0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Club",                                0x007A1200, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Mace",                                0x007A3910, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Morning Star",                        0x007A6020, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Reinforced Club",                     0x007A8730, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Large Club",                          0x007AFC60, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Great Club",                          0x007B4A80, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Great Mace",                          0x007BBFB0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Great Wooden Hammer",                 0x007C8300, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Gargoyle Flame Hammer",               0x007CAA10, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Vordt's Great Hammer",                0x007CD120, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Old King's Great Hammer",             0x007CF830, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Heysel Pick",                         0x007D6D60, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Warpick",                             0x007DBB80, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Pickaxe",                             0x007DE290, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Dragon Tooth",                        0x007E09A0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Smough's Great Hammer",               0x007E30B0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Blacksmith Hammer",                   0x007E57C0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE,
                classification = ItemClassification.progression), # Crow trade
    DS3ItemData("Morne's Great Hammer",                0x007E7ED0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Spiked Mace",                         0x007EA5E0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Spear",                               0x00895440, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Winged Spear",                        0x00897B50, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Partizan",                            0x0089C970, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Greatlance",                          0x008A8CC0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Lothric Knight Long Spear",           0x008AB3D0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Gargoyle Flame Spear",                0x008B01F0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Rotten Ghru Spear",                   0x008B2900, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Tailbone Spear",                      0x008B5010, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Soldering Iron",                      0x008B7720, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Dragonslayer Swordspear",             0x008BC540, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Arstor's Spear",                      0x008BEC50, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Saint Bident",                        0x008C1360, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Yorshka's Spear",                     0x008C3A70, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Pike",                                0x008C6180, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Heavy Four-pronged Plow",             0x008ADAE0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Dragonslayer Spear",                  0x008CAFA0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Great Scythe",                        0x00989680, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Lucerne",                             0x0098BD90, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Glaive",                              0x0098E4A0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Halberd",                             0x00990BB0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Black Knight Greataxe",               0x009959D0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Pontiff Knight Great Scythe",         0x0099A7F0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Great Corvian Scythe",                0x0099CF00, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Winged Knight Halberd",               0x0099F610, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Gundyr's Halberd",                    0x009A1D20, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Red Hilted Halberd",                  0x009AB960, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Black Knight Glaive",                 0x009AE070, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Immolation Tinder",                   0x009B0780, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Claw",                                0x00A7D8C0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Caestus",                             0x00A7FFD0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Manikin Claws",                       0x00A826E0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Demon's Fist",                        0x00A84DF0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Dark Hand",                           0x00A87500, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Whip",                                0x00B71B00, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Witch's Locks",                       0x00B7B740, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Notched Whip",                        0x00B7DE50, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Spotted Whip",                        0x00B80560, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Talisman",                            0x00C72090, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Sorcerer's Staff",                    0x00C747A0, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Storyteller's Staff",                 0x00C76EB0, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Mendicant's Staff",                   0x00C795C0, DS3ItemCategory.WEAPON_UPGRADE_10,
                classification = ItemClassification.progression, # Crow trade
                inject = True), # This is just a random drop normally, but we need it in-logic
    DS3ItemData("Man-grub's Staff",                    0x00C7E3E0, DS3ItemCategory.WEAPON_UPGRADE_5,
                inject = True), # Covenant reward
    DS3ItemData("Archdeacon's Great Staff",            0x00C80AF0, DS3ItemCategory.WEAPON_UPGRADE_5,
                inject = True), # Covenant reward
    DS3ItemData("Golden Ritual Spear",                 0x00C83200, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Yorshka's Chime",                     0x00C88020, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Sage's Crystal Staff",                0x00C8CE40, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Heretic's Staff",                     0x00C8F550, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Court Sorcerer's Staff",              0x00C91C60, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Witchtree Branch",                    0x00C94370, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Izalith Staff",                       0x00C96A80, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Cleric's Sacred Chime",               0x00C99190, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Priest's Chime",                      0x00C9B8A0, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Saint-tree Bellvine",                 0x00C9DFB0, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Caitha's Chime",                      0x00CA06C0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Crystal Chime",                       0x00CA2DD0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Sunlight Talisman",                   0x00CA54E0, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Canvas Talisman",                     0x00CA7BF0, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Sunless Talisman",                    0x00CAA300, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Saint's Talisman",                    0x00CACA10, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("White Hair Talisman",                 0x00CAF120, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Pyromancy Flame",                     0x00CC77C0, DS3ItemCategory.WEAPON_UPGRADE_10,
                classification = ItemClassification.progression),
    DS3ItemData("Dragonslayer Greatbow",               0x00CF8500, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Short Bow",                           0x00D5C690, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Composite Bow",                       0x00D5EDA0, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Light Crossbow",                      0x00D63BC0, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Arbalest",                            0x00D662D0, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Longbow",                             0x00D689E0, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Dragonrider Bow",                     0x00D6B0F0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Avelyn",                              0x00D6FF10, DS3ItemCategory.WEAPON_UPGRADE_10,
                classification = ItemClassification.progression), # Crow trade
    DS3ItemData("Knight's Crossbow",                   0x00D72620, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Heavy Crossbow",                      0x00D74D30, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Darkmoon Longbow",                    0x00D79B50, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Onislayer Greatbow",                  0x00D7C260, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Black Bow of Pharis",                 0x00D7E970, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Sniper Crossbow",                     0x00D83790, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Sellsword Twinblades",                0x00F42400, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Warden Twinblades",                   0x00F47220, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Winged Knight Twinaxes",              0x00F49930, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Dancer's Enchanted Swords",           0x00F4C040, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Great Machete",                       0x00F4E750, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Brigand Twindaggers",                 0x00F50E60, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Gotthard Twinswords",                 0x00F53570, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Onikiri and Ubadachi",                0x00F58390, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Drang Twinspears",                    0x00F5AAA0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Drang Hammers",                       0x00F61FD0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),

    # Shields
    DS3ItemData("Buckler",                             0x01312D00, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Small Leather Shield",                0x01315410, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Round Shield",                        0x0131A230, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Large Leather Shield",                0x0131C940, DS3ItemCategory.SHIELD_INFUSIBLE,
                classification = ItemClassification.progression, # Crow trade
                inject = True), # This is a shop/infinite drop item, but we need it in logic
    DS3ItemData("Hawkwood's Shield",                   0x01323E70, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Iron Round Shield",                   0x01326580, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Wooden Shield",                       0x0132DAB0, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Kite Shield",                         0x013301C0, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Ghru Rotshield",                      0x013328D0, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Havel's Greatshield",                 0x013376F0, DS3ItemCategory.SHIELD),
    DS3ItemData("Target Shield",                       0x01339E00, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Elkhorn Round Shield",                0x0133C510, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Warrior's Round Shield",              0x0133EC20, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Caduceus Round Shield",               0x01341330, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Red and White Shield",                0x01343A40, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Blessed Red and White Shield+1",      0x01343FB9, DS3ItemCategory.SHIELD),
    DS3ItemData("Plank Shield",                        0x01346150, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Leather Shield",                      0x01348860, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Crimson Parma",                       0x0134AF70, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Eastern Iron Shield",                 0x0134D680, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Llewellyn Shield",                    0x0134FD90, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Golden Falcon Shield",                0x01354BB0, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Sacred Bloom Shield",                 0x013572C0, DS3ItemCategory.SHIELD),
    DS3ItemData("Ancient Dragon Greatshield",          0x013599D0, DS3ItemCategory.SHIELD),
    DS3ItemData("Lothric Knight Shield",               0x01409650, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Knight Shield",                       0x01410B80, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Pontiff Knight Shield",               0x014159A0, DS3ItemCategory.SHIELD),
    DS3ItemData("Carthus Shield",                      0x014180B0, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Black Knight Shield",                 0x0141F5E0, DS3ItemCategory.SHIELD),
    DS3ItemData("Silver Knight Shield",                0x01424400, DS3ItemCategory.SHIELD),
    DS3ItemData("Spiked Shield",                       0x01426B10, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Pierce Shield",                       0x01429220, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("East-West Shield",                    0x0142B930, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Sunlight Shield",                     0x0142E040, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Crest Shield",                        0x01430750, DS3ItemCategory.SHIELD),
    DS3ItemData("Dragon Crest Shield",                 0x01432E60, DS3ItemCategory.SHIELD),
    DS3ItemData("Spider Shield",                       0x01435570, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Grass Crest Shield",                  0x01437C80, DS3ItemCategory.SHIELD,
                classification = ItemClassification.useful),
    DS3ItemData("Sunset Shield",                       0x0143A390, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Golden Wing Crest Shield",            0x0143CAA0, DS3ItemCategory.SHIELD),
    DS3ItemData("Blue Wooden Shield",                  0x0143F1B0, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Silver Eagle Kite Shield",            0x014418C0, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Stone Parma",                         0x01443FD0, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Spirit Tree Crest Shield",            0x014466E0, DS3ItemCategory.SHIELD),
    DS3ItemData("Porcine Shield",                      0x01448DF0, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Shield of Want",                      0x0144B500, DS3ItemCategory.SHIELD),
    DS3ItemData("Wargod Wooden Shield",                0x0144DC10, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Lothric Knight Greatshield",          0x014FD890, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Cathedral Knight Greatshield",        0x014FFFA0, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Dragonslayer Greatshield",            0x01504DC0, DS3ItemCategory.SHIELD),
    DS3ItemData("Moaning Shield",                      0x015074D0, DS3ItemCategory.SHIELD,
                classification = ItemClassification.progression), # Crow trade
    DS3ItemData("Yhorm's Greatshield",                 0x0150C2F0, DS3ItemCategory.SHIELD),
    DS3ItemData("Black Iron Greatshield",              0x0150EA00, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Wolf Knight's Greatshield",           0x01511110, DS3ItemCategory.SHIELD,
                inject = True), # Covenant reward
    DS3ItemData("Twin Dragon Greatshield",             0x01513820, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Greatshield of Glory",                0x01515F30, DS3ItemCategory.SHIELD),
    DS3ItemData("Curse Ward Greatshield",              0x01518640, DS3ItemCategory.SHIELD),
    DS3ItemData("Bonewheel Shield",                    0x0151AD50, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Stone Greatshield",                   0x0151D460, DS3ItemCategory.SHIELD_INFUSIBLE),

    # Armor
    DS3ItemData("Fallen Knight Helm",                  0x1121EAC0, DS3ItemCategory.ARMOR),
    DS3ItemData("Fallen Knight Armor",                 0x1121EEA8, DS3ItemCategory.ARMOR),
    DS3ItemData("Fallen Knight Gauntlets",             0x1121F290, DS3ItemCategory.ARMOR),
    DS3ItemData("Fallen Knight Trousers",              0x1121F678, DS3ItemCategory.ARMOR),
    DS3ItemData("Knight Helm",                         0x11298BE0, DS3ItemCategory.ARMOR),
    DS3ItemData("Knight Armor",                        0x11298FC8, DS3ItemCategory.ARMOR),
    DS3ItemData("Knight Gauntlets",                    0x112993B0, DS3ItemCategory.ARMOR),
    DS3ItemData("Knight Leggings",                     0x11299798, DS3ItemCategory.ARMOR),
    DS3ItemData("Firelink Helm",                       0x11406F40, DS3ItemCategory.ARMOR),
    DS3ItemData("Firelink Armor",                      0x11407328, DS3ItemCategory.ARMOR),
    DS3ItemData("Firelink Gauntlets",                  0x11407710, DS3ItemCategory.ARMOR),
    DS3ItemData("Firelink Leggings",                   0x11407AF8, DS3ItemCategory.ARMOR),
    DS3ItemData("Sellsword Helm",                      0x11481060, DS3ItemCategory.ARMOR),
    DS3ItemData("Sellsword Armor",                     0x11481448, DS3ItemCategory.ARMOR),
    DS3ItemData("Sellsword Gauntlet",                  0x11481830, DS3ItemCategory.ARMOR),
    DS3ItemData("Sellsword Trousers",                  0x11481C18, DS3ItemCategory.ARMOR),
    DS3ItemData("Herald Helm",                         0x114FB180, DS3ItemCategory.ARMOR),
    DS3ItemData("Herald Armor",                        0x114FB568, DS3ItemCategory.ARMOR),
    DS3ItemData("Herald Gloves",                       0x114FB950, DS3ItemCategory.ARMOR),
    DS3ItemData("Herald Trousers",                     0x114FBD38, DS3ItemCategory.ARMOR),
    DS3ItemData("Sunless Veil",                        0x115752A0, DS3ItemCategory.ARMOR),
    DS3ItemData("Sunless Armor",                       0x11575688, DS3ItemCategory.ARMOR),
    DS3ItemData("Sunless Gauntlets",                   0x11575A70, DS3ItemCategory.ARMOR),
    DS3ItemData("Sunless Leggings",                    0x11575E58, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Hand Hat",                      0x115EF3C0, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Hand Armor",                    0x115EF7A8, DS3ItemCategory.ARMOR),
    DS3ItemData("Assassin Gloves",                     0x115EFB90, DS3ItemCategory.ARMOR),
    DS3ItemData("Assassin Trousers",                   0x115EFF78, DS3ItemCategory.ARMOR),
    DS3ItemData("Assassin Hood",                       0x11607A60, DS3ItemCategory.ARMOR),
    DS3ItemData("Assassin Armor",                      0x11607E48, DS3ItemCategory.ARMOR),
    DS3ItemData("Xanthous Crown",                      0x116694E0, DS3ItemCategory.ARMOR,
                classification = ItemClassification.progression), # Crow trade
    DS3ItemData("Xanthous Overcoat",                   0x116698C8, DS3ItemCategory.ARMOR),
    DS3ItemData("Xanthous Gloves",                     0x11669CB0, DS3ItemCategory.ARMOR),
    DS3ItemData("Xanthous Trousers",                   0x1166A098, DS3ItemCategory.ARMOR),
    DS3ItemData("Northern Helm",                       0x116E3600, DS3ItemCategory.ARMOR),
    DS3ItemData("Northern Armor",                      0x116E39E8, DS3ItemCategory.ARMOR),
    DS3ItemData("Northern Gloves",                     0x116E3DD0, DS3ItemCategory.ARMOR),
    DS3ItemData("Northern Trousers",                   0x116E41B8, DS3ItemCategory.ARMOR),
    DS3ItemData("Morne's Helm",                        0x1175D720, DS3ItemCategory.ARMOR),
    DS3ItemData("Morne's Armor",                       0x1175DB08, DS3ItemCategory.ARMOR),
    DS3ItemData("Morne's Gauntlets",                   0x1175DEF0, DS3ItemCategory.ARMOR),
    DS3ItemData("Morne's Leggings",                    0x1175E2D8, DS3ItemCategory.ARMOR),
    DS3ItemData("Silver Mask",                         0x117D7840, DS3ItemCategory.ARMOR),
    DS3ItemData("Leonhard's Garb",                     0x117D7C28, DS3ItemCategory.ARMOR),
    DS3ItemData("Leonhard's Gauntlets",                0x117D8010, DS3ItemCategory.ARMOR),
    DS3ItemData("Leonhard's Trousers",                 0x117D83F8, DS3ItemCategory.ARMOR),
    DS3ItemData("Sneering Mask",                       0x11851960, DS3ItemCategory.ARMOR),
    DS3ItemData("Pale Shade Robe",                     0x11851D48, DS3ItemCategory.ARMOR),
    DS3ItemData("Pale Shade Gloves",                   0x11852130, DS3ItemCategory.ARMOR),
    DS3ItemData("Pale Shade Trousers",                 0x11852518, DS3ItemCategory.ARMOR),
    DS3ItemData("Sunset Helm",                         0x118CBA80, DS3ItemCategory.ARMOR),
    DS3ItemData("Sunset Armor",                        0x118CBE68, DS3ItemCategory.ARMOR),
    DS3ItemData("Sunset Gauntlets",                    0x118CC250, DS3ItemCategory.ARMOR),
    DS3ItemData("Sunset Leggings",                     0x118CC638, DS3ItemCategory.ARMOR),
    DS3ItemData("Old Sage's Blindfold",                0x11945BA0, DS3ItemCategory.ARMOR),
    DS3ItemData("Cornyx's Garb",                       0x11945F88, DS3ItemCategory.ARMOR),
    DS3ItemData("Cornyx's Wrap",                       0x11946370, DS3ItemCategory.ARMOR),
    DS3ItemData("Cornyx's Skirt",                      0x11946758, DS3ItemCategory.ARMOR),
    DS3ItemData("Executioner Helm",                    0x119BFCC0, DS3ItemCategory.ARMOR),
    DS3ItemData("Executioner Armor",                   0x119C00A8, DS3ItemCategory.ARMOR),
    DS3ItemData("Executioner Gauntlets",               0x119C0490, DS3ItemCategory.ARMOR),
    DS3ItemData("Executioner Leggings",                0x119C0878, DS3ItemCategory.ARMOR),
    DS3ItemData("Billed Mask",                         0x11A39DE0, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Dress",                         0x11A3A1C8, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Gauntlets",                     0x11A3A5B0, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Leggings",                      0x11A3A998, DS3ItemCategory.ARMOR),
    DS3ItemData("Pyromancer Crown",                    0x11AB3F00, DS3ItemCategory.ARMOR),
    DS3ItemData("Pyromancer Garb",                     0x11AB42E8, DS3ItemCategory.ARMOR),
    DS3ItemData("Pyromancer Wrap",                     0x11AB46D0, DS3ItemCategory.ARMOR),
    DS3ItemData("Pyromancer Trousers",                 0x11AB4AB8, DS3ItemCategory.ARMOR),
    DS3ItemData("Court Sorcerer Hood",                 0x11BA8140, DS3ItemCategory.ARMOR),
    DS3ItemData("Court Sorcerer Robe",                 0x11BA8528, DS3ItemCategory.ARMOR),
    DS3ItemData("Court Sorcerer Gloves",               0x11BA8910, DS3ItemCategory.ARMOR),
    DS3ItemData("Court Sorcerer Trousers",             0x11BA8CF8, DS3ItemCategory.ARMOR),
    DS3ItemData("Sorcerer Hood",                       0x11C9C380, DS3ItemCategory.ARMOR),
    DS3ItemData("Sorcerer Robe",                       0x11C9C768, DS3ItemCategory.ARMOR),
    DS3ItemData("Sorcerer Gloves",                     0x11C9CB50, DS3ItemCategory.ARMOR),
    DS3ItemData("Sorcerer Trousers",                   0x11C9CF38, DS3ItemCategory.ARMOR),
    DS3ItemData("Clandestine Coat",                    0x11CB4E08, DS3ItemCategory.ARMOR),
    DS3ItemData("Cleric Hat",                          0x11D905C0, DS3ItemCategory.ARMOR),
    DS3ItemData("Cleric Blue Robe",                    0x11D909A8, DS3ItemCategory.ARMOR),
    DS3ItemData("Cleric Gloves",                       0x11D90D90, DS3ItemCategory.ARMOR),
    DS3ItemData("Cleric Trousers",                     0x11D91178, DS3ItemCategory.ARMOR),
    DS3ItemData("Steel Soldier Helm",                  0x12625A00, DS3ItemCategory.ARMOR),
    DS3ItemData("Deserter Armor",                      0x12625DE8, DS3ItemCategory.ARMOR),
    DS3ItemData("Deserter Trousers",                   0x126265B8, DS3ItemCategory.ARMOR),
    DS3ItemData("Thief Mask",                          0x12656740, DS3ItemCategory.ARMOR),
    DS3ItemData("Sage's Big Hat",                      0x129020C0, DS3ItemCategory.ARMOR),
    DS3ItemData("Aristocrat's Mask",                   0x129F6300, DS3ItemCategory.ARMOR),
    DS3ItemData("Jailer Robe",                         0x129F66E8, DS3ItemCategory.ARMOR),
    DS3ItemData("Jailer Gloves",                       0x129F6AD0, DS3ItemCategory.ARMOR),
    DS3ItemData("Jailer Trousers",                     0x129F6EB8, DS3ItemCategory.ARMOR),
    DS3ItemData("Grave Warden Hood",                   0x12BDE780, DS3ItemCategory.ARMOR),
    DS3ItemData("Grave Warden Robe",                   0x12BDEB68, DS3ItemCategory.ARMOR),
    DS3ItemData("Grave Warden Wrap",                   0x12BDEF50, DS3ItemCategory.ARMOR),
    DS3ItemData("Grave Warden Skirt",                  0x12BDF338, DS3ItemCategory.ARMOR),
    DS3ItemData("Worker Hat",                          0x12CD29C0, DS3ItemCategory.ARMOR),
    DS3ItemData("Worker Garb",                         0x12CD2DA8, DS3ItemCategory.ARMOR),
    DS3ItemData("Worker Gloves",                       0x12CD3190, DS3ItemCategory.ARMOR),
    DS3ItemData("Worker Trousers",                     0x12CD3578, DS3ItemCategory.ARMOR),
    DS3ItemData("Thrall Hood",                         0x12D4CAE0, DS3ItemCategory.ARMOR),
    DS3ItemData("Evangelist Hat",                      0x12DC6C00, DS3ItemCategory.ARMOR),
    DS3ItemData("Evangelist Robe",                     0x12DC6FE8, DS3ItemCategory.ARMOR),
    DS3ItemData("Evangelist Gloves",                   0x12DC73D0, DS3ItemCategory.ARMOR),
    DS3ItemData("Evangelist Trousers",                 0x12DC77B8, DS3ItemCategory.ARMOR),
    DS3ItemData("Scholar's Robe",                      0x12E41108, DS3ItemCategory.ARMOR),
    DS3ItemData("Winged Knight Helm",                  0x12EBAE40, DS3ItemCategory.ARMOR),
    DS3ItemData("Winged Knight Armor",                 0x12EBB228, DS3ItemCategory.ARMOR),
    DS3ItemData("Winged Knight Gauntlets",             0x12EBB610, DS3ItemCategory.ARMOR),
    DS3ItemData("Winged Knight Leggings",              0x12EBB9F8, DS3ItemCategory.ARMOR),
    DS3ItemData("Cathedral Knight Helm",               0x130291A0, DS3ItemCategory.ARMOR),
    DS3ItemData("Cathedral Knight Armor",              0x13029588, DS3ItemCategory.ARMOR),
    DS3ItemData("Cathedral Knight Gauntlets",          0x13029970, DS3ItemCategory.ARMOR),
    DS3ItemData("Cathedral Knight Leggings",           0x13029D58, DS3ItemCategory.ARMOR),
    DS3ItemData("Lothric Knight Helm",                 0x13197500, DS3ItemCategory.ARMOR),
    DS3ItemData("Lothric Knight Armor",                0x131978E8, DS3ItemCategory.ARMOR),
    DS3ItemData("Lothric Knight Gauntlets",            0x13197CD0, DS3ItemCategory.ARMOR),
    DS3ItemData("Lothric Knight Leggings",             0x131980B8, DS3ItemCategory.ARMOR),
    DS3ItemData("Outrider Knight Helm",                0x1328B740, DS3ItemCategory.ARMOR),
    DS3ItemData("Outrider Knight Armor",               0x1328BB28, DS3ItemCategory.ARMOR),
    DS3ItemData("Outrider Knight Gauntlets",           0x1328BF10, DS3ItemCategory.ARMOR),
    DS3ItemData("Outrider Knight Leggings",            0x1328C2F8, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Knight Helm",                   0x1337F980, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Knight Armor",                  0x1337FD68, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Knight Gauntlets",              0x13380150, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Knight Leggings",               0x13380538, DS3ItemCategory.ARMOR),
    DS3ItemData("Dark Mask",                           0x133F9AA0, DS3ItemCategory.ARMOR),
    DS3ItemData("Dark Armor",                          0x133F9E88, DS3ItemCategory.ARMOR),
    DS3ItemData("Dark Gauntlets",                      0x133FA270, DS3ItemCategory.ARMOR),
    DS3ItemData("Dark Leggings",                       0x133FA658, DS3ItemCategory.ARMOR),
    DS3ItemData("Exile Mask",                          0x13473BC0, DS3ItemCategory.ARMOR),
    DS3ItemData("Exile Armor",                         0x13473FA8, DS3ItemCategory.ARMOR),
    DS3ItemData("Exile Gauntlets",                     0x13474390, DS3ItemCategory.ARMOR),
    DS3ItemData("Exile Leggings",                      0x13474778, DS3ItemCategory.ARMOR),
    DS3ItemData("Pontiff Knight Crown",                0x13567E00, DS3ItemCategory.ARMOR),
    DS3ItemData("Pontiff Knight Armor",                0x135681E8, DS3ItemCategory.ARMOR),
    DS3ItemData("Pontiff Knight Gauntlets",            0x135685D0, DS3ItemCategory.ARMOR),
    DS3ItemData("Pontiff Knight Leggings",             0x135689B8, DS3ItemCategory.ARMOR),
    DS3ItemData("Golden Crown",                        0x1365C040, DS3ItemCategory.ARMOR),
    DS3ItemData("Dragonscale Armor",                   0x1365C428, DS3ItemCategory.ARMOR),
    DS3ItemData("Golden Bracelets",                    0x1365C810, DS3ItemCategory.ARMOR),
    DS3ItemData("Dragonscale Waistcloth",              0x1365CBF8, DS3ItemCategory.ARMOR),
    DS3ItemData("Wolnir's Crown",                      0x136D6160, DS3ItemCategory.ARMOR),
    DS3ItemData("Undead Legion Helm",                  0x13750280, DS3ItemCategory.ARMOR),
    DS3ItemData("Undead Legion Armor",                 0x13750668, DS3ItemCategory.ARMOR),
    DS3ItemData("Undead Legion Gauntlet",              0x13750A50, DS3ItemCategory.ARMOR),
    DS3ItemData("Undead Legion Leggings",              0x13750E38, DS3ItemCategory.ARMOR),
    DS3ItemData("Fire Witch Helm",                     0x13938700, DS3ItemCategory.ARMOR),
    DS3ItemData("Fire Witch Armor",                    0x13938AE8, DS3ItemCategory.ARMOR),
    DS3ItemData("Fire Witch Gauntlets",                0x13938ED0, DS3ItemCategory.ARMOR),
    DS3ItemData("Fire Witch Leggings",                 0x139392B8, DS3ItemCategory.ARMOR),
    DS3ItemData("Lorian's Helm",                       0x13A2C940, DS3ItemCategory.ARMOR),
    DS3ItemData("Lorian's Armor",                      0x13A2CD28, DS3ItemCategory.ARMOR),
    DS3ItemData("Lorian's Gauntlets",                  0x13A2D110, DS3ItemCategory.ARMOR),
    DS3ItemData("Lorian's Leggings",                   0x13A2D4F8, DS3ItemCategory.ARMOR),
    DS3ItemData("Hood of Prayer",                      0x13AA6A60, DS3ItemCategory.ARMOR),
    DS3ItemData("Robe of Prayer",                      0x13AA6E48, DS3ItemCategory.ARMOR),
    DS3ItemData("Skirt of Prayer",                     0x13AA7618, DS3ItemCategory.ARMOR),
    DS3ItemData("Dancer's Crown",                      0x13C14DC0, DS3ItemCategory.ARMOR),
    DS3ItemData("Dancer's Armor",                      0x13C151A8, DS3ItemCategory.ARMOR),
    DS3ItemData("Dancer's Gauntlets",                  0x13C15590, DS3ItemCategory.ARMOR),
    DS3ItemData("Dancer's Leggings",                   0x13C15978, DS3ItemCategory.ARMOR),
    DS3ItemData("Gundyr's Helm",                       0x13D09000, DS3ItemCategory.ARMOR),
    DS3ItemData("Gundyr's Armor",                      0x13D093E8, DS3ItemCategory.ARMOR),
    DS3ItemData("Gundyr's Gauntlets",                  0x13D097D0, DS3ItemCategory.ARMOR),
    DS3ItemData("Gundyr's Leggings",                   0x13D09BB8, DS3ItemCategory.ARMOR),
    DS3ItemData("Archdeacon White Crown",              0x13EF1480, DS3ItemCategory.ARMOR),
    DS3ItemData("Archdeacon Holy Garb",                0x13EF1868, DS3ItemCategory.ARMOR),
    DS3ItemData("Archdeacon Skirt",                    0x13EF2038, DS3ItemCategory.ARMOR),
    DS3ItemData("Deacon Robe",                         0x13F6B988, DS3ItemCategory.ARMOR),
    DS3ItemData("Deacon Skirt",                        0x13F6C158, DS3ItemCategory.ARMOR),
    DS3ItemData("Fire Keeper Robe",                    0x140D9CE8, DS3ItemCategory.ARMOR),
    DS3ItemData("Fire Keeper Gloves",                  0x140DA0D0, DS3ItemCategory.ARMOR),
    DS3ItemData("Fire Keeper Skirt",                   0x140DA4B8, DS3ItemCategory.ARMOR),
    DS3ItemData("Chain Helm",                          0x142C1D80, DS3ItemCategory.ARMOR),
    DS3ItemData("Chain Armor",                         0x142C2168, DS3ItemCategory.ARMOR),
    DS3ItemData("Leather Gauntlets",                   0x142C2550, DS3ItemCategory.ARMOR),
    DS3ItemData("Chain Leggings",                      0x142C2938, DS3ItemCategory.ARMOR),
    DS3ItemData("Nameless Knight Helm",                0x143B5FC0, DS3ItemCategory.ARMOR),
    DS3ItemData("Nameless Knight Armor",               0x143B63A8, DS3ItemCategory.ARMOR),
    DS3ItemData("Nameless Knight Gauntlets",           0x143B6790, DS3ItemCategory.ARMOR),
    DS3ItemData("Nameless Knight Leggings",            0x143B6B78, DS3ItemCategory.ARMOR),
    DS3ItemData("Elite Knight Helm",                   0x144AA200, DS3ItemCategory.ARMOR),
    DS3ItemData("Elite Knight Armor",                  0x144AA5E8, DS3ItemCategory.ARMOR),
    DS3ItemData("Elite Knight Gauntlets",              0x144AA9D0, DS3ItemCategory.ARMOR),
    DS3ItemData("Elite Knight Leggings",               0x144AADB8, DS3ItemCategory.ARMOR),
    DS3ItemData("Faraam Helm",                         0x1459E440, DS3ItemCategory.ARMOR),
    DS3ItemData("Faraam Armor",                        0x1459E828, DS3ItemCategory.ARMOR),
    DS3ItemData("Faraam Gauntlets",                    0x1459EC10, DS3ItemCategory.ARMOR),
    DS3ItemData("Faraam Boots",                        0x1459EFF8, DS3ItemCategory.ARMOR),
    DS3ItemData("Catarina Helm",                       0x14692680, DS3ItemCategory.ARMOR),
    DS3ItemData("Catarina Armor",                      0x14692A68, DS3ItemCategory.ARMOR),
    DS3ItemData("Catarina Gauntlets",                  0x14692E50, DS3ItemCategory.ARMOR),
    DS3ItemData("Catarina Leggings",                   0x14693238, DS3ItemCategory.ARMOR),
    DS3ItemData("Standard Helm",                       0x1470C7A0, DS3ItemCategory.ARMOR),
    DS3ItemData("Hard Leather Armor",                  0x1470CB88, DS3ItemCategory.ARMOR),
    DS3ItemData("Hard Leather Gauntlets",              0x1470CF70, DS3ItemCategory.ARMOR),
    DS3ItemData("Hard Leather Boots",                  0x1470D358, DS3ItemCategory.ARMOR),
    DS3ItemData("Havel's Helm",                        0x147868C0, DS3ItemCategory.ARMOR),
    DS3ItemData("Havel's Armor",                       0x14786CA8, DS3ItemCategory.ARMOR),
    DS3ItemData("Havel's Gauntlets",                   0x14787090, DS3ItemCategory.ARMOR),
    DS3ItemData("Havel's Leggings",                    0x14787478, DS3ItemCategory.ARMOR),
    DS3ItemData("Brigand Hood",                        0x148009E0, DS3ItemCategory.ARMOR),
    DS3ItemData("Brigand Armor",                       0x14800DC8, DS3ItemCategory.ARMOR),
    DS3ItemData("Brigand Gauntlets",                   0x148011B0, DS3ItemCategory.ARMOR),
    DS3ItemData("Brigand Trousers",                    0x14801598, DS3ItemCategory.ARMOR),
    DS3ItemData("Pharis's Hat",                        0x1487AB00, DS3ItemCategory.ARMOR),
    DS3ItemData("Leather Armor",                       0x1487AEE8, DS3ItemCategory.ARMOR),
    DS3ItemData("Leather Gloves",                      0x1487B2D0, DS3ItemCategory.ARMOR),
    DS3ItemData("Leather Boots",                       0x1487B6B8, DS3ItemCategory.ARMOR),
    DS3ItemData("Ragged Mask",                         0x148F4C20, DS3ItemCategory.ARMOR),
    DS3ItemData("Master's Attire",                     0x148F5008, DS3ItemCategory.ARMOR),
    DS3ItemData("Master's Gloves",                     0x148F53F0, DS3ItemCategory.ARMOR),
    DS3ItemData("Loincloth",                           0x148F57D8, DS3ItemCategory.ARMOR),
    DS3ItemData("Old Sorcerer Hat",                    0x1496ED40, DS3ItemCategory.ARMOR),
    DS3ItemData("Old Sorcerer Coat",                   0x1496F128, DS3ItemCategory.ARMOR),
    DS3ItemData("Old Sorcerer Gauntlets",              0x1496F510, DS3ItemCategory.ARMOR),
    DS3ItemData("Old Sorcerer Boots",                  0x1496F8F8, DS3ItemCategory.ARMOR),
    DS3ItemData("Conjurator Hood",                     0x149E8E60, DS3ItemCategory.ARMOR),
    DS3ItemData("Conjurator Robe",                     0x149E9248, DS3ItemCategory.ARMOR),
    DS3ItemData("Conjurator Manchettes",               0x149E9630, DS3ItemCategory.ARMOR),
    DS3ItemData("Conjurator Boots",                    0x149E9A18, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Leather Armor",                 0x14A63368, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Leather Gloves",                0x14A63750, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Leather Boots",                 0x14A63B38, DS3ItemCategory.ARMOR),
    DS3ItemData("Symbol of Avarice",                   0x14ADD0A0, DS3ItemCategory.ARMOR),
    DS3ItemData("Creighton's Steel Mask",              0x14B571C0, DS3ItemCategory.ARMOR),
    DS3ItemData("Mirrah Chain Mail",                   0x14B575A8, DS3ItemCategory.ARMOR),
    DS3ItemData("Mirrah Chain Gloves",                 0x14B57990, DS3ItemCategory.ARMOR),
    DS3ItemData("Mirrah Chain Leggings",               0x14B57D78, DS3ItemCategory.ARMOR),
    DS3ItemData("Maiden Hood",                         0x14BD12E0, DS3ItemCategory.ARMOR),
    DS3ItemData("Maiden Robe",                         0x14BD16C8, DS3ItemCategory.ARMOR),
    DS3ItemData("Maiden Gloves",                       0x14BD1AB0, DS3ItemCategory.ARMOR),
    DS3ItemData("Maiden Skirt",                        0x14BD1E98, DS3ItemCategory.ARMOR),
    DS3ItemData("Alva Helm",                           0x14C4B400, DS3ItemCategory.ARMOR),
    DS3ItemData("Alva Armor",                          0x14C4B7E8, DS3ItemCategory.ARMOR),
    DS3ItemData("Alva Gauntlets",                      0x14C4BBD0, DS3ItemCategory.ARMOR),
    DS3ItemData("Alva Leggings",                       0x14C4BFB8, DS3ItemCategory.ARMOR),
    DS3ItemData("Shadow Mask",                         0x14D3F640, DS3ItemCategory.ARMOR),
    DS3ItemData("Shadow Garb",                         0x14D3FA28, DS3ItemCategory.ARMOR),
    DS3ItemData("Shadow Gauntlets",                    0x14D3FE10, DS3ItemCategory.ARMOR),
    DS3ItemData("Shadow Leggings",                     0x14D401F8, DS3ItemCategory.ARMOR),
    DS3ItemData("Eastern Helm",                        0x14E33880, DS3ItemCategory.ARMOR),
    DS3ItemData("Eastern Armor",                       0x14E33C68, DS3ItemCategory.ARMOR),
    DS3ItemData("Eastern Gauntlets",                   0x14E34050, DS3ItemCategory.ARMOR),
    DS3ItemData("Eastern Leggings",                    0x14E34438, DS3ItemCategory.ARMOR),
    DS3ItemData("Helm of Favor",                       0x14F27AC0, DS3ItemCategory.ARMOR),
    DS3ItemData("Embraced Armor of Favor",             0x14F27EA8, DS3ItemCategory.ARMOR),
    DS3ItemData("Gauntlets of Favor",                  0x14F28290, DS3ItemCategory.ARMOR),
    DS3ItemData("Leggings of Favor",                   0x14F28678, DS3ItemCategory.ARMOR),
    DS3ItemData("Brass Helm",                          0x1501BD00, DS3ItemCategory.ARMOR),
    DS3ItemData("Brass Armor",                         0x1501C0E8, DS3ItemCategory.ARMOR),
    DS3ItemData("Brass Gauntlets",                     0x1501C4D0, DS3ItemCategory.ARMOR),
    DS3ItemData("Brass Leggings",                      0x1501C8B8, DS3ItemCategory.ARMOR),
    DS3ItemData("Silver Knight Helm",                  0x1510FF40, DS3ItemCategory.ARMOR),
    DS3ItemData("Silver Knight Armor",                 0x15110328, DS3ItemCategory.ARMOR),
    DS3ItemData("Silver Knight Gauntlets",             0x15110710, DS3ItemCategory.ARMOR),
    DS3ItemData("Silver Knight Leggings",              0x15110AF8, DS3ItemCategory.ARMOR),
    DS3ItemData("Lucatiel's Mask",                     0x15204180, DS3ItemCategory.ARMOR),
    DS3ItemData("Mirrah Vest",                         0x15204568, DS3ItemCategory.ARMOR),
    DS3ItemData("Mirrah Gloves",                       0x15204950, DS3ItemCategory.ARMOR),
    DS3ItemData("Mirrah Trousers",                     0x15204D38, DS3ItemCategory.ARMOR),
    DS3ItemData("Iron Helm",                           0x152F83C0, DS3ItemCategory.ARMOR),
    DS3ItemData("Armor of the Sun",                    0x152F87A8, DS3ItemCategory.ARMOR),
    DS3ItemData("Iron Bracelets",                      0x152F8B90, DS3ItemCategory.ARMOR),
    DS3ItemData("Iron Leggings",                       0x152F8F78, DS3ItemCategory.ARMOR),
    DS3ItemData("Drakeblood Helm",                     0x153EC600, DS3ItemCategory.ARMOR),
    DS3ItemData("Drakeblood Armor",                    0x153EC9E8, DS3ItemCategory.ARMOR),
    DS3ItemData("Drakeblood Gauntlets",                0x153ECDD0, DS3ItemCategory.ARMOR),
    DS3ItemData("Drakeblood Leggings",                 0x153ED1B8, DS3ItemCategory.ARMOR),
    DS3ItemData("Drang Armor",                         0x154E0C28, DS3ItemCategory.ARMOR),
    DS3ItemData("Drang Gauntlets",                     0x154E1010, DS3ItemCategory.ARMOR),
    DS3ItemData("Drang Shoes",                         0x154E13F8, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Iron Helm",                     0x155D4A80, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Iron Armor",                    0x155D4E68, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Iron Gauntlets",                0x155D5250, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Iron Leggings",                 0x155D5638, DS3ItemCategory.ARMOR),
    DS3ItemData("Painting Guardian Hood",              0x156C8CC0, DS3ItemCategory.ARMOR),
    DS3ItemData("Painting Guardian Gown",              0x156C90A8, DS3ItemCategory.ARMOR),
    DS3ItemData("Painting Guardian Gloves",            0x156C9490, DS3ItemCategory.ARMOR),
    DS3ItemData("Painting Guardian Waistcloth",        0x156C9878, DS3ItemCategory.ARMOR),
    DS3ItemData("Wolf Knight Helm",                    0x157BCF00, DS3ItemCategory.ARMOR),
    DS3ItemData("Wolf Knight Armor",                   0x157BD2E8, DS3ItemCategory.ARMOR),
    DS3ItemData("Wolf Knight Gauntlets",               0x157BD6D0, DS3ItemCategory.ARMOR),
    DS3ItemData("Wolf Knight Leggings",                0x157BDAB8, DS3ItemCategory.ARMOR),
    DS3ItemData("Dragonslayer Helm",                   0x158B1140, DS3ItemCategory.ARMOR),
    DS3ItemData("Dragonslayer Armor",                  0x158B1528, DS3ItemCategory.ARMOR),
    DS3ItemData("Dragonslayer Gauntlets",              0x158B1910, DS3ItemCategory.ARMOR),
    DS3ItemData("Dragonslayer Leggings",               0x158B1CF8, DS3ItemCategory.ARMOR),
    DS3ItemData("Smough's Helm",                       0x159A5380, DS3ItemCategory.ARMOR),
    DS3ItemData("Smough's Armor",                      0x159A5768, DS3ItemCategory.ARMOR),
    DS3ItemData("Smough's Gauntlets",                  0x159A5B50, DS3ItemCategory.ARMOR),
    DS3ItemData("Smough's Leggings",                   0x159A5F38, DS3ItemCategory.ARMOR),
    DS3ItemData("Helm of Thorns",                      0x15B8D800, DS3ItemCategory.ARMOR),
    DS3ItemData("Armor of Thorns",                     0x15B8DBE8, DS3ItemCategory.ARMOR),
    DS3ItemData("Gauntlets of Thorns",                 0x15B8DFD0, DS3ItemCategory.ARMOR),
    DS3ItemData("Leggings of Thorns",                  0x15B8E3B8, DS3ItemCategory.ARMOR),
    DS3ItemData("Crown of Dusk",                       0x15D75C80, DS3ItemCategory.ARMOR),
    DS3ItemData("Antiquated Dress",                    0x15D76068, DS3ItemCategory.ARMOR),
    DS3ItemData("Antiquated Gloves",                   0x15D76450, DS3ItemCategory.ARMOR),
    DS3ItemData("Antiquated Skirt",                    0x15D76838, DS3ItemCategory.ARMOR),
    DS3ItemData("Karla's Pointed Hat",                 0x15E69EC0, DS3ItemCategory.ARMOR),
    DS3ItemData("Karla's Coat",                        0x15E6A2A8, DS3ItemCategory.ARMOR),
    DS3ItemData("Karla's Gloves",                      0x15E6A690, DS3ItemCategory.ARMOR),
    DS3ItemData("Karla's Trousers",                    0x15E6AA78, DS3ItemCategory.ARMOR),

    # Covenants
    DS3ItemData("Blade of the Darkmoon",               0x20002710, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Watchdogs of Farron",                 0x20002724, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Aldrich Faithful",                    0x2000272E, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Warrior of Sunlight",                 0x20002738, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Mound-makers",                        0x20002742, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Way of Blue",                         0x2000274C, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Blue Sentinels",                      0x20002756, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Rosaria's Fingers",                   0x20002760, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Spears of the Church",                0x2000276A, DS3ItemCategory.UNIQUE, skip = True),

    # Rings
    DS3ItemData("Life Ring",                           0x20004E20, DS3ItemCategory.RING),
    DS3ItemData("Life Ring+1",                         0x20004E21, DS3ItemCategory.RING),
    DS3ItemData("Life Ring+2",                         0x20004E22, DS3ItemCategory.RING),
    DS3ItemData("Life Ring+3",                         0x20004E23, DS3ItemCategory.RING),
    DS3ItemData("Chloranthy Ring",                     0x20004E2A, DS3ItemCategory.RING,
                useful_if = UsefulIf.BASE),
    DS3ItemData("Chloranthy Ring+1",                   0x20004E2B, DS3ItemCategory.RING),
    DS3ItemData("Chloranthy Ring+2",                   0x20004E2C, DS3ItemCategory.RING,
                useful_if = UsefulIf.NO_DLC),
    DS3ItemData("Havel's Ring",                        0x20004E34, DS3ItemCategory.RING,
                useful_if = UsefulIf.BASE),
    DS3ItemData("Havel's Ring+1",                      0x20004E35, DS3ItemCategory.RING),
    DS3ItemData("Havel's Ring+2",                      0x20004E36, DS3ItemCategory.RING,
                useful_if = UsefulIf.NO_DLC),
    DS3ItemData("Ring of Favor",                       0x20004E3E, DS3ItemCategory.RING,
                useful_if = UsefulIf.BASE),
    DS3ItemData("Ring of Favor+1",                     0x20004E3F, DS3ItemCategory.RING),
    DS3ItemData("Ring of Favor+2",                     0x20004E40, DS3ItemCategory.RING,
                useful_if = UsefulIf.NO_DLC),
    DS3ItemData("Ring of Steel Protection",            0x20004E48, DS3ItemCategory.RING,
                useful_if = UsefulIf.BASE),
    DS3ItemData("Ring of Steel Protection+1",          0x20004E49, DS3ItemCategory.RING),
    DS3ItemData("Ring of Steel Protection+2",          0x20004E4A, DS3ItemCategory.RING,
                useful_if = UsefulIf.NO_DLC),
    DS3ItemData("Flame Stoneplate Ring",               0x20004E52, DS3ItemCategory.RING),
    DS3ItemData("Flame Stoneplate Ring+1",             0x20004E53, DS3ItemCategory.RING),
    DS3ItemData("Flame Stoneplate Ring+2",             0x20004E54, DS3ItemCategory.RING),
    DS3ItemData("Thunder Stoneplate Ring",             0x20004E5C, DS3ItemCategory.RING),
    DS3ItemData("Thunder Stoneplate Ring+1",           0x20004E5D, DS3ItemCategory.RING),
    DS3ItemData("Thunder Stoneplate Ring+2",           0x20004E5E, DS3ItemCategory.RING),
    DS3ItemData("Magic Stoneplate Ring",               0x20004E66, DS3ItemCategory.RING),
    DS3ItemData("Magic Stoneplate Ring+1",             0x20004E67, DS3ItemCategory.RING),
    DS3ItemData("Magic Stoneplate Ring+2",             0x20004E68, DS3ItemCategory.RING),
    DS3ItemData("Dark Stoneplate Ring",                0x20004E70, DS3ItemCategory.RING),
    DS3ItemData("Dark Stoneplate Ring+1",              0x20004E71, DS3ItemCategory.RING),
    DS3ItemData("Dark Stoneplate Ring+2",              0x20004E72, DS3ItemCategory.RING),
    DS3ItemData("Speckled Stoneplate Ring",            0x20004E7A, DS3ItemCategory.RING),
    DS3ItemData("Speckled Stoneplate Ring+1",          0x20004E7B, DS3ItemCategory.RING),
    DS3ItemData("Bloodbite Ring",                      0x20004E84, DS3ItemCategory.RING),
    DS3ItemData("Bloodbite Ring+1",                    0x20004E85, DS3ItemCategory.RING),
    DS3ItemData("Poisonbite Ring",                     0x20004E8E, DS3ItemCategory.RING),
    DS3ItemData("Poisonbite Ring+1",                   0x20004E8F, DS3ItemCategory.RING),
    DS3ItemData("Cursebite Ring",                      0x20004E98, DS3ItemCategory.RING),
    DS3ItemData("Fleshbite Ring",                      0x20004EA2, DS3ItemCategory.RING),
    DS3ItemData("Fleshbite Ring+1",                    0x20004EA3, DS3ItemCategory.RING),
    DS3ItemData("Wood Grain Ring",                     0x20004EAC, DS3ItemCategory.RING),
    DS3ItemData("Wood Grain Ring+1",                   0x20004EAD, DS3ItemCategory.RING),
    DS3ItemData("Wood Grain Ring+2",                   0x20004EAE, DS3ItemCategory.RING),
    DS3ItemData("Scholar Ring",                        0x20004EB6, DS3ItemCategory.RING),
    DS3ItemData("Priestess Ring",                      0x20004EC0, DS3ItemCategory.RING),
    DS3ItemData("Red Tearstone Ring",                  0x20004ECA, DS3ItemCategory.RING),
    DS3ItemData("Blue Tearstone Ring",                 0x20004ED4, DS3ItemCategory.RING),
    DS3ItemData("Wolf Ring",                           0x20004EDE, DS3ItemCategory.RING,
                inject = True), # Covenant reward
    DS3ItemData("Wolf Ring+1",                         0x20004EDF, DS3ItemCategory.RING),
    DS3ItemData("Wolf Ring+2",                         0x20004EE0, DS3ItemCategory.RING),
    DS3ItemData("Leo Ring",                            0x20004EE8, DS3ItemCategory.RING),
    DS3ItemData("Ring of Sacrifice",                   0x20004EF2, DS3ItemCategory.RING, filler = True),
    DS3ItemData("Young Dragon Ring",                   0x20004F06, DS3ItemCategory.RING),
    DS3ItemData("Bellowing Dragoncrest Ring",          0x20004F07, DS3ItemCategory.RING),
    DS3ItemData("Great Swamp Ring",                    0x20004F10, DS3ItemCategory.RING),
    DS3ItemData("Witch's Ring",                        0x20004F11, DS3ItemCategory.RING),
    DS3ItemData("Morne's Ring",                        0x20004F1A, DS3ItemCategory.RING),
    DS3ItemData("Ring of the Sun's First Born",        0x20004F1B, DS3ItemCategory.RING),
    DS3ItemData("Lingering Dragoncrest Ring",          0x20004F2E, DS3ItemCategory.RING),
    DS3ItemData("Lingering Dragoncrest Ring+1",        0x20004F2F, DS3ItemCategory.RING),
    DS3ItemData("Lingering Dragoncrest Ring+2",        0x20004F30, DS3ItemCategory.RING),
    DS3ItemData("Sage Ring",                           0x20004F38, DS3ItemCategory.RING,
                useful_if = UsefulIf.NO_NGP),
    DS3ItemData("Sage Ring+1",                         0x20004F39, DS3ItemCategory.RING),
    DS3ItemData("Sage Ring+2",                         0x20004F3A, DS3ItemCategory.RING,
                classification = ItemClassification.useful),
    DS3ItemData("Slumbering Dragoncrest Ring",         0x20004F42, DS3ItemCategory.RING),
    DS3ItemData("Dusk Crown Ring",                     0x20004F4C, DS3ItemCategory.RING),
    DS3ItemData("Saint's Ring",                        0x20004F56, DS3ItemCategory.RING),
    DS3ItemData("Deep Ring",                           0x20004F60, DS3ItemCategory.RING),
    DS3ItemData("Darkmoon Ring",                       0x20004F6A, DS3ItemCategory.RING,
                inject = True), # Covenant reward
    DS3ItemData("Hawk Ring",                           0x20004F92, DS3ItemCategory.RING),
    DS3ItemData("Hornet Ring",                         0x20004F9C, DS3ItemCategory.RING),
    DS3ItemData("Covetous Gold Serpent Ring",          0x20004FA6, DS3ItemCategory.RING),
    DS3ItemData("Covetous Gold Serpent Ring+1",        0x20004FA7, DS3ItemCategory.RING),
    DS3ItemData("Covetous Gold Serpent Ring+2",        0x20004FA8, DS3ItemCategory.RING),
    DS3ItemData("Covetous Silver Serpent Ring",        0x20004FB0, DS3ItemCategory.RING,
                useful_if = UsefulIf.BASE),
    DS3ItemData("Covetous Silver Serpent Ring+1",      0x20004FB1, DS3ItemCategory.RING),
    DS3ItemData("Covetous Silver Serpent Ring+2",      0x20004FB2, DS3ItemCategory.RING,
                useful_if = UsefulIf.NO_DLC),
    DS3ItemData("Sun Princess Ring",                   0x20004FBA, DS3ItemCategory.RING),
    DS3ItemData("Silvercat Ring",                      0x20004FC4, DS3ItemCategory.RING),
    DS3ItemData("Skull Ring",                          0x20004FCE, DS3ItemCategory.RING),
    DS3ItemData("Untrue White Ring",                   0x20004FD8, DS3ItemCategory.RING, skip = True),
    DS3ItemData("Carthus Milkring",                    0x20004FE2, DS3ItemCategory.RING),
    DS3ItemData("Knight's Ring",                       0x20004FEC, DS3ItemCategory.RING),
    DS3ItemData("Hunter's Ring",                       0x20004FF6, DS3ItemCategory.RING),
    DS3ItemData("Knight Slayer's Ring",                0x20005000, DS3ItemCategory.RING),
    DS3ItemData("Magic Clutch Ring",                   0x2000500A, DS3ItemCategory.RING),
    DS3ItemData("Lightning Clutch Ring",               0x20005014, DS3ItemCategory.RING),
    DS3ItemData("Fire Clutch Ring",                    0x2000501E, DS3ItemCategory.RING),
    DS3ItemData("Dark Clutch Ring",                    0x20005028, DS3ItemCategory.RING),
    DS3ItemData("Flynn's Ring",                        0x2000503C, DS3ItemCategory.RING),
    DS3ItemData("Prisoner's Chain",                    0x20005046, DS3ItemCategory.RING,
                classification = ItemClassification.useful),
    DS3ItemData("Untrue Dark Ring",                    0x20005050, DS3ItemCategory.RING),
    DS3ItemData("Obscuring Ring",                      0x20005064, DS3ItemCategory.RING),
    DS3ItemData("Ring of the Evil Eye",                0x2000506E, DS3ItemCategory.RING),
    DS3ItemData("Ring of the Evil Eye+1",              0x2000506F, DS3ItemCategory.RING),
    DS3ItemData("Ring of the Evil Eye+2",              0x20005070, DS3ItemCategory.RING),
    DS3ItemData("Calamity Ring",                       0x20005078, DS3ItemCategory.RING),
    DS3ItemData("Farron Ring",                         0x20005082, DS3ItemCategory.RING),
    DS3ItemData("Aldrich's Ruby",                      0x2000508C, DS3ItemCategory.RING),
    DS3ItemData("Aldrich's Sapphire",                  0x20005096, DS3ItemCategory.RING),
    DS3ItemData("Lloyd's Sword Ring",                  0x200050B4, DS3ItemCategory.RING,
                classification = ItemClassification.useful),
    DS3ItemData("Lloyd's Shield Ring",                 0x200050BE, DS3ItemCategory.RING),
    DS3ItemData("Estus Ring",                          0x200050DC, DS3ItemCategory.RING),
    DS3ItemData("Ashen Estus Ring",                    0x200050E6, DS3ItemCategory.RING),
    DS3ItemData("Horsehoof Ring",                      0x200050F0, DS3ItemCategory.RING),
    DS3ItemData("Carthus Bloodring",                   0x200050FA, DS3ItemCategory.RING,
                classification = ItemClassification.useful),
    DS3ItemData("Reversal Ring",                       0x20005104, DS3ItemCategory.RING),
    DS3ItemData("Pontiff's Right Eye",                 0x2000510E, DS3ItemCategory.RING),
    DS3ItemData("Pontiff's Left Eye",                  0x20005136, DS3ItemCategory.RING),
    DS3ItemData("Dragonscale Ring",                    0x2000515E, DS3ItemCategory.RING),

    # Items
    DS3ItemData("White Sign Soapstone",                0x40000064, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Red Sign Soapstone",                  0x40000066, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Red Eye Orb",                         0x40000066, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Roster of Knights",                   0x4000006C, DS3ItemCategory.UNIQUE, skip = True),
    *DS3ItemData("Cracked Red Eye Orb",                 0x4000006F, DS3ItemCategory.MISC, skip = True).counts([5]),
    DS3ItemData("Black Eye Orb",                       0x40000073, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Divine Blessing",                     0x400000F0, DS3ItemCategory.MISC),
    DS3ItemData("Hidden Blessing",                     0x400000F1, DS3ItemCategory.MISC),
    *DS3ItemData("Green Blossom",                       0x40000104, DS3ItemCategory.MISC, filler = True).counts([2, 3, 4]),
    *DS3ItemData("Budding Green Blossom",               0x40000106, DS3ItemCategory.MISC).counts([2, 3]),
    *DS3ItemData("Bloodred Moss Clump",                 0x4000010E, DS3ItemCategory.MISC, filler = True).counts([3]),
    *DS3ItemData("Purple Moss Clump",                   0x4000010F, DS3ItemCategory.MISC, filler = True).counts([2, 3, 4]),
    *DS3ItemData("Blooming Purple Moss Clump",          0x40000110, DS3ItemCategory.MISC).counts([3]),
    *DS3ItemData("Purging Stone",                       0x40000112, DS3ItemCategory.MISC, skip = True).counts([2, 3]),
    *DS3ItemData("Rime-blue Moss Clump",                0x40000114, DS3ItemCategory.MISC, filler = True).counts([2, 4]),
    *DS3ItemData("Repair Powder",                       0x40000118, DS3ItemCategory.MISC, filler = True).counts([2, 3, 4]),
    *DS3ItemData("Kukri",                               0x40000122, DS3ItemCategory.MISC).counts([8, 9]),
    DS3ItemData("Kukri x5",                            0x40000122, DS3ItemCategory.MISC, count = 5, filler = True),
    *DS3ItemData("Firebomb",                            0x40000124, DS3ItemCategory.MISC).counts([3, 5, 6]),
    DS3ItemData("Firebomb x2",                         0x40000124, DS3ItemCategory.MISC, count = 2, filler = True),
    *DS3ItemData("Dung Pie",                            0x40000125, DS3ItemCategory.MISC).counts([2, 4]),
    DS3ItemData("Dung Pie x3",                         0x40000125, DS3ItemCategory.MISC, count = 3, filler = True),
    *DS3ItemData("Alluring Skull",                      0x40000126, DS3ItemCategory.MISC, filler = True).counts([2, 3]),
    *DS3ItemData("Undead Hunter Charm",                 0x40000128, DS3ItemCategory.MISC).counts([2, 3]),
    *DS3ItemData("Black Firebomb",                      0x40000129, DS3ItemCategory.MISC, filler = True).counts([2, 3, 4]),
    DS3ItemData("Rope Firebomb",                       0x4000012B, DS3ItemCategory.MISC),
    *DS3ItemData("Lightning Urn",                       0x4000012C, DS3ItemCategory.MISC, filler = True).counts([3, 4, 6]),
    DS3ItemData("Rope Black Firebomb",                 0x4000012E, DS3ItemCategory.MISC),
    *DS3ItemData("Stalk Dung Pie",                      0x4000012F, DS3ItemCategory.MISC).counts([6]),
    *DS3ItemData("Duel Charm",                          0x40000130, DS3ItemCategory.MISC).counts([3]),
    *DS3ItemData("Throwing Knife",                      0x40000136, DS3ItemCategory.MISC).counts([6, 8]),
    DS3ItemData("Throwing Knife x5",                   0x40000136, DS3ItemCategory.MISC, count = 5, filler = True),
    DS3ItemData("Poison Throwing Knife",               0x40000137, DS3ItemCategory.MISC),
    *DS3ItemData("Charcoal Pine Resin",                 0x4000014A, DS3ItemCategory.MISC, filler = True).counts([2]),
    *DS3ItemData("Gold Pine Resin",                     0x4000014B, DS3ItemCategory.MISC, filler = True).counts([2]),
    *DS3ItemData("Human Pine Resin",                    0x4000014E, DS3ItemCategory.MISC, filler = True).counts([2, 4]),
    *DS3ItemData("Carthus Rouge",                       0x4000014F, DS3ItemCategory.MISC, filler = True).counts([2, 3]),
    *DS3ItemData("Pale Pine Resin",                     0x40000150, DS3ItemCategory.MISC, filler = True).counts([2]),
    *DS3ItemData("Charcoal Pine Bundle",                0x40000154, DS3ItemCategory.MISC).counts([2]),
    *DS3ItemData("Gold Pine Bundle",                    0x40000155, DS3ItemCategory.MISC).counts([6]),
    *DS3ItemData("Rotten Pine Resin",                   0x40000157, DS3ItemCategory.MISC).counts([2, 4]),
    *DS3ItemData("Homeward Bone",                       0x4000015E, DS3ItemCategory.MISC, filler = True).counts([2, 3, 6]),
    DS3ItemData("Coiled Sword Fragment",               0x4000015F, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression), # Crow trade
    DS3ItemData("Wolf's Blood Swordgrass",             0x4000016E, DS3ItemCategory.MISC, skip = True),
    DS3ItemData("Human Dregs",                         0x4000016F, DS3ItemCategory.MISC, skip = True),
    DS3ItemData("Forked Pale Tongue",                  0x40000170, DS3ItemCategory.MISC, skip = True),
    DS3ItemData("Proof of a Concord Well Kept",        0x40000171, DS3ItemCategory.MISC, skip = True),
    *DS3ItemData("Prism Stone",                         0x40000172, DS3ItemCategory.MISC, skip = True).counts([4, 6, 10]),
    DS3ItemData("Binoculars",                          0x40000173, DS3ItemCategory.MISC),
    DS3ItemData("Proof of a Concord Kept",             0x40000174, DS3ItemCategory.MISC, skip = True),
    # One is needed for Leonhard's quest, others are useful for restatting.
    DS3ItemData("Pale Tongue",                         0x40000175, DS3ItemCategory.MISC,
                classification = ItemClassification.progression),
    DS3ItemData("Vertebra Shackle",                    0x40000176, DS3ItemCategory.MISC,
                classification = ItemClassification.progression), # Crow trade
    DS3ItemData("Sunlight Medal",                      0x40000177, DS3ItemCategory.MISC, skip = True),
    DS3ItemData("Dragon Head Stone",                   0x40000179, DS3ItemCategory.UNIQUE),
    DS3ItemData("Dragon Torso Stone",                  0x4000017A, DS3ItemCategory.UNIQUE),
    DS3ItemData("Rubbish",                             0x4000017C, DS3ItemCategory.MISC, skip = True),
    DS3ItemData("Dried Finger",                        0x40000181, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Twinkling Dragon Head Stone",         0x40000183, DS3ItemCategory.UNIQUE),
    DS3ItemData("Twinkling Dragon Torso Stone",        0x40000184, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Fire Keeper Soul",                    0x40000186, DS3ItemCategory.UNIQUE),
    # Allow souls up to 2k in value to be used as filler
    DS3ItemData("Fading Soul",                         0x40000190, DS3ItemCategory.SOUL, souls = 50),
    DS3ItemData("Soul of a Deserted Corpse",           0x40000191, DS3ItemCategory.SOUL, souls = 200),
    DS3ItemData("Large Soul of a Deserted Corpse",     0x40000192, DS3ItemCategory.SOUL, souls = 400),
    DS3ItemData("Soul of an Unknown Traveler",         0x40000193, DS3ItemCategory.SOUL, souls = 800),
    DS3ItemData("Large Soul of an Unknown Traveler",   0x40000194, DS3ItemCategory.SOUL, souls = 1000),
    DS3ItemData("Soul of a Nameless Soldier",          0x40000195, DS3ItemCategory.SOUL, souls = 2000),
    DS3ItemData("Large Soul of a Nameless Soldier",    0x40000196, DS3ItemCategory.SOUL, souls = 3000),
    DS3ItemData("Soul of a Weary Warrior",             0x40000197, DS3ItemCategory.SOUL, souls = 5000),
    DS3ItemData("Large Soul of a Weary Warrior",       0x40000198, DS3ItemCategory.SOUL, souls = 8000),
    DS3ItemData("Soul of a Crestfallen Knight",        0x40000199, DS3ItemCategory.SOUL, souls = 10000),
    DS3ItemData("Large Soul of a Crestfallen Knight",  0x4000019A, DS3ItemCategory.SOUL, souls = 20000),
    DS3ItemData("Soul of a Proud Paladin",             0x4000019B, DS3ItemCategory.SOUL, souls = 500),
    DS3ItemData("Large Soul of a Proud Paladin",       0x4000019C, DS3ItemCategory.SOUL, souls = 1000),
    DS3ItemData("Soul of an Intrepid Hero",            0x4000019D, DS3ItemCategory.SOUL, souls = 2000),
    DS3ItemData("Large Soul of an Intrepid Hero",      0x4000019E, DS3ItemCategory.SOUL, souls = 2500),
    DS3ItemData("Soul of a Seasoned Warrior",          0x4000019F, DS3ItemCategory.SOUL, souls = 5000),
    DS3ItemData("Large Soul of a Seasoned Warrior",    0x400001A0, DS3ItemCategory.SOUL, souls = 7500),
    DS3ItemData("Soul of an Old Hand",                 0x400001A1, DS3ItemCategory.SOUL, souls = 12500),
    DS3ItemData("Soul of a Venerable Old Hand",        0x400001A2, DS3ItemCategory.SOUL, souls = 20000),
    DS3ItemData("Soul of a Champion",                  0x400001A3, DS3ItemCategory.SOUL, souls = 25000),
    DS3ItemData("Soul of a Great Champion",            0x400001A4, DS3ItemCategory.SOUL, souls = 50000),
    DS3ItemData("Seed of a Giant Tree",                0x400001B8, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression, inject = True), # Crow trade
    *DS3ItemData("Mossfruit",                           0x400001C4, DS3ItemCategory.MISC, filler = True).counts([2]),
    DS3ItemData("Young White Branch",                  0x400001C6, DS3ItemCategory.MISC),
    *DS3ItemData("Rusted Coin",                         0x400001C7, DS3ItemCategory.MISC, filler = True).counts([2]),
    DS3ItemData("Siegbräu",                            0x400001C8, DS3ItemCategory.MISC,
                classification = ItemClassification.progression), # Crow trade
    *DS3ItemData("Rusted Gold Coin",                    0x400001C9, DS3ItemCategory.MISC, filler = True).counts([2, 3]),
    *DS3ItemData("Blue Bug Pellet",                     0x400001CA, DS3ItemCategory.MISC, filler = True).counts([2]),
    *DS3ItemData("Red Bug Pellet",                      0x400001CB, DS3ItemCategory.MISC, filler = True).counts([2, 3]),
    *DS3ItemData("Yellow Bug Pellet",                   0x400001CC, DS3ItemCategory.MISC, filler = True).counts([2, 3]),
    *DS3ItemData("Black Bug Pellet",                    0x400001CD, DS3ItemCategory.MISC, filler = True).counts([2, 3]),
    DS3ItemData("Young White Branch",                  0x400001CF, DS3ItemCategory.MISC, skip = True),
    DS3ItemData("Dark Sigil",                          0x400001EA, DS3ItemCategory.MISC, skip = True),
    *DS3ItemData("Ember",                               0x400001F4, DS3ItemCategory.MISC, filler = True).counts([2]),
    DS3ItemData("Hello Carving",                       0x40000208, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Thank you Carving",                   0x40000209, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Very good! Carving",                  0x4000020A, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("I'm sorry Carving",                   0x4000020B, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Help me! Carving",                    0x4000020C, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Soul of Champion Gundyr",             0x400002C8, DS3ItemCategory.BOSS, souls = 20000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of the Dancer",                  0x400002CA, DS3ItemCategory.BOSS, souls = 10000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of a Crystal Sage",              0x400002CB, DS3ItemCategory.BOSS, souls = 3000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of the Blood of the Wolf",       0x400002CD, DS3ItemCategory.BOSS, souls = 20000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of Consumed Oceiros",            0x400002CE, DS3ItemCategory.BOSS, souls = 12000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of Boreal Valley Vordt",         0x400002CF, DS3ItemCategory.BOSS, souls = 2000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of the Old Demon King",          0x400002D0, DS3ItemCategory.BOSS, souls = 10000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of Dragonslayer Armour",         0x400002D1, DS3ItemCategory.BOSS, souls = 15000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of the Nameless King",           0x400002D2, DS3ItemCategory.BOSS, souls = 16000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of Pontiff Sulyvahn",            0x400002D4, DS3ItemCategory.BOSS, souls = 12000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of Aldrich",                     0x400002D5, DS3ItemCategory.BOSS, souls = 15000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of High Lord Wolnir",            0x400002D6, DS3ItemCategory.BOSS, souls = 10000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of the Rotted Greatwood",        0x400002D7, DS3ItemCategory.BOSS, souls = 3000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of Rosaria",                     0x400002D8, DS3ItemCategory.BOSS, souls = 5000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of the Deacons of the Deep",     0x400002D9, DS3ItemCategory.BOSS, souls = 20000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of the Twin Princes",            0x400002DB, DS3ItemCategory.BOSS, souls = 20000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of Yhorm the Giant",             0x400002DC, DS3ItemCategory.BOSS, souls = 20000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of the Lords",                   0x400002DD, DS3ItemCategory.BOSS, souls = 20000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of a Demon",                     0x400002E3, DS3ItemCategory.BOSS, souls = 20000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of a Stray Demon",               0x400002E7, DS3ItemCategory.BOSS, souls = 20000,
                classification = ItemClassification.progression),
    *DS3ItemData("Titanite Shard",                      0x400003E8, DS3ItemCategory.UPGRADE).counts([2]),
    *DS3ItemData("Large Titanite Shard",                0x400003E9, DS3ItemCategory.UPGRADE).counts([2, 3]),
    *DS3ItemData("Titanite Chunk",                      0x400003EA, DS3ItemCategory.UPGRADE).counts([2, 6]),
    DS3ItemData("Titanite Slab",                       0x400003EB, DS3ItemCategory.UPGRADE,
                classification = ItemClassification.useful),
    *DS3ItemData("Titanite Scale",                      0x400003FC, DS3ItemCategory.UPGRADE).counts([2, 3]),
    *DS3ItemData("Twinkling Titanite",                  0x40000406, DS3ItemCategory.UPGRADE).counts([2, 3]),
    DS3ItemData("Heavy Gem",                           0x4000044C, DS3ItemCategory.UPGRADE),
    DS3ItemData("Sharp Gem",                           0x40000456, DS3ItemCategory.UPGRADE),
    DS3ItemData("Refined Gem",                         0x40000460, DS3ItemCategory.UPGRADE),
    DS3ItemData("Crystal Gem",                         0x4000046A, DS3ItemCategory.UPGRADE),
    DS3ItemData("Simple Gem",                          0x40000474, DS3ItemCategory.UPGRADE),
    DS3ItemData("Fire Gem",                            0x4000047E, DS3ItemCategory.UPGRADE),
    DS3ItemData("Chaos Gem",                           0x40000488, DS3ItemCategory.UPGRADE),
    DS3ItemData("Lightning Gem",                       0x40000492, DS3ItemCategory.UPGRADE),
    DS3ItemData("Deep Gem",                            0x4000049C, DS3ItemCategory.UPGRADE),
    DS3ItemData("Dark Gem",                            0x400004A6, DS3ItemCategory.UPGRADE),
    DS3ItemData("Poison Gem",                          0x400004B0, DS3ItemCategory.UPGRADE),
    DS3ItemData("Blood Gem",                           0x400004BA, DS3ItemCategory.UPGRADE),
    DS3ItemData("Raw Gem",                             0x400004C4, DS3ItemCategory.UPGRADE),
    DS3ItemData("Blessed Gem",                         0x400004CE, DS3ItemCategory.UPGRADE),
    DS3ItemData("Hollow Gem",                          0x400004D8, DS3ItemCategory.UPGRADE),
    DS3ItemData("Shriving Stone",                      0x400004E2, DS3ItemCategory.UPGRADE),
    DS3ItemData("Lift Chamber Key",                    0x400007D1, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Small Doll",                          0x400007D5, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Jailbreaker's Key",                   0x400007D7, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Jailer's Key Ring",                   0x400007D8, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Grave Key",                           0x400007D9, DS3ItemCategory.UNIQUE),
    DS3ItemData("Cell Key",                            0x400007DA, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Dungeon Ground Floor Key",            0x400007DB, DS3ItemCategory.UNIQUE),
    DS3ItemData("Old Cell Key",                        0x400007DC, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Grand Archives Key",                  0x400007DE, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Tower Key",                           0x400007DF, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Small Lothric Banner",                0x40000836, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Farron Coal",                         0x40000837, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.useful),
    DS3ItemData("Sage's Coal",                         0x40000838, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.useful),
    DS3ItemData("Giant's Coal",                        0x40000839, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.useful),
    DS3ItemData("Profaned Coal",                       0x4000083A, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.useful),
    DS3ItemData("Mortician's Ashes",                   0x4000083B, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Dreamchaser's Ashes",                 0x4000083C, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Paladin's Ashes",                     0x4000083D, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Grave Warden's Ashes",                0x4000083E, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Greirat's Ashes",                     0x4000083F, DS3ItemCategory.UNIQUE),
    DS3ItemData("Orbeck's Ashes",                      0x40000840, DS3ItemCategory.UNIQUE),
    DS3ItemData("Cornyx's Ashes",                      0x40000841, DS3ItemCategory.UNIQUE),
    DS3ItemData("Karla's Ashes",                       0x40000842, DS3ItemCategory.UNIQUE),
    DS3ItemData("Irina's Ashes",                       0x40000843, DS3ItemCategory.UNIQUE),
    DS3ItemData("Yuria's Ashes",                       0x40000844, DS3ItemCategory.UNIQUE),
    DS3ItemData("Basin of Vows",                       0x40000845, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Loretta's Bone",                      0x40000846, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Braille Divine Tome of Carim",        0x40000847, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Braille Divine Tome of Lothric",      0x40000848, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Cinders of a Lord - Abyss Watcher",   0x4000084B, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Cinders of a Lord - Aldrich",         0x4000084C, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Cinders of a Lord - Yhorm the Giant", 0x4000084D, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Cinders of a Lord - Lothric Prince",  0x4000084E, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Great Swamp Pyromancy Tome",          0x4000084F, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Carthus Pyromancy Tome",              0x40000850, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Izalith Pyromancy Tome",              0x40000851, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Quelana Pyromancy Tome",              0x40000852, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Grave Warden Pyromancy Tome",         0x40000853, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Sage's Scroll",                       0x40000854, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Logan's Scroll",                      0x40000855, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Crystal Scroll",                      0x40000856, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Transposing Kiln",                    0x40000857, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Coiled Sword",                        0x40000859, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Eyes of a Fire Keeper",               0x4000085A, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.useful), # Allow players to do any ending
    DS3ItemData("Sword of Avowal",                     0x4000085B, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.useful),
    DS3ItemData("Golden Scroll",                       0x4000085C, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Estus Shard",                         0x4000085D, DS3ItemCategory.HEALING,
                classification = ItemClassification.useful),
    DS3ItemData("Hawkwood's Swordgrass",               0x4000085E, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Undead Bone Shard",                   0x4000085F, DS3ItemCategory.HEALING,
                classification = ItemClassification.useful),
    DS3ItemData("Deep Braille Divine Tome",            0x40000860, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Londor Braille Divine Tome",          0x40000861, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Excrement-covered Ashes",             0x40000862, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.useful),
    DS3ItemData("Prisoner Chief's Ashes",              0x40000863, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Xanthous Ashes",                      0x40000864, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Hollow's Ashes",                      0x40000865, DS3ItemCategory.UNIQUE),
    DS3ItemData("Patches' Ashes",                      0x40000866, DS3ItemCategory.UNIQUE),
    DS3ItemData("Dragon Chaser's Ashes",               0x40000867, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Easterner's Ashes",                   0x40000868, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),

    # Fake item for controlling access to Archdragon Peak. The real drop isn't actually an item as
    # such, so we have to inject this because there's no slot for it to come from.
    DS3ItemData("Path of the Dragon",                  0x40002346, DS3ItemCategory.UNIQUE,
                inject = True, classification = ItemClassification.progression),

    # Spells
    DS3ItemData("Farron Dart",                         0x40124F80, DS3ItemCategory.SPELL),
    DS3ItemData("Great Farron Dart",                   0x40127690, DS3ItemCategory.SPELL),
    DS3ItemData("Soul Arrow",                          0x4013D620, DS3ItemCategory.SPELL),
    DS3ItemData("Great Soul Arrow",                    0x4013DA08, DS3ItemCategory.SPELL),
    DS3ItemData("Heavy Soul Arrow",                    0x4013DDF0, DS3ItemCategory.SPELL),
    DS3ItemData("Great Heavy Soul Arrow",              0x4013E1D8, DS3ItemCategory.SPELL),
    DS3ItemData("Homing Soulmass",                     0x4013E5C0, DS3ItemCategory.SPELL),
    DS3ItemData("Homing Crystal Soulmass",             0x4013E9A8, DS3ItemCategory.SPELL),
    DS3ItemData("Soul Spear",                          0x4013ED90, DS3ItemCategory.SPELL),
    DS3ItemData("Crystal Soul Spear",                  0x4013F178, DS3ItemCategory.SPELL),
    DS3ItemData("Deep Soul",                           0x4013F560, DS3ItemCategory.SPELL),
    DS3ItemData("Great Deep Soul",                     0x4013F948, DS3ItemCategory.SPELL,
                inject = True), # Covenant reward
    DS3ItemData("Magic Weapon",                        0x4013FD30, DS3ItemCategory.SPELL),
    DS3ItemData("Great Magic Weapon",                  0x40140118, DS3ItemCategory.SPELL),
    DS3ItemData("Crystal Magic Weapon",                0x40140500, DS3ItemCategory.SPELL),
    DS3ItemData("Magic Shield",                        0x40144B50, DS3ItemCategory.SPELL),
    DS3ItemData("Great Magic Shield",                  0x40144F38, DS3ItemCategory.SPELL),
    DS3ItemData("Hidden Weapon",                       0x40147260, DS3ItemCategory.SPELL),
    DS3ItemData("Hidden Body",                         0x40147648, DS3ItemCategory.SPELL,
                classification = ItemClassification.useful),
    DS3ItemData("Cast Light",                          0x40149970, DS3ItemCategory.SPELL),
    DS3ItemData("Repair",                              0x4014A528, DS3ItemCategory.SPELL),
    DS3ItemData("Spook",                               0x4014A910, DS3ItemCategory.SPELL,
                classification = ItemClassification.useful),
    DS3ItemData("Chameleon",                           0x4014ACF8, DS3ItemCategory.SPELL,
                classification = ItemClassification.progression),
    DS3ItemData("Aural Decoy",                         0x4014B0E0, DS3ItemCategory.SPELL),
    DS3ItemData("White Dragon Breath",                 0x4014E790, DS3ItemCategory.SPELL),
    DS3ItemData("Farron Hail",                         0x4014EF60, DS3ItemCategory.SPELL),
    DS3ItemData("Crystal Hail",                        0x4014F348, DS3ItemCategory.SPELL),
    DS3ItemData("Soul Greatsword",                     0x4014F730, DS3ItemCategory.SPELL),
    DS3ItemData("Farron Flashsword",                   0x4014FB18, DS3ItemCategory.SPELL),
    DS3ItemData("Affinity",                            0x401875B8, DS3ItemCategory.SPELL),
    DS3ItemData("Dark Edge",                           0x40189CC8, DS3ItemCategory.SPELL),
    DS3ItemData("Soul Stream",                         0x4018B820, DS3ItemCategory.SPELL),
    DS3ItemData("Twisted Wall of Light",               0x40193138, DS3ItemCategory.SPELL),
    DS3ItemData("Pestilent Mist",                      0x401A8CE0, DS3ItemCategory.SPELL,
                classification = ItemClassification.useful), # Originally called "Pestilent Mercury" pre 1.15
    DS3ItemData("Fireball",                            0x40249F00, DS3ItemCategory.SPELL),
    DS3ItemData("Fire Orb",                            0x4024A6D0, DS3ItemCategory.SPELL),
    DS3ItemData("Firestorm",                           0x4024AAB8, DS3ItemCategory.SPELL),
    DS3ItemData("Fire Surge",                          0x4024B288, DS3ItemCategory.SPELL),
    DS3ItemData("Black Serpent",                       0x4024BA58, DS3ItemCategory.SPELL),
    DS3ItemData("Combustion",                          0x4024C610, DS3ItemCategory.SPELL),
    DS3ItemData("Great Combustion",                    0x4024C9F8, DS3ItemCategory.SPELL),
    DS3ItemData("Poison Mist",                         0x4024ED20, DS3ItemCategory.SPELL),
    DS3ItemData("Toxic Mist",                          0x4024F108, DS3ItemCategory.SPELL),
    DS3ItemData("Acid Surge",                          0x4024F4F0, DS3ItemCategory.SPELL),
    DS3ItemData("Iron Flesh",                          0x40251430, DS3ItemCategory.SPELL),
    DS3ItemData("Flash Sweat",                         0x40251818, DS3ItemCategory.SPELL),
    DS3ItemData("Carthus Flame Arc",                   0x402527B8, DS3ItemCategory.SPELL),
    DS3ItemData("Rapport",                             0x40252BA0, DS3ItemCategory.SPELL,
                classification = ItemClassification.useful),
    DS3ItemData("Power Within",                        0x40253B40, DS3ItemCategory.SPELL,
                classification = ItemClassification.useful),
    DS3ItemData("Great Chaos Fire Orb",                0x40256250, DS3ItemCategory.SPELL),
    DS3ItemData("Chaos Storm",                         0x40256638, DS3ItemCategory.SPELL),
    DS3ItemData("Fire Whip",                           0x40256A20, DS3ItemCategory.SPELL),
    DS3ItemData("Black Flame",                         0x40256E08, DS3ItemCategory.SPELL),
    DS3ItemData("Profaned Flame",                      0x402575D8, DS3ItemCategory.SPELL),
    DS3ItemData("Chaos Bed Vestiges",                  0x402579C0, DS3ItemCategory.SPELL),
    DS3ItemData("Warmth",                              0x4025B070, DS3ItemCategory.SPELL,
                inject = True), # Covenant reward
    DS3ItemData("Profuse Sweat",                       0x402717D0, DS3ItemCategory.SPELL),
    DS3ItemData("Black Fire Orb",                      0x4027D350, DS3ItemCategory.SPELL),
    DS3ItemData("Bursting Fireball",                   0x4027FA60, DS3ItemCategory.SPELL),
    DS3ItemData("Boulder Heave",                       0x40282170, DS3ItemCategory.SPELL),
    DS3ItemData("Sacred Flame",                        0x40284880, DS3ItemCategory.SPELL),
    DS3ItemData("Carthus Beacon",                      0x40286F90, DS3ItemCategory.SPELL),
    DS3ItemData("Heal Aid",                            0x403540D0, DS3ItemCategory.SPELL),
    DS3ItemData("Heal",                                0x403567E0, DS3ItemCategory.SPELL),
    DS3ItemData("Med Heal",                            0x40356BC8, DS3ItemCategory.SPELL,
                classification = ItemClassification.useful),
    DS3ItemData("Great Heal",                          0x40356FB0, DS3ItemCategory.SPELL),
    DS3ItemData("Soothing Sunlight",                   0x40357398, DS3ItemCategory.SPELL),
    DS3ItemData("Replenishment",                       0x40357780, DS3ItemCategory.SPELL),
    DS3ItemData("Bountiful Sunlight",                  0x40357B68, DS3ItemCategory.SPELL),
    DS3ItemData("Bountiful Light",                     0x40358338, DS3ItemCategory.SPELL),
    DS3ItemData("Caressing Tears",                     0x40358720, DS3ItemCategory.SPELL),
    DS3ItemData("Tears of Denial",                     0x4035B600, DS3ItemCategory.SPELL,
                classification = ItemClassification.useful),
    DS3ItemData("Homeward",                            0x4035B9E8, DS3ItemCategory.SPELL,
                classification = ItemClassification.useful),
    DS3ItemData("Force",                               0x4035DD10, DS3ItemCategory.SPELL),
    DS3ItemData("Wrath of the Gods",                   0x4035E0F8, DS3ItemCategory.SPELL),
    DS3ItemData("Emit Force",                          0x4035E4E0, DS3ItemCategory.SPELL),
    DS3ItemData("Seek Guidance",                       0x40360420, DS3ItemCategory.SPELL),
    DS3ItemData("Lightning Spear",                     0x40362B30, DS3ItemCategory.SPELL),
    DS3ItemData("Great Lightning Spear",               0x40362F18, DS3ItemCategory.SPELL,
                inject = True), # Covenant reward
    DS3ItemData("Sunlight Spear",                      0x40363300, DS3ItemCategory.SPELL),
    DS3ItemData("Lightning Storm",                     0x403636E8, DS3ItemCategory.SPELL),
    DS3ItemData("Gnaw",                                0x40363AD0, DS3ItemCategory.SPELL),
    DS3ItemData("Dorhys' Gnawing",                     0x40363EB8, DS3ItemCategory.SPELL),
    DS3ItemData("Magic Barrier",                       0x40365240, DS3ItemCategory.SPELL),
    DS3ItemData("Great Magic Barrier",                 0x40365628, DS3ItemCategory.SPELL),
    DS3ItemData("Sacred Oath",                         0x40365DF8, DS3ItemCategory.SPELL,
                inject = True), # Covenant reward
    DS3ItemData("Vow of Silence",                      0x4036A448, DS3ItemCategory.SPELL),
    DS3ItemData("Lightning Blade",                     0x4036C770, DS3ItemCategory.SPELL),
    DS3ItemData("Darkmoon Blade",                      0x4036CB58, DS3ItemCategory.SPELL,
                inject = True), # Covenant reward
    DS3ItemData("Dark Blade",                          0x40378AC0, DS3ItemCategory.SPELL),
    DS3ItemData("Dead Again",                          0x40387520, DS3ItemCategory.SPELL),
    DS3ItemData("Lightning Stake",                     0x40389C30, DS3ItemCategory.SPELL),
    DS3ItemData("Divine Pillars of Light",             0x4038C340, DS3ItemCategory.SPELL),
    DS3ItemData("Lifehunt Scythe",                     0x4038EA50, DS3ItemCategory.SPELL),
    DS3ItemData("Blessed Weapon",                      0x40395F80, DS3ItemCategory.SPELL),
    DS3ItemData("Deep Protection",                     0x40398690, DS3ItemCategory.SPELL),
    DS3ItemData("Atonement",                           0x4039ADA0, DS3ItemCategory.SPELL),
]

_dlc_items = [
    # Ammunition
    *DS3ItemData("Millwood Greatarrow",              0x000623E0, DS3ItemCategory.MISC).counts([5]),

    # Weapons
    DS3ItemData("Aquamarine Dagger",                0x00116520, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Murky Hand Scythe",                0x00118C30, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Onyx Blade",                       0x00222E00, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Ringed Knight Straight Sword",     0x00225510, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Gael's Greatsword",                0x00227C20, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Follower Sabre",                   0x003EDDC0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Demon's Scar",                     0x003F04D0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Frayed Blade",                     0x004D35A0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Harald Curved Greatsword",         0x006159E0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Millwood Battle Axe",              0x006D67D0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Earth Seeker",                     0x006D8EE0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Quakestone Hammer",                0x007ECCF0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Ledo's Great Hammer",              0x007EF400, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Follower Javelin",                 0x008CD6B0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Ringed Knight Spear",              0x008CFDC0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Lothric War Banner",               0x008D24D0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Crucifix of the Mad King",         0x008D4BE0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Splitleaf Greatsword",             0x009B2E90, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Friede's Great Scythe",            0x009B55A0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Crow Talons",                      0x00A89C10, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Rose of Ariandel",                 0x00B82C70, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Pyromancer's Parting Flame",       0x00CC9ED0, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Murky Longstaff",                  0x00CCC5E0, DS3ItemCategory.WEAPON_UPGRADE_10),
    DS3ItemData("Sacred Chime of Filianore",        0x00CCECF0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Preacher's Right Arm",             0x00CD1400, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("White Birch Bow",                  0x00D77440, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Millwood Greatbow",                0x00D85EA0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Repeating Crossbow",               0x00D885B0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Giant Door Shield",                0x00F5F8C0, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Valorheart",                       0x00F646E0, DS3ItemCategory.WEAPON_UPGRADE_5),
    DS3ItemData("Crow Quills",                      0x00F66DF0, DS3ItemCategory.WEAPON_UPGRADE_10_INFUSIBLE),
    DS3ItemData("Ringed Knight Paired Greatswords", 0x00F69500, DS3ItemCategory.WEAPON_UPGRADE_5),

    # Shields
    DS3ItemData("Follower Shield",                  0x0135C0E0, DS3ItemCategory.SHIELD_INFUSIBLE),
    DS3ItemData("Dragonhead Shield",                0x0135E7F0, DS3ItemCategory.SHIELD),
    DS3ItemData("Ethereal Oak Shield",              0x01450320, DS3ItemCategory.SHIELD),
    DS3ItemData("Dragonhead Greatshield",           0x01452A30, DS3ItemCategory.SHIELD),
    DS3ItemData("Follower Torch",                   0x015F1AD0, DS3ItemCategory.SHIELD),

    # Armor
    DS3ItemData("Vilhelm's Helm",                   0x11312D00, DS3ItemCategory.ARMOR),
    DS3ItemData("Vilhelm's Armor",                  0x113130E8, DS3ItemCategory.ARMOR),
    DS3ItemData("Vilhelm's Gauntlets",              0x113134D0, DS3ItemCategory.ARMOR),
    DS3ItemData("Vilhelm's Leggings",               0x113138B8, DS3ItemCategory.ARMOR),
    DS3ItemData("Antiquated Plain Garb",            0x11B2E408, DS3ItemCategory.ARMOR),
    DS3ItemData("Violet Wrappings",                 0x11B2E7F0, DS3ItemCategory.ARMOR),
    DS3ItemData("Loincloth 2",                      0x11B2EBD8, DS3ItemCategory.ARMOR),
    DS3ItemData("Shira's Crown",                    0x11C22260, DS3ItemCategory.ARMOR),
    DS3ItemData("Shira's Armor",                    0x11C22648, DS3ItemCategory.ARMOR),
    DS3ItemData("Shira's Gloves",                   0x11C22A30, DS3ItemCategory.ARMOR),
    DS3ItemData("Shira's Trousers",                 0x11C22E18, DS3ItemCategory.ARMOR),
    DS3ItemData("Lapp's Helm",                      0x11E84800, DS3ItemCategory.ARMOR),
    DS3ItemData("Lapp's Armor",                     0x11E84BE8, DS3ItemCategory.ARMOR),
    DS3ItemData("Lapp's Gauntlets",                 0x11E84FD0, DS3ItemCategory.ARMOR),
    DS3ItemData("Lapp's Leggings",                  0x11E853B8, DS3ItemCategory.ARMOR),
    DS3ItemData("Slave Knight Hood",                0x134EDCE0, DS3ItemCategory.ARMOR),
    DS3ItemData("Slave Knight Armor",               0x134EE0C8, DS3ItemCategory.ARMOR),
    DS3ItemData("Slave Knight Gauntlets",           0x134EE4B0, DS3ItemCategory.ARMOR),
    DS3ItemData("Slave Knight Leggings",            0x134EE898, DS3ItemCategory.ARMOR),
    DS3ItemData("Ordained Hood",                    0x135E1F20, DS3ItemCategory.ARMOR),
    DS3ItemData("Ordained Dress",                   0x135E2308, DS3ItemCategory.ARMOR),
    DS3ItemData("Ordained Trousers",                0x135E2AD8, DS3ItemCategory.ARMOR),
    DS3ItemData("Follower Helm",                    0x137CA3A0, DS3ItemCategory.ARMOR),
    DS3ItemData("Follower Armor",                   0x137CA788, DS3ItemCategory.ARMOR),
    DS3ItemData("Follower Gloves",                  0x137CAB70, DS3ItemCategory.ARMOR),
    DS3ItemData("Follower Boots",                   0x137CAF58, DS3ItemCategory.ARMOR),
    DS3ItemData("Millwood Knight Helm",             0x139B2820, DS3ItemCategory.ARMOR),
    DS3ItemData("Millwood Knight Armor",            0x139B2C08, DS3ItemCategory.ARMOR),
    DS3ItemData("Millwood Knight Gauntlets",        0x139B2FF0, DS3ItemCategory.ARMOR),
    DS3ItemData("Millwood Knight Leggings",         0x139B33D8, DS3ItemCategory.ARMOR),
    DS3ItemData("Ringed Knight Hood",               0x13C8EEE0, DS3ItemCategory.ARMOR),
    DS3ItemData("Ringed Knight Armor",              0x13C8F2C8, DS3ItemCategory.ARMOR),
    DS3ItemData("Ringed Knight Gauntlets",          0x13C8F6B0, DS3ItemCategory.ARMOR),
    DS3ItemData("Ringed Knight Leggings",           0x13C8FA98, DS3ItemCategory.ARMOR),
    DS3ItemData("Harald Legion Armor",              0x13D83508, DS3ItemCategory.ARMOR),
    DS3ItemData("Harald Legion Gauntlets",          0x13D838F0, DS3ItemCategory.ARMOR),
    DS3ItemData("Harald Legion Leggings",           0x13D83CD8, DS3ItemCategory.ARMOR),
    DS3ItemData("Iron Dragonslayer Helm",           0x1405F7E0, DS3ItemCategory.ARMOR),
    DS3ItemData("Iron Dragonslayer Armor",          0x1405FBC8, DS3ItemCategory.ARMOR),
    DS3ItemData("Iron Dragonslayer Gauntlets",      0x1405FFB0, DS3ItemCategory.ARMOR),
    DS3ItemData("Iron Dragonslayer Leggings",       0x14060398, DS3ItemCategory.ARMOR),
    DS3ItemData("White Preacher Head",              0x14153A20, DS3ItemCategory.ARMOR),
    DS3ItemData("Ruin Helm",                        0x14CC5520, DS3ItemCategory.ARMOR),
    DS3ItemData("Ruin Armor",                       0x14CC5908, DS3ItemCategory.ARMOR),
    DS3ItemData("Ruin Gauntlets",                   0x14CC5CF0, DS3ItemCategory.ARMOR),
    DS3ItemData("Ruin Leggings",                    0x14CC60D8, DS3ItemCategory.ARMOR),
    DS3ItemData("Desert Pyromancer Hood",           0x14DB9760, DS3ItemCategory.ARMOR),
    DS3ItemData("Desert Pyromancer Garb",           0x14DB9B48, DS3ItemCategory.ARMOR),
    DS3ItemData("Desert Pyromancer Gloves",         0x14DB9F30, DS3ItemCategory.ARMOR),
    DS3ItemData("Desert Pyromancer Skirt",          0x14DBA318, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Witch Hat",                  0x14EAD9A0, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Witch Garb",                 0x14EADD88, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Witch Wrappings",            0x14EAE170, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Witch Trousers",             0x14EAE558, DS3ItemCategory.ARMOR),
    DS3ItemData("Black Witch Veil",                 0x14FA1BE0, DS3ItemCategory.ARMOR),
    DS3ItemData("Blindfold Mask",                   0x15095E20, DS3ItemCategory.ARMOR),

    # Covenants
    DS3ItemData("Spear of the Church",              0x2000276A, DS3ItemCategory.UNIQUE, skip = True),

    # Rings
    DS3ItemData("Chloranthy Ring+3",                0x20004E2D, DS3ItemCategory.RING,
                classification = ItemClassification.useful),
    DS3ItemData("Havel's Ring+3",                   0x20004E37, DS3ItemCategory.RING,
                classification = ItemClassification.useful),
    DS3ItemData("Ring of Favor+3",                  0x20004E41, DS3ItemCategory.RING,
                classification = ItemClassification.useful),
    DS3ItemData("Ring of Steel Protection+3",       0x20004E4B, DS3ItemCategory.RING,
                classification = ItemClassification.useful),
    DS3ItemData("Wolf Ring+3",                      0x20004EE1, DS3ItemCategory.RING),
    DS3ItemData("Covetous Gold Serpent Ring+3",     0x20004FA9, DS3ItemCategory.RING),
    DS3ItemData("Covetous Silver Serpent Ring+3",   0x20004FB3, DS3ItemCategory.RING,
                classification = ItemClassification.useful),
    DS3ItemData("Ring of the Evil Eye+3",           0x20005071, DS3ItemCategory.RING),
    DS3ItemData("Chillbite Ring",                   0x20005208, DS3ItemCategory.RING),

    # Items
    DS3ItemData("Church Guardian Shiv",             0x4000013B, DS3ItemCategory.MISC),
    DS3ItemData("Filianore's Spear Ornament",       0x4000017B, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Ritual Spear Fragment",            0x4000028A, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Divine Spear Fragment",            0x4000028B, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Soul of Sister Friede",            0x400002E8, DS3ItemCategory.BOSS, souls = 20000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of Slave Knight Gael",        0x400002E9, DS3ItemCategory.BOSS, souls = 20000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of the Demon Prince",         0x400002EA, DS3ItemCategory.BOSS, souls = 20000,
                classification = ItemClassification.progression),
    DS3ItemData("Soul of Darkeater Midir",          0x400002EB, DS3ItemCategory.BOSS, souls = 20000,
                classification = ItemClassification.progression),
    DS3ItemData("Champion's Bones",                 0x40000869, DS3ItemCategory.UNIQUE, skip = True),
    DS3ItemData("Captain's Ashes",                  0x4000086A, DS3ItemCategory.MISC,
                classification = ItemClassification.progression),
    DS3ItemData("Contraption Key",                  0x4000086B, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Small Envoy Banner",               0x4000086C, DS3ItemCategory.UNIQUE,
                classification = ItemClassification.progression),
    DS3ItemData("Old Woman's Ashes",                0x4000086D, DS3ItemCategory.UNIQUE),
    DS3ItemData("Blood of the Dark Soul",           0x4000086E, DS3ItemCategory.UNIQUE, skip = True),

    # Spells
    DS3ItemData("Frozen Weapon",                    0x401408E8, DS3ItemCategory.SPELL),
    DS3ItemData("Old Moonlight",                    0x4014FF00, DS3ItemCategory.SPELL),
    DS3ItemData("Great Soul Dregs",                 0x401879A0, DS3ItemCategory.SPELL),
    DS3ItemData("Snap Freeze",                      0x401A90C8, DS3ItemCategory.SPELL),
    DS3ItemData("Floating Chaos",                   0x40257DA8, DS3ItemCategory.SPELL),
    DS3ItemData("Flame Fan",                        0x40258190, DS3ItemCategory.SPELL),
    DS3ItemData("Seething Chaos",                   0x402896A0, DS3ItemCategory.SPELL),
    DS3ItemData("Lightning Arrow",                  0x40358B08, DS3ItemCategory.SPELL),
    DS3ItemData("Way of White Corona",              0x403642A0, DS3ItemCategory.SPELL),
    DS3ItemData("Projected Heal",                   0x40364688, DS3ItemCategory.SPELL),
]
for item in _dlc_items:
    item.is_dlc = True

# Unused list for future reference
# These items exist to some degree in the code, but aren't accessible
# in-game and can't be picked up without modifications
_cut_content_items = [
    # Weapons
    DS3ItemData("Blood-stained Short Sword",           0x00100590, DS3ItemCategory.UNIQUE),
    DS3ItemData("Missionary's Axe",                    0x006C2F50, DS3ItemCategory.UNIQUE),
    DS3ItemData("Dragon King Greataxe",                0x006D40C0, DS3ItemCategory.UNIQUE),
    DS3ItemData("Four Knights Hammer",                 0x007D4650, DS3ItemCategory.UNIQUE),
    DS3ItemData("Hammer of the Great Tree",            0x007D9470, DS3ItemCategory.UNIQUE),
    DS3ItemData("Lothric's Scythe",                    0x009A4430, DS3ItemCategory.UNIQUE),
    DS3ItemData("Ancient Dragon Halberd",              0x009A6B40, DS3ItemCategory.UNIQUE),
    DS3ItemData("Scythe of Want",                      0x009A9250, DS3ItemCategory.UNIQUE),
    DS3ItemData("Sacred Beast Catalyst",               0x00C8A730, DS3ItemCategory.UNIQUE),
    DS3ItemData("Deep Pyromancy Flame",                0x00CC9ED0, DS3ItemCategory.UNIQUE), # Duplicate?
    DS3ItemData("Flickering Pyromancy Flame",          0x00CD3B10, DS3ItemCategory.UNIQUE),
    DS3ItemData("Strong Pyromancy Flame",              0x00CD6220, DS3ItemCategory.UNIQUE),
    DS3ItemData("Deep Pyromancy Flame",                0x00CDFE60, DS3ItemCategory.UNIQUE), # Duplicate?
    DS3ItemData("Pitch-Dark Pyromancy Flame",          0x00CE2570, DS3ItemCategory.UNIQUE),
    DS3ItemData("Dancer's Short Bow",                  0x00D77440, DS3ItemCategory.UNIQUE),
    DS3ItemData("Shield Crossbow",                     0x00D81080, DS3ItemCategory.UNIQUE),
    DS3ItemData("Golden Dual Swords",                  0x00F55C80, DS3ItemCategory.UNIQUE),
    DS3ItemData("Channeler's Trident",                 0x008C8890, DS3ItemCategory.UNIQUE),

    # Shields
    DS3ItemData("Cleric's Parma",                      0x013524A0, DS3ItemCategory.UNIQUE),
    DS3ItemData("Prince's Shield",                     0x01421CF0, DS3ItemCategory.UNIQUE),

    # Armor
    DS3ItemData("Dingy Maiden's Overcoat",             0x11DA9048, DS3ItemCategory.UNIQUE),
    DS3ItemData("Grotto Hat",                          0x11F78A40, DS3ItemCategory.UNIQUE),
    DS3ItemData("Grotto Robe",                         0x11F78E28, DS3ItemCategory.UNIQUE),
    DS3ItemData("Grotto Wrap",                         0x11F79210, DS3ItemCategory.UNIQUE),
    DS3ItemData("Grotto Trousers",                     0x11F795F8, DS3ItemCategory.UNIQUE),
    DS3ItemData("Soldier's Gauntlets",                 0x126261D0, DS3ItemCategory.UNIQUE),
    DS3ItemData("Soldier's Hood",                      0x1263E0A0, DS3ItemCategory.UNIQUE),
    DS3ItemData("Elder's Robe",                        0x129024A8, DS3ItemCategory.UNIQUE),
    DS3ItemData("Saint's Veil",                        0x12A70420, DS3ItemCategory.UNIQUE),
    DS3ItemData("Saint's Dress",                       0x12A70808, DS3ItemCategory.UNIQUE),
    DS3ItemData("Footman's Hood",                      0x12AEA540, DS3ItemCategory.UNIQUE),
    DS3ItemData("Footman's Overcoat",                  0x12AEA928, DS3ItemCategory.UNIQUE),
    DS3ItemData("Footman's Bracelets",                 0x12AEAD10, DS3ItemCategory.UNIQUE),
    DS3ItemData("Footman's Trousers",                  0x12AEB0F8, DS3ItemCategory.UNIQUE),
    DS3ItemData("Scholar's Shed Skin",                 0x12E40D20, DS3ItemCategory.UNIQUE),
    DS3ItemData("Man Serpent's Mask",                  0x138BE5E0, DS3ItemCategory.UNIQUE),
    DS3ItemData("Man Serpent's Robe",                  0x138BE9C8, DS3ItemCategory.UNIQUE),
    DS3ItemData("Old Monarch's Crown",                 0x13DFD240, DS3ItemCategory.UNIQUE),
    DS3ItemData("Old Monarch's Robe",                  0x13DFD628, DS3ItemCategory.UNIQUE),
    DS3ItemData("Frigid Valley Mask",                  0x13FE56C0, DS3ItemCategory.UNIQUE),
    DS3ItemData("Dingy Hood",                          0x140D9900, DS3ItemCategory.UNIQUE),
    DS3ItemData("Hexer's Hood",                        0x15A995C0, DS3ItemCategory.UNIQUE),
    DS3ItemData("Hexer's Robes",                       0x15A999A8, DS3ItemCategory.UNIQUE),
    DS3ItemData("Hexer's Gloves",                      0x15A99D90, DS3ItemCategory.UNIQUE),
    DS3ItemData("Hexer's Boots",                       0x15A9A178, DS3ItemCategory.UNIQUE),
    DS3ItemData("Varangian Helm",                      0x15C81A40, DS3ItemCategory.UNIQUE),
    DS3ItemData("Varangian Armor",                     0x15C81E28, DS3ItemCategory.UNIQUE),
    DS3ItemData("Varangian Cuffs",                     0x15C82210, DS3ItemCategory.UNIQUE),
    DS3ItemData("Varangian Leggings",                  0x15C825F8, DS3ItemCategory.UNIQUE),

    # Rings
    DS3ItemData("Rare Ring of Sacrifice",              0x20004EFC, DS3ItemCategory.UNIQUE),
    DS3ItemData("Baneful Bird Ring",                   0x20005032, DS3ItemCategory.UNIQUE),
    DS3ItemData("Darkmoon Blade Covenant Ring",        0x20004F7E, DS3ItemCategory.UNIQUE),
    DS3ItemData("Yorgh's Ring",                        0x2000505A, DS3ItemCategory.UNIQUE),
    DS3ItemData("Ring of Hiding",                      0x200050D2, DS3ItemCategory.UNIQUE),
    DS3ItemData("Ring of Sustained Toughness",         0x20005118, DS3ItemCategory.UNIQUE),
    DS3ItemData("Ring of Sustained Energy",            0x20005122, DS3ItemCategory.UNIQUE),
    DS3ItemData("Ring of Sustained Magic",             0x2000512C, DS3ItemCategory.UNIQUE),
    DS3ItemData("Ring of Sustained Essence",           0x20005140, DS3ItemCategory.UNIQUE),
    DS3ItemData("Ring of Sustained Might",             0x2000514A, DS3ItemCategory.UNIQUE),
    DS3ItemData("Ring of Sustained Fortune",           0x20005154, DS3ItemCategory.UNIQUE),

    # Items
    DS3ItemData("Soul of a Wicked Spirit",             0x400002C9, DS3ItemCategory.UNIQUE),

    # Spells
    DS3ItemData("Dark Orb",                            0x4027AC40, DS3ItemCategory.UNIQUE),
    DS3ItemData("Morbid Temptation",                   0x40359AA8, DS3ItemCategory.UNIQUE),
    DS3ItemData("Dorris Swarm",                        0x40393870, DS3ItemCategory.UNIQUE),
]


item_name_groups: Dict[str, Set] = {
    "Progression": set(),
    "Cinders": set(),
    "Weapons": set(),
    "Shields": set(),
    "Armor": set(),
    "Rings": set(),
    "Spells": set(),
    "Miscellaneous": set(),
    "Unique": set(),
    "Boss Souls": set(),
    "Small Souls": set(),
    "Upgrade": set(),
    "Healing": set(),
}


item_descriptions = {
    "Progression": "Items which unlock locations.",
    "Cinders": "All four Cinders of a Lord.\n\nOnce you have these four, you can fight Soul of Cinder and win the game.",
    "Miscellaneous": "Generic stackable items, such as arrows, firebombs, buffs, and so on.",
    "Unique": "Items that are unique per NG cycle, such as scrolls, keys, ashes, and so on. Doesn't include equipment, spells, or souls.",
    "Boss Souls": "Souls that can be traded with Ludleth, including Soul of Rosaria.",
    "Small Souls": "Soul items, not including boss souls.",
    "Upgrade": "Upgrade items, including titanite, gems, and Shriving Stones.",
    "Healing": "Undead Bone Shards and Estus Shards.",
}


_all_items = _vanilla_items + _dlc_items

for item_data in _all_items:
    for group_name in item_data.item_groups():
        item_name_groups[group_name].add(item_data.name)

filler_item_names = [item_data.name for item_data in _all_items if item_data.filler]
item_dictionary = {item_data.name: item_data for item_data in _all_items}
