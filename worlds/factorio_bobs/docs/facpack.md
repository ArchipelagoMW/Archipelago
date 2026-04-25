# Table of content
1. [How to Create a FacPack](#how-to-create-a-facpack)
2. [Format specification](#format-specification)
   1. [Required files](#required-files)
      1. [header.json](#headerjson)
      2. [sciencePack.json](#sciencepackjson)
      3. [worldSettings.json](#worldsettingsjson)
      4. [recipeEngineSettings.json](#recipeenginesettingsjson)
   2. [Optional files](#optional-files)
      1. [customRecipes.json](#customrecipesjson)
      2. [startingItems.json](#startingitemsjson)
      3. [progressive.json](#progressivejson)
      4. [techsOverride.json](#techsoverridejson)

# How to Create a FacPack
Warning: currently very little varification is done on FacPacks so ensure that they are completable before sending off.
If the start is completable, it should be completable all the way through.

1. Clone this repository and set it up
   - Follow the instructions on [setting up source](../../../docs/running%20from%20source.md) ensuring pulp is installed

2. Add all content mods into factorio
   - You shouldn't install pure QOL like factory planner or FNEI as all mods installed will become requirements
   - helmod is explicitly excluded from extraction as it can be useful
   - Currently, the system does not support mods that:
     - include difference surfaces with transport conditions that are required for resources or specific recipes (no space age, space exploration)
     - changes win condition (no space age, krastorio)
     - script heavy mods (no fun mode)
     - too complex (you have to just try technically it will eventually resolve 
       but not in a reasonable amount of time, Bob's Angles has been found too complex)

3. Add the extractor https://github.com/Osiris32-and-a-half/ModdedFactorioExtractor

4. Create a fresh world and run `/ap-get-info-dump`
   - This should be done on the starting surface

5. Create a new folder in `archipelago/factorio_mods/packs` this will be the pack root folder
   - The name of this folder doesn't matter, but you might want to avoid spaces if you upload to GitHub

6. Create folder in the pack called `Extractor`
   and add the files generated in step 4 that can be found in `factorio/script-output`

7. Create required files that can be found [here](#required-files)
   - It is recommended to enable `show-debug-info-in-tooltips` on factorio as all pack settings use factorio internal names (setting can be found by hitting F4)

8. Create optional files that can be found [here](#optional-files)
   - I would highly recommend adding [startingItems.json](#startingitemsjson) and [customRecipes.json](#customrecipesjson)

9. Run `GenPrecalc.py` found in [worlds/factorio_bobs/packDevUtils/](../../../worlds/factorio_bobs/packDevUtils/GenPrecalc.py)
   - You will need to set the packname in [`Packname.py`](../../../worlds/factorio_bobs/packDevUtils/Packname.py)
   - If any changes are done to the FacPack ensure to rerun this

10. You can now zip the FacPack for distribution
    - FacPacks work in zipped and non-zipped states
    - When zipped all facpacks must start with a full stop `.`, this is for it to get excluded when put into players folder
    - Ensure that all the files are on top level of the zip

# Format specification
All files in a FacPack are in JSON format.

Capitalisation of file names is important.
## Required files

### header.json
- "packName": (required) string that will be used to select the pack in the YAML
- "downloadLocation": (required) string displayed in YAML for host to find the pack if needed
- "author": (required) string, currently unused, planned to use in error messages so people know who to shout at :P
- "version": (required) string, currently unused, planned to resolve pack conflicts
- "formatVersion": (required) string, currently unused, planned to quickly error on out of date packs
#### Example:
```json
{
  "packName": "Vanilla",
  "version": "1.0.0",
  "formatVersion": "2.0.0",
  "downloadLocation": "InternalPack",
  "author": "Osiris.3"
}
```

### sciencePack.json
JSON list containing all science packs in the order they are to be obtained
#### Example:
```json
["automation-science-pack",
"logistic-science-pack",
"military-science-pack",
"chemical-science-pack",
"production-science-pack",
"utility-science-pack",
"space-science-pack"]
```

### worldSettings.json
- "forced_locations": (optional) contains two lists of locations
	- "start": name of techs forced to be local at the start of the world (This highly suggested last chance to allow full automation)
	- "end": name of techs forced to be local at the end of the world (Suggested to put at least some technologies that are required for goal here)
#### Example:
```json
{
  "forced_locations": {
    "start": ["automation", "logistics"],
    "end": ["rocket-silo"]
  }
}
```

### recipeEngineSettings.json
- "missed_machines": (optional) dictionary containing machines that the extractor missed must contain at least the cheapest version of the machine
  - if this is needed, I would like you to tell me (Osiris.3) so I can improve the extractor
  - e.g. "machine-name": [list of categories machine supports]
- "invalid_ingredients": (optional) list of ingredients that are ignored by the AP world this will also invalidate all items that require them
- "excluded_all_pools": (optional) list of ingredients that are invalid for all science packs
- "excluded_first_pool": (optional) list of ingredients that are invalid for first science pack

#### Example:
```json
{
  "excluded_automation_ingredients": [
    "bob-diamond-ore",
    "bob-amethyst-ore",
    "bob-emerald-ore",
    "bob-topaz-ore",
    "bob-sapphire-ore",
    "bob-ruby-ore",
    "bob-bauxite-ore",
    "bob-silver-ore",
    "bob-gold-ore",
    "bob-zinc-ore",
    "bob-tungsten-ore",
    "bob-nickel-ore",
    "bob-rutile-ore"
  ],
  "invalid_ingredients": [
    "raw-fish",
    "depleted-uranium-fuel-cell",
    "bob-depleted-thorium-fuel-cell",
    "bob-depleted-deuterium-fuel-cell",
    "bob-fusion-catalyst"
  ]
}
```
## Optional files

### customRecipes.json
recipe name must follow factorio requirements:
- Only characters A-Z a-z 0-9 _- are allowed.

replace <>
- "<recipe_name>":
  - "ingredients": 
    - "<ingredient_name>": amount
    - "<ingredient_name>": amount
    - ...
  - "products": 
    - "<product_name>": amount
    - "<product_name>": amount
    - ...
  - "category": "<category_name>"
  - "energy": <time for one craft>
#### Example:
```json
{
  "temp_steam": {"ingredients": {"water": 10, "coal":  1}, "products": {"steam": 100}, "category": "crafting-with-fluid", "energy": 5},
  "mine_wood": {"ingredients": {}, "products": {"wood": 1}, "category": "crafting", "energy": 5}
}
```

### startingItems.json
replace <>
- "recipes": []
  - "<recipe_name>"
  - "<recipe_name>"
  - ...

#### Example:
```json
{
  "recipes": [
    "offshore-pump",
    "small-electric-pole",
    "boiler",
    "pipe",
    "pipe-to-ground",
    "electronic-circuit",
    "lab",
    "steam-engine",
    "copper-cable",
    "automation-science-pack"
  ]
}
```

### progressive.json
#### Example:
```json
{
  "progressive-bob-fluid-generator": [
    "bob-fluid-generator-1",
    "bob-fluid-generator-2",
    "bob-fluid-generator-3"
  ],
  "progressive-worker-robots-storage": [
    "worker-robots-storage-1",
    "worker-robots-storage-2",
    "worker-robots-storage-3",
    "bob-infinite-worker-robots-storage-4"
  ],
  "progressive-physical-projectile-damage": [
    "physical-projectile-damage-1",
    "physical-projectile-damage-2",
    "physical-projectile-damage-3",
    "physical-projectile-damage-4",
    "physical-projectile-damage-5",
    "physical-projectile-damage-6",
    "physical-projectile-damage-7"
  ]
}
```
### techsOverride.json
#### Example:
```json
{
  "bob-long-inserters-1": {"useless":  false},
  "bob-long-inserters-2": {"useless":  false},
  "bob-more-inserters-1": {"useless":  false},
  "bob-more-inserters-2": {"useless":  false},
  "bob-near-inserters": {"useless":  false}
}
```

### defaultOptions.json
only `additional_logic` in `default` is currently supported
#### Example:
```json
{
  "default": {
    "additional_logic": {
      "2": [
        {"item": "gun-turret"}
      ],
      "3": [
        {"item": "lab"},
        {"item": "transport-belt"},
        {"item": "electric-mining-drill"},
        {"item": "bob-void-pump"},
        {"recipe": "bob-basic-greenhouse-cycle"},
        {"tech": "bob-long-inserters-1"}
      ]
    }
  }
}
```