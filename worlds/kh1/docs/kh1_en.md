# Kingdom Hearts Archipelago Randomizer Setup Guide

<h2 style="text-transform:none";>Required software</h2>
- Kingdom Hearts Final Mix from the [Epic Games Store](https://store.epicgames.com/en-US/discover/kingdom-hearts) or [Steam](https://store.steampowered.com/app/2552430/KINGDOM_HEARTS_HD_1525_ReMIX/)
- The latest release of [OpenKH](https://github.com/OpenKH/OpenKh/releases)
- The latest release of the [Kingdom Hearts 1FM Randomizer Software](https://github.com/gaithern/KH1FM-RANDOMIZER/releases)
- The latest release of Archipelago for the [ArchipelagoKH1Client.exe](https://github.com/ArchipelagoMW/Archipelago/releases)

<h2 style="text-transform:none";>Setting up the required software</h2>

<h3 style="text-transform:none";>OpenKH</h3>

- Extract the OpenKH files to a directory of your choosing.
- When prompted for game edition, choose PC Release, select which platform you're using (EGS or Steam), navigate to your "Kingdom Hearts I.5 + II.5" installation folder in the path box and click "Next".
- When prompted, install Panacea, then click Next
- When prompted, check KH1 plus any other AP game you want to play, and click "Install and configure Lua backend", then click "Next"
- Extract the data for KH1.
- Click "Finish"

<h3 style="text-transform:none";>Kingdom Hearts 1FM Randomizer Software</h3>

- Extract the Kingdom Hearts 1FM Randomizer Software files in a directory of your choosing.

<h2 style="text-transform:none";>Obtaining and using the seed zip</h2>

- When you generate a game you will see a download link for a KH1 .zip seed on the room page.
- After downloading this zip, open "mod_generator.exe" in your Kingdom Hearts 1FM Randomizer Software folder.
- Direct "mod_generator.exe" to both your seed zip and your KH1 data folder extracted during your OpenKH set up.
- Click "start".
- After some time, you will find a file in your "Output" folder called mod_YYYYMMDDHHMMSS.zip
- Open "OpenKh.Tools.ModsManager.exe" and ensure that the dropdown in the top right is set to "Kingdom Hearts 1"
- Click the green plus, choose "Select and install Mod Archive or Lua Script", and direct the prompt to your new mod zip.
- You should now see a mod on your list called "KH1 Randomizer Seed XYZ" where XYZ is your seed hex value.
- Ensure this mod is checked, then, if you want to play right away, click "Mod Loader" at the top.
- Click "Build and Run".  Your modded game should now open.

<h2 style="text-transform:none";>Connecting to your multiworld via the KH1 Client</h2>

- Once your game is being hosted, open "ArchipelagoLauncher.exe".
- Find "KH1 Client" and open it.
- At the top, in the "Server:" bar, type in the host address and port.
- Click the "Connect" button in the top right.
- If connection to the server was successful, you'll be prompted to type in your slot named in the "Command:" bar at the bottom.
- After typing your slot name, press enter.
- If all is well, you are now connected.

<h2 style="text-transform:none";>FAQ</h2>
- The client did not confirm connection to the game, is that normal?
    - Yes, the game and client communicate via a game communication path set up in your in your "%AppData%" folder, and therefore don't need to establish a socket connection.
- I am not sending or receiving items.
    - Check out this [troubleshooting guide](https://docs.google.com/document/d/1oAXxJWrNeqSL-tkB_01bLR0eT0urxz2FBo4URpq3VbM/edit?usp=sharing)
- Why aren't the evidence boxes spawning in Wonderland?
    - You'll need to find "Footprints" in your multiworld.
- Why won't Phil let me start the Prelims?
    - You'll need to find "Entry Pass" in the multiworld.
- Why aren't the slides spawning in Deep Jungle?
    - You'll need to find "Slides" in the multiworld.
- Why can't I make progress in Atlantica?
    - You'll need to find "Crystal Trident" in the multiworld.
- Why won't the doctor let me progress in Halloween Town?
    - You'll need to find either "Forget-Me-Not" or "Jack-in-the-Box" in the multiworld.
- Why is there a book missing in the Hollow Bastion library?
    - You'll need to find "Theon Vol. 6" in the multiworld.
- How do I unlock End of the World?
    - Depending on your settings, your options are either finding a specified amount of "Lucky Emblems" or finding the item "End of the World".
- How do I enter Destiny Islands?
    - After obtaining the item "Destiny Islands", you can land there as an additional option in Traverse Town.
- Why can't I use the summon I obtained?
    - You need at least one magic spell before you can use summons.
