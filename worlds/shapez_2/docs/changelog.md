# Changelog
Versions are sorted in ascending order, i.e. the most recent changes are at the top.

## 0.99.5 (Hexagonal update)

- Added the hexagonal shape configuration
- Fixed milestone counts of more than 8 always crashing multiworld generation
- Fixed manual-like client not allowing to check operator levels over 100

## 0.99.4 (Who's that pokémon? update)

- Fixed bad copy-pasting of the scenario preset file content
- Tried reducing the frequency of a downgraded shape being the same as before
- Added an option to show the names of other players' items in your world (enabled by default)
  - Also added the possibility to show the receiving player's name and the item's classification

## 0.99.3 (mid-stream hotfix)

- Actually fixed fluids, wires, and trains toolbars never being unlocked
- Fixed crystals having incorrect logic in very rare cases
- Added `Unlock extensions with miners` to the `item_pool_modifiers` option
- Added `Starting platform points`, `Starting research points`, and `Starting blueprint points` to the `location_adjustments` option

## 0.99.2

- Fixed some upgrades never being unlocked
- Fixed starting milestone still being called "Rotate & Cut" and having the vanilla description
  - Also made it have a random preview image and video
- Fixed fluids, wires, and trains toolbars never being unlocked
- Fixed current research points permanently being hidden
- Added surprise out-of-logic item as upgrade (this is what actually fixes the research points visibility)
- Added goal tab to manual-like client (this also fixes not being able to send the goal flag to the server)
- Fixed multiworld output zip files being rejected by webhost if they contain a shapez 2 output zip
- Fixed `Maximum processors per milestone` in the `shape_generation_adjustments` option not working
- Prevented milestones from having the same final shape twice 
- Overhauled the classification of a bunch of items
- Tweaked `location_adjustments` option description to mention minimum required locations
- Added `Include blueprint points` to the `item_pool_modifiers` option
- Added a shape generation debug file to the output zip

## 0.99.1

- Fixed logic being broken entirely (goddammit even double-checking didn't protect me from lambdas in for loops)
- Added `Location modifiers` option with modifiers `Lock task lines`, `Lock operator lines`, and `Lock operator levels tab`
- Tweaked item generation such that starting items are actually taken into account for event generation

## 0.99.0 (pre-mod release)

- Locations:
  - 3-20 Milestones containing up to 12 items
  - 3-200 Task lines containing up to 5 checks
  - 0-100 Operator levels
- Items: 
  - Buildings, space platforms, various mechanics
  - Task line unlocks, operator line unlocks
  - Research points, blueprint points, platform points
- Options:
  - Goal: Milestones, Operator levels
  - Location adjustments: 
    - Milestones, min/max checks per milestone
    - Task lines, min/max checks per task line
    - Operator lines, random operator lines, operator level checks
    - Required shapes multiplier
  - Shape configuration: Tetragonal (for now)
  - Shape generation modifiers: Milestone operator lines
  - Shape generation adjustments: Maximum layers, maximum processors per milestone
  - Blueprint shapes:
    - Regular, hard, insane
    - Randomized
    - Plando
  - Item pool modifiers: Random starting processor, arbitrary research/blueprint points, arbitrary platform items
- Shape generator and downgrader (only tetragonal for now)
- Scenario and preset files as output
- Manual-like client

## 0.0.1 (proof of concept)

Only added 4 shapesanity-like locations, without any gameplay-altering modifications.
