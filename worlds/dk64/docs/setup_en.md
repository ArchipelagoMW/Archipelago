Archipelago is a way to randomize several games together into one cohesive experience. The items from all games are placed into a pool and distributed out to all games in that session. This means you might find someone else's grenade eggs in a cage in DK64, and someone else might find the bean in Water Temple for your seed.
# Requirements list
- [Project64 4.0](./Consoles-and-Emulators:-Project-64-4.0)
- [Archipelago 0.6+](https://github.com/ArchipelagoMW/Archipelago/releases)
- [APWorld](https://dev.dk64randomizer.com/dk64.apworld)

# Resources

## Poptracker
<flex><fa-icon class="fa-solid fa-code fa-lg">Developers:</fa-icon>&nbsp;&nbsp;UmedMuzl
<fa-icon class="fa-solid fa-download fa-lg">| Download:</fa-icon>&nbsp;&nbsp;[Link](https://github.com/AmedMusl/dk64pt)
</flex>
# Tutorials
**Settings Tutorial by Keiper**
<ytvideo yt-id="xb8QsapzdWg">[![Video Tutorial - AP Settings](https://img.youtube.com/vi/xb8QsapzdWg/0.jpg)](https://www.youtube.com/watch?v=xb8QsapzdWg)</ytvideo>
# Setup Guide
## Installation Procedures
1. Download and install the Archipelago Multiworld Suite from the link above, making sure to install the most recent version.
2. Download and install the Project 64 4.0 Emulator from the link above, making sure to install the most recent version. Run the emulator at least once to make sure it is working.
3. Download the [APworld file](https://dev.dk64randomizer.com/dk64.apworld).
4. Using the AP launcher, hit "Install AP World" and point it to the dk64.apworld file you downloaded.
   **NOTE: We HIGHLY suggest you run Archipelago as Administrator for the first time run of it, it helps automatically set up your Project 64 Installation.**
## Create a Config (.yaml) File
### What is a config file and why do I need one?
Your config file contains a set of configuration options which provide the generator with information about how it should generate your game. Each player of a multiworld will provide their own config file. This setup allows each player to enjoy an experience customized for their taste, and different players in the same multiworld can all have different options.
### Where do I get a config file?
Run the ArchipelagoLauncher.exe from your Archipelago install and click `Generate Template Options` This will produce a `/Players/Templates` folder in your Archipelago install, which contains default config files for every game in your `custom_worlds` folder. You can manually edit the config file using a text editor of your choice.
## Generating a Seed and Setting up the Client
1. After modifying your yaml, place it into your Archipelago/player folder
2. Open the Archipelago Launcher and click "Generate". This will create a zip file in Archipelago output
    - You will need to open this .zip to get your `.lanky` patch file
3. Navigate to the Archipelago website and go to the Host Game page
4. Click upload file and pass it the .zip created in your output folder
5. Click the "Create New Room" link.
6. Go to the [DK64 Randomizer](https://dev.dk64randomizer.com) site and click on 'Generate from Patch File'. Load in your DK64 ROM and select your '.lanky' file. You can also select your cosmetics before clicking `Generate Seed`. Once you are ready, click on `Generate Seed`
    - The patch will be placed in the same folder as your patch file by default.
7. Open the `DK64 Randomizer` client in the AP window
    - This will load `adapter.js` into your emulator folder on first time launch for ease of use
8. Once you have loaded into the game, click the `Connect` button at the top of the DK64 Client. You are now connected and ready to play!
## Joining a MultiWorld Game
### Obtain your patch file and create your ROM
When you join a multiworld game, you will be asked to provide your config file to whoever is hosting Once that is done, the host will provide you with either a link to download your patch file, or with a zip file containing everyone's patch files. Your patch file should have a `.lanky` extension.
Put your patch file on your desktop or somewhere convenient. Open the DK64 Randomizer site as mentioned above, and Generate your seed.
### Connect to the client
1. When you launch the client, go to Project64 and run the `adapter.js` script in the emulator.
2. In the server page, there will be a port number. Copy this port number into the top of your DK64 Client.
    - The field should read `archipelago.gg:<port number>`
3. Click the `Connect` button at the top of the LMClient. Once you have loaded into the game, the client should log that Project64 has been connected. you are now connected and ready to play!
   You will know everything is working when you see `Archipelago Connected` on the save file