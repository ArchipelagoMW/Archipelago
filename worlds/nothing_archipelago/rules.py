from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule, add_rule
import math

if TYPE_CHECKING:
    from .world import NothingWorld

def set_all_rules(world: NothingWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_entrance_rules(world: NothingWorld) -> None:
    coinreq = 0
    timereq = 60/world.options.timecap_interval
    if world.options.shop_upgrades:
        coinreq += 6

    if world.options.goal > 1200 or world.options.gift_coins:
        if world.options.shop_upgrades:
            coinreq += 4
        if world.options.shop_colors:
            coinreq += 18
        if world.options.shop_music:
            coinreq += 20
        if world.options.shop_sounds:
            coinreq += 20
    
    if world.options.shop_upgrades:
        Start_to_shopdigits = world.get_entrance("Start to shopdigits")
        set_rule(Start_to_shopdigits, lambda state: (
                    (state.has("Nothing Item Progressive Time Cap", world.player,int(math.ceil(timereq*10)-1)) 
                    & state.has("Nothing Item Timer Digit", world.player,2)) | state.has("Nothing Item Gifted Coin", world.player, coinreq) | 
                    (state.has("Nothing Item Progressive Time Cap", world.player,int(math.ceil(timereq)-1)) 
                    & state.has("Nothing Item Timer Digit", world.player,1)) | (state.has("Nothing Item Progressive Time Cap", world.player,int(math.ceil(10/world.options.timecap_interval)-1)) 
                    & state.has("Nothing Item Timer Digit", world.player,0)) | world.options.gift_coins))

    if (world.options.goal > 1200): 
        if world.options.shop_upgrades:
            Start_to_shopupgrades = world.get_entrance("Start to shopupgrades")
            set_rule(Start_to_shopupgrades, lambda state: 
                    (state.has("Nothing Item Progressive Time Cap", world.player,int(math.ceil(timereq*20)-1)) 
                    & state.has("Nothing Item Timer Digit", world.player,3)) | state.has("Nothing Item Gifted Coin", world.player, coinreq))
        if world.options.shop_colors:
            Start_to_shopcolors = world.get_entrance("Start to shopcolors")
            set_rule(Start_to_shopcolors, lambda state: 
                    (state.has("Nothing Item Progressive Time Cap", world.player,int(math.ceil(timereq*20)-1)) 
                    & state.has("Nothing Item Timer Digit", world.player,3)) | state.has("Nothing Item Gifted Coin", world.player, coinreq))
        if world.options.shop_music:
            Start_to_shopmusic = world.get_entrance("Start to shopmusic")
            set_rule(Start_to_shopmusic, lambda state: 
                    (state.has("Nothing Item Progressive Time Cap", world.player,int(math.ceil(timereq*20)-1)) 
                    & state.has("Nothing Item Timer Digit", world.player,3)) | state.has("Nothing Item Gifted Coin", world.player, coinreq))
        if world.options.shop_sounds:
            Start_to_shopsounds = world.get_entrance("Start to shopsounds")
            set_rule(Start_to_shopsounds, lambda state: 
                    (state.has("Nothing Item Progressive Time Cap", world.player,int(math.ceil(timereq*20)-1)) 
                    & state.has("Nothing Item Timer Digit", world.player,3)) | state.has("Nothing Item Gifted Coin", world.player, coinreq))

def set_all_location_rules(world: NothingWorld) -> None:
    difference = world.options.milestone_interval/world.options.timecap_interval
    timereq = -1
    timerval = 0
    number = int(math.ceil(world.options.goal/world.options.milestone_interval))
    for i in range (0,number):
        location = world.get_location("Nothing Milestone "+str(i+1))
        timereq += difference
        timerval += world.options.milestone_interval
        if world.options.shop_upgrades:
            if timerval > 9:
                if timerval <= 59:
                     add_rule(location, lambda state: state.count("Nothing Item Timer Digit",world.player) > 0)
                elif timerval <= 599:
                     add_rule(location, lambda state: state.count("Nothing Item Timer Digit",world.player) > 1)
                elif timerval <= 3599:
                     add_rule(location, lambda state: state.count("Nothing Item Timer Digit",world.player) > 2)
                elif timerval <= 35999:
                     add_rule(location, lambda state: state.count("Nothing Item Timer Digit",world.player) > 3)
                elif timerval <= 86399:
                     add_rule(location, lambda state: state.count("Nothing Item Timer Digit",world.player) > 4)
                else:
                     add_rule(location, lambda state: state.count("Nothing Item Timer Digit",world.player) > 5)
        if timereq > 0:
            add_rule(location, lambda state: 
                     state.count("Nothing Item Progressive Time Cap",world.player) >= int(timereq))




def set_completion_condition(world: NothingWorld) -> None:
    if world.options.shop_upgrades and world.options.goal > 9:
        if world.options.goal < 60:
            world.multiworld.completion_condition[world.player] = lambda state: (
            state.has("Nothing Item Progressive Time Cap", world.player, int(math.ceil(world.options.goal/world.options.timecap_interval)-1)) and
            state.has("Nothing Item Timer Digit",world.player,1))
        if world.options.goal < 600:
            world.multiworld.completion_condition[world.player] = lambda state: (
            state.has("Nothing Item Progressive Time Cap", world.player, int(math.ceil(world.options.goal/world.options.timecap_interval)-1)) and
            state.has("Nothing Item Timer Digit",world.player,2))
        if world.options.goal < 3600:
            world.multiworld.completion_condition[world.player] = lambda state: (
            state.has("Nothing Item Progressive Time Cap", world.player, int(math.ceil(world.options.goal/world.options.timecap_interval)-1)) and
            state.has("Nothing Item Timer Digit",world.player,3))
        if world.options.goal < 36000:
            world.multiworld.completion_condition[world.player] = lambda state: (
            state.has("Nothing Item Progressive Time Cap", world.player, int(math.ceil(world.options.goal/world.options.timecap_interval)-1)) and
            state.has("Nothing vTimer Digit",world.player,4))
        if world.options.goal < 86400:
            world.multiworld.completion_condition[world.player] = lambda state: (
            state.has("Nothing Item Progressive Time Cap", world.player, int(math.ceil(world.options.goal/world.options.timecap_interval)-1)) and
            state.has("Nothing Item Timer Digit",world.player,5))
        else:
            world.multiworld.completion_condition[world.player] = lambda state: (
            state.has("Nothing Item Progressive Time Cap", world.player, int(math.ceil(world.options.goal/world.options.timecap_interval)-1)) and
            state.has("Nothing Item Timer Digit",world.player,6))
    else:
        world.multiworld.completion_condition[world.player] = lambda state: (
            state.has("Nothing Item Progressive Time Cap", world.player, int(math.ceil(world.options.goal/world.options.timecap_interval)-1)))
        