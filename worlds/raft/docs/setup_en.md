# Raft Randomizer Setup Guide

## Required Software

- [Raft](https://store.steampowered.com/app/648800/Raft/)
- [Raft Mod Loader](https://www.raftmodding.com/loader) ("*RML*")
- [ModUtils mod](https://www.raftmodding.com/mods/modutils)
- [Raftipelago mod](https://www.raftmodding.com/mods/raftipelago)

## Installation Procedures

1. Install Raft. The currently-supported Raft version is Version 1.0: The Final Chapter. Any minor version (such as 1.09) should be compatible.

2. Install RML.

3. Install the Raftipelago and ModUtils mods from the Raft Modding website. You should open the auto-installation link on the webpage through RML. Alternatively, you can download the .rmod file and place it in the Mods folder manually.

4. Open RML and click Play. If you've already installed it, the executable that was used to install RML ("RMLLauncher.exe" unless renamed) should be used to run RML. Raft should start after clicking Play.

5. Open the RML menu. This should open automatically when Raft first loads. If it does not, and you see RML information in the top center of the Raft main menu, press F9 to open it. If you do not see RML information at the top, close Raft+RML, go back to Step 4 and run RML as administrator.

6. Navigate to the "Mod manager" tab in the left-hand menu.

7. Click on the plug icon for ModUtils to load the mod. You can also click on the (i) next to the plug icon, then check the "Load this mod at startup" button. This will make the mod always load at startup.

8. Click on the plug icon for Raftipelago to load the mod. While it's possible to also make this mod load at startup, it's recommended *not* to do so; if this mod loads before ModUtils, the mod will fail to load properly.

## Joining a MultiWorld Game

1. Ensure you're on the Main Menu with Raftipelago loaded.

2. Open the Debug Console by pressing F10.

3. Type */connect {serverAddress} {username} {password}* into the console and hit Enter.
    - Example: */connect archipelago.gg:12345 SunnyBat*
    - If there is no password, the password argument may be omitted (as is the case in the above example).
    - serverAddress must not contain spaces.
    - If your username or password contains spaces, surround that value with quotation marks ("). Adding quotation marks even when not necessary (eg "SunnyBat") is fine.
    - If your username or password starts with a quotation mark, surround the value with an additional set of quotation marks (eg the value *"myP@s$w0rD* would be entered as *""myP@s$w0rD"*).

4. Start a new game or load an existing one. It's recommended to avoid using an existing game that was not created with your current run of Raftipelago (either vanilla or a different Raftipelago run). It will work, but if anything is unlocked, it will be automatically registered with Archipelago once the world is loaded. This is irreversible.

5. You can disconnect from an Archipelago server by typing */disconnect confirmDisconnect* into the console and hitting Enter.

## Multiplayer Raft

You're able to have multiple Raft players on a single Raftipelago world. This will work, with a few notes:
- Every player that joins the Raft world must have the Raftipelago mod loaded.
- Only the player that creates/loads the world can connect to Archipelago (this is the "host" of the Raft world). Other players do not need to run */connect*; everything will be routed through the the host.
- Players other than the host will be labeled as a "Raft Player (Steam name)" when using ingame chat, which will be routed through Archipelago chat.
- Ingame chat will only work when the host is connected to the Archipelago server.

## Installation Troubleshooting

You can press F10 to open the console to view any errors when loading the mod.

### DLL/Reflection/Image errors

Restart Raft and try again. These should be ephemeral errors.

### RML says to start Raft through Steam

If this happens, then RML is configured to only inject into an existing instance of Raft, rather than try and start a new one.

You can either:
- Click "Play" after Raft has loaded into the main menu
- Uncheck the box next to the "Disable Automatic Game Start" setting in the Settings menu then click Play.

### RML doesn't do anything when I click Play

If this happens, then RML is configured to only start a new instance of Raft, then inject into that specific instance. This also means that RML has detected an instance of Raft is already running, and will not start a new one.

You can either:
- Close the existing instance of Raft then click Play
- Check the box next to the "Disable Automatic Game Start" setting in the Settings menu then click Play.

## Game Troubleshooting

### The "Load game" button is disabled for my world / my world is corrupt

Be sure that you click the "Load game" button **after** you load Raftipelago. You can click the Load Game button again to refresh all of the saves in your folder (there is no need to restart Raft if the mod loaded successfully).

### I'm certain I'm doing things correctly, but the world is still not loadable

You can bypass Raftipelago world verification checks by loading a backup of the world. If the backup is not loadable, the world is corrupted.

In the future, be sure that when you save the game, the Raftipelago mod is loaded.

### I disconnected from the server! What do I do to reconnect?

Open the console with F10 and type the */connect* command with your server/username/password in again. You do not need to save+quit to the main menu beforehand.