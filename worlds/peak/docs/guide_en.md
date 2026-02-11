# PEAK Archipelago Mod

## Components

This mod consists of two main components:

### 1. Client Plugin (C# / BepInEx)
- **File**: `PeakArchipelagoPlugin.cs`
- **Purpose**: Runs inside the PEAK game client
- **Dependencies**: BepInEx, Archipelago.MultiClient.Net, Harmony

### 2. Archipelago World (Python)
- **Location**: `peak/` directory
- **Purpose**: Defines game logic, items, locations, and rules for the Archipelago server
- **Files**:
    - `__init__.py` - Main world definition
    - `Items.py` - Item definitions and classifications
    - `Locations.py` - Location (check) definitions
    - `Options.py` - Player-configurable options
    - `Regions.py` - Game region structure
    - `Rules.py` - Progression logic and access rules

## Installation

### Client Plugin Installation

## Manual Install
1. **Install BepInEx**:
    - Download BepInEx 5.x for your platform
    - Extract to your PEAK game directory
    - Run the game once to generate BepInEx folders

2. **Install the Plugin**:
    - Download the `peakpelago` folder from the releases
    - Drag the entire `peakpelago` folder into your `BepInEx/plugins/` directory
    - The folder contains all necessary files

3. **Launch the Game**:
    - Start PEAK - the plugin will create a configuration file on first run
    - Connect using the in game UI

### Archipelago World Installation

1. **Locate Archipelago Installation**:
    - Double click the peak.apworld file to install the PEAK AP World into your Archipelago installation

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
