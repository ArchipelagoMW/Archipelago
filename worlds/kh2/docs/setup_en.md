# Kingdom Hearts 2 Archipelago Setup Guide
<h2 style="text-transform:none";>Quick Links</h2>

- [Game Info Page](../../../../games/Kingdom%20Hearts%202/info/en)
- [Player Settings Page](../../../../games/Kingdom%20Hearts%202/player-settings)

<h2 style="text-transform:none";>Required Software:</h2>
 `Kingdom Hearts II Final Mix` from the [Epic Games Store](https://store.epicgames.com/en-US/discover/kingdom-hearts)
- Follow this Guide to set up these requirements [KH2Rando.com](https://tommadness.github.io/KH2Randomizer/setup/Panacea-ModLoader/)<br>
    1. `3.0.0 OpenKH Mod Manager with Panacea`<br>
    2. `Install mod from KH2FM-Mods-Num/GoA-ROM-Edition`<br>
    3. `Setup Lua Backend From the 3.0.0 KH2Randomizer.exe per the setup guide linked above`<br>

- Needed for Archipelago 
    1. [`ArchipelagoKH2Client.exe`](https://github.com/ArchipelagoMW/Archipelago/releases)<br>
    2. `Install mod from JaredWeakStrike/APCompanion`<br>
    3. `Install mod from KH2FM-Mods-equations19/auto-save`<br>
    4. `AP Randomizer Seed`
<h3 style="text-transform:none";>Required: Archipelago Companion Mod</h3>

Load this mod just like the <b>GoA ROM</b> you did during the KH2 Rando setup. `JaredWeakStrike/APCompanion`<br> 
Have this mod second-highest priority below the .zip seed.<br>
This mod is based upon Num's Garden of Assemblege Mod and requires it to work. Without Num this could not be possible. 

<h3 style="text-transform:none";>Required: Auto Save Mod</h3>
Load this mod just like the GoA ROM you did during the KH2 Rando setup. `KH2FM-Mods-equations19/auto-save` Location doesn't matter, required in case of crashes.

<h3 style="text-transform:none";>Installing A Seed</h3>

When you generate a game you will see a download link for a KH2 .zip seed on the room page. Download the seed then open OpenKH Mod Manager and click the green plus and `Select and install Mod Archive`.<br>
Make sure the seed is on the top of the list (Highest Priority)<br>
After Installing the seed click `Mod Loader -> Build/Build and Run`. Every slot is a unique mod to install and will be needed be repatched for different slots/rooms.

<h2 style="text-transform:none";>What the Mod Manager Should Look Like.</h2>
![image](https://i.imgur.com/QgRfjP1.png)

<h2 style="text-transform:none";>Using the KH2 Client</h2>

Once you have started the game through OpenKH Mod Manager and are on the title screen run the [ArchipelagoKH2Client.exe](https://github.com/ArchipelagoMW/Archipelago/releases). <br>
When you successfully connect to the server the client will automatically hook into the game to send/receive checks. <br>
If the client ever loses connection to the game, it will also disconnect from the server and you will need to reconnect.<br> 
`Make sure the game is open whenever you try to connect the client to the server otherwise it will immediately disconnect you.`<br>
Most checks will be sent to you anywhere outside a load or cutscene.<br>
`If you obtain magic, you will need to pause your game to have it show up in your inventory, then enter a new room for it to become properly usable.`
<br>
<h2 style="text-transform:none";>KH2 Client should look like this: </h2>
![image](https://i.imgur.com/qP6CmV8.png)
<br>
Enter `The room's port number` into the top box <b> where the x's are</b> and press "Connect". Follow the prompts there and you should be connected


<h2 style="text-transform:none";>Common Pitfalls</h2>
- Having an old GOA Lua Script in your `C:\Users\*YourName*\Documents\KINGDOM HEARTS HD 1.5+2.5 ReMIX\scripts\kh2` folder.
  - Pressing F2 while in game should look like this. ![image](https://i.imgur.com/ABSdtPC.png)
<br>
- Not having Lua Backend Configured Correctly.
  - To fix this look over the guide at [KH2Rando.com](https://tommadness.github.io/KH2Randomizer/setup/Panacea-ModLoader/). Specifically the Lua Backend Configuration Step.
<br>
- Loading into Simulated Twilight Town Instead of the GOA.
  - To fix this look over the guide at [KH2Rando.com](https://tommadness.github.io/KH2Randomizer/setup/Panacea-ModLoader/). Specifically the Panacea and Lua Backend Steps.


<h2 style="text-transform:none";>Best Practices</h2>

- Make a save at the start of the GoA before opening anything. This will be the file to select when loading an autosave if/when your game crashes.
    - If you don't want to have a save in the GoA. Disconnect the client, load the auto save, and then reconnect the client after it loads the auto save.
- Set fps limit to 60fps.
- Run the game in windows/borderless windowed mode. Fullscreen is stable but the game can crash if you alt-tab out.
- Make sure to save in a different save slot when playing in an async or disconnecting from the server to play a different seed

<h2 style="text-transform:none";>Requirement/logic sheet</h2>
Have any questions on what's in logic? This spreadsheet has the answer [Requirements/logic sheet](https://docs.google.com/spreadsheets/d/1Embae0t7pIrbzvX-NRywk7bTHHEvuFzzQBUUpSUL7Ak/edit?usp=sharing)
<h2 style="text-transform:none";>F.A.Q.</h2>

- Why is my HP/MP continuously increasing without stopping?
    - You do not have `JaredWeakStrike/APCompanion` set up correctly. Make sure it is above the `GoA ROM Mod` in the mod manager.
- Why is my HP/MP continuously increasing without stopping when I have the APCompanion Mod?
    - You have a leftover GOA lua script in your `Documents\KINGDOM HEARTS HD 1.5+2.5 ReMIX\scripts\KH2`.
- Why am I missing worlds/portals in the GoA?
    - You are missing the required visit-locking item to access the world/portal.
- Why did I not load into the correct visit?
    - You need to trigger a cutscene or visit The World That Never Was for it to register that you have received the item.
- What versions of Kingdom Hearts 2 are supported?
    - Currently `only` the most up to date version on the Epic Game Store is supported: version `1.0.0.8_WW`.
- Why am I getting wallpapered while going into a world for the first time?
  - Your `Lua Backend` was not configured correctly. Look over the step in the [KH2Rando.com](https://tommadness.github.io/KH2Randomizer/setup/Panacea-ModLoader/) guide.
- Why am I not getting magic?
    - If you obtain magic, you will need to pause your game to have it show up in your inventory, then enter a new room for it to become properly usable.
- Why did I crash?
    - The port of Kingdom Hearts 2 can and will randomly crash, this is the fault of the game not the randomizer or the archipelago client.
      - If you have a continuous/constant crash (in the same area/event every time) you will want to reverify your installed files. This can be done by doing the following: Open Epic Game Store --> Library --> Click Triple Dots --> Manage --> Verify
- Why am I getting dummy items or letters?
    - You will need to get the `JaredWeakStrike/APCompanion` (you can find how to get this if you scroll up)
- Why am I not sending or receiving items?
    - Make sure you are connected to the KH2 client and the correct room (for more information scroll up)
- Why should I install the auto save mod at `KH2FM-Mods-equations19/auto-save`?
    - Because Kingdom Hearts 2 is prone to crashes and will keep you from losing your progress.
- How do I load an auto save?
    - To load an auto-save, hold down the Select or your equivalent on your prefered controller while choosing a file. Make sure to hold the button down the whole time.


