# Gato Roboto B-Side Randomizer Setup Guide

## Required Software
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- The game (Gato Roboto)

## Installation
### Archipelago install
1. Download and install [Archipelago](<https://github.com/ArchipelagoMW/Archipelago/releases/latest>). **The installer file is located in the assets section at the bottom of the version information.**
2. Make sure it properly installs (due to emulator modding tools some anti-viruses try to prevent you from installing it)
3. Use the "Archipelago Launcher" whenever you are prompted to use a "Launcher" here!
### APWorld install
1. Get the apworld (.apworld file) in the [releases](https://github.com/Nitroxyz/Gato-Roboto-B-Side-Archipelago/releases/latest)  
2. Then install the apworld into the archipelago Launcher (you can double-click the .apworld anywhere on your pc it if you have the Launcher installed)  
3. If it prompts you with an "apworld installed" dialogue box, then you successfully installed it!
### Generate and host a game
*Only one person needs to do this process if you are playing together*  
1. Generate the default option template by opening up the Launcher, the selecting the box "Generate Template Options" 
2. A folder will open, which gives you the default template for each game installed. Find the one for "Gato Roboto B-Side"
3. Customize your options. Make sure to give yourself a unique for the slot name first! For any option you don't want, set them to 0 and set at least one to a value greater than 0. I recommend keeping (progression_balancing => 50:50) and (accessibility => full:50)
4. In the root of the folder, where you generate the templates (a folder called `Players`), put one yaml for each individual player who is playing a game (one for a solo game).
5. In the Launcher, select the box "Generate". If a command window opens and closes, then the generation was successful
6. You can find the generated multiworld inside of `output` folder (go one path down from `Players`), then you will find it
7. Go to the Archipelago website and go to the [host game](https://archipelago.gg/uploads) tab. Select the zip file inside of the output folder and pass it to the website
8. Select "Start a new room"
9. Success! You now hosted a new multiworld! Keep the link to the website you are on (which is your room) and whenever you have it open, your multiroom is active! 
10. Note the ``archipelago:XXXXX`` (with specific number)! You need this in the next step!
### Start the client and patch the game
1. If you have the apworld installed, you should be able to find a "Gato Roboto B-Side Client" box in the Launcher.
2. When you open it you get a Text client
3. At the top you need to input the ``archipelago:XXXXX`` thing from the multiworld and press the "connect" button
4. Inside the Text client, it now prompts you to input your slot name. This is the name you made inside the yaml for your game
5. Once you connected, it will return a "Client connected" prompt and you might see all the items being sent by other players already
6. You need to patch the game by typing ``/auto_patch`` into your Text client. If your game is in a different location than your steam directory, you will have to add the file path after the command.
7. Once you did that successfully, you can open up the game!
8. Keep in mind that you only need to patch once!
9. When you are inside of the game, you can confirm that you have correctly installed the mod by seeing only one savefile
10. Make sure to delete your current savefile if you played a different randomizer before!
11. If you manage to enter the game, you successfully connected the client!