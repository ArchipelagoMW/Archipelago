# Factorio Randomizer Setup Guide

## Required Software

##### Players

- Factorio: [Factorio Official Website](https://factorio.com)
    - Needed by Players and Hosts

##### Server Hosts

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

The Player Options page on the website allows you to configure your personal options and export a config file from
them. Factorio player options page: [Factorio Options Page](/games/Factorio/player-options)

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the YAML Validator page. YAML
Validator page: [Yaml Validation Page](/check)

## Connecting to Someone Else's Factorio Game

Connecting to someone else's game is the simplest way to play Factorio with Archipelago. It allows multiple people to
play in a single world, all contributing to the completion of the seed.

1. Acquire the Archipelago mod for this seed. It should be named `AP_*.zip`, where `*` is the seed number.
2. Copy the mod file into your Factorio `mods` folder, which by default is located at:  
   `C:\Users\<YourUserName>\AppData\Roaming\Factorio\mods`
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
- One running instance of `ArchipelagoFactorioClient.exe` (the Archipelago Client) per Factorio world
- A running modded Factorio Server, which should have been started by the Archipelago Client automatically
- A running modded Factorio Client

### Dedicated Server Setup

To play Factorio with Archipelago, a dedicated server setup is required. This dedicated Factorio Server must be
installed separately from your main Factorio Client installation. The recommended way to install two instances of
Factorio on your computer is to download the Factorio installer file directly from
factorio.com: [Factorio Official Website Download Page](https://factorio.com/download).

#### If you purchased Factorio on Steam, GOG, etc.

You can register your copy of Factorio on factorio.com: [Factorio Official Website](https://factorio.com/). You will be
required to create an account, if you have not done so already. As part of that process, you will be able to enter your
Factorio product code. This will allow you to download the game directly from their website.

#### Download the Standalone Version

It is recommended to download the standalone version of Factorio for use as a dedicated server. Doing so prevents any
potential conflicts with your currently-installed version of Factorio. Download the file by clicking on the button
appropriate to your operating system, and extract the folder to a convenient location. The best place to do this for 
Archipelago is to place the extracted game folder into the `Archipelago` directory and rename it to just be "Factorio".


![Factorio Download Options](/static/generated/docs/Factorio/factorio-download.png)

Next, you should launch your Factorio Server by running `factorio.exe`, which is located at: `bin/x64/factorio.exe`. You
will be asked to log in to your Factorio account using the same credentials you used on Factorio's website. After you
have logged in, you may close the game.

#### Configure your Archipelago Installation

If you did not place the Factorio standalone in your Archipelago installation, you must modify your `host.yaml` file 
inside your Archipelago installation directory so that it points to your standalone Factorio executable. Here is an 
example of the appropriate setup, note the double `\\` are required:

```yaml
factorio_options:
  executable: C:\\path\\to\\factorio\\bin\\x64\\factorio"
```

This allows you to host your own Factorio game.

## Hosting Your Own Factorio Game

1. Obtain the Factorio mod for this Archipelago seed. It should be named `AP_*.zip`, where `*` is the seed number.
2. Install the mod into your Factorio Server by copying the zip file into the `mods` folder.
3. Install the mod into your Factorio Client by copying the zip file into the `mods` folder, which is likely located
   at `C:\Users\YourName\AppData\Roaming\Factorio\mods`.
4. Obtain the Archipelago Server address from the website's host room, or from the server host.
5. Run your Archipelago Client, which is named `ArchipelagoFactorioClient.exe`. This was installed along with
   Archipelago if you chose to include it during the installation process.
6. Enter `/connect [server-address]` into the input box at the bottom of the Archipelago Client and press "Enter"

![Factorio Client for Archipelago Connection Command](/static/generated/docs/Factorio/connect-to-ap-server.png)

7. Launch your Factorio Client
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
factorio_options:
  filter_item_sends: true
```

### bridge_chat_out
By default, in-game chat is bridged to Archipelago. If you prefer to be able to speak privately, you can disable this
feature by doing one of the following:
- Type `/toggle-ap-chat` in-game
- Type `/toggle_chat` in the Archipelago Client
- In your `host.yaml` set
```
factorio_options:
  bridge_chat_out: false
```
Note that this will also disable `!` commands from within the game, and that it will not affect incoming chat.

## Troubleshooting

In case any problems should occur, the Archipelago Client will create a file `FactorioClient.txt` in the `/logs`. The
contents of this file may help you troubleshoot an issue on your own and is vital for requesting help from other people
in Archipelago.

## Additional Resources

- Alternate Tutorial by
  Umenen: [Factorio (Steam) Archipelago Setup Guide for Windows](https://docs.google.com/document/d/1yZPAaXB-QcetD8FJsmsFrenAHO5V6Y2ctMAyIoT9jS4)
- Factorio Speedrun Guide: [Factorio Speedrun Guide by Nefrums](https://www.youtube.com/watch?v=ExLrmK1c7tA)
- Factorio Wiki: [Factorio Official Wiki](https://wiki.factorio.com/)
