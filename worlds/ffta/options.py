"""
Option definitions for Final Fantasy Tactics Advance
"""
from typing import Dict, Iterable, Any, Union
from dataclasses import dataclass
from Options import (Choice, DefaultOnToggle, Option, OptionSet, Range, Toggle, FreeText, DeathLink, PerGameCommonOptions,
                     NamedRange, OptionList, TextChoice)
from copy import deepcopy
from .items import itemGroups, ShopItem
from Utils import is_iterable_except_str, get_fuzzy_results
from functools import singledispatchmethod


class OptionListSet(OptionSet):
    # A list of sets

    special_names: Dict[str, Iterable[Iterable[str]]] = {}
    default = ()
    supports_weighting = False

    def __init__(self, value: Iterable[Iterable[str]]):
        self.value = list([set(deepcopy(x)) for x in value])
        super(OptionSet, self).__init__()

    def get_option_name(self, value):
        return str(value)

    @classmethod
    def from_text(cls, text: str):
        text = text.lower()
        if text in cls.special_names:
            return cls(cls.special_names[text])
        else:
            raise ValueError(f"Invalid value {text}")

    def verify_keys(self) -> None:
        for x in self.value:
            super(OptionListSet, self).verify_keys(x)

    def verify(self, world, player_name, plando_options) -> None:
        outerArray = self.value
        for innerSet in outerArray:
            self.value = innerSet
            super(OptionListSet, self).verify(world, player_name, plando_options)
        self.value = outerArray


class OptionListList(OptionList):
    # Supports duplicate entries and ordering.
    # If only unique entries are needed and input order of elements does not matter, OptionListSet should be used instead.
    # Not a docstring so it doesn't get grabbed by the options system.

    special_names: Dict[str, Iterable[Any]] = {}
    default = ()
    supports_weighting = False

    def __init__(self, value: Iterable[Any]):
        self.value = list([list(deepcopy(x)) for x in value])
        super(OptionList, self).__init__()

    def get_option_name(self, value):
        return str(value)

    @classmethod
    def from_text(cls, text: str):
        text = text.lower()
        if text in cls.special_names:
            return cls(cls.special_names[text])
        else:
            raise ValueError(f"Invalid value {text}")

    def verify_keys(self) -> None:
        for x in self.value:
            super(OptionListList, self).verify_keys(x)

    def verify(self, world, player_name, plando_options) -> None:
        outerArray = self.value
        for innerSet in outerArray:
            self.value = innerSet
            super(OptionListList, self).verify(world, player_name, plando_options)
        self.value = outerArray


class OptionShopItems(OptionListList):
    verify_item_name = True
    convert_name_groups = True

    def verify_keys(self) -> None:
        for inner in self.value:
            inner_names = []
            for x in inner:
                inner_names.append(x[0] if isinstance(x, Iterable) else x)
            super(OptionListList, self).verify_keys(inner_names)

    @classmethod
    def from_any(cls, data: Any):
        if is_iterable_except_str(data):
            data = cls.from_iterable(data)
            return cls(data)
        return cls.from_text(str(data))

    @classmethod
    def from_iterable(cls, data: Iterable) -> Iterable[Iterable[Union[str, ShopItem]]]:
        new_data = []
        for outer in data:
            new_inner = []
            for inner in outer:
                if is_iterable_except_str(inner):
                    if len(inner) == 2:
                        new_inner.append((inner[0], inner[1]))
                    else:
                        new_inner.append((inner[0], "default"))
                elif isinstance(inner, str):
                    new_inner.append(inner)
                else:
                    raise TypeError(inner)
            new_data.append(new_inner)
        return new_data

    def verify(self, world, player_name, plando_options) -> None:
        for i, inner in enumerate(self.value):
            if self.convert_name_groups and self.verify_item_name:
                new_value = []  # empty container of whatever value is
                for item in inner:
                    if isinstance(item, str):
                        new_value += [(item, "default")]
                    else:
                        new_value += [item]
                self.value[i] = new_value
        for inner in self.value:
            if self.verify_item_name:
                for index, item in enumerate(inner):
                    item_name = item[0]
                    self.verify_item_value(item)

                    if item_name in ["random"]:
                        continue
                    elif item_name.startswith("random-"):
                        parsed_item = self.parse_random_item_name(item)
                        inner[index] = parsed_item
                        continue

                    if item_name not in world.item_names and item_name not in itemGroups:
                        picks = get_fuzzy_results(item_name, world.item_names, limit=1)
                        if picks[0][1] == 100:
                            print(f"Replacing '{item_name}' with '{picks[0][0]}' ({picks[0][1]}% sure)")
                            inner[index] = (picks[0][0],) + item[1:]
                        else:
                            raise Exception(f"Item {item_name} from option {self} "
                                            f"is not a valid item name from {world.game}. "
                                            f"Did you mean '{picks[0][0]}' ({picks[0][1]}% sure)")

    def verify_item_value(self, item):
        item_name = item[0]
        item_value = item[1]
        if not isinstance(item_value, int):
            if isinstance(item_value, str) \
                    and item_value not in ["default", "random", "random-low", "random-high", "random-middle"]:
                if item_value.startswith("random-range-"):
                    textsplit = item_value.split("-")
                    try:
                        [int(textsplit[len(textsplit) - 2]), int(textsplit[len(textsplit) - 1])]
                    except ValueError:
                        raise ValueError(f"Invalid random range {item_value} for Item {item_name} in option {self}")
                else:
                    raise ValueError(f"'{item_value}' is not a valid value for Item {item_name} in option {self}")
            elif not isinstance(item_value, str):
                raise TypeError(f"'{item_value}' is not a valid type for Item {item_name} in option {self}")
        elif item_value < 1 or item_value > 0xFFFF:
            raise ValueError(f"Value {item_value} must be in range 1-65535 for Item {item_name} in option {self}")

    def parse_random_item_name(self, item):
        item_name = item[0]
        textsplit = item_name.split("-")
        random_groups = []
        random_range = []
        for arg in textsplit[1:]:
            if arg in itemGroups:
                random_groups.append(arg)
            if arg not in itemGroups:
                picks = get_fuzzy_results(arg, itemGroups, limit=1)
                if picks[0][1] == 100:
                    print(f"Replacing '{arg}' with '{picks[0][0]}' ({picks[0][1]}% sure)")
                    random_groups.append(picks[0][0])
                else:
                    try:
                        asInt = int(arg)
                    except ValueError:
                        raise ValueError(f"Invalid item group '{arg}' for {item_name} in option {self}, "
                                         f"did you mean '{picks[0][0]}' ({picks[0][1]}% sure)")
                    random_range.append(asInt)
        if len(random_range) > 2:
            raise ValueError(f"Invalid random range {random_range} for Item {item_name} in option {self}")
        parsed_name = f"random-{'-'.join(str(x) for x in (random_groups + random_range))}"
        return (parsed_name,) + item[1:]


class FixedIntervalRange(Range):
    interval = 1

    def __init__(self, value: int):
        # Round down to nearest interval, taking into account range_start.
        # Example values if range_start=50 and interval=200:
        # 50, 250, 450, etc.
        value -= (value - self.range_start) % self.interval
        super().__init__(value)


class FixedIntervalNamedRange(NamedRange):
    interval = 1

    @singledispatchmethod
    def __init__(self, value):
        raise NotImplementedError

    @__init__.register
    def _(self, value: str):
        self.value = value

    @__init__.register
    def _(self, value: int):
        # Round down to nearest interval, taking into account range_start.
        # Example values if range_start=50 and interval=200:
        # 50, 250, 450, etc.
        if value not in self.special_range_names.values():
            value -= (value - self.range_start) % self.interval
        super().__init__(value)


class Goal(Choice):
    """
    Sets the unlock condition for the final mission

    All mission gates: The final mission is unlocked after going through every mission gate.
    Totema Gauntlet: A series of the five Totema battles must be cleared to unlock the final mission. These are
    unlocked alongside the mission gates. An additional five items are added to unlock them.
    """
    display_name = "Goal"
    default = 0
    option_mission_gates = 0
    option_totema = 1


class StartingUnits(Choice):
    """
    Sets the option for your starting units

    Vanilla: The same starting units as the original game
    Shuffle: Jobs are randomized within the original starting races of the game.
    Random: Jobs and race of the starting units are randomized
    Balanced: Ensures two attacker jobs, two magic jobs, and two support jobs. Excludes morphers, beastmasters, and gadgeteers.
    Random Monster: Starting units jobs and race are randomized with monster units also in the pool

    Note: Monsters are unable to change jobs, equip anything or use items.
    """
    display_name = "Starting units"
    default = 0
    option_starting_vanilla = 0
    option_starting_shuffle = 1
    option_starting_random = 2
    option_starting_balanced = 3
    option_random_monster = 4


class StartingSpecialChance(Range):
    """
    Percent chance of any unit besides Marche and Montblanc to be a special unit such as Ritz or Cid.
    1 = 10% and 10 = 100% chance that all units are a special unit
    """
    display_name = "Percent chance of starting special units"
    default = 0
    range_start = 0
    range_end = 10

class StartingUnitEquip(Choice):
    """
    Sets the equipment option for your starting units

    Basic: Units will always start with their most basic equipment
    Randomized: The equipment load out will be random within the job's equipment
    """
    display_name = "Starting unit equipment"
    default = 0
    option_equip_basic = 0
    option_equip_random = 1


class StartingAbilitiesMastered(Range):
    """
    Sets the amount of mastered abilities for each starting unit's job. Based on percentage. 1 = 10% and 10 = 100% of abilities mastered
    """
    display_name = "Percent of starting abilities mastered"
    default = 0
    range_start = 0
    range_end = 10


class AbilityAP(Range):
    """
    Sets a standardized amount of AP needed for job abilities. Set to 0 to have every ability already learned.
    This also applies to recruits, enemy units etc. Every number goes up by 10, for example 1 = 10 and 64 = 999.
    Use 65 for vanilla AP values
    """
    display_name = "Ability AP"
    default = 65
    range_start = 0
    range_end = 65


class AbilityRandom(Choice):
    """
    Randomize the abilities each job can use.
    WARNING: Currently certain combinations may result in softlocks.

    Vanilla: Jobs have their original abilities
    Random within race: Abilities are randomized between jobs in the same race. No duplicate abilities within jobs
    Random: Abilities are randomized throughout all jobs. Jobs may contain duplicate abilities.
    Random with monster and special unit abilities: Abilities are randomized throughout all jobs and most duplicates
    are replaced with abilities from monsters, special units, and Totema.

    """
    display_name = "Ability Randomization"
    default = 0
    option_vanilla = 0
    option_race = 1
    option_randomized = 2
    option_random_with_special = 3


class StatGrowth(Choice):
    """
    Stat growth options for all the jobs

    Vanilla: Stat growth will be the same as vanilla
    Average: Stat growth will be average across all stats in every job

    """
    display_name = "Ability Randomization"
    default = 0
    option_vanilla = 0
    option_average = 1


class JobUnlockReq(Choice):
    """
    Sets the unlock requirements for every unit's job

    Vanilla: Job unlock requirements are the same as vanilla
    All Unlocked: All jobs are unlocked from the start
    All Locked: All jobs are locked. The unit must use their assigned job and cannot change
    """
    display_name = "Job Unlock Requirements"
    default = 0
    option_req_vanilla = 0
    option_all_unlocked = 1
    option_all_locked = 2
    #option_job_items = 3


class Laws(Choice):
    """
    Enable or disable the law and judge system found in the game. JP will rarely be awarded with laws turned off.

    No Laws: Judges and laws are disabled.
    Laws: Laws are vanilla but are enabled.
    Random laws: Laws are enabled and are randomized among law sets.
    """
    display_name = "Enables or disables laws/judges."
    default = 1
    option_disable_laws = 0
    option_enable_laws = 1
    option_random_laws = 2


class LawCards(Choice):
    """
    Add Law cards to the pool.
    Optionally also unlock law cards and the law card shop from the start.
    (Using cards and trading with the card shop are normally unlocked after the Antilaws mission.)

    Disabled: No law cards in the pool.
    Enabled: Law cards are added to the pool.
    Unlock Cards: As Enabled and law cards are usable from the start.
    Unlock Cards and Shop: As Unlock Cards and the law card shop is unlocked from the start.
    """
    display_name = "Add law cards to the item pool."
    default = 0
    option_disabled = 0
    option_enabled = 1
    option_unlock_cards = 2
    option_unlock_cards_and_shop = 3


class RandomEnemies(Choice):
    """
    Randomizes the enemy units. Special units such as bosses currently are not randomized.

    Vanilla: Enemies aren't changed
    Randomized: Enemies are randomized
    """
    display_name = "Randomize Enemies"
    default = 0
    option_enemy_vanilla = 0
    option_enemy_random = 1


class EnemyScaling(Choice):
    """
    Sets the level scaling for enemies.

    Average Level: Enemies are scaled to the average level of your units.
    Highest Level: Enemies are scaled to your highest level unit.
    """
    display_name = "Enemy Level Scaling"
    default = 0
    option_average_level = 0
    option_highest_level = 1


class ExpMultiplier(Choice):
    """
    Multiplies all exp gained.
    """
    display_name = "Double EXP"
    default = 0
    option_one = 0
    option_two = 1
    option_four = 2
    option_eight = 3
    option_sixteen = 4


class StartingGil(Range):
    """
    Sets the amount of gil you will start with.
    """
    display_name = "Starting gil"
    default = 5000
    range_start = 0
    range_end = 99999999


class GilRewards(FixedIntervalNamedRange):
    """
    Sets the amount of gil you get for completing a mission.
    Must be a multiple of 200. Will be rounded down to the nearest 200 if not.
    individually-randomized(-low/-middle/-high): Sets a random value for each mission (with optional bias)
    """
    display_name = "Gil mission rewards"
    interval = 200
    default = 1000
    range_start = 0
    range_end = 51000  # 1-byte value so max is 255 * 200
    special_range_names = {
        "individually-randomized": "individually-randomized",
        "individually-randomized-low": "individually-randomized-low",
        "individually-randomized-middle": "individually-randomized-middle",
        "individually-randomized-high": "individually-randomized-high",
        }


class GateNumber(Range):
    """
    Sets the number of mission gates. Each gate contains four missions each. Expect an hour or more added for every gate.
    Royal Valley or Decision Time will always be the last mission depending on options.

    Amount of locations per gate depends on number of item rewards and dispatch missions added
    """
    display_name = "Number of mission gates"
    default = 6
    range_start = 1
    range_end = 27


class GatePaths(Range):
    """
    Sets the number of branching mission gates paths. Each must currently still
    be progressed through to unlock the final mission.
    Useful for higher mission gate counts.
    """
    display_name = "Mission gate paths"
    default = 1
    range_start = 1
    range_end = 3


class DispatchMissions(Range):
    """
    Sets the number of dispatch missions per gate. Each dispatch mission adds two locations for each gate.
    """
    display_name = "Number of dispatch missions"
    default = 0
    range_start = 0
    range_end = 6


class DispatchRandom(Toggle):
    """
    Randomizes the order of the dispatch mission. Setting only has effect is dispatch missions setting is more than 0.
    """
    display_name = "Randomize dispatch missions"
    default = 0


class GateUnlock(Choice):
    """
    Sets how the mission gates are unlocked
    One Mission item: Mission gates are unlocked by one mission item. Gate unlocks both encounter and dispatch missions.
    Two Mission items: Mission gates are unlocked by two mission items. Gate unlocks both encounter and dispatch missions.
    Dispatch mission gate: Dispatch missions are separated into their own gate sequence which each require an item.
    Dispatch missions must be more than 0 for this setting or it will be ignored

    (Adds 1 or 2 progression items to the pool for each gate depending on the setting)
    """
    display_name = "Number of required gate unlock items"
    default = 0
    option_one = 0
    option_two = 1
    option_dispatch_gate = 2


class MissionOrder(Choice):
    """
    Sets the option for the order of missions

    Linear: Missions are in order, with the first 26 being story.
    Story as gate unlocks: The story missions in linear order will be the gate unlock mission for the first 23 gates. Every other mission is random.
    Randomized: Missions are completely randomized

    """
    display_name = "Mission order"
    default = 0
    option_linear = 0
    option_story_gate = 1
    option_randomized = 2


class FinalMission(Choice):
    """
    Sets what the final mission will be between the two missions that play the credits.
    Royal Valley: The final mission will be Royal Valley. This mission is three phases. Original final mission.
    Decision Time: The final mission will be Decision Time. This mission is one phase.
    """

    display_name = "Final mission"
    default = 0
    option_royal_valley = 0
    option_decision_time = 1


class QuickOptions(Toggle):
    """
    Enables quick options by default which turn off attack names, exp popups, and turns on
    fast text and fast cursor. All of these can be tweaked in the game options.
    """
    display_name = "Turn on quick options by default"
    default = 0


class FastReceive(Toggle):
    """
    Skip most of the animations and text when receiving items
    """
    display_name = "Faster received item popup"
    default = 1


class ForceRecruitment(Choice):
    """
    Forces every mission to give a new recruit.
    Disabled: Recruit chances are vanilla
    Enabled: Every mission will give a new recruit, special recruit missions such as Mortal Snow will still
    give their vanilla unit which is Ritz in this example.
    Enabled Secret: Every mission will give a new recruit, special recruit missions will be random and there is a
    chance to receive a special unit such as Ritz, Babus and Cid from any mission.
    Enabled Monster: Every mission will give a new recruit and there is a chance to receive a monster unit.
    """
    display_name = "Force recruitment"
    default = 0
    option_disabled = 0
    option_enabled = 1
    option_enabled_secret = 2
    option_enabled_monster = 3


class MissionRewards(Range):
    """
    Sets the number of rewards received from each mission. Must be between 2 and 6.
    """
    display_name = "Number of rewards per mission"
    default = 2
    range_start = 2
    range_end = 6


class ProgressiveGateItems(Toggle):
    """
    Always receive gate items in order.
    If multiple gate paths are enabled each path will have a separate progressive item.
    Enabled: Gate items are always received in order for each path.
    """
    display_name = "Always receive gate items in order"
    default = 1


class ProgressiveItemNumber(Range):
    """
    Sets how many additional progressive items are added to the pool.
    If multiple gate paths are enabled this amount is added for each path.
    0: There is exactly the amount of progressive items in the pool that is needed to reach the goal.
    1 to 10: This amount of extra progressive items is added to the pool.
    """
    display_name = "Number of additional progressive items"
    default = 3
    range_start = 0
    range_end = 10


class ProgressiveExcessItems(NamedRange):
    """
    Sets what progressive items past the ones needed to reach the goal are replaced with.
    Nothing (or 0): Excess progressive items don't give anything.
    Random Equipment: Excess progressive items give a random non-consumable item.
    Number between 1 and 375: Excess progressive items give the item with the corresponding id.
    """
    display_name = "Choose what excess progressive items turn into"
    default = 0
    range_start = 0
    range_end = 0x177
    special_range_names = {
        "nothing": 0,
        "random_equipment": 0x300
        }


class ProgressiveShopUpgrades(Toggle):
    """
    Adds shop upgrades to the item pool
    """
    display_name = "Add shop upgrades to the item pool"
    default = 0


class ProgressiveShopBattleUnlock(Choice):
    """
    Enables unlocking 2 shop upgrades by fighting 10 and 20 battles total.
    Enabled: This progress does not stack with other upgrades. 10 battles + 1 upgrade = 1 upgrade total.
    Stacking: This progress stacks with other upgrades. 10 battles + 1 upgrade = 2 upgrades total.
    Replacing: As stacking but also removes 2 shop upgrades from the pool.
        Fighting 20 battles and finding all shop upgrades will be required to unlock the highest shop tier.
    """
    display_name = "Unlock up to 2 shop upgrades by fighting battles"
    default = 2
    option_disabled = 0
    option_enabled = 1
    option_stacking = 2
    option_replacing = 3


class ProgressiveShopTiers(OptionShopItems):
    """
    Sets how many shop upgrades there are and what items they unlock.
    If an item's price is changed its sell value is set to half its price (like most items in vanilla).

    named options:
    four_tiers: 3 shop upgrades. Starting items and first two upgrades are vanilla.
        The items normally unlocked by freeing some number of turfs are all in tier 3.
    four_tiers_random: four_tiers but with random prices
    five_tiers: 4 shop upgrades. Starting items and first two upgrades are vanilla.
        The items normally unlocked by freeing some number of turfs are split between tier 3 and 4.
    five_tiers_random: five_tiers but with random prices
    vanilla: 13 shop upgrades. Starting items and first two upgrades are vanilla.
        The rest have 1 item each, unlocked in the same order as freeing turfs.
    vanilla_random: vanilla but with random prices
    default: Same as five_tiers.

    Custom option syntax:
    [[<Tier>], [<Tier>], [<Tier>], ...]

    <Tier> syntax:
    [<Item>, <Item>, <Item>, ...]

    <Item> syntax:
    [<Name>, <Price>] or <Name>

    <Price> may be a number between 1-65535, "default", "random", "random-high",
    "random-middle", "random-low", "random-range-low-<min>-<max>", "random-range-middle-<min>-<max>",
    "random-range-high-<min>-<max>", or "random-range-<min>-<max>".

    <Name> may be the name of any equipment or consumable item, an <ItemGroup>, or a <Random> value.
    If only <Name> is specified, <Price> will be "default".

    <Random> may be: "random-<Groups>", "random-<Groups>-<number>", or "random-<Groups>-<min>-<max>".

    <Groups> syntax:
    <ItemGroup>-<ItemGroup>-<ItemGroup> ...

    <ItemGroup> may be: "vanillashoptier0", "vanillashoptier1", "vanillashoptier2", "all", "weapons", "otherequipment",
    "swords", "blades", "sabers", "knightswords", "greatswords", "broadswords", "knives", "rapiers", "katanas",
    "staves", "rods", "maces", "bows", "greatbows", "spears", "instruments", "knuckles", "souls", "guns", "shields",
    "helmets", "gloves", "hats", "armor", "rings", "clothing", "robes", "shoes", "consumables"

    If the same item appears more than once, only the first processed entry takes effect.
    Entries are processed in 3 steps. Each step starts from the lowest tier:
        1. Directly named items.
        2. Items that are added as part of a group
        3. Random items. (Will never pick an item already added in previous steps)

    Example:
    [
        [
            ["vanillashoptier0", "random-range-low-100-10000"],
            ["Elixir", "random-high"],
            ["Potion", "default"],
        ],
        [
            ["vanillashoptier1", "default"],
            ["random-otherequipment-20", "random-range-200-20000"],
            ["random-weapons-10-20", "random-range-500-50000"],
        ],
        [
            "vanillashoptier2",
            ["random-katanas-knightswords-staves-6-12", "random-range-5000-50000"],
        ]
    ]
    Before upgrades the shop will have:
        Vanilla items at random prices between 100 and 10000, biased towards 100.
        Elixirs at a random price between 1 and 65535, biased towards high numbers.
        Potions at default price (higher priority than the potion in vanillashoptier0).
    The first upgrade will add:
        Vanilla items unlocked at 10 battles.
        20 non-weapon equipment at random prices between 200 and 20000.
        A random amount between 10 and 20 of random weapons at random prices between 500 and 50000.
    The second upgrade will add:
        Vanilla items unlocked at 20 battles.
        A random amount between 6 and 12 of random katanas, knightswords,
        and staffs at random prices between 500 and 50000.

    """
    display_name = "Sets how many shop upgrades there are and what items they unlock"
    four_tiers = [
        [["vanillashoptier0", "default"]],
        [["vanillashoptier1", "default"]],
        [["vanillashoptier2", "default"]],
        [
            ["Cureall", "default"],
            ["Star Armlet", "default"],
            ["Bracers", "default"],
            ["Hunt Bow", "default"],
            ["Estreledge", "default"],
            ["Temple Cloth", "default"],
            ["Masamune", "default"],
            ["Princess Rod", "default"],
            ["Tiptaptwo", "default"],
            ["Seventh Heaven", "default"],
            ["Elixir", "default"]
            ]
    ]
    four_tiers_random = [
        [["vanillashoptier0", "random"]],
        [["vanillashoptier1", "random"]],
        [["vanillashoptier2", "random"]],
        [
            ["Cureall", "random"],
            ["Star Armlet", "random"],
            ["Bracers", "random"],
            ["Hunt Bow", "random"],
            ["Estreledge", "random"],
            ["Temple Cloth", "random"],
            ["Masamune", "random"],
            ["Princess Rod", "random"],
            ["Tiptaptwo", "random"],
            ["Seventh Heaven", "random"],
            ["Elixir", "random"]
            ]
    ]

    five_tiers = [
        [["vanillashoptier0", "default"]],
        [["vanillashoptier1", "default"]],
        [["vanillashoptier2", "default"]],
        [
            ["Cureall", "default"],
            ["Star Armlet", "default"],
            ["Bracers", "default"],
            ["Hunt Bow", "default"],
            ["Estreledge", "default"]
            ],
        [
            ["Temple Cloth", "default"],
            ["Masamune", "default"],
            ["Princess Rod", "default"],
            ["Tiptaptwo", "default"],
            ["Seventh Heaven", "default"],
            ["Elixir", "default"]
            ]
    ]
    five_tiers_random = [
        [["vanillashoptier0", "random"]],
        [["vanillashoptier1", "random"]],
        [["vanillashoptier2", "random"]],
        [
            ["Cureall", "random"],
            ["Star Armlet", "random"],
            ["Bracers", "random"],
            ["Hunt Bow", "random"],
            ["Estreledge", "random"]
            ],
        [
            ["Temple Cloth", "random"],
            ["Masamune", "random"],
            ["Princess Rod", "random"],
            ["Tiptaptwo", "random"],
            ["Seventh Heaven", "random"],
            ["Elixir", "random"]
            ]
    ]

    vanilla = [
        [["vanillashoptier0", "default"]],
        [["vanillashoptier1", "default"]],
        [["vanillashoptier2", "default"]],
        [["Cureall", "default"]],
        [["Star Armlet", "default"]],
        [["Bracers", "default"]],
        [["Hunt Bow", "default"]],
        [["Estreledge", "default"]],
        [["Temple Cloth", "default"]],
        [["Masamune", "default"]],
        [["Princess Rod", "default"]],
        [["Tiptaptwo", "default"]],
        [["Seventh Heaven", "default"]],
        [["Elixir", "default"]]
    ]
    vanilla_random = [
        [["vanillashoptier0", "random"]],
        [["vanillashoptier1", "random"]],
        [["vanillashoptier2", "random"]],
        [["Cureall", "random"]],
        [["Star Armlet", "random"]],
        [["Bracers", "random"]],
        [["Hunt Bow", "random"]],
        [["Estreledge", "random"]],
        [["Temple Cloth", "random"]],
        [["Masamune", "random"]],
        [["Princess Rod", "random"]],
        [["Tiptaptwo", "random"]],
        [["Seventh Heaven", "random"]],
        [["Elixir", "random"]]
    ]
    default = five_tiers
    special_names = {
        "default": default,
        "four_tiers": four_tiers,
        "four_tiers_random": four_tiers_random,
        "five_tiers": five_tiers,
        "five_tiers_random": five_tiers_random,
        "vanilla": vanilla,
        "vanilla_random": vanilla_random
    }


class UnitNames(Toggle):
    """
    Random unit names are named after players in the multiworld.
    """
    display_name = "Random units named after other players"
    default = 1


@dataclass
class FFTAOptions(PerGameCommonOptions):
    #"death_link": DeathLink,
    goal: Goal
    starting_units: StartingUnits
    starting_unit_equip: StartingUnitEquip
    starting_special_chance: StartingSpecialChance
    starting_abilities: StartingAbilitiesMastered
    ability_ap: AbilityAP
    randomize_abilities: AbilityRandom
    stat_growth: StatGrowth
    job_unlock_req: JobUnlockReq
    laws: Laws
    law_cards: LawCards
    randomize_enemies: RandomEnemies
    scaling: EnemyScaling
    exp_multiplier: ExpMultiplier
    starting_gil: StartingGil
    gil_rewards: GilRewards
    gate_num: GateNumber
    gate_paths: GatePaths
    dispatch: DispatchMissions
    randomize_dispatch: DispatchRandom
    gate_items: GateUnlock
    mission_order: MissionOrder
    final_mission: FinalMission
    quick_options: QuickOptions
    fast_receive: FastReceive
    force_recruitment: ForceRecruitment
    mission_reward_num: MissionRewards
    progressive_gates: ProgressiveGateItems
    progressive_item_num: ProgressiveItemNumber
    progressive_excess: ProgressiveExcessItems
    progressive_shop: ProgressiveShopUpgrades
    progressive_shop_battle_unlock: ProgressiveShopBattleUnlock
    progressive_shop_tiers: ProgressiveShopTiers
    unit_names: UnitNames
