# Encounter Plando guide for Pokémon Black and White

## How does this work?

The Encounter Plando option in your yaml file lets you force place certain Pokémon species into certain slots.
Every encounter table (one for each map that has wild Pokémon) in the game contains 56 slots, 
grouped into different encounter methods (grass, surfing, etc.), 
with each slot containing the species, a minimum catch level, and a maximum catch level.
Every entry in your Encounter Plando option will place a specific species into one or more slots of an 
encounter method in an encounter table.
Encounter Plando entries take priority over wild Pokémon randomization and works regardless of whether 
you even have wild Pokémon randomized or not.

## Important notes for multiworld hosts

Encounter Plando can lead to generation failures that might not look like coming from this option. 
The Pokémon Black and White host.yaml settings have a toggle to enable or disable this option, 
which is by default set to true. 
If disabled, yamls with Encounter Plando entries will ignore them and just print a warning to the console 
without stopping multiworld genration.

## How do I use it?

Every entry consists of 3 to 5 arguments:
- `map` determines which map (i.e. which encounter table) this entry should be placed into. 
  You can find a list of all map names on [this site](maps.md).
  The map names must match the names on that site exactly.
- `seasons` is an optional argument that determines which season(s) this entry should be placed into. 
  However, not all maps support different encounters for different seasons. 
  You can find a list of all map supporting different seasons on [this site](maps.md).
  If the map does not support different seasons, you **have to omit** this argument.
  Else, you can either write a single season or a list of seasons, with all of them starting with 
  an uppercase letter (i.e. `Spring`, `Summer`, `Autumn`, and `Winter`).
- `method` determines which encounter method this entry should be placed into. 
  Allowed method names are `Grass`, `Dark grass`, `Rustling grass`, `Surfing`, `Surfing rippling`, 
  `Fishing`, and `Fishing rippling`.
  Note that the floor of caves/dungeons/etc. count as `Grass` and dust clouds 
  and flying Pokémon's shadows count as `Rustling grass`.
- `slots` is an optional argument that determines the exact slot(s) of the entry in the specified method.
  You can either put in a single number, a list of numbers, or omit this argument.
  If omitted, this entry will be placed into all slots of the specified method.
  See [this site](slot%20values.md) for further information on allowed values.
- `species` determines which species should be placed into the specified slot(s).
  You can either put in a single species name or a list of species names.
  If multiple species are provided, a random one out of them is chosen.
  Writing the same species multiple times is allowed and can increase its chance of being chosen over 
  the other species in the list.
  See [this site](species.md) for a list of all species names. 
  Note that different forms have different names, e.g. Unown (A)/(B)/...

All entries are applied to the world in the order in which they are written into the yaml.
If multiple entries specify the same slot(s), the last one will overwrite the previous ones.
Specifying a slot that does not exist in the game (e.g. `Grass` slots in Striaton City) will not have any effect
on the game since all encounter tables have space for each encounter method, 
but it will also not be considered in logic and give no warning or error message.

## An example on how using this option could look like

```
...

Pokemon Black and White:
  ...
  
  encounter_plando:
    - map: Route 1
      method: Grass
      species: Blastoise
    - map: Route 8
      seasons: Summer
      method: Surfing
      slots: 4
      species: Liligant
    - map: Twist Mountain (Upper Level)
      seasons:
        - Spring
        - Winter
      method: Grass
      slots:
        - 0
        - 2
        - 4
        - 6
        - 8
        - 10
      species:
        - Snorlax
        - Dragonite
        - Kingdra
        - Bidoof
```
