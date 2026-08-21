from BaseClasses import Region
from worlds.generic.Rules import set_rule

from .locations import CoreKeeperLocation, LOCATION_METADATA, LOCATION_NAME_TO_ID

SANITY_GROUPS = {
    "skillsanity", "fishsanity", "figurinesanity", "cardsanity", "valuablesanity",
    "toolsanity", "weaponsanity", "jewelrysanity", "accessanity",
    "armorsanity",
}

OPTIONAL_GROUPS = {
    "unique_materials", "key_items", "bosses", "merchantsanity", "petsanity",
    "blocksanity", "goldensanity", "critters", "cattle_mutilation",
}


def _boss_region(world, name: str, location_name: str, event_name: str) -> Region:
    region = Region(name, world.player, world.multiworld)
    region.add_locations({location_name: LOCATION_NAME_TO_ID[location_name]}, CoreKeeperLocation)
    if world.options.prevent_priority_in_optional_checks:
        location = region.locations[0]
        original_rule = location.item_rule
        location.item_rule = (
            lambda item, original_rule=original_rule:
            original_rule(item) and not item.advancement
        )
    region.add_event(event_name, event_name)
    return region


def _has_boss_slot_licenses(
    state,
    world,
    *,
    workbench: int = 0,
    furnace: int = 0,
    hologram: bool = False,
    fishing_workbench: bool = False,
    table_saw: bool = False,
) -> bool:
    """Return whether the destination boss slot's hard crafting gates are met."""
    player = world.player
    return (
        (not world.options.workbench_license or not workbench
         or state.has("Progressive Workbench License", player, workbench))
        and (not world.options.furnace_license or not furnace
             or state.has("Progressive Furnace License", player, furnace))
        and (not world.options.hologram_license or not hologram
             or state.has("Ancient Hologram Pod License", player))
        and (not world.options.fishing_workbench_license or not fishing_workbench
             or state.has("Fishing Workbench License", player))
        and (not world.options.table_saw_license or not table_saw
             or state.has("Table Saw License", player))
    )


def create_regions(world) -> None:
    menu = Region("Menu", world.player, world.multiworld)
    dirt = Region("Dirt Biome", world.player, world.multiworld)
    glurch = _boss_region(world, "Glurch Arena", "Defeat Glurch the Abominous Mass", "Defeated Glurch")
    ghorm = _boss_region(world, "Ghorm Arena", "Defeat Ghorm the Devourer", "Defeated Ghorm")
    malugaz = _boss_region(world, "Malugaz Arena", "Defeat Malugaz the Corrupted", "Defeated Malugaz")
    optional_bosses = bool(world.options.bosses) or int(world.options.goal) == 0
    if optional_bosses:
        hive_mother = _boss_region(world, "Hive Mother Arena", "Defeat The Hive Mother", "Defeated Hive Mother")
        king_slime = _boss_region(world, "King Slime Arena", "Defeat King Slime", "Defeated King Slime")
    wall = Region("The Core", world.player, world.multiworld)
    wall.add_event("Wall Lowered", "Wall Lowered")

    enabled_locations: list[str] = []
    if world.options.raw_materials:
        enabled_locations.extend((
            "Collect Ancient Coin", "Collect Wood", "Collect Copper Ore", "Collect Tin Ore", "Collect Iron Ore",
            "Collect Gold Ore", "Collect Ancient Gemstone", "Collect Slime", "Collect Fiber",
            "Collect Wool", "Collect Strolly Poly Plate", "Collect Mechanical Part", "Collect Scrap Parts",
        ))
        if int(world.options.goal) != 3:
            enabled_locations.extend((
                "Collect Scarlet Ore", "Collect Octarine Ore", "Collect Galaxite Ore",
                "Collect Solarite Ore", "Collect Coral Wood", "Collect Gleam Wood",
                "Collect Jungle Emerald", "Collect Ocean Sapphire", "Collect Desert Ruby",
                "Collect Poison Slime", "Collect Slippery Slime", "Collect Magma Slime",
                "Collect Ancient Feather", "Collect Sea Shell", "Collect Scarab Wingcover",
                "Collect Blasting Dung",
            ))
        if int(world.options.goal) <= 1:
            enabled_locations.extend((
                "Collect Pandorium Ore", "Collect Relucite Ore", "Collect Calcified Shell",
                "Collect Cytoplasm", "Collect Corrupted Alloy",
            ))
    if world.options.refined_materials:
        enabled_locations.extend((
            "Collect Copper Bar", "Collect Tin Bar", "Collect Iron Bar", "Collect Gold Bar",
            "Collect Plank", "Collect Glass Piece",
        ))
        if int(world.options.goal) != 3:
            enabled_locations.extend((
                "Collect Scarlet Bar", "Collect Octarine Bar", "Collect Galaxite Bar",
                "Collect Solarite Bar", "Collect Coral Wood Plank", "Collect Gleam Wood Plank",
            ))
        if int(world.options.goal) <= 1:
            enabled_locations.extend(("Collect Pandorium Bar", "Collect Relucite Bar"))
    if world.options.unique_materials:
        enabled_locations.append("Collect Crystal Skull Shard")
        if int(world.options.goal) != 3:
            enabled_locations.extend((
                "Collect Chipped Blade", "Collect Clear Gemstone", "Collect Shutdown Protocol",
                "Collect Anomaly Report", "Collect Overwrite Transcript", "Collect Channeling Gemstone",
                "Collect Fractured Limbs", "Collect Energy String", "Collect Crystal Meteor Shard",
                "Collect Pink Hydra Eye", "Collect White Hydra Eye", "Collect Coiled Branch",
                "Collect Magma Rod", "Collect Frozen Orb",
            ))
        if int(world.options.goal) <= 1:
            enabled_locations.extend((
                "Collect Oblivion Fragment", "Collect Void-Forged Barrel",
                "Collect Sanctified Firing Core",
            ))
        if int(world.options.goal) == 0:
            enabled_locations.append("Collect S.A.H.A.B.A.R's Mortar Housing")
    if world.options.key_items:
        enabled_locations.extend(("Collect Ghorm's Horn", "Collect Glurch Eye", "Collect Stolen Crystal Heart"))
        if int(world.options.goal) != 3:
            enabled_locations.extend((
                "Collect Admin Key", "Collect Azeos Feather Fan",
                "Collect Omoroth Compass", "Collect Ra-Akar Automaton",
            ))
        if int(world.options.goal) <= 1:
            enabled_locations.extend(("Collect Brood Void Neuron", "Collect Herald Void Neuron"))
    if world.options.seeds:
        enabled_locations.extend((
            "Collect Heart Berry Seed", "Collect Glow Tulip Seed", "Collect Bomb Pepper Seed",
            "Collect Carrock Seed", "Collect Root Seed", "Collect Grub Kapok Seed",
        ))
        if int(world.options.goal) != 3:
            enabled_locations.extend((
                "Collect Puffungi Seed", "Collect Coral Wood Seed", "Collect Bloat Oat Seed",
                "Collect Pewpaya Seed", "Collect Pinegrapple Seed", "Collect Sunrice Seed",
                "Collect Lunacorn Seed", "Collect Gleam Wood Seed",
            ))
    if world.options.food:
        enabled_locations.extend((
            "Collect Mushroom", "Collect Giant Mushroom", "Collect Heart Berry",
            "Collect Glow Tulip", "Collect Bomb Pepper", "Collect Carrock", "Collect Larva Meat",
            "Collect Marbled Meat", "Collect Meadow Milk", "Collect Amber Larva",
        ))
        if int(world.options.goal) != 3:
            enabled_locations.extend((
                "Collect Puffungi", "Collect Bloat Oat",
                "Collect Pewpaya", "Collect Pinegrapple", "Collect Sunrice",
                "Collect Lunacorn", "Collect Dodo Egg", "Collect Atlantean Worm Heart",
                "Collect Paradise Fruit Basket", "Collect Splendid Amalgam",
            ))
        if int(world.options.goal) <= 1:
            enabled_locations.extend(("Collect Glowing Mushroom", "Collect Oblidra's Heart"))
    if world.options.goldensanity:
        enabled_locations.extend((
            "Collect Golden Heart Berry", "Collect Golden Bomb Pepper", "Collect Golden Carrock",
            "Collect Golden Glow Tulip", "Collect Shiny Larva Meat",
        ))
        if int(world.options.goal) != 3:
            enabled_locations.extend((
                "Collect Golden Puffungi", "Collect Golden Bloat Oat",
                "Collect Golden Pewpaya", "Collect Golden Pinegrapple",
                "Collect Golden Sunrice", "Collect Golden Lunacorn",
            ))
    if world.options.cardsanity:
        enabled_locations.extend((
            'Collect Oracle Card "Aura"', 'Collect Oracle Card "Entity"',
            'Collect Oracle Card "Brilliance"',
        ))
        if int(world.options.goal) != 3:
            enabled_locations.extend((
                'Collect Oracle Card "Wisdom"', 'Collect Oracle Card "Metropolis"',
                'Collect Oracle Card "Inspiration"', 'Collect Oracle Card "Radiance"',
                'Collect Oracle Card "Temperance"', 'Collect Oracle Card "Endurance"',
                "Collect Oracle Deck",
            ))
    if world.options.blocksanity:
        enabled_locations.extend((
            "Collect Dirt Block", "Collect Turf Block", "Collect Sand Block", "Collect Meadow Block",
            "Collect Clay Block", "Collect Larva Hive Block", "Collect Stone Block",
        ))
        if int(world.options.goal) != 3:
            enabled_locations.extend((
                "Collect Grass Block", "Collect Mold Block", "Collect Beach Block",
                "Collect Metropolis Block", "Collect Desert Block", "Collect Desert Temple Block",
                "Collect Maze Block", "Collect Lava Rock Block", "Collect Crystal Block",
                "Collect Alien Tech Block", "Collect Oasis Block",
            ))
        if int(world.options.goal) <= 1:
            enabled_locations.extend((
                "Collect Fossil Block", "Collect Excavation Block", "Collect Industrial Block",
                "Collect Tuff Block", "Collect Void Infused Tuff Block",
            ))
    if world.options.fishsanity:
        enabled_locations.extend((
            "Collect Orange Cave Guppy", "Collect Blue Cave Guppy", "Collect Rock Jaw",
            "Collect Gem Crab", "Collect Dagger Fin", "Collect Pink Palace Fish",
            "Collect Teal Palace Fish", "Collect Crown Squid", "Collect Yellow Blister Head",
            "Collect Green Blister Head", "Collect Devil Worm", "Collect Vampire Eel",
        ))
        if int(world.options.goal) != 3:
            enabled_locations.extend((
                "Collect Mold Shark", "Collect Rot Fish", "Collect Black Steel Urchin",
                "Collect Azure Feather Fish", "Collect Emerald Feather Fish", "Collect Spirit Veil",
                "Collect Astral Jelly", "Collect Bottom Tracer", "Collect Silver Dart",
                "Collect Golden Dart", "Collect Pink Coralotl", "Collect White Coralotl",
                "Collect Solid Spikeback", "Collect Sandy Spikeback", "Collect Gray Dune Tail",
                "Collect Brown Dune Tail", "Collect Tornis Kingfish", "Collect Dark Lava Eater",
                "Collect Bright Lava Eater", "Collect Verdant Dragonfish", "Collect Elder Dragonfish",
                "Collect Starlight Nautilus", "Collect Beryll Angle Fish",
                "Collect Glistening Deepstalker", "Collect Cosmic Form",
                "Collect Jasper Angle Fish", "Collect Splendid Deepstalker",
            ))
        if int(world.options.goal) <= 1:
            enabled_locations.extend((
                "Collect Terra Trilobite", "Collect Litho Trilobite", "Collect Greenhorn Pico",
                "Collect Pinkhorn Pico", "Collect Riftian Lampfish",
            ))
    if world.options.figurinesanity:
        allowed_scopes = {
            3: {"lower_wall"},
            2: {"lower_wall", "defeat_core_commander"},
            1: {"lower_wall", "defeat_core_commander", "defeat_sahabar"},
            0: {"lower_wall", "defeat_core_commander", "defeat_sahabar", "defeat_all_bosses"},
        }[int(world.options.goal)]
        enabled_locations.extend(
            name for name, (group, scope, _) in LOCATION_METADATA.items()
            if group == "figurinesanity" and scope in allowed_scopes
        )
    if world.options.critters:
        allowed_scopes = {
            3: {"lower_wall"},
            2: {"lower_wall", "defeat_core_commander"},
            1: {"lower_wall", "defeat_core_commander", "defeat_sahabar"},
            0: {"lower_wall", "defeat_core_commander", "defeat_sahabar", "defeat_all_bosses"},
        }[int(world.options.goal)]
        enabled_locations.extend(
            name for name, (group, scope, _) in LOCATION_METADATA.items()
            if group == "critters" and scope in allowed_scopes
        )
    if world.options.valuablesanity:
        allowed_scopes = {
            3: {"lower_wall"},
            2: {"lower_wall", "defeat_core_commander"},
            1: {"lower_wall", "defeat_core_commander", "defeat_sahabar"},
            0: {"lower_wall", "defeat_core_commander", "defeat_sahabar", "defeat_all_bosses"},
        }[int(world.options.goal)]
        enabled_locations.extend(
            name for name, (group, scope, _) in LOCATION_METADATA.items()
            if group == "valuablesanity" and scope in allowed_scopes
        )
    if world.options.toolsanity:
        allowed_scopes = {
            3: {"lower_wall"},
            2: {"lower_wall", "defeat_core_commander"},
            1: {"lower_wall", "defeat_core_commander", "defeat_sahabar"},
            0: {"lower_wall", "defeat_core_commander", "defeat_sahabar", "defeat_all_bosses"},
        }[int(world.options.goal)]
        enabled_locations.extend(
            name for name, (group, scope, _) in LOCATION_METADATA.items()
            if group == "toolsanity" and scope in allowed_scopes
        )
    if world.options.weaponsanity:
        allowed_scopes = {
            3: {"lower_wall"},
            2: {"lower_wall", "defeat_core_commander"},
            1: {"lower_wall", "defeat_core_commander", "defeat_sahabar"},
            0: {"lower_wall", "defeat_core_commander", "defeat_sahabar", "defeat_all_bosses"},
        }[int(world.options.goal)]
        enabled_locations.extend(
            name for name, (group, scope, _) in LOCATION_METADATA.items()
            if group == "weaponsanity" and scope in allowed_scopes
        )
    if world.options.accessanity:
        allowed_scopes = {
            3: {"lower_wall"},
            2: {"lower_wall", "defeat_core_commander"},
            1: {"lower_wall", "defeat_core_commander", "defeat_sahabar"},
            0: {"lower_wall", "defeat_core_commander", "defeat_sahabar", "defeat_all_bosses"},
        }[int(world.options.goal)]
        enabled_locations.extend(
            name for name, (group, scope, _) in LOCATION_METADATA.items()
            if group == "accessanity" and scope in allowed_scopes
        )
    if world.options.jewelrysanity:
        allowed_scopes = {
            3: {"lower_wall"},
            2: {"lower_wall", "defeat_core_commander"},
            1: {"lower_wall", "defeat_core_commander", "defeat_sahabar"},
            0: {"lower_wall", "defeat_core_commander", "defeat_sahabar", "defeat_all_bosses"},
        }[int(world.options.goal)]
        enabled_locations.extend(
            name for name, (group, scope, _) in LOCATION_METADATA.items()
            if group == "jewelrysanity" and scope in allowed_scopes
        )
    if world.options.armorsanity:
        allowed_scopes = {
            3: {"lower_wall"},
            2: {"lower_wall", "defeat_core_commander"},
            1: {"lower_wall", "defeat_core_commander", "defeat_sahabar"},
            0: {"lower_wall", "defeat_core_commander", "defeat_sahabar", "defeat_all_bosses"},
        }[int(world.options.goal)]
        enabled_locations.extend(
            name for name, (group, scope, _) in LOCATION_METADATA.items()
            if group == "armorsanity" and scope in allowed_scopes
        )
    if world.options.petsanity:
        allowed_scopes = {
            3: {"lower_wall"},
            2: {"lower_wall", "defeat_core_commander"},
            1: {"lower_wall", "defeat_core_commander", "defeat_sahabar"},
            0: {"lower_wall", "defeat_core_commander", "defeat_sahabar", "defeat_all_bosses"},
        }[int(world.options.goal)]
        enabled_locations.extend(
            name for name, (group, scope, _) in LOCATION_METADATA.items()
            if group == "petsanity" and scope in allowed_scopes
        )
    if world.options.merchantsanity:
        allowed_scopes = {
            3: {"lower_wall"},
            2: {"lower_wall", "defeat_core_commander"},
            1: {"lower_wall", "defeat_core_commander", "defeat_sahabar"},
            0: {"lower_wall", "defeat_core_commander", "defeat_sahabar", "defeat_all_bosses"},
        }[int(world.options.goal)]
        enabled_locations.extend(
            name for name, (group, scope, _) in LOCATION_METADATA.items()
            if group == "merchantsanity" and scope in allowed_scopes
        )
    if world.options.enemies:
        enabled_locations.extend((
            "Slay Shrooman", "Slay Shrooman Brute", "Slay Orange Slime", "Slay Red Slime",
            "Slay Caveling Skirmisher", "Slay Caveling Spearman", "Slay Clay Burrower",
            "Slay Larva", "Slay Big Larva", "Slay Hive Larva", "Slay Big Hive Larva",
            "Slay Acid Larva", "Slay Cocoon", "Slay Caveling", "Slay Caveling Shaman",
            "Slay Caveling Brute", "Slay Electro-Pest", "Slay Royal Slime",
        ))
        if int(world.options.goal) != 3:
            enabled_locations.extend((
                "Slay Caveling Hunter", "Slay Caveling Gardener", "Slay Snare Plant",
                "Slay Purple Slime", "Slay Infected Caveling", "Slay Mold Tentacle",
                "Slay Bubble Crab", "Slay Tentacle", "Slay Blue Slime", "Slay Caveling Scholar",
                "Slay Core Sentry", "Slay Bomb Scarab", "Slay Caveling Assassin",
                "Slay Caveling Mummy", "Slay Lava Slime", "Slay Lava Butterfly", "Slay Mimite",
                "Slay Orbital Turret", "Slay Nilipede",
            ))
        if int(world.options.goal) <= 1:
            enabled_locations.extend((
                "Slay Sulfur Worm", "Slay Colossal Amoeba", "Slay Cicada Nymph", "Slay Gold Scarab",
                "Slay Geobot Miner", "Slay Geobot Patroller", "Slay Geobot Scourer",
                "Slay Void Larva Cocoon", "Slay Void Larva", "Slay Void Caveling",
                "Slay Void Caveling Shaman", "Slay Void Caveling Brute",
            ))
    if world.options.cattle_mutilation:
        enabled_locations.extend(("Slay Moolin", "Slay Bambuck", "Slay Strolly Poly"))
        if int(world.options.goal) != 3:
            enabled_locations.extend(("Slay Kelple", "Slay Dodo", "Slay Drohmble", "Slay Crystal Snail"))
    if world.options.skillsanity:
        goal = int(world.options.goal)
        maximum = {3: 30, 2: 60, 1: 90, 0: 100}[goal]
        for skill in (
            "Mining", "Running", "Melee Combat", "Vitality", "Crafting", "Range Combat",
            "Gardening", "Fishing", "Cooking", "Magic", "Summoning", "Explosives",
        ):
            enabled_locations.extend(
                f"Level {level} {skill}" for level in range(10, maximum + 1, 10)
            )
    if world.options.locked_chests:
        enabled_locations.extend((
            "Collect Copper Key", "Unlock Locked Copper Chest",
            "Collect Iron Key", "Unlock Locked Iron Chest",
        ))
        if int(world.options.goal) != 3:
            enabled_locations.extend((
                "Collect Scarlet Key", "Unlock Locked Scarlet Chest",
                "Collect Octarine Key", "Unlock Locked Octarine Chest",
                "Collect Galaxite Key", "Unlock Locked Galaxite Chest",
                "Collect Solarite Key", "Unlock Locked Solarite Chest",
            ))
        if int(world.options.goal) <= 1:
            enabled_locations.extend(("Collect Relucite Key", "Unlock Locked Relucite Chest"))
    dirt.add_locations({name: LOCATION_NAME_TO_ID[name] for name in enabled_locations}, CoreKeeperLocation)
    restricted_groups = set()
    if world.options.prevent_priority_in_optional_checks:
        restricted_groups.update(OPTIONAL_GROUPS)
    if world.options.prevent_priority_in_sanity:
        restricted_groups.update(SANITY_GROUPS)
    if restricted_groups:
        for location in dirt.locations:
            metadata = LOCATION_METADATA.get(location.name)
            if metadata is not None and metadata[0] in restricted_groups:
                original_rule = location.item_rule
                location.item_rule = (
                    lambda item, original_rule=original_rule:
                    original_rule(item) and not item.advancement
                )

    regions = [menu, dirt, glurch, ghorm, malugaz, wall]
    world.multiworld.regions += regions
    menu.connect(dirt, "Start Game")
    dirt.connect(glurch, "Reach Glurch")
    dirt.connect(ghorm, "Reach Ghorm")
    malugaz_entrance = dirt.connect(malugaz, "Reach Malugaz")
    set_rule(malugaz_entrance, lambda state: state.has("Defeated Glurch", world.player))
    wall_entrance = dirt.connect(wall, "Insert the three boss gems")
    set_rule(wall_entrance, lambda state: state.has_all(
        {"Defeated Glurch", "Defeated Ghorm", "Defeated Malugaz"}, world.player
    ))

    if optional_bosses:
        world.multiworld.regions += [hive_mother, king_slime]
        entrance = dirt.connect(hive_mother, "Reach Hive Mother")
        set_rule(entrance, lambda state: _has_boss_slot_licenses(
            state, world, hologram=True
        ))
        entrance = dirt.connect(king_slime, "Reach King Slime")
        set_rule(entrance, lambda state: state.has("Defeated Glurch", world.player))

    if int(world.options.goal) == 3:
        wall.add_event("Lower Wall Goal", "Victory")
        return

    azeos = _boss_region(world, "Azeos Arena", "Defeat Azeos the Sky Titan", "Defeated Azeos")
    omoroth = _boss_region(world, "Omoroth Arena", "Defeat Omoroth the Sea Titan", "Defeated Omoroth")
    ra_akar = _boss_region(world, "Ra-Akar Arena", "Defeat Ra-Akar the Sand Titan", "Defeated Ra-Akar")
    druidra = _boss_region(world, "Druidra Arena", "Defeat Druidra the Wild Titan", "Defeated Druidra")
    crydra = _boss_region(world, "Crydra Arena", "Defeat Crydra the Ice Titan", "Defeated Crydra")
    pyrdra = _boss_region(world, "Pyrdra Arena", "Defeat Pyrdra the Fire Titan", "Defeated Pyrdra")
    commander = _boss_region(world, "Core Commander Arena", "Defeat Core Commander", "Defeated Core Commander")
    post_wall = [azeos, omoroth, ra_akar, druidra, crydra, pyrdra, commander]
    world.multiworld.regions += post_wall

    entrance = wall.connect(azeos, "Reach Azeos")
    set_rule(entrance, lambda state: _has_boss_slot_licenses(
        state, world, furnace=2, hologram=True
    ))
    entrance = wall.connect(omoroth, "Reach Omoroth")
    set_rule(entrance, lambda state: (
        state.has("Defeated Azeos", world.player)
        and _has_boss_slot_licenses(
            state,
            world,
            workbench=5,
            furnace=2,
            hologram=True,
            fishing_workbench=True,
        )
    ))
    entrance = wall.connect(ra_akar, "Reach Ra-Akar")
    set_rule(entrance, lambda state: (
        state.has("Defeated Omoroth", world.player)
        and _has_boss_slot_licenses(
            state, world, furnace=3, hologram=True, table_saw=True
        )
    ))
    entrance = wall.connect(druidra, "Reach Druidra")
    set_rule(entrance, lambda state: (
        state.has_all(
            {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"}, world.player
        )
        and _has_boss_slot_licenses(state, world, furnace=3, table_saw=True)
    ))
    entrance = wall.connect(crydra, "Reach Crydra")
    set_rule(entrance, lambda state: (
        state.has("Defeated Druidra", world.player)
        and _has_boss_slot_licenses(state, world, furnace=3, table_saw=True)
    ))
    entrance = wall.connect(pyrdra, "Reach Pyrdra")
    set_rule(entrance, lambda state: (
        state.has("Defeated Crydra", world.player)
        and _has_boss_slot_licenses(state, world, furnace=3, table_saw=True)
    ))
    entrance = wall.connect(commander, "Reach Core Commander")
    set_rule(entrance, lambda state: state.has_all(
        {"Defeated Druidra", "Defeated Crydra", "Defeated Pyrdra"}, world.player
    ))

    if optional_bosses:
        ivy = _boss_region(world, "Ivy Arena", "Defeat Ivy the Poisonous Mass", "Defeated Ivy")
        morpha = _boss_region(world, "Morpha Arena", "Defeat Morpha the Aquatic Mass", "Defeated Morpha")
        igneous = _boss_region(world, "Igneous Arena", "Defeat Igneous the Molten Mass", "Defeated Igneous")
        atlantean = _boss_region(world, "Atlantean Worm Arena", "Defeat Atlantean Worm", "Defeated Atlantean Worm")
        world.multiworld.regions += [ivy, morpha, igneous, atlantean]
        entrance = wall.connect(ivy, "Reach Ivy")
        set_rule(entrance, lambda state: _has_boss_slot_licenses(
            state, world, hologram=True
        ))
        entrance = wall.connect(morpha, "Reach Morpha")
        set_rule(entrance, lambda state: _has_boss_slot_licenses(
            state, world, hologram=True
        ))
        entrance = wall.connect(igneous, "Reach Igneous")
        set_rule(entrance, lambda state: _has_boss_slot_licenses(
            state, world, hologram=True
        ))
        entrance = wall.connect(atlantean, "Reach Atlantean Worm")
        set_rule(entrance, lambda state: (
            state.has_all(
                {"Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"}, world.player
            )
            and _has_boss_slot_licenses(state, world, hologram=True)
        ))

    if int(world.options.goal) == 2:
        commander.add_event("Core Commander Goal", "Victory")
        return

    nimruza = _boss_region(
        world,
        "Nimruza Arena",
        "Defeat Nimruza, Queen of the Burrowed Sands",
        "Defeated Nimruza",
    )
    sahabar = _boss_region(world, "S.A.H.A.B.A.R Arena", "Defeat S.A.H.A.B.A.R", "Defeated S.A.H.A.B.A.R")
    world.multiworld.regions += [nimruza, sahabar]
    entrance = commander.connect(nimruza, "Reach Nimruza")
    set_rule(entrance, lambda state: (
        state.has("Defeated Core Commander", world.player)
        and _has_boss_slot_licenses(state, world, furnace=3)
    ))
    entrance = nimruza.connect(sahabar, "Reach S.A.H.A.B.A.R")
    set_rule(entrance, lambda state: state.has("Defeated Nimruza", world.player))
    if int(world.options.goal) == 1:
        sahabar.add_event("S.A.H.A.B.A.R Goal", "Victory")
        return

    oblidra = _boss_region(world, "Oblidra Arena", "Defeat Oblidra the Void Titan", "Defeated Oblidra")
    urschleim = _boss_region(world, "Urschleim Arena", "Defeat Urschleim", "Defeated Urschleim")
    victory = Region("All Bosses Goal", world.player, world.multiworld)
    victory.add_event("All Bosses Goal", "Victory")
    world.multiworld.regions += [urschleim, oblidra, victory]
    entrance = commander.connect(urschleim, "Reach Urschleim")
    set_rule(entrance, lambda state: state.has("Defeated Core Commander", world.player))
    entrance = nimruza.connect(oblidra, "Reach Oblidra")
    set_rule(entrance, lambda state: state.has("Defeated Nimruza", world.player))
    entrance = sahabar.connect(victory, "Complete All Bosses")
    set_rule(entrance, lambda state: state.has_all({
        "Defeated Glurch", "Defeated Ghorm", "Defeated Malugaz",
        "Defeated Hive Mother", "Defeated King Slime", "Defeated Azeos",
        "Defeated Ivy", "Defeated Omoroth", "Defeated Morpha", "Defeated Ra-Akar",
        "Defeated Igneous", "Defeated Druidra", "Defeated Crydra", "Defeated Pyrdra",
        "Defeated Atlantean Worm", "Defeated Core Commander", "Defeated Urschleim",
        "Defeated Nimruza", "Defeated Oblidra", "Defeated S.A.H.A.B.A.R",
    }, world.player))
