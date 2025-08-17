# Client integration

This document describes how you can integrate Universal Tracker into your own game's client and take advantage of its features.

## Adding a tracker tab to your CommonClient client

With the addition of ctx.make_gui() in 0.5.1 adding a UT tracker tab is very simplified,
When you import CommonContext, try and import the UT context instead
```py

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext
```

You'll also need to remove the "Tracker" tag from your context by resetting it back to {"AP"}
```py
class YourGameContext(SuperContext):
    tags = {"AP"}
```

if you edit your GameManager at all, just use super().make_gui() to inheret UT's ui if it got loaded
```py
def make_gui(self):
    ui = super().make_gui()
    ui.base_title = "Minit CLIENT"
    return ui
```

and when you start your client up add a call to ctx.run_generate() if the UT apworld was found
```py
if tracker_loaded:
    ctx.run_generator()
if gui_enabled:
    ctx.run_gui()
```

## Calling UT's tracker engine directly

This one is a bit stranger because UT is built off of client code that doesn't need a reason to run if there is no connection, but the functionality is fully there still. 
Here's an example that instantiates the ctx object without a connection, runs generation, and then picks the correct player id from UT's internal multiworld.
Then with the ctx created you can check which locations are in logic by:
1. Setting ctx.missing_locations to the location IDs to be checked
1. Filling ctx.items_received to be the NetworkItem representation of items received (Note: only the id will be checked by UT so that's why a single value tuple is valid in this example)
1. Running updateTracker() on the ctx
1. checking ctx.locations_available for the avaliable location IDs


```py
from worlds.tracker.TrackerClient import TrackerGameContext, updateTracker


def get_tracker_ctx(name):
    ctx = TrackerGameContext("", "", no_connection=True)
    ctx.run_generator()

    ctx.player_id = ctx.launch_multiworld.world_name_lookup[name]
    return ctx


def get_in_logic(ctx, items=[], locations=[]):
    ctx.items_received = [(item,) for item in items]  # to account for the list being ids and not Items
    ctx.missing_locations = locations
    updateTracker(ctx)
    return ctx.locations_available


name = "qwintBug"
ctx = get_tracker_ctx(name)
print(get_in_logic(ctx, items=[16777224, 16777227, 16777289], locations=[16777360, 16777370, 16777410]))

# [16777370, 16777410]
```

## World flags

UT supports a number of world flags that determine how UT will handle the world, the following is the current list

 * `disable_ut` : This causes UT to ignore the world, to be used only if the world is known to have issues when loaded in UT and fixing it would be more trouble then it's worth (Merged game/existing compatent poptracker etc)
 * `ut_can_gen_without_yaml` : Tells UT that the game will do a full regen

## Command Line Interface

UT provides two args that allow it to run as a "single shot" command line utility

  * `--list` which simply lists all currently in logic locations (as they would appear on the tab in the UI)
  * `--count` which provides an easier to parse overview of the current in logic state

To  use these commands, do the following

  1) Invoke the Launcher (if not on source, use the debug launcher to get a command line)
  2) Tell the launcher to open Universal Tracker
  3) Pass in the `--nogui` and whichever (or both) CLI args you want
  4) Input the URL

For example
```sh
python .\Launcher.py "Universal Tracker" -- --nogui --list Player1:None@localhost
```

## Adding In-Logic Callbacks

To be filled out later
