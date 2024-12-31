from Options import Choice, Toggle, DefaultOnToggle, Range, OptionList, DeathLink, PlandoConnections, \
    PerGameCommonOptions
from .Constants import region_info
from dataclasses import dataclass


class AdvancementGoal(Range):
    """Number of advancements required to spawn bosses."""
    display_name = "Advancement Goal"
    range_start = 0
    range_end = 114
    default = 40


class EggShardsRequired(Range):
    """Number of dragon egg shards to collect to spawn bosses."""
    display_name = "Egg Shards Required"
    range_start = 0
    range_end = 50
    default = 0


class EggShardsAvailable(Range):
    """Number of dragon egg shards available to collect."""
    display_name = "Egg Shards Available"
    range_start = 0
    range_end = 50
    default = 0


class BossGoal(Choice):
    """Bosses which must be defeated to finish the game."""
    display_name = "Required Bosses"
    option_none = 0
    option_ender_dragon = 1
    option_wither = 2
    option_both = 3
    default = 1

    @property
    def dragon(self):
        return self.value % 2 == 1

    @property
    def wither(self):
        return self.value > 1


class ShuffleStructures(DefaultOnToggle):
    """Enables shuffling of villages, outposts, fortresses, bastions, and end cities."""
    display_name = "Shuffle Structures"


class StructureCompasses(DefaultOnToggle):
    """Adds structure compasses to the item pool, which point to the nearest indicated structure."""
    display_name = "Structure Compasses"


class BeeTraps(Range):
    """Replaces a percentage of junk items with bee traps, which spawn multiple angered bees around every player when
    received."""
    display_name = "Bee Trap Percentage"
    range_start = 0
    range_end = 100
    default = 0


class CombatDifficulty(Choice):
    """Modifies the level of items logically required for exploring dangerous areas and fighting bosses."""
    display_name = "Combat Difficulty"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    default = 1


class HardAdvancements(Toggle):
    """Enables certain RNG-reliant or tedious advancements."""
    display_name = "Include Hard Advancements"


class UnreasonableAdvancements(Toggle):
    """Enables the extremely difficult advancements "How Did We Get Here?" and "Adventuring Time.\""""
    display_name = "Include Unreasonable Advancements"


class PostgameAdvancements(Toggle):
    """Enables advancements that require spawning and defeating the required bosses."""
    display_name = "Include Postgame Advancements"


class SendDefeatedMobs(Toggle):
    """Send killed mobs to other Minecraft worlds which have this option enabled."""
    display_name = "Send Defeated Mobs"


class StartingItems(OptionList):
    """Start with these items. Each entry should be of this format: {item: "item_name", amount: #}
    `item` can include components, and should be in an identical format to a `/give` command with
    `"` escaped for json reasons.

    `amount` is optional and will default to 1 if omitted.

    example:
    ```
    starting_items: [
        { "item": "minecraft:stick[minecraft:custom_name=\"{'text':'pointy stick'}\"]" },
        { "item": "minecraft:arrow[minecraft:rarity=epic]", amount: 64 }
    ]
    ```
    """
    display_name = "Starting Items"


class MCPlandoConnections(PlandoConnections):
    entrances = set(connection[0] for connection in region_info["default_connections"])
    exits = set(connection[1] for connection in region_info["default_connections"])

    @classmethod
    def can_connect(cls, entrance, exit):
        if exit in region_info["illegal_connections"] and entrance in region_info["illegal_connections"][exit]:
            return False
        return True


@dataclass
class MinecraftOptions(PerGameCommonOptions):
    plando_connections: MCPlandoConnections
    advancement_goal: AdvancementGoal
    egg_shards_required: EggShardsRequired
    egg_shards_available: EggShardsAvailable
    required_bosses: BossGoal
    shuffle_structures: ShuffleStructures
    structure_compasses: StructureCompasses

    combat_difficulty: CombatDifficulty
    include_hard_advancements: HardAdvancements
    include_unreasonable_advancements: UnreasonableAdvancements
    include_postgame_advancements: PostgameAdvancements
    bee_traps: BeeTraps
    send_defeated_mobs: SendDefeatedMobs
    death_link: DeathLink
    starting_items: StartingItems
