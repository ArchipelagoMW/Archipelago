from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from worlds.sonic_heroes import SonicHeroesWorld

from .constants import *
from .logicfunctions import *


def create_logic_mapping_dict_seaside_hill_sonic(world: SonicHeroesWorld):
    return \
    {
        #"": lambda state: True,  # No rules

        #"NOTPOSSIBLE": lambda state: False,

        "BreakKeyCageSonicSH": lambda state: can_break_key_cage(world, SONIC, SEASIDEHILL, state),

        "BreakKeyCageandRuinsSonicSH": lambda state: can_break_key_cage(world, SONIC, SEASIDEHILL, state) and can_ruins(world, SONIC, SEASIDEHILL, state),

        "BreakorCannonPowerSonicSH": lambda state: can_break_things(world, SONIC, SEASIDEHILL, state) or can_cannon_power(world, SONIC, SEASIDEHILL, state),

        "FlyingFullorRuinsSonicSH": lambda state: can_ruins(world, SONIC, SEASIDEHILL, state) or can_fly(world, SONIC, SEASIDEHILL, state, speedreq=True, powerreq=True),

        "FlyingFullSonicSH": lambda state: can_fly(world, SONIC, SEASIDEHILL, state, speedreq=True, powerreq=True),

        "FlyingOneCharorTripleSpringSonicSH": lambda state: can_fly(world, SONIC, SEASIDEHILL, state, speedreq=True, powerreq=True, orcondition=True) or can_triple_spring(world, SONIC, SEASIDEHILL, state),

        "FlyingFullor(RuinsandSingleSpringandSmallStonePlatform)SonicSH": lambda state: can_fly(world, SONIC, SEASIDEHILL, state, speedreq=True, powerreq=True) or (can_ruins(world, SONIC, SEASIDEHILL, state) and can_single_spring(world, SONIC, SEASIDEHILL, state) and can_small_stone_platform(world, SONIC, SEASIDEHILL, state)),

        "DashRampSonicSH": lambda state: can_dash_ramp(world, SONIC, SEASIDEHILL, state),

        "DashPanelorSpeedSonicSH": lambda state: can_dash_panel(world, SONIC, SEASIDEHILL, state) or has_char(world, SONIC, SEASIDEHILL, state, speed=True),

        "SingleSpringSonicSH": lambda state: can_single_spring(world, SONIC, SEASIDEHILL, state),

        "(BreakandSingleSpring)orFlyingAnySonicSH": lambda state: (can_break_things(world, SONIC, SEASIDEHILL, state) and can_single_spring(world, SONIC, SEASIDEHILL, state)) or can_fly(world, SONIC, SEASIDEHILL, state),

        "(BreakandTripleSpring)orFlyingAnySonicSH": lambda state: (can_break_things(world, SONIC, SEASIDEHILL, state) and can_triple_spring(world, SONIC, SEASIDEHILL, state)) or can_fly(world, SONIC, SEASIDEHILL, state),

        "FlyingAnySonicSH": lambda state: can_fly(world, SONIC, SEASIDEHILL, state),

        "FlyingAnyandSmallStonePlatformSonicSH": lambda state: can_fly(world, SONIC, SEASIDEHILL, state) and can_small_stone_platform(world, SONIC, SEASIDEHILL, state),

        "FlyingAnyorTripleSpringSonicSH": lambda state: can_fly(world, SONIC,SEASIDEHILL, state) or can_triple_spring(world, SONIC, SEASIDEHILL, state),

        "BreakorFlyingAnyorHomingSonicSH": lambda state: can_break_things(world, SONIC, SEASIDEHILL, state) or can_fly(world, SONIC, SEASIDEHILL, state) or can_homing_attack(world, SONIC, SEASIDEHILL, state),

        "BreakorFlyingAnySonicSH": lambda state: can_break_things(world, SONIC, SEASIDEHILL, state) or can_fly(world, SONIC, SEASIDEHILL, state),

        "(CannonAnyorFlyingFull)andRuinsSonicSH": lambda state: (can_cannon(world, SONIC, SEASIDEHILL, state, speed=True, flying=True, power=True, orcondition=True) or can_fly(world, SONIC, SEASIDEHILL, state, speedreq=True, powerreq=True)) and can_ruins(world, SONIC, SEASIDEHILL, state),

        "FlyingFullandRuinsSonicSH": lambda state: can_ruins(world, SONIC, SEASIDEHILL, state) and can_fly(world, SONIC, SEASIDEHILL, state, speedreq=True, powerreq=True),

        "CannonSpeedSonicSH": lambda state: can_cannon(world, SONIC, SEASIDEHILL, state, speed=True),

        "CannonFlyingSonicSH": lambda state: can_cannon(world, SONIC, SEASIDEHILL, state, flying=True),

        "CannonPowerSonicSH": lambda state: can_cannon(world, SONIC, SEASIDEHILL, state, power=True),

        "DashRingorFlyingAnySonicSH": lambda state: can_dash_ring(world, SONIC, SEASIDEHILL, state) or can_fly(world, SONIC, SEASIDEHILL, state),

        "DashRampandDashRingandFlyingAnySonicSH": lambda state: can_dash_ramp(world, SONIC, SEASIDEHILL, state) and can_dash_ring(world, SONIC, SEASIDEHILL, state) and can_fly(world, SONIC, SEASIDEHILL, state),

        "FlyingAnyandRuinsSonicSH": lambda state: can_fly(world, SONIC, SEASIDEHILL, state) and can_ruins(world, SONIC, SEASIDEHILL, state),

        "RuinsSonicSH": lambda state: can_ruins(world,SONIC,SEASIDEHILL, state),

        "DashPanelor(DashRingandFlyingAny)orSpeedSonicSH": lambda state: can_dash_panel(world,SONIC,SEASIDEHILL, state) or (can_dash_ring(world,SONIC,SEASIDEHILL, state) and can_fly(world,SONIC,SEASIDEHILL, state)) or has_char(world,SONIC,SEASIDEHILL, state, speed=True),

        "((BreakorHoming)andSingleSpring)orFlyingAnySonicSH": lambda state: ((can_break_things(world,SONIC,SEASIDEHILL, state) or can_homing_attack(world,SONIC,SEASIDEHILL, state)) and can_single_spring(world,SONIC,SEASIDEHILL, state)) or can_fly(world,SONIC,SEASIDEHILL, state),

        "TripsleSpringSonicSH": lambda state: can_triple_spring(world, SONIC, SEASIDEHILL, state),

        "DashRingandFlyingAnyandSingleSpringSonicSH": lambda state: can_dash_ring(world, SONIC, SEASIDEHILL, state) and can_fly(world, SONIC, SEASIDEHILL, state) and can_single_spring(world, SONIC, SEASIDEHILL, state),

        "Breakand(DashRingorFlyingAny)andSingleSpringSonicSH": lambda state: can_break_things(world, SONIC, SEASIDEHILL, state) and (can_dash_ring(world, SONIC, SEASIDEHILL, state) or can_fly(world, SONIC, SEASIDEHILL, state)) and can_single_spring(world, SONIC, SEASIDEHILL, state),

        "DashRingandFlyingAnySonicSH": lambda state: can_dash_ring(world, SONIC, SEASIDEHILL, state) and can_fly(world, SONIC, SEASIDEHILL, state),

        "GlideandRuinsandTripleSpringSonicSH": lambda state: can_glide(world, SONIC, SEASIDEHILL, state) and can_ruins(world, SONIC, SEASIDEHILL, state) and can_triple_spring(world, SONIC, SEASIDEHILL, state),

        "DashRampandRuinsSonicSH": lambda state: can_dash_ramp(world, SONIC, SEASIDEHILL, state) and can_ruins(world, SONIC, SEASIDEHILL, state),

        "BobsledSonicSH": lambda state: can_bobsled(world, SONIC, SEASIDEHILL, state),

        "TripleSpringSonicSH": lambda state: can_triple_spring(world, SONIC, SEASIDEHILL, state),

        "DashRingandSingleSpringSonicSH": lambda state: can_dash_ring(world, SONIC, SEASIDEHILL, state) and can_single_spring(world, SONIC, SEASIDEHILL, state),

        "DashRingSonicSH": lambda state: can_dash_ring(world, SONIC, SEASIDEHILL, state)
    }

def create_logic_mapping_dict_ocean_palace_sonic(world: SonicHeroesWorld):
    return \
    {
        #"": lambda state: True,

        #"NOTPOSSIBLE": lambda state: False,

        "BreakKeyCageSonicOP": lambda state: can_break_key_cage(world, SONIC, OCEANPALACE, state),

        "DashRampSonicOP": lambda state: can_dash_ramp(world, SONIC, OCEANPALACE, state),

        "FlyingAnyorTripleSpringSonicOP": lambda state: can_fly(world, SONIC, OCEANPALACE, state) or can_triple_spring(world, SONIC, OCEANPALACE, state),

        "BreakSonicOP": lambda state: can_break_things(world, SONIC, OCEANPALACE, state),

        "(DashRingorFlyingAny)andFallingStoneStructureSonicOP": lambda state: (can_dash_ring(world, SONIC, OCEANPALACE, state) or can_fly(world, SONIC, OCEANPALACE, state)) and can_falling_stone_structure(world, SONIC, OCEANPALACE, state),

        "FanandGlideSonicOP": lambda state: can_fan(world, SONIC, OCEANPALACE, state) and can_glide(world, SONIC, OCEANPALACE, state),

        "FallingStoneStructureandFlyingAnySonicOP": lambda state: can_falling_stone_structure(world, SONIC, OCEANPALACE, state) and can_fly(world, SONIC, OCEANPALACE, state),

        "FlyingAnySonicOP": lambda state: can_fly(world, SONIC, OCEANPALACE, state),

        "FlyingFullSonicOP": lambda state: can_fly(world, SONIC, OCEANPALACE, state, speedreq=True, powerreq=True),

        "TriangleJumpSonicOP": lambda state: can_triangle_jump(world, SONIC, OCEANPALACE, state),

        "FlyingFullor(FanandGlide)SonicOP": lambda state: can_fly(world, SONIC, OCEANPALACE, state, speedreq=True, powerreq=True) or (can_fan(world, SONIC, OCEANPALACE, state) and can_glide(world, SONIC, OCEANPALACE, state)),

        "DashRampor(FlyingFullandRainbowHoops)SonicOP": lambda state: can_dash_ramp(world, SONIC, OCEANPALACE, state) or (can_fly(world, SONIC, OCEANPALACE, state, speedreq=True, powerreq=True) or can_rainbow_hoops(world, SONIC, OCEANPALACE, state)),

        "BreakorFlyingAnySonicOP": lambda state: can_break_things(world, SONIC, OCEANPALACE, state) or can_fly(world, SONIC, OCEANPALACE, state),

        "CannonSpeedSonicOP": lambda state: can_cannon(world, SONIC, OCEANPALACE, state, speed=True),

        "CannonFlyingSonicOP": lambda state: can_cannon(world, SONIC, OCEANPALACE, state, flying=True),

        "CannonPowerSonicOP": lambda state: can_cannon(world, SONIC, OCEANPALACE, state, power=True),

        "KillGroundEnemyConcreteShieldSonicOP": lambda state: can_kill_ground_enemy(world, SONIC, OCEANPALACE, state, concreteshield=True),

        "KillFlyingEnemyGreenShotNothingSonicOP": lambda state: can_kill_flying_enemy(world, SONIC, OCEANPALACE, state, green_shot=True, nothing=True),

        "KillGroundEnemySpearConcreteShieldandKillFlyingEnemyGreenShotNothingSonicOP": lambda state: can_kill_ground_enemy(world, SONIC, OCEANPALACE, state, spear=True, concreteshield=True) and can_kill_flying_enemy(world, SONIC, OCEANPALACE, state, green_shot=True, nothing=True),

        "SingleSpringSonicOP": lambda state: can_single_spring(world, SONIC, OCEANPALACE, state),

        "DashRingandFlyingAnySonicOP": lambda state: can_dash_ring(world, SONIC, OCEANPALACE, state) and can_fly(world, SONIC, OCEANPALACE, state),

        "DashRingandFanandGlideSonicOP": lambda state: can_dash_ring(world, SONIC, OCEANPALACE, state) and can_fan(world, SONIC, OCEANPALACE, state) and can_glide(world, SONIC, OCEANPALACE, state),

        "KillGroundEnemySonicOP": lambda state: can_kill_ground_enemy(world, SONIC, OCEANPALACE, state),

        "FlyingAnyorHomingAttackSonicOP": lambda state: can_fly(world, SONIC, OCEANPALACE, state) or can_homing_attack(world, SONIC, OCEANPALACE, state),

        "TripleSpringorFlyingFullSonicOP": lambda state: can_triple_spring(world, SONIC, OCEANPALACE, state) or can_fly(world, SONIC, OCEANPALACE, state, speedreq=True, powerreq=True),

        "(FanandGlide)orFlyingFullSonicOP": lambda state: (can_fan(world, SONIC, OCEANPALACE, state) and can_glide(world, SONIC, OCEANPALACE, state)) or can_fly(world, SONIC, OCEANPALACE, state, speedreq=True, powerreq=True),

        "FlyingFullorTripleSpringSonicOP": lambda state: can_fly(world, SONIC, OCEANPALACE, state, speedreq=True, powerreq=True) or can_triple_spring(world, SONIC, OCEANPALACE, state),

        "TripleSpringSonicOP": lambda state: can_triple_spring(world, SONIC, OCEANPALACE, state),

        "DashRingandSpeedcharandSingleSpringandSmallStonePlatformSonicOP": lambda state: can_dash_ring(world, SONIC, OCEANPALACE, state) and has_char(world, SONIC, OCEANPALACE, state, speed=True) and can_single_spring(world, SONIC, OCEANPALACE, state) and can_small_stone_platform(world, SONIC, OCEANPALACE, state),

        "BreakandSingleSpringSonicOP": lambda state: can_break_things(world, SONIC, OCEANPALACE, state) and can_single_spring(world, SONIC, OCEANPALACE, state)
    }

def create_logic_mapping_dict_grand_metropolis_sonic(world: SonicHeroesWorld):
    return \
    {
        #"": lambda state: True,

        #"NOTPOSSIBLE": lambda state: False,

        "BreakKeyCageSonicGM": lambda state: can_break_key_cage(world, SONIC, GRANDMETROPOLIS, state),

        "DashRampSonicGM": lambda state: can_dash_ramp(world, SONIC, GRANDMETROPOLIS, state),

        "FlyingFullSonicGM": lambda state: can_fly(world, SONIC, GRANDMETROPOLIS, state, speedreq=True, powerreq=True),

        "TripleSpringSonicGM": lambda state: can_triple_spring(world, SONIC, GRANDMETROPOLIS, state),

        "HomingAttackSonicGM": lambda state: can_homing_attack(world, SONIC, GRANDMETROPOLIS, state),

        "KillGroundEnemyCameronSonicGM": lambda state: can_kill_ground_enemy(world, SONIC, GRANDMETROPOLIS, state, cameron=True),

        "PushPullSwitchSonicGM": lambda state: can_switch(world, SONIC, GRANDMETROPOLIS, state, push_pull=True),

        "AccelRoadandKillFlyingEnemyRedNothingSonicGM": lambda state: can_accel_road(world, SONIC, GRANDMETROPOLIS, state) and can_kill_flying_enemy(world, SONIC, GRANDMETROPOLIS, state, red_flapper=True, nothing=True),

        "KillFlyingEnemyRedNothingSonicGM": lambda state: can_kill_flying_enemy(world, SONIC, GRANDMETROPOLIS, state, red_flapper=True, nothing=True),

        "BreakNotKeySonicGM": lambda state: can_break_things(world, SONIC, GRANDMETROPOLIS, state),

        "SwitchSonicGM": lambda state: can_switch(world, SONIC, GRANDMETROPOLIS, state, regular=True),

        "KillGroundEnemyNothingSonicGM": lambda state: can_kill_ground_enemy(world, SONIC, GRANDMETROPOLIS, state, nothing=True),

        "LightDashSonicGM": lambda state: can_light_dash(world, SONIC, GRANDMETROPOLIS, state),

        "FlyingAnyorSingleSpringorTripleSpringSonicGM": lambda state: can_fly(world, SONIC, GRANDMETROPOLIS, state) or can_single_spring(world, SONIC, GRANDMETROPOLIS, state) or can_triple_spring(world, SONIC, GRANDMETROPOLIS, state),

        "HomingAttackandLightDashSonicGM": lambda state: can_homing_attack(world, SONIC, GRANDMETROPOLIS, state) and can_light_dash(world, SONIC, GRANDMETROPOLIS, state),

        "FlyingAnySonicGM": lambda state: can_fly(world, SONIC, GRANDMETROPOLIS, state),

        "SingleSpringSonicGM": lambda state: can_single_spring(world, SONIC, GRANDMETROPOLIS, state),

        "FlyingAnyorLightDashSonicGM": lambda state: can_fly(world, SONIC, GRANDMETROPOLIS, state) or can_light_dash(world, SONIC, GRANDMETROPOLIS, state),

        "FlyingAnyor(HomingAttackandLightDash)SonicGM": lambda state: can_fly(world, SONIC, GRANDMETROPOLIS, state) or (can_homing_attack(world, SONIC, GRANDMETROPOLIS, state) and can_light_dash(world, SONIC, GRANDMETROPOLIS, state)),

        "(FlyingOneCharandUnbreakableContainer)orTripleSpringSonicGM": lambda state: (can_fly(world, SONIC, GRANDMETROPOLIS, state, speedreq=True, powerreq=True, orcondition=True) and can_unbreakable_container(world, SONIC, GRANDMETROPOLIS, state)) or can_triple_spring(world, SONIC, GRANDMETROPOLIS, state),

        "KillGroundEnemySpearConcreteShieldSonicGM": lambda state: can_kill_ground_enemy(world, SONIC, GRANDMETROPOLIS, state, spear=True, concreteshield=True),

        "DashRamporFlyingAnySonicGM": lambda state: can_dash_ramp(world, SONIC, GRANDMETROPOLIS, state) or can_fly(world, SONIC, GRANDMETROPOLIS, state),

        "PoleSonicGM": lambda state: can_pole(world, SONIC, GRANDMETROPOLIS, state),

        "FlyingAnyorHomingorGlideSonicGM": lambda state: can_fly(world, SONIC, GRANDMETROPOLIS, state) or can_homing_attack(world, SONIC, GRANDMETROPOLIS, state) or can_glide(world, SONIC, GRANDMETROPOLIS, state),

        "PoleandSwitchSonicGM": lambda state: can_pole(world, SONIC, GRANDMETROPOLIS, state) and can_switch(world, SONIC, GRANDMETROPOLIS, state, regular=True),

        "LightDashorTripleSpringSonicGM": lambda state: can_light_dash(world, SONIC, GRANDMETROPOLIS, state) or can_triple_spring(world, SONIC, GRANDMETROPOLIS, state),

        "CannonSpeedSonicGM": lambda state: can_cannon(world, SONIC, GRANDMETROPOLIS, state, speed=True),

        "CannonFlyingSonicGM": lambda state: can_cannon(world, SONIC, GRANDMETROPOLIS, state, flying=True),

        "CannonPowerSonicGM": lambda state: can_cannon(world, SONIC, GRANDMETROPOLIS, state, power=True),

        "FlyingAnyorTripleSpringSonicGM": lambda state: can_fly(world, SONIC, GRANDMETROPOLIS, state) or can_triple_spring(world, SONIC, GRANDMETROPOLIS, state),

        "PoleandSingleSpringSonicGM": lambda state: can_pole(world, SONIC, GRANDMETROPOLIS, state) and can_single_spring(world, SONIC, GRANDMETROPOLIS, state),

        "FlyingOneCharandPoleandThunderShootSonicGM": lambda state: can_fly(world, SONIC, GRANDMETROPOLIS, state, speedreq=True, powerreq=True, orcondition=True) and can_pole(world, SONIC, GRANDMETROPOLIS, state) and can_thundershoot_both(world, SONIC, GRANDMETROPOLIS, state),

        "FallingBridgeandKillGroundEnemyCameronSonicGM": lambda state: can_falling_drawbridge(world, SONIC, GRANDMETROPOLIS, state) and can_kill_ground_enemy(world, SONIC, GRANDMETROPOLIS, state, cameron=True),

        "DashRingSonicGM": lambda state: can_dash_ring(world, SONIC, GRANDMETROPOLIS, state),

        "AccelRoadandKillGroundEnemyCameronSonicGM": lambda state: can_accel_road(world, SONIC, GRANDMETROPOLIS, state) and can_kill_ground_enemy(world, SONIC, GRANDMETROPOLIS, state, cameron=True),

        "(Homing3orTornado)andPoleSonicGM": lambda state: ((can_homing_attack(world, SONIC, GRANDMETROPOLIS, state) and has_char_levelup(world, SONIC, GRANDMETROPOLIS, state, 3, speed=True)) or can_tornado(world, SONIC, GRANDMETROPOLIS, state)) and can_pole(world, SONIC, GRANDMETROPOLIS, state),
    }

def create_logic_mapping_dict_power_plant_sonic(world: SonicHeroesWorld):
    return \
    {
        #"": lambda state: True,

        #"NOTPOSSIBLE": lambda state: False,

        "BreakKeyCageSonicPP": lambda state: can_break_key_cage(world, SONIC, POWERPLANT, state),

        "DashRingSonicPP": lambda state: can_dash_ring(world, SONIC, POWERPLANT, state),

        "SingleSpringSonicPP": lambda state: can_single_spring(world, SONIC, POWERPLANT, state),

        "FlyingAnyorGlideSonicPP": lambda state: can_fly(world, SONIC, POWERPLANT, state) or can_glide(world, SONIC, POWERPLANT, state),

        "KillFlyingEnemyRedNothingandPPUpwardPathSonicPP": lambda state: can_kill_flying_enemy(world, SONIC, POWERPLANT, state, red_flapper=True, nothing=True) and can_energy_road_upward_effect(world, SONIC, POWERPLANT, state),

        "KillFlyingEnemyGreenLightningNothingHomingFireDunkandEnergyColumnSonicPP": lambda state: can_kill_flying_enemy(world, SONIC, POWERPLANT, state, green_lightning=True, nothing=True, homing=True, firedunk=True) and can_energy_column(world, SONIC, POWERPLANT, state),

        "KillFlyingEnemyGreenLightningNothingHomingFireDunkandPPUpwardPathSonicPP": lambda state: can_kill_flying_enemy(world, SONIC, POWERPLANT, state, green_lightning=True, nothing=True, homing=True, firedunk=True) and can_energy_road_upward_effect(world, SONIC, POWERPLANT, state),

        "FlyingAnySonicPP": lambda state: can_fly(world, SONIC, POWERPLANT, state),

        "AccelRoadandKillFlyingEnemyGreenLightningNothingHomingFireDunkSonicPP": lambda state: can_accel_road(world, SONIC, POWERPLANT, state) and can_kill_flying_enemy(world, SONIC, POWERPLANT, state, green_lightning=True, nothing=True, homing=True, firedunk=True),

        "PPUpwardPathSonicPP": lambda state: can_energy_road_upward_effect(world, SONIC, POWERPLANT, state),

        "FlyingAnyandPulleySonicPP": lambda state: can_fly(world, SONIC, POWERPLANT, state) and can_pulley(world, SONIC, POWERPLANT, state),

        "EnergyColumnandKillFlyingEnemyGreenLightningSonicPP": lambda state: can_energy_column(world, SONIC, POWERPLANT, state) and can_kill_flying_enemy(world, SONIC, POWERPLANT, state, green_lightning=True),

        "FlyingAnyandPPUpwardPathSonicPP": lambda state: can_fly(world, SONIC, POWERPLANT, state) and can_energy_road_upward_effect(world, SONIC, POWERPLANT, state),

        "FlyingAnyorHomingorGlideSonicPP": lambda state: can_fly(world, SONIC, POWERPLANT, state) or can_homing_attack(world, SONIC, POWERPLANT, state) or can_glide(world, SONIC, POWERPLANT, state),

        "KillFlyingEnemyRedandPoleandSwitch": lambda state: can_kill_flying_enemy(world, SONIC, POWERPLANT, state, red_flapper=True) and can_pole(world, SONIC, POWERPLANT, state) and can_switch(world, SONIC, POWERPLANT, state, regular=True),

        "FlyingAnyorHomingorPPUpwardPathSonicPP": lambda state: can_fly(world, SONIC, POWERPLANT, state) or can_homing_attack(world, SONIC, POWERPLANT, state) or can_energy_road_upward_effect(world, SONIC, POWERPLANT, state),

        "KillFlyingEnemyGreenLightningandPoleandSwitch": lambda state: can_kill_flying_enemy(world, SONIC, POWERPLANT, state, green_lightning=True) and can_pole(world, SONIC, POWERPLANT, state) and can_switch(world, SONIC, POWERPLANT, state, regular=True),

        "KillGroundEnemyCameronSonicPP": lambda state: can_kill_ground_enemy(world, SONIC, POWERPLANT, state, cameron=True),

        "PulleySonicPP": lambda state: can_pulley(world, SONIC, POWERPLANT, state),

        "EnergyColumnandFlyingAnyandKillFlyingEnemyRedSonicPP": lambda state: can_energy_column(world, SONIC, POWERPLANT, state) and can_fly(world, SONIC, POWERPLANT, state) and can_kill_flying_enemy(world, SONIC, POWERPLANT, state, red_flapper=True),

        "EnergyColumnandFlyingAnyandKillGroundEnemyCameronSonicPP": lambda state: can_energy_column(world, SONIC, POWERPLANT, state) and can_fly(world, SONIC, POWERPLANT, state) and can_kill_ground_enemy(world, SONIC, POWERPLANT, state, cameron=True),

        "EnergyColumnandFlyingOneCharandKillFlyingEnemyRedSonicPP": lambda state: can_energy_column(world, SONIC, POWERPLANT, state) and can_fly(world, SONIC, POWERPLANT, state, speedreq=True, powerreq=True, orcondition=True) and can_kill_flying_enemy(world, SONIC, POWERPLANT, state, red_flapper=True),

        "FlyingAnyorLightDashSonicPP": lambda state: can_fly(world, SONIC, POWERPLANT, state) or can_light_dash(world, SONIC, POWERPLANT, state),

        "EnergyColumnandFlyingAnyandKillFlyingEnemyGreenLightningSonicPP": lambda state: can_energy_column(world, SONIC, POWERPLANT, state) and can_fly(world, SONIC, POWERPLANT, state) and can_kill_flying_enemy(world, SONIC, POWERPLANT, state, green_lightning=True),

        "FlyingAnyorTripleSpringSonicPP": lambda state: can_fly(world, SONIC, POWERPLANT, state) or can_triple_spring(world, SONIC, POWERPLANT, state),

        "(DashRamporFlyingAny)andElevatorSonicPP": lambda state: (can_dash_ramp(world, SONIC, POWERPLANT, state) or can_fly(world, SONIC, POWERPLANT, state)) and can_elevator(world, SONIC, POWERPLANT, state),

        "FlyingAnyandShutterSonicPP": lambda state: can_fly(world, SONIC, POWERPLANT, state) and can_shutter(world, SONIC, POWERPLANT, state),

        "KillFlyingEnemyGreenShotNothingSonicPP": lambda state: can_kill_flying_enemy(world, SONIC, POWERPLANT, state, green_shot=True, nothing=True),

        "ElevatorandFlyingAnySonicPP": lambda state: can_elevator(world, SONIC, POWERPLANT, state) and can_fly(world, SONIC, POWERPLANT, state),

        "EnergyColumnandFlyingAnyandKillFlyingEnemyRedNothingSonicPP": lambda state: can_energy_column(world, SONIC, POWERPLANT, state) and can_fly(world, SONIC, POWERPLANT, state) and can_kill_flying_enemy(world, SONIC, POWERPLANT, state, red_flapper=True, nothing=True),

        "FlyingAnyorGlideorHomingSonicPP": lambda state: can_fly(world, SONIC, POWERPLANT, state) or can_glide(world, SONIC, POWERPLANT, state) or can_homing_attack(world, SONIC, POWERPLANT, state),

        "DashPanelorFlyingAnyorLightDashorSpeedCharSonicPP": lambda state: can_dash_panel(world, SONIC, POWERPLANT, state) or can_fly(world, SONIC, POWERPLANT, state) or can_light_dash(world, SONIC, POWERPLANT, state) or has_char(world, SONIC, POWERPLANT, state, speed=True),

        "FlyingFullorPulleySonicPP": lambda state: can_fly(world, SONIC, POWERPLANT, state, speedreq=True, powerreq=True) or can_pulley(world, SONIC, POWERPLANT, state),

        "DashPanelorFlyingAnyorSpeedCharSonicPP": lambda state: can_dash_panel(world, SONIC, POWERPLANT, state) or can_fly(world, SONIC, POWERPLANT, state) or has_char(world, SONIC, POWERPLANT, state, speed=True),

        "EnergyColumnandFlyingAnyandKillFlyingEnemyGreenShotSonicPP": lambda state: can_energy_column(world, SONIC, POWERPLANT, state) and can_fly(world, SONIC, POWERPLANT, state) and can_kill_flying_enemy(world, SONIC, POWERPLANT, state, green_shot=True),

        "EnergyColumnand(FlyingAnyorHoming)andKillFlyingEnemyRedHomingSonicPP": lambda state: can_energy_column(world, SONIC, POWERPLANT, state) and (can_fly(world, SONIC, POWERPLANT, state) or can_homing_attack(world, SONIC, POWERPLANT, state)) and can_kill_flying_enemy(world, SONIC, POWERPLANT, state, red_flapper=True, homing=True),

        "EnergyColumnandFlyingAnySonicPP": lambda state: can_energy_column(world, SONIC, POWERPLANT, state) and can_fly(world, SONIC, POWERPLANT, state),

        "KillFlyingEnemyGreenShotNothingandSingleSpringSonicPP": lambda state: can_kill_flying_enemy(world, SONIC, POWERPLANT, state, green_shot=True, nothing=True) and can_single_spring(world, SONIC, POWERPLANT, state),

        "KillFlyingEnemyRedNothingSonicPP": lambda state: can_kill_flying_enemy(world, SONIC, POWERPLANT, state, red_flapper=True, nothing=True),

        "KillFlyingEnemyRedSonicPP": lambda state: can_kill_flying_enemy(world, SONIC, POWERPLANT, state, red_flapper=True),

        "KillFlyingEnemyGreenLightningSonicPP": lambda state: can_kill_flying_enemy(world, SONIC, POWERPLANT, state, green_lightning=True),

        "KillFlyingEnemyGreenLightningHomingFireDunkSonicPP": lambda state: can_kill_flying_enemy(world, SONIC, POWERPLANT, state, green_lightning=True, homing=True, firedunk=True),

        "EnergyColumnSonicPP": lambda state: can_energy_column(world, SONIC, POWERPLANT, state),

        "KillGroundEnemyCameronandSingleSpringSonicPP": lambda state: can_kill_ground_enemy(world, SONIC, POWERPLANT, state, cameron=True),

        "EnergyColumnandKillGroundEnemyCameronSonicPP": lambda state: can_energy_column(world, SONIC, POWERPLANT, state) and can_kill_ground_enemy(world, SONIC, POWERPLANT, state, cameron=True),

        "PoleSonicPP": lambda state: can_pole(world, SONIC, POWERPLANT, state),

        "ElevatorSonicPP": lambda state: can_elevator(world, SONIC, POWERPLANT, state),

        "KillGroundEnemyCameronandPPUpwardPathSonicPP": lambda state: can_kill_ground_enemy(world, SONIC, POWERPLANT, state, cameron=True) and can_energy_road_upward_effect(world, SONIC, POWERPLANT, state),

        "DashRamporFlyingAnySonicPP": lambda state: can_dash_ramp(world, SONIC, POWERPLANT, state) or can_fly(world, SONIC, POWERPLANT, state),

        "DashRingorFlyingAnySonicPP": lambda state: can_dash_ring(world, SONIC, POWERPLANT, state) or can_fly(world, SONIC, POWERPLANT, state),

        "FlyingAnyorHomingSonicPP": lambda state: can_fly(world, SONIC, POWERPLANT, state) or can_homing_attack(world, SONIC, POWERPLANT, state),

        "DashRingandFlyingAnySonicPP": lambda state: can_dash_ring(world, SONIC, POWERPLANT, state) and can_fly(world, SONIC, POWERPLANT, state),

        "HomingandLightDashSonicPP": lambda state: can_homing_attack(world, SONIC, POWERPLANT, state) and can_light_dash(world, SONIC, POWERPLANT, state),

        "(FlyingAnyorHoming)andDashRingSonicPP": lambda state: (can_fly(world, SONIC, POWERPLANT, state) or can_homing_attack(world, SONIC, POWERPLANT, state)) and can_dash_ring(world, SONIC, POWERPLANT, state),

        "(FlyingAnyorHoming)andPulleySonicPP": lambda state: (can_fly(world, SONIC, POWERPLANT, state) or can_homing_attack(world, SONIC, POWERPLANT, state)) and can_pulley(world, SONIC, POWERPLANT, state),

        "FlyingAnyandSingleSpringSonicPP": lambda state: can_fly(world, SONIC, POWERPLANT, state) and can_single_spring(world, SONIC, POWERPLANT, state),
    }

def create_logic_mapping_dict_casino_park_sonic(world: SonicHeroesWorld):
    return \
    {
        #"": lambda state: True,

        #"NOTPOSSIBLE": lambda state: False,

        "BreakKeyCageSonicCP": lambda state: can_break_key_cage(world, SONIC, CASINOPARK, state),

        "SpringSonicCP": lambda state: can_single_spring(world, SONIC, CASINOPARK, state),

        "PinballandSingleSpringSonicCP": lambda state: can_pinball(world, SONIC, CASINOPARK, state) and can_single_spring(world, SONIC, CASINOPARK, state),

        "FlyingAnyorGlideorHomingorStarPanelSonicCP": lambda state: can_fly(world, SONIC, CASINOPARK, state) or can_glide(world, SONIC, CASINOPARK, state) or can_star_glass_air_panel(world, SONIC, CASINOPARK, state),

        "TripleSpringSonicCP": lambda state: can_triple_spring(world, SONIC, CASINOPARK, state),

        "FlyingAnyorGreenBumperSpringSonicCP": lambda state: can_fly(world, SONIC, CASINOPARK, state) or can_green_floating_bumper(world, SONIC, CASINOPARK, state),

        "LightDashandSwitchSonicCP": lambda state: can_light_dash(world, SONIC, CASINOPARK, state) and can_switch(world, SONIC, CASINOPARK, state, regular=True),

        "FlyingAnyorGlideorRocketAccelSonicCP": lambda state: can_fly(world, SONIC, CASINOPARK, state) or can_glide(world, SONIC, CASINOPARK, state) or can_rocket_accel(world, SONIC, CASINOPARK, state),

        "PushPullSwitchSonicCP": lambda state: can_switch(world, SONIC, CASINOPARK, state, push_pull=True),

        "BreakGlassFloorSonicCP": lambda state: can_break_glass_floor(world, SONIC, CASINOPARK, state),

        "PinballSonicCP": lambda state: can_pinball(world, SONIC, CASINOPARK, state),

        "FloatingDiceorFlyingAnySonicCP": lambda state: can_floating_dice(world, SONIC, CASINOPARK, state) or can_fly(world, SONIC, CASINOPARK, state),

        "FlyingAnyandTripleSpringSonicCP": lambda state: can_fly(world, SONIC, CASINOPARK, state) and can_triple_spring(world, SONIC, CASINOPARK, state),

        "SingleSpringSonicCP": lambda state: can_single_spring(world, SONIC, CASINOPARK, state),

        "GongSonicCP": lambda state: can_gong(world, SONIC, CASINOPARK, state),

        "Cannonand(FlyingCharorSpeedChar)andPinballandPulleyandSingleSpringandTripleSpringSonicCP": lambda state: can_cannon(world, SONIC, CASINOPARK, state, speed=True, flying=True, orcondition=True) and can_pinball(world, SONIC, CASINOPARK, state) and can_pulley(world, SONIC, CASINOPARK, state) and can_single_spring(world, SONIC, CASINOPARK, state) and can_triple_spring(world, SONIC, CASINOPARK, state),

        "PulleyandTripleSpringSonicCP": lambda state: can_pulley(world, SONIC, CASINOPARK, state) and can_triple_spring(world, SONIC, CASINOPARK, state),

        "CannonandSpeedCharSonicCP": lambda state: can_cannon(world, SONIC, CASINOPARK, state, speed=True),

        "CannonandFlyingCharSonicCP": lambda state: can_cannon(world, SONIC, CASINOPARK, state, flying=True),

        "FlyingCharand(PowerCharorSpeedChar)andPushPullSwitchSonicCP": lambda state: has_char(world, SONIC, CASINOPARK, state, flying=True) and (has_char(world, SONIC, CASINOPARK, state, speed=True, power=True, orcondition=True)) and can_switch(world, SONIC, CASINOPARK, state, push_pull=True),

        "KillGroundEnemyGoldCameronKlagenPlainShieldSonicCP": lambda state: can_kill_ground_enemy(world, SONIC, CASINOPARK, state, plainshield=True, klagen=True, goldcameron=True),

        "FlyingAnySonicCP": lambda state: can_fly(world, SONIC, CASINOPARK, state),

        "DashPanelandSingleSpringSonicCP": lambda state: can_dash_panel(world, SONIC, CASINOPARK, state) and can_single_spring(world, SONIC, CASINOPARK, state),

        "CannonorFloatingDiceorFlyingAnyorGlideorRocketAccelSonicCP": lambda state: can_cannon(world, SONIC, CASINOPARK, state) or can_floating_dice(world, SONIC, CASINOPARK, state) or can_fly(world, SONIC, CASINOPARK, state) or can_glide(world, SONIC, CASINOPARK, state) or can_rocket_accel(world, SONIC, CASINOPARK, state),

        "GreenBumperSpringSonicCP": lambda state: can_green_floating_bumper(world, SONIC, CASINOPARK, state),

        "FlyingAnyandLightDashandPushPullSwitchSonicCP": lambda state: can_fly(world, SONIC, CASINOPARK, state) and can_light_dash(world, SONIC, CASINOPARK, state) and can_switch(world, SONIC, CASINOPARK, state, push_pull=True),

        "FlyingAnyandPushPullSwitchSonicCP": lambda state: can_fly(world, SONIC, CASINOPARK, state) and can_switch(world, SONIC, CASINOPARK, state, push_pull=True),
    }

def create_logic_mapping_dict_bingo_highway_sonic(world: SonicHeroesWorld):
    return \
    {
        #"": lambda state: True,

        #"NOTPOSSIBLE": lambda state: False,

        "BreakKeyCageSonicBH": lambda state: can_break_key_cage(world, SONIC, BINGOHIGHWAY, state),

        "PinballSonicBH": lambda state: can_pinball(world, SONIC, BINGOHIGHWAY, state),

        "(FlyingAnyorKillFlyingEnemyGreenLightning)andSingleSpringSonicBH": lambda state: (can_fly(world, SONIC, BINGOHIGHWAY, state) or can_kill_flying_enemy(world, SONIC, BINGOHIGHWAY, state, green_lightning=True)) and can_single_spring(world, SONIC, BINGOHIGHWAY, state),

        "KillFlyingEnemyYellowLightHomingFireDunkSonicBH": lambda state: can_kill_flying_enemy(world, SONIC, BINGOHIGHWAY, state, yellow_light=True, homing=True, firedunk=True),

        "TeamBlastSonicBH": lambda state: can_team_blast(world, SONIC, BINGOHIGHWAY, state),

        "FanandGlideSonicBH": lambda state: can_fan(world, SONIC, BINGOHIGHWAY, state) and can_glide(world, SONIC, BINGOHIGHWAY, state),

        "FlyingAnySonicBH": lambda state: can_fly(world, SONIC, BINGOHIGHWAY, state),

        "BreakGlassFloorSonicBH": lambda state: can_break_glass_floor(world, SONIC, BINGOHIGHWAY, state),

        "SingleSpringSonicBH": lambda state: can_single_spring(world, SONIC, BINGOHIGHWAY, state),

        "KillFlyingEnemySilverArmorFireDunkSonicBH": lambda state: can_kill_flying_enemy(world, SONIC, BINGOHIGHWAY, state, silver_armor=True, firedunk=True),

        "FloatingDiceandSwitchSonicBH": lambda state: can_floating_dice(world, SONIC, BINGOHIGHWAY, state) and can_switch(world, SONIC, BINGOHIGHWAY, state, regular=True),

        "GongandPinballandSingleSpringSonicBH": lambda state: can_gong(world, SONIC, BINGOHIGHWAY, state) and can_pinball(world, SONIC, BINGOHIGHWAY, state) and can_single_spring(world, SONIC, BINGOHIGHWAY, state),

        "DashRingSonicBH": lambda state: can_dash_ring(world, SONIC, BINGOHIGHWAY, state),

        "FloatingDiceandFlyingAnyandKillFlyingEnemySilverArmorFireDunkandSwitchSonicBH": lambda state: can_floating_dice(world, SONIC, BINGOHIGHWAY, state) and can_fly(world, SONIC, BINGOHIGHWAY, state) and can_kill_flying_enemy(world, SONIC, BINGOHIGHWAY, state, silver_armor=True, firedunk=True) and can_switch(world, SONIC, BINGOHIGHWAY, state, regular=True),

        "FlyingAnyandPulleySonicBH": lambda state: can_fly(world, SONIC, BINGOHIGHWAY, state) and can_pulley(world, SONIC, BINGOHIGHWAY, state),

        "GreenBumperSpringandPinballandSingleSpringSonicBH": lambda state: can_green_floating_bumper(world, SONIC, BINGOHIGHWAY, state) and can_pinball(world, SONIC, BINGOHIGHWAY, state) and can_single_spring(world, SONIC, BINGOHIGHWAY, state),

        "FloatingDiceand(FlyingAnyorGreenBumperSpring)andKillGroundEnemyKlagenSonicBH": lambda state: can_floating_dice(world, SONIC, BINGOHIGHWAY, state) and (can_fly(world, SONIC, BINGOHIGHWAY, state) or can_green_floating_bumper(world, SONIC, BINGOHIGHWAY, state)) and can_kill_ground_enemy(world, SONIC, BINGOHIGHWAY, state, klagen=True),

        "GreenBumperSpringSonicBH": lambda state: can_green_floating_bumper(world, SONIC, BINGOHIGHWAY, state),

        "FloatingDiceorFlyingAnySonicBH": lambda state: can_floating_dice(world, SONIC, BINGOHIGHWAY, state) or can_fly(world, SONIC, BINGOHIGHWAY, state),

        "TripleSpringSonicBH": lambda state: can_triple_spring(world, SONIC, BINGOHIGHWAY, state),

        "KillFlyingEnemySilverArmorFireDunkandSwitchSonicBH": lambda state: can_kill_flying_enemy(world, SONIC, BINGOHIGHWAY, state, silver_armor=True, firedunk=True),

        "KillGroundEnemyPlainShieldKlagenandSwitchSonicBH": lambda state: can_kill_ground_enemy(world, SONIC, BINGOHIGHWAY, state, plainshield=True, klagen=True) and can_switch(world, SONIC, BINGOHIGHWAY, state, regular=True),

        "BreakGlassFloorandPinballSonicBH": lambda state: can_break_glass_floor(world, SONIC, BINGOHIGHWAY, state) and can_pinball(world, SONIC, BINGOHIGHWAY, state),

        "FlyingAnyorStarPanelSonicBH": lambda state: can_fly(world, SONIC, BINGOHIGHWAY, state) or can_star_glass_air_panel(world, SONIC, BINGOHIGHWAY, state),

        "FloatingDiceSonicBH": lambda state: can_floating_dice(world, SONIC, BINGOHIGHWAY, state),

        "((FloatingDiceandSwitch)orWeight)andFlyingAnyandPushPullSwitchSonicBH": lambda state: ((can_floating_dice(world, SONIC, BINGOHIGHWAY, state) and can_switch(world, SONIC, BINGOHIGHWAY, state, regular=True)) or can_weight(world, SONIC, BINGOHIGHWAY, state, regular=True)) and can_fly(world, SONIC, BINGOHIGHWAY, state) and can_switch(world, SONIC, BINGOHIGHWAY, state, push_pull=True),

        "GongSonicBH": lambda state: can_gong(world, SONIC, BINGOHIGHWAY, state),

        "((FloatingDiceandSwitch)orWeight)andFlyingAnySonicBH": lambda state: ((can_floating_dice(world, SONIC, BINGOHIGHWAY, state) and can_switch(world, SONIC, BINGOHIGHWAY, state, regular=True)) or can_weight(world, SONIC, BINGOHIGHWAY, state, regular=True)) and can_fly(world, SONIC, BINGOHIGHWAY, state),

        "FlyingFullorTripleSpringSonicBH": lambda state: can_fly(world, SONIC, BINGOHIGHWAY, state, speedreq=True, powerreq=True) or can_triple_spring(world, SONIC, BINGOHIGHWAY, state),

        "BreakGlassFloorandFloatingDiceand(FlyingAnyor(GreenBumperSpringandSingleSpring))andSwitchSonicBH": lambda state: can_break_glass_floor(world, SONIC, BINGOHIGHWAY, state) and can_floating_dice(world, SONIC, BINGOHIGHWAY, state) and (can_fly(world, SONIC, BINGOHIGHWAY, state) or (can_green_floating_bumper(world, SONIC, BINGOHIGHWAY, state) and can_single_spring(world, SONIC, BINGOHIGHWAY, state))) and can_switch(world, SONIC, BINGOHIGHWAY, state, regular=True),

        "DashRingandSingleSpringSonicBH": lambda state: can_dash_ring(world, SONIC, BINGOHIGHWAY, state) and can_single_spring(world, SONIC, BINGOHIGHWAY, state),

        "DashRingandPinballandSingleSpringSonicBH": lambda state: can_dash_ring(world, SONIC, BINGOHIGHWAY, state) and can_pinball(world, SONIC, BINGOHIGHWAY, state) and can_single_spring(world, SONIC, BINGOHIGHWAY, state),
    }


def create_logic_mapping_dict_rail_canyon_sonic(world: SonicHeroesWorld):
    return \
    {
        #"": lambda state: True,

        #"NOTPOSSIBLE": lambda state: False,

        "BreakKeyCageSonicRC": lambda state: can_break_key_cage(world, SONIC, RAILCANYON, state),

        "RailSonicRC": lambda state: can_rail(world, SONIC, RAILCANYON, state),

        "FlyingAnyorSingleSpringSonicRC": lambda state: can_fly(world, SONIC, RAILCANYON, state) or can_single_spring(world, SONIC, RAILCANYON, state),

        "FlyingAnyorSwitchableRailSonicRC": lambda state: can_fly(world, SONIC, RAILCANYON, state) or can_switchable_rail(world, SONIC, RAILCANYON, state),

        "(BarrelandFlyingAny)orPulleySonicRC": lambda state: (can_barrel(world, SONIC, RAILCANYON, state) and can_fly(world, SONIC, RAILCANYON, state)) or can_pulley(world, SONIC, RAILCANYON, state),

        "3RailPlatformSonicRC": lambda state: can_rail_platform(world, SONIC, RAILCANYON, state),

        "FlyingAnyand3RailPlatformSonicRC": lambda state: can_fly(world, SONIC, RAILCANYON, state) and can_rail_platform(world, SONIC, RAILCANYON, state),

        "RailSwitchSonicRC": lambda state: can_rail_switch(world, SONIC, RAILCANYON, state),

        "FlyingAnyandRailSwitchSonicRC": lambda state: can_fly(world, SONIC, RAILCANYON, state) and can_rail_switch(world, SONIC, RAILCANYON, state),

        "RailSwitchandSwitchableRailSonicRC": lambda state: can_rail_switch(world, SONIC, RAILCANYON, state) and can_switchable_rail(world, SONIC, RAILCANYON, state),

        "FlyingAnySonicRC": lambda state: can_fly(world, SONIC, RAILCANYON, state),

        "RailandSingleSpringSonicRC": lambda state: can_rail(world, SONIC, RAILCANYON, state) and can_single_spring(world, SONIC, RAILCANYON, state),

        "RailandRailSwitchandSwitchableRailSonicRC": lambda state: can_rail(world, SONIC, RAILCANYON, state) and can_rail_switch(world, SONIC, RAILCANYON, state) and can_switchable_rail(world, SONIC, RAILCANYON, state),

        "TripleSpringSonicRC": lambda state: can_triple_spring(world, SONIC, RAILCANYON, state),

        "FlyingAnyandTripleSpringSonicRC": lambda state: can_fly(world, SONIC, RAILCANYON, state) and can_triple_spring(world, SONIC, RAILCANYON, state),

        "PoleSonicRC": lambda state: can_pole(world, SONIC, RAILCANYON, state),

        "RCStationDoorandSwitchSonicRC": lambda state: can_rc_door(world, SONIC, RAILCANYON, state) and can_switch(world, SONIC, RAILCANYON, state, regular=True),

        "RailandSwitchableRailSonicRC": lambda state: can_rail(world, SONIC, RAILCANYON, state) and can_switchable_rail(world, SONIC, RAILCANYON, state),

        "LightDashand3RailPlatformSonicRC": lambda state: can_light_dash(world, SONIC, RAILCANYON, state) and can_rail_platform(world, SONIC, RAILCANYON, state),

        "FlyingAnyor(All3CharsandSwitch)SonicRC": lambda state: can_fly(world, SONIC, RAILCANYON, state) or (has_char(world, SONIC, RAILCANYON, state, speed=True, flying=True, power=True) and can_switch(world, SONIC, RAILCANYON, state, regular=True)),

        "RailandTripleSpringSonicRC": lambda state: can_rail(world, SONIC, RAILCANYON, state) and can_triple_spring(world, SONIC, RAILCANYON, state),

        "KillFlyingEnemyPurpleBombSonicRC": lambda state: can_kill_flying_enemy(world, SONIC, RAILCANYON, state, purple_bombs=True),

        "FlyingAnyorPulleySonicRC": lambda state: can_fly(world, SONIC, RAILCANYON, state) or can_pulley(world, SONIC, RAILCANYON, state),

        "KillGroundEnemyNothingSonicRC": lambda state: can_kill_ground_enemy(world, SONIC, RAILCANYON, state, nothing=True),

        "FlyingAll3CharsandSwitchSonicRC": lambda state: can_fly(world, SONIC, RAILCANYON, state, speedreq=True, powerreq=True) and can_switch(world, SONIC, RAILCANYON, state, regular=True),

        "SingleSpringSonicRC": lambda state: can_single_spring(world, SONIC, RAILCANYON, state),

        "FlyingAnyandSingleSpringSonicRC": lambda state: can_fly(world, SONIC, RAILCANYON, state) and can_single_spring(world, SONIC, RAILCANYON, state),

        "FanandRailandRailSwitchandSwitchableRailand3RailPlatformSonicRC": lambda state: can_fan(world, SONIC, RAILCANYON, state) and can_rail(world, SONIC, RAILCANYON, state) and can_rail_switch(world, SONIC, RAILCANYON, state) and can_switchable_rail(world, SONIC, RAILCANYON, state) and can_rail_platform(world, SONIC, RAILCANYON, state),

        "FanandRailandRailSwitchandSingleSpringandSwitchableRailand3RailPlatformSonicRC": lambda state: can_fan(world, SONIC, RAILCANYON, state) and can_rail(world, SONIC, RAILCANYON, state) and can_rail_switch(world, SONIC, RAILCANYON, state) and can_single_spring(world, SONIC, RAILCANYON, state) and can_switchable_rail(world, SONIC, RAILCANYON, state) and can_rail_platform(world, SONIC, RAILCANYON, state),

        "RailandRailSwitchandSwitchableRailand3RailPlatformSonicRC": lambda state: can_rail(world, SONIC, RAILCANYON, state) and can_rail_switch(world, SONIC, RAILCANYON, state) and can_switchable_rail(world, SONIC, RAILCANYON, state) and can_rail_platform(world, SONIC, RAILCANYON, state),

        "PoleandTargetSwitchSonicRC": lambda state: can_pole(world, SONIC, RAILCANYON, state) and can_target_switch(world, SONIC, RAILCANYON, state),
    }


def create_logic_mapping_dict_bullet_station_sonic(world: SonicHeroesWorld):
    return \
    {
        #"": lambda state: True,

        #"NOTPOSSIBLE": lambda state: False,

        "BreakKeyCageSonicBS": lambda state: can_break_key_cage(world, SONIC, BULLETSTATION, state),

        "RailSonicBS": lambda state: can_rail(world, SONIC, BULLETSTATION, state),

        "TriangleJumpSonicBS": lambda state: can_triangle_jump(world, SONIC, BULLETSTATION, state),

        "FlyingAnyorTriangleJumpSonicBS": lambda state: can_fly(world, SONIC, BULLETSTATION, state) or can_triangle_jump(world, SONIC, BULLETSTATION, state),

        "FlyingAnyorWeightSonicBS": lambda state: can_fly(world, SONIC, BULLETSTATION, state) or can_weight(world, SONIC, BULLETSTATION, state, regular=True),

        "FlyingAnySonicBS": lambda state: can_fly(world, SONIC, BULLETSTATION, state),

        "FireDunkandTPObjSonicBS": lambda state: can_fire_dunk(world, SONIC, BULLETSTATION, state) and can_tp_obj(world, SONIC, BULLETSTATION, state),

        "BreakandEngineCoreSonicBS": lambda state: can_break_things(world, SONIC, BULLETSTATION, state) and can_engine_core(world, SONIC, BULLETSTATION, state),

        "BreakandRailSonicBS": lambda state: can_break_things(world, SONIC, BULLETSTATION, state) and can_rail(world, SONIC, BULLETSTATION, state),

        "SingleSpringandRailSonicBS": lambda state: can_single_spring(world, SONIC, BULLETSTATION, state) and can_rail(world, SONIC, BULLETSTATION, state),

        "CannonSonicBS": lambda state: can_cannon_obj(world, SONIC, BULLETSTATION, state),

        "FlyingAnyandRailSonicBS": lambda state: can_fly(world, SONIC, BULLETSTATION, state) and can_rail(world, SONIC, BULLETSTATION, state),

        "CannonSpeedSonicBS": lambda state: can_cannon(world, SONIC, BULLETSTATION, state, speed=True),

        "CannonFlyingSonicBS": lambda state: can_cannon(world, SONIC, BULLETSTATION, state, flying=True),

        "CannonPowerSonicBS": lambda state: can_cannon(world, SONIC, BULLETSTATION, state, power=True),

        "RailandSingleSpringand3RailPlatformSonicBS": lambda state: can_rail(world, SONIC, BULLETSTATION, state) and can_single_spring(world, SONIC, BULLETSTATION, state) and can_rail_platform(world, SONIC, BULLETSTATION, state),

        "KillGroundEnemyPlainShieldSonicBS": lambda state: can_kill_ground_enemy(world, SONIC, BULLETSTATION, state, plainshield=True),

        "RailandRailSwitchandSwitchableRailSonicBS": lambda state: can_rail(world, SONIC, BULLETSTATION, state) and can_rail_switch(world, SONIC, BULLETSTATION, state) and can_switchable_rail(world, SONIC, BULLETSTATION, state),

        "BreakandSwitchSonicBS": lambda state: can_break_things(world, SONIC, BULLETSTATION, state) and can_switch(world, SONIC, BULLETSTATION, state, regular=True),

        "SingleSpringSonicBS": lambda state: can_single_spring(world, SONIC, BULLETSTATION, state),

        "FanorRailSonicBS": lambda state: can_fan(world, SONIC, BULLETSTATION, state) or can_rail(world, SONIC, BULLETSTATION, state),

        "PoleSonicBS": lambda state: can_pole(world, SONIC, BULLETSTATION, state),

        "All3CharsandSwitchSonicBS": lambda state: has_char(world, SONIC, BULLETSTATION, state, speed=True, flying=True, power=True) and can_switch(world, SONIC, BULLETSTATION, state, regular=True),

        "FireDunkSonicBS": lambda state: can_fire_dunk(world, SONIC, BULLETSTATION, state),

        "CannonFlyingandDashRingSonicBS": lambda state: can_cannon_flying(world, SONIC, BULLETSTATION, state) and can_dash_ring(world, SONIC, BULLETSTATION, state),

        "BreakSonicBS": lambda state: can_break_things(world, SONIC, BULLETSTATION, state),

        "All3CharsandBreakandSwitchSonicBS": lambda state: has_char(world, SONIC, BULLETSTATION, state, speed=True, flying=True, power=True) and can_break_things(world, SONIC, BULLETSTATION, state) and can_switch(world, SONIC, BULLETSTATION, state, regular=True),

        "BigCannonGunSonicBS": lambda state: can_big_gun_interior(world, SONIC, BULLETSTATION, state),

        "RailandRailSwitchandSwitchableRailand3RailPlatformSonicBS": lambda state: can_rail(world, SONIC, BULLETSTATION, state) and can_rail_switch(world, SONIC, BULLETSTATION, state) and can_switchable_rail(world, SONIC, BULLETSTATION, state) and can_rail_platform(world, SONIC, BULLETSTATION, state),

        "FanSonicBS": lambda state: can_fan(world, SONIC, BULLETSTATION, state),

        "FlyingAnyand3RailPlatformSonicBS": lambda state: can_fly(world, SONIC, BULLETSTATION, state),

        "LightDashSonicBS": lambda state: can_light_dash(world, SONIC, BULLETSTATION, state),

        "FlyingAnyandSwitchSonicBS": lambda state: can_fly(world, SONIC, BULLETSTATION, state) and can_switch(world, SONIC, BULLETSTATION, state, regular=True),

        "FlyingAnyorPulleySonicBS": lambda state: can_fly(world, SONIC, BULLETSTATION, state) or can_pulley(world, SONIC, BULLETSTATION, state),

        "RailandRailSwitchandSingleSpringandSwitchableRailand3RailPlatformSonicBS": lambda state: can_rail(world, SONIC, BULLETSTATION, state) and can_rail_switch(world, SONIC, BULLETSTATION, state) and can_single_spring(world, SONIC, BULLETSTATION, state) and can_switchable_rail(world, SONIC, BULLETSTATION, state) and can_rail_platform(world, SONIC, BULLETSTATION, state),

        "KillGroundEnemyKlagenSonicBS": lambda state: can_kill_ground_enemy(world, SONIC, BULLETSTATION, state, klagen=True),

        "FlyingAll3CharsandSwitchSonicBS": lambda state: can_fly(world, SONIC, BULLETSTATION, state, speedreq=True, powerreq=True) and can_switch(world, SONIC, BULLETSTATION, state, regular=True),

        "FlyingAnyorTripleSpringSonicBS": lambda state: can_fly(world, SONIC, BULLETSTATION, state) or can_triple_spring(world, SONIC, BULLETSTATION, state),

        "FlyingAnyorGlideorHomingSonicBS": lambda state: can_fly(world, SONIC, BULLETSTATION, state) or can_glide(world, SONIC, BULLETSTATION, state) or can_homing_attack(world, SONIC, BULLETSTATION, state),

        "BobsledandRailSwitchandSwitchableRailandSingleSpringSonicBS": lambda state: can_bobsled(world, SONIC, BULLETSTATION, state) and can_rail_switch(world, SONIC, BULLETSTATION, state) and can_switchable_rail(world, SONIC, BULLETSTATION, state) and can_single_spring(world, SONIC, BULLETSTATION, state),
    }


def create_logic_mapping_dict_frog_forest_sonic(world: SonicHeroesWorld):
    return \
    {
        #"": lambda state: True,

        #"NOTPOSSIBLE": lambda state: False,

        "BreakKeyCageSonicFrog": lambda state: can_break_key_cage(world, SONIC, FROGFOREST, state),

        "BouncyFruitorFlyingAnySonicFrog": lambda state: can_bouncy_fruit(world, SONIC, FROGFOREST, state) or can_fly(world, SONIC, FROGFOREST, state),

        "DashPanelSonicFrog": lambda state: can_dash_panel(world, SONIC, FROGFOREST, state),

        "GreenFrogSonicFrog": lambda state: can_green_frog(world, SONIC, FROGFOREST, state),

        "TallTreePlatformSonicFrog": lambda state: can_tall_tree_platforms(world, SONIC, FROGFOREST, state),

        "YellowPlatformSonicFrog": lambda state: can_large_yellow_platform(world, SONIC, FROGFOREST, state),

        "DashRingandFlyingAnySonicFrog": lambda state: can_dash_ring(world, SONIC, FROGFOREST, state) and can_fly(world, SONIC, FROGFOREST, state),

        "SwingingVineSonicFrog": lambda state: can_swinging_vine(world, SONIC, FROGFOREST, state),

        "SmallBouncyMushroomSonicFrog": lambda state: can_small_bouncy_mushroom(world, SONIC, FROGFOREST, state),

        "(All3CharsandDashRing)orFlyingAnySonicFrog": lambda state: (has_char(world, SONIC, FROGFOREST, state, speed=True, flying=True, power=True)) or can_fly(world, SONIC, FROGFOREST, state),

        "FlyingAnySonicFrog": lambda state: can_fly(world, SONIC, FROGFOREST, state),

        "FlyingAnyorGlideorHomingSonicFrog": lambda state: can_fly(world, SONIC, FROGFOREST, state) or can_glide(world, SONIC, FROGFOREST, state) or can_homing_attack(world, SONIC, FROGFOREST, state),

        "FlyingAnyandSmallGreenPlatformSonicFrog": lambda state: can_fly(world, SONIC, FROGFOREST, state) and can_small_green_rain_platform(world, SONIC, FROGFOREST, state),

        "FlyingAnyorLargeBouncyMushroomSonicFrog": lambda state: can_fly(world, SONIC, FROGFOREST, state) or can_large_bouncy_mushroom(world, SONIC, FROGFOREST, state),

        "LargeBouncyMushroomSonicFrog": lambda state: can_large_bouncy_mushroom(world, SONIC, FROGFOREST, state),

        "FlyingAnyorPowerGongSonicFrog": lambda state: can_fly(world, SONIC, FROGFOREST, state) or can_gong(world, SONIC, FROGFOREST, state),

        "DashPanelandDashRingandFlyingAnySonicFrog": lambda state: can_dash_panel(world, SONIC, FROGFOREST, state) and can_dash_ring(world, SONIC, FROGFOREST, state) and can_fly(world, SONIC, FROGFOREST, state),

        "DashPanelandYellowPlatformSonicFrog": lambda state: can_dash_panel(world, SONIC, FROGFOREST, state) and can_large_yellow_platform(world, SONIC, FROGFOREST, state),

        "(DashRingorFlyingAny)andSmallGreenPlatformandTripleSpringSonicFrog": lambda state: (can_dash_ring(world, SONIC, FROGFOREST, state) or can_fly(world, SONIC, FROGFOREST, state)) and can_small_green_rain_platform(world, SONIC, FROGFOREST, state),

        "FlyingAnyandGreenPlatformSonicFrog": lambda state: can_fly(world, SONIC, FROGFOREST, state) and can_small_green_rain_platform(world, SONIC, FROGFOREST, state),

        "TripleSpringSonicFrog": lambda state: can_triple_spring(world, SONIC, FROGFOREST, state),

        "(FlyingAnyorGlideorHoming)andYellowPlatformSonicFrog": lambda state: (can_fly(world, SONIC, FROGFOREST, state) or can_glide(world, SONIC, FROGFOREST, state) or can_homing_attack(world, SONIC, FROGFOREST, state)) and can_large_yellow_platform(world, SONIC, FROGFOREST, state),

        "FlyingAnyandLargeBouncyMushroomSonicFrog": lambda state: can_fly(world, SONIC, FROGFOREST, state) and can_large_bouncy_mushroom(world, SONIC, FROGFOREST, state),

        "LightDashandTargetSwitchandThundershootSonicFrog": lambda state: can_light_dash(world, SONIC, FROGFOREST, state) and can_target_switch(world, SONIC, FROGFOREST, state) and can_thundershoot_both(world, SONIC, FROGFOREST, state),

        "LightDashSonicFrog": lambda state: can_light_dash(world, SONIC, FROGFOREST, state),

        "BreakSonicFrog": lambda state: can_break_things(world, SONIC, FROGFOREST, state),

        "KillGroundEnemySpearPlainShieldSonicFrog": lambda state: can_kill_ground_enemy(world, SONIC, FROGFOREST, state, spear=True, plainshield=True),

        "LargeBouncyMushroomandPowerGongSonicFrog": lambda state: can_large_bouncy_mushroom(world, SONIC, FROGFOREST, state) and can_gong(world, SONIC, FROGFOREST, state),

        "PropellerSonicFrog": lambda state: can_propeller(world, SONIC, FROGFOREST, state),

        "DashRamporFlyingAnySonicFrog": lambda state: can_dash_ramp(world, SONIC, FROGFOREST, state) or can_fly(world, SONIC, FROGFOREST, state),

        "FlyingAnyandTallTreePlatformSonicFrog": lambda state: can_fly(world, SONIC, FROGFOREST, state) and can_tall_tree_platforms(world, SONIC, FROGFOREST, state),

        "(FlyingAnyorGlideorHoming)andSmallGreenPlatformSonicFrog": lambda state: (can_fly(world, SONIC, FROGFOREST, state) or can_glide(world, SONIC, FROGFOREST, state) or can_homing_attack(world, SONIC, FROGFOREST, state)) and can_small_green_rain_platform(world, SONIC, FROGFOREST, state),

        "BouncyFruitandFlyingAnySonicFrog": lambda state: can_bouncy_fruit(world, SONIC, FROGFOREST, state) and can_fly(world, SONIC, FROGFOREST, state),

        "FlyingAnyandSwingingVineSonicFrog": lambda state: can_fly(world, SONIC, FROGFOREST, state) and can_swinging_vine(world, SONIC, FROGFOREST, state),

        "FireDunkSonicFrog": lambda state: can_fire_dunk(world, SONIC, FROGFOREST, state),

        "SingleSpringandSwingingVineSonicFrog": lambda state: can_single_spring(world, SONIC, FROGFOREST, state) and can_swinging_vine(world, SONIC, FROGFOREST, state),

        "KillGroundEnemyCameronSonicFrog": lambda state: can_kill_ground_enemy(world, SONIC, FROGFOREST, state, nothing=True, cameron=True),

        "BouncyFruitandSwingingVineSonicFrog": lambda state: can_bouncy_fruit(world, SONIC, FROGFOREST, state) and can_swinging_vine(world, SONIC, FROGFOREST, state),

        "FlyingOneCharorLightDashSonicFrog": lambda state: can_fly(world, SONIC, FROGFOREST, state, speedreq=True, powerreq=True, orcondition=True) or can_light_dash(world, SONIC, FROGFOREST, state),

        "FlyingOneCharSonicFrog": lambda state: can_fly(world, SONIC, FROGFOREST, state, speedreq=True, powerreq=True, orcondition=True),

        "BouncyFruitandSingleSpringSonicFrog": lambda state: can_bouncy_fruit(world, SONIC, FROGFOREST, state) and can_single_spring(world, SONIC, FROGFOREST, state),

        "BouncyFruitSonicFrog": lambda state: can_bouncy_fruit(world, SONIC, FROGFOREST, state),
    }


def create_logic_mapping_dict_lost_jungle_sonic(world: SonicHeroesWorld):
    return \
    {
        #"": lambda state: True,

        #"NOTPOSSIBLE": lambda state: False,

        "BreakKeyCageSonicLJ": lambda state: can_break_key_cage(world, SONIC, LOSTJUNGLE, state),

        #world, SONIC, LOSTJUNGLE, state
        "KillGroundEnemyEggHammerSonicLJ": lambda state: can_kill_ground_enemy(world, SONIC, LOSTJUNGLE, state, egghammer=True),

        "LargeBouncyMushroomandSwingingVineSonicLJ": lambda state: can_large_bouncy_mushroom(world, SONIC, LOSTJUNGLE, state) and can_swinging_vine(world, SONIC, LOSTJUNGLE, state),

        "FlyingAnyorTornadoorTripleSpringSonicLJ": lambda state: can_fly(world, SONIC, LOSTJUNGLE, state) or can_tornado(world, SONIC, LOSTJUNGLE, state) or can_triple_spring(world, SONIC, LOSTJUNGLE, state),

        "FlyingAnyorTornadoSonicLJ": lambda state: can_fly(world, SONIC, LOSTJUNGLE, state) or can_tornado(world, SONIC, LOSTJUNGLE, state),

        "SingleSpringSonicLJ": lambda state: can_single_spring(world, SONIC, LOSTJUNGLE, state),

        "(FlyingAnyorTornado)andSmallGreenPlatformSonicLJ": lambda state: (can_fly(world, SONIC, LOSTJUNGLE, state) or can_tornado(world, SONIC, LOSTJUNGLE, state)) and can_small_green_rain_platform(world, SONIC, LOSTJUNGLE, state),

        "SmallGreenPlatformSonicLJ": lambda state: can_small_green_rain_platform(world, SONIC, LOSTJUNGLE, state),

        "Flying3CharsorSwingingVineSonicLJ": lambda state: can_fly(world, SONIC, LOSTJUNGLE, state, speedreq=True, powerreq=True) or can_swinging_vine(world, SONIC, LOSTJUNGLE, state),

        "BouncyFruitSonicLJ": lambda state: can_bouncy_fruit(world, SONIC, LOSTJUNGLE, state),

        "FlyingAnySonicLJ": lambda state: can_fly(world, SONIC, LOSTJUNGLE, state),

        "SwingingVineSonicLJ": lambda state: can_swinging_vine(world, SONIC, LOSTJUNGLE, state),

        "SmallGreenPlatformandSwingingVineSonicLJ": lambda state: can_small_green_rain_platform(world, SONIC, LOSTJUNGLE, state) and can_swinging_vine(world, SONIC, LOSTJUNGLE, state),

        "GreenFrogSonicLJ": lambda state: can_green_frog(world, SONIC, LOSTJUNGLE, state),

        "DashRampSonicLJ": lambda state: can_dash_ramp(world, SONIC, LOSTJUNGLE, state),

        "FlyingAnyorSingleSpringSonicLJ": lambda state: can_fly(world, SONIC, LOSTJUNGLE, state) or can_single_spring(world, SONIC, LOSTJUNGLE, state),

        "PropellerSonicLJ": lambda state: can_propeller(world, SONIC, LOSTJUNGLE, state),

        "KillFlyingEnemyPurpleBombSonicLJ": lambda state: can_kill_flying_enemy(world, SONIC, LOSTJUNGLE, state, purple_bombs=True),

        "LargeBouncyMushroomSonicLJ": lambda state: can_large_bouncy_mushroom(world, SONIC, LOSTJUNGLE, state),

        "FlyingOneCharSonicLJ": lambda state: can_fly(world, SONIC, LOSTJUNGLE, state, speedreq=True, powerreq=True, orcondition=True),

        "SmallBouncyMushroomandSwingingVineSonicLJ": lambda state: can_small_bouncy_mushroom(world, SONIC, LOSTJUNGLE, state) and can_swinging_vine(world, SONIC, LOSTJUNGLE, state),

        "TripleSpringSonicLJ": lambda state: can_triple_spring(world, SONIC, LOSTJUNGLE, state),

        "FlyingAnyorLargeBouncyMushroomSonicLJ": lambda state: can_fly(world, SONIC, LOSTJUNGLE, state) or can_large_bouncy_mushroom(world, SONIC, LOSTJUNGLE, state),

        "FlyingAnyandSmallBouncyMushroomSonicLJ": lambda state: can_fly(world, SONIC, LOSTJUNGLE, state) and can_small_bouncy_mushroom(world, SONIC, LOSTJUNGLE, state),

        "BouncyFruitandHoming2SonicLJ": lambda state: can_bouncy_fruit(world, SONIC, LOSTJUNGLE, state) and can_homing_attack(world, SONIC, LOSTJUNGLE, state) and has_char_levelup(world, SONIC, LOSTJUNGLE, state, levelup=2, speed=True),

        "FlyingAnyandSmallGreenPlatformSonicLJ": lambda state: can_fly(world, SONIC, LOSTJUNGLE, state) and can_small_green_rain_platform(world, SONIC, LOSTJUNGLE, state),

        "DashRingandFlyingAnySonicLJ": lambda state: can_dash_ring(world, SONIC, LOSTJUNGLE, state) and can_fly(world, SONIC, LOSTJUNGLE, state),

        "BouncyFruitandSingleSpringSonicLJ": lambda state: can_bouncy_fruit(world, SONIC, LOSTJUNGLE, state) and can_single_spring(world, SONIC, LOSTJUNGLE, state),

        "KillFlyingEnemyGreenShotSonicLJ": lambda state: can_kill_flying_enemy(world, SONIC, LOSTJUNGLE, state, green_shot=True),

        "(FlyingAnyorTornado)andTallTreePlatformSonicLJ": lambda state: (can_fly(world, SONIC, LOSTJUNGLE, state) or can_tornado(world, SONIC, LOSTJUNGLE, state)) and can_tall_tree_platforms(world, SONIC, LOSTJUNGLE, state),

        "BouncyFruitorFlyingAnyorHomingSonicLJ": lambda state: can_bouncy_fruit(world, SONIC, LOSTJUNGLE, state) or can_fly(world, SONIC, LOSTJUNGLE, state) or can_homing_attack(world, SONIC, LOSTJUNGLE, state),

        "KillGroundEnemyKlagenSonicLJ": lambda state: can_kill_ground_enemy(world, SONIC, LOSTJUNGLE, state, nothing=True, klagen=True),

        "LightDashandSwitchSonicLJ": lambda state: can_light_dash(world, SONIC, LOSTJUNGLE, state) and can_switch(world, SONIC, LOSTJUNGLE, state, regular=True),

        "LargeYellowPlatformandSingleSpringandSwingingVineSonicLJ": lambda state: can_large_yellow_platform(world, SONIC, LOSTJUNGLE, state) and can_single_spring(world, SONIC, LOSTJUNGLE, state) and can_swinging_vine(world, SONIC, LOSTJUNGLE, state),

        "SmallBouncyMushroomSonicLJ": lambda state: can_small_bouncy_mushroom(world, SONIC, LOSTJUNGLE, state),
    }


def create_logic_mapping_dict_hang_castle_sonic(world: SonicHeroesWorld):
    return \
    {
        #"": lambda state: True,

        #"NOTPOSSIBLE": lambda state: False,

        "BreakKeyCageSonicHC": lambda state: can_break_key_cage(world, SONIC, HANGCASTLE, state),

        "KillGroundEnemyNothingSonicHC": lambda state: can_kill_ground_enemy(world, SONIC, HANGCASTLE, state, nothing=True),

        "TPSwitchSonicHC": lambda state: can_tp_switch(world, SONIC, HANGCASTLE, state),

        "FlyingAnyorTornadoSonicHC": lambda state: can_fly(world, SONIC, HANGCASTLE, state) or can_tornado(world, SONIC, HANGCASTLE, state),

        "LightDashSonicHC": lambda state: can_light_dash(world, SONIC, HANGCASTLE, state),

        "FlyingAnySonicHC": lambda state: can_fly(world, SONIC, HANGCASTLE, state),

        "BreakandSwitchSonicHC": lambda state: can_break_things(world, SONIC, HANGCASTLE, state) and can_switch(world, SONIC, HANGCASTLE, state, regular=True),

        "TripleSpringSonicHC": lambda state: can_triple_spring(world, SONIC, HANGCASTLE, state),

        "BreakInGroundWoodContainerSonicHC": lambda state: can_break_in_ground_wood_container(world, SONIC, HANGCASTLE, state),

        "FlameTorchSonicHC": lambda state: can_flame_torch(world, SONIC, HANGCASTLE, state),

        "KillFlyingEnemySilverArmorSonicHC": lambda state: can_kill_flying_enemy(world, SONIC, HANGCASTLE, state, silver_armor=True),

        "LightDashandSwitchSonicHC": lambda state: can_light_dash(world, SONIC, HANGCASTLE, state) and can_switch(world, SONIC, HANGCASTLE, state, regular=True),

        "CastleFloatingPlatformSonicHC": lambda state: can_castle_floating_platform(world, SONIC, HANGCASTLE, state),

        "BreakSonicHC": lambda state: can_break_things(world, SONIC, HANGCASTLE, state),

        "GongandSingleSpringSonicHC": lambda state: can_gong(world, SONIC, HANGCASTLE, state) and can_single_spring(world, SONIC, HANGCASTLE, state),

        "DashRampandTPSwitchSonicHC": lambda state: can_dash_ramp(world, SONIC, HANGCASTLE, state) and can_tp_switch(world, SONIC, HANGCASTLE, state),

        "CastleFloatingPlatformorFlyingAnySonicHC": lambda state: can_castle_floating_platform(world, SONIC, HANGCASTLE, state) or can_fly(world, SONIC, HANGCASTLE, state),

        "CastleFloatingPlatformandFlyingAnySonicHC": lambda state: can_castle_floating_platform(world, SONIC, HANGCASTLE, state) and can_fly(world, SONIC, HANGCASTLE, state),

        "KillGroundEnemySpearConcreteShieldBishopSonicHC": lambda state: can_kill_ground_enemy(world, SONIC, HANGCASTLE, state, spear=True, concreteshield=True, eggbishop=True),

        "FlyingOneCharandPushPullSwitchSonicHC": lambda state: can_fly(world, SONIC, HANGCASTLE, state, speedreq=True, powerreq=True, orcondition=True) and can_switch(world, SONIC, HANGCASTLE, state, push_pull=True),

        "KillGroundEnemyBishopSonicHC": lambda state: can_kill_ground_enemy(world, SONIC, HANGCASTLE, state, eggbishop=True),

        "KillGroundEnemySpearSonicHC": lambda state: can_kill_ground_enemy(world, SONIC, HANGCASTLE, state, spear=True),

        "FlyingOneCharandLightDashandPushPullSwitchSonicHC": lambda state: can_fly(world, SONIC, HANGCASTLE, state, speedreq=True, powerreq=True, orcondition=True),

        "TargetSwitchandThundershootSonicHC": lambda state: can_switch(world, SONIC, HANGCASTLE, state, target=True) and can_thundershoot_both(world, SONIC, HANGCASTLE, state),

        "PoleandTargetSwitchandThundershootSonicHC": lambda state: can_pole(world, SONIC, HANGCASTLE, state) and can_switch(world, SONIC, HANGCASTLE, state, target=True) and can_thundershoot_both(world, SONIC, HANGCASTLE, state),

        "DashRampSonicHC": lambda state: can_dash_ramp(world, SONIC, HANGCASTLE, state),
    }


def create_logic_mapping_dict_mystic_mansion_sonic(world: SonicHeroesWorld):
    return \
    {
        #"": lambda state: True,

        #"NOTPOSSIBLE": lambda state: False,

        "BreakKeyCageSonicMM": lambda state: can_break_key_cage(world, SONIC, MYSTICMANSION, state),

        #world, SONIC, MYSTICMANSION, state
        "SwitchSonicMM": lambda state: can_switch(world, SONIC, MYSTICMANSION, state, regular=True),

        "KillGroundEnemySpearSonicMM": lambda state: can_kill_ground_enemy(world, SONIC, MYSTICMANSION, state, spear=True),

        "BreakInGroundIronContainerSonicMM": lambda state: can_break_in_ground_iron_container(world, SONIC, MYSTICMANSION, state),

        "TPSwitchSonicMM": lambda state: can_tp_switch(world, SONIC, MYSTICMANSION, state),

        "FlyingAnyandWeightSonicMM": lambda state: can_fly(world, SONIC, MYSTICMANSION, state) and can_weight(world, SONIC, MYSTICMANSION, state, regular=True),

        "KillGroundEnemySpearSpikeShieldEggHammerSonicMM": lambda state: can_kill_ground_enemy(world, SONIC, MYSTICMANSION, state, spear=True, spikeshield=True, egghammer=True),

        "FlyingAnyorTornadoSonicMM": lambda state: can_fly(world, SONIC, MYSTICMANSION, state) or can_tornado(world, SONIC, MYSTICMANSION, state),

        "BobsledSonicMM": lambda state: can_bobsled(world, SONIC, MYSTICMANSION, state),

        "KillGroundEnemySpearSpikeShieldSonicMM": lambda state: can_kill_ground_enemy(world, SONIC, MYSTICMANSION, state, spear=True, spikeshield=True),

        "Flying3CharsSonicMM": lambda state: can_fly(world, SONIC, MYSTICMANSION, state, speedreq=True, powerreq=True),

        "FlyingAnySonicMM": lambda state: can_fly(world, SONIC, MYSTICMANSION, state),

        "PulleySonicMM": lambda state: can_pulley(world, SONIC, MYSTICMANSION, state),

        "BreakSonicMM": lambda state: can_break_things(world, SONIC, MYSTICMANSION, state),

        "BreakandFanandSwitchSonicMM": lambda state: can_break_things(world, SONIC, MYSTICMANSION, state) and can_fan(world, SONIC, MYSTICMANSION, state) and can_switch(world, SONIC, MYSTICMANSION, state, regular=True),

        "FlyingAnyorSingleSpringSonicMM": lambda state: can_fly(world, SONIC, MYSTICMANSION, state) or can_single_spring(world, SONIC, MYSTICMANSION, state),

        "FlyingOneCharandPushPullSwitchSonicMM": lambda state: can_fly(world, SONIC, MYSTICMANSION, state, speedreq=True, powerreq=True, orcondition=True),

        "KillGroundEnemyHeavyEggHammerSonicMM": lambda state: can_kill_ground_enemy(world, SONIC, MYSTICMANSION, state, heavyegghammer=True),

        "FlyingAnyandMansionFloatingPlatformSonicMM": lambda state: can_fly(world, SONIC, MYSTICMANSION, state) and can_mansion_floating_platform(world, SONIC, MYSTICMANSION, state),

        "KillGroundEnemySpearBishopSonicMM": lambda state: can_kill_ground_enemy(world, SONIC, MYSTICMANSION, state, spear=True, eggbishop=True),

        "TriangleJumpSonicMM": lambda state: can_triangle_jump(world, SONIC, MYSTICMANSION, state),

        "(FlyingAnyorTornado)andWeightSonicMM": lambda state: (can_fly(world, SONIC, MYSTICMANSION, state) or can_tornado(world, SONIC, MYSTICMANSION, state)) and can_weight(world, SONIC, MYSTICMANSION, state, regular=True),

        "All3CharsandSwitchandThundershootSonicMM": lambda state: has_char(world, SONIC, MYSTICMANSION, state, speed=True, flying=True, power=True) and can_switch(world, SONIC, MYSTICMANSION, state, regular=True) and can_thundershoot_both(world, SONIC, MYSTICMANSION, state),

        "FanandFlying3CharsandHomingandKillGroundEnemyBishopHeavyEggHammerandTPSwitchSonicMM": lambda state: can_fan(world, SONIC, MYSTICMANSION, state) and can_fly(world, SONIC, MYSTICMANSION, state, speedreq=True, powerreq=True) and can_homing_attack(world, SONIC, MYSTICMANSION, state) and can_kill_ground_enemy(world, SONIC, MYSTICMANSION, state, eggbishop=True, heavyegghammer=True) and can_tp_switch(world, SONIC, MYSTICMANSION, state),
    }


def create_logic_mapping_dict_egg_fleet_sonic(world: SonicHeroesWorld):
    return \
    {
        #"": lambda state: True,

        #"NOTPOSSIBLE": lambda state: False,

        "BreakKeyCageSonicEF": lambda state: can_break_key_cage(world, SONIC, EGGFLEET, state),

        "KillGroundEnemyNothingSonicEF": lambda state: can_kill_ground_enemy(world, SONIC, EGGFLEET, state, nothing=True),

        "PoleSonicEF": lambda state: can_pole(world, SONIC, EGGFLEET, state),

        "TripleSpringSonicEF": lambda state: can_triple_spring(world, SONIC, EGGFLEET, state),

        "FlyingAnySonicEF": lambda state: can_fly(world, SONIC, EGGFLEET, state),

        "CannonSonicEF": lambda state: can_cannon_obj(world, SONIC, EGGFLEET, state),

        "CannonSpeedSonicEF": lambda state: can_cannon(world, SONIC, EGGFLEET, state, speed=True),

        "CannonFlyingSonicEF": lambda state: can_cannon(world, SONIC, EGGFLEET, state, flying=True),

        "DashRingSonicEF": lambda state: can_dash_ring(world, SONIC, EGGFLEET, state),

        "CannonPowerSonicEF": lambda state: can_cannon(world, SONIC, EGGFLEET, state, power=True),

        "DashRingandFlyingAnySonicEF": lambda state: can_dash_ring(world, SONIC, EGGFLEET, state) and can_fly(world, SONIC, EGGFLEET, state),

        "FanSonicEF": lambda state: can_fan(world, SONIC, EGGFLEET, state),

        "KillGroundEnemyCannonandSingleSpringSonicEF": lambda state: can_kill_ground_enemy(world, SONIC, EGGFLEET, state, cannon=True) and can_single_spring(world, SONIC, EGGFLEET, state),

        "FlyingAnyorTripleSpringSonicEF": lambda state: can_fly(world, SONIC, EGGFLEET, state) or can_triple_spring(world, SONIC, EGGFLEET, state),

        "SquareFloatingPlatformSonicEF": lambda state: can_square_floating_platform(world, SONIC, EGGFLEET, state),

        "SquareFloatingPlatformandTripleSpringSonicEF": lambda state: can_square_floating_platform(world, SONIC, EGGFLEET, state),

        "FlyingAnyandSquareFloatingPlatformSonicEF": lambda state: can_fly(world, SONIC, EGGFLEET, state) and can_square_floating_platform(world, SONIC, EGGFLEET, state),

        "FlyingAnyorLightDashSonicEF": lambda state: can_fly(world, SONIC, EGGFLEET, state) or can_light_dash(world, SONIC, EGGFLEET, state),

        "KillGroundEnemyE2000SonicEF": lambda state: can_kill_ground_enemy(world, SONIC, EGGFLEET, state, e2000=True),

        "PropellerSonicEF": lambda state: can_propeller(world, SONIC, EGGFLEET, state),

        "FlyingAnyor(KillGroundEnemyCannonandSingleSpring)SonicEF": lambda state: can_fly(world, SONIC, EGGFLEET, state) or (can_kill_ground_enemy(world, SONIC, EGGFLEET, state, cannon=True) and can_single_spring(world, SONIC, EGGFLEET, state)),

        "FanorFlyingAnySonicEF": lambda state: can_fan(world, SONIC, EGGFLEET, state) or can_fly(world, SONIC, EGGFLEET, state),

        "FlyingAnyor(KillGroundEnemyCannonandTripleSpring)SonicEF": lambda state: can_fly(world, SONIC, EGGFLEET, state) or (can_kill_ground_enemy(world, SONIC, EGGFLEET, state, cannon=True) and can_triple_spring(world, SONIC, EGGFLEET, state)),

        "FlyingAnyorPoleSonicEF": lambda state: can_fly(world, SONIC, EGGFLEET, state) or can_pole(world, SONIC, EGGFLEET, state),

        "RocketAccelSonicEF": lambda state: can_rocket_accel(world, SONIC, EGGFLEET, state),

        "FlyingAnyandFloatingSquarePlatformandRainbowRingsSonicEF": lambda state: can_fly(world, SONIC, EGGFLEET, state) and can_square_floating_platform(world, SONIC, EGGFLEET, state) and can_rainbow_hoops(world, SONIC, EGGFLEET, state),

        "LightDashSonicEF": lambda state: can_light_dash(world, SONIC, EGGFLEET, state),

        "FanandTripleSpringSonicEF": lambda state: can_fan(world, SONIC, EGGFLEET, state) and can_triple_spring(world, SONIC, EGGFLEET, state),

        "KillGroundEnemyPlainShieldE2000SonicEF": lambda state: can_kill_ground_enemy(world, SONIC, EGGFLEET, state, plainshield=True, e2000=True),

        "FanandSwitchSonicEF": lambda state: can_fan(world, SONIC, EGGFLEET, state) and can_switch(world, SONIC, EGGFLEET, state, regular=True),

        "DashRampSonicEF": lambda state: can_dash_ramp(world, SONIC, EGGFLEET, state),

        "Flying3CharsSonicEF": lambda state: can_fly(world, SONIC, EGGFLEET, state, speedreq=True, powerreq=True),

        "KillGroundEnemyCannonandPoleandSwitchSonicEF": lambda state: can_kill_ground_enemy(world, SONIC, EGGFLEET, state, cannon=True) and can_pole(world, SONIC, EGGFLEET, state) and can_switch(world, SONIC, EGGFLEET, state, regular=True),

        "KillGroundEnemySpikeShieldSonicEF": lambda state: can_kill_ground_enemy(world, SONIC, EGGFLEET, state, spikeshield=True),

        "SingleSpringSonicEF": lambda state: can_single_spring(world, SONIC, EGGFLEET, state),
    }


def create_logic_mapping_dict_final_fortress_sonic(world: SonicHeroesWorld):
    return \
    {
        #"": lambda state: True,

        #"NOTPOSSIBLE": lambda state: False,

        "BreakKeyCageSonicFinal": lambda state: can_break_key_cage(world, SONIC, FINALFORTRESS, state),

        "FlyingAnySonicFinal": lambda state: can_fly(world, SONIC, FINALFORTRESS, state),

        "FallingPlatformand(FlyingAnyorTornadoHoverorTripleSpring)SonicFinal": lambda state: can_falling_platform(world, SONIC, FINALFORTRESS, state) and (can_fly(world, SONIC, FINALFORTRESS, state) or can_tornado_hover(world, SONIC, FINALFORTRESS, state) or can_triple_spring(world, SONIC, FINALFORTRESS, state)),

        "(FlyingAnyorHomingorTornadoHover)andTripleSpringSonicFinal": lambda state: (can_fly(world, SONIC, FINALFORTRESS, state) or can_tornado_hover(world, SONIC, FINALFORTRESS, state)) and can_triple_spring(world, SONIC, FINALFORTRESS, state),

        "FallingPlatformSonicFinal": lambda state: can_falling_platform(world, SONIC, FINALFORTRESS, state),

        "FallingPlatformand(FlyingAnyorLightDash)SonicFinal": lambda state: can_falling_platform(world, SONIC, FINALFORTRESS, state) and (can_fly(world, SONIC, FINALFORTRESS, state) or can_light_dash(world, SONIC, FINALFORTRESS, state)),

        "SquareFloatingPlatformSonicFinal": lambda state: can_square_floating_platform(world, SONIC, FINALFORTRESS, state),

        "FlyingAnyorGlideorSpeedCharorTripleSpringSonicFinal": lambda state: can_fly(world, SONIC, FINALFORTRESS, state) or can_glide(world, SONIC, FINALFORTRESS, state) or has_char(world, SONIC, FINALFORTRESS, state, speed=True) or can_triple_spring(world, SONIC, FINALFORTRESS, state),

        "(DashRamporFlyingAny)andFallingPlatformSonicFinal": lambda state: (can_dash_ramp(world, SONIC, FINALFORTRESS, state) or can_fly(world, SONIC, FINALFORTRESS, state)) and can_falling_platform(world, SONIC, FINALFORTRESS, state),

        "FallingPlatformandSqaureFloatingPlatformSonicFinal": lambda state: can_falling_platform(world, SONIC, FINALFORTRESS, state) and can_square_floating_platform(world, SONIC, FINALFORTRESS, state),

        "(FlyingAnyorTornadoHover)andSquareFloatingPlatformSonicFinal": lambda state: (can_fly(world, SONIC, FINALFORTRESS, state) or can_tornado_hover(world, SONIC, FINALFORTRESS, state)) and can_square_floating_platform(world, SONIC, FINALFORTRESS, state),

        "DashRingSonicFinal": lambda state: can_dash_ring(world, SONIC, FINALFORTRESS, state),

        "KillGroundEnemyEggHammerSonicFinal": lambda state: can_kill_ground_enemy(world, SONIC, FINALFORTRESS, state, egghammer=True),

        "BreakSonicFinal": lambda state: can_break_things(world, SONIC, FINALFORTRESS, state),

        "FlyingAnyorTornadoHoverSonicFinal": lambda state: can_fly(world, SONIC, FINALFORTRESS, state) or can_tornado_hover(world, SONIC, FINALFORTRESS, state),

        "FallingPlatformandLightDashSonicFinal": lambda state: can_falling_platform(world, SONIC, FINALFORTRESS, state) and can_light_dash(world, SONIC, FINALFORTRESS, state),

        "FlyingAnyandFallingPlatformandKillGroundEnemyCannonandSingleSpringSonicFinal": lambda state: can_fly(world, SONIC, FINALFORTRESS, state) and can_falling_platform(world, SONIC, FINALFORTRESS, state) and can_kill_ground_enemy(world, SONIC, FINALFORTRESS, state, cannon=True) and can_single_spring(world, SONIC, FINALFORTRESS, state),

        "KillGroundEnemyCannonandSingleSpringSonicFinal": lambda state: can_kill_ground_enemy(world, SONIC, FINALFORTRESS, state, cannon=True) and can_single_spring(world, SONIC, FINALFORTRESS, state),

        "FallingPlatformand((FlyingAnyandItemBalloon)orFlyingOneChar)SonicFinal": lambda state: can_falling_platform(world, SONIC, FINALFORTRESS, state and ((can_fly(world, SONIC, FINALFORTRESS, state) and can_item_balloon(world, SONIC, FINALFORTRESS, state)) or can_fly(world, SONIC, FINALFORTRESS, state, speedreq=True, powerreq=True, orcondition=True))),
        "FlyingAnyandFallingPlatformSonicFinal": lambda state: can_fly(world, SONIC, FINALFORTRESS, state) and can_falling_platform(world, SONIC, FINALFORTRESS, state),

        "FallingPlatformandTriangleJumpSonicFinal": lambda state: can_falling_platform(world, SONIC, FINALFORTRESS, state) and can_triangle_jump(world, SONIC, FINALFORTRESS, state),

        "(BreakandSingleSpring)orFlying3CharsSonicFinal": lambda state: (can_break_things(world, SONIC, FINALFORTRESS, state) and can_single_spring(world, SONIC, FINALFORTRESS, state)) or can_fly(world, SONIC, FINALFORTRESS, state, speedreq=True, powerreq=True),

        "TriangleJumpSonicFinal": lambda state: can_triangle_jump(world, SONIC, FINALFORTRESS, state),

        "BreakandDashPanelSonicFinal": lambda state: can_break_things(world, SONIC, FINALFORTRESS, state) and can_dash_panel(world, SONIC, FINALFORTRESS, state),

        "KillGroundEnemyHeavyEggHammerSonicFinal": lambda state: can_kill_ground_enemy(world, SONIC, FINALFORTRESS, state, heavyegghammer=True),

        "PoleandRegularSwitchSonicFinal": lambda state: can_pole(world, SONIC, FINALFORTRESS, state) and can_switch(world, SONIC, FINALFORTRESS, state, regular=True),

        "PoleSonicFinal": lambda state: can_pole(world, SONIC, FINALFORTRESS, state),

        "PoleAirSonicFinal": lambda state: can_pole(world, SONIC, FINALFORTRESS, state, air=True),

        "(FlyingAnyorTornadoHover)andWeightSonicFinal": lambda state: (can_fly(world, SONIC, FINALFORTRESS, state) or can_tornado_hover(world, SONIC, FINALFORTRESS, state)) and can_weight(world, SONIC, FINALFORTRESS, state, regular=True),

        "FireDunkSonicFinal": lambda state: can_fire_dunk(world, SONIC, FINALFORTRESS, state),

        "(BreakorFlyingAnyorTornadoHover)andSingleSpringSonicFinal": lambda state: (can_break_things(world, SONIC, FINALFORTRESS, state) or can_fly(world, SONIC, FINALFORTRESS, state) or can_tornado_hover(world, SONIC, FINALFORTRESS, state)) and can_single_spring(world, SONIC, FINALFORTRESS, state),

        "KillGroundEnemyPlainShieldSonicFinal": lambda state: can_kill_ground_enemy(world, SONIC, FINALFORTRESS, state, plainshield=True),

        "SingleSpringSonicFinal": lambda state: can_single_spring(world, SONIC, FINALFORTRESS, state),

        "(FlyingAnyorTornadoHover)andPoleAirSonicFinal": lambda state: (can_fly(world, SONIC, FINALFORTRESS, state) or can_tornado(world, SONIC, FINALFORTRESS, state)) and can_pole(world, SONIC, FINALFORTRESS, state, air=True),

        "TriangleJumpandTripleSpringSonicFinal": lambda state: can_triangle_jump(world, SONIC, FINALFORTRESS, state) and can_triple_spring(world, SONIC, FINALFORTRESS, state),

        "KillGroundEnemyE2000RSonicFinal": lambda state: can_kill_ground_enemy(world, SONIC, FINALFORTRESS, state, e2000r=True),

        "SelfDestructSwitchSonicFinal": lambda state: can_self_destruct_tp_switch(world, SONIC, FINALFORTRESS, state),

        "FanandFlyingAnyandTargetSwitchandThunderShootSonicFinal": lambda state: can_fan(world, SONIC, FINALFORTRESS, state) and can_fly(world, SONIC, FINALFORTRESS, state) and can_switch(world, SONIC, FINALFORTRESS, state, target=True) and can_thundershoot_both(world, SONIC, FINALFORTRESS, state),

        "FanSonicFinal": lambda state: can_fan(world, SONIC, FINALFORTRESS, state),

        "FlyingAnyandPulleySonicFinal": lambda state: can_fly(world, SONIC, FINALFORTRESS, state) and can_pulley(world, SONIC, FINALFORTRESS, state),

        "PoleAirandSwitchSonicFinal": lambda state: can_pole(world, SONIC, FINALFORTRESS, state, air=True) and can_switch(world, SONIC, FINALFORTRESS, state, regular=True),

        "LightDashSonicFinal": lambda state: can_light_dash(world, SONIC, FINALFORTRESS, state),

        "All3CharsandFanandKillGroundEnemyCannonSonicFinal": lambda state: can_fly(world, SONIC, FINALFORTRESS, state, speedreq=True, powerreq=True) and can_fan(world, SONIC, FINALFORTRESS, state) and can_kill_ground_enemy(world, SONIC, FINALFORTRESS, state, cannon=True),

        "FanandFlyingAnyandPushPullSwitchSonicFinal": lambda state: can_fan(world, SONIC, FINALFORTRESS, state) and can_fly(world, SONIC, FINALFORTRESS, state) and can_switch(world, SONIC, FINALFORTRESS, state, push_pull=True),

        "GongSonicFinal": lambda state: can_gong(world, SONIC, FINALFORTRESS, state),

        "FlyingAnyorGlideorHomingSonicFinal": lambda state: can_fly(world, SONIC, FINALFORTRESS, state) or can_glide(world, SONIC, FINALFORTRESS, state) or can_homing_attack(world, SONIC, FINALFORTRESS, state),

        "KillGroundEnemyEggHammerandTargetSwitchandThunderShootSonicFinal": lambda state: can_kill_ground_enemy(world, SONIC, FINALFORTRESS, state, egghammer=True) and can_switch(world, SONIC, FINALFORTRESS, state, target=True) and can_thundershoot_both(world, SONIC, FINALFORTRESS, state),

        "KillGroundEnemyEggHammerHeavyEggHammerSonicFinal": lambda state: can_kill_ground_enemy(world, SONIC, FINALFORTRESS, state, egghammer=True, heavyegghammer=True),

        "FlyingAnyorTornadoHoverorTripleSpringSonicFinal": lambda state: can_fly(world, SONIC, FINALFORTRESS, state) or can_tornado_hover(world, SONIC, FINALFORTRESS, state) or can_triple_spring(world, SONIC, FINALFORTRESS, state),
    }


"""
def create_logic_mapping_dict_placeholder_sonic(world: SonicHeroesWorld):
    return \
    {
        #"": lambda state: True,
        #"NOTPOSSIBLE": lambda state: False,
    }
"""










