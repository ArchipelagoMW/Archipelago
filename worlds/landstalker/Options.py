from dataclasses import dataclass

from Options import Choice, DeathLink, DefaultOnToggle, PerGameCommonOptions, Range, Toggle


class LandstalkerGoal(Choice):
    """
    The goal to accomplish in order to complete the seed.
    - Beat Gola: beat the usual final boss (same as vanilla)
    - Reach Kazalt: find the jewels and take the teleporter to Kazalt
    - Beat Dark Nole: the door to King Nole's fight brings you into a final dungeon with an absurdly hard boss you have
        to beat to win the game
    """
    display_name = "Goal"

    option_beat_gola = 0
    option_reach_kazalt = 1
    option_beat_dark_nole = 2

    default = 0


class JewelCount(Range):
    """
    Determines the number of jewels to find to be able to reach Kazalt.
    """
    display_name = "Jewel Count"
    range_start = 0
    range_end = 9
    default = 5


class ProgressiveArmors(DefaultOnToggle):
    """
    When obtaining an armor, you get the next armor tier instead of getting the specific armor tier that was
    placed here by randomization. Enabling this provides a smoother progression.
    """
    display_name = "Progressive Armors"


class UseRecordBook(DefaultOnToggle):
    """
    Gives a Record Book item in starting inventory, allowing to save the game anywhere.
    This makes the game significantly less frustrating and enables interesting save-scumming strategies in some places.
    """
    display_name = "Use Record Book"


class UseSpellBook(DefaultOnToggle):
    """
    Gives a Spell Book item in starting inventory, allowing to warp back to the starting location at any time.
    This prevents any kind of softlock and makes the world easier to explore.
    """
    display_name = "Use Spell Book"


class EnsureEkeEkeInShops(DefaultOnToggle):
    """
    Ensures an EkeEke will always be for sale in one shop per region in the game.
    Disabling this can lead to frustrating situations where you cannot refill your health items and might get locked.
    """
    display_name = "Ensure EkeEke in Shops"


class RemoveGumiBoulder(Toggle):
    """
    Removes the boulder between Gumi and Ryuma, which is usually a one-way path.
    This makes the vanilla early game (Massan, Gumi...) more easily accessible when starting outside it.
    """
    display_name = "Remove Boulder After Gumi"


class EnemyJumpingInLogic(Toggle):
    """
    Adds jumping on enemies' heads as a logical rule.
    This gives access to Mountainous Area from Lake Shrine sector and to the cliff chest behind a magic tree near Mir Tower.
    These tricks not being easy, you should leave this disabled until practiced.
    """
    display_name = "Enemy Jumping in Logic"


class TreeCuttingGlitchInLogic(Toggle):
    """
    Adds tree-cutting glitch as a logical rule, enabling access to both chests behind magic trees in Mir Tower Sector
    without having Axe Magic.
    """
    display_name = "Tree-cutting Glitch in Logic"


class DamageBoostingInLogic(Toggle):
    """
    Adds damage boosting as a logical rule, removing any requirements involving Iron Boots or Fireproof Boots.
    Who doesn't like walking on spikes and lava?
    """
    display_name = "Damage Boosting in Logic"


class WhistleUsageBehindTrees(DefaultOnToggle):
    """
    In Greenmaze, Einstein Whistle can only be used to call Cutter from the intended side by default.
    Enabling this allows using Einstein Whistle from both sides of the magic trees.
    This is only useful in seeds starting in the "waterfall" spawn region or where teleportation trees are made open from the start.
    """
    display_name = "Allow Using Einstein Whistle Behind Trees"


class SpawnRegion(Choice):
    """
    List of spawn locations that can be picked by the randomizer.
    It is advised to keep Massan as your spawn location for your first few seeds.
    Picking a late-game location can make the seed significantly harder, both for logic and combat.
    """
    display_name = "Starting Region"

    option_massan = 0
    option_gumi = 1
    option_kado = 2
    option_waterfall = 3
    option_ryuma = 4
    option_mercator = 5
    option_verla = 6
    option_greenmaze = 7
    option_destel = 8

    default = 0


class TeleportTreeRequirements(Choice):
    """
    Determines the requirements to be able to use a teleport tree pair.
    - None: All teleport trees are available right from the start
    - Clear Tibor: Tibor needs to be cleared before unlocking any tree
    - Visit Trees: Both trees from a tree pair need to be visited to teleport between them
    Vanilla behavior is "Clear Tibor And Visit Trees"
    """
    display_name = "Teleportation Trees Requirements"

    option_none = 0
    option_clear_tibor = 1
    option_visit_trees = 2
    option_clear_tibor_and_visit_trees = 3

    default = 3


class ShuffleTrees(Toggle):
    """
    If enabled, all teleportation trees will be shuffled into new pairs.
    """
    display_name = "Shuffle Teleportation Trees"


class ReviveUsingEkeeke(DefaultOnToggle):
    """
    In the vanilla game, when you die, you are automatically revived by Friday using an EkeEke.
    This setting allows disabling this feature, making the game extremely harder.
    USE WITH CAUTION!
    """
    display_name = "Revive Using EkeEke"


class ShopPricesFactor(Range):
    """
    Applies a percentage factor on all prices in shops. Having higher prices can lead to a bit of gold farming, which
    can make seeds longer but also sometimes more frustrating.
    """
    display_name = "Shop Prices Factor (%)"
    range_start = 50
    range_end = 200
    default = 100


class CombatDifficulty(Choice):
    """
    Determines the overall combat difficulty in the game by modifying both monsters HP & damage.
    - Peaceful: 50% HP & damage
    - Easy: 75% HP & damage
    - Normal: 100% HP & damage
    - Hard: 140% HP & damage
    - Insane: 200% HP & damage
    """
    display_name = "Combat Difficulty"

    option_peaceful = 0
    option_easy = 1
    option_normal = 2
    option_hard = 3
    option_insane = 4

    default = 2


class HintCount(Range):
    """
    Determines the number of Foxy NPCs that will be scattered across the world, giving various types of hints
    """
    display_name = "Hint Count"
    range_start = 0
    range_end = 25
    default = 12


@dataclass
class LandstalkerOptions(PerGameCommonOptions):
    goal: LandstalkerGoal
    spawn_region: SpawnRegion
    jewel_count: JewelCount
    progressive_armors: ProgressiveArmors
    use_record_book: UseRecordBook
    use_spell_book: UseSpellBook

    shop_prices_factor: ShopPricesFactor
    combat_difficulty: CombatDifficulty

    teleport_tree_requirements: TeleportTreeRequirements
    shuffle_trees: ShuffleTrees

    ensure_ekeeke_in_shops: EnsureEkeEkeInShops
    remove_gumi_boulder: RemoveGumiBoulder
    allow_whistle_usage_behind_trees: WhistleUsageBehindTrees
    handle_damage_boosting_in_logic: DamageBoostingInLogic
    handle_enemy_jumping_in_logic: EnemyJumpingInLogic
    handle_tree_cutting_glitch_in_logic: TreeCuttingGlitchInLogic

    hint_count: HintCount

    revive_using_ekeeke: ReviveUsingEkeeke
    death_link: DeathLink
