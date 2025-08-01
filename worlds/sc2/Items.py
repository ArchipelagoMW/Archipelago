import inspect
from pydoc import describe

from BaseClasses import Item, ItemClassification, MultiWorld
import typing

from .Options import get_option_value, RequiredTactics
from .MissionTables import SC2Mission, SC2Race, SC2Campaign, campaign_mission_table
from . import ItemNames
from worlds.AutoWorld import World


class ItemData(typing.NamedTuple):
    code: int
    type: str
    number: int  # Important for bot commands to send the item into the game
    race: SC2Race
    classification: ItemClassification = ItemClassification.useful
    quantity: int = 1
    parent_item: typing.Optional[str] = None
    origin: typing.Set[str] = {"wol"}
    description: typing.Optional[str] = None
    important_for_filtering: bool = False

    def is_important_for_filtering(self):
        return self.important_for_filtering \
            or self.classification == ItemClassification.progression \
            or self.classification == ItemClassification.progression_skip_balancing


class StarcraftItem(Item):
    game: str = "Starcraft 2"


def get_full_item_list():
    return item_table


SC2WOL_ITEM_ID_OFFSET = 1000
SC2HOTS_ITEM_ID_OFFSET = SC2WOL_ITEM_ID_OFFSET + 1000
SC2LOTV_ITEM_ID_OFFSET = SC2HOTS_ITEM_ID_OFFSET + 1000

# Descriptions
WEAPON_ARMOR_UPGRADE_NOTE = inspect.cleandoc("""
    Must be researched during the mission if the mission type isn't set to auto-unlock generic upgrades.
""")
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
RESOURCE_EFFICIENCY_DESCRIPTION_TEMPLATE = "Reduces {} resource and supply cost."
RESOURCE_EFFICIENCY_NO_SUPPLY_DESCRIPTION_TEMPLATE = "Reduces {} resource cost."
CLOAK_DESCRIPTION_TEMPLATE = "Allows {} to use the Cloak ability."


# The items are sorted by their IDs. The IDs shall be kept for compatibility with older games.
item_table = {
    # WoL
    ItemNames.MARINE:
        ItemData(0 + SC2WOL_ITEM_ID_OFFSET, "Unit", 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="General-purpose infantry."),
    ItemNames.MEDIC:
        ItemData(1 + SC2WOL_ITEM_ID_OFFSET, "Unit", 1, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Support trooper. Heals nearby biological units."),
    ItemNames.FIREBAT:
        ItemData(2 + SC2WOL_ITEM_ID_OFFSET, "Unit", 2, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Specialized anti-infantry attacker."),
    ItemNames.MARAUDER:
        ItemData(3 + SC2WOL_ITEM_ID_OFFSET, "Unit", 3, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Heavy assault infantry."),
    ItemNames.REAPER:
        ItemData(4 + SC2WOL_ITEM_ID_OFFSET, "Unit", 4, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Raider. Capable of jumping up and down cliffs. Throws explosive mines."),
    ItemNames.HELLION:
        ItemData(5 + SC2WOL_ITEM_ID_OFFSET, "Unit", 5, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Fast scout. Has a flame attack that damages all enemy units in its line of fire."),
    ItemNames.VULTURE:
        ItemData(6 + SC2WOL_ITEM_ID_OFFSET, "Unit", 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Fast skirmish unit. Can use the Spider Mine ability."),
    ItemNames.GOLIATH:
        ItemData(7 + SC2WOL_ITEM_ID_OFFSET, "Unit", 7, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Heavy-fire support unit."),
    ItemNames.DIAMONDBACK:
        ItemData(8 + SC2WOL_ITEM_ID_OFFSET, "Unit", 8, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Fast, high-damage hovertank. Rail Gun can fire while the Diamondback is moving."),
    ItemNames.SIEGE_TANK:
        ItemData(9 + SC2WOL_ITEM_ID_OFFSET, "Unit", 9, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Heavy tank. Long-range artillery in Siege Mode."),
    ItemNames.MEDIVAC:
        ItemData(10 + SC2WOL_ITEM_ID_OFFSET, "Unit", 10, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Air transport. Heals nearby biological units."),
    ItemNames.WRAITH:
        ItemData(11 + SC2WOL_ITEM_ID_OFFSET, "Unit", 11, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Highly mobile flying unit. Excellent at surgical strikes."),
    ItemNames.VIKING:
        ItemData(12 + SC2WOL_ITEM_ID_OFFSET, "Unit", 12, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description=inspect.cleandoc(
                     """
                     Durable support flyer. Loaded with strong anti-capital air missiles. 
                     Can switch into Assault Mode to attack ground units.
                     """
                 )),
    ItemNames.BANSHEE:
        ItemData(13 + SC2WOL_ITEM_ID_OFFSET, "Unit", 13, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Tactical-strike aircraft."),
    ItemNames.BATTLECRUISER:
        ItemData(14 + SC2WOL_ITEM_ID_OFFSET, "Unit", 14, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Powerful warship."),
    ItemNames.GHOST:
        ItemData(15 + SC2WOL_ITEM_ID_OFFSET, "Unit", 15, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description=inspect.cleandoc(
                     """
                     Infiltration unit. Can use Snipe and Cloak abilities. Can also call down Tactical Nukes.
                     """
                 )),
    ItemNames.SPECTRE:
        ItemData(16 + SC2WOL_ITEM_ID_OFFSET, "Unit", 16, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description=inspect.cleandoc(
                     """
                     Infiltration unit. Can use Ultrasonic Pulse, Psionic Lash, and Cloak. 
                     Can also call down Tactical Nukes.
                     """
                 )),
    ItemNames.THOR:
        ItemData(17 + SC2WOL_ITEM_ID_OFFSET, "Unit", 17, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Heavy assault mech."),
    # EE units
    ItemNames.LIBERATOR:
        ItemData(18 + SC2WOL_ITEM_ID_OFFSET, "Unit", 18, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"nco", "ext"},
                 description=inspect.cleandoc(
                     """
                     Artillery fighter. Loaded with missiles that deal area damage to enemy air targets. 
                     Can switch into Defender Mode to provide siege support.
                     """
                 )),
    ItemNames.VALKYRIE:
        ItemData(19 + SC2WOL_ITEM_ID_OFFSET, "Unit", 19, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"bw"},
                 description=inspect.cleandoc(
                     """
                     Advanced anti-aircraft fighter. 
                     Able to use cluster missiles that deal area damage to air targets.
                     """
                 )),
    ItemNames.WIDOW_MINE:
        ItemData(20 + SC2WOL_ITEM_ID_OFFSET, "Unit", 20, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"ext"},
                 description=inspect.cleandoc(
                     """
                     Robotic mine. Launches missiles at nearby enemy units while burrowed. 
                     Attacks deal splash damage in a small area around the target. 
                     Widow Mine is revealed when Sentinel Missile is on cooldown.
                     """
                 )),
    ItemNames.CYCLONE:
        ItemData(21 + SC2WOL_ITEM_ID_OFFSET, "Unit", 21, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"ext"},
                 description=inspect.cleandoc(
                     """
                     Mobile assault vehicle. Can use Lock On to quickly fire while moving.
                     """
                 )),
    ItemNames.HERC:
        ItemData(22 + SC2WOL_ITEM_ID_OFFSET, "Unit", 26, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"ext"},
                 description=inspect.cleandoc(
                     """
                     Front-line infantry. Can use Grapple.
                     """
                 )),
    ItemNames.WARHOUND:
        ItemData(23 + SC2WOL_ITEM_ID_OFFSET, "Unit", 27, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"ext"},
                 description=inspect.cleandoc(
                     """
                     Anti-vehicle mech. Haywire missiles do bonus damage to mechanical units.
                     """
                 )),

    # Some other items are moved to Upgrade group because of the way how the bot message is parsed
    ItemNames.PROGRESSIVE_TERRAN_INFANTRY_WEAPON:
        ItemData(100 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 0, SC2Race.TERRAN,
                 quantity=3,
                 description=inspect.cleandoc(
                     f"""
                     Increases damage of Terran infantry units. 
                     {WEAPON_ARMOR_UPGRADE_NOTE}
                     """
                 )),
    ItemNames.PROGRESSIVE_TERRAN_INFANTRY_ARMOR:
        ItemData(102 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 2, SC2Race.TERRAN,
                 quantity=3,
                 description=inspect.cleandoc(
                     f"""
                     Increases armor of Terran infantry units. 
                     {WEAPON_ARMOR_UPGRADE_NOTE}
                     """
                 )),
    ItemNames.PROGRESSIVE_TERRAN_VEHICLE_WEAPON:
        ItemData(103 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 4, SC2Race.TERRAN,
                 quantity=3,
                 description=inspect.cleandoc(
                     f"""
                     Increases damage of Terran vehicle units. 
                     {WEAPON_ARMOR_UPGRADE_NOTE}
                     """
                 )),
    ItemNames.PROGRESSIVE_TERRAN_VEHICLE_ARMOR:
        ItemData(104 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 6, SC2Race.TERRAN,
                 quantity=3,
                 description=inspect.cleandoc(
                     f"""
                     Increases armor of Terran vehicle units. 
                     {WEAPON_ARMOR_UPGRADE_NOTE}
                     """
                 )),
    ItemNames.PROGRESSIVE_TERRAN_SHIP_WEAPON:
        ItemData(105 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 8, SC2Race.TERRAN,
                 quantity=3,
                 description=inspect.cleandoc(
                     f"""
                     Increases damage of Terran starship units. 
                     {WEAPON_ARMOR_UPGRADE_NOTE}
                     """
                 )),
    ItemNames.PROGRESSIVE_TERRAN_SHIP_ARMOR:
        ItemData(106 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 10, SC2Race.TERRAN,
                 quantity=3,
                 description=inspect.cleandoc(
                     f"""
                     Increases armor of Terran starship units. 
                     {WEAPON_ARMOR_UPGRADE_NOTE}
                     """
                 )),
    # Upgrade bundle 'number' values are used as indices to get affected 'number's
    ItemNames.PROGRESSIVE_TERRAN_WEAPON_UPGRADE: ItemData(107 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 0, SC2Race.TERRAN, quantity=3),
    ItemNames.PROGRESSIVE_TERRAN_ARMOR_UPGRADE: ItemData(108 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 1, SC2Race.TERRAN, quantity=3),
    ItemNames.PROGRESSIVE_TERRAN_INFANTRY_UPGRADE: ItemData(109 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 2, SC2Race.TERRAN, quantity=3),
    ItemNames.PROGRESSIVE_TERRAN_VEHICLE_UPGRADE: ItemData(110 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 3, SC2Race.TERRAN, quantity=3),
    ItemNames.PROGRESSIVE_TERRAN_SHIP_UPGRADE: ItemData(111 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 4, SC2Race.TERRAN, quantity=3),
    ItemNames.PROGRESSIVE_TERRAN_WEAPON_ARMOR_UPGRADE: ItemData(112 + SC2WOL_ITEM_ID_OFFSET, "Upgrade", 5, SC2Race.TERRAN, quantity=3),

    # Unit and structure upgrades
    ItemNames.BUNKER_PROJECTILE_ACCELERATOR:
        ItemData(200 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 0, SC2Race.TERRAN,
                 parent_item=ItemNames.BUNKER,
                 description="Increases range of all units in the Bunker by 1."),
    ItemNames.BUNKER_NEOSTEEL_BUNKER:
        ItemData(201 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 1, SC2Race.TERRAN,
                 parent_item=ItemNames.BUNKER,
                 description="Increases the number of Bunker slots by 2."),
    ItemNames.MISSILE_TURRET_TITANIUM_HOUSING:
        ItemData(202 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 2, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MISSILE_TURRET,
                 description="Increases Missile Turret life by 75."),
    ItemNames.MISSILE_TURRET_HELLSTORM_BATTERIES:
        ItemData(203 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 3, SC2Race.TERRAN,
                 parent_item=ItemNames.MISSILE_TURRET,
                 description="The Missile Turret unleashes an additional flurry of missiles with each attack."),
    ItemNames.SCV_ADVANCED_CONSTRUCTION:
        ItemData(204 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 4, SC2Race.TERRAN,
                 description="Multiple SCVs can construct a structure, reducing its construction time."),
    ItemNames.SCV_DUAL_FUSION_WELDERS:
        ItemData(205 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 5, SC2Race.TERRAN,
                 description="SCVs repair twice as fast."),
    ItemNames.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM:
        ItemData(206 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 24, SC2Race.TERRAN,
                 quantity=2,
                 description=inspect.cleandoc(
                     """
                     Level 1: While on low health, Terran structures are repaired to half health instead of burning down.
                     Level 2: Terran structures are repaired to full health instead of half health
                     """
                 )),
    ItemNames.PROGRESSIVE_ORBITAL_COMMAND:
        ItemData(207 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 26, SC2Race.TERRAN,
                 quantity=2, classification=ItemClassification.progression,
                 description=inspect.cleandoc(
                     """
                     Level 1: Allows Command Centers to use Scanner Sweep and Calldown: MULE abilities.
                     Level 2: Orbital Command abilities work even in Planetary Fortress mode.
                     """
                 )),
    ItemNames.MARINE_PROGRESSIVE_STIMPACK:
        ItemData(208 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.MARINE, quantity=2,
                 description=STIMPACK_SMALL_DESCRIPTION),
    ItemNames.MARINE_COMBAT_SHIELD:
        ItemData(209 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 9, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.MARINE,
                 description="Increases Marine life by 10."),
    ItemNames.MEDIC_ADVANCED_MEDIC_FACILITIES:
        ItemData(210 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 10, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIC,
                 description=INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Medics", "Barracks")),
    ItemNames.MEDIC_STABILIZER_MEDPACKS:
        ItemData(211 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 11, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.MEDIC,
                 description="Increases Medic heal speed. Reduces the amount of energy required for each heal."),
    ItemNames.FIREBAT_INCINERATOR_GAUNTLETS:
        ItemData(212 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 12, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.FIREBAT,
                 description="Increases Firebat's damage radius by 40%"),
    ItemNames.FIREBAT_JUGGERNAUT_PLATING:
        ItemData(213 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 13, SC2Race.TERRAN,
                 parent_item=ItemNames.FIREBAT,
                 description="Increases Firebat's armor by 2."),
    ItemNames.MARAUDER_CONCUSSIVE_SHELLS:
        ItemData(214 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 14, SC2Race.TERRAN,
                 parent_item=ItemNames.MARAUDER,
                 description="Marauder attack temporarily slows all units in target area."),
    ItemNames.MARAUDER_KINETIC_FOAM:
        ItemData(215 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 15, SC2Race.TERRAN,
                 parent_item=ItemNames.MARAUDER,
                 description="Increases Marauder life by 25."),
    ItemNames.REAPER_U238_ROUNDS:
        ItemData(216 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 16, SC2Race.TERRAN,
                 parent_item=ItemNames.REAPER,
                 description=inspect.cleandoc(
                     """
                     Increases Reaper pistol attack range by 1.
                     Reaper pistols do additional 3 damage to Light Armor.
                     """
                 )),
    ItemNames.REAPER_G4_CLUSTERBOMB:
        ItemData(217 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 17, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.REAPER,
                 description="Timed explosive that does heavy area damage."),
    ItemNames.CYCLONE_MAG_FIELD_ACCELERATORS:
        ItemData(218 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 18, SC2Race.TERRAN,
                 parent_item=ItemNames.CYCLONE, origin={"ext"},
                 description="Increases Cyclone Lock On damage"),
    ItemNames.CYCLONE_MAG_FIELD_LAUNCHERS:
        ItemData(219 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 19, SC2Race.TERRAN,
                 parent_item=ItemNames.CYCLONE, origin={"ext"},
                 description="Increases Cyclone attack range by 2."),
    ItemNames.MARINE_LASER_TARGETING_SYSTEM:
        ItemData(220 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 8, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MARINE, origin={"nco"},
                 description=LASER_TARGETING_SYSTEMS_DESCRIPTION),
    ItemNames.MARINE_MAGRAIL_MUNITIONS:
        ItemData(221 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 20, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.MARINE, origin={"nco"},
                 description="Deals 20 damage to target unit. Autocast on attack with a cooldown."),
    ItemNames.MARINE_OPTIMIZED_LOGISTICS:
        ItemData(222 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 21, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MARINE, origin={"nco"},
                 description="Increases Marine training speed."),
    ItemNames.MEDIC_RESTORATION:
        ItemData(223 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 22, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIC, origin={"bw"},
                 description="Removes negative status effects from target allied unit."),
    ItemNames.MEDIC_OPTICAL_FLARE:
        ItemData(224 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 23, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIC, origin={"bw"},
                 description="Reduces vision range of target enemy unit. Disables detection."),
    ItemNames.MEDIC_RESOURCE_EFFICIENCY:
        ItemData(225 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 24, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIC, origin={"bw"},
                 description=RESOURCE_EFFICIENCY_DESCRIPTION_TEMPLATE.format("Medic")),
    ItemNames.FIREBAT_PROGRESSIVE_STIMPACK:
        ItemData(226 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 6, SC2Race.TERRAN,
                 parent_item=ItemNames.FIREBAT, quantity=2, origin={"bw"},
                 description=STIMPACK_LARGE_DESCRIPTION),
    ItemNames.FIREBAT_RESOURCE_EFFICIENCY:
        ItemData(227 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 25, SC2Race.TERRAN,
                 parent_item=ItemNames.FIREBAT, origin={"bw"},
                 description=RESOURCE_EFFICIENCY_DESCRIPTION_TEMPLATE.format("Firebat")),
    ItemNames.MARAUDER_PROGRESSIVE_STIMPACK:
        ItemData(228 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 8, SC2Race.TERRAN,
                 parent_item=ItemNames.MARAUDER, quantity=2, origin={"nco"},
                 description=STIMPACK_LARGE_DESCRIPTION),
    ItemNames.MARAUDER_LASER_TARGETING_SYSTEM:
        ItemData(229 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 26, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MARAUDER, origin={"nco"},
                 description=LASER_TARGETING_SYSTEMS_DESCRIPTION),
    ItemNames.MARAUDER_MAGRAIL_MUNITIONS:
        ItemData(230 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 27, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MARAUDER, origin={"nco"},
                 description="Deals 20 damage to target unit. Autocast on attack with a cooldown."),
    ItemNames.MARAUDER_INTERNAL_TECH_MODULE:
        ItemData(231 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 28, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MARAUDER, origin={"nco"},
                 description=INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Marauders", "Barracks")),
    ItemNames.SCV_HOSTILE_ENVIRONMENT_ADAPTATION:
        ItemData(232 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 29, SC2Race.TERRAN,
                 classification=ItemClassification.filler, origin={"bw"},
                 description="Increases SCV life by 15 and attack speed slightly."),
    ItemNames.MEDIC_ADAPTIVE_MEDPACKS:
        ItemData(233 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.MEDIC, origin={"ext"},
                 description="Allows Medics to heal mechanical and air units."),
    ItemNames.MEDIC_NANO_PROJECTOR:
        ItemData(234 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 1, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIC, origin={"ext"},
                 description="Increases Medic heal range by 2."),
    ItemNames.FIREBAT_INFERNAL_PRE_IGNITER:
        ItemData(235 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 2, SC2Race.TERRAN,
                 parent_item=ItemNames.FIREBAT, origin={"bw"},
                 description="Firebats do an additional 4 damage to Light Armor."),
    ItemNames.FIREBAT_KINETIC_FOAM:
        ItemData(236 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 3, SC2Race.TERRAN,
                 parent_item=ItemNames.FIREBAT, origin={"ext"},
                 description="Increases Firebat life by 100."),
    ItemNames.FIREBAT_NANO_PROJECTORS:
        ItemData(237 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 4, SC2Race.TERRAN,
                 parent_item=ItemNames.FIREBAT, origin={"ext"},
                 description="Increases Firebat attack range by 2"),
    ItemNames.MARAUDER_JUGGERNAUT_PLATING:
        ItemData(238 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 5, SC2Race.TERRAN,
                 parent_item=ItemNames.MARAUDER, origin={"ext"},
                 description="Increases Marauder's armor by 2."),
    ItemNames.REAPER_JET_PACK_OVERDRIVE:
        ItemData(239 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 6, SC2Race.TERRAN,
                 parent_item=ItemNames.REAPER, origin={"ext"},
                 description=inspect.cleandoc(
                     """
                     Allows the Reaper to fly for 10 seconds.
                     While flying, the Reaper can attack air units.
                     """
                 )),
    ItemNames.HELLION_INFERNAL_PLATING:
        ItemData(240 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 7, SC2Race.TERRAN,
                 parent_item=ItemNames.HELLION, origin={"ext"},
                 description="Increases Hellion and Hellbat armor by 2."),
    ItemNames.VULTURE_AUTO_REPAIR:
        ItemData(241 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 8, SC2Race.TERRAN,
                 parent_item=ItemNames.VULTURE, origin={"ext"},
                 description="Vultures regenerate life."),
    ItemNames.GOLIATH_SHAPED_HULL:
        ItemData(242 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 9, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.GOLIATH, origin={"nco", "ext"},
                 description="Increases Goliath life by 25."),
    ItemNames.GOLIATH_RESOURCE_EFFICIENCY:
        ItemData(243 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 10, SC2Race.TERRAN,
                 parent_item=ItemNames.GOLIATH, origin={"nco", "bw"},
                 description=RESOURCE_EFFICIENCY_DESCRIPTION_TEMPLATE.format("Goliath")),
    ItemNames.GOLIATH_INTERNAL_TECH_MODULE:
        ItemData(244 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 11, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.GOLIATH, origin={"nco", "bw"},
                 description=INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Goliaths", "Factory")),
    ItemNames.SIEGE_TANK_SHAPED_HULL:
        ItemData(245 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 12, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.SIEGE_TANK, origin={"nco", "ext"},
                 description="Increases Siege Tank life by 25."),
    ItemNames.SIEGE_TANK_RESOURCE_EFFICIENCY:
        ItemData(246 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 13, SC2Race.TERRAN,
                 parent_item=ItemNames.SIEGE_TANK, origin={"bw"},
                 description=RESOURCE_EFFICIENCY_DESCRIPTION_TEMPLATE.format("Siege Tank")),
    ItemNames.PREDATOR_CLOAK:
        ItemData(247 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 14, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.PREDATOR, origin={"ext"},
                 description=CLOAK_DESCRIPTION_TEMPLATE.format("Predators")),
    ItemNames.PREDATOR_CHARGE:
        ItemData(248 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 15, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.PREDATOR, origin={"ext"},
                 description="Allows Predators to intercept enemy ground units."),
    ItemNames.MEDIVAC_SCATTER_VEIL:
        ItemData(249 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 16, SC2Race.TERRAN,
                 parent_item=ItemNames.MEDIVAC, origin={"ext"},
                 description="Medivacs get 100 shields."),
    ItemNames.REAPER_PROGRESSIVE_STIMPACK:
        ItemData(250 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 10, SC2Race.TERRAN,
                 parent_item=ItemNames.REAPER, quantity=2, origin={"nco"},
                 description=STIMPACK_SMALL_DESCRIPTION),
    ItemNames.REAPER_LASER_TARGETING_SYSTEM:
        ItemData(251 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 17, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.REAPER, origin={"nco"},
                 description=LASER_TARGETING_SYSTEMS_DESCRIPTION),
    ItemNames.REAPER_ADVANCED_CLOAKING_FIELD:
        ItemData(252 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 18, SC2Race.TERRAN,
                 parent_item=ItemNames.REAPER, origin={"nco"},
                 description="Reapers are permanently cloaked."),
    ItemNames.REAPER_SPIDER_MINES:
        ItemData(253 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 19, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.REAPER, origin={"nco"},
                 important_for_filtering=True,
                 description="Allows Reapers to lay Spider Mines. 3 charges per Reaper."),
    ItemNames.REAPER_COMBAT_DRUGS:
        ItemData(254 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 20, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.REAPER, origin={"ext"},
                 description="Reapers regenerate life while out of combat."),
    ItemNames.HELLION_HELLBAT_ASPECT:
        ItemData(255 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 21, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.HELLION, origin={"nco"},
                 description="Allows Hellions to transform into Hellbats."),
    ItemNames.HELLION_SMART_SERVOS:
        ItemData(256 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 22, SC2Race.TERRAN,
                 parent_item=ItemNames.HELLION, origin={"nco"},
                 description="Transforms faster between modes. Hellions can attack while moving."),
    ItemNames.HELLION_OPTIMIZED_LOGISTICS:
        ItemData(257 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 23, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.HELLION, origin={"nco"},
                 description="Increases Hellion training speed."),
    ItemNames.HELLION_JUMP_JETS:
        ItemData(258 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 24, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.HELLION, origin={"nco"},
                 description=inspect.cleandoc(
                     """
                     Increases movement speed in Hellion mode.
                     In Hellbat mode, launches the Hellbat toward enemy ground units and briefly stuns them.
                     """
                 )),
    ItemNames.HELLION_PROGRESSIVE_STIMPACK:
        ItemData(259 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 12, SC2Race.TERRAN,
                 parent_item=ItemNames.HELLION, quantity=2, origin={"nco"},
                 description=STIMPACK_LARGE_DESCRIPTION),
    ItemNames.VULTURE_ION_THRUSTERS:
        ItemData(260 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 25, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.VULTURE, origin={"bw"},
                 description="Increases Vulture movement speed."),
    ItemNames.VULTURE_AUTO_LAUNCHERS:
        ItemData(261 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 26, SC2Race.TERRAN,
                 parent_item=ItemNames.VULTURE, origin={"bw"},
                 description="Allows Vultures to attack while moving."),
    ItemNames.SPIDER_MINE_HIGH_EXPLOSIVE_MUNITION:
        ItemData(262 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 27, SC2Race.TERRAN,
                 origin={"bw"},
                 description="Increases Spider mine damage."),
    ItemNames.GOLIATH_JUMP_JETS:
        ItemData(263 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 28, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.GOLIATH, origin={"nco"},
                 description="Allows Goliaths to jump up and down cliffs."),
    ItemNames.GOLIATH_OPTIMIZED_LOGISTICS:
        ItemData(264 + SC2WOL_ITEM_ID_OFFSET, "Armory 2", 29, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.GOLIATH, origin={"nco"},
                 description="Increases Goliath training speed."),
    ItemNames.DIAMONDBACK_HYPERFLUXOR:
        ItemData(265 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 0, SC2Race.TERRAN,
                 parent_item=ItemNames.DIAMONDBACK, origin={"ext"},
                 description="Increases Diamondback attack speed."),
    ItemNames.DIAMONDBACK_BURST_CAPACITORS:
        ItemData(266 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 1, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.DIAMONDBACK, origin={"ext"},
                 description=inspect.cleandoc(
                     """
                     While not attacking, the Diamondback charges its weapon. 
                     The next attack does 10 additional damage.
                     """
                 )),
    ItemNames.DIAMONDBACK_RESOURCE_EFFICIENCY:
        ItemData(267 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 2, SC2Race.TERRAN,
                 parent_item=ItemNames.DIAMONDBACK, origin={"ext"},
                 description=RESOURCE_EFFICIENCY_DESCRIPTION_TEMPLATE.format("Diamondback")),
    ItemNames.SIEGE_TANK_JUMP_JETS:
        ItemData(268 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 3, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.SIEGE_TANK, origin={"nco"},
                 description=inspect.cleandoc(
                     """
                     Repositions Siege Tank to a target location. 
                     Can be used in either mode and to jump up and down cliffs. 
                     """
                 )),
    ItemNames.SIEGE_TANK_SPIDER_MINES:
        ItemData(269 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 4, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.SIEGE_TANK, origin={"nco"},
                 important_for_filtering=True,
                 description=inspect.cleandoc(
                     """
                     Allows Siege Tanks to lay Spider Mines. 
                     Lays 3 Spider Mines at once. 3 charges
                     """
                 )),
    ItemNames.SIEGE_TANK_SMART_SERVOS:
        ItemData(270 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 5, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.SIEGE_TANK, origin={"nco"},
                 description=SMART_SERVOS_DESCRIPTION),
    ItemNames.SIEGE_TANK_GRADUATING_RANGE:
        ItemData(271 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.SIEGE_TANK, origin={"ext"},
                 description=inspect.cleandoc(
                     """
                     Increases the Siege Tank's attack range by 1 every 3 seconds while in Siege Mode, 
                     up to a maximum of 5 additional range.
                     """
                 )),
    ItemNames.SIEGE_TANK_LASER_TARGETING_SYSTEM:
        ItemData(272 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 7, SC2Race.TERRAN,
                 parent_item=ItemNames.SIEGE_TANK, origin={"nco"},
                 description=LASER_TARGETING_SYSTEMS_DESCRIPTION),
    ItemNames.SIEGE_TANK_ADVANCED_SIEGE_TECH:
        ItemData(273 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 8, SC2Race.TERRAN,
                 parent_item=ItemNames.SIEGE_TANK, origin={"ext"},
                 description="Siege Tanks gain +3 armor in Siege Mode."),
    ItemNames.SIEGE_TANK_INTERNAL_TECH_MODULE:
        ItemData(274 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 9, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.SIEGE_TANK, origin={"nco"},
                 description=INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Siege Tanks", "Factory")),
    ItemNames.PREDATOR_RESOURCE_EFFICIENCY:
        ItemData(275 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 10, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.PREDATOR, origin={"ext"},
                 description="Decreases Predator resource and supply cost."),
    ItemNames.MEDIVAC_EXPANDED_HULL:
        ItemData(276 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 11, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIVAC, origin={"ext"},
                 description="Increases Medivac cargo space by 4."),
    ItemNames.MEDIVAC_AFTERBURNERS:
        ItemData(277 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 12, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIVAC, origin={"ext"},
                 description="Ability. Temporarily increases the Medivac's movement speed by 70%."),
    ItemNames.WRAITH_ADVANCED_LASER_TECHNOLOGY:
        ItemData(278 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 13, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.WRAITH, origin={"ext"},
                 description=inspect.cleandoc(
                     """
                     Burst Lasers do more damage and can hit both ground and air targets.
                     Replaces Gemini Missiles weapon.
                     """
                 )),
    ItemNames.VIKING_SMART_SERVOS:
        ItemData(279 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 14, SC2Race.TERRAN,
                 parent_item=ItemNames.VIKING, origin={"ext"},
                 description=SMART_SERVOS_DESCRIPTION),
    ItemNames.VIKING_ANTI_MECHANICAL_MUNITION:
        ItemData(280 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 15, SC2Race.TERRAN,
                 parent_item=ItemNames.VIKING, origin={"ext"},
                 description="Increases Viking damage to mechanical units while in Assault Mode."),
    ItemNames.DIAMONDBACK_ION_THRUSTERS:
        ItemData(281 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 21, SC2Race.TERRAN,
                 parent_item=ItemNames.DIAMONDBACK, origin={"ext"},
                 description="Increases Diamondback movement speed."),
    ItemNames.WARHOUND_RESOURCE_EFFICIENCY:
        ItemData(282 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 13, SC2Race.TERRAN,
                 parent_item=ItemNames.WARHOUND, origin={"ext"},
                 description=RESOURCE_EFFICIENCY_NO_SUPPLY_DESCRIPTION_TEMPLATE.format("Warhound")),
    ItemNames.WARHOUND_REINFORCED_PLATING:
        ItemData(283 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 14, SC2Race.TERRAN,
                 parent_item=ItemNames.WARHOUND, origin={"ext"},
                 description="Increases Warhound armor by 2."),
    ItemNames.HERC_RESOURCE_EFFICIENCY:
        ItemData(284 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 15, SC2Race.TERRAN,
                 parent_item=ItemNames.HERC, origin={"ext"},
                 description=RESOURCE_EFFICIENCY_DESCRIPTION_TEMPLATE.format("HERC")),
    ItemNames.HERC_JUGGERNAUT_PLATING:
        ItemData(285 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 16, SC2Race.TERRAN,
                 parent_item=ItemNames.HERC, origin={"ext"},
                 description="Increases HERC armor by 2."),
    ItemNames.HERC_KINETIC_FOAM:
        ItemData(286 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 17, SC2Race.TERRAN,
                 parent_item=ItemNames.HERC, origin={"ext"},
                 description="Increases HERC life by 50."),

    ItemNames.HELLION_TWIN_LINKED_FLAMETHROWER:
        ItemData(300 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 16, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.HELLION,
                 description="Doubles the width of the Hellion's flame attack."),
    ItemNames.HELLION_THERMITE_FILAMENTS:
        ItemData(301 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 17, SC2Race.TERRAN,
                 parent_item=ItemNames.HELLION,
                 description="Hellions do an additional 10 damage to Light Armor."),
    ItemNames.SPIDER_MINE_CERBERUS_MINE:
        ItemData(302 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 18, SC2Race.TERRAN,
                 classification=ItemClassification.filler,
                 description="Increases trigger and blast radius of Spider Mines."),
    ItemNames.VULTURE_PROGRESSIVE_REPLENISHABLE_MAGAZINE:
        ItemData(303 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 16, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.VULTURE, quantity=2,
                 description=inspect.cleandoc(
                     """
                     Level 1: Allows Vultures to replace used Spider Mines. Costs 15 minerals.
                     Level 2: Replacing used Spider Mines no longer costs minerals.
                     """
                 )),
    ItemNames.GOLIATH_MULTI_LOCK_WEAPONS_SYSTEM:
        ItemData(304 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 19, SC2Race.TERRAN,
                 parent_item=ItemNames.GOLIATH,
                 description="Goliaths can attack both ground and air targets simultaneously."),
    ItemNames.GOLIATH_ARES_CLASS_TARGETING_SYSTEM:
        ItemData(305 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 20, SC2Race.TERRAN,
                 parent_item=ItemNames.GOLIATH,
                 description="Increases Goliath ground attack range by 1 and air by 3."),
    ItemNames.DIAMONDBACK_PROGRESSIVE_TRI_LITHIUM_POWER_CELL:
        ItemData(306 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade 2", 4, SC2Race.TERRAN,
                 parent_item=ItemNames.DIAMONDBACK, quantity=2,
                 description=inspect.cleandoc(
                     """
                     Level 1: Tri-Lithium Power Cell: Increases Diamondback attack range by 1.
                     Level 2: Tungsten Spikes: Increases Diamondback attack range by 3.
                     """
                 )),
    ItemNames.DIAMONDBACK_SHAPED_HULL:
        ItemData(307 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 22, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.DIAMONDBACK,
                 description="Increases Diamondback life by 50."),
    ItemNames.SIEGE_TANK_MAELSTROM_ROUNDS:
        ItemData(308 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 23, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.SIEGE_TANK,
                 description="Siege Tanks do an additional 40 damage to the primary target in Siege Mode."),
    ItemNames.SIEGE_TANK_SHAPED_BLAST:
        ItemData(309 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 24, SC2Race.TERRAN,
                 parent_item=ItemNames.SIEGE_TANK,
                 description="Reduces splash damage to friendly targets while in Siege Mode by 75%."),
    ItemNames.MEDIVAC_RAPID_DEPLOYMENT_TUBE:
        ItemData(310 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 25, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIVAC,
                 description="Medivacs deploy loaded troops almost instantly."),
    ItemNames.MEDIVAC_ADVANCED_HEALING_AI:
        ItemData(311 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 26, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.MEDIVAC,
                 description="Medivacs can heal two targets at once."),
    ItemNames.WRAITH_PROGRESSIVE_TOMAHAWK_POWER_CELLS:
        ItemData(312 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 18, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.WRAITH, quantity=2,
                 description=inspect.cleandoc(
                     """
                     Level 1: Tomahawk Power Cells: Increases Wraith starting energy by 100.
                     Level 2: Unregistered Cloaking Module: Wraiths do not require energy to cloak and remain cloaked.
                     """
                 )),
    ItemNames.WRAITH_DISPLACEMENT_FIELD:
        ItemData(313 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 27, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.WRAITH,
                 description="Wraiths evade 20% of incoming attacks while cloaked."),
    ItemNames.VIKING_RIPWAVE_MISSILES:
        ItemData(314 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 28, SC2Race.TERRAN,
                 parent_item=ItemNames.VIKING,
                 description="Vikings do area damage while in Fighter Mode"),
    ItemNames.VIKING_PHOBOS_CLASS_WEAPONS_SYSTEM:
        ItemData(315 + SC2WOL_ITEM_ID_OFFSET, "Armory 3", 29, SC2Race.TERRAN,
                 parent_item=ItemNames.VIKING,
                 description="Increases Viking attack range by 1 in Assault mode and 2 in Fighter mode."),
    ItemNames.BANSHEE_PROGRESSIVE_CROSS_SPECTRUM_DAMPENERS:
        ItemData(316 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 2, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.BANSHEE, quantity=2,
                 description=inspect.cleandoc(
                     """
                     Level 1: Banshees can remain cloaked twice as long.
                     Level 2: Banshees do not require energy to cloak and remain cloaked.
                     """
                 )),
    ItemNames.BANSHEE_SHOCKWAVE_MISSILE_BATTERY:
        ItemData(317 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.BANSHEE,
                 description="Banshees do area damage in a straight line."),
    ItemNames.BATTLECRUISER_PROGRESSIVE_MISSILE_PODS:
        ItemData(318 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade 2", 2, SC2Race.TERRAN,
                 parent_item=ItemNames.BATTLECRUISER, quantity=2,
                 description="Spell. Missile Pods do damage to air targets in a target area."),
    ItemNames.BATTLECRUISER_PROGRESSIVE_DEFENSIVE_MATRIX:
        ItemData(319 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 20, SC2Race.TERRAN,
                 parent_item=ItemNames.BATTLECRUISER, quantity=2,
                 description=inspect.cleandoc(
                     """
                     Level 1: Spell. For 20 seconds the Battlecruiser gains a shield that can absorb up to 200 damage.
                     Level 2: Passive. Battlecruiser gets 200 shields.
                     """
                 )),
    ItemNames.GHOST_OCULAR_IMPLANTS:
        ItemData(320 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 2, SC2Race.TERRAN,
                 parent_item=ItemNames.GHOST,
                 description="Increases Ghost sight range by 3 and attack range by 2."),
    ItemNames.GHOST_CRIUS_SUIT:
        ItemData(321 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 3, SC2Race.TERRAN,
                 parent_item=ItemNames.GHOST,
                 description="Cloak no longer requires energy to activate or maintain."),
    ItemNames.SPECTRE_PSIONIC_LASH:
        ItemData(322 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 4, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.SPECTRE,
                 description="Spell. Deals 200 damage to a single target."),
    ItemNames.SPECTRE_NYX_CLASS_CLOAKING_MODULE:
        ItemData(323 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 5, SC2Race.TERRAN,
                 parent_item=ItemNames.SPECTRE,
                 description="Cloak no longer requires energy to activate or maintain."),
    ItemNames.THOR_330MM_BARRAGE_CANNON:
        ItemData(324 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 6, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.THOR,
                 description=inspect.cleandoc(
                     """
                     Improves 250mm Strike Cannons ability to deal area damage and stun units in a small area.
                     Can be also freely aimed on ground.
                     """
                 )),
    ItemNames.THOR_PROGRESSIVE_IMMORTALITY_PROTOCOL:
        ItemData(325 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 22, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.THOR, quantity=2,
                 description=inspect.cleandoc("""
                 Level 1: Allows destroyed Thors to be reconstructed on the field. Costs Vespene Gas.
                 Level 2: Thors are automatically reconstructed after falling for free.
                 """
        )),
    ItemNames.LIBERATOR_ADVANCED_BALLISTICS:
        ItemData(326 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 7, SC2Race.TERRAN,
                 parent_item=ItemNames.LIBERATOR, origin={"ext"},
                 description="Increases Liberator range by 3 in Defender Mode."),
    ItemNames.LIBERATOR_RAID_ARTILLERY:
        ItemData(327 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 8, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.LIBERATOR, origin={"nco"},
                 description="Allows Liberators to attack structures while in Defender Mode."),
    ItemNames.WIDOW_MINE_DRILLING_CLAWS:
        ItemData(328 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 9, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.WIDOW_MINE, origin={"ext"},
                 description="Allows Widow Mines to burrow and unburrow faster."),
    ItemNames.WIDOW_MINE_CONCEALMENT:
        ItemData(329 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 10, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.WIDOW_MINE, origin={"ext"},
                 description="Burrowed Widow Mines are no longer revealed when the Sentinel Missile is on cooldown."),
    ItemNames.MEDIVAC_ADVANCED_CLOAKING_FIELD:
        ItemData(330 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 11, SC2Race.TERRAN,
                 parent_item=ItemNames.MEDIVAC, origin={"ext"},
                 description="Medivacs are permanently cloaked."),
    ItemNames.WRAITH_TRIGGER_OVERRIDE:
        ItemData(331 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 12, SC2Race.TERRAN,
                 parent_item=ItemNames.WRAITH, origin={"ext"},
                 description="Wraith attack speed increases by 10% with each attack, up to a maximum of 100%."),
    ItemNames.WRAITH_INTERNAL_TECH_MODULE:
        ItemData(332 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 13, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.WRAITH, origin={"bw"},
                 description=INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Wraiths", "Starport")),
    ItemNames.WRAITH_RESOURCE_EFFICIENCY:
        ItemData(333 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 14, SC2Race.TERRAN,
                 parent_item=ItemNames.WRAITH, origin={"bw"},
                 description=RESOURCE_EFFICIENCY_NO_SUPPLY_DESCRIPTION_TEMPLATE.format("Wraith")),
    ItemNames.VIKING_SHREDDER_ROUNDS:
        ItemData(334 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 15, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.VIKING, origin={"ext"},
                 description="Attacks in Assault mode do line splash damage."),
    ItemNames.VIKING_WILD_MISSILES:
        ItemData(335 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 16, SC2Race.TERRAN,
                 parent_item=ItemNames.VIKING, origin={"ext"},
                 description="Launches 5 rockets at the target unit. Each rocket does 25 (40 vs armored) damage."),
    ItemNames.BANSHEE_SHAPED_HULL:
        ItemData(336 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 17, SC2Race.TERRAN,
                 parent_item=ItemNames.BANSHEE, origin={"ext"},
                 description="Increases Banshee life by 100."),
    ItemNames.BANSHEE_ADVANCED_TARGETING_OPTICS:
        ItemData(337 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 18, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.BANSHEE, origin={"ext"},
                 description="Increases Banshee attack range by 2 while cloaked."),
    ItemNames.BANSHEE_DISTORTION_BLASTERS:
        ItemData(338 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 19, SC2Race.TERRAN,
                 parent_item=ItemNames.BANSHEE, origin={"ext"},
                 description="Increases Banshee attack damage by 25% while cloaked."),
    ItemNames.BANSHEE_ROCKET_BARRAGE:
        ItemData(339 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 20, SC2Race.TERRAN,
                 parent_item=ItemNames.BANSHEE, origin={"ext"},
                 description="Deals 75 damage to enemy ground units in the target area."),
    ItemNames.GHOST_RESOURCE_EFFICIENCY:
        ItemData(340 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 21, SC2Race.TERRAN,
                 parent_item=ItemNames.GHOST, origin={"bw"},
                 description=RESOURCE_EFFICIENCY_DESCRIPTION_TEMPLATE.format("Ghost")),
    ItemNames.SPECTRE_RESOURCE_EFFICIENCY:
        ItemData(341 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 22, SC2Race.TERRAN,
                 parent_item=ItemNames.SPECTRE, origin={"ext"},
                 description=RESOURCE_EFFICIENCY_DESCRIPTION_TEMPLATE.format("Spectre")),
    ItemNames.THOR_BUTTON_WITH_A_SKULL_ON_IT:
        ItemData(342 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 23, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.THOR, origin={"ext"},
                 description="Allows Thors to launch nukes."),
    ItemNames.THOR_LASER_TARGETING_SYSTEM:
        ItemData(343 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 24, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.THOR, origin={"ext"},
                 description=LASER_TARGETING_SYSTEMS_DESCRIPTION),
    ItemNames.THOR_LARGE_SCALE_FIELD_CONSTRUCTION:
        ItemData(344 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 25, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.THOR, origin={"ext"},
                 description="Allows Thors to be built by SCVs like a structure."),
    ItemNames.RAVEN_RESOURCE_EFFICIENCY:
        ItemData(345 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 26, SC2Race.TERRAN,
                 parent_item=ItemNames.RAVEN, origin={"ext"},
                 description=RESOURCE_EFFICIENCY_NO_SUPPLY_DESCRIPTION_TEMPLATE.format("Raven")),
    ItemNames.RAVEN_DURABLE_MATERIALS:
        ItemData(346 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 27, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.RAVEN, origin={"ext"},
                 description="Extends timed life duration of Raven's summoned objects."),
    ItemNames.SCIENCE_VESSEL_IMPROVED_NANO_REPAIR:
        ItemData(347 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 28, SC2Race.TERRAN,
                 parent_item=ItemNames.SCIENCE_VESSEL, origin={"ext"},
                 description="Nano-Repair no longer requires energy to use."),
    ItemNames.SCIENCE_VESSEL_ADVANCED_AI_SYSTEMS:
        ItemData(348 + SC2WOL_ITEM_ID_OFFSET, "Armory 4", 29, SC2Race.TERRAN,
                 parent_item=ItemNames.SCIENCE_VESSEL, origin={"ext"},
                 description="Science Vessel can use Nano-Repair at two targets at once."),
    ItemNames.CYCLONE_RESOURCE_EFFICIENCY:
        ItemData(349 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 0, SC2Race.TERRAN,
                 parent_item=ItemNames.CYCLONE, origin={"ext"},
                 description=RESOURCE_EFFICIENCY_DESCRIPTION_TEMPLATE.format("Cyclone")),
    ItemNames.BANSHEE_HYPERFLIGHT_ROTORS:
        ItemData(350 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 1, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.BANSHEE, origin={"ext"},
                 description="Increases Banshee movement speed."),
    ItemNames.BANSHEE_LASER_TARGETING_SYSTEM:
        ItemData(351 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 2, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.BANSHEE, origin={"nco"},
                 description=LASER_TARGETING_SYSTEMS_DESCRIPTION),
    ItemNames.BANSHEE_INTERNAL_TECH_MODULE:
        ItemData(352 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 3, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.BANSHEE, origin={"nco"},
                 description=INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Banshees", "Starport")),
    ItemNames.BATTLECRUISER_TACTICAL_JUMP:
        ItemData(353 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 4, SC2Race.TERRAN,
                 parent_item=ItemNames.BATTLECRUISER, origin={"nco", "ext"},
                 description=inspect.cleandoc(
                     """
                     Allows Battlecruisers to warp to a target location anywhere on the map.
                     """
                 )),
    ItemNames.BATTLECRUISER_CLOAK:
        ItemData(354 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 5, SC2Race.TERRAN,
                 parent_item=ItemNames.BATTLECRUISER, origin={"nco"},
                 description=CLOAK_DESCRIPTION_TEMPLATE.format("Battlecruisers")),
    ItemNames.BATTLECRUISER_ATX_LASER_BATTERY:
        ItemData(355 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.BATTLECRUISER, origin={"nco"},
                 description=inspect.cleandoc(
                     """
                     Battlecruisers can attack while moving, 
                     do the same damage to both ground and air targets, and fire faster.
                     """
                 )),
    ItemNames.BATTLECRUISER_OPTIMIZED_LOGISTICS:
        ItemData(356 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 7, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.BATTLECRUISER, origin={"ext"},
                 description="Increases Battlecruiser training speed."),
    ItemNames.BATTLECRUISER_INTERNAL_TECH_MODULE:
        ItemData(357 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 8, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.BATTLECRUISER, origin={"nco"},
                 description=INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Battlecruisers", "Starport")),
    ItemNames.GHOST_EMP_ROUNDS:
        ItemData(358 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 9, SC2Race.TERRAN,
                 parent_item=ItemNames.GHOST, origin={"ext"},
                 description=inspect.cleandoc(
                     """
                     Spell. Does 100 damage to shields and drains all energy from units in the targeted area. 
                     Cloaked units hit by EMP are revealed for a short time.
                     """
                 )),
    ItemNames.GHOST_LOCKDOWN:
        ItemData(359 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 10, SC2Race.TERRAN,
                 parent_item=ItemNames.GHOST, origin={"bw"},
                 description="Spell. Stuns a target mechanical unit for a long time."),
    ItemNames.SPECTRE_IMPALER_ROUNDS:
        ItemData(360 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 11, SC2Race.TERRAN,
                 parent_item=ItemNames.SPECTRE, origin={"ext"},
                 description="Spectres do additional damage to armored targets."),
    ItemNames.THOR_PROGRESSIVE_HIGH_IMPACT_PAYLOAD:
        ItemData(361 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 14, SC2Race.TERRAN,
                 parent_item=ItemNames.THOR, quantity=2, origin={"ext"},
                 description=inspect.cleandoc(
                     f"""
                     Level 1: Allows Thors to transform in order to use an alternative air attack.
                     Level 2: {SMART_SERVOS_DESCRIPTION}
                     """
                 )),
    ItemNames.RAVEN_BIO_MECHANICAL_REPAIR_DRONE:
        ItemData(363 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 12, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.RAVEN, origin={"nco"},
                 description="Spell. Deploys a drone that can heal biological or mechanical units."),
    ItemNames.RAVEN_SPIDER_MINES:
        ItemData(364 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 13, SC2Race.TERRAN,
                 parent_item=ItemNames.RAVEN, origin={"nco"}, important_for_filtering=True,
                 description="Spell. Deploys 3 Spider Mines to a target location."),
    ItemNames.RAVEN_RAILGUN_TURRET:
        ItemData(365 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 14, SC2Race.TERRAN,
                 parent_item=ItemNames.RAVEN, origin={"nco"},
                 description=inspect.cleandoc(
                     """
                     Spell. Allows Ravens to deploy an advanced Auto-Turret, 
                     that can attack enemy ground units in a straight line.
                     """
                 )),
    ItemNames.RAVEN_HUNTER_SEEKER_WEAPON:
        ItemData(366 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 15, SC2Race.TERRAN,
                 classification=ItemClassification.progression, parent_item=ItemNames.RAVEN, origin={"nco"},
                 description="Allows Ravens to attack with a Hunter-Seeker weapon."),
    ItemNames.RAVEN_INTERFERENCE_MATRIX:
        ItemData(367 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 16, SC2Race.TERRAN,
                 parent_item=ItemNames.RAVEN, origin={"ext"},
                 description=inspect.cleandoc(
                     """
                     Spell. Target enemy Mechanical or Psionic unit can't attack or use abilities for a short duration.
                     """
                 )),
    ItemNames.RAVEN_ANTI_ARMOR_MISSILE:
        ItemData(368 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 17, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.RAVEN, origin={"ext"},
                 description="Spell. Decreases target and nearby enemy units armor by 2."),
    ItemNames.RAVEN_INTERNAL_TECH_MODULE:
        ItemData(369 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 18, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.RAVEN, origin={"nco"},
                 description=INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Ravens", "Starport")),
    ItemNames.SCIENCE_VESSEL_EMP_SHOCKWAVE:
        ItemData(370 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 19, SC2Race.TERRAN,
                 parent_item=ItemNames.SCIENCE_VESSEL, origin={"bw"},
                 description="Spell. Depletes all energy and shields of all units in a target area."),
    ItemNames.SCIENCE_VESSEL_DEFENSIVE_MATRIX:
        ItemData(371 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 20, SC2Race.TERRAN,
                 parent_item=ItemNames.SCIENCE_VESSEL, origin={"bw"},
                 description=inspect.cleandoc(
                     """
                     Spell. Provides a target unit with a defensive barrier that can absorb up to 250 damage
                     """
                 )),
    ItemNames.CYCLONE_TARGETING_OPTICS:
        ItemData(372 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 21, SC2Race.TERRAN,
                 parent_item=ItemNames.CYCLONE, origin={"ext"},
                 description="Increases Cyclone Lock On casting range and the range while Locked On."),
    ItemNames.CYCLONE_RAPID_FIRE_LAUNCHERS:
        ItemData(373 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 22, SC2Race.TERRAN,
                 parent_item=ItemNames.CYCLONE, origin={"ext"},
                 description="The first 12 shots of Lock On are fired more quickly."),
    ItemNames.LIBERATOR_CLOAK:
        ItemData(374 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 23, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.LIBERATOR, origin={"nco"},
                 description=CLOAK_DESCRIPTION_TEMPLATE.format("Liberators")),
    ItemNames.LIBERATOR_LASER_TARGETING_SYSTEM:
        ItemData(375 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 24, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.LIBERATOR, origin={"ext"},
                 description=LASER_TARGETING_SYSTEMS_DESCRIPTION),
    ItemNames.LIBERATOR_OPTIMIZED_LOGISTICS:
        ItemData(376 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 25, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.LIBERATOR, origin={"nco"},
                 description="Increases Liberator training speed."),
    ItemNames.WIDOW_MINE_BLACK_MARKET_LAUNCHERS:
        ItemData(377 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 26, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.WIDOW_MINE, origin={"ext"},
                 description="Increases Widow Mine Sentinel Missile range."),
    ItemNames.WIDOW_MINE_EXECUTIONER_MISSILES:
        ItemData(378 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 27, SC2Race.TERRAN,
                 parent_item=ItemNames.WIDOW_MINE, origin={"ext"},
                 description=inspect.cleandoc(
                     """
                     Reduces Sentinel Missile cooldown.
                     When killed, Widow Mines will launch several missiles at random enemy targets.
                     """
                 )),
    ItemNames.VALKYRIE_ENHANCED_CLUSTER_LAUNCHERS:
        ItemData(379 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 28,
                 SC2Race.TERRAN, parent_item=ItemNames.VALKYRIE, origin={"ext"},
                 description="Valkyries fire 2 additional rockets each volley."),
    ItemNames.VALKYRIE_SHAPED_HULL:
        ItemData(380 + SC2WOL_ITEM_ID_OFFSET, "Armory 5", 29, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.VALKYRIE, origin={"ext"},
                 description="Increases Valkyrie life by 50."),
    ItemNames.VALKYRIE_FLECHETTE_MISSILES:
        ItemData(381 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 0, SC2Race.TERRAN,
                 parent_item=ItemNames.VALKYRIE, origin={"ext"},
                 description="Equips Valkyries with Air-to-Surface missiles to attack ground units."),
    ItemNames.VALKYRIE_AFTERBURNERS:
        ItemData(382 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 1, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.VALKYRIE, origin={"ext"},
                 description="Ability. Temporarily increases the Valkyries's movement speed by 70%."),
    ItemNames.CYCLONE_INTERNAL_TECH_MODULE:
        ItemData(383 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 2, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.CYCLONE, origin={"ext"},
                 description=INTERNAL_TECH_MODULE_DESCRIPTION_TEMPLATE.format("Cyclones", "Factory")),
    ItemNames.LIBERATOR_SMART_SERVOS:
        ItemData(384 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 3, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.LIBERATOR, origin={"nco"},
                 description=SMART_SERVOS_DESCRIPTION),
    ItemNames.LIBERATOR_RESOURCE_EFFICIENCY:
        ItemData(385 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 4, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.LIBERATOR, origin={"ext"},
                 description=RESOURCE_EFFICIENCY_NO_SUPPLY_DESCRIPTION_TEMPLATE.format("Liberator")),
    ItemNames.HERCULES_INTERNAL_FUSION_MODULE:
        ItemData(386 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 5, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.HERCULES, origin={"ext"},
                 description="Hercules can be trained from a Starport without having a Fusion Core."),
    ItemNames.HERCULES_TACTICAL_JUMP:
        ItemData(387 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 6, SC2Race.TERRAN,
                 parent_item=ItemNames.HERCULES, origin={"ext"},
                 description=inspect.cleandoc(
                     """
                     Allows Hercules to warp to a target location anywhere on the map.
                     """
                 )),
    ItemNames.PLANETARY_FORTRESS_PROGRESSIVE_AUGMENTED_THRUSTERS:
        ItemData(388 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 28, SC2Race.TERRAN,
                 parent_item=ItemNames.PLANETARY_FORTRESS, origin={"ext"}, quantity=2,
                 description=inspect.cleandoc(
                    """
                    Level 1: Lift Off - Planetary Fortress can lift off.
                    Level 2: Armament Stabilizers - Planetary Fortress can attack while lifted off.
                    """
                 )),
    ItemNames.PLANETARY_FORTRESS_ADVANCED_TARGETING:
        ItemData(389 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 7, SC2Race.TERRAN,
                 parent_item=ItemNames.PLANETARY_FORTRESS, origin={"ext"},
                 description="Planetary Fortress can attack air units."),
    ItemNames.VALKYRIE_LAUNCHING_VECTOR_COMPENSATOR:
        ItemData(390 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 8, SC2Race.TERRAN,
                 classification=ItemClassification.filler, parent_item=ItemNames.VALKYRIE, origin={"ext"},
                 description="Allows Valkyries to shoot air while moving."),
    ItemNames.VALKYRIE_RESOURCE_EFFICIENCY:
        ItemData(391 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 9, SC2Race.TERRAN,
                 parent_item=ItemNames.VALKYRIE, origin={"ext"},
                 description=RESOURCE_EFFICIENCY_DESCRIPTION_TEMPLATE.format("Valkyrie")),
    ItemNames.PREDATOR_PREDATOR_S_FURY:
        ItemData(392 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 10, SC2Race.TERRAN,
                 parent_item=ItemNames.PREDATOR, origin={"ext"},
                 description="Predators can use an attack that jumps between targets."),
    ItemNames.BATTLECRUISER_BEHEMOTH_PLATING:
        ItemData(393 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 11, SC2Race.TERRAN,
                 parent_item=ItemNames.BATTLECRUISER, origin={"ext"},
                 description="Increases Battlecruiser armor by 2."),
    ItemNames.BATTLECRUISER_COVERT_OPS_ENGINES:
        ItemData(394 + SC2WOL_ITEM_ID_OFFSET, "Armory 6", 12, SC2Race.TERRAN,
                 parent_item=ItemNames.BATTLECRUISER, origin={"nco"},
                 description="Increases Battlecruiser movement speed."),

    #Buildings
    ItemNames.BUNKER:
        ItemData(400 + SC2WOL_ITEM_ID_OFFSET, "Building", 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Defensive structure. Able to load infantry units, giving them +1 range to their attacks."),
    ItemNames.MISSILE_TURRET:
        ItemData(401 + SC2WOL_ITEM_ID_OFFSET, "Building", 1, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Anti-air defensive structure."),
    ItemNames.SENSOR_TOWER:
        ItemData(402 + SC2WOL_ITEM_ID_OFFSET, "Building", 2, SC2Race.TERRAN,
                 description="Reveals locations of enemy units at long range."),

    ItemNames.WAR_PIGS:
        ItemData(500 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 0, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Mercenary Marines"),
    ItemNames.DEVIL_DOGS:
        ItemData(501 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 1, SC2Race.TERRAN,
                 classification=ItemClassification.filler,
                 description="Mercenary Firebats"),
    ItemNames.HAMMER_SECURITIES:
        ItemData(502 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 2, SC2Race.TERRAN,
                 description="Mercenary Marauders"),
    ItemNames.SPARTAN_COMPANY:
        ItemData(503 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 3, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Mercenary Goliaths"),
    ItemNames.SIEGE_BREAKERS:
        ItemData(504 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 4, SC2Race.TERRAN,
                 description="Mercenary Siege Tanks"),
    ItemNames.HELS_ANGELS:
        ItemData(505 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 5, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Mercenary Vikings"),
    ItemNames.DUSK_WINGS:
        ItemData(506 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 6, SC2Race.TERRAN,
                 description="Mercenary Banshees"),
    ItemNames.JACKSONS_REVENGE:
        ItemData(507 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 7, SC2Race.TERRAN,
                 description="Mercenary Battlecruiser"),
    ItemNames.SKIBIS_ANGELS:
        ItemData(508 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 8, SC2Race.TERRAN,
                 origin={"ext"},
                 description="Mercenary Medics"),
    ItemNames.DEATH_HEADS:
        ItemData(509 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 9, SC2Race.TERRAN,
                 origin={"ext"},
                 description="Mercenary Reapers"),
    ItemNames.WINGED_NIGHTMARES:
        ItemData(510 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 10, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"ext"},
                 description="Mercenary Wraiths"),
    ItemNames.MIDNIGHT_RIDERS:
        ItemData(511 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 11, SC2Race.TERRAN,
                 origin={"ext"},
                 description="Mercenary Liberators"),
    ItemNames.BRYNHILDS:
        ItemData(512 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 12, SC2Race.TERRAN,
                 classification=ItemClassification.progression, origin={"ext"},
                 description="Mercenary Valkyries"),
    ItemNames.JOTUN:
        ItemData(513 + SC2WOL_ITEM_ID_OFFSET, "Mercenary", 13, SC2Race.TERRAN,
                 origin={"ext"},
                 description="Mercenary Thor"),

    ItemNames.ULTRA_CAPACITORS:
        ItemData(600 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 0, SC2Race.TERRAN,
                 description="Increases attack speed of units by 5% per weapon upgrade."),
    ItemNames.VANADIUM_PLATING:
        ItemData(601 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 1, SC2Race.TERRAN,
                 description="Increases the life of units by 5% per armor upgrade."),
    ItemNames.ORBITAL_DEPOTS:
        ItemData(602 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 2, SC2Race.TERRAN,
                 description="Supply depots are built instantly."),
    ItemNames.MICRO_FILTERING:
        ItemData(603 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 3, SC2Race.TERRAN,
                 description="Refineries produce Vespene gas 25% faster."),
    ItemNames.AUTOMATED_REFINERY:
        ItemData(604 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 4, SC2Race.TERRAN,
                 description="Eliminates the need for SCVs in vespene gas production."),
    ItemNames.COMMAND_CENTER_REACTOR:
        ItemData(605 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 5, SC2Race.TERRAN,
                 description="Command Centers can train two SCVs at once."),
    ItemNames.RAVEN:
        ItemData(606 + SC2WOL_ITEM_ID_OFFSET, "Unit", 22, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Aerial Caster unit."),
    ItemNames.SCIENCE_VESSEL:
        ItemData(607 + SC2WOL_ITEM_ID_OFFSET, "Unit", 23, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Aerial Caster unit. Can repair mechanical units."),
    ItemNames.TECH_REACTOR:
        ItemData(608 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 6, SC2Race.TERRAN,
                 description="Merges Tech Labs and Reactors into one add on structure to provide both functions."),
    ItemNames.ORBITAL_STRIKE:
        ItemData(609 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 7, SC2Race.TERRAN,
                 description="Trained units from Barracks are instantly deployed on rally point."),
    ItemNames.BUNKER_SHRIKE_TURRET:
        ItemData(610 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 6, SC2Race.TERRAN,
                 parent_item=ItemNames.BUNKER,
                 description="Adds an automated turret to Bunkers."),
    ItemNames.BUNKER_FORTIFIED_BUNKER:
        ItemData(611 + SC2WOL_ITEM_ID_OFFSET, "Armory 1", 7, SC2Race.TERRAN,
                 parent_item=ItemNames.BUNKER,
                 description="Bunkers have more life."),
    ItemNames.PLANETARY_FORTRESS:
        ItemData(612 + SC2WOL_ITEM_ID_OFFSET, "Building", 3, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description=inspect.cleandoc(
                     """
                     Allows Command Centers to upgrade into a defensive structure with a turret and additional armor.
                     Planetary Fortresses cannot Lift Off, or cast Orbital Command spells.
                     """
                 )),
    ItemNames.PERDITION_TURRET:
        ItemData(613 + SC2WOL_ITEM_ID_OFFSET, "Building", 4, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Automated defensive turret. Burrows down while no enemies are nearby."),
    ItemNames.PREDATOR:
        ItemData(614 + SC2WOL_ITEM_ID_OFFSET, "Unit", 24, SC2Race.TERRAN,
                 classification=ItemClassification.filler,
                 description="Anti-infantry specialist that deals area damage with each attack."),
    ItemNames.HERCULES:
        ItemData(615 + SC2WOL_ITEM_ID_OFFSET, "Unit", 25, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Massive transport ship."),
    ItemNames.CELLULAR_REACTOR:
        ItemData(616 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 8, SC2Race.TERRAN,
                 description="All Terran spellcasters get +100 starting and maximum energy."),
    ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL:
        ItemData(617 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade", 4, SC2Race.TERRAN, quantity=3,
                 classification= ItemClassification.progression,
                 description=inspect.cleandoc(
                     """
                     Allows Terran mechanical units to regenerate health while not in combat.
                     Each level increases life regeneration speed.
                     """
                 )),
    ItemNames.HIVE_MIND_EMULATOR:
        ItemData(618 + SC2WOL_ITEM_ID_OFFSET, "Building", 5, SC2Race.TERRAN,
                 ItemClassification.progression,
                 description="Defensive structure. Can permanently Mind Control Zerg units."),
    ItemNames.PSI_DISRUPTER:
        ItemData(619 + SC2WOL_ITEM_ID_OFFSET, "Building", 6, SC2Race.TERRAN,
                 classification=ItemClassification.progression,
                 description="Defensive structure. Slows the attack and movement speeds of all nearby Zerg units."),
    ItemNames.STRUCTURE_ARMOR:
        ItemData(620 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 9, SC2Race.TERRAN,
                 description="Increases armor of all Terran structures by 2.", origin={"ext"}),
    ItemNames.HI_SEC_AUTO_TRACKING:
        ItemData(621 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 10, SC2Race.TERRAN,
                 description="Increases attack range of all Terran structures by 1.", origin={"ext"}),
    ItemNames.ADVANCED_OPTICS:
        ItemData(622 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 11, SC2Race.TERRAN,
                 description="Increases attack range of all Terran mechanical units by 1.", origin={"ext"}),
    ItemNames.ROGUE_FORCES:
        ItemData(623 + SC2WOL_ITEM_ID_OFFSET, "Laboratory", 12, SC2Race.TERRAN,
                 description="Mercenary calldowns are no longer limited by charges.", origin={"ext"}),

    ItemNames.ZEALOT:
        ItemData(700 + SC2WOL_ITEM_ID_OFFSET, "Unit", 0, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"wol", "lotv"},
                 description="Powerful melee warrior. Can use the charge ability."),
    ItemNames.STALKER: 
        ItemData(701 + SC2WOL_ITEM_ID_OFFSET, "Unit", 1, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"wol", "lotv"},
                 description="Ranged attack strider. Can use the Blink ability."),
    ItemNames.HIGH_TEMPLAR: 
        ItemData(702 + SC2WOL_ITEM_ID_OFFSET, "Unit", 2, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"wol", "lotv"},
                 description="Potent psionic master. Can use the Feedback and Psionic Storm abilities. Can merge into an Archon."),             
    ItemNames.DARK_TEMPLAR: 
        ItemData(703 + SC2WOL_ITEM_ID_OFFSET, "Unit", 3, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"wol", "lotv"},
                 description="Deadly warrior-assassin. Permanently cloaked. Can use the Shadow Fury ability."),
    ItemNames.IMMORTAL: 
        ItemData(704 + SC2WOL_ITEM_ID_OFFSET, "Unit", 4, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"wol", "lotv"},
                 description="Assault strider. Can use Barrier to absorb damage."),
    ItemNames.COLOSSUS:
        ItemData(705 + SC2WOL_ITEM_ID_OFFSET, "Unit", 5, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"wol", "lotv"},
                 description="Battle strider with a powerful area attack. Can walk up and down cliffs. Attacks set fire to the ground, dealing extra damage to enemies over time."),
    ItemNames.PHOENIX:
        ItemData(706 + SC2WOL_ITEM_ID_OFFSET, "Unit", 6, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"wol", "lotv"},
                 description="Air superiority starfighter. Can use Graviton Beam and Phasing Armor abilities."),
    ItemNames.VOID_RAY:
        ItemData(707 + SC2WOL_ITEM_ID_OFFSET, "Unit", 7, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"wol", "lotv"},
                 description="Surgical strike craft. Has the Prismatic Alignment and Prismatic Range abilities."),
    ItemNames.CARRIER:
        ItemData(708 + SC2WOL_ITEM_ID_OFFSET, "Unit", 8, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"wol", "lotv"},
                 description="Capital ship. Builds and launches Interceptors that attack enemy targets. Repair Drones heal nearby mechanical units."),

    # Filler items to fill remaining spots
    ItemNames.STARTING_MINERALS:
        ItemData(800 + SC2WOL_ITEM_ID_OFFSET, "Minerals", 15, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.filler,
                 description="Increases the starting minerals for all missions."),
    ItemNames.STARTING_VESPENE:
        ItemData(801 + SC2WOL_ITEM_ID_OFFSET, "Vespene", 15, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.filler,
                 description="Increases the starting vespene for all missions."),
    ItemNames.STARTING_SUPPLY:
        ItemData(802 + SC2WOL_ITEM_ID_OFFSET, "Supply", 2, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.filler,
                 description="Increases the starting supply for all missions."),
    # This item is used to "remove" location from the game. Never placed unless plando'd
    ItemNames.NOTHING:
        ItemData(803 + SC2WOL_ITEM_ID_OFFSET, "Nothing Group", 2, SC2Race.ANY, quantity=0,
                 classification=ItemClassification.trap,
                 description="Does nothing. Used to remove a location from the game."),

    # Nova gear
    ItemNames.NOVA_GHOST_VISOR:
        ItemData(900 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 0, SC2Race.TERRAN, origin={"nco"},
                 description="Reveals the locations of enemy units in the fog of war around Nova. Can detect cloaked units."),
    ItemNames.NOVA_RANGEFINDER_OCULUS:
        ItemData(901 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 1, SC2Race.TERRAN, origin={"nco"},
                 description="Increaases Nova's vision range and non-melee weapon attack range by 2. Also increases range of melee weapons by 1."),
    ItemNames.NOVA_DOMINATION:
        ItemData(902 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 2, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression,
                 description="Gives Nova the ability to mind-control a target enemy unit."),
    ItemNames.NOVA_BLINK:
        ItemData(903 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 3, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression,
                 description="Gives Nova the ability to teleport a short distance and cloak for 10s."),
    ItemNames.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE:
        ItemData(904 + SC2WOL_ITEM_ID_OFFSET, "Progressive Upgrade 2", 0, SC2Race.TERRAN, quantity=2, origin={"nco"},
                 classification=ItemClassification.progression,
                 description=inspect.cleandoc(
                     """
                     Level 1: Gives Nova the ability to cloak.
                     Level 2: Nova is permanently cloaked.
                     """
                 )),
    ItemNames.NOVA_ENERGY_SUIT_MODULE:
        ItemData(905 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 4, SC2Race.TERRAN, origin={"nco"},
                 description="Increases Nova's maximum energy and energy regeneration rate."),
    ItemNames.NOVA_ARMORED_SUIT_MODULE:
        ItemData(906 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 5, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression,
                 description="Increases Nova's health by 100 and armour by 1. Nova also regenerates life quickly out of combat."),
    ItemNames.NOVA_JUMP_SUIT_MODULE:
        ItemData(907 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 6, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression,
                 description="Increases Nova's movement speed and allows her to jump up and down cliffs."),
    ItemNames.NOVA_C20A_CANISTER_RIFLE:
        ItemData(908 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 7, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression,
                 description="Allows Nova to equip the C20A Canister Rifle, which has a ranged attack and allows Nova to cast Snipe."),
    ItemNames.NOVA_HELLFIRE_SHOTGUN:
        ItemData(909 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 8, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression,
                 description="Allows Nova to equip the Hellfire Shotgun, which has a short-range area attack in a cone and allows Nova to cast Penetrating Blast."),
    ItemNames.NOVA_PLASMA_RIFLE:
        ItemData(910 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 9, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression,
                 description="Allows Nova to equip the Plasma Rifle, which has a rapidfire ranged attack and allows Nova to cast Plasma Shot."),
    ItemNames.NOVA_MONOMOLECULAR_BLADE:
        ItemData(911 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 10, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression,
                 description="Allows Nova to equip the Monomolecular Blade, which has a melee attack and allows Nova to cast Dash Attack."),
    ItemNames.NOVA_BLAZEFIRE_GUNBLADE:
        ItemData(912 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 11, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression,
                 description="Allows Nova to equip the Blazefire Gunblade, which has a melee attack and allows Nova to cast Fury of One."),
    ItemNames.NOVA_STIM_INFUSION:
        ItemData(913 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 12, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression,
                 description="Gives Nova the ability to heal herself and temporarily increase her movement and attack speeds."),
    ItemNames.NOVA_PULSE_GRENADES:
        ItemData(914 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 13, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression,
                 description="Gives Nova the ability to throw a grenade dealing large damage in an area."),
    ItemNames.NOVA_FLASHBANG_GRENADES:
        ItemData(915 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 14, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression,
                 description="Gives Nova the ability to throw a grenade to stun enemies and disable detection in a large area."),
    ItemNames.NOVA_IONIC_FORCE_FIELD:
        ItemData(916 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 15, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression,
                 description="Gives Nova the ability to shield herself temporarily."),
    ItemNames.NOVA_HOLO_DECOY:
        ItemData(917 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 16, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression,
                 description="Gives Nova the ability to summon a decoy unit which enemies will prefer to target and takes reduced damage."),
    ItemNames.NOVA_NUKE:
        ItemData(918 + SC2WOL_ITEM_ID_OFFSET, "Nova Gear", 17, SC2Race.TERRAN, origin={"nco"},
                 classification=ItemClassification.progression,
                 description="Gives Nova the ability to launch tactical nukes built from the Shadow Ops."),

    # HotS
    ItemNames.ZERGLING:
        ItemData(0 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 0, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"},
                 description="Fast inexpensive melee attacker. Hatches in pairs from a single larva. Can morph into a Baneling."),
    ItemNames.SWARM_QUEEN:
        ItemData(1 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 1, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"},
                 description="Ranged support caster. Can use the Spawn Creep Tumor and Rapid Transfusion abilities."),
    ItemNames.ROACH:
        ItemData(2 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 2, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"},
                 description="Durable short ranged attacker. Regenerates life quickly when burrowed."),
    ItemNames.HYDRALISK:
        ItemData(3 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 3, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"},
                 description="High-damage generalist ranged attacker."),
    ItemNames.ZERGLING_BANELING_ASPECT:
        ItemData(4 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 5, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"},
                 description="Anti-ground suicide unit. Does damage over a small area on death."),
    ItemNames.ABERRATION:
        ItemData(5 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 5, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"},
                 description="Durable melee attacker that deals heavy damage and can walk over other units."),
    ItemNames.MUTALISK:
        ItemData(6 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 6, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"},
                 description="Fragile flying attacker. Attacks bounce between targets."),
    ItemNames.SWARM_HOST:
        ItemData(7 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 7, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"},
                 description="Siege unit that attacks by rooting in place and continually spawning Locusts."),
    ItemNames.INFESTOR:
        ItemData(8 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 8, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"},
                 description="Support caster that can move while burrowed. Can use the Fungal Growth, Parasitic Domination, and Consumption abilities."),
    ItemNames.ULTRALISK:
        ItemData(9 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 9, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"},
                 description="Massive melee attacker. Has an area-damage cleave attack."),
    ItemNames.SPORE_CRAWLER:
        ItemData(10 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 10, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"},
                 description="Anti-air defensive structure that can detect cloaked units."),
    ItemNames.SPINE_CRAWLER:
        ItemData(11 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 11, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"hots"},
                 description="Anti-ground defensive structure."),
    ItemNames.CORRUPTOR:
        ItemData(12 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 12, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"ext"},
                 description="Anti-air flying attacker specializing in taking down enemy capital ships."),
    ItemNames.SCOURGE:
        ItemData(13 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 13, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"bw", "ext"},
                 description="Flying anti-air suicide unit. Hatches in pairs from a single larva."),
    ItemNames.BROOD_QUEEN:
        ItemData(14 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 4, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"bw", "ext"},
                 description="Flying support caster. Can cast the Ocular Symbiote and Spawn Broodlings abilities."),
    ItemNames.DEFILER:
        ItemData(15 + SC2HOTS_ITEM_ID_OFFSET, "Unit", 14, SC2Race.ZERG,
                 classification=ItemClassification.progression, origin={"bw"},
                 description="Support caster. Can use the Dark Swarm, Consume, and Plague abilities."),

    ItemNames.PROGRESSIVE_ZERG_MELEE_ATTACK: ItemData(100 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 0, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_MISSILE_ATTACK: ItemData(101 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 2, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_GROUND_CARAPACE: ItemData(102 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 4, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_FLYER_ATTACK: ItemData(103 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 6, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_FLYER_CARAPACE: ItemData(104 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 8, SC2Race.ZERG, quantity=3, origin={"hots"}),
    # Upgrade bundle 'number' values are used as indices to get affected 'number's
    ItemNames.PROGRESSIVE_ZERG_WEAPON_UPGRADE: ItemData(105 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 6, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_ARMOR_UPGRADE: ItemData(106 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 7, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_GROUND_UPGRADE: ItemData(107 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 8, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_FLYER_UPGRADE: ItemData(108 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 9, SC2Race.ZERG, quantity=3, origin={"hots"}),
    ItemNames.PROGRESSIVE_ZERG_WEAPON_ARMOR_UPGRADE: ItemData(109 + SC2HOTS_ITEM_ID_OFFSET, "Upgrade", 10, SC2Race.ZERG, quantity=3, origin={"hots"}),

    ItemNames.ZERGLING_HARDENED_CARAPACE:
        ItemData(200 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 0, SC2Race.ZERG, parent_item=ItemNames.ZERGLING,
                 origin={"hots"}, description="Increases Zergling health by +10."),
    ItemNames.ZERGLING_ADRENAL_OVERLOAD:
        ItemData(201 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 1, SC2Race.ZERG, parent_item=ItemNames.ZERGLING,
                 origin={"hots"}, description="Increases Zergling attack speed."),
    ItemNames.ZERGLING_METABOLIC_BOOST:
        ItemData(202 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 2, SC2Race.ZERG, parent_item=ItemNames.ZERGLING,
                 origin={"hots"}, classification=ItemClassification.filler,
                 description="Increases Zergling movement speed."),
    ItemNames.ROACH_HYDRIODIC_BILE:
        ItemData(203 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 3, SC2Race.ZERG, parent_item=ItemNames.ROACH,
                 origin={"hots"}, description="Roaches deal +8 damage to light targets."),
    ItemNames.ROACH_ADAPTIVE_PLATING:
        ItemData(204 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 4, SC2Race.ZERG, parent_item=ItemNames.ROACH,
                 origin={"hots"}, description="Roaches gain +3 armour when their life is below 50%."),
    ItemNames.ROACH_TUNNELING_CLAWS:
        ItemData(205 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 5, SC2Race.ZERG, parent_item=ItemNames.ROACH,
                 origin={"hots"}, classification=ItemClassification.filler,
                 description="Allows Roaches to move while burrowed."),
    ItemNames.HYDRALISK_FRENZY:
        ItemData(206 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 6, SC2Race.ZERG, parent_item=ItemNames.HYDRALISK,
                 origin={"hots"},
                 description="Allows Hydralisks to use the Frenzy ability, which increases their attack speed by 50%."),
    ItemNames.HYDRALISK_ANCILLARY_CARAPACE:
        ItemData(207 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 7, SC2Race.ZERG, parent_item=ItemNames.HYDRALISK,
                 origin={"hots"}, classification=ItemClassification.filler, description="Hydralisks gain +20 health."),
    ItemNames.HYDRALISK_GROOVED_SPINES:
        ItemData(208 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 8, SC2Race.ZERG, parent_item=ItemNames.HYDRALISK,
                 origin={"hots"}, description="Hydralisks gain +1 range."),
    ItemNames.BANELING_CORROSIVE_ACID:
        ItemData(209 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 9, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"hots"},
                 description="Increases the damage banelings deal to their primary target. Splash damage remains the same."),
    ItemNames.BANELING_RUPTURE:
        ItemData(210 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 10, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"hots"},
                 classification=ItemClassification.filler,
                 description="Increases the splash radius of baneling attacks."),
    ItemNames.BANELING_REGENERATIVE_ACID:
        ItemData(211 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 11, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"hots"},
                 classification=ItemClassification.filler,
                 description="Banelings will heal nearby friendly units when they explode."),
    ItemNames.MUTALISK_VICIOUS_GLAIVE:
        ItemData(212 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 12, SC2Race.ZERG, parent_item=ItemNames.MUTALISK,
                 origin={"hots"}, description="Mutalisks attacks will bounce an additional 3 times."),
    ItemNames.MUTALISK_RAPID_REGENERATION:
        ItemData(213 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 13, SC2Race.ZERG, parent_item=ItemNames.MUTALISK,
                 origin={"hots"}, description="Mutalisks will regenerate quickly when out of combat."),
    ItemNames.MUTALISK_SUNDERING_GLAIVE:
        ItemData(214 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 14, SC2Race.ZERG, parent_item=ItemNames.MUTALISK,
                 origin={"hots"}, description="Mutalisks deal increased damage to their primary target."),
    ItemNames.SWARM_HOST_BURROW:
        ItemData(215 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 15, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"hots"}, classification=ItemClassification.filler,
                 description="Allows Swarm Hosts to burrow instead of root to spawn locusts."),
    ItemNames.SWARM_HOST_RAPID_INCUBATION:
        ItemData(216 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 16, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"hots"}, description="Swarm Hosts will spawn locusts 20% faster."),
    ItemNames.SWARM_HOST_PRESSURIZED_GLANDS:
        ItemData(217 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 17, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"hots"}, classification=ItemClassification.progression,
                 description="Allows Swarm Host Locusts to attack air targets."),
    ItemNames.ULTRALISK_BURROW_CHARGE:
        ItemData(218 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 18, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"hots"},
                 description="Allows Ultralisks to burrow and charge at enemy units, knocking back and stunning units when it emerges."),
    ItemNames.ULTRALISK_TISSUE_ASSIMILATION:
        ItemData(219 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 19, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"hots"}, description="Ultralisks recover health when they deal damage."),
    ItemNames.ULTRALISK_MONARCH_BLADES:
        ItemData(220 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 20, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"hots"}, description="Ultralisks gain increased splash damage."),
    ItemNames.CORRUPTOR_CAUSTIC_SPRAY:
        ItemData(221 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 21, SC2Race.ZERG, parent_item=ItemNames.CORRUPTOR,
                 origin={"ext"},
                 description="Allows Corruptors to use the Caustic Spray ability, which deals ramping damage to buildings over time."),
    ItemNames.CORRUPTOR_CORRUPTION:
        ItemData(222 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 22, SC2Race.ZERG, parent_item=ItemNames.CORRUPTOR,
                 origin={"ext"},
                 description="Allows Corruptors to use the Corruption ability, which causes a target enemy unit to take increased damage."),
    ItemNames.SCOURGE_VIRULENT_SPORES:
        ItemData(223 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 23, SC2Race.ZERG, parent_item=ItemNames.SCOURGE,
                 origin={"ext"}, description="Scourge will deal splash damage."),
    ItemNames.SCOURGE_RESOURCE_EFFICIENCY:
        ItemData(224 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 24, SC2Race.ZERG, parent_item=ItemNames.SCOURGE,
                 origin={"ext"}, classification=ItemClassification.progression,
                 description="Reduces the cost of Scourge by 50 gas per egg."),
    ItemNames.SCOURGE_SWARM_SCOURGE:
        ItemData(225 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 25, SC2Race.ZERG, parent_item=ItemNames.SCOURGE,
                 origin={"ext"}, description="An extra Scourge will be built from each egg at no additional cost."),
    ItemNames.ZERGLING_SHREDDING_CLAWS:
        ItemData(226 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 26, SC2Race.ZERG, parent_item=ItemNames.ZERGLING,
                 origin={"ext"}, description="Zergling attacks will temporarily reduce their target's armour to 0."),
    ItemNames.ROACH_GLIAL_RECONSTITUTION:
        ItemData(227 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 27, SC2Race.ZERG, parent_item=ItemNames.ROACH,
                 origin={"ext"}, description="Increases Roach movement speed."),
    ItemNames.ROACH_ORGANIC_CARAPACE:
        ItemData(228 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 28, SC2Race.ZERG, parent_item=ItemNames.ROACH,
                 origin={"ext"}, description="Increases Roach health by +25."),
    ItemNames.HYDRALISK_MUSCULAR_AUGMENTS:
        ItemData(229 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 1", 29, SC2Race.ZERG, parent_item=ItemNames.HYDRALISK,
                 origin={"bw"}, description="Increases Hydralisk movement speed."),
    ItemNames.HYDRALISK_RESOURCE_EFFICIENCY:
        ItemData(230 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 0, SC2Race.ZERG, parent_item=ItemNames.HYDRALISK,
                 origin={"bw"}, description="Reduces Hydralisk resource cost by 25/25 and supply cost by 1."),
    ItemNames.BANELING_CENTRIFUGAL_HOOKS:
        ItemData(231 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 1, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"ext"},
                 description="Increases the movement speed of Banelings."),
    ItemNames.BANELING_TUNNELING_JAWS:
        ItemData(232 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 2, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"ext"},
                 description="Allows Banelings to move while burrowed."),
    ItemNames.BANELING_RAPID_METAMORPH:
        ItemData(233 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 3, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"ext"}, description="Banelings morph faster."),
    ItemNames.MUTALISK_SEVERING_GLAIVE:
        ItemData(234 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 4, SC2Race.ZERG, parent_item=ItemNames.MUTALISK,
                 origin={"ext"}, description="Mutalisk bounce attacks will deal full damage."),
    ItemNames.MUTALISK_AERODYNAMIC_GLAIVE_SHAPE:
        ItemData(235 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 5, SC2Race.ZERG, parent_item=ItemNames.MUTALISK,
                 origin={"ext"}, description="Increases the attack range of Mutalisks by 2."),
    ItemNames.SWARM_HOST_LOCUST_METABOLIC_BOOST:
        ItemData(236 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 6, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"ext"}, classification=ItemClassification.filler,
                 description="Increases Locust movement speed."),
    ItemNames.SWARM_HOST_ENDURING_LOCUSTS:
        ItemData(237 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 7, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"ext"}, description="Increases the duration of Swarm Hosts' Locusts by 10s."),
    ItemNames.SWARM_HOST_ORGANIC_CARAPACE:
        ItemData(238 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 8, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"ext"}, description="Increases Swarm Host health by +40."),
    ItemNames.SWARM_HOST_RESOURCE_EFFICIENCY:
        ItemData(239 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 9, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"ext"}, description="Reduces Swarm Host resource cost by 100/25."),
    ItemNames.ULTRALISK_ANABOLIC_SYNTHESIS:
        ItemData(240 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 10, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"bw"}, classification=ItemClassification.filler),
    ItemNames.ULTRALISK_CHITINOUS_PLATING:
        ItemData(241 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 11, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"bw"}),
    ItemNames.ULTRALISK_ORGANIC_CARAPACE:
        ItemData(242 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 12, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"ext"}),
    ItemNames.ULTRALISK_RESOURCE_EFFICIENCY:
        ItemData(243 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 13, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"bw"}),
    ItemNames.DEVOURER_CORROSIVE_SPRAY:
        ItemData(244 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 14, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_DEVOURER_ASPECT, origin={"ext"}),
    ItemNames.DEVOURER_GAPING_MAW:
        ItemData(245 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 15, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_DEVOURER_ASPECT, origin={"ext"}),
    ItemNames.DEVOURER_IMPROVED_OSMOSIS:
        ItemData(246 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 16, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_DEVOURER_ASPECT, origin={"ext"},
                 classification=ItemClassification.filler),
    ItemNames.DEVOURER_PRESCIENT_SPORES:
        ItemData(247 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 17, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_DEVOURER_ASPECT, origin={"ext"}),
    ItemNames.GUARDIAN_PROLONGED_DISPERSION:
        ItemData(248 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 18, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT, origin={"ext"}),
    ItemNames.GUARDIAN_PRIMAL_ADAPTATION:
        ItemData(249 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 19, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT, origin={"ext"}),
    ItemNames.GUARDIAN_SORONAN_ACID:
        ItemData(250 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 20, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT, origin={"ext"}),
    ItemNames.IMPALER_ADAPTIVE_TALONS:
        ItemData(251 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 21, SC2Race.ZERG,
                 parent_item=ItemNames.HYDRALISK_IMPALER_ASPECT, origin={"ext"},
                 classification=ItemClassification.filler),
    ItemNames.IMPALER_SECRETION_GLANDS:
        ItemData(252 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 22, SC2Race.ZERG,
                 parent_item=ItemNames.HYDRALISK_IMPALER_ASPECT, origin={"ext"}),
    ItemNames.IMPALER_HARDENED_TENTACLE_SPINES:
        ItemData(253 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 23, SC2Race.ZERG,
                 parent_item=ItemNames.HYDRALISK_IMPALER_ASPECT, origin={"ext"}),
    ItemNames.LURKER_SEISMIC_SPINES:
        ItemData(254 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 24, SC2Race.ZERG,
                 parent_item=ItemNames.HYDRALISK_LURKER_ASPECT, origin={"ext"}),
    ItemNames.LURKER_ADAPTED_SPINES:
        ItemData(255 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 25, SC2Race.ZERG,
                 parent_item=ItemNames.HYDRALISK_LURKER_ASPECT, origin={"ext"}),
    ItemNames.RAVAGER_POTENT_BILE:
        ItemData(256 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 26, SC2Race.ZERG,
                 parent_item=ItemNames.ROACH_RAVAGER_ASPECT, origin={"ext"}),
    ItemNames.RAVAGER_BLOATED_BILE_DUCTS:
        ItemData(257 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 27, SC2Race.ZERG,
                 parent_item=ItemNames.ROACH_RAVAGER_ASPECT, origin={"ext"}),
    ItemNames.RAVAGER_DEEP_TUNNEL:
        ItemData(258 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 28, SC2Race.ZERG,
                 parent_item=ItemNames.ROACH_RAVAGER_ASPECT, origin={"ext"}),
    ItemNames.VIPER_PARASITIC_BOMB:
        ItemData(259 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 2", 29, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_VIPER_ASPECT, origin={"ext"}),
    ItemNames.VIPER_PARALYTIC_BARBS:
        ItemData(260 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 0, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_VIPER_ASPECT, origin={"ext"}),
    ItemNames.VIPER_VIRULENT_MICROBES:
        ItemData(261 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 1, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_VIPER_ASPECT, origin={"ext"}),
    ItemNames.BROOD_LORD_POROUS_CARTILAGE:
        ItemData(262 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 2, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT, origin={"ext"}),
    ItemNames.BROOD_LORD_EVOLVED_CARAPACE:
        ItemData(263 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 3, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT, origin={"ext"}),
    ItemNames.BROOD_LORD_SPLITTER_MITOSIS:
        ItemData(264 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 4, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT, origin={"ext"}),
    ItemNames.BROOD_LORD_RESOURCE_EFFICIENCY:
        ItemData(265 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 5, SC2Race.ZERG,
                 parent_item=ItemNames.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT, origin={"ext"}),
    ItemNames.INFESTOR_INFESTED_TERRAN:
        ItemData(266 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 6, SC2Race.ZERG, parent_item=ItemNames.INFESTOR,
                 origin={"ext"}),
    ItemNames.INFESTOR_MICROBIAL_SHROUD:
        ItemData(267 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 7, SC2Race.ZERG, parent_item=ItemNames.INFESTOR,
                 origin={"ext"}),
    ItemNames.SWARM_QUEEN_SPAWN_LARVAE:
        ItemData(268 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 8, SC2Race.ZERG, parent_item=ItemNames.SWARM_QUEEN,
                 origin={"ext"}),
    ItemNames.SWARM_QUEEN_DEEP_TUNNEL:
        ItemData(269 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 9, SC2Race.ZERG, parent_item=ItemNames.SWARM_QUEEN,
                 origin={"ext"}),
    ItemNames.SWARM_QUEEN_ORGANIC_CARAPACE:
        ItemData(270 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 10, SC2Race.ZERG, parent_item=ItemNames.SWARM_QUEEN,
                 origin={"ext"}, classification=ItemClassification.filler),
    ItemNames.SWARM_QUEEN_BIO_MECHANICAL_TRANSFUSION:
        ItemData(271 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 11, SC2Race.ZERG, parent_item=ItemNames.SWARM_QUEEN,
                 origin={"ext"}),
    ItemNames.SWARM_QUEEN_RESOURCE_EFFICIENCY:
        ItemData(272 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 12, SC2Race.ZERG, parent_item=ItemNames.SWARM_QUEEN,
                 origin={"ext"}),
    ItemNames.SWARM_QUEEN_INCUBATOR_CHAMBER:
        ItemData(273 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 13, SC2Race.ZERG, parent_item=ItemNames.SWARM_QUEEN,
                 origin={"ext"}),
    ItemNames.BROOD_QUEEN_FUNGAL_GROWTH:
        ItemData(274 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 14, SC2Race.ZERG, parent_item=ItemNames.BROOD_QUEEN,
                 origin={"ext"}),
    ItemNames.BROOD_QUEEN_ENSNARE:
        ItemData(275 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 15, SC2Race.ZERG, parent_item=ItemNames.BROOD_QUEEN,
                 origin={"ext"}),
    ItemNames.BROOD_QUEEN_ENHANCED_MITOCHONDRIA:
        ItemData(276 + SC2HOTS_ITEM_ID_OFFSET, "Mutation 3", 16, SC2Race.ZERG, parent_item=ItemNames.BROOD_QUEEN,
                 origin={"ext"}),

    ItemNames.ZERGLING_RAPTOR_STRAIN:
        ItemData(300 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 0, SC2Race.ZERG, parent_item=ItemNames.ZERGLING,
                 origin={"hots"},
                 description="Allows Zerglings to jump up and down cliffs and leap onto enemies. Also increases Zergling attack damage by 2."),
    ItemNames.ZERGLING_SWARMLING_STRAIN:
        ItemData(301 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 1, SC2Race.ZERG, parent_item=ItemNames.ZERGLING,
                 origin={"hots"},
                 description="Zerglings will spawn instantly and with an extra Zergling per egg at no additional cost."),
    ItemNames.ROACH_VILE_STRAIN:
        ItemData(302 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 2, SC2Race.ZERG, parent_item=ItemNames.ROACH, origin={"hots"},
                 description="Roach attacks will slow the movement and attack speed of enemies."),
    ItemNames.ROACH_CORPSER_STRAIN:
        ItemData(303 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 3, SC2Race.ZERG, parent_item=ItemNames.ROACH, origin={"hots"},
                 description="Units killed after being attacked by Roaches will spawn 2 Roachlings."),
    ItemNames.HYDRALISK_IMPALER_ASPECT:
        ItemData(304 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 0, SC2Race.ZERG, origin={"hots"},
                 classification=ItemClassification.progression,
                 description="Allows Hydralisks to morph into Impalers."),
    ItemNames.HYDRALISK_LURKER_ASPECT:
        ItemData(305 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 1, SC2Race.ZERG, origin={"hots"},
                 classification=ItemClassification.progression, description="Allows Hydralisks to morph into Lurkers."),
    ItemNames.BANELING_SPLITTER_STRAIN:
        ItemData(306 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 6, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"hots"},
                 description="Banelings will split into two smaller Splitterlings on exploding."),
    ItemNames.BANELING_HUNTER_STRAIN:
        ItemData(307 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 7, SC2Race.ZERG,
                 parent_item=ItemNames.ZERGLING_BANELING_ASPECT, origin={"hots"},
                 description="Allows Banelings to jump up and down cliffs and leap onto enemies."),
    ItemNames.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT:
        ItemData(308 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 2, SC2Race.ZERG, origin={"hots"},
                 classification=ItemClassification.progression,
                 description="Allows Mutalisks and Corruptors to morph into Brood Lords."),
    ItemNames.MUTALISK_CORRUPTOR_VIPER_ASPECT:
        ItemData(309 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 3, SC2Race.ZERG, origin={"hots"},
                 classification=ItemClassification.progression,
                 description="Allows Mutalisks and Corruptors to morph into Vipers."),
    ItemNames.SWARM_HOST_CARRION_STRAIN:
        ItemData(310 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 10, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"hots"}, description="Swarm Hosts will spawn Flying Locusts."),
    ItemNames.SWARM_HOST_CREEPER_STRAIN:
        ItemData(311 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 11, SC2Race.ZERG, parent_item=ItemNames.SWARM_HOST,
                 origin={"hots"}, classification=ItemClassification.filler,
                 description="Allows Swarm Hosts to teleport to any creep on the map in vision. Swarm Hosts will spread creep around them when rooted or burrowed."),
    ItemNames.ULTRALISK_NOXIOUS_STRAIN:
        ItemData(312 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 12, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"hots"}, classification=ItemClassification.filler,
                 description="Ultralisks will periodically spread poison, damaging nearby biological enemies."),
    ItemNames.ULTRALISK_TORRASQUE_STRAIN:
        ItemData(313 + SC2HOTS_ITEM_ID_OFFSET, "Strain", 13, SC2Race.ZERG, parent_item=ItemNames.ULTRALISK,
                 origin={"hots"}, description="Ultralisks will revive after being killed."),

    ItemNames.KERRIGAN_KINETIC_BLAST: ItemData(400 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 0, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_HEROIC_FORTITUDE: ItemData(401 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 1, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEAPING_STRIKE: ItemData(402 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 2, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_CRUSHING_GRIP: ItemData(403 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 3, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_CHAIN_REACTION: ItemData(404 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 4, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_PSIONIC_SHIFT: ItemData(405 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 5, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_ZERGLING_RECONSTITUTION: ItemData(406 + SC2HOTS_ITEM_ID_OFFSET, "Evolution Pit", 0, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.filler),
    ItemNames.KERRIGAN_IMPROVED_OVERLORDS: ItemData(407 + SC2HOTS_ITEM_ID_OFFSET, "Evolution Pit", 1, SC2Race.ZERG, origin={"hots"}),
    ItemNames.KERRIGAN_AUTOMATED_EXTRACTORS: ItemData(408 + SC2HOTS_ITEM_ID_OFFSET, "Evolution Pit", 2, SC2Race.ZERG, origin={"hots"}),
    ItemNames.KERRIGAN_WILD_MUTATION: ItemData(409 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 6, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_SPAWN_BANELINGS: ItemData(410 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 7, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_MEND: ItemData(411 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 8, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_TWIN_DRONES: ItemData(412 + SC2HOTS_ITEM_ID_OFFSET, "Evolution Pit", 3, SC2Race.ZERG, origin={"hots"}),
    ItemNames.KERRIGAN_MALIGNANT_CREEP: ItemData(413 + SC2HOTS_ITEM_ID_OFFSET, "Evolution Pit", 4, SC2Race.ZERG, origin={"hots"}),
    ItemNames.KERRIGAN_VESPENE_EFFICIENCY: ItemData(414 + SC2HOTS_ITEM_ID_OFFSET, "Evolution Pit", 5, SC2Race.ZERG, origin={"hots"}),
    ItemNames.KERRIGAN_INFEST_BROODLINGS: ItemData(415 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 9, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_FURY: ItemData(416 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 10, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_ABILITY_EFFICIENCY: ItemData(417 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 11, SC2Race.ZERG, origin={"hots"}),
    ItemNames.KERRIGAN_APOCALYPSE: ItemData(418 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 12, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_SPAWN_LEVIATHAN: ItemData(419 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 13, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_DROP_PODS: ItemData(420 + SC2HOTS_ITEM_ID_OFFSET, "Ability", 14, SC2Race.ZERG, origin={"hots"}, classification=ItemClassification.progression),
    # Handled separately from other abilities
    ItemNames.KERRIGAN_PRIMAL_FORM: ItemData(421 + SC2HOTS_ITEM_ID_OFFSET, "Primal Form", 0, SC2Race.ZERG, origin={"hots"}),

    ItemNames.KERRIGAN_LEVELS_10: ItemData(500 + SC2HOTS_ITEM_ID_OFFSET, "Level", 10, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_9: ItemData(501 + SC2HOTS_ITEM_ID_OFFSET, "Level", 9, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_8: ItemData(502 + SC2HOTS_ITEM_ID_OFFSET, "Level", 8, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_7: ItemData(503 + SC2HOTS_ITEM_ID_OFFSET, "Level", 7, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_6: ItemData(504 + SC2HOTS_ITEM_ID_OFFSET, "Level", 6, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_5: ItemData(505 + SC2HOTS_ITEM_ID_OFFSET, "Level", 5, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_4: ItemData(506 + SC2HOTS_ITEM_ID_OFFSET, "Level", 4, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression_skip_balancing),
    ItemNames.KERRIGAN_LEVELS_3: ItemData(507 + SC2HOTS_ITEM_ID_OFFSET, "Level", 3, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression_skip_balancing),
    ItemNames.KERRIGAN_LEVELS_2: ItemData(508 + SC2HOTS_ITEM_ID_OFFSET, "Level", 2, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression_skip_balancing),
    ItemNames.KERRIGAN_LEVELS_1: ItemData(509 + SC2HOTS_ITEM_ID_OFFSET, "Level", 1, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression_skip_balancing),
    ItemNames.KERRIGAN_LEVELS_14: ItemData(510 + SC2HOTS_ITEM_ID_OFFSET, "Level", 14, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_35: ItemData(511 + SC2HOTS_ITEM_ID_OFFSET, "Level", 35, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),
    ItemNames.KERRIGAN_LEVELS_70: ItemData(512 + SC2HOTS_ITEM_ID_OFFSET, "Level", 70, SC2Race.ZERG, origin={"hots"}, quantity=0, classification=ItemClassification.progression),

    # Zerg Mercs
    ItemNames.INFESTED_MEDICS: ItemData(600 + SC2HOTS_ITEM_ID_OFFSET, "Mercenary", 0, SC2Race.ZERG, origin={"ext"}),
    ItemNames.INFESTED_SIEGE_TANKS: ItemData(601 + SC2HOTS_ITEM_ID_OFFSET, "Mercenary", 1, SC2Race.ZERG, origin={"ext"}),
    ItemNames.INFESTED_BANSHEES: ItemData(602 + SC2HOTS_ITEM_ID_OFFSET, "Mercenary", 2, SC2Race.ZERG, origin={"ext"}),

    # Misc Upgrades
    ItemNames.OVERLORD_VENTRAL_SACS: ItemData(700 + SC2HOTS_ITEM_ID_OFFSET, "Evolution Pit", 6, SC2Race.ZERG, origin={"bw"}),

    # Morphs
    ItemNames.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT: ItemData(800 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 6, SC2Race.ZERG, origin={"bw"}),
    ItemNames.MUTALISK_CORRUPTOR_DEVOURER_ASPECT: ItemData(801 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 7, SC2Race.ZERG, origin={"bw"}),
    ItemNames.ROACH_RAVAGER_ASPECT: ItemData(802 + SC2HOTS_ITEM_ID_OFFSET, "Morph", 8, SC2Race.ZERG, origin={"ext"}),


    # Protoss Units (those that aren't as items in WoL (Prophecy))
    ItemNames.OBSERVER: ItemData(0 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 9, SC2Race.PROTOSS, 
                 classification=ItemClassification.filler, origin={"wol"},
                 description="Flying spy. Cloak renders the unit invisible to enemies without detection."),
    ItemNames.CENTURION: ItemData(1 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 10, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Powerful melee warrior. Has the Shadow Charge and Darkcoil abilities."),
    ItemNames.SENTINEL: ItemData(2 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 11, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Powerful melee warrior. Has the Charge and Reconstruction abilities."),
    ItemNames.SUPPLICANT: ItemData(3 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 12, SC2Race.PROTOSS, 
                 classification=ItemClassification.filler, important_for_filtering=True, origin={"ext"},
                 description="Powerful melee warrior. Has powerful damage resistant shields."),
    ItemNames.INSTIGATOR: ItemData(4 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 13, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"ext"},
                 description="Ranged support strider. Can store multiple Blink charges."),
    ItemNames.SLAYER: ItemData(5 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 14, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"ext"},
                 description="Ranged attack strider. Can use the Phase Blink and Phasing Armor abilities."),
    ItemNames.SENTRY: ItemData(6 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 15, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Robotic support unit can use the Guardian Shield ability and restore the shields of nearby Protoss units."),
    ItemNames.ENERGIZER: ItemData(7 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 16, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Robotic support unit. Can use the Chrono Beam ability and become stationary to power nearby structures."),
    ItemNames.HAVOC: ItemData(8 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 17, SC2Race.PROTOSS,
                 origin={"lotv"}, important_for_filtering=True,
                 description="Robotic support unit. Can use the Target Lock and Force Field abilities and increase the range of nearby Protoss units."),
    ItemNames.SIGNIFIER: ItemData(9 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 18, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"ext"},
                 description="Potent permanently cloaked psionic master. Can use the Feedback and Crippling Psionic Storm abilities. Can merge into an Archon."),
    ItemNames.ASCENDANT: ItemData(10 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 19, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Potent psionic master. Can use the Psionic Orb, Mind Blast, and Sacrifice abilities."),
    ItemNames.AVENGER: ItemData(11 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 20, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Deadly warrior-assassin. Permanently cloaked. Recalls to the nearest Dark Shrine upon death."),
    ItemNames.BLOOD_HUNTER: ItemData(12 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 21, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Deadly warrior-assassin. Permanently cloaked. Can use the Void Stasis ability."),
    ItemNames.DRAGOON: ItemData(13 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 22, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Ranged assault strider. Has enhanced health and damage."),
    ItemNames.DARK_ARCHON: ItemData(14 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 23, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Potent psionic master. Can use the Confuse and Mind Control abilities."),
    ItemNames.ADEPT: ItemData(15 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 24, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Ranged specialist. Can use the Psionic Transfer ability."),
    ItemNames.WARP_PRISM: ItemData(16 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 25, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"ext"},
                 description="Flying transport. Can carry units and become stationary to deploy a power field."),
    ItemNames.ANNIHILATOR: ItemData(17 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 26, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Assault Strider. Can use the Shadow Cannon ability to damage air and ground units."),
    ItemNames.VANGUARD: ItemData(18 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 27, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Assault Strider. Deals splash damage around the primary target."),
    ItemNames.WRATHWALKER: ItemData(19 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 28, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Battle strider with a powerful single target attack.  Can walk up and down cliffs."),
    ItemNames.REAVER: ItemData(20 + SC2LOTV_ITEM_ID_OFFSET, "Unit", 29, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Area damage siege unit. Builds and launches explosive Scarabs for high burst damage."),
    ItemNames.DISRUPTOR: ItemData(21 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 0, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"ext"},
                 description="Robotic disruption unit. Can use the Purification Nova ability to deal heavy area damage."),
    ItemNames.MIRAGE: ItemData(22 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 1, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Air superiority starfighter. Can use Graviton Beam and Phasing Armor abilities."),
    ItemNames.CORSAIR: ItemData(23 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 2, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Air superiority starfighter. Can use the Disruption Web ability."),
    ItemNames.DESTROYER: ItemData(24 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 3, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Area assault craft. Can use the Destruction Beam ability to attack multiple units at once."),
    ItemNames.SCOUT: ItemData(25 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 4, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"ext"},
                 description="Versatile high-speed fighter."),
    ItemNames.TEMPEST: ItemData(26 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 5, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Siege artillery craft. Attacks from long range. Can use the Disintegration ability."),
    ItemNames.MOTHERSHIP: ItemData(27 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 6, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Ultimate Protoss vessel, Can use the Vortex and Mass Recall abilities. Cloaks nearby units and structures."),
    ItemNames.ARBITER: ItemData(28 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 7, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="Army support craft. Has the Stasis Field and Recall abilities. Cloaks nearby units."),
    ItemNames.ORACLE: ItemData(29 + SC2LOTV_ITEM_ID_OFFSET, "Unit 2", 8, SC2Race.PROTOSS, 
                 classification=ItemClassification.progression, origin={"ext"},
                 description="Flying caster. Can use the Revelation and Stasis Ward abilities."),

    # Protoss Upgrades
    ItemNames.PROGRESSIVE_PROTOSS_GROUND_WEAPON: ItemData(100 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 0, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_GROUND_ARMOR: ItemData(101 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 2, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_SHIELDS: ItemData(102 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 4, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_AIR_WEAPON: ItemData(103 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 6, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_AIR_ARMOR: ItemData(104 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 8, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    # Upgrade bundle 'number' values are used as indices to get affected 'number's
    ItemNames.PROGRESSIVE_PROTOSS_WEAPON_UPGRADE: ItemData(105 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 11, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_ARMOR_UPGRADE: ItemData(106 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 12, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_GROUND_UPGRADE: ItemData(107 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 13, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_AIR_UPGRADE: ItemData(108 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 14, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),
    ItemNames.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE: ItemData(109 + SC2LOTV_ITEM_ID_OFFSET, "Upgrade", 15, SC2Race.PROTOSS, quantity=3, origin={"wol", "lotv"}),

    # Protoss Buildings
    ItemNames.PHOTON_CANNON: ItemData(200 + SC2LOTV_ITEM_ID_OFFSET, "Building", 0, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"wol", "lotv"}),
    ItemNames.KHAYDARIN_MONOLITH: ItemData(201 + SC2LOTV_ITEM_ID_OFFSET, "Building", 1, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.SHIELD_BATTERY: ItemData(202 + SC2LOTV_ITEM_ID_OFFSET, "Building", 2, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"lotv"}),

    # Protoss Unit Upgrades
    ItemNames.SUPPLICANT_BLOOD_SHIELD: ItemData(300 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 0, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.SUPPLICANT),
    ItemNames.SUPPLICANT_SOUL_AUGMENTATION: ItemData(301 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 1, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.SUPPLICANT),
    ItemNames.SUPPLICANT_SHIELD_REGENERATION: ItemData(302 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 2, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.SUPPLICANT),
    ItemNames.ADEPT_SHOCKWAVE: ItemData(303 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 3, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ADEPT),
    ItemNames.ADEPT_RESONATING_GLAIVES: ItemData(304 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 4, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ADEPT),
    ItemNames.ADEPT_PHASE_BULWARK: ItemData(305 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 5, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ADEPT),
    ItemNames.STALKER_INSTIGATOR_SLAYER_DISINTEGRATING_PARTICLES: ItemData(306 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 6, SC2Race.PROTOSS, origin={"ext"}, classification=ItemClassification.progression),
    ItemNames.STALKER_INSTIGATOR_SLAYER_PARTICLE_REFLECTION: ItemData(307 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 7, SC2Race.PROTOSS, origin={"ext"}, classification=ItemClassification.progression),
    ItemNames.DRAGOON_HIGH_IMPACT_PHASE_DISRUPTORS: ItemData(308 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 8, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.DRAGOON),
    ItemNames.DRAGOON_TRILLIC_COMPRESSION_SYSTEM: ItemData(309 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 9, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.DRAGOON),
    ItemNames.DRAGOON_SINGULARITY_CHARGE: ItemData(310 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 10, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.DRAGOON),
    ItemNames.DRAGOON_ENHANCED_STRIDER_SERVOS: ItemData(311 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 11, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.DRAGOON),
    ItemNames.SCOUT_COMBAT_SENSOR_ARRAY: ItemData(312 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 12, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.SCOUT),
    ItemNames.SCOUT_APIAL_SENSORS: ItemData(313 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 13, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.SCOUT),
    ItemNames.SCOUT_GRAVITIC_THRUSTERS: ItemData(314 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 14, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.SCOUT),
    ItemNames.SCOUT_ADVANCED_PHOTON_BLASTERS: ItemData(315 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 15, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.SCOUT),
    ItemNames.TEMPEST_TECTONIC_DESTABILIZERS: ItemData(316 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 16, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.TEMPEST),
    ItemNames.TEMPEST_QUANTIC_REACTOR: ItemData(317 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 17, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.TEMPEST),
    ItemNames.TEMPEST_GRAVITY_SLING: ItemData(318 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 18, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.TEMPEST),
    ItemNames.PHOENIX_MIRAGE_IONIC_WAVELENGTH_FLUX: ItemData(319 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 19, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.PHOENIX_MIRAGE_ANION_PULSE_CRYSTALS: ItemData(320 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 20, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.CORSAIR_STEALTH_DRIVE: ItemData(321 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 21, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.CORSAIR),
    ItemNames.CORSAIR_ARGUS_JEWEL: ItemData(322 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 22, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.CORSAIR),
    ItemNames.CORSAIR_SUSTAINING_DISRUPTION: ItemData(323 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 23, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.CORSAIR),
    ItemNames.CORSAIR_NEUTRON_SHIELDS: ItemData(324 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 24, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.CORSAIR),
    ItemNames.ORACLE_STEALTH_DRIVE: ItemData(325 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 25, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ORACLE),
    ItemNames.ORACLE_STASIS_CALIBRATION: ItemData(326 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 26, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ORACLE),
    ItemNames.ORACLE_TEMPORAL_ACCELERATION_BEAM: ItemData(327 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 27, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ORACLE),
    ItemNames.ARBITER_CHRONOSTATIC_REINFORCEMENT: ItemData(328 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 28, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.ARBITER),
    ItemNames.ARBITER_KHAYDARIN_CORE: ItemData(329 + SC2LOTV_ITEM_ID_OFFSET, "Forge 1", 29, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.ARBITER),
    ItemNames.ARBITER_SPACETIME_ANCHOR: ItemData(330 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 0, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.ARBITER),
    ItemNames.ARBITER_RESOURCE_EFFICIENCY: ItemData(331 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 1, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.ARBITER),
    ItemNames.ARBITER_ENHANCED_CLOAK_FIELD: ItemData(332 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 2, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.ARBITER),
    ItemNames.CARRIER_GRAVITON_CATAPULT:
        ItemData(333 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 3, SC2Race.PROTOSS, origin={"wol"},
                 parent_item=ItemNames.CARRIER,
                 description="Carriers can launch Interceptors more quickly."),
    ItemNames.CARRIER_HULL_OF_PAST_GLORIES:
        ItemData(334 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 4, SC2Race.PROTOSS, origin={"bw"},
                 parent_item=ItemNames.CARRIER,
                 description="Carriers gain +2 armour."),
    ItemNames.VOID_RAY_DESTROYER_FLUX_VANES:
        ItemData(335 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 5, SC2Race.PROTOSS, classification=ItemClassification.filler,
                 origin={"ext"},
                 description="Increases Void Ray and Destroyer movement speed."),
    ItemNames.DESTROYER_REFORGED_BLOODSHARD_CORE:
        ItemData(336 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 6, SC2Race.PROTOSS, origin={"ext"},
                 parent_item=ItemNames.DESTROYER,
                 description="When fully charged, the Destroyer's Destruction Beam weapon does full damage to secondary targets."),
    ItemNames.WARP_PRISM_GRAVITIC_DRIVE:
        ItemData(337 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 7, SC2Race.PROTOSS, classification=ItemClassification.filler,
                 origin={"ext"}, parent_item=ItemNames.WARP_PRISM,
                 description="Increases the movement speed of Warp Prisms."),
    ItemNames.WARP_PRISM_PHASE_BLASTER:
        ItemData(338 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 8, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"ext"}, parent_item=ItemNames.WARP_PRISM,
                 description="Equips Warp Prisms with an auto-attack that can hit ground and air targets."),
    ItemNames.WARP_PRISM_WAR_CONFIGURATION: ItemData(339 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 9, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.WARP_PRISM),
    ItemNames.OBSERVER_GRAVITIC_BOOSTERS: ItemData(340 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 10, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.OBSERVER),
    ItemNames.OBSERVER_SENSOR_ARRAY: ItemData(341 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 11, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.OBSERVER),
    ItemNames.REAVER_SCARAB_DAMAGE: ItemData(342 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 12, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.REAVER),
    ItemNames.REAVER_SOLARITE_PAYLOAD: ItemData(343 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 13, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.REAVER),
    ItemNames.REAVER_REAVER_CAPACITY: ItemData(344 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 14, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}, parent_item=ItemNames.REAVER),
    ItemNames.REAVER_RESOURCE_EFFICIENCY: ItemData(345 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 15, SC2Race.PROTOSS, origin={"bw"}, parent_item=ItemNames.REAVER),
    ItemNames.VANGUARD_AGONY_LAUNCHERS: ItemData(346 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 16, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.VANGUARD),
    ItemNames.VANGUARD_MATTER_DISPERSION: ItemData(347 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 17, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.VANGUARD),
    ItemNames.IMMORTAL_ANNIHILATOR_SINGULARITY_CHARGE: ItemData(348 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 18, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.IMMORTAL_ANNIHILATOR_ADVANCED_TARGETING_MECHANICS: ItemData(349 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 19, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.COLOSSUS_PACIFICATION_PROTOCOL: ItemData(350 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 20, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.COLOSSUS),
    ItemNames.WRATHWALKER_RAPID_POWER_CYCLING: ItemData(351 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 21, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.WRATHWALKER),
    ItemNames.WRATHWALKER_EYE_OF_WRATH: ItemData(352 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 22, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.WRATHWALKER),
    ItemNames.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_SHROUD_OF_ADUN: ItemData(353 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 23, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_SHADOW_GUARD_TRAINING: ItemData(354 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 24, SC2Race.PROTOSS, origin={"bw"}),
    ItemNames.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_BLINK: ItemData(355 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 25, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"ext"}),
    ItemNames.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_RESOURCE_EFFICIENCY: ItemData(356 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 26, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.DARK_TEMPLAR_DARK_ARCHON_MELD: ItemData(357 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 27, SC2Race.PROTOSS, origin={"bw"}, important_for_filtering=True ,parent_item=ItemNames.DARK_TEMPLAR),
    ItemNames.HIGH_TEMPLAR_SIGNIFIER_UNSHACKLED_PSIONIC_STORM: ItemData(358 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 28, SC2Race.PROTOSS, origin={"bw"}),
    ItemNames.HIGH_TEMPLAR_SIGNIFIER_HALLUCINATION: ItemData(359 + SC2LOTV_ITEM_ID_OFFSET, "Forge 2", 29, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"bw"}),
    ItemNames.HIGH_TEMPLAR_SIGNIFIER_KHAYDARIN_AMULET: ItemData(360 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 0, SC2Race.PROTOSS, origin={"bw"}),
    ItemNames.ARCHON_HIGH_ARCHON: ItemData(361 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 1, SC2Race.PROTOSS, origin={"ext"}, important_for_filtering=True),
    ItemNames.DARK_ARCHON_FEEDBACK: ItemData(362 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 2, SC2Race.PROTOSS, origin={"bw"}),
    ItemNames.DARK_ARCHON_MAELSTROM: ItemData(363 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 3, SC2Race.PROTOSS, origin={"bw"}),
    ItemNames.DARK_ARCHON_ARGUS_TALISMAN: ItemData(364 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 4, SC2Race.PROTOSS, origin={"bw"}),
    ItemNames.ASCENDANT_POWER_OVERWHELMING: ItemData(365 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 5, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ASCENDANT),
    ItemNames.ASCENDANT_CHAOTIC_ATTUNEMENT: ItemData(366 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 6, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ASCENDANT),
    ItemNames.ASCENDANT_BLOOD_AMULET: ItemData(367 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 7, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ASCENDANT),
    ItemNames.SENTRY_ENERGIZER_HAVOC_CLOAKING_MODULE: ItemData(368 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 8, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.SENTRY_ENERGIZER_HAVOC_SHIELD_BATTERY_RAPID_RECHARGING: ItemData(369 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 9, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.SENTRY_FORCE_FIELD: ItemData(370 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 10, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.SENTRY),
    ItemNames.SENTRY_HALLUCINATION: ItemData(371 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 11, SC2Race.PROTOSS, classification=ItemClassification.filler, origin={"ext"}, parent_item=ItemNames.SENTRY),
    ItemNames.ENERGIZER_RECLAMATION: ItemData(372 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 12, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ENERGIZER),
    ItemNames.ENERGIZER_FORGED_CHASSIS: ItemData(373 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 13, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.ENERGIZER),
    ItemNames.HAVOC_DETECT_WEAKNESS: ItemData(374 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 14, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.HAVOC),
    ItemNames.HAVOC_BLOODSHARD_RESONANCE: ItemData(375 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 15, SC2Race.PROTOSS, origin={"ext"}, parent_item=ItemNames.HAVOC),
    ItemNames.ZEALOT_SENTINEL_CENTURION_LEG_ENHANCEMENTS: ItemData(376 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 16, SC2Race.PROTOSS, origin={"bw"}),
    ItemNames.ZEALOT_SENTINEL_CENTURION_SHIELD_CAPACITY: ItemData(377 + SC2LOTV_ITEM_ID_OFFSET, "Forge 3", 17, SC2Race.PROTOSS, origin={"bw"}),

    # SoA Calldown powers
    ItemNames.SOA_CHRONO_SURGE: ItemData(700 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 0, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.SOA_PROGRESSIVE_PROXY_PYLON: ItemData(701 + SC2LOTV_ITEM_ID_OFFSET, "Progressive Upgrade", 0, SC2Race.PROTOSS, origin={"lotv"}, quantity=2),
    ItemNames.SOA_PYLON_OVERCHARGE: ItemData(702 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 1, SC2Race.PROTOSS, origin={"ext"}),
    ItemNames.SOA_ORBITAL_STRIKE: ItemData(703 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 2, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.SOA_TEMPORAL_FIELD: ItemData(704 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 3, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.SOA_SOLAR_LANCE: ItemData(705 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 4, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.SOA_MASS_RECALL: ItemData(706 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 5, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.SOA_SHIELD_OVERCHARGE: ItemData(707 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 6, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.SOA_DEPLOY_FENIX: ItemData(708 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 7, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.SOA_PURIFIER_BEAM: ItemData(709 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 8, SC2Race.PROTOSS, origin={"lotv"}),
    ItemNames.SOA_TIME_STOP: ItemData(710 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 9, SC2Race.PROTOSS, classification=ItemClassification.progression, origin={"lotv"}),
    ItemNames.SOA_SOLAR_BOMBARDMENT: ItemData(711 + SC2LOTV_ITEM_ID_OFFSET, "Spear of Adun", 10, SC2Race.PROTOSS, origin={"lotv"}),

    # Generic Protoss Upgrades
    ItemNames.MATRIX_OVERLOAD:
        ItemData(800 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 0, SC2Race.PROTOSS, origin={"lotv"},
                 description=r"All friendly units gain 25% movement speed and 15% attack speed within a Pylon's power field and for 15 seconds after leaving it."),
    ItemNames.QUATRO:
        ItemData(801 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 1, SC2Race.PROTOSS, origin={"ext"},
                 description="All friendly Protoss units gain the equivalent of their +1 armour, attack, and shield upgrades."),
    ItemNames.NEXUS_OVERCHARGE:
        ItemData(802 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 2, SC2Race.PROTOSS, origin={"lotv"},
                 important_for_filtering=True, description="The Protoss Nexus gains a long-range auto-attack."),
    ItemNames.ORBITAL_ASSIMILATORS:
        ItemData(803 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 3, SC2Race.PROTOSS, origin={"lotv"},
                 description="Assimilators automatically harvest Vespene Gas without the need for Probes."),
    ItemNames.WARP_HARMONIZATION:
        ItemData(804 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 4, SC2Race.PROTOSS, origin={"lotv"},
                 description=r"Stargates and Robotics Facilities can transform to utilize Warp In technology. Warp In cooldowns are 20% faster than original build times."),
    ItemNames.GUARDIAN_SHELL:
        ItemData(805 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 5, SC2Race.PROTOSS, origin={"lotv"},
                 description="The Spear of Adun passively shields friendly Protoss units before death, making them invulnerable for 5 seconds. Each unit can only be shielded once every 60 seconds."),
    ItemNames.RECONSTRUCTION_BEAM:
        ItemData(806 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 6, SC2Race.PROTOSS,
                 classification=ItemClassification.progression, origin={"lotv"},
                 description="The Spear of Adun will passively heal mechanical units for 5 and non-biological structures for 10 life per second. Up to 3 targets can be repaired at once."),
    ItemNames.OVERWATCH:
        ItemData(807 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 7, SC2Race.PROTOSS, origin={"ext"},
                 description="Once per second, the Spear of Adun will last-hit a damaged enemy unit that is below 50 health."),
    ItemNames.SUPERIOR_WARP_GATES:
        ItemData(808 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 8, SC2Race.PROTOSS, origin={"ext"},
                 description="Protoss Warp Gates can hold up to 3 charges of unit warp-ins."),
    ItemNames.ENHANCED_TARGETING:
        ItemData(809 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 9, SC2Race.PROTOSS, origin={"ext"},
                 description="Protoss defensive structures gain +2 range."),
    ItemNames.OPTIMIZED_ORDNANCE:
        ItemData(810 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 10, SC2Race.PROTOSS, origin={"ext"},
                 description="Increases the attack speed of Protoss defensive structures by 25%."),
    ItemNames.KHALAI_INGENUITY:
        ItemData(811 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 11, SC2Race.PROTOSS, origin={"ext"},
                 description="Pylons, Photon Cannons, Monoliths, and Shield Batteries warp in near-instantly."),
    ItemNames.AMPLIFIED_ASSIMILATORS:
        ItemData(812 + SC2LOTV_ITEM_ID_OFFSET, "Solarite Core", 12, SC2Race.PROTOSS, origin={"ext"},
                 description=r"Assimilators produce Vespene gas 25% faster."),
}


def get_item_table():
    return item_table


basic_units = {
    SC2Race.TERRAN: {
        ItemNames.MARINE,
        ItemNames.MARAUDER,
        ItemNames.GOLIATH,
        ItemNames.HELLION,
        ItemNames.VULTURE,
        ItemNames.WARHOUND,
    },
    SC2Race.ZERG: {
        ItemNames.ZERGLING,
        ItemNames.SWARM_QUEEN,
        ItemNames.ROACH,
        ItemNames.HYDRALISK,
    },
    SC2Race.PROTOSS: {
        ItemNames.ZEALOT,
        ItemNames.CENTURION,
        ItemNames.SENTINEL,
        ItemNames.STALKER,
        ItemNames.INSTIGATOR,
        ItemNames.SLAYER,
        ItemNames.DRAGOON,
        ItemNames.ADEPT,
    }
}

advanced_basic_units = {
    SC2Race.TERRAN: basic_units[SC2Race.TERRAN].union({
        ItemNames.REAPER,
        ItemNames.DIAMONDBACK,
        ItemNames.VIKING,
        ItemNames.SIEGE_TANK,
        ItemNames.BANSHEE,
        ItemNames.THOR,
        ItemNames.BATTLECRUISER,
        ItemNames.CYCLONE
    }),
    SC2Race.ZERG: basic_units[SC2Race.ZERG].union({
        ItemNames.INFESTOR,
        ItemNames.ABERRATION,
    }),
    SC2Race.PROTOSS: basic_units[SC2Race.PROTOSS].union({
        ItemNames.DARK_TEMPLAR,
        ItemNames.BLOOD_HUNTER,
        ItemNames.AVENGER,
        ItemNames.IMMORTAL,
        ItemNames.ANNIHILATOR,
        ItemNames.VANGUARD,
    })
}

no_logic_starting_units = {
    SC2Race.TERRAN: advanced_basic_units[SC2Race.TERRAN].union({
        ItemNames.FIREBAT,
        ItemNames.GHOST,
        ItemNames.SPECTRE,
        ItemNames.WRAITH,
        ItemNames.RAVEN,
        ItemNames.PREDATOR,
        ItemNames.LIBERATOR,
        ItemNames.HERC,
    }),
    SC2Race.ZERG: advanced_basic_units[SC2Race.ZERG].union({
        ItemNames.ULTRALISK,
        ItemNames.SWARM_HOST
    }),
    SC2Race.PROTOSS: advanced_basic_units[SC2Race.PROTOSS].union({
        ItemNames.CARRIER,
        ItemNames.TEMPEST,
        ItemNames.VOID_RAY,
        ItemNames.DESTROYER,
        ItemNames.COLOSSUS,
        ItemNames.WRATHWALKER,
        ItemNames.SCOUT,
        ItemNames.HIGH_TEMPLAR,
        ItemNames.SIGNIFIER,
        ItemNames.ASCENDANT,
        ItemNames.DARK_ARCHON,
        ItemNames.SUPPLICANT,
    })
}

not_balanced_starting_units = {
    ItemNames.SIEGE_TANK,
    ItemNames.THOR,
    ItemNames.BANSHEE,
    ItemNames.BATTLECRUISER,
    ItemNames.ULTRALISK,
    ItemNames.CARRIER,
    ItemNames.TEMPEST,
}


def get_basic_units(world: World, race: SC2Race) -> typing.Set[str]:
    logic_level = get_option_value(world, 'required_tactics')
    if logic_level == RequiredTactics.option_no_logic:
        return no_logic_starting_units[race]
    elif logic_level == RequiredTactics.option_advanced:
        return advanced_basic_units[race]
    else:
        return basic_units[race]


# Items that can be placed before resources if not already in
# General upgrades and Mercs
second_pass_placeable_items: typing.Tuple[str, ...] = (
    # Global weapon/armor upgrades
    ItemNames.PROGRESSIVE_TERRAN_ARMOR_UPGRADE,
    ItemNames.PROGRESSIVE_TERRAN_WEAPON_UPGRADE,
    ItemNames.PROGRESSIVE_TERRAN_WEAPON_ARMOR_UPGRADE,
    ItemNames.PROGRESSIVE_ZERG_ARMOR_UPGRADE,
    ItemNames.PROGRESSIVE_ZERG_WEAPON_UPGRADE,
    ItemNames.PROGRESSIVE_ZERG_WEAPON_ARMOR_UPGRADE,
    ItemNames.PROGRESSIVE_PROTOSS_ARMOR_UPGRADE,
    ItemNames.PROGRESSIVE_PROTOSS_WEAPON_UPGRADE,
    ItemNames.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE,
    ItemNames.PROGRESSIVE_PROTOSS_SHIELDS,
    # Terran Buildings without upgrades
    ItemNames.SENSOR_TOWER,
    ItemNames.HIVE_MIND_EMULATOR,
    ItemNames.PSI_DISRUPTER,
    ItemNames.PERDITION_TURRET,
    # Terran units without upgrades
    ItemNames.HERC,
    ItemNames.WARHOUND,
    # General Terran upgrades without any dependencies
    ItemNames.SCV_ADVANCED_CONSTRUCTION,
    ItemNames.SCV_DUAL_FUSION_WELDERS,
    ItemNames.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM,
    ItemNames.PROGRESSIVE_ORBITAL_COMMAND,
    ItemNames.ULTRA_CAPACITORS,
    ItemNames.VANADIUM_PLATING,
    ItemNames.ORBITAL_DEPOTS,
    ItemNames.MICRO_FILTERING,
    ItemNames.AUTOMATED_REFINERY,
    ItemNames.COMMAND_CENTER_REACTOR,
    ItemNames.TECH_REACTOR,
    ItemNames.CELLULAR_REACTOR,
    ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL,  # Place only L1
    ItemNames.STRUCTURE_ARMOR,
    ItemNames.HI_SEC_AUTO_TRACKING,
    ItemNames.ADVANCED_OPTICS,
    ItemNames.ROGUE_FORCES,
    # Mercenaries (All races)
    *[item_name for item_name, item_data in get_full_item_list().items()
      if item_data.type == "Mercenary"],
    # Kerrigan and Nova levels, abilities and generally useful stuff
    *[item_name for item_name, item_data in get_full_item_list().items()
      if item_data.type in ("Level", "Ability", "Evolution Pit", "Nova Gear")],
    ItemNames.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE,
    # Zerg static defenses
    ItemNames.SPORE_CRAWLER,
    ItemNames.SPINE_CRAWLER,
    # Defiler, Aberration (no upgrades)
    ItemNames.DEFILER,
    ItemNames.ABERRATION,
    # Spear of Adun Abilities
    ItemNames.SOA_CHRONO_SURGE,
    ItemNames.SOA_PROGRESSIVE_PROXY_PYLON,
    ItemNames.SOA_PYLON_OVERCHARGE,
    ItemNames.SOA_ORBITAL_STRIKE,
    ItemNames.SOA_TEMPORAL_FIELD,
    ItemNames.SOA_SOLAR_LANCE,
    ItemNames.SOA_MASS_RECALL,
    ItemNames.SOA_SHIELD_OVERCHARGE,
    ItemNames.SOA_DEPLOY_FENIX,
    ItemNames.SOA_PURIFIER_BEAM,
    ItemNames.SOA_TIME_STOP,
    ItemNames.SOA_SOLAR_BOMBARDMENT,
    # Protoss generic upgrades
    ItemNames.MATRIX_OVERLOAD,
    ItemNames.QUATRO,
    ItemNames.NEXUS_OVERCHARGE,
    ItemNames.ORBITAL_ASSIMILATORS,
    ItemNames.WARP_HARMONIZATION,
    ItemNames.GUARDIAN_SHELL,
    ItemNames.RECONSTRUCTION_BEAM,
    ItemNames.OVERWATCH,
    ItemNames.SUPERIOR_WARP_GATES,
    ItemNames.KHALAI_INGENUITY,
    ItemNames.AMPLIFIED_ASSIMILATORS,
    # Protoss static defenses
    ItemNames.PHOTON_CANNON,
    ItemNames.KHAYDARIN_MONOLITH,
    ItemNames.SHIELD_BATTERY
)


filler_items: typing.Tuple[str, ...] = (
    ItemNames.STARTING_MINERALS,
    ItemNames.STARTING_VESPENE,
    ItemNames.STARTING_SUPPLY,
)

# Defense rating table
# Commented defense ratings are handled in LogicMixin
defense_ratings = {
    ItemNames.SIEGE_TANK: 5,
    # "Maelstrom Rounds": 2,
    ItemNames.PLANETARY_FORTRESS: 3,
    # Bunker w/ Marine/Marauder: 3,
    ItemNames.PERDITION_TURRET: 2,
    ItemNames.VULTURE: 1,
    ItemNames.BANSHEE: 1,
    ItemNames.BATTLECRUISER: 1,
    ItemNames.LIBERATOR: 4,
    ItemNames.WIDOW_MINE: 1,
    # "Concealment (Widow Mine)": 1
}
zerg_defense_ratings = {
    ItemNames.PERDITION_TURRET: 2,
    # Bunker w/ Firebat: 2,
    ItemNames.LIBERATOR: -2,
    ItemNames.HIVE_MIND_EMULATOR: 3,
    ItemNames.PSI_DISRUPTER: 3,
}
air_defense_ratings = {
    ItemNames.MISSILE_TURRET: 2,
}

kerrigan_levels = [item_name for item_name, item_data in get_full_item_list().items()
                        if item_data.type == "Level" and item_data.race == SC2Race.ZERG]

spider_mine_sources = {
    ItemNames.VULTURE,
    ItemNames.REAPER_SPIDER_MINES,
    ItemNames.SIEGE_TANK_SPIDER_MINES,
    ItemNames.RAVEN_SPIDER_MINES,
}

progressive_if_nco = {
    ItemNames.MARINE_PROGRESSIVE_STIMPACK,
    ItemNames.FIREBAT_PROGRESSIVE_STIMPACK,
    ItemNames.BANSHEE_PROGRESSIVE_CROSS_SPECTRUM_DAMPENERS,
    ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL,
}

progressive_if_ext = {
    ItemNames.VULTURE_PROGRESSIVE_REPLENISHABLE_MAGAZINE,
    ItemNames.WRAITH_PROGRESSIVE_TOMAHAWK_POWER_CELLS,
    ItemNames.BATTLECRUISER_PROGRESSIVE_DEFENSIVE_MATRIX,
    ItemNames.BATTLECRUISER_PROGRESSIVE_MISSILE_PODS,
    ItemNames.THOR_PROGRESSIVE_IMMORTALITY_PROTOCOL,
    ItemNames.PROGRESSIVE_FIRE_SUPPRESSION_SYSTEM,
    ItemNames.DIAMONDBACK_PROGRESSIVE_TRI_LITHIUM_POWER_CELL,
    ItemNames.PROGRESSIVE_ORBITAL_COMMAND
}

kerrigan_actives: typing.List[typing.Set[str]] = [
    {ItemNames.KERRIGAN_KINETIC_BLAST, ItemNames.KERRIGAN_LEAPING_STRIKE},
    {ItemNames.KERRIGAN_CRUSHING_GRIP, ItemNames.KERRIGAN_PSIONIC_SHIFT},
    set(),
    {ItemNames.KERRIGAN_WILD_MUTATION, ItemNames.KERRIGAN_SPAWN_BANELINGS, ItemNames.KERRIGAN_MEND},
    set(),
    set(),
    {ItemNames.KERRIGAN_APOCALYPSE, ItemNames.KERRIGAN_SPAWN_LEVIATHAN, ItemNames.KERRIGAN_DROP_PODS},
]

kerrigan_passives: typing.List[typing.Set[str]] = [
    {ItemNames.KERRIGAN_HEROIC_FORTITUDE},
    {ItemNames.KERRIGAN_CHAIN_REACTION},
    {ItemNames.KERRIGAN_ZERGLING_RECONSTITUTION, ItemNames.KERRIGAN_IMPROVED_OVERLORDS, ItemNames.KERRIGAN_AUTOMATED_EXTRACTORS},
    set(),
    {ItemNames.KERRIGAN_TWIN_DRONES, ItemNames.KERRIGAN_MALIGNANT_CREEP, ItemNames.KERRIGAN_VESPENE_EFFICIENCY},
    {ItemNames.KERRIGAN_INFEST_BROODLINGS, ItemNames.KERRIGAN_FURY, ItemNames.KERRIGAN_ABILITY_EFFICIENCY},
    set(),
]

kerrigan_only_passives = {
    ItemNames.KERRIGAN_HEROIC_FORTITUDE, ItemNames.KERRIGAN_CHAIN_REACTION,
    ItemNames.KERRIGAN_INFEST_BROODLINGS, ItemNames.KERRIGAN_FURY, ItemNames.KERRIGAN_ABILITY_EFFICIENCY,
}

spear_of_adun_calldowns = {
    ItemNames.SOA_CHRONO_SURGE,
    ItemNames.SOA_PROGRESSIVE_PROXY_PYLON,
    ItemNames.SOA_PYLON_OVERCHARGE,
    ItemNames.SOA_ORBITAL_STRIKE,
    ItemNames.SOA_TEMPORAL_FIELD,
    ItemNames.SOA_SOLAR_LANCE,
    ItemNames.SOA_MASS_RECALL,
    ItemNames.SOA_SHIELD_OVERCHARGE,
    ItemNames.SOA_DEPLOY_FENIX,
    ItemNames.SOA_PURIFIER_BEAM,
    ItemNames.SOA_TIME_STOP,
    ItemNames.SOA_SOLAR_BOMBARDMENT
}

spear_of_adun_castable_passives = {
    ItemNames.RECONSTRUCTION_BEAM,
    ItemNames.OVERWATCH,
}

nova_equipment = {
    *[item_name for item_name, item_data in get_full_item_list().items()
      if item_data.type == "Nova Gear"],
    ItemNames.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE
}

# 'number' values of upgrades for upgrade bundle items
upgrade_numbers = [
    # Terran
    {0, 4, 8}, # Weapon
    {2, 6, 10}, # Armor
    {0, 2}, # Infantry
    {4, 6}, # Vehicle
    {8, 10}, # Starship
    {0, 2, 4, 6, 8, 10}, # All
    # Zerg
    {0, 2, 6}, # Weapon
    {4, 8}, # Armor
    {0, 2, 4}, # Ground
    {6, 8}, # Flyer
    {0, 2, 4, 6, 8}, # All
    # Protoss
    {0, 6}, # Weapon
    {2, 4, 8}, # Armor
    {0, 2}, # Ground, Shields are handled specially
    {6, 8}, # Air, Shields are handled specially
    {0, 2, 4, 6, 8}, # All
]
# 'upgrade_numbers' indices for all upgrades
upgrade_numbers_all = {
    SC2Race.TERRAN: 5,
    SC2Race.ZERG: 10,
    SC2Race.PROTOSS: 15,
}

# Names of upgrades to be included for different options
upgrade_included_names = [
    { # Individual Items
        ItemNames.PROGRESSIVE_TERRAN_INFANTRY_WEAPON,
        ItemNames.PROGRESSIVE_TERRAN_INFANTRY_ARMOR,
        ItemNames.PROGRESSIVE_TERRAN_VEHICLE_WEAPON,
        ItemNames.PROGRESSIVE_TERRAN_VEHICLE_ARMOR,
        ItemNames.PROGRESSIVE_TERRAN_SHIP_WEAPON,
        ItemNames.PROGRESSIVE_TERRAN_SHIP_ARMOR,
        ItemNames.PROGRESSIVE_ZERG_MELEE_ATTACK,
        ItemNames.PROGRESSIVE_ZERG_MISSILE_ATTACK,
        ItemNames.PROGRESSIVE_ZERG_GROUND_CARAPACE,
        ItemNames.PROGRESSIVE_ZERG_FLYER_ATTACK,
        ItemNames.PROGRESSIVE_ZERG_FLYER_CARAPACE,
        ItemNames.PROGRESSIVE_PROTOSS_GROUND_WEAPON,
        ItemNames.PROGRESSIVE_PROTOSS_GROUND_ARMOR,
        ItemNames.PROGRESSIVE_PROTOSS_SHIELDS,
        ItemNames.PROGRESSIVE_PROTOSS_AIR_WEAPON,
        ItemNames.PROGRESSIVE_PROTOSS_AIR_ARMOR,
    },
    { # Bundle Weapon And Armor
        ItemNames.PROGRESSIVE_TERRAN_WEAPON_UPGRADE,
        ItemNames.PROGRESSIVE_TERRAN_ARMOR_UPGRADE,
        ItemNames.PROGRESSIVE_ZERG_WEAPON_UPGRADE,
        ItemNames.PROGRESSIVE_ZERG_ARMOR_UPGRADE,
        ItemNames.PROGRESSIVE_PROTOSS_WEAPON_UPGRADE,
        ItemNames.PROGRESSIVE_PROTOSS_ARMOR_UPGRADE,
    },
    { # Bundle Unit Class
        ItemNames.PROGRESSIVE_TERRAN_INFANTRY_UPGRADE,
        ItemNames.PROGRESSIVE_TERRAN_VEHICLE_UPGRADE,
        ItemNames.PROGRESSIVE_TERRAN_SHIP_UPGRADE,
        ItemNames.PROGRESSIVE_ZERG_GROUND_UPGRADE,
        ItemNames.PROGRESSIVE_ZERG_FLYER_UPGRADE,
        ItemNames.PROGRESSIVE_PROTOSS_GROUND_UPGRADE,
        ItemNames.PROGRESSIVE_PROTOSS_AIR_UPGRADE,
    },
    { # Bundle All
        ItemNames.PROGRESSIVE_TERRAN_WEAPON_ARMOR_UPGRADE,
        ItemNames.PROGRESSIVE_ZERG_WEAPON_ARMOR_UPGRADE,
        ItemNames.PROGRESSIVE_PROTOSS_WEAPON_ARMOR_UPGRADE,
    }
]

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in get_full_item_list().items() if
                                            data.code}

# Map type to expected int
type_flaggroups: typing.Dict[SC2Race, typing.Dict[str, int]] = {
    SC2Race.ANY: {
        "Minerals": 0,
        "Vespene": 1,
        "Supply": 2,
        "Goal": 3,
        "Nothing Group": 4,
    },
    SC2Race.TERRAN: {
        "Armory 1": 0,
        "Armory 2": 1,
        "Armory 3": 2,
        "Armory 4": 3,
        "Armory 5": 4,
        "Armory 6": 5,
        "Progressive Upgrade": 6,  # Unit upgrades that exist multiple times (Stimpack / Super Stimpack)
        "Laboratory": 7,
        "Upgrade": 8,  # Weapon / Armor upgrades
        "Unit": 9,
        "Building": 10,
        "Mercenary": 11,
        "Nova Gear": 12,
        "Progressive Upgrade 2": 13,
    },
    SC2Race.ZERG: {
        "Ability": 0,
        "Mutation 1": 1,
        "Strain": 2,
        "Morph": 3,
        "Upgrade": 4,
        "Mercenary": 5,
        "Unit": 6,
        "Level": 7,
        "Primal Form": 8,
        "Evolution Pit": 9,
        "Mutation 2": 10,
        "Mutation 3": 11
    },
    SC2Race.PROTOSS: {
        "Unit": 0,
        "Unit 2": 1,
        "Upgrade": 2,  # Weapon / Armor upgrades
        "Building": 3,
        "Progressive Upgrade": 4,
        "Spear of Adun": 5,
        "Solarite Core": 6,
        "Forge 1": 7,
        "Forge 2": 8,
        "Forge 3": 9,
    }
}
