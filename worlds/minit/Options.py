from dataclasses import dataclass
from typing import ClassVar
from Options import (
    Toggle,
    Choice,
    PerGameCommonOptions,
    DeathLink,
    Range,
    StartInventoryPool,
    )


class EarlySword(Toggle):
    """
    Start With a Sword in vanilla Sword Location.
    or with Entrance Rando on puts one accessible from spawn
    """
    display_name = "Early Sword"


class Darkrooms(Choice):
    """
    Puts Darkroom navigation without FlashLight in logic.
    off: makes any darkness out of logic without flashlight
    minor: only regions where the majority of travel is lit are in logic
    on: common darkrooms that require precise movement or specific map knowledge will be in logic
    insane: darkness will never be considered out of logic
    """
    display_name = "Darkrooms"
    option_off = 0
    option_minor = 1
    option_on = 2
    option_insane = 3
    default = 1


class Obscure(Toggle):
    """Adds Obscure logic like using only swim to access Island Shack."""
    display_name = "Obscure"


class DeathLinkAmnesty(Range):
    """Amount of deaths before a deathlink is sent."""
    range_start = 0
    range_end = 20
    default = 10


class ProgressiveSword(Choice):
    """
    Sets the Broken, Basic, and Mega swords to be Progressive Items.
    If set to reverse they will increment from Mega to Basic to Broken,
    expected to be used with Toilet Goal.
    """
    display_name = "ProgressiveSword"
    option_forward_progressive = 0
    option_reverse_progressive = 1
    option_off = 2
    default = 2
    sword_item_name_lookup: ClassVar[dict[int, str]] = {
        0: "Progressive Sword",
        1: "Reverse Progressive Sword",
        2: "ItemSword"
    }

    def get_sword_item_name(self) -> str:
        return self.sword_item_name_lookup[self.value]


class Goal(Choice):
    """
    Forces the player to win via a specific Goal condition.
    Boss is use the Mega Sword to destroy the factory machine
    and beat the boss. Toilet is to aquire the Broken Sword
    and drop it into the Factory toilet.
    """
    display_name = "Goal"
    option_boss_fight = 0
    option_toilet_goal = 1
    option_any_goal = 2
    default = 0

    def parse_goals(self) -> list[str]:
        if self == "boss_fight":
            return ["boss"]
        elif self == "toilet_goal":
            return ["toilet"]
        elif self == "any_goal":
            return ["toilet", "boss"]


class EntranceRando(Choice):
    """Choose if the room entrances are randomized as well."""
    display_name = "EntranceRando"
    option_off = 0
    option_on = 1
    default = 0


class MinHP(Toggle):
    """
    If on replaces all Health Pieces with bonus coins,
    keeping the player at 2 HP
    """
    display_name = "MinHP"


class DamageBoosts(Toggle):
    """
    Enables high damage routes through poisoned water
    note: this does not exclude taking one damage
    to cross the rivers before factory and camera house
    Multi-hit damages boosts are not currently in ER
    """
    display_name = "DamageBoosts"


@dataclass
class MinitGameOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    starting_sword: EarlySword
    darkrooms: Darkrooms
    obscure: Obscure
    progressive_sword: ProgressiveSword
    chosen_goal: Goal
    death_link: DeathLink
    death_amnisty_total: DeathLinkAmnesty
    er_option: EntranceRando
    min_hp: MinHP
    damage_boosts: DamageBoosts


# add options
# TODO - add puzzleless to de-prio longer/confusing puzzles
# TODO - add random start locations
