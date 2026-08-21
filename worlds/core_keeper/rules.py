from collections import Counter

from worlds.generic.Rules import add_item_rule, set_rule

from .locations import LOCATION_METADATA
from .options import LICENSE_OPTION_BY_ITEM


def _legacy_license_mode(options) -> int:
    """Keep the documented preliminary rules evaluable until metadata replaces them."""
    return 3


def set_rules(world) -> None:
    if world.options.raw_materials:
        requirements = {
            "Collect Scarlet Ore": {"Wall Lowered"},
            "Collect Poison Slime": {"Wall Lowered"},
            "Collect Ancient Feather": {"Wall Lowered"},
            "Collect Octarine Ore": {"Defeated Azeos"},
            "Collect Coral Wood": {"Defeated Azeos"},
            "Collect Slippery Slime": {"Defeated Azeos"},
            "Collect Sea Shell": {"Defeated Azeos"},
            "Collect Galaxite Ore": {"Defeated Omoroth"},
            "Collect Magma Slime": {"Defeated Omoroth"},
            "Collect Scarab Wingcover": {"Defeated Omoroth"},
            "Collect Blasting Dung": {"Defeated Omoroth"},
            "Collect Solarite Ore": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
            "Collect Gleam Wood": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
            "Collect Jungle Emerald": {"Defeated Druidra"},
            "Collect Ocean Sapphire": {"Defeated Crydra"},
            "Collect Desert Ruby": {"Defeated Pyrdra"},
            "Collect Pandorium Ore": {"Defeated Core Commander"},
            "Collect Calcified Shell": {"Defeated Core Commander"},
            "Collect Cytoplasm": {"Defeated Core Commander"},
            "Collect Relucite Ore": {"Defeated Nimruza"},
            "Collect Corrupted Alloy": {"Defeated Nimruza"},
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name, required in requirements.items():
            if location_name in present:
                set_rule(
                    world.get_location(location_name),
                    lambda state, required=required: state.has_all(required, world.player),
                )
    if world.options.refined_materials:
        boss_requirements = {
            "Collect Scarlet Bar": {"Wall Lowered"},
            "Collect Octarine Bar": {"Defeated Azeos"},
            "Collect Galaxite Bar": {"Defeated Omoroth"},
            "Collect Solarite Bar": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
            "Collect Coral Wood Plank": {"Defeated Azeos"},
            "Collect Gleam Wood Plank": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
            "Collect Pandorium Bar": {"Defeated Core Commander"},
            "Collect Relucite Bar": {"Defeated Nimruza"},
        }
        furnace_stages = {
            "Collect Copper Bar": 1, "Collect Tin Bar": 1, "Collect Iron Bar": 1,
            "Collect Gold Bar": 2, "Collect Scarlet Bar": 2, "Collect Octarine Bar": 2,
            "Collect Galaxite Bar": 3, "Collect Solarite Bar": 3,
            "Collect Pandorium Bar": 3, "Collect Relucite Bar": 3,
        }
        table_saw_checks = {"Collect Plank", "Collect Coral Wood Plank", "Collect Gleam Wood Plank"}
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name in present & set(furnace_stages):
            required = boss_requirements.get(location_name, set())
            stage = furnace_stages[location_name]
            set_rule(
                world.get_location(location_name),
                lambda state, required=required, stage=stage: (
                    state.has_all(required, world.player)
                    and (_legacy_license_mode(world.options) < 2
                         or state.has("Progressive Furnace License", world.player, stage))
                ),
            )
        for location_name in present & table_saw_checks:
            required = boss_requirements.get(location_name, set())
            set_rule(
                world.get_location(location_name),
                lambda state, required=required: (
                    state.has_all(required, world.player)
                    and (_legacy_license_mode(world.options) < 3
                         or state.has("Table Saw License", world.player))
                ),
            )
        if "Collect Glass Piece" in present:
            set_rule(
                world.get_location("Collect Glass Piece"),
                lambda state: (_legacy_license_mode(world.options) < 3
                               or state.has("Glass Smelter License", world.player)),
            )
    if world.options.unique_materials:
        requirements = {
            "Collect Chipped Blade": {"Wall Lowered"},
            "Collect Clear Gemstone": {"Wall Lowered"},
            "Collect Shutdown Protocol": {"Defeated Azeos"},
            "Collect Anomaly Report": {"Defeated Azeos"},
            "Collect Overwrite Transcript": {"Defeated Azeos"},
            "Collect Channeling Gemstone": {"Defeated Azeos"},
            "Collect Fractured Limbs": {"Defeated Azeos"},
            "Collect Energy String": {"Defeated Azeos"},
            "Collect Crystal Meteor Shard": {"Defeated Druidra", "Defeated Crydra", "Defeated Pyrdra"},
            "Collect Pink Hydra Eye": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
            "Collect Coiled Branch": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
            "Collect White Hydra Eye": {"Defeated Druidra"},
            "Collect Frozen Orb": {"Defeated Druidra"},
            "Collect Magma Rod": {"Defeated Crydra"},
            "Collect Oblivion Fragment": {"Defeated Nimruza"},
            "Collect Void-Forged Barrel": {"Defeated Nimruza"},
            "Collect Sanctified Firing Core": {"Defeated Nimruza"},
            "Collect S.A.H.A.B.A.R's Mortar Housing": {"Defeated S.A.H.A.B.A.R"},
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name, required in requirements.items():
            if location_name in present:
                set_rule(
                    world.get_location(location_name),
                    lambda state, required=required: state.has_all(required, world.player),
                )
    if world.options.locked_chests:
        key_checks = {
            "Collect Copper Key": (set(), 1),
            "Collect Iron Key": (set(), 1),
            "Collect Scarlet Key": ({"Wall Lowered"}, 2),
            "Collect Octarine Key": ({"Defeated Azeos"}, 2),
            "Collect Galaxite Key": ({"Defeated Omoroth"}, 3),
            "Collect Solarite Key": ({"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"}, 3),
            "Collect Relucite Key": ({"Defeated Nimruza"}, 3),
        }
        chest_checks = {
            "Unlock Locked Copper Chest": (set(), 1),
            "Unlock Locked Iron Chest": (set(), 1),
            "Unlock Locked Scarlet Chest": ({"Wall Lowered"}, 2),
            "Unlock Locked Octarine Chest": ({"Defeated Azeos"}, 2),
            "Unlock Locked Galaxite Chest": ({"Defeated Omoroth"}, 3),
            "Unlock Locked Solarite Chest": ({"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"}, 3),
            "Unlock Locked Relucite Chest": ({"Defeated Nimruza"}, 3),
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name, (required, stage) in key_checks.items():
            if location_name in present:
                set_rule(
                    world.get_location(location_name),
                    lambda state, required=required, stage=stage: (
                        state.has_all(required, world.player)
                        and (_legacy_license_mode(world.options) < 2 or (
                            state.has("Key Casting Table License", world.player)
                            and state.has("Progressive Furnace License", world.player, stage)
                        ))
                    ),
                )
        for location_name, (required, stage) in chest_checks.items():
            if location_name in present:
                set_rule(
                    world.get_location(location_name),
                    lambda state, required=required, stage=stage: (
                        state.has_all(required, world.player)
                        and (_legacy_license_mode(world.options) < 2 or (
                            state.has("Key Casting Table License", world.player)
                            and state.has("Progressive Furnace License", world.player, stage)
                        ))
                    ),
                )
    if world.options.key_items:
        requirements = {
            "Collect Stolen Crystal Heart": {"Defeated Glurch"},
            "Collect Admin Key": {"Defeated Azeos", "Defeated Ghorm"},
            "Collect Azeos Feather Fan": {"Wall Lowered"},
            "Collect Omoroth Compass": {"Defeated Azeos"},
            "Collect Ra-Akar Automaton": {"Defeated Omoroth"},
            "Collect Brood Void Neuron": {"Defeated Core Commander"},
            "Collect Herald Void Neuron": {"Defeated Nimruza"},
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name, required in requirements.items():
            if location_name in present:
                set_rule(
                    world.get_location(location_name),
                    lambda state, required=required: state.has_all(required, world.player),
                )
    if world.options.seeds:
        requirements = {
            "Collect Puffungi Seed": {"Wall Lowered"},
            "Collect Coral Wood Seed": {"Defeated Azeos"},
            "Collect Bloat Oat Seed": {"Wall Lowered"},
            "Collect Pewpaya Seed": {"Defeated Azeos"},
            "Collect Pinegrapple Seed": {"Defeated Azeos"},
            "Collect Sunrice Seed": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
            "Collect Lunacorn Seed": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
            "Collect Gleam Wood Seed": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name, required in requirements.items():
            if location_name in present:
                set_rule(
                    world.get_location(location_name),
                    lambda state, required=required: state.has_all(required, world.player),
                )
    if world.options.food:
        requirements = {
            "Collect Carrock": {"Wall Lowered"},
            "Collect Puffungi": {"Wall Lowered"},
            "Collect Bloat Oat": {"Wall Lowered"},
            "Collect Pewpaya": {"Defeated Azeos"},
            "Collect Pinegrapple": {"Defeated Azeos"},
            "Collect Sunrice": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
            "Collect Lunacorn": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
            "Collect Dodo Egg": {"Wall Lowered"},
            "Collect Atlantean Worm Heart": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
            "Collect Paradise Fruit Basket": {"Wall Lowered"},
            "Collect Splendid Amalgam": {"Defeated Omoroth"},
            "Collect Glowing Mushroom": {"Defeated Core Commander"},
            "Collect Oblidra's Heart": {"Defeated Core Commander"},
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name, required in requirements.items():
            if location_name in present:
                set_rule(
                    world.get_location(location_name),
                    lambda state, required=required: state.has_all(required, world.player),
                )
    if world.options.goldensanity:
        requirements = {
            "Collect Golden Puffungi": {"Wall Lowered"},
            "Collect Golden Bloat Oat": {"Wall Lowered"},
            "Collect Golden Pewpaya": {"Defeated Azeos"},
            "Collect Golden Pinegrapple": {"Defeated Azeos"},
            "Collect Golden Glow Tulip": {"Defeated Omoroth"},
            "Collect Golden Sunrice": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
            "Collect Golden Lunacorn": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name, required in requirements.items():
            if location_name in present:
                set_rule(
                    world.get_location(location_name),
                    lambda state, required=required: state.has_all(required, world.player),
                )
    if world.options.cardsanity:
        requirements = {
            'Collect Oracle Card "Entity"': {"Defeated Glurch"},
            'Collect Oracle Card "Wisdom"': {"Defeated Azeos"},
            'Collect Oracle Card "Metropolis"': {"Defeated Azeos"},
            'Collect Oracle Card "Inspiration"': {"Defeated Azeos"},
            'Collect Oracle Card "Radiance"': {"Defeated Omoroth"},
            'Collect Oracle Card "Temperance"': {"Defeated Omoroth"},
            'Collect Oracle Card "Endurance"': {"Defeated Omoroth"},
            "Collect Oracle Deck": {"Defeated Omoroth"},
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name, required in requirements.items():
            if location_name in present:
                set_rule(
                    world.get_location(location_name),
                    lambda state, required=required: state.has_all(required, world.player),
                )
    if world.options.blocksanity:
        requirements = {
            "Collect Grass Block": {"Wall Lowered"},
            "Collect Mold Block": {"Wall Lowered"},
            "Collect Beach Block": {"Defeated Azeos"},
            "Collect Metropolis Block": {"Defeated Azeos"},
            "Collect Desert Block": {"Defeated Omoroth"},
            "Collect Desert Temple Block": {"Defeated Omoroth"},
            "Collect Maze Block": {"Defeated Omoroth"},
            "Collect Lava Rock Block": {"Defeated Omoroth"},
            "Collect Oasis Block": {"Defeated Omoroth"},
            "Collect Crystal Block": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
            "Collect Alien Tech Block": {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"},
            "Collect Fossil Block": {"Defeated Core Commander"},
            "Collect Excavation Block": {"Defeated Nimruza"},
            "Collect Industrial Block": {"Defeated Nimruza"},
            "Collect Tuff Block": {"Defeated Nimruza"},
            "Collect Void Infused Tuff Block": {"Defeated Nimruza"},
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name, required in requirements.items():
            if location_name in present:
                set_rule(
                    world.get_location(location_name),
                    lambda state, required=required: state.has_all(required, world.player),
                )
    if world.options.fishsanity:
        fish_stages = {}
        for name in ("Dagger Fin", "Pink Palace Fish", "Teal Palace Fish", "Crown Squid"):
            fish_stages[f"Collect {name}"] = (set(), 3, 1)
        for name in ("Yellow Blister Head", "Green Blister Head", "Devil Worm", "Vampire Eel"):
            fish_stages[f"Collect {name}"] = (set(), 2, 1)
        for name in ("Mold Shark", "Rot Fish", "Black Steel Urchin", "Azure Feather Fish",
                     "Emerald Feather Fish", "Spirit Veil", "Astral Jelly"):
            fish_stages[f"Collect {name}"] = ({"Wall Lowered"}, 4, 2)
        for name in ("Bottom Tracer", "Silver Dart", "Golden Dart", "Pink Coralotl", "White Coralotl"):
            fish_stages[f"Collect {name}"] = ({"Defeated Azeos"}, 5, 2)
        for name in ("Solid Spikeback", "Sandy Spikeback", "Gray Dune Tail", "Brown Dune Tail",
                     "Tornis Kingfish"):
            fish_stages[f"Collect {name}"] = ({"Defeated Omoroth"}, 5, 2)
        for name in ("Dark Lava Eater", "Bright Lava Eater", "Verdant Dragonfish",
                     "Elder Dragonfish", "Starlight Nautilus"):
            fish_stages[f"Collect {name}"] = ({"Defeated Omoroth"}, 6, 3)
        for name in ("Beryll Angle Fish", "Glistening Deepstalker", "Cosmic Form",
                     "Jasper Angle Fish", "Splendid Deepstalker"):
            fish_stages[f"Collect {name}"] = (
                {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"}, 6, 3)
        for name in ("Terra Trilobite", "Litho Trilobite", "Greenhorn Pico", "Pinkhorn Pico",
                     "Riftian Lampfish"):
            fish_stages[f"Collect {name}"] = ({"Defeated Core Commander"}, 7, 3)
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name in present & set(fish_stages):
            required, workbench_stage, furnace_stage = fish_stages[location_name]
            set_rule(
                world.get_location(location_name),
                lambda state, required=required, workbench_stage=workbench_stage,
                furnace_stage=furnace_stage: (
                    state.has_all(required, world.player)
                    and (_legacy_license_mode(world.options) < 2 or (
                        state.has("Progressive Workbench License", world.player, workbench_stage)
                        and state.has("Progressive Furnace License", world.player, furnace_stage)
                    ))
                ),
            )
    if world.options.figurinesanity:
        milestone_items = {
            "lower_wall": "Wall Lowered",
            "defeat_glurch": "Defeated Glurch",
            "defeat_azeos": "Defeated Azeos",
            "defeat_omoroth": "Defeated Omoroth",
            "defeat_ra_akar": "Defeated Ra-Akar",
            "defeat_druidra": "Defeated Druidra",
            "defeat_crydra": "Defeated Crydra",
            "defeat_pyrdra": "Defeated Pyrdra",
            "defeat_core_commander": "Defeated Core Commander",
            "defeat_nimruza": "Defeated Nimruza",
        }
        hologram_checks = {
            "Collect Hive Larva Figurine", "Collect Big Hive Larva Figurine",
            "Collect Hive Mother Figurine", "Collect Ivy Figurine", "Collect Morpha Figurine",
            "Collect Igneous Figurine",
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name in present:
            metadata = LOCATION_METADATA.get(location_name)
            if metadata is None or metadata[0] != "figurinesanity":
                continue
            required = {
                milestone_items[key] for key in metadata[2]
            }
            set_rule(
                world.get_location(location_name),
                lambda state, location_name=location_name, required=required: (
                    state.has_all(required, world.player)
                    and (_legacy_license_mode(world.options) < 2 or (
                        (location_name not in hologram_checks
                         or state.has("Ancient Hologram Pod License", world.player))
                        and (location_name != "Collect Azeos Figurine"
                             or state.has("Progressive Furnace License", world.player, 2))
                        and (location_name != "Collect Omoroth Figurine" or (
                            state.has("Progressive Workbench License", world.player, 5)
                            and state.has("Progressive Furnace License", world.player, 2)
                            and state.has("Fishing Workbench License", world.player)
                        ))
                        and (location_name != "Collect Ra-Akar Figurine" or (
                            state.has("Progressive Furnace License", world.player, 3)
                            and state.has("Table Saw License", world.player)
                        ))
                        and (location_name != "Collect Nimruza Figurine"
                             or state.has("Progressive Furnace License", world.player, 3))
                    ))
                ),
            )
    if world.options.valuablesanity:
        milestone_items = {
            "lower_wall": "Wall Lowered",
            "defeat_glurch": "Defeated Glurch",
            "defeat_azeos": "Defeated Azeos",
            "defeat_omoroth": "Defeated Omoroth",
            "defeat_ra_akar": "Defeated Ra-Akar",
            "defeat_nimruza": "Defeated Nimruza",
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name in present:
            metadata = LOCATION_METADATA.get(location_name)
            if metadata is None or metadata[0] != "valuablesanity":
                continue
            required = {milestone_items[key] for key in metadata[2]}
            set_rule(
                world.get_location(location_name),
                lambda state, required=required: state.has_all(required, world.player),
            )
    if world.options.toolsanity:
        milestone_items = {
            "lower_wall": "Wall Lowered",
            "defeat_azeos": "Defeated Azeos",
            "defeat_omoroth": "Defeated Omoroth",
            "defeat_ra_akar": "Defeated Ra-Akar",
        }
        license_stages = {
            "Collect Copper Pickaxe": (1, 1, False),
            "Collect Tin Pickaxe": (2, 1, False),
            "Collect Iron Pickaxe": (3, 2, False),
            "Collect Scarlet Pickaxe": (4, 2, False),
            "Collect Octarine Pickaxe": (5, 2, False),
            "Collect Galaxite Pickaxe": (6, 3, True),
            "Collect Solarite Pickaxe": (7, 3, False),
            "Collect Copper Shovel": (0, 1, False),
            "Collect Tin Shovel": (2, 1, False),
            "Collect Iron Shovel": (3, 2, False),
            "Collect Scarlet Shovel": (4, 2, False),
            "Collect Octarine Shovel": (5, 2, False),
            "Collect Galaxite Shovel": (6, 3, True),
            "Collect Watering Can": (0, 1, False),
            "Collect Copper Hoe": (1, 1, False),
            "Collect Tin Hoe": (2, 1, False),
            "Collect Iron Hoe": (3, 2, False),
            "Collect Large Watering Can": (3, 1, False),
            "Collect Scarlet Hoe": (4, 2, False),
            "Collect Octarine Garden Trowel": (5, 2, False),
            "Collect Wood Fishing Rod": (1, 0, False),
            "Collect Tin Fishing Rod": (2, 1, False),
            "Collect Iron Fishing Rod": (3, 2, False),
            "Collect Scarlet Fishing Rod": (4, 2, False),
            "Collect Octarine Fishing Rod": (5, 2, False),
            "Collect Galaxite Fishing Rod": (6, 3, True),
            "Collect Solarite Fishing Rod": (7, 3, True),
            "Collect Bug Net": (2, 0, False),
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name in present:
            metadata = LOCATION_METADATA.get(location_name)
            if metadata is None or metadata[0] != "toolsanity":
                continue
            required = {milestone_items[key] for key in metadata[2]}
            workbench_stage, furnace_stage, table_saw = license_stages.get(
                location_name, (0, 0, False))
            set_rule(
                world.get_location(location_name),
                lambda state, required=required, workbench_stage=workbench_stage,
                furnace_stage=furnace_stage, table_saw=table_saw: (
                    state.has_all(required, world.player)
                    and (_legacy_license_mode(world.options) < 2 or (
                        (not workbench_stage or state.has(
                            "Progressive Workbench License", world.player, workbench_stage))
                        and (not furnace_stage or state.has(
                            "Progressive Furnace License", world.player, furnace_stage))
                        and (not table_saw or state.has("Table Saw License", world.player))
                    ))
                ),
            )
    if world.options.weaponsanity:
        milestone_items = {
            "lower_wall": "Wall Lowered",
            "defeat_azeos": "Defeated Azeos",
            "defeat_omoroth": "Defeated Omoroth",
            "defeat_ra_akar": "Defeated Ra-Akar",
            "defeat_druidra": "Defeated Druidra",
            "defeat_crydra": "Defeated Crydra",
            "defeat_pyrdra": "Defeated Pyrdra",
            "defeat_core_commander": "Defeated Core Commander",
            "defeat_nimruza": "Defeated Nimruza",
        }
        license_stages = {
            "Collect Copper Sword": (1, 1, False, False, 0),
            "Collect Tin Sword": (2, 1, False, False, 0),
            "Collect Slime Sword": (0, 1, True, False, 0),
            "Collect Iron Sword": (3, 2, False, False, 0),
            "Collect Tin Dagger": (2, 1, False, False, 0),
            "Collect Ritual Dagger": (0, 1, False, False, 0),
            "Collect Tin Axe": (2, 1, False, False, 0),
            "Collect Iron Halberd": (3, 2, False, False, 0),
            "Collect Larva Spike Club": (0, 1, False, False, 0),
            "Collect Wood Bow": (1, 0, False, False, 0),
            "Collect Iron Bow": (3, 2, False, False, 0),
            "Collect Slingshot": (2, 1, False, False, 0),
            "Collect Grubzooka": (0, 1, False, False, 0),
            "Collect Scarlet Sword": (4, 2, False, False, 0),
            "Collect Scarlet Dagger": (4, 2, False, False, 0),
            "Collect Scarlet Crossbow": (4, 2, False, False, 0),
            "Collect Octarine Sword": (5, 2, False, False, 0),
            "Collect Octarine Axe": (5, 2, False, False, 0),
            "Collect Octarine Bow": (5, 2, False, False, 0),
            "Collect Galaxite Sword": (6, 3, False, False, 0),
            "Collect Galaxite Dagger": (6, 3, False, False, 0),
            "Collect Galaxite Chakram": (6, 3, False, False, 0),
            "Collect Solarite Sword": (7, 3, False, False, 0),
            "Collect Solarite Crossbow": (7, 3, False, False, 0),
            "Collect Pandorium Axe": (0, 3, False, True, 0),
            "Collect Chaos Staff": (0, 3, False, True, 0),
            "Collect Scrap Minigun": (0, 0, False, False, 2),
            "Collect Flamethrower": (0, 0, False, False, 2),
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name in present:
            metadata = LOCATION_METADATA.get(location_name)
            if metadata is None or metadata[0] != "weaponsanity":
                continue
            required = {milestone_items[key] for key in metadata[2]}
            anvil_stage, furnace_stage, distillery, rift_statue, smithing_stage = (
                license_stages.get(location_name, (0, 0, False, False, 0)))
            set_rule(
                world.get_location(location_name),
                lambda state, required=required, anvil_stage=anvil_stage,
                furnace_stage=furnace_stage, distillery=distillery,
                rift_statue=rift_statue, smithing_stage=smithing_stage: (
                    state.has_all(required, world.player)
                    and (_legacy_license_mode(world.options) < 2 or (
                        (not anvil_stage or state.has(
                            "Progressive Anvil License", world.player, anvil_stage))
                        and (not furnace_stage or state.has(
                            "Progressive Furnace License", world.player, furnace_stage))
                        and (not distillery or state.has("Distillery Table License", world.player))
                        and (not rift_statue or state.has("Rift Statue License", world.player))
                        and (not smithing_stage or state.has(
                            "Progressive Smithing Table License", world.player, smithing_stage))
                    ))
                ),
            )
    if world.options.accessanity:
        milestone_items = {
            "lower_wall": "Wall Lowered", "defeat_glurch": "Defeated Glurch",
            "defeat_azeos": "Defeated Azeos", "defeat_omoroth": "Defeated Omoroth",
            "defeat_ra_akar": "Defeated Ra-Akar", "defeat_druidra": "Defeated Druidra",
            "defeat_crydra": "Defeated Crydra", "defeat_pyrdra": "Defeated Pyrdra",
            "defeat_nimruza": "Defeated Nimruza",
        }
        license_stages = {
            "Collect Small Backpack": (1, 1, 0, False, False, False),
            "Collect Explorer Backpack": (2, 1, 0, False, False, False),
            "Collect Small Ore and Block Pouch": (0, 1, 0, True, False, False),
            "Collect Medium Ore and Block Pouch": (0, 2, 0, True, False, False),
            "Collect Small Seed and Crop Pouch": (0, 1, 0, True, False, False),
            "Collect Medium Seed and Crop Pouch": (0, 2, 0, True, False, False),
            "Collect Small Fish Pouch": (0, 1, 0, True, False, False),
            "Collect Medium Fish Pouch": (0, 2, 0, True, False, False),
            "Collect Small Valuable Pouch": (0, 1, 0, True, False, False),
            "Collect Medium Valuable Pouch": (0, 2, 0, True, False, False),
            "Collect Potion Pouch": (0, 1, 0, True, False, False),
            "Collect Medium Potion Pouch": (0, 2, 0, True, False, False),
            "Collect Large Potion Pouch": (0, 0, 0, True, False, False),
            "Collect Critter Pouch": (0, 1, 0, True, False, False),
            "Collect Medium Critter Pouch": (0, 2, 0, True, False, False),
            "Collect Large Critter Pouch": (0, 0, 0, True, False, False),
            "Collect Small Lantern": (1, 1, 0, False, True, False),
            "Collect Orb Lantern": (4, 2, 0, False, True, False),
            "Collect Pearl Lantern": (5, 2, 0, False, True, False),
            "Collect Wooden Shield": (0, 1, 1, False, False, False),
            "Collect Iron Shield": (0, 2, 3, False, False, False),
            "Collect Octarine Shield": (0, 2, 5, False, False, False),
            "Collect Scarlet Shell Backpack": (4, 2, 0, False, False, False),
            "Collect Octarine Backpack": (5, 2, 0, False, False, False),
            "Collect Morpha's Bubble Backpack": (0, 0, 0, False, False, True),
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name in present:
            metadata = LOCATION_METADATA.get(location_name)
            if metadata is None or metadata[0] != "accessanity":
                continue
            required = {milestone_items[key] for key in metadata[2]}
            workbench, furnace, anvil, pouch, distillery, hologram = license_stages.get(
                location_name, (0, 0, 0, False, False, False))
            set_rule(
                world.get_location(location_name),
                lambda state, required=required, workbench=workbench, furnace=furnace,
                anvil=anvil, pouch=pouch, distillery=distillery, hologram=hologram: (
                    state.has_all(required, world.player)
                    and (_legacy_license_mode(world.options) < 2 or (
                        (not workbench or state.has("Progressive Workbench License", world.player, workbench))
                        and (not furnace or state.has("Progressive Furnace License", world.player, furnace))
                        and (not anvil or state.has("Progressive Anvil License", world.player, anvil))
                        and (not pouch or state.has("Pouch Workbench License", world.player))
                        and (not distillery or state.has("Distillery Table License", world.player))
                        and (not hologram or state.has("Ancient Hologram Pod License", world.player))
                    ))
                ),
            )
    if world.options.jewelrysanity:
        milestone_items = {
            "lower_wall": "Wall Lowered", "defeat_glurch": "Defeated Glurch",
            "defeat_azeos": "Defeated Azeos", "defeat_omoroth": "Defeated Omoroth",
            "defeat_ra_akar": "Defeated Ra-Akar", "defeat_druidra": "Defeated Druidra",
            "defeat_crydra": "Defeated Crydra", "defeat_nimruza": "Defeated Nimruza",
        }
        license_stages = {
            "Collect Copper Cross Necklace": (1, 1),
            "Collect Iron Chunk Necklace": (1, 1),
            "Collect Gold Crystal Necklace": (2, 1),
            "Collect Scarlet Chunk Necklace": (2, 2),
            "Collect Octarine Necklace": (2, 2),
            "Collect Coral Amulet": (0, 2),
            "Collect Glow Tulip Ring": (1, 1),
            "Collect Swift Ring": (1, 1),
            "Collect Gold Crystal Ring": (2, 1),
            "Collect Magnetic Ring": (1, 2),
            "Collect Golden Spike Ring": (2, 2),
            "Collect Octarine Ring": (2, 2),
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name in present:
            metadata = LOCATION_METADATA.get(location_name)
            if metadata is None or metadata[0] != "jewelrysanity":
                continue
            required = {milestone_items[key] for key in metadata[2]}
            furnace, jewelry = license_stages.get(location_name, (0, 0))
            set_rule(
                world.get_location(location_name),
                lambda state, required=required, furnace=furnace, jewelry=jewelry: (
                    state.has_all(required, world.player)
                    and (_legacy_license_mode(world.options) < 2 or (
                        (not furnace or state.has(
                            "Progressive Furnace License", world.player, furnace))
                        and (not jewelry or state.has(
                            "Progressive Jewelry Workbench License", world.player, jewelry))
                    ))
                ),
            )
    if world.options.armorsanity:
        milestone_items = {
            "lower_wall": "Wall Lowered", "defeat_glurch": "Defeated Glurch",
            "defeat_azeos": "Defeated Azeos", "defeat_omoroth": "Defeated Omoroth",
            "defeat_ra_akar": "Defeated Ra-Akar", "defeat_druidra": "Defeated Druidra",
            "defeat_crydra": "Defeated Crydra", "defeat_pyrdra": "Defeated Pyrdra",
            "defeat_core_commander": "Defeated Core Commander",
            "defeat_nimruza": "Defeated Nimruza",
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name in present:
            metadata = LOCATION_METADATA.get(location_name)
            if metadata is None or metadata[0] != "armorsanity":
                continue
            requirements = metadata[2]
            required = {
                milestone_items[key] for key in requirements if key in milestone_items
            }
            anvil = requirements.count("progressive_anvil_license")
            furnace = requirements.count("progressive_furnace_license")
            smithing = requirements.count("progressive_smithing_table_license")
            distillery = "distillery_table_license" in requirements
            rift_statue = "rift_statue_license" in requirements
            set_rule(
                world.get_location(location_name),
                lambda state, required=required, anvil=anvil, furnace=furnace,
                smithing=smithing, distillery=distillery, rift_statue=rift_statue: (
                    state.has_all(required, world.player)
                    and (_legacy_license_mode(world.options) < 2 or (
                        (not anvil or state.has("Progressive Anvil License", world.player, anvil))
                        and (not furnace or state.has("Progressive Furnace License", world.player, furnace))
                        and (not smithing or state.has(
                            "Progressive Smithing Table License", world.player, smithing))
                        and (not distillery or state.has("Distillery Table License", world.player))
                        and (not rift_statue or state.has("Rift Statue License", world.player))
                    ))
                ),
            )
    if world.options.petsanity:
        milestone_items = {
            "lower_wall": "Wall Lowered",
            "defeat_glurch": "Defeated Glurch",
            "defeat_core_commander": "Defeated Core Commander",
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name in present:
            metadata = LOCATION_METADATA.get(location_name)
            if metadata is None or metadata[0] != "petsanity":
                continue
            requirements = metadata[2]
            required = {
                milestone_items[key] for key in requirements if key in milestone_items
            }
            incubator = "egg_incubator_license" in requirements
            hologram = "ancient_hologram_pod_license" in requirements
            set_rule(
                world.get_location(location_name),
                lambda state, required=required, incubator=incubator, hologram=hologram: (
                    state.has_all(required, world.player)
                    and (_legacy_license_mode(world.options) < 2 or (
                        (not incubator or state.has("Egg Incubator License", world.player))
                        and (not hologram or state.has("Ancient Hologram Pod License", world.player))
                    ))
                ),
            )
    if world.options.merchantsanity:
        milestone_items = {
            "defeat_glurch": "Defeated Glurch", "defeat_ghorm": "Defeated Ghorm",
            "defeat_azeos": "Defeated Azeos", "defeat_omoroth": "Defeated Omoroth",
            "defeat_ra_akar": "Defeated Ra-Akar", "defeat_sahabar": "Defeated S.A.H.A.B.A.R",
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name in present:
            metadata = LOCATION_METADATA.get(location_name)
            if metadata is None or metadata[0] != "merchantsanity":
                continue
            required = {milestone_items[key] for key in metadata[2] if key in milestone_items}
            set_rule(
                world.get_location(location_name),
                lambda state, required=required: state.has_all(required, world.player),
            )
    if world.options.enemies or world.options.cattle_mutilation:
        milestone_items = {
            "lower_wall": "Wall Lowered",
            "defeat_azeos": "Defeated Azeos",
            "defeat_omoroth": "Defeated Omoroth",
            "defeat_ra_akar": "Defeated Ra-Akar",
            "defeat_druidra": "Defeated Druidra",
            "defeat_crydra": "Defeated Crydra",
            "defeat_pyrdra": "Defeated Pyrdra",
            "defeat_core_commander": "Defeated Core Commander",
            "defeat_nimruza": "Defeated Nimruza",
            "defeat_sahabar": "Defeated S.A.H.A.B.A.R",
        }
        present = {location.name for location in world.multiworld.get_locations(world.player)}
        for location_name in present:
            metadata = LOCATION_METADATA.get(location_name)
            if metadata is None or metadata[0] not in {"enemies", "cattle_mutilation"}:
                continue
            required = {
                milestone_items[key] for key in metadata[2] if key in milestone_items
            }
            set_rule(
                world.get_location(location_name),
                lambda state, required=required: state.has_all(required, world.player),
            )
    # LOCATION_METADATA is generated from the corrected logic catalog and is
    # authoritative.  Older group-specific rules above are retained as useful
    # documentation, but must not leave stale gates (or omit newly corrected
    # ones) after the catalog changes.  Repeated progressive tokens represent
    # the exact license stage required by Archipelago fill.
    milestone_items = {
        "lower_wall": "Wall Lowered",
        "defeat_glurch": "Defeated Glurch",
        "defeat_ghorm": "Defeated Ghorm",
        "defeat_azeos": "Defeated Azeos",
        "defeat_omoroth": "Defeated Omoroth",
        "defeat_ra_akar": "Defeated Ra-Akar",
        "defeat_druidra": "Defeated Druidra",
        "defeat_crydra": "Defeated Crydra",
        "defeat_pyrdra": "Defeated Pyrdra",
        "defeat_core_commander": "Defeated Core Commander",
        "defeat_nimruza": "Defeated Nimruza",
        "defeat_sahabar": "Defeated S.A.H.A.B.A.R",
    }
    license_items = {
        "progressive_workbench_license": "Progressive Workbench License",
        "progressive_anvil_license": "Progressive Anvil License",
        "progressive_furnace_license": "Progressive Furnace License",
        "ancient_hologram_pod_license": "Ancient Hologram Pod License",
        "egg_incubator_license": "Egg Incubator License",
        "fishing_workbench_license": "Fishing Workbench License",
        "key_casting_table_license": "Key Casting Table License",
        "distillery_table_license": "Distillery Table License",
        "glass_smelter_license": "Glass Smelter License",
        "progressive_smithing_table_license": "Progressive Smithing Table License",
        "rift_statue_license": "Rift Statue License",
        "table_saw_license": "Table Saw License",
    }
    for location in world.multiworld.get_locations(world.player):
        metadata = LOCATION_METADATA.get(location.name)
        if metadata is None:
            continue
        counts = Counter(metadata[2])
        milestones = {
            milestone_items[token] for token in counts if token in milestone_items
        }
        licenses = {
            item_name: counts[token]
            for token, item_name in license_items.items()
            if counts[token]
            and getattr(world.options, LICENSE_OPTION_BY_ITEM[item_name])
        }
        set_rule(
            location,
            lambda state, milestones=milestones, licenses=licenses: (
                state.has_all(milestones, world.player)
                and all(state.has(item, world.player, count)
                        for item, count in licenses.items())
            ),
        )

    if world.options.early_repair_and_salvage and world.options.repair_salvage_license:
        sphere_one_milestones = {
            "defeat_glurch", "defeat_ghorm", "defeat_malugaz",
            "defeat_hive_mother", "defeat_king_slime",
        }
        for location in world.multiworld.get_locations(world.player):
            metadata = LOCATION_METADATA.get(location.name)
            if metadata is None or not set(metadata[2]).issubset(sphere_one_milestones):
                add_item_rule(
                    location,
                    lambda item: item.name not in {
                        "Salvage and Repair Station License",
                        "Progressive Furnace License",
                    },
                )
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
