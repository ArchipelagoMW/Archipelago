from typing import Dict

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet


class JewelCount(Range):
    """
    Determines the number of jewels to find in order to be able to reach Kazalt
    """
    display_name = "Jewel Count"
    range_start = 0
    range_end = 5
    default = 2


class ProgressiveArmors(DefaultOnToggle):
    """
    When obtaining an armor, you get the next armor tier instead of getting the specific armor tier that was
    placed here by randomization. Enabling this provides a smoother progression.
    """
    display_name = "Progressive Armors"


class RemoveGumiBoulder(Toggle):
    """
    Removes the boulder between Gumi and Ryuma which is usually a one-way path.
    This makes the vanilla early game (Massan, Gumi...) more easily accessible when starting outside of it.
    """
    display_name = "Remove boulder after Gumi"


class EnemyJumpingInLogic(Toggle):
    """
    Adds jumping on enemies' heads as a logical rule, enabling access to Mountainous Area from Lake Shrine sector and
    to the cliff chest behind a magic tree in Mir Tower sector. These tricks not being easy, you should leave this
    disabled until practiced.
    """
    display_name = "Enemy jumping in logic"


class TreeCuttingGlitchInLogic(Toggle):
    """
    Adds tree-cutting glitch as a logical rule, enabling access to both chests behind magic trees in Mir Tower Sector
    without having Axe Magic.
    """
    display_name = "Tree-cutting glitch in logic"


class DamageBoostingInLogic(Toggle):
    """
    Adds damage boosting as a logical rule, removing any requirements involving Iron Boots or Fireproof Boots.
    Who doesn't like walking on spikes and lava?
    """
    display_name = "Damage boosting in logic"


class WhistleUsageBehindTrees(DefaultOnToggle):
    """
    In Greenmaze, Einstein Whistle can only be used to call the lumberjack from the intended side by default.
    Enabling this allows using Einstein Whistle from behind the trees, which can only be useful in seeds
    starting in the "waterfall" spawn region or where teleportation trees are made open from the start.
    """
    display_name = "Allow using Einstein Whistle behind trees"


class SpawnRegion(Choice):
    """
    List of spawn locations that can be picked by the randomizer. It is advised to keep Massan as your spawn location
    for your first few seeds since picking a late-game location can make the seed significantly harder, both for
    logic and combat.
    """
    display_name = "Starting Region"

    option_massan = "massan"
    option_gumi = "gumi"
    option_kado = "kado"
    option_waterfall = "waterfall"
    option_ryuma = "ryuma"
    option_mercator = "mercator"
    option_verla = "verla"
    option_greenmaze = "greenmaze"
    option_destel = "destel"

    default = "massan"


class TeleportTreeRequirements(Choice):
    """
    Determines the requirements to be able to use a teleport tree pair.
    - None: All teleport trees are available right from the start
    - Clear Tibor: Tibor needs to be cleared before unlocking any tree
    - Visit Trees: Both trees from a tree pair need to be visited to teleport between them
    Vanilla behavior is "Clear Tibor And Visit Trees"
    """
    display_name = "Teleportation trees requirements"

    option_none = 0
    option_clear_tibor = 1
    option_visit_trees = 2
    option_clear_tibor_and_visit_trees = 3

    default = 3


class ShuffleTrees(Toggle):
    """
    If enabled, all teleportation trees will be shuffled into new pairs.
    """
    display_name = "Shuffle teleportation trees"


# TODO: Also integrate cosmetic options
ls_options: Dict[str, type(Option)] = {
    "spawn_region": SpawnRegion,
    "jewel_count": JewelCount,
    "progressive_armors": ProgressiveArmors,

    "teleport_tree_requirements": TeleportTreeRequirements,
    "shuffle_trees": ShuffleTrees,

    "remove_gumi_boulder": RemoveGumiBoulder,
    "allow_whistle_usage_behind_trees": WhistleUsageBehindTrees,
    "handle_damage_boosting_in_logic": DamageBoostingInLogic,
    "handle_enemy_jumping_in_logic": EnemyJumpingInLogic,
    "handle_tree_cutting_glitch_in_logic": TreeCuttingGlitchInLogic,

    # "healthGainedPerLifestock": 1,

    # "enemiesDamageFactor": 100,
    # "enemiesHealthFactor": 100,
    # "enemiesArmorFactor": 100,
    # "enemiesGoldsFactor": 100,
    # "enemiesDropChanceFactor": 100,

    "death_link": DeathLink,
}

#    "startingGold": 0,

#    "startingItems": {
#        "Record Book": 1,
#        "Spell Book": 1
#    },
#    "consumableRecordBook": false,
#    "consumableSpellBook": false,

#    "ekeekeAutoRevive": true

#    "hintsDistribution": {
#        "regionRequirement": 6,
#        "itemRequirement": 5,
#        "itemLocation": 8,
#        "darkRegion": 1,
#        "joke": 3
#    }
