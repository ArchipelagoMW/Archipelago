from enum import Enum
from BaseClasses import CollectionState
from .data.RoomNames import RoomName
from .Items import (
    ProgressiveUpgrade,
    SuitUpgrade,
    get_item_for_options,
    get_progressive_upgrade_for_item,
)
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from . import MetroidPrimeWorld


class CombatLogicDifficulty(Enum):
    NO_LOGIC = -1
    NORMAL = 0
    MINIMAL = 1


class Logic:
    def __init__(self, world: "MetroidPrimeWorld"):
        self.can_power_bomb: Callable[["MetroidPrimeWorld", CollectionState], bool] = (
            self._can_main_power_bomb
            if world.options.main_power_bomb
            else self._can_power_bomb
        )

        self.can_missile: Callable[
            ["MetroidPrimeWorld", CollectionState, int], bool
        ] = (
            self._can_missile_launcher
            if world.options.missile_launcher
            else self._can_missile
        )

    def _can_power_bomb(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return state.has_all(
            [SuitUpgrade.Power_Bomb_Expansion.value, SuitUpgrade.Morph_Ball.value],
            world.player,
        )

    def _can_main_power_bomb(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return state.has_all(
            [SuitUpgrade.Morph_Ball.value, SuitUpgrade.Main_Power_Bomb.value],
            world.player,
        )

    def has_required_artifact_count(
        self, world: "MetroidPrimeWorld", state: CollectionState, required_count: int
    ) -> bool:
        return state.has_group("Artifacts", world.player, required_count)

    def can_boost(self, world: "MetroidPrimeWorld", state: CollectionState) -> bool:
        return state.has_all(
            [SuitUpgrade.Morph_Ball.value, SuitUpgrade.Boost_Ball.value], world.player
        )

    def can_bomb(self, world: "MetroidPrimeWorld", state: CollectionState) -> bool:
        return state.has_all(
            [SuitUpgrade.Morph_Ball.value, SuitUpgrade.Morph_Ball_Bomb.value],
            world.player,
        )

    def can_power_beam(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return state.has_any(
            [
                SuitUpgrade.Power_Beam.value,
                ProgressiveUpgrade.Progressive_Power_Beam.value,
            ],
            world.player,
        )

    def can_spider(self, world: "MetroidPrimeWorld", state: CollectionState) -> bool:
        return state.has_all(
            [SuitUpgrade.Spider_Ball.value, SuitUpgrade.Morph_Ball.value], world.player
        )

    def _can_missile_launcher(
        self,
        world: "MetroidPrimeWorld",
        state: CollectionState,
        num_expansions: int = 1,
    ) -> bool:
        can_shoot = state.has(SuitUpgrade.Missile_Launcher.value, world.player)
        return can_shoot and (
            num_expansions <= 1
            or state.has(
                SuitUpgrade.Missile_Expansion.value,
                world.player,
                num_expansions - 1,
            )
        )

    def _can_missile(
        self,
        world: "MetroidPrimeWorld",
        state: CollectionState,
        num_expansions: int = 1,
    ) -> bool:
        return state.has(
            SuitUpgrade.Missile_Expansion.value, world.player, num_expansions
        )

    def can_super_missile(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return (
            self.can_power_beam(world, state)
            and self.can_missile(world, state, 1)
            and (
                state.has_all(
                    [SuitUpgrade.Charge_Beam.value, SuitUpgrade.Super_Missile.value],
                    world.player,
                )
                or state.has(
                    ProgressiveUpgrade.Progressive_Power_Beam.value, world.player, 3
                )
            )
        )

    def can_wave_beam(self, world: "MetroidPrimeWorld", state: CollectionState) -> bool:
        return state.has_any(
            [
                SuitUpgrade.Wave_Beam.value,
                ProgressiveUpgrade.Progressive_Wave_Beam.value,
            ],
            world.player,
        )

    def can_ice_beam(self, world: "MetroidPrimeWorld", state: CollectionState) -> bool:
        return state.has_any(
            [SuitUpgrade.Ice_Beam.value, ProgressiveUpgrade.Progressive_Ice_Beam.value],
            world.player,
        )

    def can_plasma_beam(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return state.has_any(
            [
                SuitUpgrade.Plasma_Beam.value,
                ProgressiveUpgrade.Progressive_Plasma_Beam.value,
            ],
            world.player,
        )

    can_melt_ice = can_plasma_beam

    def can_grapple(self, world: "MetroidPrimeWorld", state: CollectionState) -> bool:
        return state.has(SuitUpgrade.Grapple_Beam.value, world.player)

    def can_space_jump(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return state.has(SuitUpgrade.Space_Jump_Boots.value, world.player)

    def can_morph_ball(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return state.has(SuitUpgrade.Morph_Ball.value, world.player)

    def can_xray(
        self,
        world: "MetroidPrimeWorld",
        state: CollectionState,
        usually_required: bool = False,
        hard_required: bool = False,
    ) -> bool:
        if hard_required:
            return state.has(SuitUpgrade.X_Ray_Visor.value, world.player)
        if (
            usually_required
            and world.options.remove_xray_requirements == "remove_all_but_omega_pirate"
        ):
            return True
        if usually_required:
            return state.has(SuitUpgrade.X_Ray_Visor.value, world.player)
        return bool(world.options.remove_xray_requirements.value) or state.has(
            SuitUpgrade.X_Ray_Visor.value, world.player
        )

    def can_thermal(
        self,
        world: "MetroidPrimeWorld",
        state: CollectionState,
        usually_required: bool = False,
        hard_required: bool = False,
    ) -> bool:
        if hard_required:
            return state.has(SuitUpgrade.Thermal_Visor.value, world.player)
        if (
            usually_required
            and world.options.remove_thermal_requirements == "remove_all"
        ):
            return True
        if usually_required:
            return state.has(SuitUpgrade.Thermal_Visor.value, world.player)
        return bool(world.options.remove_thermal_requirements.value) or state.has(
            SuitUpgrade.Thermal_Visor.value, world.player
        )

    def can_move_underwater(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return state.has(SuitUpgrade.Gravity_Suit.value, world.player)

    def can_charge_beam(
        self,
        world: "MetroidPrimeWorld",
        state: CollectionState,
        required_beam: Optional[SuitUpgrade] = None,
    ) -> bool:
        if required_beam is not None:
            progressive_item = get_progressive_upgrade_for_item(required_beam)
            assert progressive_item is not None
            return state.has_all(
                [SuitUpgrade.Charge_Beam.value, required_beam.value], world.player
            ) or state.has(progressive_item.value, world.player, 2)

        # If no beam is required, just check for Charge Beam or 2 of any progressive beam upgrade
        return state.has(
            SuitUpgrade.Charge_Beam.value, world.player
        ) or state.has_any_count(
            {upgrade.value: 2 for upgrade in ProgressiveUpgrade}, world.player
        )

    def can_beam_combo(
        self,
        world: "MetroidPrimeWorld",
        state: CollectionState,
        required_beam: SuitUpgrade,
    ) -> bool:
        if not self.can_missile(world, state, 2) or not self.can_charge_beam(
            world, state, required_beam
        ):
            return False

        if required_beam == SuitUpgrade.Wave_Beam:
            return self.can_missile(world, state, 3) and (
                state.has(SuitUpgrade.Wavebuster.value, world.player)
                or state.has(
                    ProgressiveUpgrade.Progressive_Wave_Beam.value, world.player, 3
                )
            )
        elif required_beam == SuitUpgrade.Ice_Beam:
            return state.has(SuitUpgrade.Ice_Spreader.value, world.player) or state.has(
                ProgressiveUpgrade.Progressive_Ice_Beam.value, world.player, 3
            )
        elif required_beam == SuitUpgrade.Plasma_Beam:
            return self.can_missile(world, state, 3) and (
                state.has(SuitUpgrade.Flamethrower.value, world.player)
                or state.has(
                    ProgressiveUpgrade.Progressive_Plasma_Beam.value, world.player, 3
                )
            )
        else:
            raise ValueError(f"Invalid required beam: {required_beam}")

    def can_scan(self, world: "MetroidPrimeWorld", state: CollectionState) -> bool:
        return state.has(SuitUpgrade.Scan_Visor.value, world.player)

    def can_heat(self, world: "MetroidPrimeWorld", state: CollectionState) -> bool:
        if world.options.non_varia_heat_damage:
            return state.has(SuitUpgrade.Varia_Suit.value, world.player)
        else:
            return state.has_any(
                [
                    SuitUpgrade.Varia_Suit.value,
                    SuitUpgrade.Phazon_Suit.value,
                    SuitUpgrade.Gravity_Suit.value,
                ],
                world.player,
            )

    def can_phazon(self, world: "MetroidPrimeWorld", state: CollectionState) -> bool:
        return state.has(SuitUpgrade.Phazon_Suit.value, world.player)

    def has_energy_tanks(
        self, world: "MetroidPrimeWorld", state: CollectionState, count: int
    ) -> bool:
        return state.has(SuitUpgrade.Energy_Tank.value, world.player, count)

    def can_infinite_speed(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return self.can_boost(world, state) and self.can_bomb(world, state)

    def can_defeat_sheegoth(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return (
            self.can_bomb(world, state)
            or self.can_missile(world, state, 1)
            or self.can_power_bomb(world, state)
            or self.can_plasma_beam(world, state)
        )

    def can_backwards_lower_mines(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return bool(world.options.backwards_lower_mines.value)

    def has_power_bomb_count(
        self, world: "MetroidPrimeWorld", state: CollectionState, required_count: int
    ) -> bool:
        count = state.count(SuitUpgrade.Power_Bomb_Expansion.value, world.player)
        if state.has(SuitUpgrade.Main_Power_Bomb.value, world.player):
            count += 4
        return count >= required_count

    def can_warp_to_start(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        SAVE_ROOMS = [
            RoomName.Landing_Site.value,
            RoomName.Save_Station_1.value,
            RoomName.Save_Station_2.value,
            RoomName.Save_Station_3.value,
            RoomName.Save_Station_Magmoor_A.value,
            RoomName.Save_Station_Magmoor_B.value,
            RoomName.Save_Station_A.value,
            RoomName.Save_Station_B.value,
            RoomName.Save_Station_C.value,
            RoomName.Save_Station_D.value,
            RoomName.Cargo_Freight_Lift_to_Deck_Gamma.value,
            RoomName.Save_Station_Mines_A.value,
            RoomName.Save_Station_Mines_B.value,
            RoomName.Save_Station_Mines_C.value,
        ]
        for room in SAVE_ROOMS:
            if state.can_reach_region(room, world.player):
                return True
        return False

    def _can_combat_generic(
        self,
        world: "MetroidPrimeWorld",
        state: CollectionState,
        normal_tanks: int,
        minimal_tanks: int,
        requires_charge_beam: bool = True,
    ) -> bool:
        difficulty = CombatLogicDifficulty(world.options.combat_logic_difficulty)
        if difficulty == CombatLogicDifficulty.NO_LOGIC:
            return True
        elif difficulty == CombatLogicDifficulty.NORMAL:
            return self.has_energy_tanks(world, state, normal_tanks) and (
                self.can_charge_beam(world, state) or not requires_charge_beam
            )
        elif difficulty == CombatLogicDifficulty.MINIMAL:
            return self.has_energy_tanks(world, state, minimal_tanks) and (
                self.can_charge_beam(world, state) or not requires_charge_beam
            )
        return True

    def can_combat_mines(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return self._can_combat_generic(world, state, 5, 3)

    def can_combat_labs(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return world.starting_room_name in [
            RoomName.East_Tower.value,
            RoomName.Save_Station_B.value,
            RoomName.Quarantine_Monitor.value,
        ] or self._can_combat_generic(world, state, 1, 0, False)

    def can_combat_thardus(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        """Require charge and plasma or power for thardus on normal"""
        if world.starting_room_name in [
            RoomName.Quarantine_Monitor.value,
            RoomName.Save_Station_B.value,
        ]:
            return (
                self.can_plasma_beam(world, state)
                or self.can_power_beam(world, state)
                or self.can_wave_beam(world, state)
            )
        difficulty = world.options.combat_logic_difficulty.value
        if difficulty == CombatLogicDifficulty.NO_LOGIC.value:
            return True
        elif difficulty == CombatLogicDifficulty.NORMAL.value:
            return self.has_energy_tanks(world, state, 3) and (
                self.can_charge_beam(world, state)
                and (
                    self.can_plasma_beam(world, state)
                    or self.can_power_beam(world, state)
                )
            )
        elif difficulty == CombatLogicDifficulty.MINIMAL.value:
            return (
                self.can_plasma_beam(world, state)
                or self.can_power_beam(world, state)
                or self.can_wave_beam(world, state)
            )
        return True

    def can_combat_omega_pirate(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return self._can_combat_generic(world, state, 6, 3) and self.can_xray(
            world, state, True
        )

    def can_combat_flaahgra(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return (
            world.starting_room_name == RoomName.Sunchamber_Lobby.value
            or self._can_combat_generic(world, state, 2, 1, False)
        )

    def can_combat_ridley(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return self._can_combat_generic(world, state, 8, 8)

    def can_combat_prime(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        return self._can_combat_generic(world, state, 8, 5)

    def can_combat_ghosts(
        self, world: "MetroidPrimeWorld", state: CollectionState
    ) -> bool:
        difficulty = world.options.combat_logic_difficulty.value
        if difficulty == CombatLogicDifficulty.NO_LOGIC.value:
            return True
        elif difficulty == CombatLogicDifficulty.NORMAL.value:
            return (
                self.can_charge_beam(world, state, SuitUpgrade.Power_Beam)
                and self.can_power_beam(world, state)
                and self.can_xray(world, state, True)
            )
        elif difficulty == CombatLogicDifficulty.MINIMAL.value:
            return self.can_power_beam(world, state)
        return True

    def can_combat_beam_pirates(
        self, world: "MetroidPrimeWorld", state: CollectionState, beam_type: SuitUpgrade
    ) -> bool:
        if world.options.combat_logic_difficulty.value in [
            CombatLogicDifficulty.NO_LOGIC.value,
            CombatLogicDifficulty.MINIMAL.value,
        ]:
            return True
        return state.has(get_item_for_options(world, beam_type).value, world.player)
