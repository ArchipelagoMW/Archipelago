# Kingdom Hearts 2 Archipelago Setup Guide

<h2 style="text-transform:none";>Quick Links</h2>

- [Game Info Page](../../../../games/Kingdom%20Hearts%202/info/en)
- [Player Options Page](../../../../games/Kingdom%20Hearts%202/player-options)

<h2 style="text-transform:none";>Required Software:</h2>

Kingdom Hearts II Final Mix from the [Epic Games Store](https://store.epicgames.com/en-US/discover/kingdom-hearts) or [Steam](https://store.steampowered.com/app/2552430/KINGDOM_HEARTS_HD_1525_ReMIX/)

- Follow this Guide to set up these requirements [KH2Rando.com](https://tommadness.github.io/KH2Randomizer/setup/Panacea-ModLoader/)
    1. Version 3.4.0 or greater OpenKH Mod Manager with Panacea
    2. Lua Backend from the OpenKH Mod Manager
    3. Install the mod `KH2FM-Mods-Num/GoA-ROM-Edition` using OpenKH Mod Manager
- Needed for Archipelago 
    1. [ArchipelagoKH2Client.exe](https://github.com/ArchipelagoMW/Archipelago/releases)
    2. Install the Archipelago Companion mod from `JaredWeakStrike/APCompanion` using OpenKH Mod Manager
    3. Install the mod from `KH2FM-Mods-equations19/auto-save` using OpenKH Mod Manager
    4. Install the mod from `KH2FM-Mods-equations19/KH2-Lua-Library` using OpenKH Mod Manager
    5. AP Randomizer Seed
- Optional Quality of Life Mods for Archipelago
    1. Optionally Install the Archipelago Quality Of Life mod from `JaredWeakStrike/AP_QOL` using OpenKH Mod Manager
    2. Optionally Install the Quality Of Life mod from `shananas/BearSkip` using OpenKH Mod Manager

<h3 style="text-transform:none";>Required: Archipelago Companion Mod</h3>

Load this mod just like the <b>GoA ROM</b> you did during the KH2 Rando setup. `JaredWeakStrike/APCompanion`<br> 
Have this mod second-highest priority below the .zip seed.<br>
This mod is based upon Num's Garden of Assemblege Mod and requires it to work. Without Num this could not be possible. 

<h3 style="text-transform:none";>Required: Auto Save Mod and KH2 Lua Library</h3>

Load these mods just like you loaded the GoA ROM mod during the KH2 Rando setup. `KH2FM-Mods-equations19/auto-save` and `KH2FM-Mods-equations19/KH2-Lua-Library` Location doesn't matter, required in case of crashes. See [Best Practices](en#best-practices) on how to load the auto save

<h3 style="text-transform:none";>Optional QoL Mods: AP QoL and Bear Skip</h3>

`JaredWeakStrike/AP_QOL` Makes the urns minigames much faster, makes Cavern of Remembrance orbs drop significantly more drive orbs for refilling drive/leveling master form, skips the animation when using the bulky vendor RC, skips carpet escape auto scroller in Agrabah 2, and prevents the wardrobe in the Beasts Castle wardrobe push minigame from waking up while being pushed.

`shananas/BearSkip` Skips all minigames in 100 Acre Woods except the Spooky Cave minigame since there are chests in Spooky Cave you can only get during the minigame. For Spooky Cave, Pooh is moved to the other side of the invisible wall that prevents you from using his RC to finish the minigame.

<h3 style="text-transform:none";>Installing A Seed</h3>

When you generate a game you will see a download link for a KH2 .zip seed on the room page. Download the seed then open OpenKH Mod Manager and click the green plus and "Select and install Mod Archive".<br>
Make sure the seed is on the top of the list (Highest Priority)<br>
After Installing the seed click "Mod Loader -> Build/Build and Run". Every slot is a unique mod to install and will be needed be repatched for different slots/rooms.

<h2 style="text-transform:none";>Optional Software:</h2>

- [Kingdom Hearts 2 AP Tracker](https://github.com/palex00/kh2-ap-tracker/releases/latest/), for use with
[PopTracker](https://github.com/black-sliver/PopTracker/releases)

<h2 style="text-transform:none";>What the Mod Manager Should Look Like.</h2>

![image](https://i.imgur.com/N0WJ8Qn.png)


<h2 style="text-transform:none";>Using the KH2 Client</h2>

Start the game through OpenKH Mod Manager. If starting a new run, enter the Garden of Assemblage from a new save. If returning to a run, load the save and enter the Garden of Assemblage. Then run the [ArchipelagoKH2Client.exe](https://github.com/ArchipelagoMW/Archipelago/releases).<br>
When you successfully connect to the server the client will automatically hook into the game to send/receive checks. <br>
If the client ever loses connection to the game, it will also disconnect from the server and you will need to reconnect.<br> 

Make sure the game is open whenever you try to connect the client to the server otherwise it will immediately disconnect you.<br>

Most checks will be sent to you anywhere outside a load or cutscene.<br>

If you obtain magic, you will need to pause your game to have it show up in your inventory, then enter a new room for it to become properly usable.

<h2 style="text-transform:none";>KH2 Client should look like this: </h2>

![image](https://i.imgur.com/qP6CmV8.png)

Enter The room's port number into the top box <b> where the x's are</b> and press "Connect". Follow the prompts there and you should be connected

<h2 style="text-transform:none";>Common Pitfalls</h2>

- Having an old GOA Lua Script in your `C:\Users\*YourName*\Documents\KINGDOM HEARTS HD 1.5+2.5 ReMIX\scripts\kh2` folder.
    - Pressing F2 while in game should look like this. ![image](https://i.imgur.com/ABSdtPC.png)
- Not having Lua Backend Configured Correctly.
    - To fix this look over the guide at [KH2Rando.com](https://tommadness.github.io/KH2Randomizer/setup/Panacea-ModLoader/). Specifically the Lua Backend Configuration Step.

- Loading into Simulated Twilight Town Instead of the GOA.
    - To fix this look over the guide at [KH2Rando.com](https://tommadness.github.io/KH2Randomizer/setup/Panacea-ModLoader/). Specifically the Panacea and Lua Backend Steps.

<h2 style="text-transform:none"; >Best Practices</h2>

- Make a save at the start of the GoA before opening anything. This will be the file to select when loading an autosave if/when your game crashes.
    - If you don't want to have a save in the GoA. Disconnect the client, load the auto save, and then reconnect the client after it loads the auto save.
- Set fps limit to 60fps.
- Run the game in windows/borderless windowed mode. Fullscreen is stable but the game can crash if you alt-tab out.
- Make sure to save in a different save slot when playing in an async or disconnecting from the server to play a different seed

<h2 style="text-transform:none";>Logic Sheet & PopTracker Autotracking</h2>

Have any questions on what's in logic? This spreadsheet made by Bulcon has the answer [Requirements/logic sheet](https://docs.google.com/spreadsheets/d/1nNi8ohEs1fv-sDQQRaP45o6NoRcMlLJsGckBonweDMY/edit?usp=sharing)

Alternatively you can use the Kingdom Hearts 2 PopTracker Pack that is based off of the logic sheet above and does all the work for you.

<h3 style="text-transform:none";>PopTracker Pack</h3>

1. Download [Kingdom Hearts 2 AP Tracker](https://github.com/palex00/kh2-ap-tracker/releases/latest/) and
[PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Put the tracker pack into packs/ in your PopTracker install.
3. Open PopTracker, and load the Kingdom Hearts 2 pack.
4. For autotracking, click on the "AP" symbol at the top.
5. Enter the Archipelago server address (the one you connected your client to), slot name, and password.

This pack will handle logic, received items, checked locations and autotabbing for you!


<h2 style="text-transform:none";>F.A.Q.</h2>

- Why is my Client giving me a "Cannot Open Process: " error?
    - Due to how the client reads kingdom hearts 2 memory some people's computer flags it as a virus. Run the client as admin.
- Why is my HP/MP continuously increasing without stopping?
    - You do not have `JaredWeakStrike/APCompanion` set up correctly. Make sure it is above the GoA ROM Edition Mod in the mod manager.
- Why is my HP/MP continuously increasing without stopping when I have the APCompanion Mod?
    - You have a leftover GOA lua script in your `Documents\KINGDOM HEARTS HD 1.5+2.5 ReMIX\scripts\KH2`.
- Why am I missing worlds/portals in the GoA?
    - You are missing the required visit-locking item to access the world/portal.
- Why did I not load into the correct visit?
    - You need to trigger a cutscene or visit The World That Never Was for it to register that you have received the item.
- What versions of Kingdom Hearts 2 are supported?
    - Currently the only supported versions are Epic Games Version 1.0.0.10_WW and Steam Build Version 15194255.
- Why am I getting wallpapered while going into a world for the first time?
    - Your Lua Backend was not configured correctly. Look over the step in the [KH2Rando.com](https://tommadness.github.io/KH2Randomizer/setup/Panacea-ModLoader/) guide.
- Why am I not getting magic?
    - If you obtain magic, you will need to pause your game to have it show up in your inventory, then enter a new room for it to become properly usable.
- Why did I crash after picking my dream weapon?
    - This is normally caused by having an outdated GOA mod or having an outdated panacea and/or luabackend. To fix this rerun the setup wizard and reinstall luabackend and panacea. Also make sure all your mods are up-to-date.
- Why did I crash?
    - The port of Kingdom Hearts 2 can and will randomly crash, this is the fault of the game not the randomizer or the archipelago client.
      - If you have a continuous/constant crash (in the same area/event every time) you will want to reverify your installed files. This can be done by doing the following: Open Epic Game Store --> Library --> Click Triple Dots --> Manage --> Verify
- Why am I getting dummy items or letters?
    - You will need to get the `JaredWeakStrike/APCompanion` (you can find how to get this if you scroll up)
- Why am I not sending or receiving items?
    - Make sure you are connected to the KH2 client and the correct room (for more information scroll up)
- Why should I install the auto save mod at `KH2FM-Mods-equations19/auto-save` and `KH2FM-Mods-equations19/KH2-Lua-Library`?
    - Because Kingdom Hearts 2 is prone to crashes and will keep you from losing your progress. Both mods are needed for auto save to work.
- How do I load an auto save?
    - To load an auto-save, hold down the Select or your equivalent on your prefered controller while choosing a file. Make sure to hold the button down the whole time.
