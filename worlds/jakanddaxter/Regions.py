import typing

from Options import OptionError
from . import JakAndDaxterWorld
from .Items import item_table
from .Options import EnableOrbsanity, CompletionCondition
from .Rules import can_reach_orbs_global
from .locs import CellLocations as Cells, ScoutLocations as Scouts
from .regs import (GeyserRockRegions as GeyserRock,
                   SandoverVillageRegions as SandoverVillage,
                   ForbiddenJungleRegions as ForbiddenJungle,
                   SentinelBeachRegions as SentinelBeach,
                   MistyIslandRegions as MistyIsland,
                   FireCanyonRegions as FireCanyon,
                   RockVillageRegions as RockVillage,
                   PrecursorBasinRegions as PrecursorBasin,
                   LostPrecursorCityRegions as LostPrecursorCity,
                   BoggySwampRegions as BoggySwamp,
                   MountainPassRegions as MountainPass,
                   VolcanicCraterRegions as VolcanicCrater,
                   SpiderCaveRegions as SpiderCave,
                   SnowyMountainRegions as SnowyMountain,
                   LavaTubeRegions as LavaTube,
                   GolAndMaiasCitadelRegions as GolAndMaiasCitadel)
from .regs.RegionBase import JakAndDaxterRegion


def create_regions(world: JakAndDaxterWorld):
    multiworld = world.multiworld
    options = world.options
    player = world.player

    # Always start with Menu.
    menu = JakAndDaxterRegion("Menu", player, multiworld)
    multiworld.regions.append(menu)

    # Build the special "Free 7 Scout Flies" Region. This is a virtual region always accessible to Menu.
    # The Locations within are automatically checked when you receive the 7th scout fly for the corresponding cell.
    free7 = JakAndDaxterRegion("'Free 7 Scout Flies' Power Cells", player, multiworld)
    free7.add_cell_locations(Cells.loc7SF_cellTable.keys())
    for scout_fly_cell in free7.locations:

        # Translate from Cell AP ID to Scout AP ID using game ID as an intermediary.
        scout_fly_id = Scouts.to_ap_id(Cells.to_game_id(typing.cast(int, scout_fly_cell.address)))
        scout_fly_cell.access_rule = lambda state, flies=scout_fly_id: state.has(item_table[flies], player, 7)
    multiworld.regions.append(free7)
    menu.connect(free7)

    # If Global Orbsanity is enabled, build the special Orbsanity Region. This is a virtual region always
    # accessible to Menu. The Locations within are automatically checked when you collect enough orbs.
    if options.enable_orbsanity == EnableOrbsanity.option_global:
        orbs = JakAndDaxterRegion("Orbsanity", player, multiworld)

        bundle_count = 2000 // world.orb_bundle_size
        for bundle_index in range(bundle_count):

            # Unlike Per-Level Orbsanity, Global Orbsanity Locations always have a level_index of 16.
            orbs.add_orb_locations(16,
                                   bundle_index,
                                   access_rule=lambda state, bundle=bundle_index:
                                   can_reach_orbs_global(state, player, world, bundle))
        multiworld.regions.append(orbs)
        menu.connect(orbs)

    # Build all regions. Include their intra-connecting Rules, their Locations, and their Location access rules.
    [gr] = GeyserRock.build_regions("Geyser Rock", world)
    [sv] = SandoverVillage.build_regions("Sandover Village", world)
    [fj, fjp] = ForbiddenJungle.build_regions("Forbidden Jungle", world)
    [sb] = SentinelBeach.build_regions("Sentinel Beach", world)
    [mi] = MistyIsland.build_regions("Misty Island", world)
    [fc] = FireCanyon.build_regions("Fire Canyon", world)
    [rv, rvp, rvc] = RockVillage.build_regions("Rock Village", world)
    [pb] = PrecursorBasin.build_regions("Precursor Basin", world)
    [lpc] = LostPrecursorCity.build_regions("Lost Precursor City", world)
    [bs] = BoggySwamp.build_regions("Boggy Swamp", world)
    [mp, mpr] = MountainPass.build_regions("Mountain Pass", world)
    [vc] = VolcanicCrater.build_regions("Volcanic Crater", world)
    [sc] = SpiderCave.build_regions("Spider Cave", world)
    [sm] = SnowyMountain.build_regions("Snowy Mountain", world)
    [lt] = LavaTube.build_regions("Lava Tube", world)
    [gmc, fb, fd] = GolAndMaiasCitadel.build_regions("Gol and Maia's Citadel", world)

    # Configurable counts of cells for connector levels.
    fc_count = options.fire_canyon_cell_count.value
    mp_count = options.mountain_pass_cell_count.value
    lt_count = options.lava_tube_cell_count.value

    # Define the interconnecting rules.
    menu.connect(gr)
    gr.connect(sv)  # Geyser Rock modified to let you leave at any time.
    sv.connect(fj)
    sv.connect(sb)
    sv.connect(mi, rule=lambda state: state.has("Fisherman's Boat", player))
    sv.connect(fc, rule=lambda state: state.has("Power Cell", player, fc_count))  # Normally 20.
    fc.connect(rv)
    rv.connect(pb)
    rv.connect(lpc)
    rvp.connect(bs)  # rv->rvp/rvc connections defined internally by RockVillageRegions.
    rvc.connect(mp, rule=lambda state: state.has("Power Cell", player, mp_count))  # Normally 45.
    mpr.connect(vc)  # mp->mpr connection defined internally by MountainPassRegions.
    vc.connect(sc)
    vc.connect(sm, rule=lambda state: state.has("Snowy Mountain Gondola", player))
    vc.connect(lt, rule=lambda state: state.has("Power Cell", player, lt_count))  # Normally 72.
    lt.connect(gmc)  # gmc->fb connection defined internally by GolAndMaiasCitadelRegions.

    # Set the completion condition.
    if options.jak_completion_condition == CompletionCondition.option_cross_fire_canyon:
        multiworld.completion_condition[player] = lambda state: state.can_reach(rv, "Region", player)

    elif options.jak_completion_condition == CompletionCondition.option_cross_mountain_pass:
        multiworld.completion_condition[player] = lambda state: state.can_reach(vc, "Region", player)

    elif options.jak_completion_condition == CompletionCondition.option_cross_lava_tube:
        multiworld.completion_condition[player] = lambda state: state.can_reach(gmc, "Region", player)

    elif options.jak_completion_condition == CompletionCondition.option_defeat_dark_eco_plant:
        multiworld.completion_condition[player] = lambda state: state.can_reach(fjp, "Region", player)

    elif options.jak_completion_condition == CompletionCondition.option_defeat_klaww:
        multiworld.completion_condition[player] = lambda state: state.can_reach(mp, "Region", player)

    elif options.jak_completion_condition == CompletionCondition.option_defeat_gol_and_maia:
        multiworld.completion_condition[player] = lambda state: state.can_reach(fb, "Region", player)

    elif options.jak_completion_condition == CompletionCondition.option_open_100_cell_door:
        multiworld.completion_condition[player] = lambda state: state.can_reach(fd, "Region", player)

    else:
        raise OptionError(f"{world.player_name}: Unknown completion goal ID "
                          f"({options.jak_completion_condition.value}).")
