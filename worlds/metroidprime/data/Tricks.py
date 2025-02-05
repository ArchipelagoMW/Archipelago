from dataclasses import dataclass
from enum import Enum
from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState
from ..data.RoomNames import RoomName
from ..Items import SuitUpgrade

if TYPE_CHECKING:
    from .. import MetroidPrimeWorld


class TrickDifficulty(Enum):
    No_Tricks = -1
    Easy = 0
    Medium = 1
    Hard = 2


@dataclass
class TrickInfo:
    name: str
    description: str
    difficulty: TrickDifficulty
    rule_func: Callable[["MetroidPrimeWorld", CollectionState], bool]


class Tricks:
    def __init__(self, world: "MetroidPrimeWorld"):
        self.logic = world.logic

        # Tallon
        self.alcove_escape: TrickInfo = TrickInfo(
            "Alcove Escape",
            "Escape the Alcove without space jump",
            TrickDifficulty.Easy,
            lambda world, state: True,
        )
        self.landing_site_scan_dash: TrickInfo = TrickInfo(
            "Landing Site Scan Dash",
            "Perform a scan dash to reach the landing site without bombs",
            TrickDifficulty.Easy,
            self.logic.can_scan,
        )

        self.frigate_no_gravity: TrickInfo = TrickInfo(
            "Frigate No Gravity",
            "Complete the Frigate without Gravity Suit",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_space_jump(world, state)
            and self.logic.can_wave_beam(world, state)
            and self.logic.can_thermal(world, state),
        )

        self.hydro_access_tunnel_no_gravity: TrickInfo = TrickInfo(
            "Hydro Access Tunnel No Gravity",
            "Complete the Hydro Access Tunnel without Gravity Suit using Wall Boosting",
            TrickDifficulty.Hard,
            lambda world, state: self.logic.can_boost(world, state),
        )

        self.frigate_backwards_no_gravity: TrickInfo = TrickInfo(
            "Frigate No Gravity",
            "Complete the Frigate without Gravity Suit",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_morph_ball(world, state)
            and self.logic.can_space_jump(world, state)
            and self.logic.can_boost(world, state),
        )

        self.frigate_crash_site_scan_dash: TrickInfo = TrickInfo(
            "Crashed Frigate Scan Dash",
            "Perform a scan dash to reach the item at Crashed Frigate",
            TrickDifficulty.Hard,
            self.logic.can_scan,
        )

        self.frigate_crash_site_slope_jump: TrickInfo = TrickInfo(
            "Crashed Frigate Slope Jump",
            "Perform a slope jump to reach the item at Crashed Frigate",
            TrickDifficulty.Easy,
            self.logic.can_space_jump,
        )
        self.frigate_crash_site_slope_jump_no_sjb: TrickInfo = TrickInfo(
            "Crashed Frigate Slope Jump No Space Jump",
            "Perform a slope jump to reach the item at Crashed Frigate",
            TrickDifficulty.Medium,
            lambda world, state: True,
        )

        self.frigate_crash_site_climb_to_overgrown_cavern: TrickInfo = TrickInfo(
            "Crashed Frigate Climb to Overgrown Cavern",
            "Climb to Overgrown Cavern",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_space_jump(world, state),
        )
        self.great_tree_hall_skip_bars: TrickInfo = TrickInfo(
            "Great Tree Hall Skip Bars",
            "Skip the bars in Great Tree Hall using Morph Ball Bombs",
            TrickDifficulty.Hard,
            self.logic.can_bomb,
        )

        self.great_tree_chamber_no_xray: TrickInfo = TrickInfo(
            "Great Tree Chamber No XRay",
            "Reach the Great Tree Chamber without XRay Visor",
            TrickDifficulty.Easy,
            self.logic.can_space_jump,
        )
        self.great_tree_chamber_nsj_no_xray: TrickInfo = TrickInfo(
            "Great Tree Chamber no Space Jump no XRay",
            "Reach the Great Tree Chamber without Space Jump or XRay Visor",
            TrickDifficulty.Medium,
            self.logic.can_bomb,
        )

        self.great_tree_hall_no_spider_ball: TrickInfo = TrickInfo(
            "Great Tree Hall No Spider Ball",
            "Reach the door to the Life Grove Tunnel without Spider Ball",
            TrickDifficulty.Easy,
            self.logic.can_space_jump,
        )

        self.root_cave_arbor_chamber_no_grapple_xray: TrickInfo = TrickInfo(
            "Root Cave Arbor Chamber No Grapple XRay",
            "Reach the Arbor Chamber without Grapple Beam or XRay Visor using a Combat Dash",
            TrickDifficulty.Hard,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_scan(world, state),
        )
        # Chozo
        self.vault_via_plaza: TrickInfo = TrickInfo(
            "Vault Via Plaza",
            "Reach the Vault via the Main Plaza using an L Jump",
            TrickDifficulty.Easy,
            self.logic.can_space_jump,
        )
        self.plaza_half_pipe_no_boost: TrickInfo = TrickInfo(
            "Plaza Half Pipe No Boost",
            "Reach the Half Pipe in the Main Plaza using a slope jump",
            TrickDifficulty.Easy,
            self.logic.can_space_jump,
        )
        self.plaza_half_pipe_morph_only: TrickInfo = TrickInfo(
            "Plaza Half Pipe with only Morph Ball",
            "Roll down the half pipe from the opposite side to gain enough speed to reach the ledge",
            TrickDifficulty.Hard,
            self.logic.can_morph_ball,
        )
        self.plaza_grapple_ledge_r_jump: TrickInfo = TrickInfo(
            "Plaza Grapple Ledge R Jump",
            "Reach the Grapple Ledge in the Main Plaza using an R Jump",
            TrickDifficulty.Easy,
            self.logic.can_space_jump,
        )
        self.plaza_grapple_ledge_tree_grapple: TrickInfo = TrickInfo(
            "Plaza Grapple Ledge Tree Grapple",
            "Reach the Grapple Ledge in the Main Plaza by L jumping to the tree and then grappling to the ledge",
            TrickDifficulty.Easy,
            self.logic.can_grapple,
        )

        self.ruined_shrine_upper_door_no_spider_ball: TrickInfo = TrickInfo(
            "Ruined Shrine Upper Door L Jump",
            "Reach the upper door in the Ruined Shrine by L Jumping off the root",
            TrickDifficulty.Easy,
            self.logic.can_space_jump,
        )
        self.ruined_shrine_upper_door_scan_dash: TrickInfo = TrickInfo(
            "Ruined Shrine Upper Door Scan Dash",
            "Reach the upper door in the Ruined Shrine by scan dashing without space jump",
            TrickDifficulty.Hard,
            self.logic.can_scan,
        )
        self.ruined_shrine_scan_dash_escape: TrickInfo = TrickInfo(
            "Ruined Shrine Scan Dash Escape",
            "Escape the Ruined Shrine by scan dashing  off the branches",
            TrickDifficulty.Easy,
            self.logic.can_scan,
        )

        self.tower_of_light_climb_without_missiles: TrickInfo = TrickInfo(
            "Tower of Light Climb Without Missiles",
            "Tower of Light can be climbed by dashing to the outside edges, skipping the 40 missile requirement.",
            TrickDifficulty.Easy,
            rule_func=lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_scan(world, state),
        )
        self.tower_of_light_climb_nsj: TrickInfo = TrickInfo(
            "Tower of Light Climb No Space Jump",
            "Climb Tower of Light through a series of double bomb jumps",
            TrickDifficulty.Hard,
            rule_func=lambda world, state: (
                self.logic.can_missile(world, state, 1)
                and state.has(SuitUpgrade.Missile_Expansion.value, world.player, 8)
            )
            and self.logic.can_bomb(world, state),
        )
        self.tower_chamber_no_gravity: TrickInfo = TrickInfo(
            "Tower Chamber No Gravity",
            "Reach the Tower Chamber without Gravity Suit by using a slope jump",
            TrickDifficulty.Easy,
            self.logic.can_space_jump,
        )
        self.tower_chamber_no_space_jump: TrickInfo = TrickInfo(
            "Tower Chamber No Space Jump",
            "Reach the Tower Chamber without Space Jump by using a double bomb jump",
            TrickDifficulty.Easy,
            rule_func=lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_move_underwater(world, state),
        )

        self.ruined_nursery_no_bombs: TrickInfo = TrickInfo(
            "Ruined Nursery No Bombs",
            "Reach the Ruined Nursery Item by space jumping and morphing near the item",
            TrickDifficulty.Hard,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_morph_ball(world, state),
        )

        self.magma_pool_scan_dash: TrickInfo = TrickInfo(
            "Cross Magma Pool Suitless",
            "Cross magma pool using a scan dash on the crate items",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_scan(world, state),
        )
        self.magma_pool_debris_jump: TrickInfo = TrickInfo(
            "Cross Magma Pool With SJB and Gravity",
            "Use the space jump boots to jump off debris to cross the pool",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_move_underwater(world, state)
            and self.logic.has_energy_tanks(world, state, 2),
        )
        self.magma_pool_item_debris_jump: TrickInfo = TrickInfo(
            "Magma Pool Debris Jump",
            "Use the space jump boots to jump off debris to cross the pool",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_move_underwater(world, state)
            and self.logic.has_energy_tanks(world, state, 2)
            and self.logic.can_power_bomb(world, state),
        )
        self.magma_pool_item_scan_dash: TrickInfo = TrickInfo(
            "Magma Pool Item No Grapple",
            "Use the scan dash and a power bomb to get the item in the magma pool",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_scan(world, state)
            and self.logic.can_power_bomb(world, state),
        )
        self.magma_pool_item_infinite_speed: TrickInfo = TrickInfo(
            "Magma Pool Item Infinite Speed",
            "Use infinite speed to get the item in the magma pool. Stay in morph ball and navigate to a save station or elevator afterward",
            TrickDifficulty.Medium,
            rule_func=lambda world, state: self.logic.can_infinite_speed(world, state)
            and self.logic.can_bomb(world, state),
        )

        self.arboretum_scan_gate_skip: TrickInfo = TrickInfo(
            "Arboretum Scan Gate Skip",
            "Skip the gate in the Arboretum by double bomb jumping",
            TrickDifficulty.Easy,
            self.logic.can_bomb,
        )

        self.gathering_hall_without_space_jump: TrickInfo = TrickInfo(
            "Gathering Hall Without Space Jump",
            "Double bomb jump from the side platform to the grate where the item is",
            TrickDifficulty.Easy,
            self.logic.can_bomb,
        )

        self.watery_hall_no_gravity: TrickInfo = TrickInfo(
            "Watery Hall No Gravity",
            "Reach the Watery Hall Underwater Item without Gravity Suit by using a slope jump",
            TrickDifficulty.Easy,
            self.logic.can_space_jump,
        )
        self.watery_hall_no_gravity_no_space_jump: TrickInfo = TrickInfo(
            "Watery Hall No Gravity No Space Jump",
            "Reach the Watery Hall Underwater Item without Gravity Suit or Space Jump by using a slope jump or bomb jump",
            TrickDifficulty.Medium,
            lambda world, state: True,
        )

        self.furnace_no_spider_ball = TrickInfo(
            "Furnace No Spider Ball",
            "Reach the Item inside the Furnace without Spider Ball by jumping on the side of the spider track",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_bomb(world, state),
        )
        self.furnace_spider_track_hbj = TrickInfo(
            "Furnace Spider Track HBJ",
            "Reach the first track in furnace with a hyper bomb jump",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_spider(world, state),
        )
        self.furnace_spider_track_sj_bombs = TrickInfo(
            "Furnace Spider Track SJ Bombs",
            "You can climb the Furnace and its spider tracks using Space Jump, reach the top of the room, then bomb jump across to the item.",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_space_jump(world, state),
        )

        self.crossway_item_fewer_reqs = TrickInfo(
            "Crossway Item Fewer Reqs",
            "Reach the crossway item using only SJB and Morph Ball by jumping along the pegs on the wall.",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_morph_ball(world, state)
            and self.logic.can_space_jump(world, state),
        )
        self.crossway_hpbj = TrickInfo(
            "Crossway Half pipe bomb jump",
            "Reach Hall of the Elders using a half pipe bomb jump",
            TrickDifficulty.Hard,
            lambda world, state: self.logic.can_bomb(world, state),
        )

        self.hall_of_elders_bomb_slots_no_spider = TrickInfo(
            "Hall of Elders No Spider Ball",
            "Reach the bomb slots without the spider ball by jumping on a peg to activate the top bomb slot",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_bomb(world, state)
            and self.logic.can_power_beam(world, state)
            and self.logic.can_combat_ghosts(world, state),
        )
        self.hall_of_elders_reflecting_pool_no_spider = TrickInfo(
            "Hall of Elders Reflecting Pool No Spider Ball",
            "Reach the reflecting pool without the spider ball",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_wave_beam(world, state)
            and self.logic.can_bomb(world, state)
            and self.logic.can_power_beam(world, state)
            and self.logic.can_combat_ghosts(world, state),
        )
        self.hall_of_elders_reflecting_pool_no_wave_beam = TrickInfo(
            "Hall of Elders Reflecting Pool No Wave Beam",
            "In Hall of the Elders, you can Hyper Bomb Jump (HBJ) to the morph ball track and reach the door to Reflecting Pool Access.",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_bomb(world, state)
            and self.logic.can_power_beam(world, state)
            and self.logic.can_combat_ghosts(world, state),
        )

        self.hall_of_elders_elder_chamber_no_spider = TrickInfo(
            "Hall of Elders Elder Chamber No Spider Ball",
            "Reach the bomb slots without the spider ball by jumping on a peg to activate the top bomb slot",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_plasma_beam(world, state)
            and self.logic.can_space_jump(world, state)
            and self.logic.can_power_beam(world, state)
            and self.logic.can_combat_ghosts(world, state),
        )
        self.hall_of_elders_item_no_spider = TrickInfo(
            "Hall of Elders Item No Spider Ball",
            "Reach the bomb slots without the spider ball by jumping on a peg to activate the top bomb slot",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_ice_beam(world, state)
            and self.logic.can_space_jump(world, state)
            and self.logic.can_power_beam(world, state)
            and self.logic.can_combat_ghosts(world, state),
        )

        self.reflecting_pool_space_jump_climb = TrickInfo(
            "Reflecting Pool Space Jump Climb",
            "Climb the reflecting pool by space jumping off a stone toad",
            TrickDifficulty.Easy,
            self.logic.can_space_jump,
        )
        self.reflecting_pool_nsj_climb: TrickInfo = TrickInfo(
            "Reflecting Pool No Space Jump Climb",
            "Perform an HBJ, UBJ, or BSJ off a stone toad",
            TrickDifficulty.Hard,
            self.logic.can_bomb,
        )

        # Magmoor

        self.lava_lake_item_suitless = TrickInfo(
            "Lava Lake Item Suitless",
            "Reach the Lava Lake item without the Varia Suit",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_missile(world, state, 1)
            and self.logic.can_space_jump(world, state)
            and self.logic.has_energy_tanks(world, state, 4)
            and self.logic.can_heat(world, state)
            and state.can_reach(RoomName.Burning_Trail.value, None, world.player),
        )
        self.lava_lake_item_missiles_only = TrickInfo(
            "Lava Lake Item Missiles Only",
            "Reach lava lake item without space jump by jumping on base of column",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_missile(world, state, 1)
            and state.can_reach(RoomName.Burning_Trail.value, None, world.player),
        )

        self.triclops_pit_item_no_sj = TrickInfo(
            "Triclops Pit Item No SJ",
            "Reach the Triclops Pit item without Space Jump, assumes has xray and can use charge or missiles",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_xray(world, state)
            and (
                self.logic.can_missile(world, state, 1)
                or self.logic.can_charge_beam(world, state)
            ),
        )
        self.triclops_pit_item_no_xray = TrickInfo(
            "Triclops Pit Item No XRay",
            "Reach the Triclops Pit item without XRay Visor, assumes has space jump and can use charge or missiles",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_space_jump(world, state)
            and (
                self.logic.can_missile(world, state, 1)
                or self.logic.can_charge_beam(world, state)
            ),
        )
        self.triclops_pit_item_no_sj_no_xray = TrickInfo(
            "Triclops Pit Item No SJ No XRay",
            "Reach the Triclops Pit item without Space Jump or XRay Visor, assumes has charge or missiles",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_missile(world, state, 1)
            or self.logic.can_charge_beam(world, state),
        )
        self.triclops_pit_item_no_missiles = TrickInfo(
            "Triclops Pit Item No Missiles",
            "Reach the Triclops Pit item without Missiles, and instead use Charge Beam",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_xray(world, state)
            and self.logic.can_charge_beam(world, state),
        )

        self.warrior_shrine_no_boost = TrickInfo(
            "Warrior Shrine No Boost",
            "Reach the Warrior Shrine by using an R Jump or Scan Dash",
            TrickDifficulty.Easy,
            self.logic.can_space_jump,
        )
        self.warrior_shrine_scan_only = TrickInfo(
            "Warrior Shrine Scan Only",
            "Reach the Warrior Shrine with only Scan Visor",
            TrickDifficulty.Medium,
            self.logic.can_scan,
        )
        self.warrior_shrine_no_items = TrickInfo(
            "Warrior Shrine No Items",
            "Reach the Warrior Shrine without any items by abusing standable collision and a Combat Dash",
            TrickDifficulty.Medium,
            lambda world, state: True,
        )

        self.shore_tunnel_escape_no_sj = TrickInfo(
            "Shore Tunnel Escape No SJ",
            "Escape the Shore Tunnel without Space Jump by using a double bomb jump",
            TrickDifficulty.Medium,
            self.logic.can_bomb,
        )

        self.fiery_shores_morphball_track_sj = TrickInfo(
            "Fiery Shores Morphball Track SJ",
            "Reach the Morph Ball Track in Fiery Shores using the space jump boots",
            TrickDifficulty.Easy,
            self.logic.can_space_jump,
        )

        self.transport_tunnel_b_damage_boost = TrickInfo(
            "Transport Tunnel B Damage Boost",
            "Cross the tunnel through the lava rather than using the morph ball track",
            TrickDifficulty.Easy,
            self.logic.can_heat,
        )

        self.twin_fires_tunnel_no_spider = TrickInfo(
            "Twin Fires Tunnel No Spider Ball",
            "Traverse the Twin Fires Tunnel by using an R Jump and geometrey near the transport door",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_space_jump(world, state),
        )
        self.cross_twin_fires_suitless = TrickInfo(
            "Cross Twin Fires Suitless",
            "Removes the suit requirement when crossing this room. Twin Fires Tunnel is the only room in late Magmoor that is superheated. This trick automatically assumes you have 2 Energy Tanks and can cross without Spider Ball, since it cannot be used while you are taking heat damage.",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.has_energy_tanks(world, state, 2),
        )

        self.geothermal_core_no_grapple_spider = TrickInfo(
            "Geothermal Core No Grapple Spider",
            "You can R jump or dash to reach the boost spinners, and either slope R jump or abuse standable collision to skip the spider track.",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_boost(world, state)
            and self.logic.can_space_jump(world, state),
        )

        self.magmoor_workstation_no_thermal = TrickInfo(
            "Magmoor Workstation No Thermal",
            "Reach the Magmoor Workstation Item without the Thermal Visor",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_scan(world, state)
            and self.logic.can_wave_beam(world, state)
            and self.logic.can_morph_ball(world, state),
        )
        # Phendrana

        self.ice_temple_no_sj = TrickInfo(
            "Ice Temple No SJ",
            "You can reach these locations by doing a hyper bomb jump in Phendrana Shorelines to reach the temple, and double bomb jumping to climb the temple itself",
            TrickDifficulty.Medium,
            rule_func=self.logic.can_bomb,
        )
        self.ice_temple_to_chapel_no_sj = TrickInfo(
            "Ice Temple to chapel No SJ",
            "You can reach these locations by doing a hyper bomb jump in Phendrana Shorelines to reach the temple, and double bomb jumping to climb the temple itself",
            TrickDifficulty.Medium,
            rule_func=lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_missile(world, state, 1),
        )
        self.shorelines_spider_track_no_sj = TrickInfo(
            "Shorelines Spider Track No SJ",
            "You can reach the item in the Phendrana Shorelines Spider Track without Space Jump by using a hyper bomb jump",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_spider(world, state)
            and self.logic.can_super_missile(world, state)
            and self.logic.can_scan(world, state),
        )

        self.ice_temple_item_no_sj = TrickInfo(
            "Ice Temple Item No SJ",
            "Reach the Ice Temple item without Space Jump by double bomb jumps",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_melt_ice(world, state),
        )
        self.chapel_of_elders_escape_no_sj = TrickInfo(
            "Chapel of Elders Escape No SJ",
            "Escape the Chapel of Elders without Space Jump by using a double bomb jump",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_defeat_sheegoth(world, state)
            and self.logic.can_bomb(world, state)
            and self.logic.can_wave_beam(world, state),
        )

        self.phendrana_canyon_escape_no_items = TrickInfo(
            "Phendrana Canyon Escape No Items",
            "You can leave Phendrana Canyon without any items by jumping on the crates. However, if you destroy the crates and don't have Boost Ball or Space Jump, you will softlock.",
            TrickDifficulty.Easy,
            lambda world, state: True,
        )
        self.phendrana_courtyard_no_boost_spider = TrickInfo(
            "Phendrana Courtyard No Boost Spider",
            "There is standable collision near the lower door that can be used to climb to the top of the room.",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_space_jump(world, state),
        )
        self.phendrana_courtyard_item_no_boost_spider = TrickInfo(
            "Phendrana Courtyard No Boost Spider",
            "There is standable collision near the lower door that can be used to climb to the top of the room. You can enter the hole by jumping on top of it and then morphin.",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_morph_ball(world, state),
        )

        self.control_tower_item_no_plasma = TrickInfo(
            "Control Tower Item No Plasma",
            "Reach the Control Tower item without Plasma Beam by jumping off of crates in the middle and missiling the tower base",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_missile(world, state, 1)
            and self.logic.can_space_jump(world, state),
        )

        self.monitor_cave_no_grapple = TrickInfo(
            "Monitor Cave No Grapple",
            "Reach the Monitor Station without the Grapple Beam by using a scan dash",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_spider(world, state)
            and self.logic.can_space_jump(world, state)
            and self.logic.can_scan(world, state),
        )
        self.quarantine_to_north_courtyard_slope_jump = TrickInfo(
            "Quarantine to North Courtyard Slope Jump",
            "You can exit Quarantine Cave to Ruined Courtyard by slope jumping next to the Spider Ball track.",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_space_jump(world, state),
        )

        self.observatory_puzzle_skip = TrickInfo(
            "Observatory Puzzle Skip",
            "This trick expects you to dash to climb Observatory without Boost Ball and Bombs, and then slope jump to the pipes to reach the item.",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_scan(world, state),
        )
        self.frozen_pike_no_bombs = TrickInfo(
            "Frozen Pike No Bombs",
            "To skip the morph ball bomb tunnel, you can R jump or dash to the upper platform on the opposite end of the tunnel.",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_space_jump(world, state),
        )
        self.frozen_pike_no_gravity_suit = TrickInfo(
            "Frozen Pike No Gravity Suit",
            "Reach hunter cave without gravity suit by doing a slope jump",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_space_jump(world, state),
        )

        self.frost_cave_no_grapple = TrickInfo(
            "Frost Cave No Grapple",
            "Reach the Frost Cave item without the Grapple Beam",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_missile(world, state, 1)
            and self.logic.can_space_jump(world, state)
            and self.logic.can_move_underwater(world, state),
        )  # Requires gravity

        self.phendranas_edge_storage_cavern_no_grapple = TrickInfo(
            "Phendrana's Edge Storage Cavern No Grapple",
            "Reach the Phendrana's Edge storage cavern without the Grapple Beam",
            TrickDifficulty.Easy,
            lambda world, state: (
                self.logic.can_thermal(world, state)
                or self.logic.can_xray(world, state)
            )
            and self.logic.can_power_bomb(world, state)
            and self.logic.can_space_jump(world, state),
        )
        self.phendranas_edge_security_cavern_no_grapple = TrickInfo(
            "Phendrana's Edge Security Cavern No Grapple",
            "Reach the Phendrana's Edge security cavern without the Grapple Beam",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_grapple(world, state)
            and self.logic.can_morph_ball(world, state)
            and self.logic.can_space_jump(world, state),
        )

        self.hunter_cave_no_grapple = TrickInfo(
            "Hunter Cave No Grapple",
            "Reach the Hunter Cave upper levels without the grapple beam using an r jump",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_space_jump(world, state),
        )

        self.gravity_chamber_no_grapple_plasma = TrickInfo(
            "Gravity Chamber No Grapple Plasma",
            "You can R jump to reach the ledge without Grapple and Plasma Beam.",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_move_underwater(world, state),
        )

        # Phazon Mines

        self.main_quarry_item_no_spider = TrickInfo(
            "Main Quarry Item No Spider Ball",
            "You can slope jump onto the top of the crane and R jump over to the item.",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_morph_ball(world, state)
            and self.logic.can_bomb(world, state)
            and self.logic.can_thermal(world, state)
            and self.logic.can_wave_beam(world, state)
            and self.logic.can_scan(world, state)
            and self.logic.can_space_jump(world, state),
        )
        self.main_quarry_to_waste_disposal_no_grapple = TrickInfo(
            "Main Quarry to Waste Disposal No Grapple",
            "You can scan dash from the top of the structure (using the crane spider track scan point) to reach the door to Waste Disposal.",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_scan(world, state)
            and self.logic.can_space_jump(world, state),
        )

        self.ore_processing_to_storage_depot_b_no_spider = TrickInfo(
            "Ore Processing Climb to Storage No Grapple Spider",
            "You can stand on various collision in the room, such as on the rotating column, to climb to the top of Ore Processing.",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_power_bomb(world, state)
            and self.logic.can_space_jump(world, state)
            and self.logic.can_combat_beam_pirates(
                world, state, SuitUpgrade.Power_Beam
            ),
        )
        self.ore_processing_climb_no_grapple_spider = TrickInfo(
            "Ore Processing Climb No Grapple Spider",
            "You can stand on various collision in the room, such as on the rotating column, to climb to the top of Ore Processing.",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_power_bomb(world, state)
            and self.logic.can_space_jump(world, state)
            and self.logic.can_combat_beam_pirates(
                world, state, SuitUpgrade.Power_Beam
            ),
        )

        self.mines_climb_shafts_no_spider = TrickInfo(
            "Mines Climb Shafts No Spider Ball",
            "Elevator Access A and Research Access can be climbed without Spider Ball.",
            TrickDifficulty.Hard,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_wave_beam(world, state),
        )  # Wave Beam is needed to kill the Bombu

        self.elite_research_spinner_no_boost = TrickInfo(
            "Elite Research laser No Boost",
            "You can get the laser turret to spin by wedging the morph ball in the spinner, bombing out, and then spinning the morph ball while in the laser before it locks you in.",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_scan(world, state)
            and self.logic.can_space_jump(world, state)
            and self.logic.can_combat_beam_pirates(
                world, state, SuitUpgrade.Power_Beam
            ),
        )
        self.elite_research_backwards_wall_boost: TrickInfo = TrickInfo(
            "Elite Research Backwards Wall Boost",
            "Enter Elite Research from the top door and use Boost Ball to get through the backwards wall",
            TrickDifficulty.Easy,
            self.logic.can_boost,
        )
        self.elite_research_backwards_wall_boost_no_spider: TrickInfo = TrickInfo(
            "Elite Research Backwards Wall Boost No Spider",
            "Reach elite research via Research Access without the spider ball",
            TrickDifficulty.Hard,
            lambda world, state: self.elite_research_backwards_wall_boost.rule_func(
                world, state
            )
            and self.mines_climb_shafts_no_spider.rule_func(world, state),
        )

        self.ventilation_shaft_hpbj = TrickInfo(
            "Ventilation Shaft HPBJ",
            "It's possible to return to Elite Control by performing a half pipe bomb jump to reach the Elite Control door.",
            TrickDifficulty.Hard,
            lambda world, state: self.logic.can_bomb(world, state)
            and self.logic.can_space_jump(world, state),
        )

        self.metroid_quarantine_a_no_spider = TrickInfo(
            "Metroid Quarantine A No Spider Ball",
            "Using R jumps, slope jumps, and dashes, you can traverse the entirety of lower Phazon Mines without Spider Ball and Grapple Beam.",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_scan(world, state)
            and self.logic.can_xray(world, state)
            and self.logic.can_space_jump(world, state),
        )

        self.fungal_hall_access_no_phazon_suit = TrickInfo(
            "Fungal Hall Access No Phazon Suit",
            "You can reach the Fungal Hall Access item without the Phazon Suit",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_morph_ball(world, state)
            and self.logic.has_energy_tanks(world, state, 1),
        )

        self.fungal_hall_a_no_grapple = TrickInfo(
            "Fungal Hall A No Grapple",
            "Traverse Fungal Hall A with Slope Jumps and R Jumps",
            TrickDifficulty.Medium,
            self.logic.can_space_jump,
        )
        self.fungal_hall_b_no_grapple = TrickInfo(
            "Fungal Hall B No Grapple",
            "Traverse Fungal Hall B with Slope Jumps and R Jumps",
            TrickDifficulty.Medium,
            self.logic.can_space_jump,
        )

        self.metroid_quarantine_b_no_spider_grapple = TrickInfo(
            "Metroid Quarantine B No Spider Grapple",
            "You can reach the other side of the quarantine by using a slope jump and an r jump",
            TrickDifficulty.Medium,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_scan(world, state),
        )

        self.phazon_processing_center_item_no_spider = TrickInfo(
            "Phazon Processing Center Item No Spider Ball",
            "You can abuse standable collision such as the morph track and the scaffolding to access the top of the room without needing Spider Ball.",
            TrickDifficulty.Easy,
            lambda world, state: self.logic.can_space_jump(world, state)
            and self.logic.can_power_bomb(world, state),
        )
        self.phazon_processing_center_no_phazon_suit = TrickInfo(
            "Phazon Processing Center No Phazon Suit",
            "Reach the elite quarters by damage boosting through the phazon without the suit",
            TrickDifficulty.Easy,
            lambda world, state: True,
        )
        self.climb_phazon_processing_center_no_spider = TrickInfo(
            "Phazon Processing Center No Spider Ball",
            "You can abuse standable collision such as the morph track and the scaffolding to access the top of the room without needing Spider Ball.",
            TrickDifficulty.Easy,
            self.logic.can_space_jump,
        )
