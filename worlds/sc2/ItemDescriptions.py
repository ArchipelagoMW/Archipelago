"""
Contains descriptions for Starcraft 2 items.
"""
import inspect

from . import ItemNames

WEAPON_ARMOR_UPGRADE_NOTE = inspect.cleandoc("""
    Must be researched during the mission if the mission type isn't set to auto-unlock generic upgrades.
""")
GENERIC_UPGRADE_TEMPLATE = "Increases {} of {} {}.\n" + WEAPON_ARMOR_UPGRADE_NOTE
TERRAN = "Terran"
ZERG = "Zerg"
PROTOSS = "Protoss"

LASER_TARGETING_SYSTEMS_DESCRIPTION = "Increases vision by 2 and weapon range by 1."
STIMPACK_SMALL_COST = 10
STIMPACK_SMALL_HEAL = 30
STIMPACK_LARGE_COST = 20
STIMPACK_LARGE_HEAL = 60
STIMPACK_TEMPLATE = inspect.cleandoc("""
    Level 1: Stimpack: Increases unit movement and attack speed for 15 seconds. Injures the unit for {} life.
    Level 2: Super Stimpack: Instead of injuring the unit, heals the unit for {} life instead.
""")
STIMPACK_SMALL_DESCRIPTION = STIMPACK_TEMPLATE.format(STIMPACK_SMALL_COST, STIMPACK_SMALL_HEAL)
STIMPACK_LARGE_DESCRIPTION = STIMPACK_TEMPLATE.format(STIMPACK_LARGE_COST, STIMPACK_LARGE_HEAL)
SMART_SERVOS_DESCRIPTION = "Increases transformation speed between modes."
INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE = "{} can be trained from a {} without an attached Tech Lab."
CLOAK_DESCRIPTION_TEMPLATE = "Allows {} to use the Cloak ability."

DISPLAY_NAME_BROOD_LORD = "Brood Lord"
DISPLAY_NAME_CLOAKED_ASSASSIN = "Dark Templar, Avenger, and Blood Hunter"

resource_efficiency_cost_reduction = {
    ItemNames.MEDIC: (25, 25, 1),
    ItemNames.FIREBAT: (50, 0, 1),
    ItemNames.GOLIATH: (50, 0, 1),
    ItemNames.SIEGE_TANK: (0, 25, 1),
    ItemNames.DIAMONDBACK: (0, 50, 1),
    ItemNames.PREDATOR: (0, 75, 1),
    ItemNames.WARHOUND: (75, 0, 0),
    ItemNames.HERC: (25, 25, 1),
    ItemNames.WRAITH: (0, 50, 0),
    ItemNames.GHOST: (125, 75, 1),
    ItemNames.SPECTRE: (125, 75, 1),
    ItemNames.RAVEN: (0, 50, 0),
    ItemNames.CYCLONE: (25, 50, 1),
    ItemNames.LIBERATOR: (25, 25, 0),
    ItemNames.VALKYRIE: (100, 25, 1),
    ItemNames.SCOURGE: (0, 50, 0),
    ItemNames.HYDRALISK: (25, 25, 1),
    ItemNames.SWARM_HOST: (100, 25, 0),
    ItemNames.ULTRALISK: (100, 0, 2),
    DISPLAY_NAME_BROOD_LORD: (0, 75, 0),
    ItemNames.SWARM_QUEEN: (0, 50, 0),
    ItemNames.ARBITER: (50, 0, 0),
    ItemNames.REAVER: (100, 100, 2),
    DISPLAY_NAME_CLOAKED_ASSASSIN: (0, 50, 0),
}

def get_resource_efficiency_desc(item_name: str) -> str:
    cost = resource_efficiency_cost_reduction[item_name]
    parts = [f"{cost[0]} minerals"] if cost[0] else []
    parts += [f"{cost[1]} gas"] if cost[1] else []
    parts += [f"{cost[2]} supply"] if cost[2] else []
    assert parts, f"{item_name} doesn't reduce cost by anything"
    if len(parts) == 1:
        amount = parts[0]
    elif len(parts) == 2:
        amount = " and ".join(parts)
    else:
        amount = ", ".join(parts[:-1]) + ", and " + parts[-1]
    return (f"Reduces {item_name} cost by {amount}")

item_descriptions = {
    ItemNames.MARINE: "General-purpose infantry.",
    ItemNames.MEDIC: "Support trooper. Heals nearby biological units.",
    ItemNames.FIREBAT: "Specialized anti-infantry attacker.",
    ItemNames.MARAUDER: "Heavy assault infantry.",
    ItemNames.REAPER: "Raider. Capable of jumping up and down cliffs. Throws explosive mines.",
    ItemNames.HELLION: "Fast scout. Has a flame attack that damages all enemy units in its line of fire.",
    ItemNames.VULTURE: "Fast skirmish unit. Can use the Spider Mine ability.",
    ItemNames.GOLIATH: "Heavy-fire support unit.",
    ItemNames.DIAMONDBACK: "Fast, high-damage hovertank. Rail Gun can fire while the Diamondback is moving.",
    ItemNames.SIEGE_TANK: "Heavy tank. Long-range artillery in Siege Mode.",
    ItemNames.MEDIVAC: "Air transport. Heals nearby biological units.",
    ItemNames.WRAITH: "Highly mobile flying unit. Excellent at surgical strikes.",
    ItemNames.VIKING: inspect.cleandoc("""
                     Durable support flyer. Loaded with strong anti-capital air missiles. 
                     Can switch into Assault Mode to attack ground units.
                     """),
    ItemNames.BANSHEE: "Tactical-strike aircraft.",
    ItemNames.BATTLECRUISER: "Powerful warship.",
    ItemNames.GHOST: inspect.cleandoc("""
                     Infiltration unit. Can use Snipe and Cloak abilities. Can also call down Tactical Nukes.
                     """),
    ItemNames.SPECTRE: inspect.cleandoc("""
                     Infiltration unit. Can use Ultrasonic Pulse, Psionic Lash, and Cloak. 
                     Can also call down Tactical Nukes.
                     """),
    ItemNames.THOR: "Heavy assault mech.",
    ItemNames.LIBERATOR: inspect.cleandoc("""
                     Artillery fighter. Loaded with missiles that deal area damage to enemy air targets. 
                     Can switch into Defender Mode to provide siege support.
                     """),
    ItemNames.VALKYRIE: inspect.cleandoc("""
                     Advanced anti-aircraft fighter. 
                     Able to use cluster missiles that deal area damage to air targets.
                     """),
    ItemNames.WIDOW_MINE: inspect.cleandoc("""
                     Robotic mine. Launches missiles at nearby enemy units while burrowed. 
                     Attacks deal splash damage in a small area around the target. 
                     Widow Mine is revealed when Sentinel Missile is on cooldown.
                     """),
    ItemNames.CYCLONE: inspect.cleandoc("""
                     Mobile assault vehicle. Can use Lock On to quickly fire while moving.
                     """),
    ItemNames.HERC: inspect.cleandoc("""
                     Front-line infantry. Can use Grapple.
                     """),
    ItemNames.WARHOUND: inspect.cleandoc("""
                     Anti-vehicle mech. Haywire missiles do bonus damage to mechanical units.
                     """),
    ItemNames.PROGRESSIVE_TERRAN_INFANTRY_WEAPON: GENERIC_UPGRADE_TEMPLATE.format("damage", TERRAN, "infantry"),
    ItemNames.PROGRESSIVE_TERRAN_INFANTRY_ARMOR: GENERIC_UPGRADE_TEMPLATE.format("armor", TERRAN, "infantry"),
    ItemNames.PROGRESSIVE_TERRAN_VEHICLE_WEAPON: GENERIC_UPGRADE_TEMPLATE.format("damage", TERRAN, "vehicles"),
    ItemNames.PROGRESSIVE_TERRAN_VEHICLE_ARMOR: GENERIC_UPGRADE_TEMPLATE.format("armor", TERRAN, "vehicles"),
    ItemNames.PROGRESSIVE_TERRAN_SHIP_WEAPON: GENERIC_UPGRADE_TEMPLATE.format("damage", TERRAN, "starships"),
    ItemNames.PROGRESSIVE_TERRAN_SHIP_ARMOR: GENERIC_UPGRADE_TEMPLATE.format("armor", TERRAN, "starships"),
    ItemNames.PROGRESSIVE_TERRAN_WEAPON_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage", TERRAN, "units"),
    ItemNames.PROGRESSIVE_TERRAN_ARMOR_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("armor", TERRAN, "units"),
    ItemNames.PROGRESSIVE_TERRAN_INFANTRY_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", TERRAN, "infantry"),
    ItemNames.PROGRESSIVE_TERRAN_VEHICLE_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", TERRAN, "vehicles"),
    ItemNames.PROGRESSIVE_TERRAN_SHIP_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", TERRAN, "starships"),
    ItemNames.PROGRESSIVE_TERRAN_WEAPON_ARMOR_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", TERRAN, "units"),
    ItemNames.BUNKER_PROJECTILE_ACCELERATOR: "Increases range of all units in the Bunker by 1.",
    ItemNames.BUNKER_NEOSTEEL_BUNKER: "Increases the number of Bunker slots by 2.",
    ItemNames.MISSILE_TURRET_TITANIUM_HOUSING: "Increases Missile Turret life by 75.",
    ItemNames.MISSILE_TURRET_HELLSTORM_BATTERIES: "The Missile Turret unleashes an additional flurry of missiles with each attack.",
    ItemNames.SCV_ADVANCED_CONSTRUCTION: "Multiple SCVs can construct a structure, reducing its construction time.",
    ItemNames.SCV_DUAL_FUSION_WELDERS: "SCVs repair twice as fast.",
    ItemNames.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM: inspect.cleandoc("""
                     Level 1: While on low health, Terran structures are repaired to half health instead of burning down.
                     Level 2: Terran structures are repaired to full health instead of half health
                     """),
    ItemNames.PROGRESSIVE_ORBITAL_COMMAND: inspect.cleandoc("""
                     Level 1: Allows Command Centers to use Scanner Sweep and Calldown: MULE abilities.
                     Level 2: Orbital Command abilities work even in Planetary Fortress mode.
                     """),
    ItemNames.MARINE_PROGRESSIVE_STIMPACK: STIMPACK_SMALL_DESCRIPTION,
    ItemNames.MARINE_COMBAT_SHIELD: "Increases Marine life by 10.",
    ItemNames.MEDIC_ADVANCED_MEDIC_FACILITIES: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Medics", "Barracks"),
    ItemNames.MEDIC_STABILIZER_MEDPACKS: "Increases Medic heal speed. Reduces the amount of energy required for each heal.",
    ItemNames.FIREBAT_INCINERATOR_GAUNTLETS: "Increases Firebat's damage radius by 40%",
    ItemNames.FIREBAT_JUGGERNAUT_PLATING: "Increases Firebat's armor by 2.",
    ItemNames.MARAUDER_CONCUSSIVE_SHELLS: "Marauder attack temporarily slows all units in target area.",
    ItemNames.MARAUDER_KINETIC_FOAM: "Increases Marauder life by 25.",
    ItemNames.REAPER_U238_ROUNDS: inspect.cleandoc("""
                     Increases Reaper pistol attack range by 1.
                     Reaper pistols do additional 3 damage to Light Armor.
                     """),
    ItemNames.REAPER_G4_CLUSTERBOMB: "Timed explosive that does heavy area damage.",
    ItemNames.CYCLONE_MAG_FIELD_ACCELERATORS: "Increases Cyclone Lock On damage",
    ItemNames.CYCLONE_MAG_FIELD_LAUNCHERS: "Increases Cyclone attack range by 2.",
    ItemNames.MARINE_LASER_TARGETING_SYSTEM: LASER_TARGETING_SYSTEMS_DESCRIPTION,
    ItemNames.MARINE_MAGRAIL_MUNITIONS: "Deals 20 damage to target unit. Autocast on attack with a cooldown.",
    ItemNames.MARINE_OPTIMIZED_LOGISTICS: "Increases Marine training speed.",
    ItemNames.MEDIC_RESTORATION: "Removes negative status effects from target allied unit.",
    ItemNames.MEDIC_OPTICAL_FLARE: "Reduces vision range of target enemy unit. Disables detection.",
    ItemNames.MEDIC_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.MEDIC),
    ItemNames.FIREBAT_PROGRESSIVE_STIMPACK: STIMPACK_LARGE_DESCRIPTION,
    ItemNames.FIREBAT_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.FIREBAT),
    ItemNames.MARAUDER_PROGRESSIVE_STIMPACK: STIMPACK_LARGE_DESCRIPTION,
    ItemNames.MARAUDER_LASER_TARGETING_SYSTEM: LASER_TARGETING_SYSTEMS_DESCRIPTION,
    ItemNames.MARAUDER_MAGRAIL_MUNITIONS: "Deals 20 damage to target unit. Autocast on attack with a cooldown.",
    ItemNames.MARAUDER_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Marauders", "Barracks"),
    ItemNames.SCV_HOSTILE_ENVIRONMENT_ADAPTATION: "Increases SCV life by 15 and attack speed slightly.",
    ItemNames.MEDIC_ADAPTIVE_MEDPACKS: "Allows Medics to heal mechanical and air units.",
    ItemNames.MEDIC_NANO_PROJECTOR: "Increases Medic heal range by 2.",
    ItemNames.FIREBAT_INFERNAL_PRE_IGNITER: "Firebats do an additional 4 damage to Light Armor.",
    ItemNames.FIREBAT_KINETIC_FOAM: "Increases Firebat life by 100.",
    ItemNames.FIREBAT_NANO_PROJECTORS: "Increases Firebat attack range by 2",
    ItemNames.MARAUDER_JUGGERNAUT_PLATING: "Increases Marauder's armor by 2.",
    ItemNames.REAPER_JET_PACK_OVERDRIVE: inspect.cleandoc("""
                     Allows the Reaper to fly for 10 seconds.
                     While flying, the Reaper can attack air units.
                     """),
    ItemNames.HELLION_INFERNAL_PLATING: "Increases Hellion and Hellbat armor by 2.",
    ItemNames.VULTURE_AUTO_REPAIR: "Vultures regenerate life.",
    ItemNames.GOLIATH_SHAPED_HULL: "Increases Goliath life by 25.",
    ItemNames.GOLIATH_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.GOLIATH),
    ItemNames.GOLIATH_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Goliaths", "Factory"),
    ItemNames.SIEGE_TANK_SHAPED_HULL: "Increases Siege Tank life by 25.",
    ItemNames.SIEGE_TANK_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.SIEGE_TANK),
    ItemNames.PREDATOR_CLOAK: CLOAK_DESCRIPTION_TEMPLATE.format("Predators"),
    ItemNames.PREDATOR_CHARGE: "Allows Predators to intercept enemy ground units.",
    ItemNames.MEDIVAC_SCATTER_VEIL: "Medivacs get 100 shields.",
    ItemNames.REAPER_PROGRESSIVE_STIMPACK: STIMPACK_SMALL_DESCRIPTION,
    ItemNames.REAPER_LASER_TARGETING_SYSTEM: LASER_TARGETING_SYSTEMS_DESCRIPTION,
    ItemNames.REAPER_ADVANCED_CLOAKING_FIELD: "Reapers are permanently cloaked.",
    ItemNames.REAPER_SPIDER_MINES: "Allows Reapers to lay Spider Mines. 3 charges per Reaper.",
    ItemNames.REAPER_COMBAT_DRUGS: "Reapers regenerate life while out of combat.",
    ItemNames.HELLION_HELLBAT_ASPECT: "Allows Hellions to transform into Hellbats.",
    ItemNames.HELLION_SMART_SERVOS: "Transforms faster between modes. Hellions can attack while moving.",
    ItemNames.HELLION_OPTIMIZED_LOGISTICS: "Increases Hellion training speed.",
    ItemNames.HELLION_JUMP_JETS: inspect.cleandoc("""
                     Increases movement speed in Hellion mode.
                     In Hellbat mode, launches the Hellbat toward enemy ground units and briefly stuns them.
                     """),
    ItemNames.HELLION_PROGRESSIVE_STIMPACK: STIMPACK_LARGE_DESCRIPTION,
    ItemNames.VULTURE_ION_THRUSTERS: "Increases Vulture movement speed.",
    ItemNames.VULTURE_AUTO_LAUNCHERS: "Allows Vultures to attack while moving.",
    ItemNames.SPIDER_MINE_HIGH_EXPLOSIVE_MUNITION: "Increases Spider mine damage.",
    ItemNames.GOLIATH_JUMP_JETS: "Allows Goliaths to jump up and down cliffs.",
    ItemNames.GOLIATH_OPTIMIZED_LOGISTICS: "Increases Goliath training speed.",
    ItemNames.DIAMONDBACK_HYPERFLUXOR: "Increases Diamondback attack speed.",
    ItemNames.DIAMONDBACK_BURST_CAPACITORS: inspect.cleandoc("""
                     While not attacking, the Diamondback charges its weapon. 
                     The next attack does 10 additional damage.
                     """),
    ItemNames.DIAMONDBACK_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.DIAMONDBACK),
    ItemNames.SIEGE_TANK_JUMP_JETS: inspect.cleandoc("""
                     Repositions Siege Tank to a target location. 
                     Can be used in either mode and to jump up and down cliffs. 
                     """),
    ItemNames.SIEGE_TANK_SPIDER_MINES: inspect.cleandoc("""
                     Allows Siege Tanks to lay Spider Mines. 
                     Lays 3 Spider Mines at once. 3 charges
                     """),
    ItemNames.SIEGE_TANK_SMART_SERVOS: SMART_SERVOS_DESCRIPTION,
    ItemNames.SIEGE_TANK_GRADUATING_RANGE: inspect.cleandoc("""
                     Increases the Siege Tank's attack range by 1 every 3 seconds while in Siege Mode, 
                     up to a maximum of 5 additional range.
                     """),
    ItemNames.SIEGE_TANK_LASER_TARGETING_SYSTEM: LASER_TARGETING_SYSTEMS_DESCRIPTION,
    ItemNames.SIEGE_TANK_ADVANCED_SIEGE_TECH: "Siege Tanks gain +3 armor in Siege Mode.",
    ItemNames.SIEGE_TANK_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Siege Tanks", "Factory"),
    ItemNames.PREDATOR_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.PREDATOR),
    ItemNames.MEDIVAC_EXPANDED_HULL: "Increases Medivac cargo space by 4.",
    ItemNames.MEDIVAC_AFTERBURNERS: "Ability. Temporarily increases the Medivac's movement speed by 70%.",
    ItemNames.WRAITH_ADVANCED_LASER_TECHNOLOGY: inspect.cleandoc("""
                     Burst Lasers do more damage and can hit both ground and air targets.
                     Replaces Gemini Missiles weapon.
                     """),
    ItemNames.VIKING_SMART_SERVOS: SMART_SERVOS_DESCRIPTION,
    ItemNames.VIKING_ANTI_MECHANICAL_MUNITION: "Increases Viking damage to mechanical units while in Assault Mode.",
    ItemNames.DIAMONDBACK_ION_THRUSTERS: "Increases Diamondback movement speed.",
    ItemNames.WARHOUND_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.WARHOUND),
    ItemNames.WARHOUND_REINFORCED_PLATING: "Increases Warhound armor by 2.",
    ItemNames.HERC_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.HERC),
    ItemNames.HERC_JUGGERNAUT_PLATING: "Increases HERC armor by 2.",
    ItemNames.HERC_KINETIC_FOAM: "Increases HERC life by 50.",
    ItemNames.HELLION_TWIN_LINKED_FLAMETHROWER: "Doubles the width of the Hellion's flame attack.",
    ItemNames.HELLION_THERMITE_FILAMENTS: "Hellions do an additional 10 damage to Light Armor.",
    ItemNames.SPIDER_MINE_CERBERUS_MINE: "Increases trigger and blast radius of Spider Mines.",
    ItemNames.VULTURE_PROGRESSIVE_REPLENISHABLE_MAGAZINE: inspect.cleandoc("""
                     Level 1: Allows Vultures to replace used Spider Mines. Costs 15 minerals.
                     Level 2: Replacing used Spider Mines no longer costs minerals.
                     """),
    ItemNames.GOLIATH_MULTI_LOCK_WEAPONS_SYSTEM: "Goliaths can attack both ground and air targets simultaneously.",
    ItemNames.GOLIATH_ARES_CLASS_TARGETING_SYSTEM: "Increases Goliath ground attack range by 1 and air by 3.",
    ItemNames.DIAMONDBACK_PROGRESSIVE_TRI_LITHIUM_POWER_CELL: inspect.cleandoc("""
                     Level 1: Tri-Lithium Power Cell: Increases Diamondback attack range by 1.
                     Level 2: Tungsten Spikes: Increases Diamondback attack range by 3.
                     """),
    ItemNames.DIAMONDBACK_SHAPED_HULL: "Increases Diamondback life by 50.",
    ItemNames.SIEGE_TANK_MAELSTROM_ROUNDS: "Siege Tanks do an additional 40 damage to the primary target in Siege Mode.",
    ItemNames.SIEGE_TANK_SHAPED_BLAST: "Reduces splash damage to friendly targets while in Siege Mode by 75%.",
    ItemNames.MEDIVAC_RAPID_DEPLOYMENT_TUBE: "Medivacs deploy loaded troops almost instantly.",
    ItemNames.MEDIVAC_ADVANCED_HEALING_AI: "Medivacs can heal two targets at once.",
    ItemNames.WRAITH_PROGRESSIVE_TOMAHAWK_POWER_CELLS: inspect.cleandoc("""
                     Level 1: Tomahawk Power Cells: Increases Wraith starting energy by 100.
                     Level 2: Unregistered Cloaking Module: Wraiths do not require energy to cloak and remain cloaked.
                     """),
    ItemNames.WRAITH_DISPLACEMENT_FIELD: "Wraiths evade 20% of incoming attacks while cloaked.",
    ItemNames.VIKING_RIPWAVE_MISSILES: "Vikings do area damage while in Fighter Mode",
    ItemNames.VIKING_PHOBOS_CLASS_WEAPONS_SYSTEM: "Increases Viking attack range by 1 in Assault mode and 2 in Fighter mode.",
    ItemNames.BANSHEE_PROGRESSIVE_CROSS_SPECTRUM_DAMPENERS: inspect.cleandoc("""
                     Level 1: Banshees can remain cloaked twice as long.
                     Level 2: Banshees do not require energy to cloak and remain cloaked.
                     """),
    ItemNames.BANSHEE_SHOCKWAVE_MISSILE_BATTERY: "Banshees do area damage in a straight line.",
    ItemNames.BATTLECRUISER_PROGRESSIVE_MISSILE_PODS: "Spell. Missile Pods do damage to air targets in a target area.",
    ItemNames.BATTLECRUISER_PROGRESSIVE_DEFENSIVE_MATRIX: inspect.cleandoc("""
                     Level 1: Spell. For 20 seconds the Battlecruiser gains a shield that can absorb up to 200 damage.
                     Level 2: Passive. Battlecruiser gets 200 shields.
                     """),
    ItemNames.GHOST_OCULAR_IMPLANTS: "Increases Ghost sight range by 3 and attack range by 2.",
    ItemNames.GHOST_CRIUS_SUIT: "Cloak no longer requires energy to activate or maintain.",
    ItemNames.SPECTRE_PSIONIC_LASH: "Spell. Deals 200 damage to a single target.",
    ItemNames.SPECTRE_NYX_CLASS_CLOAKING_MODULE: "Cloak no longer requires energy to activate or maintain.",
    ItemNames.THOR_330MM_BARRAGE_CANNON: inspect.cleandoc("""
                     Improves 250mm Strike Cannons ability to deal area damage and stun units in a small area.
                     Can be also freely aimed on ground.
                     """),
    ItemNames.THOR_PROGRESSIVE_IMMORTALITY_PROTOCOL: inspect.cleandoc("""
                 Level 1: Allows destroyed Thors to be reconstructed on the field. Costs Vespene Gas.
                 Level 2: Thors are automatically reconstructed after falling for free.
                 """),
    ItemNames.LIBERATOR_ADVANCED_BALLISTICS: "Increases Liberator range by 3 in Defender Mode.",
    ItemNames.LIBERATOR_RAID_ARTILLERY: "Allows Liberators to attack structures while in Defender Mode.",
    ItemNames.WIDOW_MINE_DRILLING_CLAWS: "Allows Widow Mines to burrow and unburrow faster.",
    ItemNames.WIDOW_MINE_CONCEALMENT: "Burrowed Widow Mines are no longer revealed when the Sentinel Missile is on cooldown.",
    ItemNames.MEDIVAC_ADVANCED_CLOAKING_FIELD: "Medivacs are permanently cloaked.",
    ItemNames.WRAITH_TRIGGER_OVERRIDE: "Wraith attack speed increases by 10% with each attack, up to a maximum of 100%.",
    ItemNames.WRAITH_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Wraiths", "Starport"),
    ItemNames.WRAITH_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.WRAITH),
    ItemNames.VIKING_SHREDDER_ROUNDS: "Attacks in Assault mode do line splash damage.",
    ItemNames.VIKING_WILD_MISSILES: "Launches 5 rockets at the target unit. Each rocket does 25 (40 vs armored) damage.",
    ItemNames.BANSHEE_SHAPED_HULL: "Increases Banshee life by 100.",
    ItemNames.BANSHEE_ADVANCED_TARGETING_OPTICS: "Increases Banshee attack range by 2 while cloaked.",
    ItemNames.BANSHEE_DISTORTION_BLASTERS: "Increases Banshee attack damage by 25% while cloaked.",
    ItemNames.BANSHEE_ROCKET_BARRAGE: "Deals 75 damage to enemy ground units in the target area.",
    ItemNames.GHOST_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.GHOST),
    ItemNames.SPECTRE_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.SPECTRE),
    ItemNames.THOR_BUTTON_WITH_A_SKULL_ON_IT: "Allows Thors to launch nukes.",
    ItemNames.THOR_LASER_TARGETING_SYSTEM: LASER_TARGETING_SYSTEMS_DESCRIPTION,
    ItemNames.THOR_LARGE_SCALE_FIELD_CONSTRUCTION: "Allows Thors to be built by SCVs like a structure.",
    ItemNames.RAVEN_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.RAVEN),
    ItemNames.RAVEN_DURABLE_MATERIALS: "Extends timed life duration of Raven's summoned objects.",
    ItemNames.SCIENCE_VESSEL_IMPROVED_NANO_REPAIR: "Nano-Repair no longer requires energy to use.",
    ItemNames.SCIENCE_VESSEL_ADVANCED_AI_SYSTEMS: "Science Vessel can use Nano-Repair at two targets at once.",
    ItemNames.CYCLONE_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.CYCLONE),
    ItemNames.BANSHEE_HYPERFLIGHT_ROTORS: "Increases Banshee movement speed.",
    ItemNames.BANSHEE_LASER_TARGETING_SYSTEM: LASER_TARGETING_SYSTEMS_DESCRIPTION,
    ItemNames.BANSHEE_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Banshees", "Starport"),
    ItemNames.BATTLECRUISER_TACTICAL_JUMP: inspect.cleandoc("""
                     Allows Battlecruisers to warp to a target location anywhere on the map.
                     """),
    ItemNames.BATTLECRUISER_CLOAK: CLOAK_DESCRIPTION_TEMPLATE.format("Battlecruisers"),
    ItemNames.BATTLECRUISER_ATX_LASER_BATTERY: inspect.cleandoc("""
                     Battlecruisers can attack while moving, 
                     do the same damage to both ground and air targets, and fire faster.
                     """),
    ItemNames.BATTLECRUISER_OPTIMIZED_LOGISTICS: "Increases Battlecruiser training speed.",
    ItemNames.BATTLECRUISER_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Battlecruisers", "Starport"),
    ItemNames.GHOST_EMP_ROUNDS: inspect.cleandoc("""
                     Spell. Does 100 damage to shields and drains all energy from units in the targeted area. 
                     Cloaked units hit by EMP are revealed for a short time.
                     """),
    ItemNames.GHOST_LOCKDOWN: "Spell. Stuns a target mechanical unit for a long time.",
    ItemNames.SPECTRE_IMPALER_ROUNDS: "Spectres do additional damage to armored targets.",
    ItemNames.THOR_PROGRESSIVE_HIGH_IMPACT_PAYLOAD: inspect.cleandoc(f"""
                     Level 1: Allows Thors to transform in order to use an alternative air attack.
                     Level 2: {SMART_SERVOS_DESCRIPTION}
                     """),
    ItemNames.RAVEN_BIO_MECHANICAL_REPAIR_DRONE: "Spell. Deploys a drone that can heal biological or mechanical units.",
    ItemNames.RAVEN_SPIDER_MINES: "Spell. Deploys 3 Spider Mines to a target location.",
    ItemNames.RAVEN_RAILGUN_TURRET: inspect.cleandoc("""
                     Spell. Allows Ravens to deploy an advanced Auto-Turret, 
                     that can attack enemy ground units in a straight line.
                     """),
    ItemNames.RAVEN_HUNTER_SEEKER_WEAPON: "Allows Ravens to attack with a Hunter-Seeker weapon.",
    ItemNames.RAVEN_INTERFERENCE_MATRIX: inspect.cleandoc("""
                     Spell. Target enemy Mechanical or Psionic unit can't attack or use abilities for a short duration.
                     """),
    ItemNames.RAVEN_ANTI_ARMOR_MISSILE: "Spell. Decreases target and nearby enemy units armor by 2.",
    ItemNames.RAVEN_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Ravens", "Starport"),
    ItemNames.SCIENCE_VESSEL_EMP_SHOCKWAVE: "Spell. Depletes all energy and shields of all units in a target area.",
    ItemNames.SCIENCE_VESSEL_DEFENSIVE_MATRIX: inspect.cleandoc("""
                     Spell. Provides a target unit with a defensive barrier that can absorb up to 250 damage
                     """),
    ItemNames.CYCLONE_TARGETING_OPTICS: "Increases Cyclone Lock On casting range and the range while Locked On.",
    ItemNames.CYCLONE_RAPID_FIRE_LAUNCHERS: "The first 12 shots of Lock On are fired more quickly.",
    ItemNames.LIBERATOR_CLOAK: CLOAK_DESCRIPTION_TEMPLATE.format("Liberators"),
    ItemNames.LIBERATOR_LASER_TARGETING_SYSTEM: LASER_TARGETING_SYSTEMS_DESCRIPTION,
    ItemNames.LIBERATOR_OPTIMIZED_LOGISTICS: "Increases Liberator training speed.",
    ItemNames.WIDOW_MINE_BLACK_MARKET_LAUNCHERS: "Increases Widow Mine Sentinel Missile range.",
    ItemNames.WIDOW_MINE_EXECUTIONER_MISSILES: inspect.cleandoc("""
                     Reduces Sentinel Missile cooldown.
                     When killed, Widow Mines will launch several missiles at random enemy targets.
                     """),
    ItemNames.VALKYRIE_ENHANCED_CLUSTER_LAUNCHERS: "Valkyries fire 2 additional rockets each volley.",
    ItemNames.VALKYRIE_SHAPED_HULL: "Increases Valkyrie life by 50.",
    ItemNames.VALKYRIE_FLECHETTE_MISSILES: "Equips Valkyries with Air-to-Surface missiles to attack ground units.",
    ItemNames.VALKYRIE_AFTERBURNERS: "Ability. Temporarily increases the Valkyries's movement speed by 70%.",
    ItemNames.CYCLONE_INTERNAL_TECH_MODULE: INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Cyclones", "Factory"),
    ItemNames.LIBERATOR_SMART_SERVOS: SMART_SERVOS_DESCRIPTION,
    ItemNames.LIBERATOR_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.LIBERATOR),
    ItemNames.HERCULES_INTERNAL_FUSION_MODULE: "Hercules can be trained from a Starport without having a Fusion Core.",
    ItemNames.HERCULES_TACTICAL_JUMP: inspect.cleandoc("""
                     Allows Hercules to warp to a target location anywhere on the map.
                     """),
    ItemNames.PLANETARY_FORTRESS_PROGRESSIVE_AUGMENTED_THRUSTERS: inspect.cleandoc("""
                    Level 1: Lift Off - Planetary Fortress can lift off.
                    Level 2: Armament Stabilizers - Planetary Fortress can attack while lifted off.
                    """),
    ItemNames.PLANETARY_FORTRESS_ADVANCED_TARGETING: "Planetary Fortress can attack air units.",
    ItemNames.VALKYRIE_LAUNCHING_VECTOR_COMPENSATOR: "Allows Valkyries to shoot air while moving.",
    ItemNames.VALKYRIE_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.VALKYRIE),
    ItemNames.PREDATOR_PREDATOR_S_FURY: "Predators can use an attack that jumps between targets.",
    ItemNames.BATTLECRUISER_BEHEMOTH_PLATING: "Increases Battlecruiser armor by 2.",
    ItemNames.BATTLECRUISER_COVERT_OPS_ENGINES: "Increases Battlecruiser movement speed.",
    ItemNames.BUNKER: "Defensive structure. Able to load infantry units, giving them +1 range to their attacks.",
    ItemNames.MISSILE_TURRET: "Anti-air defensive structure.",
    ItemNames.SENSOR_TOWER: "Reveals locations of enemy units at long range.",
    ItemNames.WAR_PIGS: "Mercenary Marines",
    ItemNames.DEVIL_DOGS: "Mercenary Firebats",
    ItemNames.HAMMER_SECURITIES: "Mercenary Marauders",
    ItemNames.SPARTAN_COMPANY: "Mercenary Goliaths",
    ItemNames.SIEGE_BREAKERS: "Mercenary Siege Tanks",
    ItemNames.HELS_ANGELS: "Mercenary Vikings",
    ItemNames.DUSK_WINGS: "Mercenary Banshees",
    ItemNames.JACKSONS_REVENGE: "Mercenary Battlecruiser",
    ItemNames.SKIBIS_ANGELS: "Mercenary Medics",
    ItemNames.DEATH_HEADS: "Mercenary Reapers",
    ItemNames.WINGED_NIGHTMARES: "Mercenary Wraiths",
    ItemNames.MIDNIGHT_RIDERS: "Mercenary Liberators",
    ItemNames.BRYNHILDS: "Mercenary Valkyries",
    ItemNames.JOTUN: "Mercenary Thor",
    ItemNames.ULTRA_CAPACITORS: "Increases attack speed of units by 5% per weapon upgrade.",
    ItemNames.VANADIUM_PLATING: "Increases the life of units by 5% per armor upgrade.",
    ItemNames.ORBITAL_DEPOTS: "Supply depots are built instantly.",
    ItemNames.MICRO_FILTERING: "Refineries produce Vespene gas 25% faster.",
    ItemNames.AUTOMATED_REFINERY: "Eliminates the need for SCVs in vespene gas production.",
    ItemNames.COMMAND_CENTER_REACTOR: "Command Centers can train two SCVs at once.",
    ItemNames.RAVEN: "Aerial Caster unit.",
    ItemNames.SCIENCE_VESSEL: "Aerial Caster unit. Can repair mechanical units.",
    ItemNames.TECH_REACTOR: "Merges Tech Labs and Reactors into one add on structure to provide both functions.",
    ItemNames.ORBITAL_STRIKE: "Trained units from Barracks are instantly deployed on rally point.",
    ItemNames.BUNKER_SHRIKE_TURRET: "Adds an automated turret to Bunkers.",
    ItemNames.BUNKER_FORTIFIED_BUNKER: "Bunkers have more life.",
    ItemNames.PLANETARY_FORTRESS: inspect.cleandoc("""
                     Allows Command Centers to upgrade into a defensive structure with a turret and additional armor.
                     Planetary Fortresses cannot Lift Off, or cast Orbital Command spells.
                     """),
    ItemNames.PERDITION_TURRET: "Automated defensive turret. Burrows down while no enemies are nearby.",
    ItemNames.PREDATOR: "Anti-infantry specialist that deals area damage with each attack.",
    ItemNames.HERCULES: "Massive transport ship.",
    ItemNames.CELLULAR_REACTOR: "All Terran spellcasters get +100 starting and maximum energy.",
    ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL: inspect.cleandoc("""
                     Allows Terran mechanical units to regenerate health while not in combat.
                     Each level increases life regeneration speed.
                     """),
    ItemNames.HIVE_MIND_EMULATOR: "Defensive structure. Can permanently Mind Control Zerg units.",
    ItemNames.PSI_DISRUPTER: "Defensive structure. Slows the attack and movement speeds of all nearby Zerg units.",
    ItemNames.STRUCTURE_ARMOR: "Increases armor of all Terran structures by 2.",
    ItemNames.HI_SEC_AUTO_TRACKING: "Increases attack range of all Terran structures by 1.",
    ItemNames.ADVANCED_OPTICS: "Increases attack range of all Terran mechanical units by 1.",
    ItemNames.ROGUE_FORCES: "Mercenary calldowns are no longer limited by charges.",
    ItemNames.ZEALOT: "Powerful melee warrior. Can use the charge ability.",
    ItemNames.STALKER: "Ranged attack strider. Can use the Blink ability.",
    ItemNames.HIGH_TEMPLAR: "Potent psionic master. Can use the Feedback and Psionic Storm abilities. Can merge into an Archon.",
    ItemNames.DARK_TEMPLAR: "Deadly warrior-assassin. Permanently cloaked. Can use the Shadow Fury ability.",
    ItemNames.IMMORTAL: "Assault strider. Can use Barrier to absorb damage.",
    ItemNames.COLOSSUS: "Battle strider with a powerful area attack. Can walk up and down cliffs. Attacks set fire to the ground, dealing extra damage to enemies over time.",
    ItemNames.PHOENIX: "Air superiority starfighter. Can use Graviton Beam and Phasing Armor abilities.",
    ItemNames.VOID_RAY: "Surgical strike craft. Has the Prismatic Alignment and Prismatic Range abilities.",
    ItemNames.CARRIER: "Capital ship. Builds and launches Interceptors that attack enemy targets. Repair Drones heal nearby mechanical units.",
    ItemNames.STARTING_MINERALS: "Increases the starting minerals for all missions.",
    ItemNames.STARTING_VESPENE: "Increases the starting vespene for all missions.",
    ItemNames.STARTING_SUPPLY: "Increases the starting supply for all missions.",
    ItemNames.NOTHING: "Does nothing. Used to remove a location from the game.",
    ItemNames.NOVA_GHOST_VISOR: "Reveals the locations of enemy units in the fog of war around Nova. Can detect cloaked units.",
    ItemNames.NOVA_RANGEFINDER_OCULUS: "Increaases Nova's vision range and non-melee weapon attack range by 2. Also increases range of melee weapons by 1.",
    ItemNames.NOVA_DOMINATION: "Gives Nova the ability to mind-control a target enemy unit.",
    ItemNames.NOVA_BLINK: "Gives Nova the ability to teleport a short distance and cloak for 10s.",
    ItemNames.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE: inspect.cleandoc("""
                     Level 1: Gives Nova the ability to cloak.
                     Level 2: Nova is permanently cloaked.
                     """),
    ItemNames.NOVA_ENERGY_SUIT_MODULE: "Increases Nova's maximum energy and energy regeneration rate.",
    ItemNames.NOVA_ARMORED_SUIT_MODULE: "Increases Nova's health by 100 and armour by 1. Nova also regenerates life quickly out of combat.",
    ItemNames.NOVA_JUMP_SUIT_MODULE: "Increases Nova's movement speed and allows her to jump up and down cliffs.",
    ItemNames.NOVA_C20A_CANISTER_RIFLE: "Allows Nova to equip the C20A Canister Rifle, which has a ranged attack and allows Nova to cast Snipe.",
    ItemNames.NOVA_HELLFIRE_SHOTGUN: "Allows Nova to equip the Hellfire Shotgun, which has a short-range area attack in a cone and allows Nova to cast Penetrating Blast.",
    ItemNames.NOVA_PLASMA_RIFLE: "Allows Nova to equip the Plasma Rifle, which has a rapidfire ranged attack and allows Nova to cast Plasma Shot.",
    ItemNames.NOVA_MONOMOLECULAR_BLADE: "Allows Nova to equip the Monomolecular Blade, which has a melee attack and allows Nova to cast Dash Attack.",
    ItemNames.NOVA_BLAZEFIRE_GUNBLADE: "Allows Nova to equip the Blazefire Gunblade, which has a melee attack and allows Nova to cast Fury of One.",
    ItemNames.NOVA_STIM_INFUSION: "Gives Nova the ability to heal herself and temporarily increase her movement and attack speeds.",
    ItemNames.NOVA_PULSE_GRENADES: "Gives Nova the ability to throw a grenade dealing large damage in an area.",
    ItemNames.NOVA_FLASHBANG_GRENADES: "Gives Nova the ability to throw a grenade to stun enemies and disable detection in a large area.",
    ItemNames.NOVA_IONIC_FORCE_FIELD: "Gives Nova the ability to shield herself temporarily.",
    ItemNames.NOVA_HOLO_DECOY: "Gives Nova the ability to summon a decoy unit which enemies will prefer to target and takes reduced damage.",
    ItemNames.NOVA_NUKE: "Gives Nova the ability to launch tactical nukes built from the Shadow Ops.",
    ItemNames.ZERGLING: "Fast inexpensive melee attacker. Hatches in pairs from a single larva. Can morph into a Baneling.",
    ItemNames.SWARM_QUEEN: "Ranged support caster. Can use the Spawn Creep Tumor and Rapid Transfusion abilities.",
    ItemNames.ROACH: "Durable short ranged attacker. Regenerates life quickly when burrowed.",
    ItemNames.HYDRALISK: "High-damage generalist ranged attacker.",
    ItemNames.ZERGLING_BANELING_ASPECT: "Anti-ground suicide unit. Does damage over a small area on death.",
    ItemNames.ABERRATION: "Durable melee attacker that deals heavy damage and can walk over other units.",
    ItemNames.MUTALISK: "Fragile flying attacker. Attacks bounce between targets.",
    ItemNames.SWARM_HOST: "Siege unit that attacks by rooting in place and continually spawning Locusts.",
    ItemNames.INFESTOR: "Support caster that can move while burrowed. Can use the Fungal Growth, Parasitic Domination, and Consumption abilities.",
    ItemNames.ULTRALISK: "Massive melee attacker. Has an area-damage cleave attack.",
    ItemNames.SPORE_CRAWLER: "Anti-air defensive structure that can detect cloaked units.",
    ItemNames.SPINE_CRAWLER: "Anti-ground defensive structure.",
    ItemNames.CORRUPTOR: "Anti-air flying attacker specializing in taking down enemy capital ships.",
    ItemNames.SCOURGE: "Flying anti-air suicide unit. Hatches in pairs from a single larva.",
    ItemNames.BROOD_QUEEN: "Flying support caster. Can cast the Ocular Symbiote and Spawn Broodlings abilities.",
    ItemNames.DEFILER: "Support caster. Can use the Dark Swarm, Consume, and Plague abilities.",
    ItemNames.PROGRESSIVE_ZERG_MELEE_ATTACK: GENERIC_UPGRADE_TEMPLATE.format("damage", ZERG, "melee ground units"),
    ItemNames.PROGRESSIVE_ZERG_MISSILE_ATTACK: GENERIC_UPGRADE_TEMPLATE.format("damage", ZERG, "ranged ground units"),
    ItemNames.PROGRESSIVE_ZERG_GROUND_CARAPACE: GENERIC_UPGRADE_TEMPLATE.format("armor", ZERG, "ground units"),
    ItemNames.PROGRESSIVE_ZERG_FLYER_ATTACK: GENERIC_UPGRADE_TEMPLATE.format("damage", ZERG, "flyers"),
    ItemNames.PROGRESSIVE_ZERG_FLYER_CARAPACE: GENERIC_UPGRADE_TEMPLATE.format("armor", ZERG, "flyers"),
    ItemNames.PROGRESSIVE_ZERG_WEAPON_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage", ZERG, "units"),
    ItemNames.PROGRESSIVE_ZERG_ARMOR_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("armor", ZERG, "units"),
    ItemNames.PROGRESSIVE_ZERG_GROUND_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", ZERG, "ground units"),
    ItemNames.PROGRESSIVE_ZERG_FLYER_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", ZERG, "flyers"),
    ItemNames.PROGRESSIVE_ZERG_WEAPON_ARMOR_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", ZERG, "units"),
    ItemNames.ZERGLING_HARDENED_CARAPACE: "Increases Zergling health by +10.",
    ItemNames.ZERGLING_ADRENAL_OVERLOAD: "Increases Zergling attack speed.",
    ItemNames.ZERGLING_METABOLIC_BOOST: "Increases Zergling movement speed.",
    ItemNames.ROACH_HYDRIODIC_BILE: "Roaches deal +8 damage to light targets.",
    ItemNames.ROACH_ADAPTIVE_PLATING: "Roaches gain +3 armour when their life is below 50%.",
    ItemNames.ROACH_TUNNELING_CLAWS: "Allows Roaches to move while burrowed.",
    ItemNames.HYDRALISK_FRENZY: "Allows Hydralisks to use the Frenzy ability, which increases their attack speed by 50%.",
    ItemNames.HYDRALISK_ANCILLARY_CARAPACE: "Hydralisks gain +20 health.",
    ItemNames.HYDRALISK_GROOVED_SPINES: "Hydralisks gain +1 range.",
    ItemNames.BANELING_CORROSIVE_ACID: "Increases the damage banelings deal to their primary target. Splash damage remains the same.",
    ItemNames.BANELING_RUPTURE: "Increases the splash radius of baneling attacks.",
    ItemNames.BANELING_REGENERATIVE_ACID: "Banelings will heal nearby friendly units when they explode.",
    ItemNames.MUTALISK_VICIOUS_GLAIVE: "Mutalisks attacks will bounce an additional 3 times.",
    ItemNames.MUTALISK_RAPID_REGENERATION: "Mutalisks will regenerate quickly when out of combat.",
    ItemNames.MUTALISK_SUNDERING_GLAIVE: "Mutalisks deal increased damage to their primary target.",
    ItemNames.SWARM_HOST_BURROW: "Allows Swarm Hosts to burrow instead of root to spawn locusts.",
    ItemNames.SWARM_HOST_RAPID_INCUBATION: "Swarm Hosts will spawn locusts 20% faster.",
    ItemNames.SWARM_HOST_PRESSURIZED_GLANDS: "Allows Swarm Host Locusts to attack air targets.",
    ItemNames.ULTRALISK_BURROW_CHARGE: "Allows Ultralisks to burrow and charge at enemy units, knocking back and stunning units when it emerges.",
    ItemNames.ULTRALISK_TISSUE_ASSIMILATION: "Ultralisks recover health when they deal damage.",
    ItemNames.ULTRALISK_MONARCH_BLADES: "Ultralisks gain increased splash damage.",
    ItemNames.CORRUPTOR_CAUSTIC_SPRAY: "Allows Corruptors to use the Caustic Spray ability, which deals ramping damage to buildings over time.",
    ItemNames.CORRUPTOR_CORRUPTION: "Allows Corruptors to use the Corruption ability, which causes a target enemy unit to take increased damage.",
    ItemNames.SCOURGE_VIRULENT_SPORES: "Scourge will deal splash damage.",
    ItemNames.SCOURGE_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.SCOURGE),
    ItemNames.SCOURGE_SWARM_SCOURGE: "An extra Scourge will be built from each egg at no additional cost.",
    ItemNames.ZERGLING_SHREDDING_CLAWS: "Zergling attacks will temporarily reduce their target's armour to 0.",
    ItemNames.ROACH_GLIAL_RECONSTITUTION: "Increases Roach movement speed.",
    ItemNames.ROACH_ORGANIC_CARAPACE: "Increases Roach health by +25.",
    ItemNames.HYDRALISK_MUSCULAR_AUGMENTS: "Increases Hydralisk movement speed.",
    ItemNames.HYDRALISK_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.HYDRALISK),
    ItemNames.BANELING_CENTRIFUGAL_HOOKS: "Increases the movement speed of Banelings.",
    ItemNames.BANELING_TUNNELING_JAWS: "Allows Banelings to move while burrowed.",
    ItemNames.BANELING_RAPID_METAMORPH: "Banelings morph faster.",
    ItemNames.MUTALISK_SEVERING_GLAIVE: "Mutalisk bounce attacks will deal full damage.",
    ItemNames.MUTALISK_AERODYNAMIC_GLAIVE_SHAPE: "Increases the attack range of Mutalisks by 2.",
    ItemNames.SWARM_HOST_LOCUST_METABOLIC_BOOST: "Increases Locust movement speed.",
    ItemNames.SWARM_HOST_ENDURING_LOCUSTS: "Increases the duration of Swarm Hosts' Locusts by 10s.",
    ItemNames.SWARM_HOST_ORGANIC_CARAPACE: "Increases Swarm Host health by +40.",
    ItemNames.SWARM_HOST_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.SWARM_HOST),
    ItemNames.ULTRALISK_ANABOLIC_SYNTHESIS: None,
    ItemNames.ULTRALISK_CHITINOUS_PLATING: None,
    ItemNames.ULTRALISK_ORGANIC_CARAPACE: None,
    ItemNames.ULTRALISK_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.ULTRALISK),
    ItemNames.DEVOURER_CORROSIVE_SPRAY: None,
    ItemNames.DEVOURER_GAPING_MAW: None,
    ItemNames.DEVOURER_IMPROVED_OSMOSIS: None,
    ItemNames.DEVOURER_PRESCIENT_SPORES: None,
    ItemNames.GUARDIAN_PROLONGED_DISPERSION: None,
    ItemNames.GUARDIAN_PRIMAL_ADAPTATION: None,
    ItemNames.GUARDIAN_SORONAN_ACID: None,
    ItemNames.IMPALER_ADAPTIVE_TALONS: None,
    ItemNames.IMPALER_SECRETION_GLANDS: None,
    ItemNames.IMPALER_HARDENED_TENTACLE_SPINES: None,
    ItemNames.LURKER_SEISMIC_SPINES: None,
    ItemNames.LURKER_ADAPTED_SPINES: None,
    ItemNames.RAVAGER_POTENT_BILE: None,
    ItemNames.RAVAGER_BLOATED_BILE_DUCTS: None,
    ItemNames.RAVAGER_DEEP_TUNNEL: None,
    ItemNames.VIPER_PARASITIC_BOMB: None,
    ItemNames.VIPER_PARALYTIC_BARBS: None,
    ItemNames.VIPER_VIRULENT_MICROBES: None,
    ItemNames.BROOD_LORD_POROUS_CARTILAGE: None,
    ItemNames.BROOD_LORD_EVOLVED_CARAPACE: None,
    ItemNames.BROOD_LORD_SPLITTER_MITOSIS: None,
    ItemNames.BROOD_LORD_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(DISPLAY_NAME_BROOD_LORD),
    ItemNames.INFESTOR_INFESTED_TERRAN: None,
    ItemNames.INFESTOR_MICROBIAL_SHROUD: None,
    ItemNames.SWARM_QUEEN_SPAWN_LARVAE: None,
    ItemNames.SWARM_QUEEN_DEEP_TUNNEL: None,
    ItemNames.SWARM_QUEEN_ORGANIC_CARAPACE: None,
    ItemNames.SWARM_QUEEN_BIO_MECHANICAL_TRANSFUSION: None,
    ItemNames.SWARM_QUEEN_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.SWARM_QUEEN),
    ItemNames.SWARM_QUEEN_INCUBATOR_CHAMBER: None,
    ItemNames.BROOD_QUEEN_FUNGAL_GROWTH: None,
    ItemNames.BROOD_QUEEN_ENSNARE: None,
    ItemNames.BROOD_QUEEN_ENHANCED_MITOCHONDRIA: None,
    ItemNames.ZERGLING_RAPTOR_STRAIN: "Allows Zerglings to jump up and down cliffs and leap onto enemies. Also increases Zergling attack damage by 2.",
    ItemNames.ZERGLING_SWARMLING_STRAIN: "Zerglings will spawn instantly and with an extra Zergling per egg at no additional cost.",
    ItemNames.ROACH_VILE_STRAIN: "Roach attacks will slow the movement and attack speed of enemies.",
    ItemNames.ROACH_CORPSER_STRAIN: "Units killed after being attacked by Roaches will spawn 2 Roachlings.",
    ItemNames.HYDRALISK_IMPALER_ASPECT: "Allows Hydralisks to morph into Impalers.",
    ItemNames.HYDRALISK_LURKER_ASPECT: "Allows Hydralisks to morph into Lurkers.",
    ItemNames.BANELING_SPLITTER_STRAIN: "Banelings will split into two smaller Splitterlings on exploding.",
    ItemNames.BANELING_HUNTER_STRAIN: "Allows Banelings to jump up and down cliffs and leap onto enemies.",
    ItemNames.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT: "Allows Mutalisks and Corruptors to morph into Brood Lords.",
    ItemNames.MUTALISK_CORRUPTOR_VIPER_ASPECT: "Allows Mutalisks and Corruptors to morph into Vipers.",
    ItemNames.SWARM_HOST_CARRION_STRAIN: "Swarm Hosts will spawn Flying Locusts.",
    ItemNames.SWARM_HOST_CREEPER_STRAIN: "Allows Swarm Hosts to teleport to any creep on the map in vision. Swarm Hosts will spread creep around them when rooted or burrowed.",
    ItemNames.ULTRALISK_NOXIOUS_STRAIN: "Ultralisks will periodically spread poison, damaging nearby biological enemies.",
    ItemNames.ULTRALISK_TORRASQUE_STRAIN: "Ultralisks will revive after being killed.",
    ItemNames.KERRIGAN_KINETIC_BLAST: None,
    ItemNames.KERRIGAN_HEROIC_FORTITUDE: None,
    ItemNames.KERRIGAN_LEAPING_STRIKE: None,
    ItemNames.KERRIGAN_CRUSHING_GRIP: None,
    ItemNames.KERRIGAN_CHAIN_REACTION: None,
    ItemNames.KERRIGAN_PSIONIC_SHIFT: None,
    ItemNames.KERRIGAN_ZERGLING_RECONSTITUTION: None,
    ItemNames.KERRIGAN_IMPROVED_OVERLORDS: None,
    ItemNames.KERRIGAN_AUTOMATED_EXTRACTORS: None,
    ItemNames.KERRIGAN_WILD_MUTATION: None,
    ItemNames.KERRIGAN_SPAWN_BANELINGS: None,
    ItemNames.KERRIGAN_MEND: None,
    ItemNames.KERRIGAN_TWIN_DRONES: None,
    ItemNames.KERRIGAN_MALIGNANT_CREEP: None,
    ItemNames.KERRIGAN_VESPENE_EFFICIENCY: None,
    ItemNames.KERRIGAN_INFEST_BROODLINGS: None,
    ItemNames.KERRIGAN_FURY: None,
    ItemNames.KERRIGAN_ABILITY_EFFICIENCY: None,
    ItemNames.KERRIGAN_APOCALYPSE: None,
    ItemNames.KERRIGAN_SPAWN_LEVIATHAN: None,
    ItemNames.KERRIGAN_DROP_PODS: None,
    ItemNames.KERRIGAN_PRIMAL_FORM: None,
    ItemNames.KERRIGAN_LEVELS_10: None,
    ItemNames.KERRIGAN_LEVELS_9: None,
    ItemNames.KERRIGAN_LEVELS_8: None,
    ItemNames.KERRIGAN_LEVELS_7: None,
    ItemNames.KERRIGAN_LEVELS_6: None,
    ItemNames.KERRIGAN_LEVELS_5: None,
    ItemNames.KERRIGAN_LEVELS_4: None,
    ItemNames.KERRIGAN_LEVELS_3: None,
    ItemNames.KERRIGAN_LEVELS_2: None,
    ItemNames.KERRIGAN_LEVELS_1: None,
    ItemNames.KERRIGAN_LEVELS_14: None,
    ItemNames.KERRIGAN_LEVELS_35: None,
    ItemNames.KERRIGAN_LEVELS_70: None,
    ItemNames.INFESTED_MEDICS: None,
    ItemNames.INFESTED_SIEGE_TANKS: None,
    ItemNames.INFESTED_BANSHEES: None,
    ItemNames.OVERLORD_VENTRAL_SACS: None,
    ItemNames.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT: None,
    ItemNames.MUTALISK_CORRUPTOR_DEVOURER_ASPECT: None,
    ItemNames.ROACH_RAVAGER_ASPECT: None,
    ItemNames.OBSERVER: "Flying spy. Cloak renders the unit invisible to enemies without detection.",
    ItemNames.CENTURION: "Powerful melee warrior. Has the Shadow Charge and Darkcoil abilities.",
    ItemNames.SENTINEL: "Powerful melee warrior. Has the Charge and Reconstruction abilities.",
    ItemNames.SUPPLICANT: "Powerful melee warrior. Has powerful damage resistant shields.",
    ItemNames.INSTIGATOR: "Ranged support strider. Can store multiple Blink charges.",
    ItemNames.SLAYER: "Ranged attack strider. Can use the Phase Blink and Phasing Armor abilities.",
    ItemNames.SENTRY: "Robotic support unit can use the Guardian Shield ability and restore the shields of nearby Protoss units.",
    ItemNames.ENERGIZER: "Robotic support unit. Can use the Chrono Beam ability and become stationary to power nearby structures.",
    ItemNames.HAVOC: "Robotic support unit. Can use the Target Lock and Force Field abilities and increase the range of nearby Protoss units.",
    ItemNames.SIGNIFIER: "Potent permanently cloaked psionic master. Can use the Feedback and Crippling Psionic Storm abilities. Can merge into an Archon.",
    ItemNames.ASCENDANT: "Potent psionic master. Can use the Psionic Orb, Mind Blast, and Sacrifice abilities.",
    ItemNames.AVENGER: "Deadly warrior-assassin. Permanently cloaked. Recalls to the nearest Dark Shrine upon death.",
    ItemNames.BLOOD_HUNTER: "Deadly warrior-assassin. Permanently cloaked. Can use the Void Stasis ability.",
    ItemNames.DRAGOON: "Ranged assault strider. Has enhanced health and damage.",
    ItemNames.DARK_ARCHON: "Potent psionic master. Can use the Confuse and Mind Control abilities.",
    ItemNames.ADEPT: "Ranged specialist. Can use the Psionic Transfer ability.",
    ItemNames.WARP_PRISM: "Flying transport. Can carry units and become stationary to deploy a power field.",
    ItemNames.ANNIHILATOR: "Assault Strider. Can use the Shadow Cannon ability to damage air and ground units.",
    ItemNames.VANGUARD: "Assault Strider. Deals splash damage around the primary target.",
    ItemNames.WRATHWALKER: "Battle strider with a powerful single target attack.  Can walk up and down cliffs.",
    ItemNames.REAVER: "Area damage siege unit. Builds and launches explosive Scarabs for high burst damage.",
    ItemNames.DISRUPTOR: "Robotic disruption unit. Can use the Purification Nova ability to deal heavy area damage.",
    ItemNames.MIRAGE: "Air superiority starfighter. Can use Graviton Beam and Phasing Armor abilities.",
    ItemNames.CORSAIR: "Air superiority starfighter. Can use the Disruption Web ability.",
    ItemNames.DESTROYER: "Area assault craft. Can use the Destruction Beam ability to attack multiple units at once.",
    ItemNames.SCOUT: "Versatile high-speed fighter.",
    ItemNames.TEMPEST: "Siege artillery craft. Attacks from long range. Can use the Disintegration ability.",
    ItemNames.MOTHERSHIP: "Ultimate Protoss vessel, Can use the Vortex and Mass Recall abilities. Cloaks nearby units and structures.",
    ItemNames.ARBITER: "Army support craft. Has the Stasis Field and Recall abilities. Cloaks nearby units.",
    ItemNames.ORACLE: "Flying caster. Can use the Revelation and Stasis Ward abilities.",
    ItemNames.PROGRESSIVE_PROTOSS_GROUND_WEAPON: GENERIC_UPGRADE_TEMPLATE.format("damage", PROTOSS, "ground units"),
    ItemNames.PROGRESSIVE_PROTOSS_GROUND_ARMOR: GENERIC_UPGRADE_TEMPLATE.format("armor", PROTOSS, "ground units"),
    ItemNames.PROGRESSIVE_PROTOSS_SHIELDS: GENERIC_UPGRADE_TEMPLATE.format("shields", PROTOSS, "units"),
    ItemNames.PROGRESSIVE_PROTOSS_AIR_WEAPON: GENERIC_UPGRADE_TEMPLATE.format("damage", PROTOSS, "starships"),
    ItemNames.PROGRESSIVE_PROTOSS_AIR_ARMOR: GENERIC_UPGRADE_TEMPLATE.format("armor", PROTOSS, "starships"),
    ItemNames.PROGRESSIVE_PROTOSS_WEAPON_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage", PROTOSS, "units"),
    ItemNames.PROGRESSIVE_PROTOSS_ARMOR_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("armor", PROTOSS, "units"),
    ItemNames.PROGRESSIVE_PROTOSS_GROUND_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", PROTOSS, "ground units"),
    ItemNames.PROGRESSIVE_PROTOSS_AIR_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", PROTOSS, "starships"),
    ItemNames.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE: GENERIC_UPGRADE_TEMPLATE.format("damage and armor", PROTOSS, "units"),
    ItemNames.PHOTON_CANNON: "Protoss defensive structure. Can attack ground and air units.",
    ItemNames.KHAYDARIN_MONOLITH: "Advanced Protoss defensive structure. Has superior range and damage, but is very expensive and attacks slowly.",
    ItemNames.SHIELD_BATTERY: "Protoss defensive structure. Restores shields to nearby friendly units and structures.",
    ItemNames.SUPPLICANT_BLOOD_SHIELD: "Increases the armor value of Supplicant shields.",
    ItemNames.SUPPLICANT_SOUL_AUGMENTATION: "Increases Supplicant max shields by 25.",
    ItemNames.SUPPLICANT_SHIELD_REGENERATION: "Increases Supplicant shield regeneration rate.",
    ItemNames.ADEPT_SHOCKWAVE: "When Adepts deal a finishing blow, their projectiles can jump onto 2 additional targets.",
    ItemNames.ADEPT_RESONATING_GLAIVES: "Increases Adept attack speed.",
    ItemNames.ADEPT_PHASE_BULWARK: "Increases Adept shield maximum by 50.",
    ItemNames.STALKER_INSTIGATOR_SLAYER_DISINTEGRATING_PARTICLES: "Increases weapon damage of Stalkers, Instigators, and Slayers.",
    ItemNames.STALKER_INSTIGATOR_SLAYER_PARTICLE_REFLECTION: "Attacks fired by Stalkers, Instigators, and Slayers have a chance to bounce to additional targets for reduced damage.",
    ItemNames.DRAGOON_HIGH_IMPACT_PHASE_DISRUPTORS: "Dragoons deal increased damage.",
    ItemNames.DRAGOON_TRILLIC_COMPRESSION_SYSTEM: "Dragoons gain +20 life and their shield regeneration rate is doubled. Allows Dragoons to regenerate shields in combat.",
    ItemNames.DRAGOON_SINGULARITY_CHARGE: "Increases Dragoon range by 2.",
    ItemNames.DRAGOON_ENHANCED_STRIDER_SERVOS: "Increases Dragoon movement speed.",
    ItemNames.SCOUT_COMBAT_SENSOR_ARRAY: "Scouts gain +3 range against air and +1 range against ground.",
    ItemNames.SCOUT_APIAL_SENSORS: "Scouts gain increased sight range.",
    ItemNames.SCOUT_GRAVITIC_THRUSTERS: "Scouts gain increased movement speed.",
    ItemNames.SCOUT_ADVANCED_PHOTON_BLASTERS: "Scouts gain increased damage against ground targets.",
    ItemNames.TEMPEST_TECTONIC_DESTABILIZERS: "Tempests deal increased damage to buildings.",
    ItemNames.TEMPEST_QUANTIC_REACTOR: "Tempests deal increased damage to massive units.",
    ItemNames.TEMPEST_GRAVITY_SLING: "Tempests gain +8 range against air targets.",
    ItemNames.PHOENIX_MIRAGE_IONIC_WAVELENGTH_FLUX: "Increases Phoenix and Mirage weapon damage by 2.",
    ItemNames.PHOENIX_MIRAGE_ANION_PULSE_CRYSTALS: "Increases Phoenix and Mirage range by 2.",
    ItemNames.CORSAIR_STEALTH_DRIVE: "Corsairs become permanently cloaked.",
    ItemNames.CORSAIR_ARGUS_JEWEL: "Corsairs can store 2 charges of disruption web.",
    ItemNames.CORSAIR_SUSTAINING_DISRUPTION: "Corsair disruption webs last longer.",
    ItemNames.CORSAIR_NEUTRON_SHIELDS: "Increases corsair maximum shields by 20.",
    ItemNames.ORACLE_STEALTH_DRIVE: "Oracles become permanently cloaked.",
    ItemNames.ORACLE_STASIS_CALIBRATION: "Enemies caught by the Oracle's Stasis Ward may now be attacked.",
    ItemNames.ORACLE_TEMPORAL_ACCELERATION_BEAM: "Oracles no longer need to to spend energy to attack.",
    ItemNames.ARBITER_CHRONOSTATIC_REINFORCEMENT: "Arbiters gain +50 maximum life and +1 armor.",
    ItemNames.ARBITER_KHAYDARIN_CORE: "Arbiters gain +150 starting energy and +50 maximum energy.",
    ItemNames.ARBITER_SPACETIME_ANCHOR: "Arbiter Stasis Field lasts 50 seconds longer.",
    ItemNames.ARBITER_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.ARBITER),
    ItemNames.ARBITER_ENHANCED_CLOAK_FIELD: "Increases Arbiter Cloaking Field range.",
    ItemNames.CARRIER_GRAVITON_CATAPULT: "Carriers can launch Interceptors more quickly.",
    ItemNames.CARRIER_HULL_OF_PAST_GLORIES: "Carriers gain +2 armour.",
    ItemNames.VOID_RAY_DESTROYER_FLUX_VANES: "Increases Void Ray and Destroyer movement speed.",
    ItemNames.DESTROYER_REFORGED_BLOODSHARD_CORE: "When fully charged, the Destroyer's Destruction Beam weapon does full damage to secondary targets.",
    ItemNames.WARP_PRISM_GRAVITIC_DRIVE: "Increases the movement speed of Warp Prisms.",
    ItemNames.WARP_PRISM_PHASE_BLASTER: "Equips Warp Prisms with an auto-attack that can hit ground and air targets.",
    ItemNames.WARP_PRISM_WAR_CONFIGURATION: "Warp Prisms transform faster and gain increased power radius in Phasing Mode.",
    ItemNames.OBSERVER_GRAVITIC_BOOSTERS: "Increases Observer movement speed.",
    ItemNames.OBSERVER_SENSOR_ARRAY: "Increases Observer sight range.",
    ItemNames.REAVER_SCARAB_DAMAGE: "Reaver Scarabs deal +25 damage.",
    ItemNames.REAVER_SOLARITE_PAYLOAD: "Reaver Scarabs gain increased splash damage radius.",
    ItemNames.REAVER_REAVER_CAPACITY: "Reavers can store 10 Scarabs.",
    ItemNames.REAVER_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(ItemNames.REAVER),
    ItemNames.VANGUARD_AGONY_LAUNCHERS: "Increases Vanguard attack range by 2.",
    ItemNames.VANGUARD_MATTER_DISPERSION: "Increases Vanguard attack area.",
    ItemNames.IMMORTAL_ANNIHILATOR_SINGULARITY_CHARGE: "Increases Immortal and Annihilator attack range by 2.",
    ItemNames.IMMORTAL_ANNIHILATOR_ADVANCED_TARGETING_MECHANICS: "Immortals and Annihilators can attack air units.",
    ItemNames.COLOSSUS_PACIFICATION_PROTOCOL: "Increases Colossus attack speed.",
    ItemNames.WRATHWALKER_RAPID_POWER_CYCLING: "Reduces the charging time and increases attack speed of the Wrathwalker's Charged Blast.",
    ItemNames.WRATHWALKER_EYE_OF_WRATH: "Increases Wrathwalker weapon range by 1.",
    ItemNames.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_SHROUD_OF_ADUN: f"Increases {DISPLAY_NAME_CLOAKED_ASSASSIN} maximum shields by 80.",
    ItemNames.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_SHADOW_GUARD_TRAINING: f"Increases {DISPLAY_NAME_CLOAKED_ASSASSIN} maximum life by 40.",
    ItemNames.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_BLINK: "Dark Templar, Avengers, and Blood Hunters unlock Blink.",
    ItemNames.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_RESOURCE_EFFICIENCY: get_resource_efficiency_desc(DISPLAY_NAME_CLOAKED_ASSASSIN),
    ItemNames.DARK_TEMPLAR_DARK_ARCHON_MELD: "Allows 2 Dark Templar to meld into a Dark Archon.",
    ItemNames.HIGH_TEMPLAR_SIGNIFIER_UNSHACKLED_PSIONIC_STORM: "High Templar and Signifiers deal increased damage with Psi Storm.",
    ItemNames.HIGH_TEMPLAR_SIGNIFIER_HALLUCINATION: "High Templar and Signifiers gain the Hallucination ability.",
    ItemNames.HIGH_TEMPLAR_SIGNIFIER_KHAYDARIN_AMULET: "High Templar and Signifiers gain +150 starting energy and +50 maximum energy.",
    ItemNames.ARCHON_HIGH_ARCHON: "Archons can use High Templar abilities.",
    ItemNames.DARK_ARCHON_FEEDBACK: "Dark Archons gain the Feedback ability, which damages and removes energy on an enemy unit.",
    ItemNames.DARK_ARCHON_MAELSTROM: "Dark Archons gain the Maelstrom ability, which stuns biological units in an area.",
    ItemNames.DARK_ARCHON_ARGUS_TALISMAN: "Dark Archons gain +150 starting energy and +50 maximum energy.",
    ItemNames.ASCENDANT_POWER_OVERWHELMING: "Ascendants gain the ability to sacrifice Supplicants for increased shields and spell damage.",
    ItemNames.ASCENDANT_CHAOTIC_ATTUNEMENT: "Ascendants' Psionic Orbs gain 25% increased travel distance.",
    ItemNames.ASCENDANT_BLOOD_AMULET: "Ascendants gain +150 starting energy and +50 maximum energy.",
    ItemNames.SENTRY_ENERGIZER_HAVOC_CLOAKING_MODULE: "Sentries, Energizers, and Havocs become permanently cloaked.",
    ItemNames.SENTRY_ENERGIZER_HAVOC_SHIELD_BATTERY_RAPID_RECHARGING: "Sentries, Energizers, and Havocs gain 200% increased energy regeneration rate.",
    ItemNames.SENTRY_FORCE_FIELD: "Sentries gain the Force Field ability.",
    ItemNames.SENTRY_HALLUCINATION: "Sentries gain the Hallucination ability.",
    ItemNames.ENERGIZER_RECLAMATION: "Energizers gain the Reclamation ability.",
    ItemNames.ENERGIZER_FORGED_CHASSIS: "Increases Energizer Life by 20.",
    ItemNames.HAVOC_DETECT_WEAKNESS: "Havocs' Target Lock gives an additional 15% damage bonus.",
    ItemNames.HAVOC_BLOODSHARD_RESONANCE: "Havoc gain increased range for Squad Sight, Target Lock, and Force Field.",
    ItemNames.ZEALOT_SENTINEL_CENTURION_LEG_ENHANCEMENTS: "Zealots, Sentinels, and Centurions gain increased movement speed.",
    ItemNames.ZEALOT_SENTINEL_CENTURION_SHIELD_CAPACITY: "Zealots, Sentinels, and Centurions gain +30 maximum shields.",
    ItemNames.SOA_CHRONO_SURGE: "The Spear of Adun increases a target structure's unit warp in and research speeds by 1000% for 20 seconds.",
    ItemNames.SOA_PROGRESSIVE_PROXY_PYLON: inspect.cleandoc("""
        Level 1: The Spear of Adun quickly warps in a Pylon to a target location.
        Level 2: The Spear of Adun warps in a Pylon, 2 melee warriors, and 2 ranged warriors to a target location.
    """),
    ItemNames.SOA_PYLON_OVERCHARGE: "The Spear of Adun temporarily gives a target Pylon increased shields and a powerful attack.",
    ItemNames.SOA_ORBITAL_STRIKE: "The Spear of Adun fires 5 laser blasts from orbit.",
    ItemNames.SOA_TEMPORAL_FIELD: "The Spear of Adun creates 3 temporal fields that freeze enemy units and structures in time.",
    ItemNames.SOA_SOLAR_LANCE: "The Spear of Adun strafes a target area with 3 laser beams.",
    ItemNames.SOA_MASS_RECALL: "The Spear of Adun warps all units in a target area back to the primary Nexus and gives them a temporary shield.",
    ItemNames.SOA_SHIELD_OVERCHARGE: "The Spear of Adun gives all friendly units a shield that absorbs 200 damage. Lasts 20 seconds.",
    ItemNames.SOA_DEPLOY_FENIX: "The Spear of Adun drops Fenix onto the battlefield. Fenix is a powerful warrior who will fight for 30 seconds.",
    ItemNames.SOA_PURIFIER_BEAM: "The Spear of Adun fires a wide laser that deals large amounts of damage in a moveable area. Lasts 15 seconds.",
    ItemNames.SOA_TIME_STOP: "The Spear of Adun freezes all enemy units and structures in time for 20 seconds.",
    ItemNames.SOA_SOLAR_BOMBARDMENT: "The Spear of Adun fires 200 laser blasts randomly over a wide area.",
    ItemNames.MATRIX_OVERLOAD: "All friendly units gain 25% movement speed and 15% attack speed within a Pylon's power field and for 15 seconds after leaving it.",
    ItemNames.QUATRO: "All friendly Protoss units gain the equivalent of their +1 armour, attack, and shield upgrades.",
    ItemNames.NEXUS_OVERCHARGE: "The Protoss Nexus gains a long-range auto-attack.",
    ItemNames.ORBITAL_ASSIMILATORS: "Assimilators automatically harvest Vespene Gas without the need for Probes.",
    ItemNames.WARP_HARMONIZATION: "Stargates and Robotics Facilities can transform to utilize Warp In technology. Warp In cooldowns are 20% faster than original build times.",
    ItemNames.GUARDIAN_SHELL: "The Spear of Adun passively shields friendly Protoss units before death, making them invulnerable for 5 seconds. Each unit can only be shielded once every 60 seconds.",
    ItemNames.RECONSTRUCTION_BEAM: "The Spear of Adun will passively heal mechanical units for 5 and non-biological structures for 10 life per second. Up to 3 targets can be repaired at once.",
    ItemNames.OVERWATCH: "Once per second, the Spear of Adun will last-hit a damaged enemy unit that is below 50 health.",
    ItemNames.SUPERIOR_WARP_GATES: "Protoss Warp Gates can hold up to 3 charges of unit warp-ins.",
    ItemNames.ENHANCED_TARGETING: "Protoss defensive structures gain +2 range.",
    ItemNames.OPTIMIZED_ORDNANCE: "Increases the attack speed of Protoss defensive structures by 25%.",
    ItemNames.KHALAI_INGENUITY: "Pylons, Photon Cannons, Monoliths, and Shield Batteries warp in near-instantly.",
    ItemNames.AMPLIFIED_ASSIMILATORS: "Assimilators produce Vespene gas 25% faster.",
}
