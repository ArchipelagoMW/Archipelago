# Mystical Ninja Starring Goemon Randomizer (Archipelago)

This is a randomizer for Mystical Ninja Starring Goemon (N64) that integrates with the [Archipelago multiworld randomizer](https://archipelago.gg/). This randomizer shuffles items, equipment, abilities, and other game elements across multiple worlds and players in a connected multiworld session.

## What is Archipelago?

Archipelago is a multiworld randomizer framework that allows you to play randomized games with friends across different titles. Items from your game can end up in other players' worlds, and vice versa, creating a collaborative randomizer experience.

## Features

This randomizer includes the following options and features:

### Randomizer Options
- **Enemy Randomization**: Enemies throughout the game are shuffled
- **Starting Room Randomization**: Your starting spawn location is randomized
- **Increased Pot Ryo**: Pots contain more money for better progression balance
- **Health in Item Pool**: Health upgrades are added to the randomized item pool
- **Prevent One-Way Softlocks**: Normally one-way entrances are locked off to prevent softlocks

### Randomized Items
The randomizer shuffles a comprehensive set of items including:
- **Keys**: Silver, Gold, Diamond, and Jump Gym keys
- **Equipment**: Chain Pipe, Bazooka, Meat Hammer, Wind-up Camera, Ice Kunai, Medal of Flames, Flute
- **Abilities**: Mermaid, Mini Ebismaru, Sudden Impact, Jetpack
- **Characters**: Goemon, Yae, Ebismaru, Sasuke
- **Quest Items**: Cucumber, Super Pass
- **Collectibles**: Fortune Dolls (Silver/Gold), Mr. Elly Fant and Mr. Arrow collectibles, Achilles Heel
- **Upgrades**: Strength upgrades and Surprise Packs
- **Health Items**: Golden and Normal Health pickups (when enabled)~~~~

## How It Works

This randomizer consists of two main components:

1. **APWorld File (`mnsg.apworld`)**: Contains the randomizer logic, item definitions, location mappings, and game rules for Archipelago
2. **Recomp Mod**: A native code modification for Mystical Ninja Starring Goemon: Recompiled that implements the randomizer features in-game

When you generate a randomized seed in Archipelago, it creates a data file that the recomp mod reads to determine item placements, enemy randomization, and other randomized elements.
