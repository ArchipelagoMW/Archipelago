# The Legend of Zelda: Skyward Sword Randomizer Archipelago World Setup

This is the official Archipelago World for Skyward Sword.

From now on, Archipelago may be referred to as "AP". Skyward Sword may be referred to as "SS".

### What you'll Need
- The latest release of [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest)
- [Dolphin Emulator](https://dolphin-emu.org/download/) (use the dev version!) or a homebrewed Wii or Wii U console that can connect to the Internet.
- A `The Legend of Zelda: Skyward Sword` unrandomzied US 1.00 iso
- The Skyward Sword AP World:
    - This includes the [APWorld file and the YAML options file](https://github.com/Battlecats59/SS_APWorld/releases/latest)
    - You must also download the SS game patcher, which will also be available in the release above
    - To see all releases and pre-releases, visit the [SS AP release page](https://github.com/Battlecats59/SS_APWorld/releases)

### Useful Links
- [Archipelago Setup Guide](https://archipelago.gg/tutorial/Archipelago/setup/en)
- [SS AP Troubleshooting Guide](https://github.com/Battlecats59/SSArchipelago/blob/ss/worlds/ss/docs/troubleshooting_en.md)
- [Archipelago Main Discord](https://discord.gg/8Z65BR2)
- [The SS APWorld Suggestion Page](https://github.com/Battlecats59/SS_APWorld/discussions/24)
- [The SS APWorld Issue Page](https://github.com/Battlecats59/SS_APWorld/issues)
- [Trackers and other useful tools](#trackers)

### Setting up Archipelago
- Open the Archipelago launcher and click the `Install APWorld` button
- Locate your `ss.apworld` file that you downloaded earlier
- After Archipelago installs the world, restart AP
- If running from source, see [Running from Source](#running-from-source)

### Editing your YAML file
- You should have downloaded a YAML file named `Skyward Sword.yaml` with the APWorld.
- Open this file in any text editor
    - [Visual Studio Code](https://code.visualstudio.com/Download) is a good option, it will color-code the text to make it easier to read
    - Any text editor will work, but with simple ones such as notepad, be sure to keep the indentations consistent
- Scroll through the file and set the options to whatever you would like. The integer next to each option will determine the weighting of that option being chosen. If you want to make sure an option is set to a certain value, set the weight to 50 for that value and the weights for other values to 0.
    - Don't hesitate to ask someone from the community for guidance if you are struggling with editing the options yourself.
- After you set your options to your prefered settings, save the YAML file and send it to the world host.

### Joining a Multiworld
- To join a multiworld, edit your YAML file to your desired settings and send the file to the multiworld host. They will use your YAML, along with those of the other players, to generate the multiworld.
- The host should send you a APSSR file named accordingly: `AP_{seed}_P{player id}_{player name}.apssr`. If the title of this file does not fit the template, ask the host if something went wrong. See example below.
- Open the AP release of the Skyward Sword Randomizer. Set your output folder to wherever you would like the randomized iso placed. Set the APSSR file in the randomizer window to the APSSR file that you just received from the host. **MAKE SURE that you put in the correct APSSR file.**
- Set your cosmetic options in the randomizer window and select randomize.
    - NOTE: If you want to play on console, you **must** enable the `Use Wii UDP Socket` option before randomizing.
- After randomization, see [Setting up your Client (Dolphin Emulator)](#setting-up-your-client-dolphin-emulator) or [Setting up your Client (Wii Console)](#setting-up-your-client-wii-console).

### Setting up your Client (Dolphin Emulator)
- After opening the randomized iso in Dolphin, open the `Skyward Sword Client` in Archipelago.
    - Make sure your in game hash (on the top of the file select screen) is the same that the randomizer gave you when you generated the iso. It should be `AP P{player id} {three random words}`.
    - If your client does not open, follow the steps listed [here](https://github.com/Battlecats59/SS_APWorld/releases/tag/DME) to make sure the DME package is installed.
- Make sure the client hooks to Dolphin, then begin a new file in game.
    - **NOTE: It is recommended that all 3 files in-game are empty. This will prevent any confusion with the client later on.**
    - **NOTE: You MUST play the multiworld on file 1. To prevent issues with location checking in BiT, the client will only send locations and give items if it detects you on file 1. You may use the other 2 files for BiT Magic files or corrupt files, however.**
    - Your filename in game does not need to match your AP slot name
- Connect to the room in your client by running `/connect {address}`. The link to the room should be given to you by the multiworld host. The address will be in the form of `archipelago.gg:XXXXX`.
    - If you get an invalid slot error, make sure you generated with the latest build of the randomizer, you generated using the correct APSSR file, and you opened the correct iso in Dolphin.
    - Your slot name will be hardcoded into the game itself, and your client will read that from memory to connect you to the room.
- Wait until everyone is in game and ready before you leave Link's room. See [Playing the Game](#playing-the-game).
- Run `/help` in the client to see all commands.
- Though the client defaults to Dolphin Emulator connection, you may switch to console mode by running the `/console` command with the Wii's on-screen IP address, as described below. Likewise, while in console mode, you may run `/dolphin` to return to Dolphin mode.

### Setting up your Client (Wii Console)
- Transfer your randomized iso to a USB drive (or generate directly onto it), and insert the USB drive into your console.
- Before opening the randomized iso, make sure your Wii is connected to the Internet on the same network the computer running your client is on.
    - The Wii can only connect to the 2.4 GHz WiFi band, so you may need to ensure your computer is also on this band if you have two separate networks.
- Use a USB loader such as USB Loader GX, Wiiflow, or CFG USB Loader to open the randomized iso.
    - After a few seconds, the game should display a message of the form `Waiting for connection from AP client Type /console [ip]`
    - If it doesn't display this message and instead shows an error code, follow the instructions on-screen and try relaunching your game.
    - If the problem persists, double check your Wii's connection settings, or consider using an Ethernet connection.
- After opening the randomized iso, open the `Skyward Sword Client` in Archipelago.
    - Make sure your in game hash (on the top of the file select screen) is the same that the randomizer gave you when you generated the iso. It should be `AP P{player id} {three random words}`.
    - If your client does not open, follow the steps listed [here](https://github.com/Battlecats59/SS_APWorld/releases/tag/DME) to make sure the DME package is installed.
- By default, the client waits for an instance of Dolphin to connect to. Switch to console mode and connect your client to your console by running `/console {on-screen IP address}`. The shown IP is the private IP of the console on which it is listening for connections.
    - If successful, the AP client will confirm the connection, and the text on-screen will disappear. Otherwise, check to ensure your computer is on the same network as the console, or follow the error code-related instructions on-screen.
    - **NOTE: It is recommended that all 3 files in-game are empty. This will prevent any confusion with the client later on.**
    - **NOTE: You MUST play the multiworld on file 1. To prevent issues with location checking in BiT, the client will only send locations and give items if it detects you on file 1. You may use the other 2 files for BiT Magic files or corrupt files, however.**
    - Your filename in game does not need to match your AP slot name
- Connect to the room in your client by running `/connect {address}`. The link to the room should be given to you by the multiworld host. The address will be in the form of `archipelago.gg:XXXXX`.
    - If you get an invalid slot error, make sure you generated with the latest build of the randomizer, you generated using the correct APSSR file, and you opened the correct iso.
    - Your slot name will be hardcoded into the game itself, and your client will read that from memory to connect you to the room.
- Wait until everyone is in game and ready before you leave Link's room. See [Playing the Game](#playing-the-game).
- Run `/help` in the client to see all commands.
- Due to the Wii using UDP to communicate with your AP client, the client is likely to drop some packets from the Wii. If only one packet is lost, it will automatically send another confirmation packet, and will stay connected if that packet gets a response. Otherwise, the client will lose connection, and will attempt to reconnect after five seconds.

### Playing the Game
- Once the game is started, you will receive items that other players pick up for you while Link is in a state where he can receive items.
- If you find an item that belongs to someone else, it will appear as a letter and the game will say that you received an Archipelago item.
    - Some AP items from other Skyward Sword games, such as B items and boss keys, will appear as their normal model, held in front of link. The game will say that you found someone else's (item name).
    - AP items in Beedle's shop will tell you what item it is and who it belongs to, so you know if you should purchase it or not. Keep in mind, you may need to buy some items to unlock or view items hidden behind that item.
- When you beat the game, make sure the client detects that and releases your items to the other players.
    - The game should release your items upon landing the final blow on Demise. If the `skip-demise` option is enabled, it will release your items upon clearing the Fi text before entering the Demise portal.
- Keep an eye on the client while playing. If you check a location that isn't sent over AP, you may need the host to run `/send_location (player name) (location name)`. Alternatively, if the client says that you received an item, yet you're standing still, on the ground, in game and you haven't received the item, you may need the host to manually send the item again.

### Trackers
**There are several trackers you can use with Skyward Sword for Archipelago:**
- [Skyward Sword Archipelago Web Tracker](https://youraveragelink.github.io/SSR-AP-Tracker) (created by YourAverageLink and robojumper)
    - This is the recommended tracker for multiworld via archipelago, since it will auto track items and locations.
    - On the setup screen, input the AP room address and your slot name to connect.
    - When you click "connect", the tracker will automatically input all settings and locations for you.
        - Once you are connected, click "launch new tracker" to begin.
- [Skyward Sword Randomizer Web Tracker](https://robojumper.github.io/SS-Randomizer-Tracker/) (created by robojumper)
    - [Web Tracker Guide](https://robojumper.github.io/SS-Randomizer-Tracker/guide)
    - This is recommended if you want to manually track your game.
    - Set the release to "Latest Development Build (ssrando/main)"
    - You can manually put in all of the settings, or paste in a settings string **(recommended)**.
        - The settings string for the last generated seed can be copied from the randomizer application, in the box right above the "Randomize" button.
        - The settings string is also printed into the console that opens alongside the randomizer application. After seed generation, you can open the console and copy the settings string from there.
        - The settings string can also be found in the spoiler log generated by the SSR patcher itself.
            - Locate your ssrando.exe application, and find the logs folder in that directory.
            - Find the spoiler log corresponding to your current run. The seed and hash that were generated will also be in the spoiler log.
            - The settings string will be the "permalink" in the spoiler log file.
        - If you paste in a settings string, it is significantly quicker and it will include all of the starting items and excluded locations from the seed. 
- Archipelago Universal Tracker
    - It is recommended that you hide excluded locations in the tracker, as they will all appear as sphere 0 checks.
    - Don't worry, these locations will always contain junk items.

**Other useful tools:**
- [Skyward Sword Randomizer Location Guide](https://docs.google.com/document/d/1F8AmQccCvtblnRhw_kEAVTME_xX1-O_9Ln16TVDPx6w/edit?tab=t.0#heading=h.9bzfdyr09f0y)
    - Helpful if this is one of your first times playing the randomizer
- [Thrill Digger Solver](https://lepelog.github.io/thrill-digger/) by lepelog
- [BiT Tutorial Playlist](https://www.youtube.com/playlist?list=PLYgB2odQu_OYCJ6EgT-KM-orvbv3Qet2l) by Peppernicus

### Generating a multiworld
For information on generating an AP world, visit the [Archipelago Setup Guide](https://archipelago.gg/tutorial/Archipelago/setup/en#generating-a-multiplayer-game).

### Running from Source
Archipelago requires python 3.10.11 or newer (not the Windows Store version) and Git
1. Clone the SSArchipelago repository:
```
git clone https://github.com/Battlecats59/SSArchipelago
cd SSArchipelago
```
2. Checkout the `ss` branch
```
git checkout ss
```
3. Install dependencies
```
py ModuleUpdate.py
```
4. Run the launcher. The Skyward Sword world is already installed.
```
py Launcher.py
```
5. Additional Python Scripts (comments begin with #)
```
py Generate.py     # Generates a multiworld with the YAMLs in the /Players/ folder
py MultiServer.py  # Hosts the multiworld locally, using the generated MW file as a param
py WebHost.py      # Hosts the Archipelago website locally
```

Refer to the following AP guides for more information on running from source.
- [Running from source on Windows](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/running%20from%20source.md)
- [Running from source on macOS](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/generic/docs/mac_en.md)

### Discord
Discussion regarding this APWorld is in the [Archipelago Main Discord](https://discord.gg/8Z65BR2), in the Skyward Sword thread under the `future-game-design` channel.

- [Skyward Sword Randomizer Discord](https://discord.gg/evpNKkaaw6)
- [Skyward Sword HD Randomizer Discord](https://discord.gg/nNbpfH5jyG)
- [Skyward Sword Randomizer Racing Discord](https://discord.gg/cWE892y8WB)

### Credits

- **Battlecats59**: Archipelago implementation
- **YourAverageLink**: Archipelago implementation, client work, tracker implementation, console implementation
- **Harmjan387**: Significant testing and bug fixes
- **robojumper**: Client and logic work
- **Trez**: Archipelago web implementation
- **Fireworkspinner**: Early Archipelago manual designs
- **RayStormThunder**: Skyward Sword Archipelago logo design
- **lepelog**: SS Rando creator, arc work for multiworld, Rust networking code for console support
- **SS Rando Devs**: Creating the Skyward Sword Randomizer
- **tanjo3 and TWW APWorld Devs**: Created the TWW APWorld, which provided a lot of code for the SS APWorld
- **All of our APWorld testers**: Synii, Tyler Abernathy, Fireworkspinner, limited_fears, Harmjan387, DayKat, Yuvraj823, Germeister, 64bit_link, Zeldex72, spencer2585, CubeDavid, robojumper, Sledge, and others
