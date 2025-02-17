# Don't Starve Together Randomizer Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest)
- [Don't Starve Together](https://store.steampowered.com/app/322330/Dont_Starve_Together/)
- [Archipelago Randomizer Steam Workshop mod for Don't Starve Together](https://steamcommunity.com/sharedfiles/filedetails/?id=3218471273)

## Installation
- Install Archipelago.
- Follow Archipelago's basic tutorial on how to generate a game. [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)
    * Only a single YAML is needed for a Don't Starve Together server regardless of how many players will play on it.

## Setting up your world
- Open the Archipelago launcher and run the Don't Starve Together client. Connect to the Archipelago server.
    * Check the client for your world configuration if you cannot refer to your YAML (or if your settings are randomized).
    * It's also safe to launch the Don't Starve Together world before connecting the client if you don't need the info. You can do this
      to make sure your group is logged in and ready before connecting to Archipelago, for example.
- Start Don't Starve Together and choose Host Game.
- Click on "Create New World".
    * A new world is recommended, though using an existing world is also perfectly fine.
- You may be prompted to choose a server playstyle for your world. If you're not sure which to pick, Relaxed is recommended.
    * Endless, Survival, and Wilderness are also fine if you want more of a challenge.
    * World resets and character resets are fine, though will reset your progress for the Survival goal if that's your victory condition.
    * Lights Out is only appropriate if you have only night enabled in your YAML.
- On the Settings tab, make sure your Save Type is "Local Save".
    * If your world is already created, you can change this on the previous screen in the Manage World window.
- You may be prompted to choose whether or not to add Caves. Refer to the client if you don't remember.
    * It's also fine to always add Caves, even if your logic doesn't include it.
- Click on the Mods tab. Enable Archipelago Randomizer, from the Server Mods category.
    * If you don't see it, make sure you subscribe to it on the Steam Workshop. Don't worry, you don't have to restart Don't Starve Together.
    * You may also click on the Configure Mod icon to customize settings such as damage multipliers, and crafting mode and death link overrides.
    * You may also install other mods if you like.
- If you chose a starting season other than Autumn in your YAML, make sure to change it in your World Generation settings.
    * Click on the Forest tab.
    * Click on the World Generation sub-tab. Starting season should be the first option.
- If you toggled any of the seasons or day phases in your YAML, make sure to change it in your World Settings.
    * Click on the Forest tab and World Settings sub-tab.
    * Turn off any seasons or day phases that should be disabled.
    * If Season Flow in your YAML is "Unlockable", you may optionally choose the longest setting for your seasons.

## Playing the game
- If you enabled Warly's dishes in your YAML's cooking locations option, at least one player should choose Warly.
    * If you have a mod that allows other characters to use the Portable Crock Pot, this also works. Logic expects you to have the Portable
      Crock Pot right away.
- Once you load in and select your character, the client should automatically connect to DST and you can start playing!
- Depending on your YAML's settings, your checks can include interacting with or killing creatures, researching at a Science Machine, and
  cooking dishes with a Crock Pot.
- Most of your received items are recipe unlocks. Check your crafting menu for your items.
- Once you've connected your world to Archipelgo for the first time, it's possible to continue even if not connected. Progress syncs when
  you connect to Archipelago again. However, offline progress is lost if you regenerate your world!
- It is fine to play the same Archipelago slot on multiple worlds, even by multiple people at the same time.
    * You cannot play multiple slots on a single world. The DST's Archipelago client only connects to the DST server on the same machine.
- You cannot connect a different slot/multiworld to your existing Archipelago DST world. Your client will tell you if you have a mismatch.
