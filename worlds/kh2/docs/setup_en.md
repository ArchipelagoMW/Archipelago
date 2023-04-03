# Kingdom Hearts 2 Archipelago Setup Guide
<h2 style="text-transform:none";>Quick Links</h2>

- [Main Page](../../../../games/Kingdom%20Hearts%202/info/en)
- [Settings Page](../../../../games/Kingdom%20Hearts%202/player-settings)

<h2 style="text-transform:none";>What You Need to Start Playing:</h2>
 `Kingdom Hearts II Final Mix` from the [Epic Games Store](https://store.epicgames.com/en-US/discover/kingdom-hearts)
- Follow this Guide to set up these requirements [KH2Rando.com](https://tommadness.github.io/KH2Randomizer/setup/Panacea-ModLoader/)
    1. `3.0.0 OpenKH Mod Manager with Panacea`<br>
    2. `Lua Backend From the KH2Randomizer.exe`<br>
    3. `KH2FM-Mods-Num/GoA-ROM-Edition`<br>
- Archipelago Specific.
    1. `JaredWeakStrike/APCompanion`<br>
    2. `KH2FM-Mods-equations19/auto-save`<br>
    3. `ArchipelagoKH2Client.exe`<br>
    4. `AP Randomizer Seed`

<h3 style="text-transform:none";>Loading A Seed</h3>

When you generate a game you will see a download link for a KH2 .zip seed on the room page. Download the seed then open OpenKH Mod Manager and click the green plus and `Select and install Mod Archive`. Make sure the seed is on the top of the list (Highest Priority)

<h3 style="text-transform:none";>Required: Archipelago Companion Mod</h3>

Load this mod just like the <b>GoA ROM</b> you did during the KH2 Rando setup. `JaredWeakStrike/APCompanion`<br> 
Have this mod second-highest priority below the .zip seed.<br>
This mod is based upon Num's Garden of Assemblege Mod and requires it to work. Without Num this could not be possible. 


<h3 style="text-transform:none";>Required: Auto Save Mod</h3>
Load this mod just like the GoA ROM you did during the KH2 Rando setup. `KH2FM-Mods-equations19/auto-save` Location doesn't matter, recommended in case of crashes.

![Openkh mod manager setup](/static/generated/docs/kh2/openkhpicture.png)
<h2 style="text-transform:none";>Using the KH2 Client</h2>

Once you have started the game through OpenKH Mod Manager and are on the title screen run the ArchipelagoKH2Client.exe. <br>
When you successfully connect to the server the client will automatically hook into the game to send/receive checks. <br>
If the client ever loses connection to the game, it will also disconnect from the server and you will need to reconnect.<br> 
`Make sure the game is open whenever you try to connect the client to the server otherwise it will immediately disconnect you.`<br>
Most checks will be sent to you anywhere outside a load or cutscene.<br>
`but if you obtain magic, you will need to pause your game to have it show up in your inventory, then enter a new room for it to become properly usable.`

<h2 style="text-transform:none";>Common Pitfalls</h2>
- Having an old GOA Lua Script in your `C:\Users\*YourName*\Documents\KINGDOM HEARTS HD 1.5+2.5 ReMIX\scripts` folder.
  - It should look like this. ![Openkh mod manager setup](/static/generated/docs/kh2/luaconsole.png)
- Not having Lua Backend Configured Correctly.
  - To fix this look over the guide at [KH2Rando.com](https://tommadness.github.io/KH2Randomizer/setup/Panacea-ModLoader/). Specifically the Lua Backend Configuration Step.


<h2 style="text-transform:none";>Recommendation</h2>

- Recommended making a save at the start of the GoA before opening anything. This will be the recommended file to load if/when your game crashes.
    - If you don't want to have a save in the GoA. Disconnect the client, load the auto save, and then reconnect the client after it loads the auto save.
- Recommended to set fps limit to 60fps.
- Recommended to run the game in windows/borderless windowed mode. Fullscreen is stable but the game can crash if you alt-tab out.
- Recommend viewing [Requirements/logic sheet](https://docs.google.com/spreadsheets/d/1Embae0t7pIrbzvX-NRywk7bTHHEvuFzzQBUUpSUL7Ak/edit?usp=sharing)

<h2 style="text-transform:none";>F.A.Q.</h2>

- Why am I getting wallpapered while going into a world for the first time?
  - Your `Lua Backened` was not configured correctly. Look over the step in the [KH2Rando.com](https://tommadness.github.io/KH2Randomizer/setup/Panacea-ModLoader/) guide.
- Why am I not getting magic?
    - If you obtain magic, you will need to pause your game to have it show up in your inventory, then enter a new room for it to become properly usable.
- Why am I missing worlds/portals in the GoA?
    - You are missing the required visit locking item to access the world/portal.
- What versions of Kingdom Hearts 2 are supported?
    - Currently `only` the most up to date version on the Epic Game Store is supported `1.0.0.8_WW`. Emulator may be added in the future.
- Why did I crash?
    - The port of Kingdom Hearts 2 can and will randomly crash, this is the fault of the game not the randomizer or the archipelago client.
      - If you have a continuous/constant crash (in the same area/event every time) you will want to reverify your installed files. This can be done by doing the following: Open Epic Game Store --> Library --> Click Triple Dots --> Manage --> Verify
- Why am I getting dummy items or letters?
    - You will need to get the `JaredWeakStrike/APCompanion` (you can find how to get this if you scroll up)
- Why is my HP/MP continuously increasing without stopping?
    - You do not have `JaredWeakStrike/APCompanion` setup correctly. Make Sure it is above the GOA in the mod manager.
- Why am I not sending or receiving items?
    - Make sure you are connected to the KH2 client and the correct room (for more information scroll up)
- Why did I not load in to the correct visit
    - You need to trigger a cutscene or visit The World That Never Was for it to update you have recevied the item.
- Why should I install the auto save mod at `KH2FM-Mods-equations19/auto-save`?
    - Because Kingdom Hearts 2 is prone to crashes and will keep you from losing your progress.
- How do I load an auto save?
    - To load an auto-save, hold down the Select or your equivalent on your prefered controller while choosing a file. Make sure to hold the button down the whole time.


