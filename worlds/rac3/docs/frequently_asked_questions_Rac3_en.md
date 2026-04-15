# Ratchet and Clank 3 AP Frequently Asked Questions

## What are the changes from the vanilla game?

You can read about the changes [here](https://github.com/Taoshix/Archipelago-RaC3/blob/staging/worlds/rac3/docs/en_Ratchet_and_Clank_3.md)

## Which versions are supported?

All game region versions are able to be played at various levels of compatibility:
- **US (Black Label `SCUS-97353` + Greatest Hits `SCUS-97518`):** Fully Supported
- **PAL (EU/AUS `SCES-52456`):** Mostly Supported. One HP Challenge patches on Annihilation Nation wont work
- **Japanese (`SCPS-15084` + The Best release `SCPS-19309`):** No Information, Please provide feedback (previously 
supported but got removed)
- **Korean (`SCKA-20037`):** No Information, Please provide feedback
- **Chinese (`SCAJ-20109`):** No Information, Please provide feedback

## I have my client connected, but I can't send out/receive checks, what can I do?

It is probably caused by one of these:

1. Make sure you have PINE enabled in the PCSX2 settings.
2. Make sure you have only **one instance** of PCSX2 open.
3. Try out these commands in the Rac3 client: `/force_update`, `/rac3_info`
4. Try closing and reopening the client.
5. You connected to AP without verifying that it the client successfully connected to the emulator. It will say
   "Connected to RaC3" if it successfully connected.

## My RaC3 client never loads! It is always a black window no matter how long I wait, what can I do?

Try updating [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases) and see if that helps.
Sometimes it just refuses to load the client if you have an outdated version installed.
Updating Universal Tracker appears to solve this problem for those reporting this issue.

## X check is in logic, but when I go there I don't receive it, why?

Currently, there are some checks that doesn't work with sequence breaking (For example most of the Phoenix checks) 
these are collected into a location group called  `Unstable`. If you generate the .yaml for yourself make sure it
is in the **excluded locations** section (it should be there by default). This will make the unstable locations have
only filler/trap items.

## OK, but how do I know which locations are getting excluded with each option?

Go to the [Locations](https://github.com/Taoshix/Archipelago-RaC3/blob/staging/worlds/rac3/constants/data/location.py#L1254) file and search for the following tags with CTRL+F

- Unstable - RAC3TAG.UNSTABLE
- Weapons - RAC3TAG.WEAPONS
- Gadgets - RAC3TAG.GADGETS

Any location including one of those tags will be a part of the location group. 
A location can have multiple tags and be part of multiple groups at the same time.

## My cosmetics are missing, what can I do?

The client tells you to reload the save file as soon you start the game on Veldin or Phoenix if intro skip is enabled. To reapply cosmetics, restart the client and reconnect, then visit the armor vendor or reload your save file without saving first. If you accidentially overwrite your skin with the skin vendor, you can visit the ship vendor to have the randomizer apply your skin values and then visit the armor vendor to have the game reapply your player skin.

## How do I toggle death link?

You can run the /deathlink command in the Ratchet and Clank 3 client to toggle it.

## Sometimes the message popup does not show when I send/receive items

If the game is paused, you are in a menu, selecting a mission, and in other situations, the game cannot display the message box we use to show these messages. If messages cannot be displayed, they stay in the notification queue until they can be displayed.

## A Gadget didn't spawn in the world when I haven't checked the location yet

We remove your gadget to make the game think you haven't picked it up yet in order to make it respawn in the world. If it fails to respawn, teleport to the ship to force a reload of the planet and there is a good chance it should have spawned then. If not, repeat until it has appeared. Should not take more than 1-2 times at most.

## How can I contribute to the project?

- **As a player**: The best way to contribute to the project as a player is to report every issue you encounter with the most details possible.
These submissions should be sent to the `[PS2] Ratchet and Clank 3: Up Your Arsenal` channel on the Archipelago discord. When you encounter an issue, make sure to use the `/rac3_info` command in your Ratchet and Clank 3 client and send the result of that
command into the discord channel as well.
- **As a developer**: If you wish to contribute to the implementation
itself then fork this repository on GitHub, make a new branch based of the `staging` branch of the project and make your changes there. Then open a pull request targetting `staging` with a detailed description of your changes.
If the changes made in the pull request are acceptable, then they will be merged. **Make sure your pull request targets the repository's `staging` branch!**


