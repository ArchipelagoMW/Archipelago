# Factorio Randomizer Setup Guide

## Required Software

### Server Host
- [Factorio](https://factorio.com)
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)

### Players
- [Factorio](https://factorio.com)

## General Concept

One Server Host exists per Factorio World in an Archipelago Multiworld, any number of modded Factorio players can then connect to that world. From the view of Archipelago, this Factorio host is a client.
## Installation Procedures

### Dedicated Server Setup
You need a dedicated isolated Factorio installation that the FactorioClient can take control over, if you intend to both emit a world and play, you need to follow both this setup and the player setup.
This requires two Factorio installations. The easiest and cheapest way to do so is to either buy or register a Factorio on factorio.com, which allows you to download as many Factorio games as you want.
1. Download the latest Factorio from https://factorio.com/download for your system, for Windows the recommendation is "win64-manual".

2. Make sure the Factorio you play and the Factorio you use for hosting do not share paths. If you downloaded the "manual" version, this is already the case, otherwise, go into the hosting Factorio's folder and put the following text into its `config-path.cfg`:
```ini
config-path=__PATH__executable__/../../config
use-system-read-write-data-directories=false
```
3. Navigate to where you installed Archipelago and open the host.yaml file as text. Find the entry `executable` under `factorio_options` and set it to point to your Factorio. If you put Factorio into your Archipelago folder, this would already match.


### Player Setup
- Manually install the AP mod for the correct world you want to join, then use Factorio's built-in multiplayer.

    
## Joining a MultiWorld Game

1. Install the generated Factorio AP Mod (would be in <Factorio Directory>/Mods after step 2 of Setup)

2. Run FactorioClient, it should launch a Factorio server, which you can control with `/factorio <original factorio commands>`, 
   
    * It should start up, create a world and become ready for Factorio connections.

3. In FactorioClient, do `/connect <Archipelago Server Address>` to join that multiworld. You can find further commands with `/help` as well as `!help` once connected.

    * / commands are run on your local client, ! commands are requests for the AP server

    * Players should be able to connect to your Factorio Server and begin playing.
   
4. You can join yourself by connecting to address `localhost`, other people will need to connect to your IP 
   and you may need to port forward for the Factorio Server for those connections.