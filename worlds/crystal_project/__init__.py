import settings
import os
import typing
import threading
import pkgutil

from .Items import item_table, filler_items, get_item_names_per_category
from .Locations import get_locations
from .Regions import init_areas
from .Options import CrystalProjectOptions
from .rules import CrystalProjectLogic

from typing import List, Set, Dict, TextIO, Any
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, ItemClassification

#class CrystalProjectSettings(settings.Group):
    # class RomFile(settings.SNESRomPath):
    #     """Insert help text for host.yaml here."""

    # rom_file: RomFile = RomFile("MyGame.sfc")

class CrystalProjectWorld(World):
    """Insert description of the world/game here."""
    game = "Crystal Project"  # name of the game/world
    options_dataclass = CrystalProjectOptions
    options: CrystalProjectOptions
    #settings: typing.ClassVar[CrystalProjectSettings]  # will be automatically assigned from type hint
    topology_present = True  # show path to required location checks in spoiler

    item_name_to_id = {item: item_table[item].code for item in item_table}
    location_name_to_id = {location.name: location.code for location in get_locations(-1, None)}
    item_name_groups = get_item_names_per_category()

    def generate_early(self):
        self.multiworld.push_precollected(self.create_item("Item - Home Point Stone"))

        if self.options.startWithTreasureFinder:
            self.multiworld.push_precollected(self.create_item("Item - Treasure Finder"))

        if self.options.startWithMaps:
            self.multiworld.push_precollected(self.create_item("Item - Spawning Meadows Map"))
            self.multiworld.push_precollected(self.create_item("Item - Delende Map"))
            self.multiworld.push_precollected(self.create_item("Item - Pale Grotto Map"))
            self.multiworld.push_precollected(self.create_item("Item - Seaside Cliffs Map"))
            self.multiworld.push_precollected(self.create_item("Item - Draft Shaft Conduit Map"))
            self.multiworld.push_precollected(self.create_item("Item - Proving Meadows Map"))
            self.multiworld.push_precollected(self.create_item("Item - Soiled Den Map"))
            self.multiworld.push_precollected(self.create_item("Item - Yamagawa M.A. Map"))
            self.multiworld.push_precollected(self.create_item("Item - Skumparadise Map"))
            self.multiworld.push_precollected(self.create_item("Item - Capital Courtyard Map"))
            self.multiworld.push_precollected(self.create_item("Item - Capital Sequoia Map"))
            self.multiworld.push_precollected(self.create_item("Item - Jojo Sewers Map"))
            self.multiworld.push_precollected(self.create_item("Item - Greenshire Reprise Map"))
            self.multiworld.push_precollected(self.create_item("Item - Mercury Shrine Map"))
            self.multiworld.push_precollected(self.create_item("Item - Boomer Society Map"))
            self.multiworld.push_precollected(self.create_item("Item - Rolling Quintar Fields Map"))
            self.multiworld.push_precollected(self.create_item("Item - Quintar Nest Map"))
            self.multiworld.push_precollected(self.create_item("Item - Capital Jail Map"))
            self.multiworld.push_precollected(self.create_item("Item - Cobblestone Crag Map"))
            self.multiworld.push_precollected(self.create_item("Item - Okimoto N.S. Map"))
            self.multiworld.push_precollected(self.create_item("Item - Salmon Pass Map"))
            self.multiworld.push_precollected(self.create_item("Item - Salmon River Map"))
            self.multiworld.push_precollected(self.create_item("Item - Poseidon Shrine Map"))
            self.multiworld.push_precollected(self.create_item("Item - Poko Poko Desert Map"))
            self.multiworld.push_precollected(self.create_item("Item - Sara Sara Bazaar Map"))
            self.multiworld.push_precollected(self.create_item("Item - Sara Sara Beach Map"))
            self.multiworld.push_precollected(self.create_item("Item - Ancient Reservoir Map"))
            self.multiworld.push_precollected(self.create_item("Item - Shoudu Province Map"))
            self.multiworld.push_precollected(self.create_item("Item - The Undercity Map"))
            self.multiworld.push_precollected(self.create_item("Item - Beaurior Volcano Map"))
            self.multiworld.push_precollected(self.create_item("Item - Beaurior Rock Map"))
            self.multiworld.push_precollected(self.create_item("Item - The Sequoia Map"))
            self.multiworld.push_precollected(self.create_item("Item - Tall Tall Heights Map"))
            self.multiworld.push_precollected(self.create_item("Item - Slip Glide Ride Map"))
            self.multiworld.push_precollected(self.create_item("Item - Ganymede Shrine Map"))
            self.multiworld.push_precollected(self.create_item("Item - Quintar Reserve Map"))
            self.multiworld.push_precollected(self.create_item("Item - Quintar Sanctum Map"))
            self.multiworld.push_precollected(self.create_item("Item - Lake Delende Map"))
            self.multiworld.push_precollected(self.create_item("Item - Jidamba Tangle Map"))
            self.multiworld.push_precollected(self.create_item("Item - Jidamba Eaclaneya Map"))
            self.multiworld.push_precollected(self.create_item("Item - The Deep Sea Map"))
            self.multiworld.push_precollected(self.create_item("Item - The New World Map"))
            self.multiworld.push_precollected(self.create_item("Item - Continental Tram Map"))
            self.multiworld.push_precollected(self.create_item("Item - Castle Ramparts Map"))
            self.multiworld.push_precollected(self.create_item("Item - Salmon Bay Map"))
            self.multiworld.push_precollected(self.create_item("Item - Lands End Map"))
            self.multiworld.push_precollected(self.create_item("Item - Capital Pipeline Map"))
            self.multiworld.push_precollected(self.create_item("Item - Northern Cave Map"))
            self.multiworld.push_precollected(self.create_item("Item - The Depths Map"))
            self.multiworld.push_precollected(self.create_item("Item - The Open Sea Map"))
            self.multiworld.push_precollected(self.create_item("Item - Dione Shrine Map"))
            self.multiworld.push_precollected(self.create_item("Item - Neptune Shrine Map"))
            self.multiworld.push_precollected(self.create_item("Item - Castle Sequoia Map"))
            self.multiworld.push_precollected(self.create_item("Item - Ancient Labyrinth Map"))
            self.multiworld.push_precollected(self.create_item("Item - Quintar Mausoleum Map"))
            self.multiworld.push_precollected(self.create_item("Item - Basement Map"))
            self.multiworld.push_precollected(self.create_item("Item - Trial Caves Map"))
            self.multiworld.push_precollected(self.create_item("Item - Overpass Map"))
            self.multiworld.push_precollected(self.create_item("Item - Underpass Map"))
            self.multiworld.push_precollected(self.create_item("Item - River Cats Ego Map"))
            self.multiworld.push_precollected(self.create_item("Item - Northern Stretch Map"))
            self.multiworld.push_precollected(self.create_item("Item - Eastern Chasm Map"))
            self.multiworld.push_precollected(self.create_item("Item - Sequoia Athenaeum Map"))
            self.multiworld.push_precollected(self.create_item("Item - The Chalice of Tar Map"))
            self.multiworld.push_precollected(self.create_item("Item - Flyers Crag Map"))
            self.multiworld.push_precollected(self.create_item("Item - Flyers Lookout Map"))
            self.multiworld.push_precollected(self.create_item("Item - Jade Cavern Map"))
            self.multiworld.push_precollected(self.create_item("Item - The Old World Map"))

    def create_regions(self) -> None:
        init_areas(self, get_locations(self.player, self.options), self.options)

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return Item(name, data.classification, data.code, self.player)

    def create_items(self) -> None:
        pool = self.get_item_pool(self.get_excluded_items())

        self.multiworld.itempool += pool

    def get_filler_item_name(self) -> str:
        # traps go here if we have any
        # trap_chance: int = self.options.trap_chance.value
        # enabled_traps: List[str] = self.options.traps.value

        # if self.random.random() < (trap_chance / 100) and enabled_traps:
        #     return self.random.choice(enabled_traps)
        # else:
        #     return self.random.choice(filler_items) 
        return self.random.choice(filler_items)

    def get_excluded_items(self) -> Set[str]:
        excluded_items: Set[str] = set()
        excluded_items.add("Item - Home Point Stone")
        excluded_items.add("Job - Warrior")
        excluded_items.add("Job - Monk")
        excluded_items.add("Job - Rogue")
        excluded_items.add("Job - Cleric")
        excluded_items.add("Job - Wizard")
        excluded_items.add("Job - Warlock")

        if self.options.startWithTreasureFinder:
            excluded_items.add("Item - Treasure Finder")

        if self.options.startWithMaps:
            excluded_items.add("Item - Spawning Meadows Map")
            excluded_items.add("Item - Delende Map")
            excluded_items.add("Item - Pale Grotto Map")
            excluded_items.add("Item - Seaside Cliffs Map")
            excluded_items.add("Item - Draft Shaft Conduit Map")
            excluded_items.add("Item - Proving Meadows Map")
            excluded_items.add("Item - Soiled Den Map")
            excluded_items.add("Item - Yamagawa M.A. Map")
            excluded_items.add("Item - Skumparadise Map")
            excluded_items.add("Item - Capital Courtyard Map")
            excluded_items.add("Item - Capital Sequoia Map")
            excluded_items.add("Item - Jojo Sewers Map")
            excluded_items.add("Item - Greenshire Reprise Map")
            excluded_items.add("Item - Mercury Shrine Map")
            excluded_items.add("Item - Boomer Society Map")
            excluded_items.add("Item - Rolling Quintar Fields Map")
            excluded_items.add("Item - Quintar Nest Map")
            excluded_items.add("Item - Capital Jail Map")
            excluded_items.add("Item - Cobblestone Crag Map")
            excluded_items.add("Item - Okimoto N.S. Map")
            excluded_items.add("Item - Salmon Pass Map")
            excluded_items.add("Item - Salmon River Map")
            excluded_items.add("Item - Poseidon Shrine Map")
            excluded_items.add("Item - Poko Poko Desert Map")
            excluded_items.add("Item - Sara Sara Bazaar Map")
            excluded_items.add("Item - Sara Sara Beach Map")
            excluded_items.add("Item - Ancient Reservoir Map")
            excluded_items.add("Item - Shoudu Province Map")
            excluded_items.add("Item - The Undercity Map")
            excluded_items.add("Item - Beaurior Volcano Map")
            excluded_items.add("Item - Beaurior Rock Map")
            excluded_items.add("Item - The Sequoia Map")
            excluded_items.add("Item - Tall Tall Heights Map")
            excluded_items.add("Item - Slip Glide Ride Map")
            excluded_items.add("Item - Ganymede Shrine Map")
            excluded_items.add("Item - Quintar Reserve Map")
            excluded_items.add("Item - Quintar Sanctum Map")
            excluded_items.add("Item - Lake Delende Map")
            excluded_items.add("Item - Jidamba Tangle Map")
            excluded_items.add("Item - Jidamba Eaclaneya Map")
            excluded_items.add("Item - The Deep Sea Map")
            excluded_items.add("Item - The New World Map")
            excluded_items.add("Item - Continental Tram Map")
            excluded_items.add("Item - Castle Ramparts Map")
            excluded_items.add("Item - Salmon Bay Map")
            excluded_items.add("Item - Lands End Map")
            excluded_items.add("Item - Capital Pipeline Map")
            excluded_items.add("Item - Northern Cave Map")
            excluded_items.add("Item - The Depths Map")
            excluded_items.add("Item - The Open Sea Map")
            excluded_items.add("Item - Dione Shrine Map")
            excluded_items.add("Item - Neptune Shrine Map")
            excluded_items.add("Item - Castle Sequoia Map")
            excluded_items.add("Item - Ancient Labyrinth Map")
            excluded_items.add("Item - Quintar Mausoleum Map")
            excluded_items.add("Item - Basement Map")
            excluded_items.add("Item - Trial Caves Map")
            excluded_items.add("Item - Overpass Map")
            excluded_items.add("Item - Underpass Map")
            excluded_items.add("Item - River Cats Ego Map")
            excluded_items.add("Item - Northern Stretch Map")
            excluded_items.add("Item - Eastern Chasm Map")
            excluded_items.add("Item - Sequoia Athenaeum Map")
            excluded_items.add("Item - The Chalice of Tar Map")
            excluded_items.add("Item - Flyers Crag Map")
            excluded_items.add("Item - Flyers Lookout Map")
            excluded_items.add("Item - Jade Cavern Map")
            excluded_items.add("Item - The Old World Map")

        if self.options.goal == self.options.goal.option_astley:
            excluded_items.add("Item - New World Stone")

        if self.options.includeSummonAbilities == self.options.includeSummonAbilities.option_false:
            excluded_items.add("Summon - Shaku")
            excluded_items.add("Summon - Pamoa")
            excluded_items.add("Summon - Guaba")
            excluded_items.add("Summon - Niltsi")
            excluded_items.add("Summon - Ioske")
            excluded_items.add("Summon - Coyote")
            excluded_items.add("Summon - Tira")
            excluded_items.add("Summon - Juses")
            excluded_items.add("Summon - Pah")

        if self.options.includeScholarAbilities == self.options.includeScholarAbilities.option_false:
            excluded_items.add("Scholar - Roost")
            excluded_items.add("Scholar - Lucky Dice")
            excluded_items.add("Scholar - Sun Bath")
            excluded_items.add("Scholar - Sleep Aura")
            excluded_items.add("Scholar - Regenerate")
            excluded_items.add("Scholar - Reverse Polarity")
            excluded_items.add("Scholar - Barrier")
            excluded_items.add("Scholar - MP Sickle")
            excluded_items.add("Scholar - Adrenaline")
            excluded_items.add("Scholar - Fire Breath")
            excluded_items.add("Scholar - Explode")
            excluded_items.add("Scholar - Whirlwind")
            excluded_items.add("Scholar - Atmoshear")
            excluded_items.add("Scholar - Build Life")
            excluded_items.add("Scholar - Aero")
            excluded_items.add("Scholar - Insult")
            excluded_items.add("Scholar - Infusion")
            excluded_items.add("Scholar - Overload")
            excluded_items.add("Scholar - Reflection")
            excluded_items.add("Scholar - Lifegiver")

        if self.options.keyMode == self.options.keyMode.option_skeleton:
            excluded_items.add("Item - Luxury Key")
            excluded_items.add("Item - Gardeners Key")
            excluded_items.add("Item - South Wing Key")
            excluded_items.add("Item - East Wing Key")
            excluded_items.add("Item - West Wing Key")
            excluded_items.add("Item - Dark Wing Key")
            excluded_items.add("Item - Cell Key")
            excluded_items.add("Item - Room 1 Key")
            excluded_items.add("Item - Small Key")
            excluded_items.add("Item - Boss Key")
            excluded_items.add("Item - Red Door Key")
            excluded_items.add("Item - Ice Puzzle Key")
            excluded_items.add("Item - Rampart Key")
            excluded_items.add("Item - Forgotten Key")
            excluded_items.add("Item - Tram Key")
            excluded_items.add("Item - Courtyard Key")
            excluded_items.add("Item - Pyramid Key")
            excluded_items.add("Item - Foliage Key")
            excluded_items.add("Item - Cave Key")
            excluded_items.add("Item - Canopy Key")
            excluded_items.add("Item - Ice Cell Key")
            
        #all end_game_zone progression items get excluded here
        if (self.options.includedRegions == self.options.includedRegions.option_expert or
            self.options.includedRegions == self.options.includedRegions.option_advanced or
            self.options.includedRegions == self.options.includedRegions.option_beginner):
            #Swords
            excluded_items.add("Equipment - Kings Guard")
            excluded_items.add("Equipment - Oily Sword")
            #Axes
            excluded_items.add("Equipment - Aphotic Edge")
            excluded_items.add("Equipment - Decapitator")
            #Daggers
            excluded_items.add("Equipment - Sange")
            excluded_items.add("Equipment - Mages Pike")
            #Rapiers
            excluded_items.add("Equipment - Nightingale")
            #Spears
            excluded_items.add("Equipment - Royal Guard")
            #Bows
            excluded_items.add("Equipment - Dream Hunter")
            #Staves
            excluded_items.add("Equipment - Judgement")
            #Shields
            excluded_items.add("Equipment - Mirror Shield")
            #Heavy Body
            excluded_items.add("Equipment - Lunar Mail")
            #Medium Head
            excluded_items.add("Equipment - Battle Band")
            #Light Head
            excluded_items.add("Equipment - Vita Crown")
            excluded_items.add("Equipment - Protector")
            #Light Body
            excluded_items.add("Equipment - Archmage Vest")
            excluded_items.add("Equipment - Assassins Cloak")
            excluded_items.add("Equipment - Stealth Cape")
            #Accessories
            excluded_items.add("Equipment - Beads of Defense")
            excluded_items.add("Equipment - Hand of Midas")

        #all expert zone progression items get excluded here
        if (self.options.includedRegions == self.options.includedRegions.option_advanced or
            self.options.includedRegions == self.options.includedRegions.option_beginner):
            #Ore
            excluded_items.add("Item - Diamond Ore")
            excluded_items.add("Item - Diamond Ingot")
            excluded_items.add("Item - Diamond Dust")
            #Keys
            excluded_items.add("Item - Tram Key")
            excluded_items.add("Item - Small Key")
            excluded_items.add("Item - Boss Key")
            excluded_items.add("Item - Ice Cell Key")
            excluded_items.add("Item - Red Door Key")
            excluded_items.add("Item - Ice Puzzle Key")
            excluded_items.add("Item - Foliage Key")
            excluded_items.add("Item - Cave Key")
            excluded_items.add("Item - Canopy Key")
            excluded_items.add("Item - Rampart Key")
            excluded_items.add("Item - Forgotten Key")
            #Passes
            excluded_items.add("Item - Ferry Pass")
            #Key Items
            excluded_items.add("Item - Elevator Part")
            excluded_items.add("Item - Undersea Crab")
            excluded_items.add("Item - Vermillion Book")
            excluded_items.add("Item - Viridian Book")
            excluded_items.add("Item - Cerulean Book")
            #Teleport Stones
            excluded_items.add("Item - Ganymede Stone")
            excluded_items.add("Item - Triton Stone")
            excluded_items.add("Item - Callisto Stone")
            excluded_items.add("Item - Europa Stone")
            excluded_items.add("Item - Dione Stone")
            excluded_items.add("Item - Neptune Stone")
            #Swords
            excluded_items.add("Equipment - Cutlass")
            excluded_items.add("Equipment - Cold Touch")
            excluded_items.add("Equipment - Temporal Blade")
            excluded_items.add("Equipment - Defender")
            excluded_items.add("Equipment - Conquest")
            excluded_items.add("Equipment - Flame Sword")
            excluded_items.add("Equipment - Rune Sword")
            excluded_items.add("Equipment - Soul Keeper")
            excluded_items.add("Equipment - Crabs Claw")
            #Axes
            excluded_items.add("Equipment - Gaia Axe")
            #Daggers
            excluded_items.add("Equipment - Soul Kris")
            excluded_items.add("Equipment - Flamespike")
            excluded_items.add("Equipment - Yasha")
            #Rapiers
            excluded_items.add("Equipment - Fleuret")
            excluded_items.add("Equipment - Windsong")
            excluded_items.add("Equipment - Murgleys")
            #Katanas
            excluded_items.add("Equipment - Muramasa")
            #Spears
            excluded_items.add("Equipment - Halberd")
            excluded_items.add("Equipment - Radiance")
            excluded_items.add("Equipment - Partizan")
            #Scythes
            excluded_items.add("Equipment - Frost Reaper")
            excluded_items.add("Equipment - Gravedigger")
            excluded_items.add("Equipment - Wind Thresher")
            #Bows
            excluded_items.add("Equipment - Siege Bow")
            excluded_items.add("Equipment - Rune Bow")
            #Staves
            excluded_items.add("Equipment - Life Jewel")
            excluded_items.add("Equipment - Apprentice")
            excluded_items.add("Equipment - Sages Walker")
            excluded_items.add("Equipment - Staff of Balance")
            #Wands
            excluded_items.add("Equipment - Cursegiver")
            excluded_items.add("Equipment - Rune Wand")
            excluded_items.add("Equipment - Stardust Wand")
            excluded_items.add("Equipment - Paladin Wand")
            excluded_items.add("Equipment - Flameseeker")
            #Books
            excluded_items.add("Equipment - Tome of Light")
            excluded_items.add("Equipment - Dark Gospel")
            excluded_items.add("Equipment - Malifice")
            #Shields
            excluded_items.add("Equipment - The Immovable")
            excluded_items.add("Equipment - Flame Guard")
            excluded_items.add("Equipment - Wizards Wall")
            excluded_items.add("Equipment - Tower Shield")
            excluded_items.add("Equipment - Nomads Guard")
            #Heavy Head
            excluded_items.add("Equipment - Horned Helm")
            excluded_items.add("Equipment - Insignia Helm")
            excluded_items.add("Equipment - Demon Helm")
            excluded_items.add("Equipment - Spellsword Helm")
            #Heavy Body
            excluded_items.add("Equipment - Knights Plate")
            excluded_items.add("Equipment - Bone Mail")
            excluded_items.add("Equipment - Sky Armor")
            excluded_items.add("Equipment - Plate of Lion")
            excluded_items.add("Equipment - Demon Plate")
            excluded_items.add("Equipment - Plate of Whale")
            excluded_items.add("Equipment - Warrior Mail")
            excluded_items.add("Equipment - Warlock Mail")
            excluded_items.add("Equipment - Aegis Mail")
            excluded_items.add("Equipment - Reaper Mail")
            excluded_items.add("Equipment - Samurai Mail")
            excluded_items.add("Equipment - Valkyrie Mail")
            excluded_items.add("Equipment - Beastmaster Mail")
            excluded_items.add("Equipment - Mimic Mail")
            #Medium Head
            excluded_items.add("Equipment - Suitor Hat")
            excluded_items.add("Equipment - Pirate Hat")
            #Medium Body
            excluded_items.add("Equipment - Gaia Vest")
            excluded_items.add("Equipment - Brigandine")
            excluded_items.add("Equipment - Judo Gi")
            excluded_items.add("Equipment - Shadow Gi")
            excluded_items.add("Equipment - Monk Vest")
            excluded_items.add("Equipment - Rogue Vest")
            excluded_items.add("Equipment - Fencer Vest")
            excluded_items.add("Equipment - Hunter Vest")
            excluded_items.add("Equipment - Ninja Vest")
            excluded_items.add("Equipment - Nomad Vest")
            excluded_items.add("Equipment - Beatsmith Vest")
            excluded_items.add("Equipment - Assassin Vest")
            #Light Head
            excluded_items.add("Equipment - Plague Mask")
            excluded_items.add("Equipment - Guard Crown")
            excluded_items.add("Equipment - Bronze Hairpin")
            excluded_items.add("Equipment - Ravens Hood")
            excluded_items.add("Equipment - Celestial Crown")
            excluded_items.add("Equipment - Pointy Hat")
            #Light Body
            excluded_items.add("Equipment - Shelter Dress")
            excluded_items.add("Equipment - Blue Cape")
            excluded_items.add("Equipment - Seekers Garb")
            excluded_items.add("Equipment - Ravens Cloak")
            excluded_items.add("Equipment - Cleric Robe")
            excluded_items.add("Equipment - Wizard Robe")
            excluded_items.add("Equipment - Shaman Robe")
            excluded_items.add("Equipment - Scholar Robe")
            excluded_items.add("Equipment - Chemist Robe")
            excluded_items.add("Equipment - Dervish Robe")
            excluded_items.add("Equipment - Weaver Robe")
            excluded_items.add("Equipment - Summoner Robe")
            #Accessories
            excluded_items.add("Equipment - Knicked Knackers")
            excluded_items.add("Equipment - Looters Pin")
            excluded_items.add("Equipment - Acrobat Shoes")
            excluded_items.add("Equipment - Glasses")
            excluded_items.add("Equipment - Gusto Charm")
            excluded_items.add("Equipment - Muggers Glove")
            excluded_items.add("Equipment - Fursuit")
            excluded_items.add("Equipment - Sanity Ring")
            excluded_items.add("Equipment - Undead Ring")
            excluded_items.add("Equipment - Fairys Ring")
            excluded_items.add("Equipment - Oven Mitt")
            excluded_items.add("Equipment - Tall Stand Ring")
            excluded_items.add("Equipment - Nomads Emblem")
            excluded_items.add("Equipment - Ribbon")


        #all advanced zone progression items get excluded here
        if (self.options.includedRegions == self.options.includedRegions.option_beginner):
            #Consumables
            excluded_items.add("Item - Milk")
            excluded_items.add("Item - Shoudu Stew")
            excluded_items.add("Item - Rotten Salmon")
            excluded_items.add("Item - Fresh Salmon")
            #Ore
            excluded_items.add("Item - Silver Ore")
            excluded_items.add("Item - Silver Ingot")
            excluded_items.add("Item - Silver Dust")
            excluded_items.add("Item - Gold Ore")
            excluded_items.add("Item - Gold Ingot")
            excluded_items.add("Item - Gold Dust")
            #Keys
            excluded_items.add("Item - Gardeners Key")
            excluded_items.add("Item - Courtyard Key")
            excluded_items.add("Item - Luxury Key")
            excluded_items.add("Item - Cell Key")
            excluded_items.add("Item - South Wing Key")
            excluded_items.add("Item - East Wing Key")
            excluded_items.add("Item - West Wing Key")
            excluded_items.add("Item - Dark Wing Key")
            excluded_items.add("Item - Room 1 Key")
            excluded_items.add("Item - Pyramid Key")
            #Passes
            excluded_items.add("Item - Progressive Luxury Pass")
            #Key Items
            excluded_items.add("Item - Digested Head")
            excluded_items.add("Item - Lost Penguin")
            excluded_items.add("Item - West Lookout Token")
            excluded_items.add("Item - Central Lookout Token")
            excluded_items.add("Item - North Lookout Token")
            #Teleport Stones
            excluded_items.add("Item - Gaea Stone")
            excluded_items.add("Item - Poseidon Stone")
            excluded_items.add("Item - Mars Stone")
            #Swords
            excluded_items.add("Equipment - Craftwork Sword")
            excluded_items.add("Equipment - Boomer Sword")
            excluded_items.add("Equipment - Bloodbind")
            #Axes
            excluded_items.add("Equipment - Craftwork Axe")
            excluded_items.add("Equipment - Hunting Axe")
            excluded_items.add("Equipment - Hatchet")
            excluded_items.add("Equipment - Ragebringer")
            #Daggers
            excluded_items.add("Equipment - Craftwork Dagger")
            excluded_items.add("Equipment - Tanto")
            excluded_items.add("Equipment - Butterfly")
            excluded_items.add("Equipment - Ambush Knife")
            excluded_items.add("Equipment - Parry Knife")
            excluded_items.add("Equipment - Butter Cutter")
            #Rapiers
            excluded_items.add("Equipment - Craftwork Rapier")
            excluded_items.add("Equipment - Fish Skewer")
            excluded_items.add("Equipment - Dueller")
            #Katanas
            #excluded_items.add("Equipment - Craftwork Katana") beginners can have little a katana as a treat
            excluded_items.add("Equipment - Tachi")
            #Spears
            #excluded_items.add("Equipment - Craftwork Spear") beginners can have little a spear as a treat
            excluded_items.add("Equipment - Skewer")
            excluded_items.add("Equipment - Prodder")
            excluded_items.add("Equipment - Trident")
            #Scythes
            excluded_items.add("Equipment - Craftwork Scythe")
            excluded_items.add("Equipment - Grim Scythe")
            #Bows
            #excluded_items.add("Equipment - Craftwork Bow") beginners can have little a bow as a treat
            excluded_items.add("Equipment - Hunting Bow")
            #Staves
            excluded_items.add("Equipment - Craftwork Staff")
            excluded_items.add("Equipment - Iron Rod")
            excluded_items.add("Equipment - Walking Stick")
            excluded_items.add("Equipment - Knockout Stick")
            #Wands
            excluded_items.add("Equipment - Craftwork Wand")
            excluded_items.add("Equipment - Static Rod")
            excluded_items.add("Equipment - Storm Rod")
            #Books
            #excluded_items.add("Equipment - Craftwork Pages") beginners can have little a book as a treat
            excluded_items.add("Equipment - Gospel")
            excluded_items.add("Equipment - Paypirbak")
            excluded_items.add("Equipment - Art of War")
            excluded_items.add("Equipment - Blank Pages")
            #Shields
            excluded_items.add("Equipment - Craftwork Shield")
            excluded_items.add("Equipment - Lucky Platter")
            excluded_items.add("Equipment - Boomer Shield")
            excluded_items.add("Equipment - Mages Platter")
            #Heavy Head
            excluded_items.add("Equipment - Craftwork Helm")
            excluded_items.add("Equipment - Iron Helm")
            excluded_items.add("Equipment - Battle Helm")
            #Heavy Body
            excluded_items.add("Equipment - Plate of Wolf")
            excluded_items.add("Equipment - Craftwork Mail")
            excluded_items.add("Equipment - Iron Armor")
            excluded_items.add("Equipment - Battleplate")
            #Medium Head
            excluded_items.add("Equipment - Craftwork Cap")
            excluded_items.add("Equipment - Spore Blocker")
            excluded_items.add("Equipment - Red Cap")
            excluded_items.add("Equipment - Captains Hat")
            #Medium Body
            #excluded_items.add("Equipment - Craftwork Vest") beginners can have little a medium body as a treat
            excluded_items.add("Equipment - Smelly Gi")
            excluded_items.add("Equipment - Training Gi")
            excluded_items.add("Equipment - Tuxedo")
            excluded_items.add("Equipment - Red Coat")
            #Light Head
            excluded_items.add("Equipment - Craftwork Crown")
            excluded_items.add("Equipment - Circlet")
            excluded_items.add("Equipment - Woven Hood")
            #Light Body
            excluded_items.add("Equipment - Craftwork Robe")
            excluded_items.add("Equipment - Dress")
            excluded_items.add("Equipment - Woven Shirt")
            #Accessories
            excluded_items.add("Equipment - Fang Pendant")
            excluded_items.add("Equipment - Shell Amulet")
            excluded_items.add("Equipment - Magic Finder")
            excluded_items.add("Equipment - Learners Pin")
            excluded_items.add("Equipment - Givers Ring")
            excluded_items.add("Equipment - Aggro Band")
            excluded_items.add("Equipment - Float Shoes")
            excluded_items.add("Equipment - Defense Shifter")
            excluded_items.add("Equipment - Resist Shifter")
            excluded_items.add("Equipment - Scope Specs")
            excluded_items.add("Equipment - Springs Oath")
            excluded_items.add("Equipment - Lucky Socks")
            excluded_items.add("Equipment - Lucky Briefs")
            excluded_items.add("Equipment - Stone of Jodan")

        if self.options.randomizeJobs == self.options.randomizeJobs.option_false:
            excluded_items.add("Job - Fencer")
            excluded_items.add("Job - Shaman")
            excluded_items.add("Job - Scholar")
            excluded_items.add("Job - Aegis")
            excluded_items.add("Job - Hunter")
            excluded_items.add("Job - Chemist")
            excluded_items.add("Job - Reaper")
            excluded_items.add("Job - Ninja")
            excluded_items.add("Job - Nomad")
            excluded_items.add("Job - Dervish")
            excluded_items.add("Job - Beatsmith")
            excluded_items.add("Job - Samurai")
            excluded_items.add("Job - Assassin")
            excluded_items.add("Job - Valkyrie")
            excluded_items.add("Job - Summoner")
            excluded_items.add("Job - Beastmaster")
            excluded_items.add("Job - Weaver")
            excluded_items.add("Job - Mimic")

        return excluded_items

    def get_item_pool(self, excluded_items: Set[str]) -> List[Item]:
        pool: List[Item] = []

        for name, data in item_table.items():
            if name not in excluded_items:
                amount:int = data.beginnerAmount
                if self.options.includedRegions == self.options.includedRegions.option_advanced:
                    amount = amount + data.advancedAmount
                elif self.options.includedRegions == self.options.includedRegions.option_expert:
                    amount = amount + data.advancedAmount + data.expertAmount
                elif self.options.includedRegions == self.options.includedRegions.option_all:
                    amount = amount + data.advancedAmount + data.expertAmount + data.endGameAmount
                for _ in range(amount):
                    item = self.set_classifications(name)
                    pool.append(item)

        for _ in range (self.options.clamshellsInPool):
            item = self.set_classifications("Item - Clamshell")
            pool.append(item)

        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)):
            item = self.create_item(self.get_filler_item_name())
            pool.append(item)

        return pool

    def set_classifications(self, name: str) -> Item:
        data = item_table[name]
        item = Item(name, data.classification, data.code, self.player)

        return item

    def set_rules(self) -> None:
        logic = CrystalProjectLogic(self.player, self.options)
        win_condition_item: str
        if self.options.goal == self.options.goal.option_astley:
            win_condition_item = "Item - New World Stone" # todo should this still be here if we auto-hand you the stone?
        elif self.options.goal == self.options.goal.option_true_astley:
            win_condition_item = "Item - Old World Stone"
        elif self.options.goal == self.options.goal.option_clamshells:
            win_condition_item = "Item - Clamshell"
        
        if self.options.goal == 0:
            self.multiworld.completion_condition[self.player] = lambda state: logic.has_jobs(state, self.options.newWorldStoneJobQuantity)
        if self.options.goal == 1:
            self.multiworld.completion_condition[self.player] = lambda state: state.has(win_condition_item, self.player)
        if self.options.goal == 2:
            self.multiworld.completion_condition[self.player] = lambda state: state.has(win_condition_item, self.player, self.options.clamshellsQuantity.value)

    # This is data that needs to be readable from within the modded version of the game.
        # Example job rando makes the crystals behave differently, so the game needs to know about it.
    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {}
    
        slot_data = {
            "goal": self.options.goal.value,
            "clamshellsQuantity": self.options.clamshellsQuantity.value,
            "randomizeJobs": bool(self.options.randomizeJobs.value),
            "jobGoalAmount": self.options.newWorldStoneJobQuantity.value,
            "startWithMaps": bool(self.options.startWithMaps.value),
            "includedRegions": self.options.includedRegions.value
        }
    
        return slot_data