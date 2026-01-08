# Setup Guide for Spyro 2 Archipelago

## Important

As the mandatory client runs only on Windows, no other systems are supported.

Important: As the mandatory client runs only on Windows, no other systems are supported.

- [Duckstation](https://www.duckstation.org) - Detailed installation instructions for Duckstation can be found at the above link.
- Archipelago version 0.6.1 or later.
- The [Spyro 2 Archipelago Client and .apworld](https://github.com/Uroogla/S2AP/releases)
- A legal US Spyro 2: Ripto's Rage ROM.  We cannot help with this step.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

This also includes instructions on generating and hosting the file.  The "On your local installation" instructions
are particularly important.

### Where do I get a config file?

Run `ArchipelagoLauncher.exe` and generate template files.  Copy `Spyro 2.yaml`, fill it out, and place
it in the `players` folder.

Alternatively, if you are using the local Webhost rather than [archipelago.gg](archipelago.gg), the Player Options page allows you to configure
your personal options and export a config file from them. Player options page: [Spyro 2 Player Options Page](/games/Spyro%202/player-options).

### Verifying your config file

If you would like to validate your config file to make sure it works and are using the local Webhost,
you may do so on the YAML Validator page. YAML validator page: [YAML Validation page](/mysterycheck).

## Generate and host your world

Run `ArchipelagoGenerate.exe` to build a world from the YAML files in your `players` folder.  This places
a `.zip` file in the `output` folder.

You may upload this to [the Archipelago website](https://archipelago.gg/uploads) or host the game locally with
`ArchipelagoHost.exe`.

## Setting Up Spyro 2 for Archipelago

1. Download the S2AP.zip and spyro2.apworld from the GitHub page linked above.
2. Double click the apworld to install to your Archipelago installation.
3. Extract S2AP.zip and note where S2AP.Desktop.exe is.
4. Open Duckstation and load into Spyro 2: Ripto's Rage.
5. In Duckstation, navigate to Settings > Game Properties > Console and select "Interpreter" under "Execution Mode".
6. Start a new game (or if continuing an existing seed, load into that save file).
7. Open S2AP.Desktop.exe, the Spyro 2 client.  You will likely want to do so as an administrator.
8. In the top left of the Spyro 2 client, click the "burger" menu to open the settings page.
9. Enter your host, slot, and optionally your password.
10. Click Connect. The first time you connect, a few error messages may appear - these are okay.
11. Start playing!