# Shahrazad setup

## Required Software

1. None

## How do I install this randomizer?

1. Nothing to install

## Where do I get a config file (aka "YAML") for this game?

Yaml files are configuration files that tell Archipelago how you'd like your game to be randomized, even if you're only using default options.
When you're setting up a multiworld, every world needs its own yaml file.

There are three basic ways to get a yaml:
* You can go to the [Player Options](https://archipelago.gg/games/Starcraft%202/player-options) page, set your options in the GUI, and export the yaml.
* You can generate a template, either by downloading it from the [Player Options](https://archipelago.gg/games/Starcraft%202/player-options) page or by generating it from the Launcher (ArchipelagoLauncher.exe). The template includes descriptions of each option, you just have to edit it in your text editor of choice.
* You can ask someone else to share their yaml to use it for yourself or adjust it as you wish.

Remember the name you enter in the options page or in the yaml file, you'll need it to connect later!

Note that the basic Player Options page doesn't allow you to change all advanced options, such as excluding particular units or upgrades. Go through the [Weighted Options](https://archipelago.gg/weighted-options) page for that.

Check out [Creating a YAML](https://archipelago.gg/tutorial/Archipelago/setup/en#creating-a-yaml) for more game-agnostic information.

## Common yaml questions
#### How do I know I set my yaml up correctly?

The simplest way to check is to test it out. Save your yaml to the Players/ folder within your Archipelago installation and run ArchipelagoGenerate.exe. You should see a new .zip file within the output/ folder of your Archipelago installation if things worked correctly. It's advisable to run ArchipelagoGenerate through a terminal so that you can see the printout, which will include any errors and the precise output file name if it's successful. If you don't like terminals, you can also check the log file in the logs/ folder.

## How do I join a MultiWorld game?

1. Run TextClient.exe.
   - macOS users should instead follow the instructions found at ["Running in macOS"](#running-in-macos) for this step only.
2. Type `/connect [server ip]`.
   - If you're running through the website, the server IP should be displayed near the top of the room page.
3. Type your slot name from your YAML when prompted.
4. If the server has a password, enter that when prompted.
