# Raft Randomizer Setup Guide

## Required Software

- [Raft](https://store.steampowered.com/app/648800/Raft/)
- [Raft Mod Loader](https://www.raftmodding.com/loader) ("*RML*")
- [Raftipelago mod](https://www.raftmodding.com/raftipelago)

## Installation Procedures

1. Install Raft. The currently-supported Raft version is Update 13: The Renovation Update. If you plan on playing Raft mainly with Archipelago, it's recommended to disable Raft auto-updating through Steam, as there is no beta channel to get old builds.

2. Install RML. If you've already installed it, the shortcut in the Start Menu is called "RMLLauncher.exe".

3. Install the Raftipelago mod from the Raft Modding website. This requires that you open the link on the webpage through RML. Alternatively, you can download the .rmod file and place it in the Mods folder manually.

4. Start Raft through Steam. Wait for it to load into the main menu.

5. Once the Raft main menu loads, open RML and click Play. Wait a few seconds after it says "Successfully injected" for RML to appear in Raft.

6. Open the RML menu. After RML injects, this should open automatically. If it does not, and you see RML information in the top center of the Raft main menu, press F9 to open it.

7. Navigate to the "Mod manager" tab in the left-hand menu.

8. Click on the plug icon for Raftipelago to load the mod.

## Installation Troubleshooting

You can press F10 to open the console to view any errors when loading the mod.

### DLL/Reflection/Image errors

Restart Raft and try again. Although RML may be able to start Raft instead of you starting it through Steam, try specifically opening Raft through Steam (not RML), then clicking Play in RML once you're on the Raft main menu.

### RML can't find Raft

Restart Raft and try again. Try running RML as administrator by right-clicking the shortcut and clicking "Run as administrator".
    
## Joining a MultiWorld Game

1. Ensure you're on the Main Menu with Raftipelago loaded.

2. Open the Debug Console by pressing F10.

3. Type */connect {serverAddress} {username} {password}* into the console and hit Enter.
   - Example: */connect archipelago.gg:12345 SunnyBat*
   - serverAddress must not contain spaces.
   - If your username or password contains spaces, surround that value with quotation marks ("). Adding quotation marks even when not necessary (eg "SunnyBat") is fine.
   - If your username or password starts with a quotation mark, surround the value with an additional set of quotation marks (eg the value *"myP@s$w0rD* would be entered as *""myP@s$w0rD"*).

4. Start a new game or load an existing one.
   - Raftipelago save games are marked as *incompatible* with
   - Do not use an existing game that was not created with Raftipelago. It will work, but if anything is unlocked, it will be automatically registered with Archipelago once the world is loaded. This is irreversible.

5. You can disconnect by typing */disconnect confirmDisconnect* into the console and hitting Enter.

## Game Troubleshooting

### The "Load game" button is disabled for my world / my world is corrupt

Be sure that you click the "Load game" button **after** you load Raftipelago. You can click the Load Game button again to reload all of the saves in your folder (there is no need to restart Raft if the mod loaded successfully).

### I'm certain I'm doing things correctly, but the world is still not loadable

You can bypass Raftipelago world verification checks by loading a backup of the world. If the backup is not loadable, the world is corrupted.

In the future, be sure that when you save the game, the Raftipelago mod is loaded.

### I disconnected from the server! What do I do to reconnect?

Open the console with F10 and type the */connect* command with your server/username/password in again. You do not need to save+quit to the main menu beforehand.