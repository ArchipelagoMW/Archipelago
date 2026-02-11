# PEAK Archipelago Mod

An Archipelago integration mod for the game PEAK, allowing the game to be played as part of a multiworld randomizer.

Also available on Thunderstore: https://thunderstore.io/c/peak/p/PeakArchipelago/PEAKPELAGO/

## Overview

This mod connects PEAK to the [Archipelago](https://archipelago.gg/) multiworld randomizer system. Ascent unlocks, badges, and other progression items are randomized across multiple games and players, creating a unique cooperative or competitive experience.

Nothing is randomized per say in this mod as PEAK is already slightly random at its core. Yes there are some checks that rely on the biomes that can be locked each day. There are mods that can potentially allow you to pick which biome is played, but I have not tested any of these myself so do so at your own risk.

The multiplayer exclusive items are added to the regular pool of items to allow full singleplayer play.

In multiplayer, only the Host's AP slot is affected. Any player who joins that hosts world is essentially just an extension of the host when it comes to sending/recieving checks from Archipelago.

## Features

- **Ascent Progression**: Unlock ascents (1-7) by receiving Archipelago items
- **Badge Randomization**: Badges are tracked and managed through Archipelago
- **Location Checks**: Game events and collectibles send progression to other players
- **DeathLink Support**: Optional death synchronization with other players
- **RingLink Support**: Optional support for linking Stamina to Rings in participating games. Consuming edible items will have effects on Rings
- **HardRingLink Support**: Optional support for linking Stamina to Rings in participating games. Certain actions and events will have effects on Rings
- **Auto-Reconnect**: Automatically reconnects to the Archipelago server if disconnected
- **Persistent State**: Tracks received items and checked locations across game sessions
- **Real-time Integration**: Seamlessly integrates with PEAK's gameplay

## Configuration

### World Options

When generating an Archipelago game, the following PEAK-specific options are available:

- **Goal**: Choose between "Reach Peak", "Complete All Badges", "24 Karat Badge" or "Reach Peak and Complete All Badges"
- **Required Ascent Count**: Number of ascents needed to complete (0-7, default: 4)
- **Required Badge Count**: Number of badges needed for badge completion goal (10-50, default: 20)
- **Progressive Stamina**: Start with 25% Stamina and require finding Progressive Stamina Bars to reach 100%
- **Additional Stamina**: With Progressive Stamina enabled, find 4 extra Stamina Bars to reach a total of 200% Stamina
- **Trap Weigh Percent**: Determine the amount of filler items to get replaced with traps.
- **Ring Link**: Enable RingLink with other linked players.
- **Hard Ring Link**: Enable HardRingLink with other linked players.
- **Trap Link**: Enable TrapLink with other linked players.
- **Energy Link**: Enable EnergyLink to utilize a linked Energy bank with other linked players.
- **Death Link**: Enable death synchronization with other players
- **Death Link Behavior**: Choose between full run reset or checkpoint reset
- **Death Link Send Behavior**: Choose between sending on any players death or on failed run

## How to Play

1. **Generate a Multiworld**:
    - Create a YAML configuration for your PEAK world
    - Generate the multiworld using Archipelago's generator
    - Host or join a multiworld session

2. **Start PEAK**:
    - Launch the game with the mod installed
    - The in-game UI will show connection status

3. **Connect to Archipelago**:
    - Use the in-game menu in the top left
    - Fill in the connection details and click Connect or hit Enter

4. **Play the Game**:
    - Ascents are initially locked - unlock them by receiving items
    - Collecting items and completing objectives sends checks to other players
    - Receive items from other players as they complete their objectives
    - Work together (or compete) to complete your goals!

## Troubleshooting

### Plugin Not Loading
- Verify BepInEx is installed correctly
- Check `BepInEx/LogOutput.log` for errors
- Ensure all dependencies are in the plugins folder

### Cannot Connect to Server
- Verify server address and port in config
- Check firewall settings
- Ensure the Archipelago server is running and accessible

### Items Not Received
- Check connection status in UI
- Verify slot name matches your generated world
- Review state file for corruption: `BepInEx/config/Peak.AP.state.*.txt`

### Locations Not Checking
- Ensure you're connected to the server
- Check that the location exists in the world definition
- Review debug logs for check submission errors

## Credits

- **Mod Contributors**: ArchipelagoBrad, ManNamedGarbo, [Mickemoose](https://ko-fi.com/mickemoose), [Dmonet](https://bsky.app/profile/dmonett.bsky.social)
- **EnergyLink Vendor Assets**: [Dmonet](https://bsky.app/profile/dmonett.bsky.social)
- **Archipelago**: [Archipelago Team](https://archipelago.gg/)
- **PEAK**: [Landfall](https://landfall.se/) & [Aggro Crab](https://aggrocrab.com/)
- **BepInEx**: [BepInEx Team](https://github.com/BepInEx/BepInEx)

## Version

Current Version: **0.5.8**

## Links

- [Archipelago Website](https://archipelago.gg/)
- [Archipelago Discord](https://discord.gg/archipelago)
- [BepInEx Documentation](https://docs.bepinex.dev/)

---

**Note**: This is a fan-made mod and is not affiliated with or endorsed by the original PEAK developers.

