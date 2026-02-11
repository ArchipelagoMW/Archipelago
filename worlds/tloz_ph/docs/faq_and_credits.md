# FAQ and Credits for The Legend of Zelda: Phantom Hourglass Archipelago

- [Latest Release](https://github.com/carrotinator/Archipelago/releases)
- [Setup Guide](https://github.com/carrotinator/Archipelago/blob/main/worlds/tloz_ph/docs/setup.md)
- [Tricks and Skips](https://github.com/carrotinator/Archipelago/blob/main/worlds/tloz_ph/docs/tricks_and_skips.md)
- [wiki](https://github.com/carrotinator/Archipelago/wiki), has detailed location info, item+location groups

# What is this?
This is an Archipelago Randomizer for Zelda: Phantom Hourglass that doesn't use modding or romhacking to function. All randomization 
is done by reading and writing active memory with a lua script connected to the client. This means that item models and 
text boxes in game will look vanilla, but they will still give the correct items. The main way to tell what you actually 
got is with the client.

If you want to help make a randomizer that's fully integrated into the game, visit [ph-randomizer](https://github.com/phst-randomizer/ph-randomizer). Unaffiliated with this project, but real cool.

This is a spiritual successor to my discontinued [Manual for Phantom Hourglass](https://github.com/carrotinator/manual_phantomhourglass_carrot). It covers the full game but you've got to do all the memory editing manually.

# Who made this?
This version of the randomizer was made by me, @Carrotinator. Some features were added by  @CelestialKitsune and @Tanker50207, and some stuff in the shared client with Spirit tracks was written by @DayKat and @1313e. The Universal Tracker Map Integration was worked on by @palex00 and @catzador. But it wouldn't have been possible without the work of many that came before. Here are some of them:
 * The Phantom Hourglass [Decomp Project](https://github.com/AetiasHax/ph), and especially: 
   * @Aetias for making an inventory editing script while playing the manual rando for PH I made previously. This spawned the idea for using the generic bizhawk connector to do everything, and look where that got us
   * Everyone who worked on the [PH dev spreadsheet](https://docs.google.com/spreadsheets/d/1_4Bo1IxLDtaytXj7SQFIAtt9QbPfYDTGZ-CDNf0DXJA/edit?gid=0#gid=0), but especially SammyGoodTunes, for updating the dev spreadsheets memory addresses live while I was working on this. I wouldn't have been able to do anything without the documentation in the spreadsheet.
 * The standalone [Phantom Hourglass Randomizer](https://github.com/phst-randomizer/ph-randomizer)
 * @Dinopony & @Ishigh1, whose [Archipelago implementation for Zelda: Oracle of Seasons](https://github.com/Dinopony/ArchipelagoOoS/releases) I used as a starting point and a reference for how to make an Archipelago client using the bizhawk tools. And for making their code easy to understand!
 * @alwaysintreble, whose entrance randomizer code from [The Messenger](https://github.com/alwaysintreble/TheMessengerRandomizerModAP) helped me figure that stuff out
 * Codegorilla/@Ars-Ignis, whose [crystalis implementation](https://github.com/Ars-Ignis/Archipelago) was extensively referenced for doing advanced universal tracker stuff.
 * The Manual for Archipelago discord, for lowering the entry threshold to Archipelago development.
 * Everyone who worked on Archipelago as a whole, for upholding high standards in code readability, and for creating such an amazing system.
 * Everyone who playtested the early versions of this, for giving enthusiasm and bug reports!
 * Everyone who playtested the later versions of this!

# FAQ

## What is currently implemented?

The whole game!
Things not implemented:
- Internal dungeon entrance shuffle
- Travelling Ship entrance shuffle
- Postman locations
- That one treasure map from the girl on Molida Island

It's still alpha, and there are still issues around! Report issues to the [phantom hourglass thread](https://discord.com/channels/731205301247803413/1256012365049233438) in the [Archipelago Discord](https://discord.gg/8Z65BR2)

## Is there a tracker?

[Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases) is fully supported, and includes a detailed map tracker by @palex00, @catzador and me. It has some [special setup instructions](https://github.com/carrotinator/Archipelago/wiki/UT-Map-Tracker).
There's an [item tracker](https://github.com/ZobeePlays/PH-AP-Item-Tracker/tree/main) for [poptracker](https://github.com/black-sliver/PopTracker) by @ZobeePlays.

## How do I warp to start?

Open the collection screen with select or from the menu tab, and press the button to switch the screens. Then enter any 
scene transition. There will be messages in the archipelago client to let you know it's working.
You can warp to start with a save and quit too. But not a save and reset.

## How does map warping work?

Map warping is my custom fast travel system. First it must be enabled in the yaml settings.
Map warping lets you warp to any ocean or island port you've previously visited. Open the sea chart map while on land, and click on an island to select it as a warp destination. Then enter any entrance to warp there! The client will let you know what goes wrong if it fails
There are some special conditions for warping:
- You cannot map warp from the ocean. You can from ships at sea, like beedle.
- You need to have visited an island or ocean to warp there, and have logical access to the port. 
- If overworld entrances are shuffled, it will specifically check for the port quadrant.
- If you enabled warp items in the yaml, you'll need those for warping to each island. Not having warp items will remove the islands from your map.
- You cannot map warp with a save and quit.

If using Universal Tracker and `/get_logical_path`, map warps will be accounted for when warping after selecting a valid warp destination once. You can disable this feature in your `host.yaml`.

## Where do I find more ammo?

Warp to start now refills health and ammo!
The Milk Bar on Mercay Island will also give free refills. How nice

## My ship is slow. How do i go faster?
There are multiple ways of doing this, but my favorite is to create a cheat in bizhawk for address `021FA0A4` in 
`ARM7 system bus`, and set to any speed value. Default max speed is ``0x0080``.  My favorite is `0x0200`, or 4x speed.
Note that this forces a max speed, and makes turning weird- you'll need to toggle it on and off to do things precisely. 
Highly recommend setting a hotkey for toggling all cheats!

## My game crashed/I quit without saving

The client should give you back your missing items when you reenter the game. It can take a while if you're missing a 
lot of items, but it will tell you what it's doing in the client.

## Where is `Location`?
There's a location guide being worked on at the [wiki](https://github.com/carrotinator/Archipelago/wiki). If the location you're looking for isn't there, and the map tracker isn't helping, ask about it in the discord.

## I collected some locations while the client wasn't connected

There is a backup system that reads savedata for missing checks when you enter a room. To trigger this, save and 
reenter the room with the locations in question. So far this is only implemented for save slot 1 and the overworld 
checks on Mercay Island, and some problematic checks like big rupees that can despawn or fall in the sea. I'm planning 
to add all locations in bulk soon.

This is also implemented for some problematic locations that are close together. Most of which have been fixed.

## How do small keys work in Temple of the Ocean King?

Since most locked doors in TotOK re-lock themselves each time you enter, TotOK has some special key rules:
* When you enter the dungeon, you start with as many TotOK small keys as you've found so far
* If you've opened the locked door on 1F that stays *permanently* unlocked, you don't get that key back. Logic assumes you can permanently lose that key, so you can safely open the 1F door unless you wanna go out of logic.
* When you reach the midway room with the yellow warp, it saves the number of keys you still have. When you take the yellow warp you should start with however many keys you saved.
* Finding more TotOK small keys after reaching the yellow midway will add them to the number of keys you get both at the start of the dungeon and from the midway.
* Logic can expect you to restart from the beginning to use your keys differently.
* The grappling hook can be used to skip a key on B3. This is in logic.
