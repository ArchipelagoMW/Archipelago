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
You need a dedicated isolated Factorio installation that the FactorioClient can take control over. If you intend to both host a world and play on the same device, you will need two separate Factorio installations; one for the **FactorioClient** to hook into and one for you to play on.
The easiest and cheapest way to do so is to either buy or register a Factorio key on factorio.com, which allows you to download as many Factorio games as you want. If you own a steam copy already you can link your account on the website.
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

1. Make a fresh world. Using any Factorio, create a savegame with options of your choice and save that world as Archipelago.

2. Take that savegame and put it into your Archipelago folder

3. Install the generated Factorio AP Mod

4. Run FactorioClient, it should launch a Factorio server, which you can control with `/factorio <original factorio commands>`, 
   
    * It should say it loaded  the Archipelago mod and found a bridge file. If not, the most likely case is that the mod is not correctly installed or activated.

5. In FactorioClient, do `/connect <Archipelago Server Address>` to join that multiworld. You can find further commands with `/help` as well as `!help` once connected.

    * / commands are run on your local client, ! commands are requests for the AP server

    * Players should be able to connect to your Factorio Server and begin playing.

