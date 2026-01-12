# Factorio Modded Randomizer Setup Guide

## Required Software

##### Players

- Factorio: [Factorio Official Website](https://factorio.com)
    - Needed by Players and Hosts

##### Factorio server Hosts (Not ap Hosts)

- Factorio: [Factorio Official Website](https://factorio.com)
    - Needed by Players and Hosts
- Archipelago: [Archipelago Releases Page](https://github.com/ArchipelagoMW/Archipelago/releases)
    - Needed by Hosts

## Create a Config (.yaml) File

### What is a config file and why do I need one?

Your config file contains a set of configuration options which provide the generator with information about how it
should generate your game. Each player of a multiworld will provide their own config file. This setup allows each player
to enjoy an experience customized for their taste, and different players in the same multiworld can all have different
options.

### Where do I get a config file?

Install the custom APWorld this can be getting it from the [github](https://github.com/Osiris32-and-a-half/BobFactorioAP/releases)
and double-clicking the `.apworld` or adding it to archipelago's custom world folder.

Reload the ap launcher.

If you want to play with custom packs add them to the new `factorio_mods\packs` folder in the archipelago folder.

Then in the ap launcher find and run "Generate template options" this will generate and open up the template folder
the latest YAML name is currently `Factorio Bob's.yaml`


## Connecting to Someone Else's Factorio Game

Connecting to someone else's game is the simplest way to play Factorio with Archipelago. It allows multiple people to
play in a single world, all contributing to the completion of the seed.

1. Acquire the Archipelago mod for this seed. This needs to be obtained from the ap host.
2. Copy the mod file into your Factorio `mods` folder, which by default is located at:  
   `%appdata%\Factorio\mods` or alongside factorio.exe ensure it has all the mods needed to run the modpack you have chosen
3. Get the server address from the person hosting the game you are joining.
4. Launch Factorio
5. Click on "Multiplayer" in the main menu
6. Click on "Connect to address"
7. Enter the address into this box
8. Click "Connect"

## Prepare to Host Your Own Factorio Game

### Defining Some Terms

In Archipelago, multiple Factorio worlds may be played simultaneously. Each of these worlds must be hosted by a Factorio
server, which is connected to the Archipelago Server via middleware.

This guide uses the following terms to refer to the software:

- **Factorio Client** - The Factorio instance which will be used to play the game.
- **Factorio Server** - The Factorio instance which will be used to host the Factorio world. Any number of Factorio
  Clients may connect to this server.
- **Archipelago Client** - The middleware software used to connect the Factorio Server to the Archipelago Server.
- **Archipelago Server** - The central Archipelago server, which connects all games to each other.

### What a Playable State Looks Like

- An Archipelago Server
- The generated Factorio Mod, created as a result of running `ArchipelagoGenerate.exe`
- One running instance of the ap "FactorioBobs Client" found inside the ap launcher
- A running modded Factorio Server, which should have been started by the Archipelago Client automatically
- A running modded Factorio Client

#### Configure your Archipelago Installation

If you did not place a Factorio standalone in your Archipelago installation, the first time you run the client a dialog will open to locate `Factorio.exe`.

If you need to change this in the future the setting is located in `host.yaml` file 
inside your Archipelago installation directory so that it points to your standalone Factorio executable. Here is an 
example of the appropriate setup, note the double `\\` are required:

```yaml
factorio_bobs_options:
  executable: C:\\path\\to\\factorio\\bin\\x64\\factorio"
```

## Hosting Your Own Factorio Game

1. Get the Factorio mod for this Archipelago seed from the ap host. It should be named `AP_*.zip`, where `*` is the seed number.
2. Copy the mod file into your Factorio `mods` folder, which by default is located at:  
   `%appdata%\Factorio\mods` or alongside factorio.exe ensure it has all the mods needed to run the modpack you have chosen
3. Get the Archipelago Server address from the website's host room, or from the server host.
4. Run your Archipelago Client, which is named `FactorioBobs Client` inside the ap launcher. 
5. Enter `/connect [server-address]` into the input box at the bottom of the Archipelago Client and press "Enter"
6. Enter `/start_client` this will start a factorio client that should use the same mods as the server
7. If the client fails to connect
8. Click on "Multiplayer" in the main menu
9. Click on "Connect to address"
10. Enter `localhost` into the server address box
11. Click "Connect"

For additional client features, issue the `/help` command in the Archipelago Client. Once connected to the AP server,
you can also issue the `!help` command to learn about additional commands like `!hint`.
For more information about the commands you can use, see the [Commands Guide](/tutorial/Archipelago/commands/en) and
[Other Options](#other-options).

## Allowing Other People to Join Your Game

1. Ensure your Archipelago Client is running.
2. Ensure port `34197` is forwarded to the computer running the Archipelago Client.
3. Obtain your IP address by visiting whatismyip.com: [WhatIsMyIP Website](https://whatismyip.com/).
4. Provide your IP address to anyone you want to join your game, and have them follow the steps for
   "Connecting to Someone Else's Factorio Game" above.

## Enabling Peaceful Mode

By default, peaceful mode is disabled. There are two methods to enable peaceful mode:

### By config file
You can specify Factorio game options such as peaceful mode and terrain and resource generation parameters in your
config .yaml file by including the `world_gen` option. This option is currently not supported by the web UI, so you'll
have to manually create or edit your config file with a text editor of your choice.
The [template file](/static/generated/configs/Factorio.yaml) is a good starting point and contains the default value of
the `world_gen` option. If you already have a config file you may also just copy that option over from the template.
To enable peaceful mode, simply replace `peaceful_mode: false` with `peaceful_mode: true`. Finally, use the
[.yaml checker](/check) to ensure your file is valid.

### After starting
If you have already submitted your config file, generated the seed, or even started playing, you can retroactively
enable peaceful mode by entering the following commands into your Archipelago Factorio Client:
```
/factorio /c game.surfaces[1].peaceful_mode=true
/factorio /c game.forces["enemy"].kill_all_units()
```
(If this warns you that these commands may disable achievements, you may need to repeat them for them to take effect.)

## Other Options

### filter_item_sends

By default, all item sends are displayed in-game. In larger async seeds this may become overly spammy.
To hide all item sends that are not to or from your factory, do one of the following:
- Type `/toggle-ap-send-filter` in-game
- Type `/toggle_send_filter` in the Archipelago Client
- In your `host.yaml` set
```
factorio_bobs_options:
  filter_item_sends: true
```

### bridge_chat_out
By default, in-game chat is bridged to Archipelago. If you prefer to be able to speak privately, you can disable this
feature by doing one of the following:
- Type `/toggle-ap-chat` in-game
- Type `/toggle_chat` in the Archipelago Client
- In your `host.yaml` set
```
factorio_bobs_options:
  bridge_chat_out: false
```
Note that this will also disable `!` commands from within the game, and that it will not affect incoming chat.

### Alternate mods folder

By default, the APWorld will look for factorio's mod's folder in commonly known locations.
If this fails, or you want to use a different mod folder, you can set it in `host.yaml`. 

```
factorio_bobs_options:
  mod_directory: null
```


## Troubleshooting

In case any problems should occur, pop by the customs discord channel https://discord.com/channels/731205301247803413/1426234278462750860

## Additional Resources

- Factorio Speedrun Guide: [Factorio Speedrun Guide by Nefrums](https://www.youtube.com/watch?v=ExLrmK1c7tA)
- Factorio Wiki: [Factorio Official Wiki](https://wiki.factorio.com/)
