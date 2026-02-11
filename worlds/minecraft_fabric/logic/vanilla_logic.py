from __future__ import annotations

from math import floor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from worlds.minecraft_fabric import FabricMinecraftWorld

from BaseClasses import CollectionState

########################################################################################################################
# VANILLA ##############################################################################################################
########################################################################################################################

# DIFFICULTY CHECK #####################################################################################################

def getDifficultyRequirements(required_options: set[str], world: FabricMinecraftWorld, state: CollectionState):
    required = True

    if "Iron Weapons" in required_options:
        required = required and canUseIronWeapons(world, state)
    if "Iron Armor" in required_options:
        required = required and canWearIronArmor(world, state)
    if "Bow" in required_options:
        required = required and canUseBow(world, state)
    if "Sprint" in required_options:
        required = required and optionalRequireSprint(world, state)
    if "Jump" in required_options:
        required = required and optionalRequireJump(world, state)
    if "Beds" in required_options:
        required = required and canSleep(world, state)
    return required

# OPTIONAL ABILITY CHECKS ##############################################################################################

def optionalRequireSprint(world: FabricMinecraftWorld, state: CollectionState):
    return checkRandomizedAbility(world, state, "Sprint", "Sprint")

def optionalRequireJump(world: FabricMinecraftWorld, state: CollectionState):
    return checkRandomizedAbility(world, state, "Jump", "Jump")

def canAccessChests(world: FabricMinecraftWorld, state: CollectionState):
    return checkRandomizedAbility(world, state, "Chests", "Chests & Barrels")

def canSwim(world: FabricMinecraftWorld, state: CollectionState):
    return checkRandomizedAbility(world, state, "Swim", "Swim")

def checkRandomizedAbility(world: FabricMinecraftWorld, state: CollectionState, value: str, item: str):
    if value in world.options.randomized_abilities.value:
        return state.has(item, world.player)
    else:
        return True

def hasOptionalGoalAbilities(world: FabricMinecraftWorld, state: CollectionState):
    return optionalRequireJump(world, state) and optionalRequireSprint(world, state)

# ABILITY CHECKS #######################################################################################################

def canTrade(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Villager Trading", world.player)

def canBarter(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Piglin Bartering", world.player) and canAccessNether(world, state) and canSmelt(world, state)

def canSleep(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Sleeping", world.player)

# CRAFTING STATION CHECKS ##############################################################################################

def canSmelt(world: FabricMinecraftWorld, state: CollectionState):
    return canUseStoneTools(world, state) and state.has("Progressive Smelting", world.player)

def canSmeltBetter(world: FabricMinecraftWorld, state: CollectionState):
    return canUseStoneTools(world, state) and state.has("Progressive Smelting", world.player, 2)

def canSmith(world: FabricMinecraftWorld, state: CollectionState):
    return canSmelt(world, state) and state.has("Smithing", world.player)

def canBrew(world: FabricMinecraftWorld, state: CollectionState):
    return canAccessNether(world, state) and canUseBottles(world, state) and state.has("Brewing", world.player)

def canEnchant(world: FabricMinecraftWorld, state: CollectionState):
    return canUseDiamondTools(world, state) and state.has("Enchanting", world.player) and canCompactResources(world, state)

def canAccessMiscJobsites(world: FabricMinecraftWorld, state: CollectionState):
    return canSmelt(world, state) and state.has("Other Crafting Stations", world.player)

# MINING TOOL CHECKS ###################################################################################################

def canUseStoneTools(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Progressive Tools", world.player)

def canUseIronTools(world: FabricMinecraftWorld, state: CollectionState):
    return canSmelt(world, state) and state.has("Progressive Tools", world.player, 2)

def canUseDiamondTools(world: FabricMinecraftWorld, state: CollectionState):
    return canUseIronTools(world, state) and state.has("Progressive Tools", world.player, 3)

def canUseNetheriteTools(world: FabricMinecraftWorld, state: CollectionState):
    return canUseDiamondTools(world, state) and state.has("Progressive Tools", world.player, 4) and canSmith(world, state) and canGetUpgradeTemplate(world, state)

# WEAPON CHECKS ###################################################################################################

def canUseStoneWeapons(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Progressive Weapons", world.player)

def canUseIronWeapons(world: FabricMinecraftWorld, state: CollectionState):
    return canUseStoneTools(world, state) and canSmelt(world, state) and state.has("Progressive Weapons", world.player, 2)

def canUseDiamondWeapons(world: FabricMinecraftWorld, state: CollectionState):
    return canUseIronTools(world, state) and state.has("Progressive Weapons", world.player, 3)

def canUseNetheriteWeapons(world: FabricMinecraftWorld, state: CollectionState):
    return canUseDiamondTools(world, state) and state.has("Progressive Weapons", world.player, 4) and canSmith(world, state) and canGetUpgradeTemplate(world, state)

# ARMOR CHECKS #########################################################################################################

def canWearLeatherArmor(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Progressive Armor", world.player)

def canWearGoldArmor(world: FabricMinecraftWorld, state: CollectionState):
    return canSmelt(world, state) and state.has("Progressive Armor", world.player, 2)

def canWearIronArmor(world: FabricMinecraftWorld, state: CollectionState):
    return canSmelt(world, state) and state.has("Progressive Armor", world.player, 3)

def canWearDiamondArmor(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Progressive Armor", world.player, 4) and canUseIronTools(world, state)

def canWearNetheriteArmor(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Progressive Armor", world.player, 5) and canSmith(world, state) and canUseDiamondTools(world, state) and canGetUpgradeTemplate(world, state)

# OTHER TOOL CHECKS ####################################################################################################

def canUseBucket(world: FabricMinecraftWorld, state: CollectionState):
    return canSmelt(world, state) and state.has("Bucket Recipes", world.player)

def canUseFlintAndSteel(world: FabricMinecraftWorld, state: CollectionState):
    return canSmelt(world, state) and state.has("Flint and Steel Recipes", world.player)

def canUseMinecart(world: FabricMinecraftWorld, state: CollectionState):
    return canSmelt(world, state) and state.has("Minecart Recipes", world.player)

def canUseBrush(world: FabricMinecraftWorld, state: CollectionState):
    return canSmelt(world, state) and state.has("Brush Recipes", world.player)

def canUseSpyglass(world: FabricMinecraftWorld, state: CollectionState):
    return canSmelt(world, state) and state.has("Spyglass Recipes", world.player)

def canUseShears(world: FabricMinecraftWorld, state: CollectionState):
    return canSmelt(world, state) and state.has("Shear Recipes", world.player)

def canUseFishingRod(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Fishing Rod Recipes", world.player)

def canUseBottles(world: FabricMinecraftWorld, state: CollectionState):
    return canSmelt(world, state) and state.has("Glass Bottle Recipes", world.player)

def canUseBow(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Progressive Archery", world.player)

def canUseCrossBow(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Progressive Archery", world.player, 2) and canSmelt(world, state)

def canUseShield(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Shield Recipes", world.player) and canSmelt(world, state)

# OTHER RECIPE CHECKS ##################################################################################################

def canCompactResources(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Resource Compacting Recipes", world.player)

def canGetEyesOfEnder(world: FabricMinecraftWorld, state: CollectionState):
    return canAccessNether(world, state) and state.has("Eye of Ender Recipes", world.player)

def canGetAndUseArmorTrims(world: FabricMinecraftWorld, state: CollectionState):
    return canSmith(world, state) and canAccessChests(world, state) and canWearLeatherArmor(world, state)

# DIMENSION CHECKS #####################################################################################################

def canAccessNether(world: FabricMinecraftWorld, state: CollectionState):
    return (((canUseDiamondTools(world, state) or canUseBucket(world, state)) and canUseFlintAndSteel(world, state))
            and getDifficultyRequirements(world.options.required_before_nether.value, world, state))

def canAccessEnd(world: FabricMinecraftWorld, state: CollectionState):
    return (canGetEyesOfEnder(world, state) and getDifficultyRequirements(world.options.required_before_bosses.value, world, state))

# MISC VANILLA #########################################################################################################

def canPlaceBeacon(world: FabricMinecraftWorld, state: CollectionState):
    return canGoalWither(world, state) and canSmelt(world, state) and canUseDiamondTools(world, state) and canCompactResources(world, state)

def canGetCryingObsidian(world: FabricMinecraftWorld, state: CollectionState):
    return canBarter(world, state) or canUseDiamondTools(world, state)

def canAccessVanillaEndGame(world: FabricMinecraftWorld, state: CollectionState):
    return ((canEnchant(world, state) and canBrew(world, state) and canPlaceBeacon(world, state)
            and canBeatDragonAndWither(world, state) and canUseDiamondTools(world, state))
            and canAccessChests(world, state))

def canDyeBasic(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Progressive Dye Recipes", world.player)

def canDyeFull(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Progressive Dye Recipes", world.player, 2)

def canDyeBlack(world: FabricMinecraftWorld, state: CollectionState):
    return canDyeBasic(world, state) and canSwim(world, state)

def canGetUpgradeTemplate(world: FabricMinecraftWorld, state: CollectionState):
    return canAccessNether(world, state) and canAccessChests(world, state)

def canCureZombieVillager(world: FabricMinecraftWorld, state: CollectionState):
    return canBrew(world, state) and (canAccessNether(world, state) or canUseIronTools(world, state))

def canGetSmoothStone(world: FabricMinecraftWorld, state: CollectionState):
    return canSmelt(world, state) or canEnchant(world, state)

def canFightRaid(world: FabricMinecraftWorld, state: CollectionState):
    return getDifficultyRequirements(world.options.required_before_raids.value, world, state)

# GOAL CHECKS ##########################################################################################################

def canGoalEnderDragon(world: FabricMinecraftWorld, state: CollectionState):
    return canAccessEnd(world, state)

def canGoalWither(world: FabricMinecraftWorld, state: CollectionState):
    return (canAccessNether(world, state) and state.has("Wither Summoning", world.player)
            and getDifficultyRequirements(world.options.required_before_bosses.value, world, state))

def canBeatDragonAndWither(world: FabricMinecraftWorld, state: CollectionState):
    return canGoalEnderDragon(world, state) and canGoalWither(world, state)

def canCompleteRubyHunt(world: FabricMinecraftWorld, state: CollectionState):
    return state.has("Ruby", world.player, floor(world.max_ruby_count * (world.options.percentage_of_rubies_needed.value * 0.01)))

