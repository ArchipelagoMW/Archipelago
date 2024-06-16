
##Setting up the required mods
1. Install Psychonauts for PC, Astralathe, and the Psychonauts Randomizer Mod from the AP Companion Branch.
    Full Psychonauts Randomizer and Astralathe setup guide here: https://docs.google.com/document/d/1cI3M07nWfDuBkv2M2c4NtCHPyq9koH4f2p53fgCQS4E/edit?usp=sharing
    **MAKE SURE TO USE THE AP COMPANION BRANCH**
    
2. Download the psychonauts.apworld and place inside your Archipelago/lib/worlds folder

3. Find the folder that contains your Psychonauts and Astralathe installation, and copy the folder directory. For example, the most common place for the Steam version is "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Psychonauts"  

4. Run ArchipelagoLauncher.exe and open host.yaml from the Archipelago Launcher, find the psychonauts_options and paste your psychonauts game directory into the root_directory setting between the quotes.

5. Click "Generate Template Settings". This will open file explorer.
Find "Psychonauts.yaml" and copy it to /Players/ (create this folder if it does not exist)

6. Open the YAML file and change the line that says "name: Player{number}" to your desired player name.
Adjust the settings in the YAML to your liking

7. Run ArchipelagoGenerate.exe

8. Take the newly created AP_XXX.zip file in /output/ and upload it here: https://archipelago.gg/uploads

9. Unzip the AP_XXX.zip file. Find the zipped file containing your player number and name, and unzip it. This contains a file called RandoSeed.lua 

10. Find your Psychonauts game directory and open /ModResource/PsychoRando/Scripts

11. Paste RandoSeed.lua from your generated Archipelago file into this folder. Replace the file in the destination if needed.

12. Run AstralatheLauncher.exe to open the game. You should see your player number and name on the menu screen, along with your current randomizer version.

13. From the menu, enter the yellow door to start a new game.

14. Using the Archipelago Launcher, open the Psychonauts Client and connect to your server hosted on archipelago.gg

15. Once you've started a new save file and connected to the server, you can start playing!

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.
