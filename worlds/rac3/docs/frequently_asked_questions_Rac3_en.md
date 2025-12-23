# Ratchet and Clank 3 AP Frequently Asked Questions

## I have my client connected, but I can't send out/receive checks, what can I do?

It is probably caused by one of these:

1. Make sure you have PINE enabled in the PCSX2 settings.
2. Make sure you have only **one instance** of PCSX2 open.
3. Try out these commands in the Rac3 client: `/force_update`, `/rac3_info`
4. Try closing and reopening the client.
5. You connected to AP without verifying that it the client successfully connected to the emulator. It will say
   "Connected to RaC3" if it sucessfully connected.

## My RaC3 client never loads! It is always a black window no matter how long I wait, what can I do?

Try updating [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases) and see if that helps.
Sometimes it just refuses to load the client if you have an outdated version installed.
Updating Universal Tracker appears to solve this problem for those reporting this issue.

## In the vendors I can purchase a weapon multiple times, but I get nothing, why?

Until you don't have a weapon it's vendor slot will be active, because the game tries to put it back to the shop because
you don't have it, don't purchase weapons or Armor in the current versions.

## When I receive a weapon/gadget it sends out multiple checks, why is it happening?

Currently, weapon vendors and some gadget checks are being sent out when you receive them as items. This is because we currently don't know how to properly distinguish between items received from Archipelago or obtained in the vanilla game. The best action to
take to mitigate the effect of this is to put **Gadgets** and **Weapons** into the exclusion list, this makes them always contain filler items (e.g.
jackpot mode, bolts).

## X check is in logic, but when I go there I don't receive it, why?

Currently, there are some checks that doesn't work with sequence breaking (Example Obani Gemini: Infobot: Blackwater
City) these are collected into a location group called  `Unstable`. If you generate the yaml for yourself make sure it
is in the **excluded locations** section (it should be there by default along with some ones).
Due to how problematic this has become, the locations in the `Unstable` group have straight up been skipped during generation to prevent issues until a solution has been found.

## Ok, but how do I know which locations are getting excluded with each option?

Go to the [Locations](https://github.com/Taoshix/Archipelago-RaC3/blob/staging/worlds/rac3/constants/data/location.py#L1254) file and search for the following tags with CTRL+F

- Unstable - RAC3TAG.UNSTABLE
- Weapons - RAC3TAG.WEAPONS
- Gadgets - RAC3TAG.GADGETS

Any location including one of those tags will be a part of the location group. 
A location can have multiple tags and be part of multiple groups at the same time.

## I'm missing Holostar Studios and/or Qwark's hideout in my ship, but I got their infobots, what should I do?

These 2 specific planets have softlock preventions in place. In order to visit Holostar you need to have the hypershot
and the hacker. For Hideout, you need to have the refractor to avoid being softlocked on Phoenix Rescue.

## My cosmetics are missing, what can I do?

The client tells you to reload the save file as soon you start the game on Veldin. To reapply cosmetics, restart the client and reconnect, then reload your save file without saving first.

## How do i toggle death link?

You can run the /death_link command in the Ratchet and Clank 3 client to toggle it.

## Sometimes the message popup does not show when I send/receive items

If the game is paused, you are in a menu, selecting a mission etc the game cannot display the message box we use to show these messages.




