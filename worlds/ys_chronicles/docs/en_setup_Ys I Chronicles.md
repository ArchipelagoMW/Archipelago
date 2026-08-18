# Ys I Chronicles Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) (0.6.6 or later)
- Ys I & II Chronicles+ (Steam, PC version)
- CrossOver or Wine (for macOS/Linux)
- i686-w64-mingw32-gcc (32-bit cross-compiler)

## Installation

1. Build the apworld and DLL: `./build_apworld.sh`
2. Copy `ys_chronicles.apworld` to your Archipelago worlds directory
3. Deploy the mod to your game directory: `./setup_mod.sh`

## Game Setup

1. The mod installs as a `steam_api.dll` proxy — no game files are modified
2. Create `ap_connect.txt` in your game directory with your server info:
   ```
   server=localhost:38281
   slot=YourName
   password=
   ```
3. Launch the game normally through Steam or CrossOver

## Joining a Multiworld

1. Generate a seed using `ArchipelagoGenerate` with your YAML config
2. Host the server using `ArchipelagoServer` with the generated zip
3. Launch the game — the mod connects automatically
4. Connection status is displayed on screen (green = connected)

## Gameplay

- Play the game normally
- Chests, NPC gifts, boss kills, and shop purchases are location checks
- Items you receive from other players appear automatically in your inventory
- The AP server is the source of truth — your inventory syncs on every save load
