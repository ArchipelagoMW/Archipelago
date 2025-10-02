# Helping with SoH AP logic - A shitty contribution guide

## What is this?

We are looking for people to help us translate logic files from Ship of Harkinian over to our in-progress SoH apworld. This means taking a file from an area that exists in C++ in Ship’s repository, and turning it into a similar file in Python.


## What files?

The location_access files holding all the logic can be found in these 2 locations:
For Ship: https://github.com/HarbourMasters/Shipwright/tree/develop/soh/soh/Enhancements/randomizer/location_access

For the apworld:
https://github.com/aMannus/Archipelago/tree/soh/worlds/oot_soh/location_access


## I want to help!

Great! First things first, please claim an area in this document to prevent overlap from people working on the same area: https://docs.google.com/spreadsheets/d/1Or9bBvX7NJ7-uFOfDWMKSPNq4shwpw22IDStkHBOIZY/edit?usp=sharing

Don’t worry, you can always remove your claim if you end up not having time, especially when we’re still in the early stages and have lots of files to fill. 

Second, you want to fork the official Archipelago repository. Then, make a new branch and pull in our development branch: https://github.com/aMannus/Archipelago/tree/soh

Then, once you have your area finished, you want to make a pull request to that development branch.


## What should my pull requests contain?

Keep your PRs limited to one area file only. If your area is missing logic helpers (located in LogicHelpers.py), please make a pull request separately from the PR containing the area itself. This is to prevent as many merge conflicts as possible, and may help other people working on their regions that may also be missing the same helper.


## Great, how do I translate the files?

First off, we're ignoring Master Quest entirely for now, so feel free to skip over any regions related to that. 

We’re going to follow the code structure from Ship’s location_access files as much as we can. This means try to follow the order in which regions appear within an area as much as possible from the Ship file, copy the logic as 1 to 1 as possible, and keep every region in an order of: Events -> Locations -> Connections.

If you need examples to follow, take a look at other completed files like deku_tree.py. You can copy/paste a lot of the structure from those and adjust them to whatever regions with whatever logic you’re translating.

If you’re missing a helper, make sure it’s not there in LogicHelpers.py (maybe under a different name). If you’re unsure, please just ask in the discord thread and you’ll get an answer in no time. If it really doesn’t exist, like mentioned earlier, make a separate PR with just the helper, we’ll get it merged ASAP and you can start using it in your area file.

Once the area is fully translated to python (excluding MQ), create the PR!


## How the hell do these events work?

Events have a couple different parts. First, at the top of the file, you’ll declare any EventLocations your file is going to need. These are just places you’ll be placing your events in. If your event is something that’s only relevant to the local area (ex: Deku Tree Upper Basement Block Pushed), you also add it to the LocalEvents (also at the top of the file). If it’s an event that’s used across areas (ex: Can Farm Sticks), check the Events in Enums.py if it doesn’t exist yet, otherwise add it there. 

Again it’s probably best to look at existing files and see how they’re utilized there. Deku tree has quite a few events, some local, some used in other places, so it’s a good place to look.


## I made my PR, now what?

We’ll review it whenever we have time. Keep in mind we’re just doing this in our free time too, so it may take a couple days before we get to it. There may be changes that are requested, and once all questions/requested changes are made, it’ll get merged. Once we have all the areas mapped out, we’ll start a testing phase and start bug fixing. Let’s do this!
