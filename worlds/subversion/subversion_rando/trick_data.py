from typing import Iterable

from .item_data import Items
from .trick import Trick

# adding new tricks has a cost
# custom logic strings will break
# unless you add them at the end?


class Tricks:
    infinite_bomb_jump = Trick("use bombs to gain infinite height", Items.Morph, Items.Bombs)
    """ use bombs to gain infinite height """

    sbj_underwater_no_hjb = Trick("underwater springball jump - no hi jump boots", Items.Morph, Items.Speedball)
    """ underwater springball jump - no hi jump boots """

    sbj_underwater_w_hjb = Trick("underwater springball jump with hi jump boots",
                                 Items.Morph, Items.Speedball, Items.HiJump)
    """ underwater springball jump with hi jump boots """

    sbj_no_hjb = Trick("springball jump - no hi jump boots (no water)", Items.Morph, Items.Speedball)
    """ springball jump - no hi jump boots (no water) """

    sbj_w_hjb = Trick("springball jump with hi jump boots (no water)", Items.Morph, Items.Speedball, Items.HiJump)
    """ springball jump with hi jump boots (no water) """

    sbj_wall = Trick("springball jump off of a wall jump - not underwater", Items.Morph, Items.Speedball)
    """ springball jump off of a wall jump - not underwater """

    uwu_2_tile = Trick("underwater wall jumps between left and right in a 2-tile wide space")
    """ underwater wall jumps between left and right in a 2-tile wide space """

    uwu_2_tile_surface = Trick("underwater wall jumps between left and right in a 2-tile wide space "
                               "to get above the surface of the water")
    """
    underwater wall jumps between left and right in a 2-tile wide space
    to get above the surface of the water
    """

    gravity_jump = Trick("remove aqua suit right after jumping for extra jump height in water", Items.Aqua)
    """ remove aqua suit right after jumping for extra jump height in water """

    hell_run_hard = Trick("heated or cold without varia suit - hell runs requiring the minimum amount of energy")
    """ heated or cold without varia hell runs requiring the minimum amount of energy """

    hell_run_medium = Trick("heated or cold without varia suit - hell runs requiring 1.5x energy")
    """ heated or cold without varia hell runs requiring 1.5x energy """

    hell_run_easy = Trick("heated or cold without varia suit - hell runs requiring 2x energy")
    """ heated or cold without varia hell runs requiring 2x energy """

    movement_moderate = Trick("moderately fast/precise movement")
    """ moderately fast/precise movement """

    movement_zoast = Trick("difficult fast/precise movement")
    """ difficult fast/precise movement """

    wall_jump_delayed = Trick("need to jump as far from the wall as possible ")
    """
    need to jump as far from the wall as possible
    (like top of hive crossways left side, or vanilla getting up to gauntlet)
    """

    wall_jump_precise = Trick("short walls or around wide ledges")
    """ short walls or around wide ledges (2 tiles without hjb, 3 tiles with hjb) """

    crumble_jump = Trick("jump off of crumble blocks")
    """ jump off of crumble blocks """

    mockball_hard = Trick("short hop or short run", Items.Morph)
    """ short hop or short run (warrior shrine) """

    morphless_tunnel_crawl = Trick("travel through a 2-tile high space without morph ball")
    """ travel through a 2-tile high space without morph ball """

    morph_jump_3_tile = Trick("mid-air morph in a 3-tile-high space (no water)", Items.Morph)
    """ mid-air morph in a 3-tile-high space (no water) """

    morph_jump_4_tile = Trick("mid-air morph in a 4-tile-high space (no water)", Items.Morph)
    """ mid-air morph in a 4-tile-high space (no water) """

    # TODO: I think morph_jump_3_tile or 4 may have been used where it should be this.
    morph_jump_3_tile_up_1 = Trick("mid-air morph in a 3-tile-high space up 1 tile (no water)", Items.Morph)
    """ mid-air morph in a 3-tile-high space into 1 tile higher than where you started (no water) """

    morph_jump_3_tile_water = Trick("mid-air morph in a 3-tile-high space in water", Items.Morph)
    """ mid-air morph in a 3-tile-high space in water """

    crouch_or_downgrab = Trick("use crouch jump and/or down-grab to jump to higher ledge")
    """ use crouch jump and/or down-grab to jump to higher ledge """

    crouch_precise = Trick("crouch jump along with some precision movement")
    """ crouch jump along with some precision movement (not just straight up and over at the top) """

    dark_easy = Trick("without dark visor, move through darker rooms where walls are light-colored")
    """
    without dark visor, move through darker rooms where walls are light-colored (Spore Field)

    This is also used for killing the invisible enemies in the Cellar.
    """

    dark_medium = Trick("without dark visor, move through darker rooms where walls are NOT light-colored")
    """ without dark visor, move through darker rooms where walls are NOT light-colored (Meandering Passage) """

    dark_hard = Trick("without dark visor, move through very dark rooms (Dark Crevice)")
    """ without dark visor, move through very dark rooms (Dark Crevice) """

    freeze_hard = Trick("freeze an enemy that's difficult to freeze in the right place", Items.Ice)
    """
    freeze an enemy that's difficult to freeze in the right place, because of erratic/fast/dangerous movement

    an example of an enemy that's NOT hard to freeze in the right place is Choot (pancake)
    """

    wave_gate_glitch = Trick("shoot a normal beam through a wave gate")
    """ shoot a normal beam through a wave gate """

    ggg = Trick("green gate glitch")
    """ green gate glitch - shoot missiles or super missiles through a gate from right to left """

    clip_crouch = Trick("jump into a 2-tile high space crouched to clip through the ceiling")
    """ jump into a 2-tile high space crouched to clip through the ceiling """

    short_charge_2 = Trick("charge shinespark in smaller running space - 2 tap", Items.SpeedBooster)
    """ charge shinespark in smaller running space - 2 tap """

    short_charge_3 = Trick("charge shinespark in smaller running space - 3 tap", Items.SpeedBooster)
    """ charge shinespark in smaller running space - 3 tap """

    short_charge_4 = Trick("charge shinespark in smaller running space - 4 tap", Items.SpeedBooster)
    """ charge shinespark in smaller running space - 4 tap """

    xray_climb = Trick("use Xray to climb through terrain", Items.Xray)
    """ use Xray to climb through terrain """

    ice_clip = Trick("freeze an enemy at a specific distance from the ceiling to jump through the ceiling", Items.Ice)
    """ freeze an enemy at a specific distance from the ceiling to jump through the ceiling """

    moonfall_clip = Trick("use moonfall to fall through a floor or downward door")
    """ use moonfall to fall through a floor or downward door """

    super_sink_easy = Trick("use gravity boots glitch to fall through terrain by spin jumping into 2-tile high space",
                            Items.GravityBoots)
    """ use gravity boots glitch to fall through terrain by spin jumping into 2-tile high space """
    # super sink easy includes door-stuck start

    super_sink_hard = Trick("use gravity boots glitch to fall through terrain (without a 2-tile high space)",
                            Items.GravityBoots, Items.Morph)
    """ use gravity boots glitch to fall through terrain (without a 2-tile high space) """

    patience = Trick("RAGE!!!")
    """ determination """

    # specific location tricks

    plasma_gate_glitch = Trick("get through the plasma+wave gate in Geothermal Magma Pump with only wave beam",
                               Items.Wave)
    """ get through the plasma+wave gate in Geothermal Magma Pump with only wave beam """

    searing_gate_tricks = Trick("", Items.Morph)
    """ "It's a secret to everybody." """

    spazer_into_lower_pirate_lab = Trick("", Items.Spazer)
    """ She's made of wood! """


trick_name_lookup = {
    trick: trick_name
    for trick_name, trick in vars(Tricks).items()
    if isinstance(trick, Trick)
}


def tricks_to_jsonable(tricks: frozenset[Trick]) -> list[str]:
    return [
        trick_name
        for trick, trick_name in trick_name_lookup.items()
        if trick in tricks
    ]


def tricks_from_names(tricks: Iterable[str]) -> frozenset[Trick]:
    return frozenset([
        getattr(Tricks, trick_name)
        for trick_name in tricks
    ])
