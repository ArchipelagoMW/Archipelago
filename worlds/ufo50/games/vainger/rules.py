from typing import TYPE_CHECKING, Dict
from BaseClasses import Region, CollectionState
from worlds.generic.Rules import set_rule, CollectionRule

if TYPE_CHECKING:
    from ... import UFO50World

# adapted from Barbuta, thanks Scipio! <3

# name upgrades for convenience
heat_mod = "Vainger - Heat Mod"
multi_mod = "Vainger - Multi Mod"
pulse_mod = "Vainger - Pulse Mod"
force_mod = "Vainger - Force Mod"

stabilizer = "Vainger - Stabilizer"
shield_upgrade = "Vainger - Shield Upgrade"
keycode_A = "Vainger - Key Code A"
keycode_B = "Vainger - Key Code B"
keycode_C = "Vainger - Key Code C"
keycode_D = "Vainger - Key Code D"
security_clearance = "Vainger - Progressive Security Clearance"


# can the player do a given hell run?
# TODO: option for this
def hell_run(shield_upgrades_required: int, is_vanilla: bool, state: CollectionState, world: "UFO50World") -> bool:
    return state.count(shield_upgrade, world.player) >= shield_upgrades_required


# can the player beat a given boss? currently checks how many mods the player has,
# whether they have a stabilizer, and if they hit a vibes-based shield threshold.
# TODO: option for this
# difficulty must be between 0 and 4 inclusive
def boss_logic(difficulty: int, state: CollectionState, world:"UFO50World") -> bool:
    player = world.player
    if not state.has_from_list_unique([heat_mod, multi_mod, pulse_mod, force_mod], player, difficulty):
        return False
    if difficulty == 4 and not state.has(stabilizer, player):
        return False
    shield_upgrades_required = [0, 0, 5, 10, 15][difficulty]
    return state.has(shield_upgrade, player, shield_upgrades_required)


# can the player tank two hits from spikes without spike-ng?
# either there and back through one layer, or two hits in and zero out
# TODO: option for this
def spike_tank(state: CollectionState, world: "UFO50World") -> bool:
    player = world.player
    # without magmatek, there's no way to have enough shield to cross the spikes in both directions
    if not state.has(heat_mod, player):
        return False
    shield_upgrades_required = 6  # 105 shield, enough to take two hits with magmatek
    return state.has(shield_upgrade, player, shield_upgrades_required)


def create_rules(world: "UFO50World", regions: Dict[str, Region]) -> None:
    player = world.player

    # name regions for convenience
    latomr6c3 = regions["Vainger - LatomR6C3 Genepod"]
    latomr9c3 = regions["Vainger - LatomR9C3 Genepod"]
    latomr3c4 = regions["Vainger - LatomR3C4 Genepod"]
    latomr5c4 = regions["Vainger - LatomR5C4 Genepod"]
    latomr5c6 = regions["Vainger - LatomR5C6 Genepod"]
    latomr7c6 = regions["Vainger - LatomR7C6 Genepod"]
    latomr4c9 = regions["Vainger - LatomR4C9 Genepod"]
    latomr6c4area = regions["Vainger - LatomR6C4 Area"]

    thetar4c1 = regions["Vainger - ThetaR4C1 Genepod"]
    thetar9c5 = regions["Vainger - ThetaR9C5 Genepod"]
    thetar5c6 = regions["Vainger - ThetaR5C6 Genepod"]
    thetar6c6 = regions["Vainger - ThetaR6C6 Genepod"]
    thetar7c9 = regions["Vainger - ThetaR7C9 Genepod"]
    thetar9c9 = regions["Vainger - ThetaR9C9 Genepod"]
    thetar8c3loc = regions["Vainger - ThetaR8C3 Location"]
    thetar10c3loc = regions["Vainger - ThetaR10C3 Location"]
    
    verder1c1 = regions["Vainger - VerdeR1C1 Genepod"]
    verder1c5 = regions["Vainger - VerdeR1C5 Genepod"]
    verder6c5 = regions["Vainger - VerdeR6C5 Genepod"]
    verder7c9 = regions["Vainger - VerdeR7C9 Genepod"]
    verder9c9 = regions["Vainger - VerdeR9C9 Genepod"]
    verdeswarea = regions["Vainger - VerdeSW Area"]
    verder7c8loc = regions["Vainger - VerdeR7C8 Location"]
    
    control = regions["Vainger - Control Genepod"] 

    # ThetaR5C6 is the starting genepod
    regions["Vainger - Menu"].connect(thetar5c6)

    thetar5c6.connect(thetar7c9)
    # whether this hell run should be in logic itemless is a big question. it'll expand the possibilities
    # for heat mod placement a lot, but it's tricky and doing it every single time in sphere 1 could get old fast.
    # currently this is considered logical itemless
    thetar5c6.connect(thetar4c1,
                      rule=lambda state: state.has(heat_mod, player)
                      or hell_run(0, False, state, world))  # itemless hell run
    thetar5c6.connect(control,
                      rule=lambda state: (state.has(heat_mod, player)
                                          or hell_run(0, False, state, world))  # itemless hell run
                      and state.has_all((keycode_A, keycode_B, keycode_C, keycode_D), player))
    thetar7c9.connect(thetar9c9)
    thetar4c1.connect(latomr9c3)  # TODO: do we need logic for the miniboss in ThetaB2?
    thetar4c1.connect(verder1c1)
    thetar4c1.connect(thetar6c6,
                      rule=lambda state: state.has_any([multi_mod, force_mod], player)
                      or spike_tank(state, world))  # shadow or spike-ng or spike tank
    thetar6c6.connect(thetar9c5,
                      rule=lambda state: state.has("Vainger - ThetaR9C5 - Boss Defeated", player))  # genepod only exists after boss kill
    thetar9c9.connect(thetar4c1,
                      rule=lambda state: state.has_all((multi_mod, heat_mod), player))  # shadow + hot-shot
    thetar9c9.connect(verder7c9,
                      rule=lambda state: state.has(heat_mod, player))  # hot-shot
    # logic for the two weird locations in Theta SW
    thetar9c9.connect(thetar10c3loc,
                      rule=lambda state: state.has_all((multi_mod, heat_mod, force_mod), player))  # shadow + hot-shot + spike-ng
    thetar9c9.connect(thetar8c3loc,
                      rule=lambda state: state.has_all((multi_mod, heat_mod), player))  # shadow + hot-shot
    verder1c1.connect(thetar10c3loc,
                      rule=lambda state: state.has(heat_mod, player))  # hot-shot
    verder1c1.connect(thetar8c3loc,
                      rule=lambda state: state.has(heat_mod, player))  # hot-shot
    verder1c1.connect(verder1c5,
                      rule=lambda state: state.has("Vainger - VerdeR1C5 - Ramses Defeated", player))  # genepod only exists after boss kill
    verder1c5.connect(verder6c5)
    verder1c5.connect(verder7c9)
    verder6c5.connect(verdeswarea,
                      rule=lambda state: state.has(security_clearance, player, 2)
                      or state.has(heat_mod, player))  # hot-shot for the shortcut R5C6 -> R5C5
    verder7c9.connect(verdeswarea,
                      rule=lambda state: state.has(security_clearance, player, 1))
    verdeswarea.connect(verder9c9,
                        rule=lambda state: state.has(security_clearance, player, 2)
                        and state.has("Vainger - VerdeR9C9 - Sura Defeated", player))  # genepod only exists after boss
    # the spike tank strat is unreasonable coming from the left, so the fact that a player coming from the
    # left *might* have used hot-shot to get here is irrelevant.
    verdeswarea.connect(verder7c8loc,
                        rule=lambda state: state.has(force_mod, player))  # spike-ng.
    verder7c9.connect(verder7c8loc,
                      rule=lambda state: state.has(force_mod, player) or spike_tank(state, world))  # here spike tanking is reasonable

    # TODO: check how hard this hell run is
    latomr9c3.connect(latomr7c6,
                      rule=lambda state: state.has(heat_mod, player)
                      or hell_run(10, False, state, world))  # hot-shot, magmatek, or hell run
    latomr9c3.connect(latomr5c6,
                      rule=lambda state: state.has_all((heat_mod, pulse_mod), player))  # hot-shot and thunder
    latomr7c6.connect(latomr6c3,
                      rule=lambda state: state.has(security_clearance, player, 3)
                      and state.has_any((pulse_mod, multi_mod), player))  # thunder or tri-shot
    latomr7c6.connect(latomr3c4,
                      rule=lambda state: state.has_any([pulse_mod, multi_mod], player))  # thunder or tri-shot
    latomr7c6.connect(latomr5c6,
                      rule=lambda state: state.has(pulse_mod, player))  # thunder or possibly tanking an electrical arc later
    latomr3c4.connect(latomr5c6)
    latomr3c4.connect(latomr6c3,
                      rule=lambda state: state.has(security_clearance, player, 3))
    latomr5c6.connect(latomr3c4)
    latomr5c6.connect(latomr6c3,
                      rule=lambda state: state.has(security_clearance, player, 2) and state.has(heat_mod, player))  # hot-shot
    latomr6c3.connect(latomr5c4,
                      rule=lambda state: state.has(security_clearance, player, 3) and state.has("Vainger - LatomR5C4 - Boss Defeated", player))
    # TODO: the normal route is one-way; does the miniboss block you from doing the upper route in reverse?
    latomr5c6.connect(latomr4c9,
                      rule=lambda state: state.has(pulse_mod, player))  # NOTE: thunder required to prevent a softlock; this means vanilla pulse mod will be impossible.
    latomr6c3.connect(latomr6c4area,
                      rule=lambda state: state.has(heat_mod, player))  # hot-shot for the shortcut R6C3 -> R6C4
    latomr5c6.connect(latomr6c4area,
                      rule=lambda state: state.has(security_clearance, player, 2))
    
    def sr(loc: str, rule: CollectionRule = lambda state: True):
        set_rule(world.get_location(f"Vainger - {loc}"), rule)

    # LatomR3C4
    # sr("LatomR4C1 - Shield Upgrade")
    sr("LatomR7C1 - Shield Upgrade")  # TODO: double-check this, I'm not exactly sure where the upgrade was
    # LatomR9C3
    sr("LatomR9C1 - Shield Upgrade", rule=lambda state: state.has(heat_mod, player)
        and hell_run(10, True, state, world))  # mandatory hell run; TODO: check difficulty
    sr("LatomR9C2 - Shield Upgrade", rule=lambda state: state.has(multi_mod, player))  # shadow
    sr("LatomR10C10 - Shield Upgrade", rule=lambda state: state.has(heat_mod, player))  # hot-shot
    # LatomR6C3
    sr("LatomR4C3 - Shield Upgrade", rule=lambda state: state.has(security_clearance, player, 3))
    # sr("LatomR6C3 - Clone Material")
    # LatomR6C4 Area
    # sr("LatomR6C4 - Security Clearance")  # accounted for by region logic
    # LatomR7C6
    # sr("LatomR8C7 - Multi Mod")  # the fight here will be a pain itemless but it should be possible
    # LatomR4C9
    # sr("LatomR4C9 - Pulse Mod")
    # LatomR5C6
    # TODO: does this need to be R4C9 instead due to the miniboss?
    sr("LatomR1C10 - Stabilizer", rule=lambda state: boss_logic(1, state, world)  # TODO: check miniboss difficulty
        and state.has_all((pulse_mod, heat_mod), player) and hell_run(0, True, state, world))

    # sr("LatomR4C5 - Shield Upgrade")
    sr("LatomR3C10 - Shield Upgrade", rule=lambda state: state.has(pulse_mod, player)  # including pulse mod to avoid softlocking near R4C9
        and (state.has(force_mod, player) or spike_tank(state, world)))  # meteor or spike-ng or spike tank
    #
    # Alien boss, from LatomR6C3
    sr("LatomR5C4 - Boss Defeated", rule=lambda state: state.has(security_clearance, player, 3)
       and boss_logic(2, state, world))  # TODO: check boss difficulty
    # sr("LatomR5C4 - Key Code")  # relative to boss genepod
    #
    # ThetaR4C1
    sr("ThetaR2C1 - Clone Material", rule=lambda state: state.has(force_mod, player)
       or spike_tank(state, world))  # spike-ng or spike tank
    sr("ThetaR3C1 - Shield Upgrade", rule=lambda state: state.has(force_mod, player)
       or spike_tank(state, world))  # meteor, spike-ng or spike tank
    sr("ThetaR5C3 - Clone Material", rule=lambda state: state.has(pulse_mod, player))  # zap-shot
    sr("ThetaR7C4 - Shield Upgrade", rule=lambda state: state.has(pulse_mod, player))  # thunder
    # ThetaR7C9
    # sr("ThetaR1C8 - Shield Upgrade")
    # sr("ThetaR4C8 - Heat Mod")
    sr("ThetaR4C9 - Shield Upgrade", rule=lambda state: state.has(heat_mod, player))  # hot-shot
    sr("ThetaR7C10 - Shield Upgrade", rule=lambda state: state.has(pulse_mod, player))  # thunder? check this
    #
    # Boss from ThetaR6C6
    sr("ThetaR9C5 - Boss Defeated", rule=lambda state: boss_logic(2, state, world))  # TODO: check boss difficulty
    # sr("ThetaR9C5 - Key Code") # relative to boss genepod
    
    # VerdeR1C1
    # sr("ThetaR9C1 - Shield Upgrade") # might be a little tough itemless?
    # sr("VerdeR1C1 - Shield Upgrade")
    # sr("VerdeR4C3 - Shield Upgrade")
    # VerdeR7C9
    # sr("VerdeR10C7 - Security Clearance")
    sr("VerdeR4C9 - Shield Upgrade", rule=lambda state: state.has(pulse_mod, player))  # thunder
    sr("VerdeR2C10 - Stabilizer", rule=lambda state: state.has(pulse_mod, player))  # zap-shot
    sr("VerdeR9C10 - Shield Upgrade", rule=lambda state: state.has(force_mod, player))  # meteor
    sr("VerdeR5C7 - Shield Upgrade", rule=lambda state: state.has(pulse_mod, player))  # thunder
    # VerdeSW Area - note that depending on entrance, the player *may* be required to have hot-shot equipped here
    # I found this surprisingly difficult casually, I'm giving it boss logic for now
    sr("VerdeR5C2 - Force Mod", rule=lambda state: boss_logic(2, state, world) and state.has(security_clearance, player, 2))
    # sr("VerdeR5C3 - Shield Upgrade")
    # sr("VerdeR5C5 - Security Clearance")
    sr("VerdeR8C6 - Shield Upgrade", rule=lambda state: state.has(pulse_mod, player))  # thunder

    # Ramses fight, from VerdeR1C1
    sr("VerdeR1C5 - Ramses Defeated", rule=lambda state: boss_logic(1, state, world))  # TODO: check difficulty
    # sr("VerdeR1C5 - Key Code") # relative to boss genepod
    # Sura fight, or maybe Jorgensen. From either R6C5 or R7C9 genepod
    sr("VerdeR9C9 - Sura Defeated", rule=lambda state: state.has(security_clearance, player, 2)
       and boss_logic(3, state, world))  # absolute monster
    # sr("VerdeR9C9 - Key Code") # relative to boss genepod

    # Control
    # sr("Control - Shield Upgrade") # yeah I was surprised this was itemless
    # boss logic has everything you could want, but be careful if that changes
    sr("Control - Hooper Defeated", rule=lambda state: boss_logic(4, state, world))
    
    # special locations; these are gated by unique regions
    # sr("ThetaR8C3 - Shield Upgrade")
    # sr("ThetaR10C3 - Shield Upgrade")
    # sr("VerdeR7C8 - Shield Upgrade")

    # garden: same logic as heat mod
    # sr("Garden")
    # gold: check the boss defeat state
    sr("Gold", rule=lambda state: state.has("Vainger - Control - Hooper Defeated", player))
    # cherry: beating Hooper requires everything but the security clearance, so checking those two should be enough
    if "Vainger" in world.options.cherry_allowed_games:
        sr("Cherry", rule=lambda state: state.has("Vainger - Control - Hooper Defeated", player)
            and state.has(security_clearance, player, 3))
