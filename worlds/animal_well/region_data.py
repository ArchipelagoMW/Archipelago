from typing import Dict, List, NamedTuple, Optional, Union
from enum import IntEnum
from .names import ItemNames as iname, LocationNames as lname, RegionNames as rname
from .options import Goal


class AWType(IntEnum):
    location = 1
    region = 2


class LocType(IntEnum):
    bunny = 1
    candle = 2
    figure = 3
    fruit = 4


class AWData(NamedTuple):
    type: int  # location or region
    rules: List[List[str]] = [[]]  # how to access it
    # the rules are formatted such that [[wand], [disc, remote]] means you need wand OR you need disc + remote
    loc_type: Optional[int] = None
    eggs_required: int = 0
    event: Optional[str] = None  # if the location is a non-victory event, fill in what item it gives
    victory: Optional[int] = None  # if the location is a victory event, list the goal value.
    bunny_warp: bool = False  # flag for entrances not to make if bunny warp logic is off


# instructions for contributors:
# the outer string is the name of the origin region
# the inner string is the name of the destination region or location
# use AWData to specify if it's a region or location, and then put the rules in the second parameter if any
# add item names used within rules to the names.py file if any are missing
# reason: we will probably change the names of things, so this'll make it easier
# if you want to add something like an event to a rule, do so, that's fine
# this is to set them apart from the rest for now, just making it easier as we write it initially
traversal_requirements: Dict[Union[lname, rname], Dict[Union[lname, rname], AWData]] = {
    rname.bird_area: {
        lname.fruit_66:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_67:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.fish_upper:
            AWData(AWType.region),
        rname.bear_area_entry:
            AWData(AWType.region),
        rname.dog_area:
            AWData(AWType.region),
        lname.fruit_44:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.dog_upper:
            AWData(AWType.region),
        rname.bird_capybara_waterfall:  # kinda tight with the disc, but you can just make it to the egg chest
            AWData(AWType.region, [[iname.disc, iname.obscure_tricks], [iname.disc_hop],
                                   [iname.bubble_short], [iname.wheel_hard]]),
        lname.fruit_79:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.bird_below_mouse_statues:  # enter from the room where you can get the planet egg
            AWData(AWType.region, [[iname.can_break_spikes_below], [iname.disc, iname.tanking_damage]]),
        rname.frog_near_wombat:  # to the right of the bunny mural, drop down
            AWData(AWType.region),
        rname.hippo_entry:
            AWData(AWType.region, [[iname.blue_flame, iname.green_flame, iname.pink_flame, iname.violet_flame]]),
        rname.bear_truth_egg_spot:
            AWData(AWType.region, [[iname.disc_hop], [iname.bubble_long_real, iname.obscure_tricks]]),
        lname.stamp_chest:
            AWData(AWType.location),
        rname.bird_flute_chest:
            AWData(AWType.region, eggs_required=8),
        lname.pencil_chest:
            AWData(AWType.location, [[iname.bubble], [iname.disc], [iname.wheel_hop]], eggs_required=16),
        lname.top_chest:
            AWData(AWType.location, [[iname.bubble], [iname.disc], [iname.wheel_hop]], eggs_required=32),
        lname.egg_65:
            AWData(AWType.location, [[iname.bubble], [iname.disc], [iname.wheel_hop]], eggs_required=64),
        lname.victory_egg_hunt:
            AWData(AWType.location, [[iname.bubble], [iname.disc], [iname.wheel_hop]], eggs_required=64, victory=Goal.option_egg_hunt),
        lname.key_office:  # does not actually require eggs. edit if we shuffle songs
            AWData(AWType.location, [[iname.bubble_short, iname.flute], [iname.disc, iname.flute],
                                     [iname.bubble, iname.wheel_hop, iname.flute]]),
        lname.bunny_duck:  # edit rule if we shuffle songs
            AWData(AWType.location, [[iname.flute]], loc_type=LocType.bunny),
        lname.bunny_mural:
            AWData(AWType.location, [[iname.remote]], loc_type=LocType.bunny),
        lname.bunny_uv:  # probably only need uv for it
            AWData(AWType.location, [[iname.uv]], loc_type=LocType.bunny),
        lname.egg_virtual:  # sneaky passage in the top left of the screen with the penguin hedges
            AWData(AWType.location),
        rname.match_above_egg_room:
            AWData(AWType.region, [[iname.disc], [iname.bubble_short], [iname.ball_trick_easy],
                                   [iname.yoyo], [iname.top, iname.obscure_tricks],
                                   [iname.wheel_hop], [iname.wheel_climb]]),
        lname.egg_holiday:  # in the wall to the right of the egg room entrance
            AWData(AWType.location, [[iname.bubble], [iname.disc_hop], [iname.wheel_hard],
                                     [iname.flute_jump]]),
        lname.egg_rain:
            AWData(AWType.location, [[iname.top]]),
    },
    rname.bird_flute_chest: {
        lname.activate_bird_fast_travel:
            AWData(AWType.location, [[iname.flute]], event=iname.activated_bird_fast_travel),
        lname.flute_chest:
            AWData(AWType.location),
        lname.fruit_59:
            AWData(AWType.location, loc_type=LocType.fruit),
        # path to egg room isn't relevant since it's sphere 1
    },
    rname.bird_capybara_waterfall: {
        lname.egg_sweet:
            AWData(AWType.location),
    },
    rname.bird_below_mouse_statues: {
        lname.fruit_68:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_77:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_78:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.match_under_mouse_statue:
            AWData(AWType.location),
        lname.egg_planet:
            AWData(AWType.location, [[iname.can_break_spikes_below]]),
        rname.frog_travel_egg_spot:
            AWData(AWType.region, [[iname.top]]),
    },
    rname.match_above_egg_room: {
        lname.match_above_egg_room:
            AWData(AWType.location),
    },

    rname.menu: {
        rname.starting_area:
            AWData(AWType.region),
    },
    rname.starting_area: {
        rname.starting_after_ghost:  # it would feel weird to call this the central area imo
            AWData(AWType.region, [[iname.firecrackers], [iname.lantern], [iname.event_candle_first],
                                   [iname.water_bounce]]),  # speedrunner trick
        rname.candle_area:
            AWData(AWType.region, [[iname.event_candle_first, iname.event_candle_dog_dark,
                                    iname.event_candle_dog_switch_box, iname.event_candle_dog_many_switches,
                                    iname.event_candle_dog_disc_switches, iname.event_candle_dog_bat,
                                    iname.event_candle_penguin, iname.event_candle_frog, iname.event_candle_bear,
                                    iname.bubble]]),
        rname.s_disc_area:
            AWData(AWType.region, [[iname.s_medal, iname.bubble], [iname.s_medal, iname.disc_hop],
                                   [iname.s_medal, iname.wheel_hop]]),
        lname.egg_clover:  # in room where you see the status of the candles
            AWData(AWType.location),
        lname.match_start_ceiling:
            AWData(AWType.location),
        lname.bunny_face:
            AWData(AWType.location, [[iname.flute]], loc_type=LocType.bunny),
        lname.bunny_dream:
            AWData(AWType.location, loc_type=LocType.bunny),
        rname.fast_travel_fake:
            AWData(AWType.region, [[iname.flute]]),
    },
    rname.starting_after_ghost: {
        # with firecracker rando being viable, "start from 4 statue room" may be a path we want to consider
        rname.starting_area:
            AWData(AWType.region, [[iname.firecrackers], [iname.lantern], [iname.event_candle_first]]),
        rname.bird_area:
            AWData(AWType.region),
        lname.candle_first:
            AWData(AWType.location, [[iname.matchbox]], loc_type=LocType.candle),
        lname.candle_first_event:
            AWData(AWType.location, [[iname.firecrackers, iname.matchbox]], event=iname.event_candle_first),
        lname.egg_gorgeous:  # up and right of the candle
            AWData(AWType.location, [[iname.firecrackers], [iname.lantern], [iname.event_candle_first]]),
        lname.map_chest:
            AWData(AWType.location),
    },
    rname.s_disc_area: {
        lname.remote_chest:
            AWData(AWType.location),
        lname.egg_iridescent:
            AWData(AWType.location, [[iname.remote]]),
        lname.egg_ice:
            AWData(AWType.location, [[iname.remote], [iname.bubble_long], [iname.disc_hop_hard],
                                     [iname.disc_hop, iname.precise_tricks]]),
        lname.fruit_101:
            AWData(AWType.location, [[iname.remote]], loc_type=LocType.fruit),
        lname.fruit_102:
            AWData(AWType.location, [[iname.ball]], loc_type=LocType.fruit),
        lname.fruit_100:
            AWData(AWType.location, [[iname.ball]], loc_type=LocType.fruit),
        lname.egg_neon:
            AWData(AWType.location, [[iname.remote, iname.ball]]),
    },
    rname.candle_area: {
        lname.medal_e:
            AWData(AWType.location),
    },
    rname.bulb_bunny_spot: {
        lname.bunny_file_bud:
            AWData(AWType.location, loc_type=LocType.bunny),
        # brings you back to starting area so no need to include the connection back
    },

    rname.fish_upper: {
        rname.fish_wand_pit:  # enter the fish wand pit
            AWData(AWType.region),
        lname.match_fish_mural:  # right at the start, just some platforming
            AWData(AWType.location),
        lname.bunny_fish:
            AWData(AWType.location, [[iname.flute]], loc_type=LocType.bunny),
        # upper right of fish mural room leads to Virtual Egg, which you can get itemless
        # upper right of first bubble room leads to a door that requires a button hit on both sides
        lname.fruit_58:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.egg_mystic:  # avoid the fireball thrower, hit some buttons
            AWData(AWType.location),
        lname.fruit_74:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.egg_great:  # east end of the crane room
            AWData(AWType.location, [[iname.bubble], [iname.disc_hop], [iname.wheel_hop],
                                     [iname.water_bounce, iname.yoyo], [iname.water_bounce, iname.ball]]),
        lname.fruit_75:
            AWData(AWType.location, [[iname.bubble], [iname.disc_hop], [iname.wheel_hop],
                                     [iname.water_bounce, iname.yoyo], [iname.water_bounce, iname.ball]], loc_type=LocType.fruit),
        lname.fruit_73:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.egg_normal:  # hidden wall in lower left of first bubble room
            AWData(AWType.location),
        lname.egg_dazzle:  # little obstacle course, feels like the bubble jump tutorial?
            AWData(AWType.location, [[iname.bubble], [iname.disc, iname.wheel], [iname.disc_hop_hard],
                                     [iname.wheel_hard]]),
        lname.fruit_65:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_64:
            AWData(AWType.location, [[iname.bubble], [iname.disc], [iname.wheel_hop]], loc_type=LocType.fruit),
        rname.fish_tube_room:  # enter at the save room fish pipe, the rooms with all the fish pipes
            AWData(AWType.region, [[iname.bubble]]),
        lname.fruit_70:
            AWData(AWType.location, [[iname.bubble], [iname.disc], [iname.wheel_hop]], loc_type=LocType.fruit),
        lname.egg_sunset:  # break the spikes in the room to the right of the fish warp
            AWData(AWType.location, [[iname.ball], [iname.yoyo], [iname.top], [iname.disc],
                                     [iname.wheel, iname.obscure_tricks]]),  # wheel while moving into the gap
        lname.fruit_72:
            AWData(AWType.location, [[iname.ball], [iname.yoyo], [iname.top], [iname.disc], [iname.wheel]], loc_type=LocType.fruit),
        lname.fruit_71:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.water_spike_bunny_spot:
            AWData(AWType.region, [[iname.bubble_long]]),
    },
    rname.fish_wand_pit: {
        # fish_upper:  # commented out because not logically relevant
        #     AWData(AWType.region, [[iname.bubble_long], [iname.disc_hop]]),
        rname.fish_west:  # Bubble OR disc to go vertically out of the pit
            AWData(AWType.region, [[iname.bubble], [iname.disc], [iname.wheel_hop]]),
        lname.fruit_81:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.b_wand_chest:
            AWData(AWType.location),
    },
    rname.fish_west: {
        rname.fish_wand_pit: 
            AWData(AWType.region, [[iname.bubble], [iname.disc], [iname.wheel, iname.obscure_tricks]]),
        lname.fruit_54:
            AWData(AWType.location, [[iname.bubble], [iname.disc_hop_hard], [iname.wheel_hard]], loc_type=LocType.fruit),
        lname.fruit_63:
            AWData(AWType.location, [[iname.bubble], [iname.disc_hop_hard], [iname.wheel_hard]], loc_type=LocType.fruit),
        lname.egg_ancient:  # one room up and left of save point, vines in top right
        # single bubble possible, but it's much tighter than doing bubble_short, so it's not logical
            AWData(AWType.location, [[iname.bubble_short], [iname.disc_hop_hard], 
                                     [iname.wheel_hard], [iname.bubble, iname.disc]]),
        lname.fruit_53:
            AWData(AWType.location, [[iname.bubble_short], [iname.disc_hop_hard], 
                                     [iname.wheel_hard], [iname.bubble, iname.disc]], loc_type=LocType.fruit),
        rname.fish_lower:  # bubble to go down, activate switches, breakspike to pass icicles in first penguin room
            AWData(AWType.region, [[iname.bubble, iname.remote, iname.can_break_spikes],
                                   [iname.remote, iname.wheel_hop],
                                   # throwing disc to hit switch while wheel stalling is very tight
                                   [iname.disc, iname.wheel_hop, iname.precise_tricks],
                                   [iname.bubble, iname.disc],
                                   [iname.disc, iname.remote]]),
        lname.activate_fish_fast_travel:  # vertical implied by access
            AWData(AWType.location, [[iname.flute]], event=iname.activated_fish_fast_travel),
        rname.fast_travel:  # vertical implied by access
            AWData(AWType.region, [[iname.activated_fish_fast_travel]]),
        lname.fruit_69:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.egg_galaxy:
            AWData(AWType.location, [[iname.remote, iname.disc]]),
    },        
    rname.fish_tube_room: {  # no location access rules because you need bubble wand to get here anyway
        lname.fruit_55:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_56:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_57:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.egg_friendship:  # the green pipe in the fish tube room
            AWData(AWType.location),  # tight timing with no midair bubble jumps
        lname.egg_magic:  # open the gate in the fish tube room
            AWData(AWType.location),
    },
    rname.fish_lower: {
        lname.fruit_87:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.fish_west:
            AWData(AWType.region, [[iname.bubble]]),  # fish pipe left of the save point
        # reflect water while standing on ladder to skip disc req. Other reqs are for passing whale room w/o disc
        rname.fish_boss_1:
            AWData(AWType.region, [[iname.disc], [iname.obscure_tricks, iname.bubble_long], 
                                   [iname.obscure_tricks, iname.wheel_hop, iname.ball_trick_medium],
                                   [iname.obscure_tricks, iname.bubble, iname.ball_trick_medium]]),
        rname.bobcat_room:
            AWData(AWType.region, [[iname.top]]),
        lname.fruit_82:
            AWData(AWType.location, [[iname.can_break_spikes]], loc_type=LocType.fruit),
        lname.fruit_83:
            AWData(AWType.location, [[iname.can_break_spikes]], loc_type=LocType.fruit),
        lname.candle_fish:  # spike breaking presumed by access
            AWData(AWType.location, [[iname.disc, iname.matchbox], [iname.bubble, iname.matchbox]],
                   loc_type=LocType.candle),
        lname.candle_fish_event:  # spike breaking presumed by access
            AWData(AWType.location, [[iname.disc, iname.matchbox], [iname.bubble, iname.matchbox],
                                     [iname.wheel_hop, iname.matchbox]],
                   event=iname.event_candle_penguin),
        lname.egg_goodnight:
            AWData(AWType.location, [[iname.can_defeat_ghost], [iname.event_candle_penguin]]),
    },
    rname.fish_boss_1: {  # the disc required to clear this puzzle is in the entrance reqs, so not duplicated here
        lname.fruit_99:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.chest_on_spikes_region:  # the one you're supposed to get to after getting the wheel
            AWData(AWType.region, [[iname.bubble_short]]),
        rname.fish_boss_2:
            AWData(AWType.region),
        lname.egg_brick:  # disc hard required for one switch, and you can use disc to get in
            AWData(AWType.location, [[iname.disc, iname.wheel]]),
    },
    rname.chest_on_spikes_region: {
        lname.egg_scarlet:
            AWData(AWType.location, [[iname.wheel]]),
        # no connection to fish_boss_1 since you'd need to open the door in fish_boss_1
        rname.fish_boss_2:
            AWData(AWType.region),  # you can just jump down the shaft
    },
    rname.fish_boss_2: {
        lname.flame_blue:
            AWData(AWType.location, [[iname.can_open_flame]], event=iname.blue_flame),
        rname.bird_area:
            AWData(AWType.region),
        # little hole above the fish pipe. you can jump there w/o vertical if you land on the fish pipe first
        rname.abyss:
            AWData(AWType.region, [[iname.top, iname.e_medal]]),
    },
    rname.water_spike_bunny_spot: {
        lname.fruit_76:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.bunny_water_spike:  # bubble_long is covered by the region access rule
            AWData(AWType.location, loc_type=LocType.bunny),
        rname.starting_after_ghost:
            AWData(AWType.region),
    },
    rname.abyss: {
        lname.fruit_108:
            AWData(AWType.location, [[iname.top]], loc_type=LocType.fruit),
        rname.abyss_lower:
            AWData(AWType.region),
    },
    rname.abyss_lower: {
        # abyss:  # should never be relevant
        #     AWData(AWType.region, [[iname.top, iname.bubble], [iname.bubble_long]]),
        rname.uv_lantern_spot:  # for bubble, blow bubble at flute spot, then jump on left or right platform
            AWData(AWType.region, [[iname.flute, iname.disc], [iname.flute, iname.bubble], 
                                   [iname.flute, iname.wheel_hop]]),
        lname.activate_bonefish_fast_travel:
            AWData(AWType.location, [[iname.flute]], event=iname.activated_bonefish_fast_travel),
    },

    rname.bear_area_entry: {
        lname.fruit_61:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_62:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.key_bear_lower:
            AWData(AWType.location),
        rname.bear_capybara_and_below:
            AWData(AWType.region, [[iname.key_ring], [iname.bubble_short], [iname.wheel_climb]]),
        rname.bear_transcendental:  # might be controversial? it's across a screen transition but only 4 bubbles
            AWData(AWType.region, [[iname.bubble_short], [iname.disc_hop_hard]]),
        rname.bear_kangaroo_waterfall:
            AWData(AWType.region, [[iname.slink], [iname.top, iname.yoyo], [iname.top, iname.ball],
                                   [iname.ball_trick_easy]]),  # stand on left button, throw ball neutral
        rname.bear_razzle_egg_spot:
            AWData(AWType.region, [[iname.defeated_chameleon, iname.bubble_short],
                                   [iname.defeated_chameleon, iname.disc_hop_hard],
                                   [iname.defeated_chameleon, iname.wheel_hop]]),
    },
    rname.bear_capybara_and_below: {
        lname.fruit_31:
            AWData(AWType.location, [[iname.bubble_short], [iname.disc], [iname.wheel_hop]], loc_type=LocType.fruit),
        lname.fruit_32:
            AWData(AWType.location, [[iname.bubble_short], [iname.disc], [iname.wheel_hop]], loc_type=LocType.fruit),
        lname.fruit_33:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_34:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.bear_future_egg_room:
            AWData(AWType.region),
        lname.key_bear_upper:
            AWData(AWType.location),
        rname.zen_egg_spot:
            AWData(AWType.region, [[iname.bubble], [iname.disc], [iname.wheel_hop]]),
        lname.fruit_51:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.bear_dark_maze:  # need one key to open the gate, or do downward bubbles to get to the button
            AWData(AWType.region, [[iname.key_ring], [iname.bubble_short, iname.precise_tricks],
                                   [iname.ball_trick_medium]]),  # or hit it with a ball
        rname.value_egg_spot:
            AWData(AWType.region, [[iname.bubble_short], [iname.disc], [iname.wheel_climb]]),
    },
    rname.zen_egg_spot: {
        lname.egg_zen:
            AWData(AWType.location),
        lname.fruit_41:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.egg_universal:
            AWData(AWType.location, [[iname.firecrackers], [iname.yoyo], [iname.disc], [iname.wheel]]),
        rname.bear_capybara_and_below:  # just drop down into the chinchilla room. key chest handled there.
            AWData(AWType.region)
    },
    rname.value_egg_spot: {  # broke this one out into its own region because the reqs were getting really big
        lname.egg_value:
            AWData(AWType.location, [[iname.firecrackers], [iname.disc_hop_hard], 
                                     [iname.flute], [iname.ball_trick_medium]]),
    },
    rname.bear_future_egg_room: {
        lname.egg_future:  # chinchilla on the moving platforms puzzle room
            AWData(AWType.location),
        lname.fruit_52:
            AWData(AWType.location, loc_type=LocType.fruit),
    },
    rname.bear_chinchilla_song_room: {
        lname.bunny_chinchilla_vine:
            AWData(AWType.location, loc_type=LocType.bunny),
        rname.bear_future_egg_room:
            AWData(AWType.region, bunny_warp=True),
    },
    rname.bear_dark_maze: {
        rname.bear_chameleon_room_1:
            AWData(AWType.region),
        lname.candle_bear:
            AWData(AWType.location, [[iname.bubble, iname.matchbox], [iname.disc, iname.matchbox],
                                     [iname.wheel_hop, iname.matchbox]],
                   loc_type=LocType.candle),
        lname.candle_bear_event:
            AWData(AWType.location, [[iname.bubble, iname.matchbox], [iname.disc, iname.matchbox],
                                     [iname.wheel_hop, iname.matchbox]],
                   event=iname.event_candle_bear),
        lname.fruit_49:
            AWData(AWType.location, [[iname.bubble], [iname.disc], [iname.wheel_hop]], loc_type=LocType.fruit),
        lname.fruit_50:
            AWData(AWType.location, [[iname.bubble], [iname.disc], [iname.wheel_hop]], loc_type=LocType.fruit),
        lname.egg_lf:
            AWData(AWType.location, [[iname.firecrackers, iname.bubble], [iname.firecrackers, iname.disc],
                                     [iname.firecrackers, iname.wheel_hop]]),
    },
    rname.bear_chameleon_room_1: {
        rname.bear_dark_maze:
            AWData(AWType.region, [[iname.bubble], [iname.disc]]),
        rname.bear_ladder_after_chameleon:
            AWData(AWType.region),
        lname.medal_s:
            AWData(AWType.location, [[iname.defeated_chameleon]]),
    },
    rname.bear_ladder_after_chameleon: {
        lname.fruit_48:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.bear_slink_room:  # jump up through the floor at the top of the ladder
            AWData(AWType.region),
    },
    rname.bear_slink_room: {
        lname.slink_chest:
            AWData(AWType.location),
        rname.bear_slink_room_doors:
            AWData(AWType.region, [[iname.slink], [iname.top], [iname.ball_trick_easy]]),
        # bear_area_entry:  # unnecessary because it's a sphere 1 area
        #     AWData(AWType.region),
    },
    rname.bear_slink_room_doors: {
        rname.bear_transcendental:  # descend, jump into left wall, or disc hop from the platforms underneath
            AWData(AWType.region, [[iname.bubble], [iname.disc_hop], [iname.flute_jump]]),
    },
    rname.bear_transcendental: {
        lname.egg_transcendental:
            AWData(AWType.location),
    },
    rname.bear_kangaroo_waterfall: {
        lname.fruit_47:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.bear_ladder_after_chameleon:
            AWData(AWType.region),  # just press a button
        rname.bear_slink_room:
            AWData(AWType.region, [[iname.bubble], [iname.disc_hop], [iname.wheel_hop]]),  # just go up
        lname.fruit_40:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_29:
            AWData(AWType.location, loc_type=LocType.fruit),
        # just throw the ball into the hole, it'll hit the yellow button like 99% of the time
        rname.bear_middle_phone_room:
            AWData(AWType.region, [[iname.slink], [iname.ball_trick_easy]]),
        lname.egg_post_modern:
            AWData(AWType.location, [[iname.top, iname.switch_for_post_modern_egg]]),
        rname.bear_truth_egg_spot:  # throw disc to the right after jumping down the waterfall
            AWData(AWType.region, [[iname.disc]]),
        rname.bear_transcendental:  # todo: figure out which bubble, which disc option
            AWData(AWType.region, [[iname.wheel_hop], [iname.bubble]]),
        rname.zen_egg_spot:  # secret pathway just before middle phone room
            AWData(AWType.region, [[iname.top]]),
    },
    rname.bear_truth_egg_spot: {
        lname.fruit_45:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.egg_truth:
            AWData(AWType.location),
        rname.bear_kangaroo_waterfall:
            AWData(AWType.region),
    },
    rname.bear_middle_phone_room: {
        lname.fruit_23:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.activate_bear_fast_travel:
            AWData(AWType.location, [[iname.flute]], event=iname.activated_bear_fast_travel),
        rname.fast_travel:
            AWData(AWType.region, [[iname.activated_bear_fast_travel]]),
        lname.egg_chaos:  # in the room with the monkey that throws rocks at you
            AWData(AWType.location),
        lname.fruit_24:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.bear_crow_rooms:
            AWData(AWType.region, [[iname.slink], [iname.ball_trick_hard]]),
        # shoot some hoops! throw the ball to the button. can be done without vertical if you throw early
        rname.bear_match_chest_spot:
            AWData(AWType.region, [[iname.ball_trick_medium], [iname.bubble, iname.tanking_damage],
                                   [iname.bubble_long_real, iname.lantern],
                                   [iname.disc, iname.tanking_damage, iname.precise_tricks],
                                   [iname.wheel_climb, iname.tanking_damage]]),
        rname.bear_chameleon_room_2:
            AWData(AWType.region, [[iname.bubble_long, iname.tanking_damage],
                                   [iname.disc_hop_hard, iname.tanking_damage, iname.precise_tricks],
                                   [iname.wheel_hard, iname.tanking_damage, iname.precise_tricks],
                                   [iname.bubble_long_real, iname.lantern]]),  # preset your bubbles then lantern jump up
    },
    rname.bear_crow_rooms: {
        rname.bear_shadow_egg_spot:  # get across the room with the lifters and the miasma
            AWData(AWType.region, [[iname.slink], [iname.lantern], [iname.tanking_damage]]),
        lname.bunny_crow:  # it jumps down after a moment
            AWData(AWType.location, [[iname.flute]], loc_type=LocType.bunny),
        rname.bear_hedgehog_square:  # slink needed for puzzle to get to the button
            AWData(AWType.region, [[iname.slink], [iname.ball_trick_hard]]),
    },
    rname.bear_shadow_egg_spot: {
        lname.egg_shadow:
            AWData(AWType.location),
        rname.bear_crow_rooms:
            AWData(AWType.region),
    },
    rname.bear_hedgehog_square: {
        lname.fruit_30:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.bunny_ghost_dog:  # flute is to make it less tedious mostly
            AWData(AWType.location, [[iname.m_disc, iname.flute, iname.activated_bear_fast_travel],
                                     [iname.m_disc, iname.precise_tricks]],  # you don't /need/ flute
                   loc_type=LocType.bunny),
        rname.bear_connector_passage:
            AWData(AWType.region, [[iname.slink]]),
    },
    rname.bear_connector_passage: {
        rname.bear_capybara_and_below:
            AWData(AWType.region),
        rname.bear_middle_phone_room:
            AWData(AWType.region),
        # starting here, use slink to open a path to open the door to the match chest
        rname.bear_match_chest_spot:
            AWData(AWType.region, [[iname.slink]]),
    },
    rname.bear_match_chest_spot: {
        lname.match_bear:
            AWData(AWType.location),
        rname.chocolate_egg_spot:
            # wall juts out, need bubble or mid-air jump
            AWData(AWType.region, [[iname.bubble], [iname.wheel_hard],
                                   [iname.flute_jump]]),
        rname.match_center_well_spot:
            AWData(AWType.region),  # wall is flush, just hold left
        rname.bear_truth_egg_spot:
            # fall down the shaft, catch yourself on a bubble, and jump right quickly before the bird pops it
            AWData(AWType.region, [[iname.wheel_hard], [iname.bubble, iname.precise_tricks]]),
        # top_of_the_well:  # unnecessary because of the connection from match center spot
        #     AWData(AWType.region, [[iname.bubble_long]]),
        rname.bear_upper_phone_room:
            AWData(AWType.region, [[iname.slink, iname.yoyo],
                                   # throw the ball in the yoyo pipe then run left with yoyo or slink
                                   [iname.slink, iname.ball_trick_easy],
                                   [iname.yoyo, iname.ball_trick_easy]]),
        rname.bear_middle_phone_room:
            AWData(AWType.region, [[iname.bubble, iname.tanking_damage],
                                   [iname.bubble_long_real, iname.lantern],
                                   [iname.disc, iname.tanking_damage, iname.precise_tricks],
                                   [iname.wheel_climb, iname.tanking_damage]]),
    },
    rname.bear_upper_phone_room: {
        lname.fruit_8:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_9:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.bear_above_chameleon:
            AWData(AWType.region, [[iname.yoyo], [iname.ball_trick_medium, iname.obscure_tricks],
                                   [iname.slink, iname.bubble, iname.obscure_tricks],
                                   [iname.disc, iname.slink, iname.obscure_tricks],
                                   [iname.disc, iname.top, iname.obscure_tricks]]),
    },
    rname.bear_above_chameleon: {  # includes the screens to the right of it
        lname.egg_swan:  # wake one chinchilla, lure upper one right, run left
            AWData(AWType.location, [[iname.flute], [iname.firecrackers]]),
        # chinchilla can be woken up with flute or firecrackers
        # otters can be distracted with firecrackers, yoyo, or top
        # you need 3 firecrackers minimum if you want to get through without yoyo or flute
        # alternatively, use ball to hit the two door switches + the trapdoor switch
        lname.fruit_10:
            AWData(AWType.location, [[iname.slink, iname.yoyo, iname.flute], [iname.slink, iname.firecrackers]], loc_type=LocType.fruit),
        rname.bear_shadow_egg_spot:
            AWData(AWType.region, [[iname.top, iname.slink, iname.yoyo, iname.flute],
                                   [iname.top, iname.slink, iname.firecrackers]]),
        rname.bear_chameleon_room_2:
            AWData(AWType.region, [[iname.yoyo, iname.slink, iname.flute],
                                   [iname.yoyo, iname.slink, iname.firecrackers],
                                   # hitting lower button with ball is medium, hitting upper through 1way is hard.
                                   [iname.flute, iname.ball_trick_medium],
                                   [iname.firecrackers, iname.ball_trick_medium],
                                   [iname.bubble, iname.ball_trick_hard],
                                   [iname.disc, iname.ball_trick_hard],
                                   [iname.wheel_hop, iname.ball_trick_hard]]),
    },
    rname.bear_chameleon_room_2: {
        rname.bear_middle_phone_room:  # drop down, probably unimportant
            AWData(AWType.region),
        lname.defeated_chameleon:
            AWData(AWType.location, event=iname.defeated_chameleon),
        lname.fruit_16:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.flame_violet:
            AWData(AWType.location, [[iname.can_open_flame]], event=iname.violet_flame),
        lname.fruit_15:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.bear_upper_phone_room:
            AWData(AWType.region),
    },
    rname.bear_razzle_egg_spot: {
        lname.fruit_60:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.egg_razzle:
            AWData(AWType.location),
        rname.bear_dark_maze:
            AWData(AWType.region),
    },
    rname.bear_map_bunny_spot: {
        lname.bunny_map:
            AWData(AWType.location, loc_type=LocType.bunny),
        rname.bear_kangaroo_waterfall:
            AWData(AWType.region, bunny_warp=True),  # drop down after getting the bunny
    },

    rname.dog_area: {
        lname.disc_spot:
            AWData(AWType.location, [[iname.m_disc]], event=iname.disc),
        lname.fruit_38:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.candle_dog_dark:
            AWData(AWType.location, [[iname.matchbox]], loc_type=LocType.candle),
        lname.fruit_42:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.candle_dog_dark_event:
            AWData(AWType.location, [[iname.matchbox]], event=iname.event_candle_dog_dark),
        rname.dog_chinchilla_skull:  # hit a switch with any number of things, or jump up there yourself
            AWData(AWType.region, [[iname.bubble], [iname.remote], [iname.disc], [iname.ball_trick_easy],
                                   [iname.wheel_hop], [iname.top, iname.obscure_tricks]]),
        rname.dog_upside_down_egg_spot:  # upper right of switch platform room above second dog
            AWData(AWType.region, [[iname.bubble_short]]),
        lname.fruit_36:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_37:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.dog_at_mock_disc:  # you drop down to here, but can't get back up immediately
            AWData(AWType.region),
        lname.egg_orange:
            AWData(AWType.location, [[iname.top]]),
    },
    rname.dog_upside_down_egg_spot: {
        lname.egg_upside_down:
            AWData(AWType.location),
        rname.dog_area:
            AWData(AWType.region),
        rname.dog_many_switches:
            AWData(AWType.region, [[iname.remote]]),
    },
    rname.dog_at_mock_disc: {
        lname.mock_disc_chest:
            AWData(AWType.location),
        rname.dog_area:  # can leave by letting the dachshund chase you out
            AWData(AWType.region),
        lname.egg_sour:  # when escaping the dachsund, jump up and right out of the tunnel
            AWData(AWType.location),
        lname.fruit_43:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.bird_area:  # after the sour egg chest, you escape to the central area
            AWData(AWType.region),
    },
    rname.dog_chinchilla_skull: {
        lname.egg_red:  # use a firecracker to scare them, or throw a disc between them
            AWData(AWType.location, [[iname.firecrackers], [iname.disc]])
    },
    rname.dog_upper: {
        rname.dog_upper_past_lake:  # enter with the switch pre-flipped to make sure you can pass the switch box room
            AWData(AWType.region, [[iname.disc_hop], [iname.bubble_long], [iname.flute, iname.bubble_short]]),
        rname.dog_upper_above_switch_lines:
            AWData(AWType.region, [[iname.disc], [iname.remote], [iname.top]]),
        lname.egg_evil:
            AWData(AWType.location, [[iname.flute]]),
        lname.fruit_28:
            AWData(AWType.location, loc_type=LocType.fruit),
    },
    rname.dog_upper_past_lake: {
        # logical note: there's several items that can get past switch box, but you're logically guaranteed
        # to have one of them to get to this region, so it's accounted for.
        lname.candle_dog_switch_box:
            AWData(AWType.location, [[iname.matchbox]], loc_type=LocType.candle),
        lname.candle_dog_switch_box_event:
            AWData(AWType.location, [[iname.matchbox]], event=iname.event_candle_dog_switch_box),
        rname.dog_upper_above_switch_lines:
            AWData(AWType.region, [[iname.can_distract_dogs], [iname.tanking_damage]]),  # need to get past the 3 dogs
        lname.fruit_18:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.barcode_bunny:  # region since you can get this in two spots
            AWData(AWType.region, [[iname.flute]]),
        lname.mama_cha:  # removing for now, may shuffle later
            AWData(AWType.location, [[iname.flute]], loc_type=LocType.figure),  # add song req if we're shuffling songs
        lname.bunny_lava:
            AWData(AWType.location, [[iname.bubble_long, iname.remote]], loc_type=LocType.bunny),
        rname.dog_many_switches:
            AWData(AWType.region, [[iname.ball_trick_medium], [iname.yoyo], [iname.disc], [iname.wheel, iname.bubble],
                                   [iname.wheel_hop], [iname.top]]),
        rname.dog_under_fast_travel_room:  # very tight, need to jump from the lower ledge one room to the right
            AWData(AWType.region, [[iname.switch_next_to_bat_room], [iname.bubble_short], [iname.disc_hop],
                                   [iname.wheel_climb]]),
    },
    rname.dog_under_fast_travel_room: {
        rname.dog_upper_past_lake:
            AWData(AWType.region, [[iname.bubble_short]]),
        rname.dog_fast_travel_room:  # wheel can allow you to crank safely. not usable at most other dogs
            AWData(AWType.region, [[iname.can_distract_dogs], [iname.bubble_long], [iname.wheel]]),
    },
    rname.dog_fast_travel_room: {
        rname.dog_under_fast_travel_room:
            AWData(AWType.region),
        lname.activate_dog_fast_travel:
            AWData(AWType.location, [[iname.flute]], event=iname.activated_dog_fast_travel),
        lname.fruit_12:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_11:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.dog_swordfish_lake_ledge:
            AWData(AWType.region, [[iname.disc], [iname.bubble_long_real], [iname.bubble_long, iname.precise_tricks]]),
        rname.dog_upper_past_lake:  # ride bubble down, jump the partial-height wall
            AWData(AWType.region, [[iname.bubble]]),
        # disc: go across lake, then go back at higher elevation. wheel_hop: jump off the moving block
        rname.dog_above_fast_travel:
            AWData(AWType.region, [[iname.slink], [iname.bubble_short], [iname.disc], [iname.wheel_hop]]),
        rname.dog_mock_disc_shrine:
            AWData(AWType.region, [[iname.slink], [iname.wheel_hop], [iname.top, iname.precise_tricks]]),
    },
    rname.dog_mock_disc_shrine: {
        lname.fruit_5:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_6:
            AWData(AWType.location, [[iname.disc], [iname.bubble], [iname.wheel_hop], [iname.key_ring], 
                                     [iname.can_break_spikes], [iname.remote, iname.obscure_tricks]], loc_type=LocType.fruit),
        lname.fruit_4:
            AWData(AWType.location, [[iname.disc_hop_hard], [iname.bubble_short], [iname.wheel_hop], [iname.key_ring]], loc_type=LocType.fruit),
        lname.egg_raw:
            AWData(AWType.location, [[iname.slink, iname.disc_hop_hard],
                                     [iname.slink, iname.bubble_short],
                                     [iname.slink, iname.wheel_hop],
                                     [iname.slink, iname.key_ring]]),
        lname.flame_pink:
            AWData(AWType.location, [[iname.m_disc, iname.can_open_flame]], event=iname.pink_flame),
        lname.fruit_13:
            AWData(AWType.location, [[iname.m_disc]], loc_type=LocType.fruit),
        rname.dog_elevator_middle:
            AWData(AWType.region, [[iname.m_disc]]),
        rname.dog_upper_east:
            AWData(AWType.region),  # hit one-way switch to go down
    },
    rname.dog_above_fast_travel: {
        lname.fruit_3:
            AWData(AWType.location, [[iname.top]], loc_type=LocType.fruit),
        lname.egg_brown:
            AWData(AWType.location, [[iname.slink]]),
        lname.fruit_2:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.egg_reference:  # funny slink and disc room
            AWData(AWType.location, [[iname.slink, iname.disc]]),
        rname.dog_fast_travel_room:
            AWData(AWType.region),
        lname.egg_crystal:
            AWData(AWType.location, [[iname.top, iname.ball, iname.remote, iname.wheel, iname.slink],
                                     # rooby's version
                                     [iname.top, iname.ball, iname.remote, iname.wheel, iname.disc, iname.obscure_tricks],
                                     # 8's version
                                     [iname.top, iname.wheel_hop, iname.obscure_tricks, iname.precise_tricks],
                                     # who needs a wheel anyway
                                     [iname.top, iname.bubble_long, iname.obscure_tricks, iname.precise_tricks]]),
    },
    rname.dog_swordfish_lake_ledge: {
        rname.dog_fast_travel_room:
            AWData(AWType.region, [[iname.disc]]),
        lname.egg_forbidden:
            AWData(AWType.location),
        lname.bunny_disc_spike:  # not disc hop since you literally need to do this
            AWData(AWType.location, [[iname.disc_hop_hard], [iname.bubble_long, iname.wheel_hop, iname.precise_tricks]],
                   loc_type=LocType.bunny),
        lname.fruit_0:
            AWData(AWType.location, [[iname.disc_hop_hard], [iname.bubble, iname.disc],
                                     [iname.bubble_long]], loc_type=LocType.fruit),
        lname.fruit_1:
            AWData(AWType.location, [[iname.disc_hop_hard], [iname.bubble_long, iname.wheel_hop, iname.precise_tricks]],
                   loc_type=LocType.fruit),
        rname.behind_kangaroo:
            AWData(AWType.region, [[iname.slink]]),
    },
    rname.behind_kangaroo: {
        rname.bear_middle_phone_room:
            AWData(AWType.region),  # activate dynamite
        rname.dog_swordfish_lake_ledge:
            AWData(AWType.region, [[iname.top]]),  # destroy blocks under block by forbidden egg chest
        lname.egg_plant:
            AWData(AWType.location, [[iname.disc, iname.slink], [iname.bubble_short, iname.obscure_tricks]]),
        lname.fruit_35:
            AWData(AWType.location, [[iname.disc, iname.slink], [iname.bubble_short, iname.obscure_tricks]], loc_type=LocType.fruit),
        rname.kangaroo_blocks:
            AWData(AWType.region, [[iname.ball]]),
    },
    rname.dog_many_switches: {
        lname.candle_dog_many_switches:
            AWData(AWType.location, [[iname.matchbox]], loc_type=LocType.candle),
        lname.candle_dog_many_switches_event:
            AWData(AWType.location, [[iname.matchbox]], event=iname.event_candle_dog_many_switches),
        rname.dog_upside_down_egg_spot:  # throw a disc or top at a switch
            AWData(AWType.region, [[iname.remote], [iname.disc], [iname.top], [iname.ball_trick_easy]]),
        rname.dog_bat_room:
            AWData(AWType.region),
    },
    rname.dog_bat_room: {
        lname.fruit_17:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.candle_dog_bat:
            AWData(AWType.location, [[iname.matchbox]], loc_type=LocType.candle),
        lname.candle_dog_bat_event:
            AWData(AWType.location, [[iname.matchbox]], event=iname.event_candle_dog_bat),
        lname.key_dog:
            AWData(AWType.location),
        lname.switch_next_to_bat_room:
            AWData(AWType.location, event=iname.switch_next_to_bat_room),
        lname.egg_service:
            AWData(AWType.location),
        rname.kangaroo_room:
            AWData(AWType.region),  # this one is done in region scripts to account for the number of k shards
    },
    rname.kangaroo_room: {
        rname.dog_bat_room:
            AWData(AWType.region),
        lname.b_ball_chest:
            AWData(AWType.location),
        lname.fruit_25:
            AWData(AWType.location, [[iname.can_break_spikes]], loc_type=LocType.fruit),
        lname.fruit_26:
            AWData(AWType.location, [[iname.can_break_spikes]], loc_type=LocType.fruit),
        lname.fruit_27:
            AWData(AWType.location, [[iname.can_break_spikes]], loc_type=LocType.fruit),
        rname.kangaroo_blocks:
            AWData(AWType.region, [[iname.ball, iname.disc], [iname.ball, iname.bubble]]),
    },
    rname.kangaroo_blocks: {
        rname.kangaroo_room:
            AWData(AWType.region),
        lname.egg_vanity:
            AWData(AWType.location),
        rname.behind_kangaroo:
            AWData(AWType.region),
    },
    rname.dog_upper_above_switch_lines: {
        lname.match_dog_switch_bounce:  # in the little switch area
            AWData(AWType.location, [[iname.disc], [iname.remote], [iname.top]]),
        lname.fruit_19:
            AWData(AWType.location, [[iname.disc], [iname.remote], [iname.top]], loc_type=LocType.fruit),
        lname.candle_dog_disc_switches:
            AWData(AWType.location, [[iname.disc, iname.matchbox], [iname.remote, iname.matchbox],
                                     [iname.top, iname.matchbox]], loc_type=LocType.candle),
        lname.candle_dog_disc_switches_event:
            AWData(AWType.location, [[iname.disc, iname.matchbox], [iname.remote, iname.matchbox],
                                     [iname.top, iname.matchbox]], event=iname.event_candle_dog_disc_switches),
        lname.egg_depraved:  # in the little switch area, you need to take care of the ghost
            AWData(AWType.location, [[iname.disc, iname.can_defeat_ghost],
                                     [iname.remote, iname.can_defeat_ghost],
                                     [iname.top, iname.can_defeat_ghost],
                                     [iname.disc, iname.event_candle_dog_disc_switches],
                                     [iname.remote, iname.event_candle_dog_disc_switches],
                                     [iname.top, iname.event_candle_dog_disc_switches]]),
        rname.dog_upper_above_switch_lines_to_upper_east:
            AWData(AWType.region, [[iname.disc], [iname.remote], [iname.top]]),
        rname.dog_upper_past_lake:
            AWData(AWType.region, [[iname.disc], [iname.top],
                                   [iname.remote, iname.can_distract_dogs],
                                   [iname.remote, iname.tanking_damage]]),
    },
    rname.dog_upper_above_switch_lines_to_upper_east: {
        rname.dog_upper_above_switch_lines:
            AWData(AWType.region),  # hit button, walk into the hallway
        rname.dog_upper_east:
            AWData(AWType.region),
    },
    rname.dog_upper_east: {
        lname.fruit_20:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_21:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.dog_upper_above_switch_lines_to_upper_east:
            AWData(AWType.region, [[iname.bubble_short]]),  # jump up to the switch
        lname.match_dog_upper_east:
            AWData(AWType.location),
        rname.dog_upper:  # hit the dynamite switch to get back to the bird area and upper dog
            AWData(AWType.region),
        rname.frog_dark_room:  # take the bubble pipe by the dynamite, this is the really long pipe
            AWData(AWType.region, [[iname.bubble]]),
        rname.dog_elevator:
            AWData(AWType.region, [[iname.slink], [iname.ball_trick_hard]]),
        rname.match_center_well_spot:  # not connected to dog elevator directly because of the dog plinko doors
            AWData(AWType.region, [[iname.slink], [iname.ball_trick_hard]]),
    },
    rname.dog_elevator: {
        lname.switch_for_post_modern_egg:
            AWData(AWType.location, event=iname.switch_for_post_modern_egg),
        rname.dog_wheel:
            AWData(AWType.region, [[iname.remote]]),
        rname.dog_elevator_upper:  # no direct connection to middle due to indirect connection through upper
            AWData(AWType.region, [[iname.dog_wheel_flip]]),
        lname.fruit_46:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.match_above_egg_room:  # if the switch is flipped right you can just get this chest
            AWData(AWType.region),
    },
    rname.dog_wheel: {
        # bird_area:
        #     AWData(AWType.region),
        lname.fruit_39:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.dog_wheel_flip:
            AWData(AWType.location, [[iname.yoyo]], event=iname.dog_wheel_flip),
    },
    rname.dog_elevator_upper: {
        lname.egg_big:
            AWData(AWType.location),
        lname.fruit_7:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.dog_elevator_middle:
            AWData(AWType.region),
        rname.bear_match_chest_spot:
            AWData(AWType.region, [[iname.bubble]]),
    },
    rname.dog_elevator_middle: {
        lname.fruit_14:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_22:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.dog_elevator:  # no connection to upper due to redundant connection with dog_elevator
            AWData(AWType.region),
    },

    rname.frog_near_wombat: {
        lname.fruit_86:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.candle_frog:
            AWData(AWType.location, [[iname.matchbox]], loc_type=LocType.candle),
        lname.candle_frog_event:
            AWData(AWType.location, [[iname.matchbox]], event=iname.event_candle_frog),
        lname.fruit_80:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.egg_moon:  # the one with all the mouse heads
            AWData(AWType.location, [[iname.disc, iname.lantern], [iname.bubble, iname.lantern]]),
            # bubble short or maybe just bubble? You have to shoot down at the apex of your jump, feels weird
            # I was getting this 90% of the time, not sure it's intuitive? make it logical and put it in the tricks FAQ.
        lname.egg_promise:  # under spikes in 3 bird room, solve puzzle then can break spikes without bird in the way
            # fall onto spikes while throwing disc to the left with good timing to break a path
            AWData(AWType.location, [[iname.can_break_spikes_below], [iname.disc, iname.tanking_damage]]),
        lname.fruit_93:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.frog_under_ostrich_statue:  # after hitting the switch, no items needed
            AWData(AWType.region),
        rname.frog_travel_egg_spot:
            AWData(AWType.region, [[iname.key_ring]]),
        rname.frog_pre_ostrich_attack:
            AWData(AWType.region, [[iname.top]]),
    },
    rname.frog_travel_egg_spot: {  # the spot behind the groundhog
        lname.fruit_85:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.egg_travel:
            AWData(AWType.location),
        rname.frog_ostrich_attack:
            AWData(AWType.region, [[iname.yoyo], [iname.ball_trick_easy]]),
        rname.frog_near_wombat:
            AWData(AWType.region, [[iname.key_ring]]),  # assuming the key can open it from the left
    },
    rname.frog_under_ostrich_statue: {
        rname.frog_near_wombat:  # may have to go a few screens away to hit a switch, but you don't need items
            AWData(AWType.region),
        lname.fruit_92:
            AWData(AWType.location, [[iname.disc], [iname.ball], [iname.yoyo], [iname.top]], loc_type=LocType.fruit),
        lname.egg_bubble:  # top right of room with the mouse ghost that throws its head
            AWData(AWType.location, [[iname.bubble], [iname.disc]]),
        rname.frog_pre_ostrich_attack:
            AWData(AWType.region),
    },
    rname.frog_pre_ostrich_attack: {
        rname.frog_ostrich_attack:
            AWData(AWType.region),
    },
    rname.frog_ostrich_attack: {
        lname.fruit_84:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.key_chest_mouse_head_lever:
            AWData(AWType.location),
        lname.egg_dream:  # right after the key chest
            AWData(AWType.location),
        rname.bird_area:  # door switch to get you out under the bunny mural
            AWData(AWType.region),
        lname.fruit_91:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.frog_worm_shaft_top:
            AWData(AWType.region),
    },
    rname.frog_worm_shaft_top: {
        lname.fruit_90:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.egg_fire:  # after ostrich attack room
            AWData(AWType.location, [[iname.disc], [iname.bubble_short]]),
        rname.frog_worm_shaft_bottom:
            AWData(AWType.region),
    },
    rname.frog_worm_shaft_bottom: {
        lname.fruit_109:
            AWData(AWType.location, loc_type=LocType.fruit),
        rname.frog_worm_shaft_top:
            AWData(AWType.region, [[iname.bubble_long]]),  # climb the shaft above the save point
        lname.yoyo_chest:
            AWData(AWType.location),
        rname.frog_bird_after_yoyo_1:  # can bypass the locked door with bubble jumps + lantern
            AWData(AWType.region, [[iname.yoyo], [iname.bubble_long, iname.lantern], [iname.ball_trick_hard],
                                   # spam bubbles then jump up the left side
                                   [iname.bubble_long, iname.precise_tricks]]),
    },
    rname.frog_bird_after_yoyo_1: {
        rname.frog_bird_after_yoyo_2:  # pain in the ass, but you can get up with downwards bubbles
            AWData(AWType.region, [[iname.yoyo], [iname.bubble_long], [iname.ball_trick_medium]]),
        rname.frog_worm_shaft_bottom:  # if you fall along the left side, the bird doesn't reach you in time
            AWData(AWType.region, [[iname.obscure_tricks], [iname.lantern]]),
        lname.egg_sapphire:
            AWData(AWType.location, [[iname.lantern]]),
    },
    rname.frog_bird_after_yoyo_2: {  # this is where the fast travel activator is
        lname.activate_frog_fast_travel:
            AWData(AWType.location, [[iname.flute]], event=iname.activated_frog_fast_travel),
        lname.fruit_95:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_94:
            AWData(AWType.location, [[iname.key_ring]], loc_type=LocType.fruit),
        lname.key_frog_guard_room_west:  # you can just throw the ball at their shields lmao
            AWData(AWType.location, [[iname.yoyo], [iname.flute], [iname.ball]]),
        lname.match_guard_room:  # hit guard then jump off its head, or jump up with mobility
            AWData(AWType.location, [[iname.yoyo], [iname.flute], [iname.disc_hop],
                                     [iname.bubble], [iname.ball]]),
        # 2 doors in the top right of this region
        lname.fruit_96:
            AWData(AWType.location, [[iname.yoyo], [iname.flute], [iname.ball]], loc_type=LocType.fruit),
        lname.key_frog_guard_room_east:
            AWData(AWType.location, [[iname.yoyo], [iname.bubble, iname.flute], 
                                     [iname.ball], [iname.flute_jump]]),
        rname.frog_dark_room:  # yoyo to open the door, lantern to fall through the bird, or ball to hit buttons
            AWData(AWType.region, [[iname.yoyo], [iname.lantern], [iname.ball_trick_easy]]),
        rname.frog_ruby_egg_ledge:  # fall through a bird onto it
            AWData(AWType.region, [[iname.lantern]]),
        rname.frog_east_of_fast_travel:  # yoyo or ball to open the doors
            AWData(AWType.region, [[iname.yoyo], [iname.ball_trick_easy]]),
        rname.frog_pre_ostrich_attack:  # needs 2 keys, but that's never relevant because of consumable key logic
            AWData(AWType.region, [[iname.key_ring]]),
    },
    rname.frog_dark_room: {
        lname.fruit_106:
            AWData(AWType.location, loc_type=LocType.fruit),
        # jump up at rust egg w/ lantern, or yoyo/ball to open the doors, or get past bird with well-timed bubble jumps
        rname.frog_bird_after_yoyo_2:
            AWData(AWType.region, [[iname.lantern], [iname.yoyo], [iname.bubble_short, iname.precise_tricks],
                                   [iname.ball_trick_easy]]),
        lname.egg_rust:  # top left of the dark room
            AWData(AWType.location),
        lname.egg_jade:  # do the puzzle
            AWData(AWType.location),
        rname.bird_capybara_waterfall:  # fish pipe to the sweet egg room
            AWData(AWType.region, [[iname.bubble]]),
        # wake the frog or just jump up there, can use flute or firecrackers to get the frog jumping
        rname.frog_ruby_egg_ledge:
            AWData(AWType.region, [[iname.bubble_short], [iname.disc], [iname.top, iname.flute],
                                   [iname.top, iname.firecrackers]]),
        rname.frog_east_of_fast_travel:
            AWData(AWType.region, [[iname.yoyo], [iname.ball_trick_easy]]),
        rname.fast_travel:
            AWData(AWType.region, [[iname.activated_frog_fast_travel]])
    },
    rname.frog_east_of_fast_travel: {
        # lname.kangaroo_first_spot:
        #     AWData(AWType.location),
        rname.frog_elevator_and_ostrich_wheel:
            AWData(AWType.region, [[iname.yoyo, iname.bubble]]),
        # logically requires bubble only -- you need vertical to get past the ledge. If that vertical isn't bubble,
        # then you can softlock yourself if you have yoyo and switch elevator directions
        # since bubble is required if you have yoyo, then this check only actually requires bubble
        # it's in this region so that we don't mess with the rest of the logic for that area
        lname.egg_desert:
            AWData(AWType.location, [[iname.bubble]]),
    },
    rname.frog_ruby_egg_ledge: {
        lname.egg_ruby:  # this whole region just for one egg
            AWData(AWType.location),
    },
    rname.frog_elevator_and_ostrich_wheel: {
        lname.fruit_97:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_98:
            AWData(AWType.location, [[iname.bubble_short], [iname.disc_hop_hard]], loc_type=LocType.fruit),
            # if you have yoyo, you can swap the mouse direction and lock yourself out of the check without bubbles
        lname.fruit_107:
            AWData(AWType.location, [[iname.top]], loc_type=LocType.fruit),
        lname.egg_obsidian:  # bounce disc between the moving walls, or do some cursed bubble jumps
            AWData(AWType.location, [[iname.disc], [iname.bubble_short, iname.precise_tricks],
                                     [iname.water_bounce, iname.yoyo], [iname.water_bounce, iname.ball]]),
        # simultaneous buttons, need an item to hold it down
        # I don't think top is unintuitive enough to warrant obscure, but disc definitely is
        lname.fruit_110:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_112:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.egg_golden:
            AWData(AWType.location, [[iname.wheel, iname.slink], [iname.wheel, iname.top],
                                     [iname.wheel, iname.disc, iname.obscure_tricks]]),
        lname.fruit_114:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_113:
            AWData(AWType.location, [[iname.bubble, iname.slink], [iname.bubble_short, iname.obscure_tricks]], loc_type=LocType.fruit),
        lname.flame_green:
            AWData(AWType.location, [[iname.can_open_flame]], event=iname.green_flame),
        rname.bobcat_room:
            AWData(AWType.region, [[iname.top]]),
        # bird_area:  # pipe after flame, you need bubble to be here so no need to put the item requirement
        #     AWData(AWType.region),
    },
    rname.bobcat_room: {
        rname.fish_lower:
            AWData(AWType.region, [[iname.top]]),
        lname.wheel_chest:  # add bobcat song if we do song shuffle
            AWData(AWType.location, [[iname.flute]]),
        rname.chest_on_spikes_region:  # kinda unreasonable without the wheel imo
            AWData(AWType.region, [[iname.wheel]]),
    },

    rname.hippo_entry: {
        lname.fruit_89:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.fruit_88:
            AWData(AWType.location, [[iname.lantern]], loc_type=LocType.fruit),
        lname.activate_hippo_fast_travel:
            AWData(AWType.location, [[iname.flute]], event=iname.activated_hippo_fast_travel),
        lname.lantern_chest:
            AWData(AWType.location, [[iname.slink, iname.disc, iname.yoyo], [iname.lantern],
                                     [iname.slink, iname.ball_trick_hard],
                                     # something chillpenguin_ posted on discord on 1/6/2025
                                     [iname.ball_trick_hard, iname.obscure_tricks]]),
        rname.hippo_manticore_room:
            AWData(AWType.region, [[iname.lantern, iname.yoyo, iname.disc], 
                                   [iname.lantern, iname.yoyo, iname.wheel_hop, iname.tanking_damage],
                                   # running into the miasma with yoyo out can hit the rightmost button
                                   [iname.lantern, iname.yoyo, iname.bubble, iname.tanking_damage],
                                   [iname.lantern, iname.yoyo, iname.water_bounce, iname.tanking_damage],
                                   # all buttons can be hit with ball with enough patience
                                   [iname.lantern, iname.wheel_hop, iname.ball_trick_hard],
                                   [iname.lantern, iname.bubble, iname.ball_trick_hard],
                                   [iname.lantern, iname.disc, iname.ball_trick_hard],
                                   [iname.lantern, iname.water_bounce, iname.ball_trick_hard],
                                   # easy ball trick if you have yoyo to hit yoyo chute button, hard otherwise
                                   [iname.lantern, iname.wheel_hop, iname.yoyo, iname.ball_trick_easy],
                                   [iname.lantern, iname.water_bounce, iname.yoyo, iname.ball_trick_easy],
                                   [iname.lantern, iname.bubble, iname.yoyo, iname.ball_trick_easy]]),
    },
    rname.hippo_manticore_room: {
        lname.fruit_103:
            AWData(AWType.location, [[iname.bubble_short], [iname.disc], [iname.wheel_hop]], loc_type=LocType.fruit),
        lname.fruit_104:
            AWData(AWType.location, [[iname.disc]], loc_type=LocType.fruit),
        lname.fruit_105:
            AWData(AWType.location, [[iname.bubble, iname.top, iname.wheel], [iname.disc, iname.top, iname.wheel],
                                     [iname.wheel_hop, iname.top]], loc_type=LocType.fruit),
        rname.hippo_fireworks:  # todo: verify you need disc
            AWData(AWType.region, [[iname.slink, iname.yoyo, iname.disc]]),
        rname.hippo_skull_room:
            AWData(AWType.region, [[iname.slink, iname.yoyo, iname.disc]]),
    },
    rname.hippo_skull_room: {
        lname.bb_wand_chest:
            AWData(AWType.location),  # need to die a lot
    },
    rname.hippo_fireworks: {
        lname.victory_first:
            AWData(AWType.location, victory=Goal.option_fireworks), 
        lname.fruit_111:
            AWData(AWType.location, loc_type=LocType.fruit),
        lname.key_house:
            AWData(AWType.location),
        rname.home:
            AWData(AWType.region, [[iname.house_key]]),
        rname.hippo_skull_room:
            AWData(AWType.region, [[iname.bubble_short], [iname.disc_hop_hard]]),
    },
    rname.home: {
        rname.hippo_fireworks:
            AWData(AWType.region, [[iname.house_key]]),
        lname.bunny_tv:
            AWData(AWType.location, [[iname.flute]], loc_type=LocType.bunny),
        lname.fanny_pack_chest:
            AWData(AWType.location),
        rname.barcode_bunny:  # add song req if we do song shuffle
            AWData(AWType.region, [[iname.flute, iname.office_key]]),
        rname.top_of_the_well:
            AWData(AWType.region, [[iname.lantern]]),
    },
    rname.barcode_bunny: {
        lname.bunny_barcode:
            AWData(AWType.location, loc_type=LocType.bunny),
    },

    rname.top_of_the_well: {
        rname.home:
            AWData(AWType.region, [[iname.lantern]]),
        lname.egg_pickled:  # hold right while falling down the well
            AWData(AWType.location),
        rname.chocolate_egg_spot:
            # wall juts out, need bubble or mid-air jump
            AWData(AWType.region, [[iname.wheel_hard], [iname.bubble],
                                   [iname.flute_jump]]),
        rname.match_center_well_spot:
            AWData(AWType.region),  # wall is flush, just hold left
        rname.bear_match_chest_spot:
            AWData(AWType.region, [[iname.wheel_hard], [iname.bubble],
                                   [iname.flute_jump]]),
        rname.bear_truth_egg_spot:
            AWData(AWType.region, [[iname.wheel_hard], [iname.bubble, iname.precise_tricks]]),
    },
    rname.chocolate_egg_spot: {
        lname.egg_chocolate:  # across from center well match
            AWData(AWType.location),
        rname.match_center_well_spot:
            AWData(AWType.region, [[iname.disc, iname.remote], [iname.bubble_short, iname.remote]]),
        rname.bear_match_chest_spot:
            AWData(AWType.region, [[iname.bubble_long], [iname.wheel_hard]]),
        rname.top_of_the_well:
            AWData(AWType.region, [[iname.bubble_long], [iname.wheel_hard]]),
        rname.bear_truth_egg_spot:
            AWData(AWType.region, [[iname.wheel_hard], [iname.bubble, iname.precise_tricks],
                                   [iname.flute_jump]]),
    },
    rname.match_center_well_spot: {
        lname.match_center_well:  # across from the chocolate egg
            AWData(AWType.location),
        rname.chocolate_egg_spot:  
            AWData(AWType.region, [[iname.disc, iname.remote], [iname.bubble, iname.remote]]),
        rname.bear_match_chest_spot:
            AWData(AWType.region, [[iname.bubble_long], [iname.wheel_hard]]),
        rname.top_of_the_well:
            AWData(AWType.region, [[iname.bubble_long], [iname.wheel_hard]]),
        rname.bear_truth_egg_spot:
            AWData(AWType.region, [[iname.wheel_hard], [iname.bubble, iname.precise_tricks]]),
    },

    rname.fast_travel: {
        rname.starting_area:
            AWData(AWType.region, [[iname.flute]]),
        rname.bird_flute_chest:
            AWData(AWType.region, [[iname.activated_bird_fast_travel]]),
        rname.fish_west:
            AWData(AWType.region, [[iname.activated_fish_fast_travel]]),
        rname.frog_dark_room:
            AWData(AWType.region, [[iname.activated_frog_fast_travel]]),
        rname.bear_middle_phone_room:
            AWData(AWType.region, [[iname.activated_bear_fast_travel]]),
        rname.dog_fast_travel_room:
            AWData(AWType.region, [[iname.activated_dog_fast_travel]]),
        rname.hippo_entry:
            AWData(AWType.region, [[iname.activated_hippo_fast_travel]]),

    },
    rname.fast_travel_fish_teleport: {
        rname.uv_lantern_spot:
            AWData(AWType.region, [[iname.bubble], [iname.disc], [iname.wheel_hop]]),
        rname.fast_travel:
            AWData(AWType.region),
    },
    rname.uv_lantern_spot: {
        lname.uv_lantern_chest:
            AWData(AWType.location),
        rname.abyss_lower:
            AWData(AWType.region, [[iname.activated_bonefish_fast_travel]]),
    },

    rname.fast_travel_fake: {  # for direct teleport spells
        rname.fast_travel:
            AWData(AWType.region),  # probably never randomizing fast travel song, so no rule
        rname.top_of_the_well:  # add song req if we do song shuffle
            AWData(AWType.region),
        rname.fast_travel_fish_teleport:  # to the little enclosure on the right side of the fast travel room
            AWData(AWType.region),  # add song req if we do song shuffle
        rname.bear_chinchilla_song_room:
            AWData(AWType.region),  # add song req if we do song shuffle
        rname.bear_map_bunny_spot:
            AWData(AWType.region),
        rname.bulb_bunny_spot:
            AWData(AWType.region),
    },
}
