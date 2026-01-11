# Data module for item/shop data.

import enum
import random
import math

from ...randomizer.logic import utils
from ...randomizer.logic.patch import Patch
from .characters import Mario, Mallow, Geno, Bowser, Peach


class ItemShuffleType(enum.Enum):
    """Enumeration for key item types for shuffling."""
    Required = enum.auto()
    Extra = enum.auto()


class Item:
    """Parent class representing an item."""
    # Global item address info.
    BASE_ADDRESS = 0x3a014d
    BASE_PRICE_ADDRESS = 0x3a40f2
    BASE_DESC_POINTER_ADDRESS = 0x3a2f20
    DESC_DATA_POINTER_OFFSET = 0x3a0000
    BASE_DESC_DATA_ADDRESSES = (
        (0x3a3120, 0x3a40f1),
        (0x3a55f0, 0x3a5fff),
    )

    # Total number of items in the data.
    NUM_ITEMS = 256

    # Stats used during equipment randomization.
    EQUIP_STATS = ["speed", "attack", "defense", "magic_attack", "magic_defense"]

    # Default per-item attributes.
    index = 0
    description = ''
    tier = 999
    order = 0
    item_type = 0
    consumable = False
    reuseable = False
    equip_chars = []
    speed = 0
    attack = 0
    defense = 0
    magic_attack = 0
    magic_defense = 0
    variance = 0
    prevent_ko = False
    elemental_immunities = []
    elemental_resistances = []
    status_immunities = []
    status_buffs = []
    price = 0
    frog_coin_item = False
    rare = False
    basic = False
    shuffle_type = ItemShuffleType.Extra
    rank_value = 0
    rank_order = 0
    rank_order_reverse = 0
    arbitrary_value = 0
    vanilla_shop = False
    hard_tier = 0
    magic_weapon = False
    effect_type = "normal"

    # Flag to override whether we include the item stats in the patch data.  By default, we only include equipment but
    # a small handful of consumable items have their effects shuffled as well.
    include_stats_in_patch = False

    def __init__(self, world):
        """

        Args:
            world (randomizer.logic.main.GameWorld):

        """
        self.world = world
        self._rank = None

    def __str__(self):
        return "<{}: price {}>".format(self.name, self.price)

    def __repr__(self):
        return str(self)

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def is_weapon(self):
        """:rtype: bool"""
        return self.item_type & 0x3 == 0

    @property
    def is_armor(self):
        """:rtype: bool"""
        return self.item_type & 0x3 == 1

    @property
    def is_accessory(self):
        """:rtype: bool"""
        return self.item_type & 0x3 == 2

    @property
    def is_equipment(self):
        """:rtype: bool"""
        return self.is_weapon or self.is_armor or self.is_accessory

    @property
    def is_key(self):
        """:rtype: bool"""
        return not (self.is_equipment or self.consumable) and self.price == 0

    @property
    def is_frog_coin_item(self):
        """:rtype: bool"""
        return self.frog_coin_item

    def become_frog_coin_item(self):
        """:rtype: bool"""
        if self.is_frog_coin_item:
            return False

        self.price = max(math.ceil(self.rank_value / 5), 1)
        self.frog_coin_item = True
        return True

    def unbecome_frog_coin_item(self):
        """:rtype: bool"""
        if not self.is_frog_coin_item:
            return False

        factor = float(random.randint(50, random.randint(50, 100)))
        price = int(round(self.price * factor))
        self.price = min(price, 9999)
        self.frog_coin_item = False
        return True

    @property
    def max_price(self):
        """
        Returns:
            int: Max allowed price for this item based on whether it's a frog coin item or not.
        """
        return 99 if self.is_frog_coin_item else 9999

    @property
    def primary_stats(self):
        """Primary stats of this item, depending on the type.

        :rtype: list[str]
        """
        if self.is_weapon and not self.magic_weapon:
            return ["attack"]
        elif self.magic_weapon:
            return ["magic_attack"]
        # Exclude Work Pants and Super Suit, include Rare Scarf
        elif (self.is_armor and self.index not in [43, 69]) or self.index == 82:
            return ["defense", "magic_defense"]
        # Speed items are the Zoom Shoes and Feather
        elif self.index in [74, 91]:
            return ["speed"]
        return self.EQUIP_STATS

    @property
    def stat_point_value(self):
        """Overall stat point score for rough item power during shuffle.

        :rtype: int
        """
        score = 0
        for attr in self.EQUIP_STATS:
            value = getattr(self, attr)
            # Subtract any negative value from overall score.
            if value < 0:
                score += value
            # For primary stat, add the raw value.
            elif attr in self.primary_stats:
                score += value
            # If item has positive stat outside of primary stats, consider that double points for the score.
            else:
                score += (2 * value)
        return score

    @property
    def rank(self):
        """Compute a ranking for this item based on price and type.  Used for shuffling shops.

        :rtype: float
        """
        if self.price == 0:
            if self.is_key:
                self._rank = -1
            else:
                self._rank = random.randint(1, random.randint(1, 999))
        elif self.is_frog_coin_item:
            self._rank = self.price * 50
        elif self.price > 1000:
            self._rank = self.price / 2
        elif self.rare and self.consumable:
            rank = 2 * self.price
            if self.price <= 50:
                rank = rank * 50
            if self.reuseable:
                rank = rank * 4
            self._rank = rank
        elif self.rare and self.is_armor:
            self._rank = self.price * 3
        elif self.index == 0x5e:  # quartz charm
            self._rank = 999
        elif self.rare and self.is_accessory:
            self._rank = self.price * 2
        else:
            self._rank = self.price

        # Add a small amount based on index so items with the same overall rank will be sorted by index.
        self._rank += self.index / 1000.0
        return self._rank

    def get_similar(self, candidates):
        """Get a random similar item from a list of potential candidates for this one.

        :type candidates: list[Item]
        :rtype: Item
        """
        # If this is a special item, don't replace it.
        if self.rank < 0:
            return self
        elif self not in candidates:
            return self

        # Sort by rank and mutate our position within the list to get a replacement item.
        candidates = sorted(candidates, key=lambda c: c.rank)
        index = candidates.index(self)
        index = utils.mutate_normal(index, maximum=len(candidates) - 1)
        return candidates[index]

    def build_equipment_description(self):
        """Generate shop/menu description text for the item based on shuffled stats.

        :rtype: str
        """
        if not self.is_equipment:
            return ''

        desc = ''

        # Elemental immunities and resistances.
        if self.elemental_immunities:
            desc += '\x96\x98'
            desc += utils.add_desc_fields((
                ('\x80\x98', 6, self.elemental_immunities),
                ('\x81', 4, self.elemental_immunities),
                ('\x82', 5, self.elemental_immunities),
            ))
        else:
            desc += '\x99' * 4
        desc += '\x99'

        if self.elemental_resistances:
            desc += '\x97\x98'
            desc += utils.add_desc_fields((
                ('\x80\x98', 6, self.elemental_resistances),
                ('\x81', 4, self.elemental_resistances),
                ('\x82', 5, self.elemental_resistances),
            ))
        else:
            desc += '\x99' * 4
        desc += '\x01'

        # Speed
        desc += ['\x93', '\x94'][self.speed < 0]
        desc += str(abs(self.speed)).ljust(3, '\x99') + '\x99'

        # Status immunities
        desc += utils.add_desc_fields((
            ('\x83', 0, self.status_immunities),
            ('\x84', 1, self.status_immunities),
            ('\x85', 2, self.status_immunities),
            ('\x86', 3, self.status_immunities),
            ('\x98\x87', 5, self.status_immunities),
            ('\x88', 6, self.status_immunities),
            ('\x89', True, self.prevent_ko),
            ('\x8A', 4, self.status_immunities),
        ))
        desc += '\x01'

        # Physical attack/defense
        desc += ['\x8B', '\x8C'][self.attack < 0]
        desc += ['\x20', '\x95'][4 in self.status_buffs]
        desc += str(abs(self.attack)).ljust(3, '\x99')
        desc += '\x99'
        desc += ['\x8F', '\x90'][self.defense < 0]
        desc += ['\x20', '\x95'][6 in self.status_buffs]
        desc += str(abs(self.defense)).ljust(3, '\x99')
        desc += '\x01'

        # Magic attack/defense
        desc += ['\x8D', '\x8E'][self.magic_attack < 0]
        desc += ['\x20', '\x95'][3 in self.status_buffs]
        desc += str(abs(self.magic_attack)).ljust(3, '\x99')
        desc += '\x99'
        desc += ['\x91', '\x92'][self.magic_defense < 0]
        desc += ['\x20', '\x95'][5 in self.status_buffs]
        desc += str(abs(self.magic_defense)).ljust(3, '\x99')

        return desc

    def get_patch(self):
        """Get patch for this item.

        :return: Patch data.
        :rtype: randomizer.logic.patch.Patch
        """
        patch = Patch()
        base_addr = self.BASE_ADDRESS + (self.index * 18)

        # For non-shop items with no price (key items), there is no randomization.
        if not self.price:
            return patch

        # Only modify equipment properties.
        if self.is_equipment or self.include_stats_in_patch:
            data = bytearray()

            # Only include initial item type and inflict/protect flags for equipment.
            if self.is_equipment:
                # Item type and instant KO protection.
                val = self.item_type
                if self.prevent_ko:
                    val |= 1 << 7
                data += utils.ByteField(val).as_bytes()

                # Inflict/protect flags for status ailments/buffs.
                val = 0
                if self.status_immunities:
                    val += 1 << 0
                if self.status_buffs:
                    val += 1 << 1
                data += utils.ByteField(val).as_bytes()

                # Which characters can equip
                data += utils.BitMapSet(1, [c.index for c in self.equip_chars]).as_bytes()

                patch.add_data(base_addr, data)

            # Stats and special properties.
            data = bytearray()
            data += utils.BitMapSet(1, self.elemental_immunities).as_bytes()
            data += utils.BitMapSet(1, self.elemental_resistances).as_bytes()
            data += utils.BitMapSet(1, self.status_immunities).as_bytes()
            data += utils.BitMapSet(1, self.status_buffs).as_bytes()
            data += utils.ByteField(self.speed).as_bytes()
            data += utils.ByteField(self.attack).as_bytes()
            data += utils.ByteField(self.defense).as_bytes()
            data += utils.ByteField(self.magic_attack).as_bytes()
            data += utils.ByteField(self.magic_defense).as_bytes()
            data += utils.ByteField(self.variance).as_bytes()
            patch.add_data(base_addr + 5, data)

        # Price
        price_addr = self.BASE_PRICE_ADDRESS + (self.index * 2)
        patch.add_data(price_addr, utils.ByteField(self.price, num_bytes=2).as_bytes())

        return patch

    @classmethod
    def build_descriptions_patch(cls, world):
        """Build patch data for item descriptions.  These use pointers, so we need to do them all together.

        :type world: randomizer.logic.main.GameWorld
        :return: Patch data.
        :rtype: randomizer.logic.patch.Patch
        """
        patch = Patch()

        # Begin text data with a single null byte to use for all empty descriptions to save space.
        pointer_data = bytearray()
        text_data = []
        for i in range(len(cls.BASE_DESC_DATA_ADDRESSES)):
            text_data.append(bytearray())
        text_data[0].append(0x00)

        # Track current base address for the text.  We have multiple banks to split the text across.
        current_bank = 0

        # Make list of blank descriptions for all items, and get description for each valid item we have based on index.
        descriptions = [''] * cls.NUM_ITEMS
        for item in world.items:
            # If this isn't an equipment, use the vanilla description, if any.
            if item.is_equipment:
                desc = item.build_equipment_description()
            else:
                desc = item.description
            descriptions[item.index] = desc

        # Now build the actual pointer data.
        for desc in descriptions:
            # If the description is empty, just use the null byte at the very beginning.
            if not desc:
                pointer = cls.BASE_DESC_DATA_ADDRESSES[0][0] - cls.DESC_DATA_POINTER_OFFSET
                pointer_data += utils.ByteField(pointer, num_bytes=2).as_bytes()
                continue

            # Compute pointer from base address and current data length.  If we exceed the ending address of the current
            # data bank, move to the next one.  If we run out, it's an error.
            while True:
                pointer = cls.BASE_DESC_DATA_ADDRESSES[current_bank][0] + len(text_data[current_bank])
                if (pointer + len(desc) + 1) > cls.BASE_DESC_DATA_ADDRESSES[current_bank][1]:
                    current_bank += 1
                    if current_bank >= len(cls.BASE_DESC_DATA_ADDRESSES):
                        raise ValueError("Text descriptions too long")
                    continue

                # Subtract base pointer offset from computed final address.
                pointer -= cls.DESC_DATA_POINTER_OFFSET
                pointer_data += utils.ByteField(pointer, num_bytes=2).as_bytes()
                break

            # Add null byte to terminate the text string.
            desc = desc.encode('latin1')
            desc += bytes([0x00])
            text_data[current_bank] += desc

        # Sanity check that pointer data has the correct number of items.
        if len(pointer_data) != cls.NUM_ITEMS * 2:
            raise ValueError("Wrong length for pointer data, something went wrong...")

        # Sanity check that text data doesn't exceed size of each bank.
        for i, bank in enumerate(cls.BASE_DESC_DATA_ADDRESSES):
            data_len = len(text_data[i])
            bank_len = bank[1] - bank[0] + 1
            if data_len > bank_len:
                raise ValueError("Item description data bank {} too long: {} > max {}".format(i, data_len, bank_len))

        # Add item description data to the patch data.
        patch.add_data(cls.BASE_DESC_POINTER_ADDRESS, pointer_data)
        for i, bank in enumerate(cls.BASE_DESC_DATA_ADDRESSES):
            patch.add_data(bank[0], text_data[i])

        return patch


# *************************** Actual item classes

class Hammer(Item):
    index = 5
    description = 'Pounds\x01enemies'
    tier = 5
    order = 53
    equip_chars = [Mario]
    attack = 10
    variance = 1
    price = 70
    rare = True


class FroggieStick(Item):
    index = 6
    description = 'Frogfucius\x01made it'
    tier = 5
    order = 67
    equip_chars = [Mallow]
    attack = 20
    variance = 2
    price = 180
    rare = True


class NokNokShell(Item):
    index = 7
    description = 'Kick to attack'
    tier = 5
    order = 58
    equip_chars = [Mario]
    attack = 20
    variance = 2
    price = 20
    vanilla_shop = True


class PunchGlove(Item):
    index = 8
    description = 'Knock out\x01power!'
    tier = 5
    order = 48
    equip_chars = [Mario]
    attack = 30
    variance = 3
    price = 36
    vanilla_shop = True


class FingerShot(Item):
    index = 9
    description = 'Fingers shoot\x01bullets'
    tier = 5
    order = 70
    equip_chars = [Geno]
    attack = 12
    variance = 3
    price = 50
    vanilla_shop = True


class Cymbals(Item):
    index = 10
    description = 'Scare enemies\x01with a clash'
    tier = 5
    order = 60
    equip_chars = [Mallow]
    attack = 30
    variance = 3
    price = 42
    vanilla_shop = True


class Chomp(Item):
    index = 11
    description = 'Just spin me\x01at an enemy!'
    tier = 3
    order = 64
    equip_chars = [Bowser]
    attack = 10
    variance = 4
    price = 140
    rare = True


class Masher(Item):
    index = 12
    description = 'Makes monster\x01mash!'
    tier = 3
    order = 54
    equip_chars = [Mario]
    attack = 50
    variance = 30
    price = 160
    rare = True


class ChompShell(Item):
    index = 13
    description = 'It~s a\x01Kinklink shell'
    tier = 5
    order = 65
    equip_chars = [Bowser]
    attack = 9
    variance = 3
    price = 60
    vanilla_shop = True


class SuperHammer(Item):
    index = 14
    description = 'The standard\x01for hammers!'
    tier = 5
    order = 55
    equip_chars = [Mario]
    attack = 40
    variance = 4
    price = 70
    vanilla_shop = True


class HandGun(Item):
    index = 15
    description = 'It packs a kick'
    tier = 5
    order = 72
    equip_chars = [Geno]
    attack = 24
    variance = 4
    price = 75
    vanilla_shop = True


class WhompGlove(Item):
    index = 16
    description = 'The old double\x01whammie!'
    tier = 5
    order = 52
    equip_chars = [Mallow]
    attack = 40
    variance = 4
    price = 72
    vanilla_shop = True


class SlapGlove(Item):
    index = 17
    description = 'It slaps ~em\x01silly'
    tier = 5
    order = 49
    equip_chars = [Peach]
    attack = 40
    variance = 4
    price = 100


class TroopaShell(Item):
    index = 18
    description = 'Kick with it!'
    tier = 5
    order = 59
    equip_chars = [Mario]
    attack = 50
    variance = 5
    price = 90
    vanilla_shop = True


class Parasol(Item):
    index = 19
    description = 'Inflicts\x01serious pain!'
    tier = 5
    order = 68
    equip_chars = [Peach]
    attack = 50
    variance = 5
    price = 84
    vanilla_shop = True


class HurlyGloves(Item):
    index = 20
    description = 'A classic\x01Mario}toss\x01attack'
    tier = 5
    order = 46
    equip_chars = [Bowser]
    attack = 20
    variance = 5
    price = 92
    vanilla_shop = True

    def get_patch(self):
        """Get patch for this item.

        Returns:
            randomizer.logic.patch.Patch:
        """
        patch = super().get_patch()

        # Alter Hurly Gloves animation script so it thinks Mario is dead and always uses the doll.  This avoids softlock
        # issues in some situations when Mario is alive but not present, or Mario uses the gloves to throw himself!
        patch.add_data(0x35f672, bytes([0x20, 0x0f, 0x01, 0x00, 0x2c, 0x0f, 0x00, 0x00]))
        patch.add_data(0x35f5f8, bytes([0x20, 0x0f, 0x01, 0x00, 0x2c, 0x0f, 0x00, 0x00]))

        return patch


class DoublePunch(Item):
    index = 21
    description = 'A handy double\x01rocket punch'
    tier = 5
    order = 44
    equip_chars = [Geno]
    attack = 35
    variance = 5
    price = 88
    vanilla_shop = True


class RibbitStick(Item):
    index = 22
    description = 'It~ll come\x01in handy'
    tier = 5
    order = 69
    equip_chars = [Mallow]
    attack = 50
    variance = 5
    price = 86
    vanilla_shop = True


class SpikedLink(Item):
    index = 23
    description = 'A studded ball\x01and chain!'
    tier = 4
    order = 66
    equip_chars = [Bowser]
    attack = 30
    variance = 6
    price = 94
    vanilla_shop = True


class MegaGlove(Item):
    index = 24
    description = 'Packs a mega\x01wallop!'
    tier = 4
    order = 47
    equip_chars = [Mario]
    attack = 60
    variance = 6
    price = 102
    vanilla_shop = True


class WarFan(Item):
    index = 25
    description = 'A mysterious\x01battle fan!'
    tier = 4
    order = 63
    equip_chars = [Peach]
    attack = 60
    variance = 6
    price = 100
    vanilla_shop = True


class HandCannon(Item):
    index = 26
    description = 'Shoots bullets\x01from elbow!'
    tier = 3
    order = 71
    equip_chars = [Geno]
    attack = 45
    variance = 6
    price = 105
    vanilla_shop = True


class StickyGlove(Item):
    index = 27
    description = 'Launches a\x01punch attack.'
    tier = 4
    order = 50
    equip_chars = [Mallow]
    attack = 60
    variance = 6
    price = 98
    vanilla_shop = True


class UltraHammer(Item):
    index = 28
    description = 'The ultimate\x01hammer!'
    tier = 2
    order = 56
    equip_chars = [Mario]
    attack = 70
    variance = 7
    price = 115
    rare = True


class SuperSlap(Item):
    index = 29
    description = 'The Princess~\x01mega}slap!'
    tier = 2
    order = 51
    equip_chars = [Peach]
    attack = 70
    variance = 7
    price = 110
    rare = True


class DrillClaw(Item):
    index = 30
    description = 'A drilling\x01claw!'
    tier = 2
    order = 45
    equip_chars = [Bowser]
    attack = 40
    variance = 7
    price = 118
    rare = True


class StarGun(Item):
    index = 31
    description = 'Try shooting\x01stars!'
    tier = 1
    order = 73
    equip_chars = [Geno]
    attack = 57
    variance = 7
    price = 120
    rare = True


class SonicCymbal(Item):
    index = 32
    description = 'Puts noise to\x01work for you!'
    tier = 2
    order = 61
    equip_chars = [Mallow]
    attack = 70
    variance = 7
    price = 108
    rare = True


class LazyShellWeapon(Item):
    index = 33
    description = 'Toss a shell\x01at an enemy!'
    tier = 1
    order = 57
    equip_chars = [Mario]
    attack = 90
    variance = 40
    price = 200
    rare = True


class FryingPan(Item):
    index = 34
    description = 'Enough iron to\x01be dangerous!'
    tier = 1
    order = 62
    equip_chars = [Peach]
    attack = 90
    variance = 20
    price = 300
    rare = True


class LuckyHammer(Item):
    index = 35
    description = 'A lucky hammer!'
    tier = 1
    order = 54
    equip_chars = [Mario]
    price = 123
    vanilla_shop = True


class Shirt(Item):
    index = 37
    description = 'It~s a\x01shirt!'
    tier = 5
    order = 102
    item_type = 1
    equip_chars = [Mario]
    defense = 6
    magic_defense = 6
    price = 7
    vanilla_shop = True


class Pants(Item):
    index = 38
    description = 'It~s a pair\x01of pants!'
    tier = 5
    order = 95
    item_type = 1
    equip_chars = [Mallow]
    defense = 6
    magic_defense = 3
    price = 7
    vanilla_shop = True


class ThickShirt(Item):
    index = 39
    description = 'A padded shirt'
    tier = 5
    order = 106
    item_type = 1
    equip_chars = [Mario]
    defense = 12
    magic_defense = 8
    price = 14
    vanilla_shop = True


class ThickPants(Item):
    index = 40
    description = 'Padded pants'
    tier = 5
    order = 105
    item_type = 1
    equip_chars = [Mallow]
    defense = 12
    magic_defense = 6
    price = 14
    vanilla_shop = True


class MegaShirt(Item):
    index = 41
    description = 'Durable stay}\x01pressed shirt'
    tier = 5
    order = 93
    item_type = 1
    equip_chars = [Mario]
    defense = 18
    magic_defense = 10
    price = 22
    vanilla_shop = True


class MegaPants(Item):
    index = 42
    description = 'Durable work\x01pants'
    tier = 5
    order = 92
    item_type = 1
    equip_chars = [Mallow]
    defense = 18
    magic_defense = 9
    price = 22
    vanilla_shop = True


class WorkPants(Item):
    index = 43
    description = 'Sweaty\x01work pants!'
    tier = 5
    order = 107
    item_type = 1
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    speed = 5
    attack = 10
    defense = 15
    magic_attack = 10
    magic_defense = 5
    price = 22
    vanilla_shop = True


class MegaCape(Item):
    index = 44
    description = 'Durable\x01pressed cape'
    tier = 5
    order = 91
    item_type = 1
    equip_chars = [Geno]
    defense = 6
    magic_defense = 3
    price = 22
    vanilla_shop = True


class HappyShirt(Item):
    index = 45
    description = 'A lucky shirt'
    tier = 5
    order = 87
    item_type = 1
    equip_chars = [Mario]
    defense = 24
    magic_defense = 12
    price = 38
    vanilla_shop = True


class HappyPants(Item):
    index = 46
    description = 'A lucky\x01pair of pants'
    tier = 5
    order = 85
    item_type = 1
    equip_chars = [Mallow]
    defense = 24
    magic_defense = 12
    price = 38
    vanilla_shop = True


class HappyCape(Item):
    index = 47
    description = 'A lucky cape'
    tier = 5
    order = 84
    item_type = 1
    equip_chars = [Geno]
    defense = 12
    magic_defense = 6
    price = 38
    vanilla_shop = True


class HappyShell(Item):
    index = 48
    description = 'A lucky shell'
    tier = 5
    order = 86
    item_type = 1
    equip_chars = [Bowser]
    defense = 6
    magic_defense = 3
    price = 38
    vanilla_shop = True


class PolkaDress(Item):
    index = 49
    description = 'A flashy dress'
    tier = 5
    order = 96
    item_type = 1
    equip_chars = [Peach]
    defense = 24
    magic_defense = 12
    price = 160
    rare = True


class SailorShirt(Item):
    index = 50
    description = 'A sailor~s\x01suit'
    tier = 5
    order = 101
    item_type = 1
    equip_chars = [Mario]
    defense = 30
    magic_defense = 15
    price = 50
    vanilla_shop = True


class SailorPants(Item):
    index = 51
    description = 'A sailor~s\x01pants'
    tier = 5
    order = 100
    item_type = 1
    equip_chars = [Mallow]
    defense = 30
    magic_defense = 15
    price = 50
    vanilla_shop = True


class SailorCape(Item):
    index = 52
    description = 'A sailor~s\x01cape'
    tier = 5
    order = 99
    item_type = 1
    equip_chars = [Geno]
    defense = 18
    magic_defense = 9
    price = 50
    vanilla_shop = True


class NauticaDress(Item):
    index = 53
    description = 'A female\x01sailor~s dress'
    tier = 5
    order = 94
    item_type = 1
    equip_chars = [Peach]
    defense = 30
    magic_defense = 15
    price = 50
    vanilla_shop = True


class CourageShell(Item):
    index = 54
    description = 'A stout shell'
    tier = 4
    order = 74
    item_type = 1
    equip_chars = [Bowser]
    defense = 12
    magic_defense = 6
    price = 60
    vanilla_shop = True


class FuzzyShirt(Item):
    index = 55
    description = 'A fuzzy shirt'
    tier = 4
    order = 83
    item_type = 1
    equip_chars = [Mario]
    defense = 36
    magic_defense = 18
    price = 70
    vanilla_shop = True


class FuzzyPants(Item):
    index = 56
    description = 'Fuzzy pants'
    tier = 4
    order = 82
    item_type = 1
    equip_chars = [Mallow]
    defense = 36
    magic_defense = 18
    price = 70
    vanilla_shop = True


class FuzzyCape(Item):
    index = 57
    description = 'A fuzzy cape'
    tier = 4
    order = 80
    item_type = 1
    equip_chars = [Geno]
    defense = 24
    magic_defense = 12
    price = 70
    vanilla_shop = True


class FuzzyDress(Item):
    index = 58
    description = 'A fuzzy dress'
    tier = 4
    order = 81
    item_type = 1
    equip_chars = [Peach]
    defense = 36
    magic_defense = 18
    price = 70
    vanilla_shop = True


class FireShirt(Item):
    index = 59
    description = 'Determined\x01person~s shirt'
    tier = 4
    order = 79
    item_type = 1
    equip_chars = [Mario]
    defense = 42
    magic_defense = 21
    price = 90
    vanilla_shop = True


class FirePants(Item):
    index = 60
    description = 'Determined\x01person~s pants'
    tier = 4
    order = 77
    item_type = 1
    equip_chars = [Mallow]
    defense = 42
    magic_defense = 21
    price = 90
    vanilla_shop = True


class FireCape(Item):
    index = 61
    description = 'Determined\x01person~s cape'
    tier = 4
    order = 75
    item_type = 1
    equip_chars = [Geno]
    defense = 30
    magic_defense = 15
    price = 90
    vanilla_shop = True


class FireShell(Item):
    index = 62
    description = 'Determined\x01person~s shell'
    tier = 4
    order = 78
    item_type = 1
    equip_chars = [Bowser]
    defense = 18
    magic_defense = 9
    price = 90
    vanilla_shop = True


class FireDress(Item):
    index = 63
    description = 'Determined\x01woman~s dress'
    tier = 4
    order = 76
    item_type = 1
    equip_chars = [Peach]
    defense = 42
    magic_defense = 21
    price = 90
    vanilla_shop = True


class HeroShirt(Item):
    index = 64
    description = 'A legendary\x01shirt.'
    tier = 3
    order = 89
    item_type = 1
    equip_chars = [Mario]
    defense = 48
    magic_defense = 24
    price = 100
    vanilla_shop = True


class PrincePants(Item):
    index = 65
    description = 'Legendary\x01pants!'
    tier = 3
    order = 97
    item_type = 1
    equip_chars = [Mallow]
    defense = 48
    magic_defense = 24
    price = 100
    vanilla_shop = True


class StarCape(Item):
    index = 66
    description = 'A legendary\x01cape.'
    tier = 3
    order = 103
    item_type = 1
    equip_chars = [Geno]
    defense = 36
    magic_defense = 18
    price = 100
    vanilla_shop = True


class HealShell(Item):
    index = 67
    description = 'A legendary\x01shell.'
    tier = 3
    order = 88
    item_type = 1
    equip_chars = [Bowser]
    defense = 24
    magic_defense = 12
    price = 100
    vanilla_shop = True


class RoyalDress(Item):
    index = 68
    description = 'A legendary\x01dress!'
    tier = 3
    order = 98
    item_type = 1
    equip_chars = [Peach]
    defense = 48
    magic_defense = 24
    price = 100
    vanilla_shop = True


class SuperSuit(Item):
    index = 69
    description = 'A truly fine\x01suit!'
    tier = 1
    order = 104
    item_type = 1
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    speed = 30
    attack = 50
    defense = 50
    magic_attack = 50
    magic_defense = 50
    elemental_immunities = [4, 5, 6, 7]
    status_immunities = [0, 1, 2, 3, 4, 5, 6]
    price = 700
    rare = True
    effect_type = "elemental immunity"


class LazyShellArmor(Item):
    index = 70
    description = 'A stout and\x01durable shell.'
    tier = 1
    order = 90
    item_type = 1
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    speed = -50
    attack = -50
    defense = 127
    magic_attack = -50
    magic_defense = 127
    elemental_immunities = [4, 5, 6, 7]
    status_immunities = [0, 1, 2, 3, 4, 5, 6]
    price = 222
    rare = True
    effect_type = "elemental immunity"


class ZoomShoes(Item):
    index = 74
    description = 'Speed up by 10!'
    tier = 4
    order = 128
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    speed = 10
    defense = 5
    magic_defense = 5
    price = 100


class SafetyBadge(Item):
    index = 75
    description = 'Prevents Mute \x9c\x01Poison attacks'
    tier = 2
    order = 121
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    defense = 5
    magic_defense = 5
    status_immunities = [0, 1, 2, 3, 4, 5, 6]
    price = 500
    rare = True
    effect_type = "status protection"


class JumpShoes(Item):
    index = 76
    description = 'Use jump attacks\x01against any foe'
    tier = 5
    order = 118
    item_type = 2
    equip_chars = [Mario]
    speed = 2
    defense = 1
    magic_attack = 5
    magic_defense = 1
    price = 30
    vanilla_shop = True


class SafetyRing(Item):
    index = 77
    description = 'Guards against\x01mortal blows.'
    tier = 1
    order = 122
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    speed = 5
    defense = 5
    magic_defense = 5
    prevent_ko = True
    elemental_immunities = [4, 5, 6, 7]
    status_immunities = [0, 1, 2, 3, 4, 5, 6]
    price = 800
    rare = True
    effect_type = "elemental immunity"


class Amulet(Item):
    index = 78
    description = 'Great item,\x01bad smell!'
    tier = 2
    order = 108
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    speed = -5
    attack = 7
    defense = 7
    magic_attack = 7
    magic_defense = 7
    elemental_resistances = [4, 5, 6, 7]
    price = 200
    rare = True
    effect_type = "elemental resistance"


class ScroogeRing(Item):
    index = 79
    description = 'Cuts FP use\x01in half\x01during battle'
    tier = 4
    order = 123
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    price = 50
    frog_coin_item = True
    rare = True
    vanilla_shop = True


class ExpBooster(Item):
    index = 80
    description = 'Doubles Exp.\x01when equipped'
    tier = 4
    order = 113
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    price = 22
    frog_coin_item = True
    rare = True
    vanilla_shop = True
    effect_type = "few effects"


class AttackScarf(Item):
    index = 81
    description = 'So comfy it~ll\x01make you jump!'
    tier = 1
    order = 110
    item_type = 2
    equip_chars = [Mario]
    speed = 30
    attack = 30
    defense = 30
    magic_attack = 30
    magic_defense = 30
    prevent_ko = True
    price = 1500
    rare = True


class RareScarf(Item):
    index = 82
    description = 'Raises defense\x01power!'
    tier = 4
    order = 120
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    defense = 15
    magic_defense = 15
    price = 150
    rare = True


class BtubRing(Item):
    index = 83
    description = 'You~ll win her\x01heart with this!'
    tier = 2
    order = 111
    item_type = 2
    equip_chars = [Peach]
    elemental_resistances = [4, 5, 6, 7]
    price = 145
    vanilla_shop = True


class AntidotePin(Item):
    index = 84
    description = 'Prevents\x01poison damage'
    tier = 3
    order = 109
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    defense = 2
    magic_defense = 2
    status_immunities = [2]
    price = 28
    vanilla_shop = True
    effect_type = "status protection"


class WakeUpPin(Item):
    index = 85
    description = 'Prevents Mute \x9c\x01Sleep attacks'
    tier = 3
    order = 127
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    defense = 3
    magic_defense = 3
    status_immunities = [0, 1]
    price = 42
    vanilla_shop = True
    effect_type = "status protection"


class FearlessPin(Item):
    index = 86
    description = 'Prevents Fear\x01attacks'
    tier = 3
    order = 114
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    defense = 5
    magic_defense = 5
    status_immunities = [3]
    price = 130
    vanilla_shop = True
    effect_type = "status protection"


class TrueformPin(Item):
    index = 87
    description = 'You won~t be\x01turned into\x01Mushrooms or\x01Scarecrows!'
    tier = 3
    order = 126
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    defense = 4
    magic_defense = 4
    status_immunities = [5, 6]
    price = 60
    vanilla_shop = True
    effect_type = "status protection"


class CoinTrick(Item):
    index = 88
    description = 'Doubles the\x01coins you win\x01in battle'
    tier = 4
    order = 112
    item_type = 2
    equip_chars = [Mario]
    price = 36
    frog_coin_item = True
    rare = True
    vanilla_shop = True
    effect_type = "few effects"


class GhostMedal(Item):
    index = 89
    description = 'Raises defense\x01while attacking'
    tier = 2
    order = 116
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    status_buffs = [5, 6]
    price = 1600
    rare = True
    effect_type = "buffs"


class JinxBelt(Item):
    index = 90
    description = 'Jinx~s emblem\x01of power!'
    tier = 1
    order = 117
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    speed = 12
    attack = 27
    defense = 27
    prevent_ko = True
    price = 1998
    rare = True


class Feather(Item):
    index = 91
    description = 'Speed up by 20'
    tier = 2
    order = 115
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    speed = 20
    defense = 5
    magic_defense = 5
    price = 666
    rare = True


class TroopaPin(Item):
    index = 92
    description = 'Grants "Troopa#\x01confidence!'
    tier = 2
    order = 125
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    speed = 20
    status_buffs = [3, 4]
    price = 1000
    rare = True
    effect_type = "buffs"


class SignalRing(Item):
    index = 93
    description = 'Noise indicates\x01a hidden chest.'
    tier = 4
    order = 124
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    speed = 10
    price = 600
    rare = True


class QuartzCharm(Item):
    index = 94
    description = 'Shining source\x01of power!'
    tier = 1
    order = 119
    item_type = 2
    equip_chars = [Mario, Mallow, Geno, Bowser, Peach]
    prevent_ko = True
    status_buffs = [3, 4, 5, 6]
    price = 7
    rare = True
    effect_type = "buffs"


class Mushroom(Item):
    index = 96
    description = 'Recovers 30 HP'
    order = 15
    item_type = 3
    consumable = True
    price = 4
    basic = True
    vanilla_shop = True
    hard_tier = 1


class MidMushroom(Item):
    index = 97
    description = 'Recovers 80 HP'
    order = 13
    item_type = 3
    consumable = True
    price = 20
    basic = True
    vanilla_shop = True
    hard_tier = 2


class MaxMushroom(Item):
    index = 98
    description = 'Recovers all HP'
    order = 11
    item_type = 3
    consumable = True
    price = 78
    basic = True
    vanilla_shop = True
    hard_tier = 3


class HoneySyrup(Item):
    index = 99
    description = 'Recovers 10 FP'
    order = 8
    item_type = 3
    consumable = True
    price = 10
    basic = True
    vanilla_shop = True
    hard_tier = 1


class MapleSyrup(Item):
    index = 100
    description = 'Recovers 40 FP'
    order = 10
    item_type = 3
    consumable = True
    price = 30
    basic = True
    vanilla_shop = True
    hard_tier = 2


class RoyalSyrup(Item):
    index = 101
    description = 'Recovers all FP'
    order = 21
    item_type = 3
    consumable = True
    price = 101
    rare = True
    basic = True
    hard_tier = 3


class PickMeUp(Item):
    index = 102
    description = 'Revives downed\x01allies'
    order = 17
    item_type = 3
    consumable = True
    price = 5
    basic = True
    vanilla_shop = True
    hard_tier = 1


class AbleJuice(Item):
    index = 103
    description = 'Heal status\x01ailments'
    item_type = 3
    consumable = True
    status_immunities = [0, 1, 2, 3, 4, 5, 6]
    price = 4
    basic = True
    vanilla_shop = True
    hard_tier = 1


class Bracer(Item):
    index = 104
    description = 'Raises ally~s\x01def. in battle'
    order = 2
    item_type = 3
    consumable = True
    status_buffs = [5, 6]
    price = 50
    frog_coin_item = True
    rare = True
    vanilla_shop = True
    hard_tier = 2
    rank_value = 10


class Energizer(Item):
    index = 105
    description = 'Raises ally~s\x01battle power\x01during battle'
    order = 5
    item_type = 3
    consumable = True
    status_buffs = [3, 4]
    price = 50
    frog_coin_item = True
    rare = True
    vanilla_shop = True
    hard_tier = 2


class YoshiAde(Item):
    index = 106
    description = 'Power raised\x01during battle'
    order = 23
    item_type = 3
    consumable = True
    status_buffs = [3, 4, 5, 6]
    price = 200
    rare = True
    hard_tier = 3


class RedEssence(Item):
    index = 107
    description = 'Become invincible\x01for 3 turns'
    order = 19
    item_type = 3
    consumable = True
    status_immunities = [7]
    price = 400
    rare = True
    hard_tier = 4


class KerokeroCola(Item):
    index = 108
    description = 'All members\x01recover fully'
    order = 9
    item_type = 3
    consumable = True
    price = 400
    vanilla_shop = True
    hard_tier = 4


class YoshiCookie(Item):
    index = 109
    description = 'Summons Yoshi\x01during battle'
    order = 26
    item_type = 3
    consumable = True
    price = 100
    rare = True
    hard_tier = 1


class PureWater(Item):
    index = 110
    description = 'Defeats ghosts\x01in a wink'
    order = 30
    item_type = 3
    consumable = True
    price = 150
    rare = True
    hard_tier = 1


class SleepyBomb(Item):
    index = 111
    description = 'Puts enemies\x01to sleep'
    order = 32
    item_type = 3
    consumable = True
    status_immunities = [1]
    price = 25
    frog_coin_item = True
    rare = True
    vanilla_shop = True
    hard_tier = 1


class BadMushroom(Item):
    index = 112
    description = 'Poisons\x01an enemy'
    order = 1
    item_type = 3
    consumable = True
    status_immunities = [2]
    price = 30
    vanilla_shop = True
    hard_tier = 2


class FireBomb(Item):
    index = 113
    description = 'Hit all\x01enemies w/fire'
    order = 27
    item_type = 3
    consumable = True
    price = 200
    vanilla_shop = True
    hard_tier = 3


class IceBomb(Item):
    index = 114
    description = 'Hit all\x01enemies w/ice'
    order = 29
    item_type = 3
    consumable = True
    price = 250
    vanilla_shop = True
    hard_tier = 3


class FlowerTab(Item):
    index = 115
    description = 'Raise FP by 1'
    order = 43
    item_type = 3
    consumable = True
    price = 200
    rare = True
    hard_tier = 2


class FlowerJar(Item):
    index = 116
    description = 'Raise FP by 3'
    order = 42
    item_type = 3
    consumable = True
    price = 600
    rare = True
    hard_tier = 3


class FlowerBox(Item):
    index = 117
    description = 'Raise FP by 5'
    order = 41
    item_type = 3
    consumable = True
    price = 1000
    rare = True
    hard_tier = 4


class YoshiCandy(Item):
    index = 118
    description = 'Heals 100 HP'
    order = 25
    item_type = 3
    consumable = True
    price = 140
    rare = True
    basic = True
    hard_tier = 2


class FroggieDrink(Item):
    index = 119
    description = 'Party heals\x0130 HP'
    order = 7
    item_type = 3
    consumable = True
    price = 16
    vanilla_shop = True
    hard_tier = 1


class MukuCookie(Item):
    index = 120
    description = 'Party heals\x0169 HP'
    order = 24
    item_type = 3
    consumable = True
    status_immunities = [0, 1, 2, 3, 4, 5, 6]
    price = 69
    vanilla_shop = True
    hard_tier = 3


class Elixir(Item):
    index = 121
    description = 'Party heals\x0180 HP'
    order = 4
    item_type = 3
    consumable = True
    price = 48
    vanilla_shop = True
    hard_tier = 2


class Megalixir(Item):
    index = 122
    description = 'Party heals\x01150 HP'
    order = 12
    item_type = 3
    consumable = True
    price = 120
    vanilla_shop = True
    hard_tier = 3
    basic = True


class SeeYa(Item):
    index = 123
    description = 'Run away from\x01battles'
    order = 39
    item_type = 3
    consumable = True
    reuseable = True
    price = 250
    frog_coin_item = True
    rare = True
    vanilla_shop = True
    hard_tier = 2


class TempleKey(Item):
    index = 124
    order = 150
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class GoodieBag(Item):
    index = 125
    order = 35
    item_type = 3
    consumable = True
    reuseable = True
    price = 1110
    rare = True
    hard_tier = 1


class EarlierTimes(Item):
    index = 126
    description = 'Use it to start\x01a battle over'
    order = 34
    item_type = 3
    consumable = True
    reuseable = True
    price = 375
    frog_coin_item = True
    rare = True
    vanilla_shop = True
    hard_tier = 1


class FreshenUp(Item):
    index = 127
    description = 'Heals party\x01status ailments'
    order = 6
    item_type = 3
    consumable = True
    status_immunities = [0, 1, 2, 3, 4, 5, 6]
    price = 50
    vanilla_shop = True
    hard_tier = 2


class RareFrogCoin(Item):
    index = 128
    order = 144
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class Wallet(Item):
    index = 129
    order = 152
    item_type = 3
    price = 246
    rare = True
    hard_tier = 1


class CricketPie(Item):
    index = 130
    order = 138
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class RockCandy(Item):
    index = 131
    description = 'Attack all\x01enemies'
    order = 31
    item_type = 3
    consumable = True
    price = 400
    rare = True
    hard_tier = 4


class CastleKey1(Item):
    index = 132
    order = 135
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class CastleKey2(Item):
    index = 134
    order = 136
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class BambinoBomb(Item):
    index = 135
    order = 136
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class SheepAttack(Item):
    index = 136
    order = 40
    item_type = 3
    consumable = True
    reuseable = True
    price = 150
    rare = True
    hard_tier = 2


class CarboCookie(Item):
    index = 137
    order = 134
    item_type = 3
    price = 2
    rare = True
    hard_tier = 1


class ShinyStone(Item):
    index = 138
    order = 148
    item_type = 3
    price = 4
    rare = True
    hard_tier = 2
    shuffle_type = ItemShuffleType.Required


class RoomKey(Item):
    index = 140
    order = 145
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class ElderKey(Item):
    index = 141
    order = 140
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class ShedKey(Item):
    index = 142
    order = 147
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class LambsLure(Item):
    index = 143
    order = 36
    item_type = 3
    consumable = True
    reuseable = True
    price = 40
    rare = True
    hard_tier = 2


class FrightBomb(Item):
    index = 144
    description = 'Inflict fear\x01on one enemy'
    order = 28
    item_type = 3
    consumable = True
    status_immunities = [3]
    price = 100
    hard_tier = 2


class MysteryEgg(Item):
    index = 145
    order = 38
    item_type = 3
    consumable = True
    reuseable = True
    price = 200
    rare = True
    hard_tier = 1


class BeetleBox(Item):
    index = 146
    order = 130
    item_type = 3
    rare = True


class BeetleBox2(Item):
    index = 147
    order = 131
    item_type = 3
    rare = True


class LuckyJewel(Item):
    index = 148
    order = 37
    item_type = 3
    consumable = True
    reuseable = True
    price = 100
    rare = True
    vanilla_shop = True
    hard_tier = 1


class SopranoCard(Item):
    index = 150
    order = 149
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class AltoCard(Item):
    index = 151
    order = 129
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class TenorCard(Item):
    index = 152
    order = 151
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class Crystalline(Item):
    index = 153
    description = 'Raises party~s\x01Defense in\x01battle'
    order = 3
    item_type = 3
    consumable = True
    status_buffs = [5, 6]
    price = 125
    frog_coin_item = True
    rare = True
    vanilla_shop = True
    hard_tier = 3


class PowerBlast(Item):
    index = 154
    description = 'Raises party~s\x01Attack Power\x01in battle'
    order = 18
    item_type = 3
    consumable = True
    status_buffs = [3, 4]
    price = 125
    frog_coin_item = True
    rare = True
    vanilla_shop = True
    hard_tier = 3


class WiltShroom(Item):
    index = 155
    order = 22
    item_type = 3
    consumable = True
    price = 8
    rare = True
    basic = True
    hard_tier = 1


class RottenMush(Item):
    index = 156
    order = 20
    item_type = 3
    consumable = True
    price = 4
    rare = True
    basic = True
    hard_tier = 1


class MoldyMush(Item):
    index = 157
    order = 14
    item_type = 3
    consumable = True
    price = 2
    rare = True
    basic = True
    hard_tier = 1


class Seed(Item):
    index = 158
    order = 146
    item_type = 3
    rare = True
    hard_tier = 3
    shuffle_type = ItemShuffleType.Required


class Fertilizer(Item):
    index = 159
    order = 141
    item_type = 3
    rare = True
    hard_tier = 3
    shuffle_type = ItemShuffleType.Required


class BigBooFlag(Item):
    index = 161
    order = 132
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class DryBonesFlag(Item):
    index = 162
    order = 139
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class GreaperFlag(Item):
    index = 163
    order = 143
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class CricketJam(Item):
    index = 166
    order = 137
    item_type = 3
    rare = True
    shuffle_type = ItemShuffleType.Required


class BrightCard(Item):
    index = 174
    description = 'For the casino'
    order = 133
    item_type = 3
    rare = True
    hard_tier = 1


class Mushroom2(Item):
    index = 175
    description = 'Recoers 30 HP,\x01but...'
    order = 16
    item_type = 3
    consumable = True
    status_immunities = [5]
    price = 4
    basic = True
    vanilla_shop = True
    hard_tier = 1
    include_stats_in_patch = True


class StarEgg(Item):
    index = 176
    description = 'Reusable battle\x01item'
    order = 33
    item_type = 3
    consumable = True
    reuseable = True
    price = 300
    rare = True
    hard_tier = 4


# ****************************** Chest content/rewards data classes

class ChestReward(Item):
    """Base class for chest-only rewards."""
    pass


# *** Coins

class Coins(ChestReward):
    """Base class for coins."""
    hard_tier = 0


class Coins5(Coins):
    index = 192
    hard_tier = 1


class Coins8(Coins):
    index = 193
    hard_tier = 1


class Coins10(Coins):
    index = 194
    hard_tier = 1


class Coins150(Coins):
    index = 195
    hard_tier = 2


class Coins100(Coins):
    index = 196
    hard_tier = 2


class Coins50(Coins):
    index = 197
    hard_tier = 2


class CoinsDoubleBig(Coins):
    index = 209
    hard_tier = 1


# *** Non-coin items (flower, frog coin, mushroom, miss)

class NonCoins(ChestReward):
    """Base class for non-coin bonuses (frog coin, flower, mushroom)."""
    hard_tier = 0
    pass


class Flower(NonCoins):
    index = 198
    hard_tier = 1


class RecoveryMushroom(NonCoins):
    index = 199
    hard_tier = 1


class FrogCoin(NonCoins):
    index = 200
    hard_tier = 1


class YouMissed(NonCoins):
    index = 210
    hard_tier = 1


# *** Invincibility stars

class InvincibilityStar(ChestReward):
    """Base class for invincibility stars."""
    hard_tier = 0
    pass


class BanditsWayStar(InvincibilityStar):
    index = 201
    hard_tier = 1


class KeroSewersStar(InvincibilityStar):
    index = 202
    hard_tier = 1


class MolevilleMinesStar(InvincibilityStar):
    index = 203
    hard_tier = 2


class SeaStar(InvincibilityStar):
    index = 204
    hard_tier = 3


class LandsEndVolcanoStar(InvincibilityStar):
    index = 205
    hard_tier = 4


class NimbusLandStar(InvincibilityStar):
    index = 206
    hard_tier = 2


class LandsEndStar2(InvincibilityStar):
    index = 207
    hard_tier = 3


class LandsEndStar3(InvincibilityStar):
    index = 208
    hard_tier = 3


# ************************** Shop data classes

class Shop:
    """Class representing a shop with a list of items."""
    BASE_ADDRESS = 0x3a44df

    # Default per-shop attributes.
    index = 0
    frog_coin_shop = False
    items = []

    def __init__(self, world):
        """

        Args:
            world (randomizer.logic.main.GameWorld):

        """
        self.world = world
        # Get actual item instances for this world.
        self.items = [world.get_item_instance(i) for i in self.items]

    def __str__(self):
        return "<{}: items {}>".format(self.name, self.items)

    def __repr__(self):
        return str(self)

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def rank(self):
        """Rank for the shop based on highest priced item for balancing.

        :rtype: int
        """
        maxprice = max([i.price for i in self.items])
        if self.frog_coin_shop:
            maxprice += 2000
        return maxprice

    def get_patch(self):
        """Get patch for this shop.

        :return: Patch data.
        :rtype: randomizer.logic.patch.Patch
        """
        patch = Patch()
        base_addr = self.BASE_ADDRESS + (self.index * 16)

        data = bytearray()
        for item in self.items:
            data += utils.ByteField(item.index).as_bytes()

        # Fill out extra shop fields with no item value.
        while len(data) < 15:
            data += utils.ByteField(255).as_bytes()

        # First byte is shop flags, don't change those.  Put items one byte later.
        patch.add_data(base_addr + 1, data)

        return patch

    def is_item_allowed(self, item):
        """Check if an item is allowed in this shop given the game world.

        Args:
            item (Item):

        Returns:
            bool: True if item is allowed in this shop/world, False otherwise.

        """
        return True


class JuiceBarShop(Shop):
    """Extra subclass to identify juice bar shops."""
    pass


class PartialJuiceBarShop(JuiceBarShop):
    pass


# **************** Actual shop classes

class MushroomKingdomShop(Shop):
    index = 0
    items = [Mushroom, HoneySyrup, PickMeUp, AbleJuice, Shirt, Pants, JumpShoes, AntidotePin]

    def is_item_allowed(self, item):
        """Check if an item is allowed in this shop given the game world.

        Args:
            item (Item):

        Returns:
            bool: True if item is allowed in this shop/world, False otherwise.

        """
        # For standard mode, make sure the first two characters can equip items.
        first_chars = set([c.index for c in self.world.character_join_order[:2]])
        equip_chars = set([c.index for c in item.equip_chars])
        can_equip = self.world.open_mode or bool(equip_chars & first_chars)
        return item.consumable or ((item.is_armor or item.is_accessory) and can_equip)


class RoseTownItemShop(Shop):
    index = 1
    items = [Mushroom, HoneySyrup, PickMeUp, AbleJuice]

    def is_item_allowed(self, item):
        """Check if an item is allowed in this shop given the game world.

        Args:
            item (Item):

        Returns:
            bool: True if item is allowed in this shop/world, False otherwise.

        """
        return item.consumable


class RoseTownArmorShop(Shop):
    index = 2
    items = [ThickShirt, ThickPants, JumpShoes, AntidotePin, WakeUpPin, TrueformPin, FearlessPin]

    def is_item_allowed(self, item):
        """Check if an item is allowed in this shop given the game world.

        Args:
            item (Item):

        Returns:
            bool: True if item is allowed in this shop/world, False otherwise.

        """
        # For standard mode, make sure the first three characters can equip items.
        first_chars = set([c.index for c in self.world.character_join_order[:3]])
        equip_chars = set([c.index for c in item.equip_chars])
        can_equip = self.world.open_mode or bool(equip_chars & first_chars)
        return (item.is_armor or item.is_accessory) and can_equip


class DiscipleShop(Shop):
    index = 3
    frog_coin_shop = True
    items = [SeeYa, EarlierTimes, ExpBooster, CoinTrick, ScroogeRing]


class MolevilleShop(Shop):
    index = 4
    items = [PunchGlove, FingerShot, Cymbals, MegaShirt, MegaCape, MegaPants, WorkPants, MidMushroom, MapleSyrup]

    def is_item_allowed(self, item):
        """Check if an item is allowed in this shop given the game world.

        Args:
            item (Item):

        Returns:
            bool: True if item is allowed in this shop/world, False otherwise.

        """
        # For standard mode, make sure the first three characters can equip items.
        first_chars = set([c.index for c in self.world.character_join_order[:3]])
        equip_chars = set([c.index for c in item.equip_chars])
        can_equip = self.world.open_mode or bool(equip_chars & first_chars)
        return item.consumable or ((item.is_armor or item.is_weapon) and can_equip)


class MarrymoreShop(Shop):
    index = 5
    items = [SuperHammer, HandGun, WhompGlove, ChompShell, HappyShirt, HappyPants, HappyCape, HappyShell, BtubRing,
             MidMushroom, MapleSyrup]

    def is_item_allowed(self, item):
        return item.consumable or item.is_equipment


class FrogCoinEmporiumShop(Shop):
    index = 6
    frog_coin_shop = True
    items = [SleepyBomb, Bracer, Energizer, Crystalline, PowerBlast]


class SeaShop(Shop):
    index = 7
    items = [HurlyGloves, SuperHammer, HandGun, WhompGlove, SailorShirt, SailorPants, SailorCape, NauticaDress,
             MidMushroom, MapleSyrup, PickMeUp, AbleJuice, FreshenUp]

    def is_item_allowed(self, item):
        return item.consumable or (item.is_armor or item.is_weapon)


class SeasideYaridShop(Shop):
    index = 8
    items = [BadMushroom, MukuCookie, FrightBomb, FireBomb, IceBomb]

    def is_item_allowed(self, item):
        """Check if an item is allowed in this shop given the game world.

        Args:
            item (Item):

        Returns:
            bool: True if item is allowed in this shop/world, False otherwise.

        """
        return item.consumable


class JuiceBarPartial1(PartialJuiceBarShop):
    index = 9
    items = [FroggieDrink]


class JuiceBarPartial2(PartialJuiceBarShop):
    index = 10
    items = [FroggieDrink, Elixir]


class JuiceBarPartial3(PartialJuiceBarShop):
    index = 11
    items = [FroggieDrink, Elixir, Megalixir]


class JuiceBarFull(JuiceBarShop):
    index = 12
    items = [FroggieDrink, Elixir, Megalixir, KerokeroCola]

    def is_item_allowed(self, item):
        """Check if an item is allowed in this shop given the game world.

        Args:
            item (Item):

        Returns:
            bool: True if item is allowed in this shop/world, False otherwise.

        """
        return item.consumable and not item.reuseable


class SeasideWeaponShop(Shop):
    index = 13
    items = [TroopaShell, Parasol, HurlyGloves, DoublePunch, RibbitStick, NokNokShell, PunchGlove, FingerShot, Cymbals,
             ChompShell, SuperHammer, HandGun, WhompGlove, SlapGlove, LuckyHammer]

    def is_item_allowed(self, item):
        """Check if an item is allowed in this shop given the game world.

        Args:
            item (Item):

        Returns:
            bool: True if item is allowed in this shop/world, False otherwise.

        """
        return item.is_weapon


class SeasideArmorShop(Shop):
    index = 14
    items = [SailorShirt, SailorPants, SailorCape, NauticaDress, Shirt, Pants, ThickShirt, ThickPants, MegaShirt,
             MegaPants, MegaCape, HappyShirt, HappyPants, HappyCape, HappyShell]

    def is_item_allowed(self, item):
        """Check if an item is allowed in this shop given the game world.

        Args:
            item (Item):

        Returns:
            bool: True if item is allowed in this shop/world, False otherwise.

        """
        return item.is_armor


class SeasideAccessoryShop(Shop):
    index = 15
    items = [JumpShoes, AntidotePin, WakeUpPin, FearlessPin, TrueformPin, ZoomShoes]

    def is_item_allowed(self, item):
        """Check if an item is allowed in this shop given the game world.

        Args:
            item (Item):

        Returns:
            bool: True if item is allowed in this shop/world, False otherwise.

        """
        return item.is_accessory


class SeasideItemShop(Shop):
    index = 16
    items = [Mushroom, MidMushroom, HoneySyrup, MapleSyrup, PickMeUp, AbleJuice, FreshenUp]

    def is_item_allowed(self, item):
        """Check if an item is allowed in this shop given the game world.

        Args:
            item (Item):

        Returns:
            bool: True if item is allowed in this shop/world, False otherwise.

        """
        return item.consumable


class MonstroTownShop(Shop):
    index = 17
    items = [SpikedLink, CourageShell, MidMushroom, MapleSyrup, PickMeUp, AbleJuice, FreshenUp]

    def is_item_allowed(self, item):
        return item.consumable or (item.is_armor or item.is_weapon)


class NimbusLandShop(Shop):
    index = 18
    items = [MidMushroom, MapleSyrup, PickMeUp, AbleJuice, FreshenUp]

    def is_item_allowed(self, item):
        """Check if an item is allowed in this shop given the game world.

        Args:
            item (Item):

        Returns:
            bool: True if item is allowed in this shop/world, False otherwise.

        """
        return item.consumable


class HinopioShop(Shop):
    index = 19
    items = [FireShirt, FirePants, FireCape, FireShell, FireDress]

    def is_item_allowed(self, item):
        """Check if an item is allowed in this shop given the game world.

        Args:
            item (Item):

        Returns:
            bool: True if item is allowed in this shop/world, False otherwise.

        """
        return item.is_armor


class BabyGoombaShop(Shop):
    index = 20
    items = [Mushroom2]

    def is_item_allowed(self, item):
        """Check if an item is allowed in this shop given the game world.

        Args:
            item (Item):

        Returns:
            bool: True if item is allowed in this shop/world, False otherwise.

        """
        return item.consumable


class NimbusLandItemWeaponShop(Shop):
    index = 21
    items = [MidMushroom, MapleSyrup, PickMeUp, AbleJuice, FreshenUp, MegaGlove, WarFan, HandCannon, StickyGlove,
             FuzzyShirt, FuzzyPants, FuzzyCape, FuzzyDress]

    def is_item_allowed(self, item):
        return item.consumable or (item.is_armor or item.is_weapon)


class CrocoShop1(Shop):
    index = 22
    items = [MidMushroom, MapleSyrup, PickMeUp, FreshenUp, FireShirt, FirePants, FireCape, FireShell, FireDress]

    def is_item_allowed(self, item):
        return item.consumable or item.is_armor


class CrocoShop2(Shop):
    index = 23
    items = [MidMushroom, MapleSyrup, PickMeUp, FreshenUp, HeroShirt, PrincePants, StarCape, HealShell, RoyalDress]

    def is_item_allowed(self, item):
        return item.consumable or item.is_armor


class ToadShop(Shop):
    index = 24
    items = [MidMushroom, MaxMushroom, MapleSyrup, PickMeUp, AbleJuice, FreshenUp, FroggieDrink]

    def is_item_allowed(self, item):
        """Check if an item is allowed in this shop given the game world.

        Args:
            item (Item):

        Returns:
            bool: True if item is allowed in this shop/world, False otherwise.

        """
        return item.consumable


# ********************* Default shop and item lists for world

def get_default_items(world):
    """Get default vanilla item list for the world.

    Args:
        world (randomizer.logic.main.GameWorld):

    Returns:
        list[Item]: List of default item objects.

    """
    return [
        Hammer(world),
        FroggieStick(world),
        NokNokShell(world),
        PunchGlove(world),
        FingerShot(world),
        Cymbals(world),
        Chomp(world),
        Masher(world),
        ChompShell(world),
        SuperHammer(world),
        HandGun(world),
        WhompGlove(world),
        SlapGlove(world),
        TroopaShell(world),
        Parasol(world),
        HurlyGloves(world),
        DoublePunch(world),
        RibbitStick(world),
        SpikedLink(world),
        MegaGlove(world),
        WarFan(world),
        HandCannon(world),
        StickyGlove(world),
        UltraHammer(world),
        SuperSlap(world),
        DrillClaw(world),
        StarGun(world),
        SonicCymbal(world),
        LazyShellWeapon(world),
        FryingPan(world),
        LuckyHammer(world),
        Shirt(world),
        Pants(world),
        ThickShirt(world),
        ThickPants(world),
        MegaShirt(world),
        MegaPants(world),
        WorkPants(world),
        MegaCape(world),
        HappyShirt(world),
        HappyPants(world),
        HappyCape(world),
        HappyShell(world),
        PolkaDress(world),
        SailorShirt(world),
        SailorPants(world),
        SailorCape(world),
        NauticaDress(world),
        CourageShell(world),
        FuzzyShirt(world),
        FuzzyPants(world),
        FuzzyCape(world),
        FuzzyDress(world),
        FireShirt(world),
        FirePants(world),
        FireCape(world),
        FireShell(world),
        FireDress(world),
        HeroShirt(world),
        PrincePants(world),
        StarCape(world),
        HealShell(world),
        RoyalDress(world),
        SuperSuit(world),
        LazyShellArmor(world),
        ZoomShoes(world),
        SafetyBadge(world),
        JumpShoes(world),
        SafetyRing(world),
        Amulet(world),
        ScroogeRing(world),
        ExpBooster(world),
        AttackScarf(world),
        RareScarf(world),
        BtubRing(world),
        AntidotePin(world),
        WakeUpPin(world),
        FearlessPin(world),
        TrueformPin(world),
        CoinTrick(world),
        GhostMedal(world),
        JinxBelt(world),
        Feather(world),
        TroopaPin(world),
        SignalRing(world),
        QuartzCharm(world),
        Mushroom(world),
        MidMushroom(world),
        MaxMushroom(world),
        HoneySyrup(world),
        MapleSyrup(world),
        RoyalSyrup(world),
        PickMeUp(world),
        AbleJuice(world),
        Bracer(world),
        Energizer(world),
        YoshiAde(world),
        RedEssence(world),
        KerokeroCola(world),
        YoshiCookie(world),
        PureWater(world),
        SleepyBomb(world),
        BadMushroom(world),
        FireBomb(world),
        IceBomb(world),
        FlowerTab(world),
        FlowerJar(world),
        FlowerBox(world),
        YoshiCandy(world),
        FroggieDrink(world),
        MukuCookie(world),
        Elixir(world),
        Megalixir(world),
        SeeYa(world),
        TempleKey(world),
        GoodieBag(world),
        EarlierTimes(world),
        FreshenUp(world),
        RareFrogCoin(world),
        Wallet(world),
        CricketPie(world),
        RockCandy(world),
        CastleKey1(world),
        CastleKey2(world),
        BambinoBomb(world),
        SheepAttack(world),
        CarboCookie(world),
        ShinyStone(world),
        RoomKey(world),
        ElderKey(world),
        ShedKey(world),
        LambsLure(world),
        FrightBomb(world),
        MysteryEgg(world),
        BeetleBox(world),
        BeetleBox2(world),
        LuckyJewel(world),
        SopranoCard(world),
        AltoCard(world),
        TenorCard(world),
        Crystalline(world),
        PowerBlast(world),
        WiltShroom(world),
        RottenMush(world),
        MoldyMush(world),
        Seed(world),
        Fertilizer(world),
        BigBooFlag(world),
        DryBonesFlag(world),
        GreaperFlag(world),
        CricketJam(world),
        BrightCard(world),
        Mushroom2(world),
        StarEgg(world),
    ]


def get_default_shops(world):
    """

    Args:
        world (randomizer.logic.main.GameWorld):

    Returns:
        list[Shop]: Default list of items.

    """
    return [
        MushroomKingdomShop(world),
        RoseTownItemShop(world),
        RoseTownArmorShop(world),
        DiscipleShop(world),
        MolevilleShop(world),
        MarrymoreShop(world),
        FrogCoinEmporiumShop(world),
        SeaShop(world),
        SeasideYaridShop(world),
        JuiceBarPartial1(world),
        JuiceBarPartial2(world),
        JuiceBarPartial3(world),
        JuiceBarFull(world),
        SeasideWeaponShop(world),
        SeasideArmorShop(world),
        SeasideAccessoryShop(world),
        SeasideItemShop(world),
        MonstroTownShop(world),
        NimbusLandShop(world),
        HinopioShop(world),
        BabyGoombaShop(world),
        NimbusLandItemWeaponShop(world),
        CrocoShop1(world),
        CrocoShop2(world),
        ToadShop(world),
    ]
