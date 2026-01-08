# Setup Guide for Spyro 3 Archipelago

## Important

As the mandatory client runs only on Windows, no other systems are supported.

## Required Software

- [Duckstation](https://www.duckstation.org) - Detailed installation instructions for Duckstation can be found at the above link.
- Archipelago version 0.6.1 or later.
- The [Spyro 3 Archipelago Client and .apworld](https://github.com/ArsonAssassin/S3AP/releases)
- A legal US (NTSC-U) Spyro: Year of the Dragon v1.1 (Greatest Hits version) ROM.  We cannot help with this step.


## Create a Config (.yaml) File

### What is a config file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

This also includes instructions on generating and hosting the file.  The "On your local installation" instructions
are particularly important.

### Where do I get a config file?

Run `ArchipelagoLauncher.exe` and generate template files.  Copy `Spyro 3.yaml`, fill it out, and place
it in the `players` folder.

Alternatively, if you are using the local Webhost rather than [archipelago.gg](archipelago.gg), the Player Options page allows you to configure
your personal options and export a config file from them. Player options page: [Spyro 3 Player Options Page](/games/Spyro%203/player-options).

### Verifying your config file

If you would like to validate your config file to make sure it works and are using the local Webhost,
you may do so on the YAML Validator page. YAML validator page: [YAML Validation page](/mysterycheck).

## Generate and host your world

Run `ArchipelagoGenerate.exe` to build a world from the YAML files in your `players` folder.  This places
a `.zip` file in the `output` folder.

You may upload this to [the Archipelago website](https://archipelago.gg/uploads) or host the game locally with
`ArchipelagoHost.exe`.

## Setting Up Spyro 3 for Archipelago

1. Download the S3AP.zip and spyro3.apworld from the GitHub page linked above.
2. Double click the apworld to install to your Archipelago installation.
3. Extract S3AP.zip and note where S3AP.exe is.
4. Open Duckstation and load into Spyro: Year of the Dragon.
5. Start a new game (or if continuing an exisiting seed, load into that save file).
6. Open S3AP.exe, the Spyro 3 client.  You will likely want to do so as an administrator.
7. In the top left of the Spyro 3 client, click the "burger" menu to open the settings page.
8. Enter your host, slot, and optionally your password. 
9. Click Connect. The first time you connect, a few error messages may appear - these are okay.
10. Start playing!
