from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

from .songinfo import Songs

from .yarghelpers import itemnamefromindex

if TYPE_CHECKING:
    from .world import YARGWorld


def set_all_rules(world: YARGWorld) -> None:
    set_all_location_rules(world)

def set_all_location_rules(world: YARGWorld) -> None:
    #Loop the songs dictionary and add location rules for both song locations
    #on every song to the relative song unlock item
    for index in world.selectedsonglist:
        if index != world.goal_song:
            location1 = world.get_location("\"" + itemnamefromindex(index) + "\" Item 1")
            location2 = world.get_location("\"" + itemnamefromindex(index) + "\" Item 2")
            location3 = world.get_location("\"" + itemnamefromindex(index) + "\" Item 3")
            item = itemnamefromindex(index)
            if world.shuffletoggle:
                inst = world.songinstruments[index]
                if inst == "guitar5F":
                    instname = "Guitar"
                if inst == "bass5F":
                    instname = "Bass"
                if inst == "rhythm5F":
                    instname = "Rhythm"
                if inst == "drums":
                    instname = "Drums"
                if inst == "keys5F":
                    instname = "Keys"
                if inst == "keysPro":
                    instname = "Pro Keys"
                if inst == "vocals":
                    instname = "Vocals"
                if inst == "harmony2":
                    instname = "2 Part Harmony"
                if inst == "harmony3":
                    instname = "3 Part Harmony"

                set_rule(location1, lambda state, i=instname, x=item: state.has_all((i, x), world.player))
                
                set_rule(location2, lambda state, i=instname, x=item: state.has_all((i, x), world.player))

                set_rule(location3, lambda state, i=instname, x=item: state.has_all((i, x), world.player))
            
            else:
                set_rule(location1, lambda state, x=item: state.has(x, world.player))
        
                set_rule(location2, lambda state, x=item: state.has(x, world.player))

                set_rule(location3, lambda state, x=item: state.has(x, world.player))