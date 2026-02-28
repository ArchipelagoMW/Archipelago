from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from BaseClasses import CollectionState, Region, Entrance

from . import names

if TYPE_CHECKING:
    from .world import SonicGensWorld

def create_region(name: str, world: SonicGensWorld) -> Region:
    return Region(name, world.player, world.multiworld)

def create_entrance(eFrom: Region, eTo:Region, rule: Optional[Callable[[CollectionState], bool]] = None):
    name:str = names.create_entrance_name(eFrom.name, eTo.name)
    
    res: Entrance = eFrom.connect(eTo, name, rule)
    
    return res

def create_and_connect_regions(world: SonicGensWorld) -> None:
    wsce    = create_region(names.Regions.WSClassic, world)
    wsde    = create_region(names.Regions.WSDreamcast, world)
    wsme    = create_region(names.Regions.WSModern, world)

    ghz1    = create_region(names.Regions.GHZ1, world)
    ghz2    = create_region(names.Regions.GHZ2, world)
    cpz1    = create_region(names.Regions.CPZ1, world)
    cpz2    = create_region(names.Regions.CPZ2, world)
    ssz1    = create_region(names.Regions.SSZ1, world)
    ssz2    = create_region(names.Regions.SSZ2, world)
    bms     = create_region(names.Regions.BMS, world)
    bde     = create_region(names.Regions.BDE, world)
    sph1    = create_region(names.Regions.SPH1, world)
    sph2    = create_region(names.Regions.SPH2, world)
    cte1    = create_region(names.Regions.CTE1, world)
    cte2    = create_region(names.Regions.CTE2, world)
    ssh1    = create_region(names.Regions.SSH1, world)
    ssh2    = create_region(names.Regions.SSH2, world)
    bsd     = create_region(names.Regions.BSD, world)
    bpc     = create_region(names.Regions.BPC, world)
    csc1    = create_region(names.Regions.CSC1, world)
    csc2    = create_region(names.Regions.CSC2, world)
    euc1    = create_region(names.Regions.EUC1, world)
    euc2    = create_region(names.Regions.EUC2, world)
    pla1    = create_region(names.Regions.PLA1, world)
    pla2    = create_region(names.Regions.PLA2, world)
    bsl     = create_region(names.Regions.BSL, world)
    bne     = create_region(names.Regions.BNE, world)
    blb     = create_region(names.Regions.BLB, world)

    world.multiworld.regions += [wsce, wsde, wsme, ghz1, ghz2, cpz1, cpz2, ssz1, ssz2, bms, bde, sph1, sph2, cte1, cte2, ssh1, ssh2, bsd, bpc, csc1, csc2, euc1, euc2, pla1, pla2, bsl, bne, blb]

    # TODO: will it be OK to bombard the player with all 30 missions per area even when the main acts havent been cleared yet? i personally dont believe so but could do with a second opinion on this (and knowledge of how to add that requirement)
    create_entrance(wsce, ghz1)
    create_entrance(wsce, ghz2)
    create_entrance(wsce, cpz1)
    create_entrance(wsce, cpz2)
    create_entrance(wsce, ssz1)
    create_entrance(wsce, ssz2)
    world.multiworld.register_indirect_condition(ssz2, create_entrance(wsce, bms, lambda state: state.can_reach_region(names.Regions.SSZ2, world.player)))
    create_entrance(wsce, bde, lambda state: state.has_all([names.Items.BKGHZ, names.Items.BKCPZ, names.Items.BKSSZ], world.player))
    world.multiworld.register_indirect_condition(bde, create_entrance(wsce, wsde, lambda state: state.can_reach_region(names.Regions.BDE, world.player)))

    create_entrance(wsde, sph1)
    create_entrance(wsde, sph2)
    create_entrance(wsde, cte1)
    create_entrance(wsde, cte2)
    create_entrance(wsde, ssh1)
    create_entrance(wsde, ssh2)
    world.multiworld.register_indirect_condition(ssh2, create_entrance(wsde, bsd, lambda state: state.can_reach_region(names.Regions.SSH2, world.player)))
    create_entrance(wsde, bpc, lambda state: state.has_all([names.Items.BKSPH, names.Items.BKCTE, names.Items.BKSSH], world.player))
    world.multiworld.register_indirect_condition(bpc, create_entrance(wsde, wsme, lambda state: state.can_reach_region(names.Regions.BPC, world.player)))

    create_entrance(wsme, csc1)
    create_entrance(wsme, csc2)
    create_entrance(wsme, euc1)
    create_entrance(wsme, euc2)
    create_entrance(wsme, pla1)
    create_entrance(wsme, pla2)
    world.multiworld.register_indirect_condition(pla2, create_entrance(wsme, bsl, lambda state: state.can_reach_region(names.Regions.PLA2, world.player)))
    create_entrance(wsme, bne, lambda state: state.has_all([names.Items.BKCSC, names.Items.BKEUC, names.Items.BKPLA], world.player))
    world.multiworld.register_indirect_condition(bne, create_entrance(wsme, blb, lambda state: state.has_all([names.Items.EGreen, names.Items.EPurple, names.Items.EBlue, names.Items.EYellow, names.Items.ERed, names.Items.ECyan, names.Items.EWhite], world.player) and
                                                                                        state.can_reach_region(names.Regions.BNE, world.player)))