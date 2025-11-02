from typing import Dict, TYPE_CHECKING

from Rac3Addresses import RAC3REGION, RAC3TAG
from .Types import EventData, LocData

if TYPE_CHECKING:
    from . import RaC3World


def get_total_locations(world: "RaC3World") -> int:
    locations = [l for l in world.multiworld.get_locations() if l.player == world.player]
    return len(locations)


def get_location_names() -> Dict[str, int]:
    names = {name: data.ap_code for name, data in location_table.items()}
    return names


def get_regions() -> list:
    regions = [data.region for _, data in location_table.items()]
    return regions


rac3_locations = {
    # ----- Planet Veldin -----#
    "Veldin: First Ranger": LocData(50010000, RAC3REGION.VELDIN),
    "Veldin: Second Ranger": LocData(50010001, RAC3REGION.VELDIN),
    "Veldin: Save Veldin": LocData(50010002, RAC3REGION.VELDIN),

    # ----- Planet Florana -----#
    "Florana: Received Plasma Whip": LocData(50020000, RAC3REGION.FLORANA),
    "Florana: Received N60 Storm": LocData(50020001, RAC3REGION.FLORANA),
    "Florana: T-Bolt: Below Gadgetron Vendor": LocData(50020002, RAC3REGION.FLORANA),
    "Florana: T-Bolt: Path of Death": LocData(50020003, RAC3REGION.FLORANA),
    "Florana: Defeat Qwark": LocData(50020004, RAC3REGION.FLORANA),
    "Florana: Skill Point: Stay Squeaky Clean": LocData(50020005, RAC3REGION.FLORANA),
    "Florana: Trophy: 2nd Building Upstairs North-East": LocData(50020006, RAC3REGION.FLORANA),  # Ratchet Trophy

    # ----- Starship Phoenix -----#
    "Phoenix: Received Suck Cannon": LocData(50030000, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Received Infector": LocData(50030001, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Received Magna Plate Armor": LocData(50030002, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Received Adamantine Armor": LocData(50030003, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Received Aegis Mark V Armor": LocData(50030004, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Received Infernox Armor": LocData(50030005, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Meet Sasha on the Bridge": LocData(50030006, RAC3REGION.STARSHIP_PHOENIX),  # Infobot: Marcadia
    "Phoenix: Post Hideout Assault": LocData(50030007, RAC3REGION.STARSHIP_PHOENIX),  # Infobot: Koros
    "Phoenix: Return after winning Grand Prize Bout": LocData(50030009, RAC3REGION.STARSHIP_PHOENIX),
    # Infobot: Aquatos
    "Phoenix: Deliver the Star Map to Qwark": LocData(50030010, RAC3REGION.STARSHIP_PHOENIX),  # Infobot: Tyhrranosis
    "Phoenix: VR Training after Noid Queen": LocData(50030011, RAC3REGION.STARSHIP_PHOENIX),  # Infobot: Daxx
    "Phoenix: T-Bolt: VR Gadget Training": LocData(50030015, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Received Hacker": LocData(50030016, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Received Hypershot": LocData(50030017, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: VR: VR Gadget Training": LocData(50030018, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: VR: Warm Up": LocData(50030019, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: VR: Don't Look Down": LocData(50030020, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: VR: Speed Round": LocData(50030021, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: VR: Hot Stepper": LocData(50030022, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: VR: 90 Second Slayer": LocData(50030023, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: VR: The Shocker": LocData(50030024, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: VR: Wrench Beatdown": LocData(50030025, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: VR: Nerves of Titanium": LocData(50030026, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: T-Bolt: VR Nerves of Titanium": LocData(50030027, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Give Al the Master Plan": LocData(50030029, RAC3REGION.STARSHIP_PHOENIX),  # VidComic 5
    "Phoenix: Skill Point: Turn Up The Heat!": LocData(50030030, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Skill Point: Strive for Arcade Perfection": LocData(50030031, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Skill Point: Beat Helga's Best VR Time": LocData(50030032, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Skill Point: Monkeying Around": LocData(50030033, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Long Term Trophy: Titanium Collector": LocData(50030034, RAC3REGION.LONG_TROPHIES),
    # All Titanium Bolts collected
    "Phoenix: Long Term Trophy: Friend of the Rangers": LocData(50030035, RAC3REGION.LONG_TROPHIES),
    # All optional Ranger missions completed
    "Phoenix: Long Term Trophy: Annihilation Nation Champion": LocData(50030036, RAC3REGION.LONG_TROPHIES),
    # All Arena completed
    "Phoenix: Long Term Trophy: Skill Master": LocData(50030037, RAC3REGION.LONG_TROPHIES),
    # All Skill Points collected

    # VidComics
    "Phoenix: Play VidComic 1": LocData(50030008, RAC3REGION.STARSHIP_PHOENIX),  # Infobot: Annihilation Nation
    "Phoenix: Qwark VidComic 1 Clear": LocData(50310000, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: T-Bolt: VidComic 1 100%": LocData(50310001, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Skill Point: Pirate booty - set a new record for qwark": LocData(50310003, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Qwark VidComic 2 Clear": LocData(50330000, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: T-Bolt: VidComic 2 100%": LocData(50330001, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Skill Point: Arriba Amoeba! - set a new record for qwark": LocData(50330003, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Qwark VidComic 3 Clear": LocData(50340000, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: T-Bolt: VidComic 3 100%": LocData(50340001, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Skill Point: Shadow of the robot - set a new record for qwark": LocData(50340003,
                                                                                      RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Play VidComic 4": LocData(50030012, RAC3REGION.STARSHIP_PHOENIX),  # Infobot: Metropolis
    "Phoenix: Qwark VidComic 4 Clear": LocData(50320000, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: T-Bolt: VidComic 4 100%": LocData(50320001, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Skill Point: Deja Q All over Again - set a new record for qwark": LocData(50320003,
                                                                                        RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Qwark VidComic 5 Clear": LocData(50350000, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: T-Bolt: VidComic 5 100%": LocData(50350001, RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Skill Point: The Shaming of the Q - set a new record for qwark": LocData(50350003,
                                                                                       RAC3REGION.STARSHIP_PHOENIX),
    "Phoenix: Play VidComic 5": LocData(50030014, RAC3REGION.STARSHIP_PHOENIX),  # Infobot: Qwarks Hideout

    # ----- Planet Marcadia -----#
    "Marcadia: Received Spitting Hydra": LocData(50040000, RAC3REGION.MARCADIA),
    "Marcadia: Received Refractor": LocData(50040001, RAC3REGION.MARCADIA),
    "Marcadia: T-Bolt: After Pool of Water": LocData(50040002, RAC3REGION.MARCADIA),
    "Marcadia: T-Bolt: Last Refractor Room": LocData(50040003, RAC3REGION.MARCADIA),
    "Marcadia: T-Bolt: Ceiling just before Al": LocData(50040004, RAC3REGION.MARCADIA),
    "Marcadia: Meet Al": LocData(50040005, RAC3REGION.MARCADIA),
    "Marcadia: Operation IRON SHIELD: Secure the Area": LocData(50040006, RAC3REGION.MARCADIA),
    "Marcadia: Operation IRON SHIELD: Air Assault": LocData(50040007, RAC3REGION.MARCADIA),
    "Marcadia: Operation IRON SHIELD: Turret Command": LocData(50040008, RAC3REGION.MARCADIA),
    "Marcadia: Operation IRON SHIELD: Under the Gun": LocData(50040009, RAC3REGION.MARCADIA),
    "Marcadia: Operation IRON SHIELD: Hit n' Run": LocData(50040010, RAC3REGION.MARCADIA),
    "Marcadia: Skill Point: Reflect on how to score": LocData(50040011, RAC3REGION.MARCADIA),

    # ----- Annihilation Nation -----#
    "Annihilation: Received Agents of Doom": LocData(50070000, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: Received Tyhrra-Guise": LocData(50070001, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: T-Bolt: Heat Street": LocData(50070002, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: T-Bolt: Maze of Blaze": LocData(50070003, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Grand Prize Bout": LocData(50070004, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: The Terrible Two": LocData(50070005, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: Robot Rampage": LocData(50070006, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: Two Minute Warning": LocData(50070007, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: 90 Seconds of Carnage": LocData(50070008, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: Onslaught": LocData(50070009, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: Whip it Good": LocData(50070010, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: Hydra'n Seek": LocData(50070011, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: Championship Bout": LocData(50070012, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: Meet Courtney - Arena": LocData(50070013, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Ninja Challenge": LocData(50070014, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Counting Ducks": LocData(50070015, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Cycling Weapons": LocData(50070016, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: One Hit Wonder": LocData(50070017, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Time to Suck": LocData(50070018, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Naptime": LocData(50070019, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: More Cycling Weapons": LocData(50070020, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Dodge the Twins": LocData(50070021, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Chop Chop": LocData(50070022, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Sleep Inducer": LocData(50070023, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: The Other White Meat": LocData(50070024, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Championship Bout II": LocData(50070025, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Qwarktastic Battle": LocData(50070026, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Heat Street": LocData(50070027, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: Crispy Critter": LocData(50070028, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: Pyro Playground": LocData(50070029, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: Suicide Run": LocData(50070030, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: BBQ Boulevard": LocData(50070031, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Maze of Blaze": LocData(50070032, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Cremation Station": LocData(50070033, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: The Annihilator (Gauntlet)": LocData(50070034, RAC3REGION.ANNIHILATION_NATION_2),
    # "Annihilation: Qwark VidComic 2": LocData(50070035, RAC3REGION.ANNIHILATION_NATION),
    # "Annihilation: Qwark VidComic 3": LocData(50070036, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Skill Point: Bash the bug": LocData(50070037, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Skill Point: Be an eight time champ": LocData(50070038, RAC3REGION.ANNIHILATION_NATION_2),
    "Annihilation: Skill Point: Flee Flawlessly": LocData(50070039, RAC3REGION.ANNIHILATION_NATION),
    "Annihilation: Skill Point: Lights, camera action!": LocData(50070040, RAC3REGION.ANNIHILATION_NATION),

    # ----- Planet Aquatos -----#
    "Aquatos: Received Flux Rifle": LocData(50080000, RAC3REGION.AQUATOS),
    "Aquatos: T-Bolt: Under the Bridge": LocData(50080001, RAC3REGION.AQUATOS),
    "Aquatos: T-Bolt: Underwater Bolt": LocData(50080002, RAC3REGION.AQUATOS),
    "Aquatos: T-Bolt: Behind the Locked Gate": LocData(50080003, RAC3REGION.AQUATOS),
    "Aquatos: Skill Point: Search for sunken treasure": LocData(50080004, RAC3REGION.AQUATOS),
    "Aquatos: Received Mini-Turret Glove": LocData(50080005, RAC3REGION.AQUATOS),
    "Aquatos: Received Lava Gun": LocData(50080006, RAC3REGION.AQUATOS),
    "Aquatos: Received Shield Charger": LocData(50080007, RAC3REGION.AQUATOS),  # Command Center
    "Aquatos: Received Bouncer": LocData(50080008, RAC3REGION.AQUATOS),  # Qwarks Hideout
    "Aquatos: Received Plasma Coil": LocData(50080009, RAC3REGION.AQUATOS),  # Koros
    # Base
    # Sewers
    "Aquatos: T-Bolt: Top Left Bolt": LocData(50280000, RAC3REGION.AQUATOS_SEWERS),
    "Aquatos: T-Bolt: Swinging Bolt": LocData(50280001, RAC3REGION.AQUATOS_SEWERS),
    "Aquatos: 1 Sewer Crystal Traded": LocData(50280002, RAC3REGION.AQUATOS_SEWERS),
    "Aquatos: 5 Sewer Crystals Traded": LocData(50280003, RAC3REGION.AQUATOS_SEWERS),
    "Aquatos: 10 Sewer Crystals Traded": LocData(50280004, RAC3REGION.AQUATOS_SEWERS),
    "Aquatos: 20 Sewer Crystals Traded": LocData(50280005, RAC3REGION.AQUATOS_SEWERS),
    "Aquatos: Skill Point: Hit the motherload": LocData(50280006, RAC3REGION.AQUATOS_SEWERS),

    # ----- Planet Tyhrranosis -----#
    "Tyhrranosis: Received Annihilator": LocData(50090000, RAC3REGION.TYHRRANOSIS),
    "Tyhrranosis: Received Holo-Shield Glove": LocData(50090001, RAC3REGION.TYHRRANOSIS),
    "Tyhrranosis: T-Bolt: South East Cannon": LocData(50090002, RAC3REGION.TYHRRANOSIS),
    "Tyhrranosis: T-Bolt: Underground Cave Bolt": LocData(50090003, RAC3REGION.TYHRRANOSIS),
    "Tyhrranosis: Destroy the Momma Tyhrranoid": LocData(50090004, RAC3REGION.TYHRRANOSIS),
    "Tyhrranosis: Skill Point: Be a Sharpshooter": LocData(50090005, RAC3REGION.TYHRRANOSIS),
    "Tyhrranosis: Trophy: North East Pillar": LocData(50090006, RAC3REGION.TYHRRANOSIS),  # Al Trophy
    # Missions
    "Tyhrranosis: Operation ISLAND STRIKE: Assault on Kavu Island": LocData(50290000, RAC3REGION.TYHRRANOSIS_MISSION),
    "Tyhrranosis: Operation ISLAND STRIKE: Dogfight over Kavu Island": LocData(50290001,
                                                                               RAC3REGION.TYHRRANOSIS_MISSION),
    "Tyhrranosis: Operation ISLAND STRIKE: Operation Thunderbolt": LocData(50290002, RAC3REGION.TYHRRANOSIS_MISSION),
    "Tyhrranosis: Operation ISLAND STRIKE: The Final Battle": LocData(50290003, RAC3REGION.TYHRRANOSIS_MISSION),

    # ----- Planet Daxx -----#
    "Daxx: Infiltrate Weapons Facility": LocData(50050000, RAC3REGION.DAXX),
    "Daxx: T-Bolt: Right of the Taxi": LocData(50050001, RAC3REGION.DAXX),
    "Daxx: T-Bolt: Time Sensitive Door": LocData(50050002, RAC3REGION.DAXX),
    "Daxx: Received Charge Boots": LocData(50050003, RAC3REGION.DAXX),
    "Daxx: Gunship": LocData(50050004, RAC3REGION.DAXX),
    "Daxx: Skill Point: Bugs to Birdie": LocData(50050005, RAC3REGION.DAXX),
    # In the vanilla game you get the quack-o-ray on Aridia, but the skill point is done on Daxx
    "Daxx: Trophy: Ledge overlooking Ship": LocData(50050006, RAC3REGION.DAXX),  # Plumber Trophy

    # ----- Obani Gemini -----#
    "Obani Gemini: Received Disc-Blade Gun": LocData(50110000, RAC3REGION.OBANI_GEMINI),
    "Obani Gemini: T-Bolt: Follow the Lava": LocData(50110001, RAC3REGION.OBANI_GEMINI),
    "Obani Gemini: T-Bolt: Between the Twin Towers": LocData(50110002, RAC3REGION.OBANI_GEMINI),
    "Obani Gemini: Infobot: Blackwater City": LocData(50110003, RAC3REGION.OBANI_GEMINI),
    "Obani Gemini: Skill Point: Get to the belt": LocData(50110004, RAC3REGION.OBANI_GEMINI),

    # ----- Planet Blackwater City -----#
    "Blackwater City: Received Gravity Boots": LocData(50120000, RAC3REGION.BLACKWATER_CITY),
    "Blackwater City: Infobot: Holostar Studios": LocData(50120001, RAC3REGION.BLACKWATER_CITY),
    # Annihilation Nation 2 Courtney
    "Blackwater City: Operation BLACK TIDE: The Battle of Blackwater City": LocData(50120002,
                                                                                    RAC3REGION.BLACKWATER_CITY),
    "Blackwater City: Operation BLACK TIDE: The Bridge": LocData(50120003, RAC3REGION.BLACKWATER_CITY),
    "Blackwater City: Operation BLACK TIDE: Counterattack": LocData(50120004, RAC3REGION.BLACKWATER_CITY),
    "Blackwater City: Skill Point: Bash the party": LocData(50120005, RAC3REGION.BLACKWATER_CITY),

    # ----- Holostar Studios -----#
    "Holostar: Received Rift Inducer": LocData(50130000, RAC3REGION.HOLOSTAR_STUDIOS),
    "Holostar: T-Bolt: Atop the Chairs": LocData(50130001, RAC3REGION.HOLOSTAR_STUDIOS),
    "Holostar: T-Bolt: Lot 42's Gravity Ramp": LocData(50130002, RAC3REGION.HOLOSTAR_STUDIOS),
    "Holostar: T-Bolt: Kamikaze Noids": LocData(50130003, RAC3REGION.HOLOSTAR_STUDIOS),
    "Holostar: Skill Point: Feeling Lucky?": LocData(50130005, RAC3REGION.HOLOSTAR_STUDIOS),
    "Holostar: Trophy: After tall Elevator": LocData(50130006, RAC3REGION.HOLOSTAR_STUDIOS),  # Clank Trophy

    # ----- Skidd Cutscene -----#
    "Skidd is captured": LocData(50130004, "Skidd Cutscene"),  # Blackwater City and Holostar completed

    # ----- Obani Draco (lol) -----#
    "Obani Draco: Defeat Courtney Gears": LocData(50210000, RAC3REGION.OBANI_DRACO),  # Infobot: Zeldrin Starport

    # ----- Zeldrin Starport -----#
    "Zeldrin Starport: Received Bolt Grabber V2": LocData(50100000, RAC3REGION.ZELDRIN_STARPORT),
    "Zeldrin Starport: T-Bolt: Inside the Second Ship": LocData(50100001, RAC3REGION.ZELDRIN_STARPORT),
    "Zeldrin Starport: T-Bolt: Atop the Twin Shooters": LocData(50100002, RAC3REGION.ZELDRIN_STARPORT),
    "Zeldrin Starport: Escape the Exploding Ship": LocData(50100003, RAC3REGION.ZELDRIN_STARPORT),  # VidComic 4

    # ----- Planet Metropolis -----#
    "Metropolis: T-Bolt: Across the Gap": LocData(50160000, RAC3REGION.METROPOLIS),
    "Metropolis: Skill Point: 2002 was a good year in the city": LocData(50160001, RAC3REGION.METROPOLIS),
    "Metropolis: Metal-Noids": LocData(50160002, RAC3REGION.METROPOLIS),
    "Metropolis: T-Bolt: Before Grav-wall": LocData(50160003, RAC3REGION.METROPOLIS),
    "Metropolis: Defeat Klunk": LocData(50160004, RAC3REGION.METROPOLIS_MISSION),  # Infobot: Crash Site
    "Metropolis: Trophy: 2nd Building Window": LocData(50160005, RAC3REGION.METROPOLIS),  # Skrunch Trophy
    # Missions
    "Metropolis: T-Bolt: Tall Tower (Hovership)": LocData(50260000, RAC3REGION.METROPOLIS_MISSION),
    "Metropolis: Operation URBAN STORM: Countdown": LocData(50260001, RAC3REGION.METROPOLIS_MISSION),
    "Metropolis: Operation URBAN STORM: Urban Combat": LocData(50260002, RAC3REGION.METROPOLIS_MISSION),
    "Metropolis: Operation URBAN STORM: Tower Attack": LocData(50260003, RAC3REGION.METROPOLIS_MISSION),
    "Metropolis: Operation URBAN STORM: Air Superiority": LocData(50260004, RAC3REGION.METROPOLIS_MISSION),
    "Metropolis: Operation URBAN STORM: Turret Command": LocData(50260005, RAC3REGION.METROPOLIS_MISSION),
    "Metropolis: Received Map-O-Matic": LocData(50260006, RAC3REGION.METROPOLIS_MISSION),

    # ----- Planet Crash Site -----#
    "Crash Site: T-Bolt: Turn Around": LocData(50170000, RAC3REGION.CRASH_SITE),
    "Crash Site: Received Nano-Pak": LocData(50170001, RAC3REGION.CRASH_SITE),
    "Crash Site: Escape Pod": LocData(50170002, RAC3REGION.CRASH_SITE),
    "Crash Site: Infobot: Aridia": LocData(50170003, RAC3REGION.CRASH_SITE),
    "Crash Site: Skill Point: Suck it up!": LocData(50170004, RAC3REGION.CRASH_SITE),
    "Crash Site: Skill Point: Aim High": LocData(50170005, RAC3REGION.CRASH_SITE),
    "Crash Site: Trophy: Near first corner": LocData(50170006, RAC3REGION.CRASH_SITE),  # Nefarious Trophy

    # ----- Planet Aridia -----#
    "Aridia: Received Warp Pad": LocData(50180000, RAC3REGION.ARIDIA),
    "Aridia: Received Qwack-O-Ray": LocData(50180001, RAC3REGION.ARIDIA),
    "Aridia: T-Bolt: Under the Bridge (Assassination)": LocData(50180002, RAC3REGION.ARIDIA),
    "Aridia: T-Bolt: Behind the Base (X12 Endgame)": LocData(50180003, RAC3REGION.ARIDIA),
    "Aridia: Operation DEATH VALLEY: The Tunnels of Outpost X12": LocData(50180004, RAC3REGION.ARIDIA),
    "Aridia: Operation DEATH VALLEY: Ambush in Red Rock Valley": LocData(50180005, RAC3REGION.ARIDIA),
    "Aridia: Operation DEATH VALLEY: Assassination": LocData(50180006, RAC3REGION.ARIDIA),
    "Aridia: Operation DEATH VALLEY: Reclaim the Valley": LocData(50180007, RAC3REGION.ARIDIA),
    "Aridia: Operation DEATH VALLEY: X12 Endgame": LocData(50180008, RAC3REGION.ARIDIA),
    "Aridia: Skill Point: Go for hang time": LocData(50180009, RAC3REGION.ARIDIA),
    "Aridia: Skill Point: Zap back at ya'": LocData(50180010, RAC3REGION.ARIDIA),

    # ----- Qwark's Hideout -----#
    "Qwarks Hideout: Received Gadgetron PDA": LocData(50190000, RAC3REGION.QWARKS_HIDEOUT),
    "Qwarks Hideout: T-Bolt: Glide from the Ramp": LocData(50190001, RAC3REGION.QWARKS_HIDEOUT),
    "Qwarks Hideout: Skill Point: Break the Dan": LocData(50190002, RAC3REGION.QWARKS_HIDEOUT),
    "Qwarks Hideout: Trophy: Outside Qwarks Room": LocData(50190003, RAC3REGION.QWARKS_HIDEOUT),  # Qwark Trophy
    # Phoenix Assault Trigger

    # ----- Planet Koros -----#
    "Koros: T-Bolt: Behind the Metal Fence": LocData(50140000, RAC3REGION.KOROS),
    "Koros: T-Bolt: Pair of Towers": LocData(50140001, RAC3REGION.KOROS),
    "Koros: Infobot: Command Center": LocData(50140002, RAC3REGION.KOROS),
    "Koros: Skill Point: You break it, you win it": LocData(50140003, RAC3REGION.KOROS),
    "Koros: Trophy: Glass House": LocData(50140004, RAC3REGION.KOROS),  # Courtney Gears Trophy

    # ----- Planet Command Center -----#
    "Command Center: T-Bolt: Behind the Forcefield": LocData(50220000, RAC3REGION.COMMAND_CENTER),
    "Command Center: Skill Point: Spread Your Germs": LocData(50220001, RAC3REGION.COMMAND_CENTER),
    "Command Center: Trophy: Up a Ladder": LocData(50220002, RAC3REGION.COMMAND_CENTER),  # Lawrence Trophy
    "Command Center: Dr. Nefarious Defeated!": LocData(50200000, RAC3REGION.COMMAND_CENTER),
    "Command Center: Biobliterator Defeated!": LocData(50200001, RAC3REGION.COMMAND_CENTER)
}

weapon_upgrades = {

    "Shock Blaster: V2": LocData(50150000, "Shock Blaster Upgrades"),
    "Shock Blaster: V3": LocData(50150001, "Shock Blaster Upgrades"),
    "Shock Blaster: V4": LocData(50150002, "Shock Blaster Upgrades"),
    "Shock Blaster: V5": LocData(50150003, "Shock Blaster Upgrades"),

    "Nitro Launcher: V2": LocData(50150004, "Nitro Launcher Upgrades"),
    "Nitro Launcher: V3": LocData(50150005, "Nitro Launcher Upgrades"),
    "Nitro Launcher: V4": LocData(50150006, "Nitro Launcher Upgrades"),
    "Nitro Launcher: V5": LocData(50150007, "Nitro Launcher Upgrades"),

    "N60 Storm: V2": LocData(50150008, "N60 Storm Upgrades"),
    "N60 Storm: V3": LocData(50150009, "N60 Storm Upgrades"),
    "N60 Storm: V4": LocData(50150010, "N60 Storm Upgrades"),
    "N60 Storm: V5": LocData(50150011, "N60 Storm Upgrades"),

    "Plasma Whip: V2": LocData(50150012, "Plasma Whip Upgrades"),
    "Plasma Whip: V3": LocData(50150013, "Plasma Whip Upgrades"),
    "Plasma Whip: V4": LocData(50150014, "Plasma Whip Upgrades"),
    "Plasma Whip: V5": LocData(50150015, "Plasma Whip Upgrades"),

    "Infector: V2": LocData(50150016, "Infector Upgrades"),
    "Infector: V3": LocData(50150017, "Infector Upgrades"),
    "Infector: V4": LocData(50150018, "Infector Upgrades"),
    "Infector: V5": LocData(50150019, "Infector Upgrades"),

    "Suck Cannon: V2": LocData(50150020, "Suck Cannon Upgrades"),
    "Suck Cannon: V3": LocData(50150021, "Suck Cannon Upgrades"),
    "Suck Cannon: V4": LocData(50150022, "Suck Cannon Upgrades"),
    "Suck Cannon: V5": LocData(50150023, "Suck Cannon Upgrades"),

    "Spitting Hydra: V2": LocData(50150024, "Spitting Hydra Upgrades"),
    "Spitting Hydra: V3": LocData(50150025, "Spitting Hydra Upgrades"),
    "Spitting Hydra: V4": LocData(50150026, "Spitting Hydra Upgrades"),
    "Spitting Hydra: V5": LocData(50150027, "Spitting Hydra Upgrades"),

    "Agents of Doom: V2": LocData(50150028, "Agents of Doom Upgrades"),
    "Agents of Doom: V3": LocData(50150029, "Agents of Doom Upgrades"),
    "Agents of Doom: V4": LocData(50150030, "Agents of Doom Upgrades"),
    "Agents of Doom: V5": LocData(50150031, "Agents of Doom Upgrades"),

    "Flux Rifle: V2": LocData(50150032, "Flux Rifle Upgrades"),
    "Flux Rifle: V3": LocData(50150033, "Flux Rifle Upgrades"),
    "Flux Rifle: V4": LocData(50150034, "Flux Rifle Upgrades"),
    "Flux Rifle: V5": LocData(50150035, "Flux Rifle Upgrades"),

    "Annihilator: V2": LocData(50150036, "Annihilator Upgrades"),
    "Annihilator: V3": LocData(50150037, "Annihilator Upgrades"),
    "Annihilator: V4": LocData(50150038, "Annihilator Upgrades"),
    "Annihilator: V5": LocData(50150039, "Annihilator Upgrades"),

    "Holo-Shield Glove: V2": LocData(50150040, "Holo-Shield Glove Upgrades"),
    "Holo-Shield Glove: V3": LocData(50150041, "Holo-Shield Glove Upgrades"),
    "Holo-Shield Glove: V4": LocData(50150042, "Holo-Shield Glove Upgrades"),
    "Holo-Shield Glove: V5": LocData(50150043, "Holo-Shield Glove Upgrades"),

    "Disc-Blade Gun: V2": LocData(50150044, "Disc-Blade Gun Upgrades"),
    "Disc-Blade Gun: V3": LocData(50150045, "Disc-Blade Gun Upgrades"),
    "Disc-Blade Gun: V4": LocData(50150046, "Disc-Blade Gun Upgrades"),
    "Disc-Blade Gun: V5": LocData(50150047, "Disc-Blade Gun Upgrades"),

    "Rift Inducer: V2": LocData(50150048, "Rift Inducer Upgrades"),
    "Rift Inducer: V3": LocData(50150049, "Rift Inducer Upgrades"),
    "Rift Inducer: V4": LocData(50150050, "Rift Inducer Upgrades"),
    "Rift Inducer: V5": LocData(50150051, "Rift Inducer Upgrades"),

    "Qwack-O-Ray: V2": LocData(50150052, "Qwack-O-Ray Upgrades"),
    "Qwack-O-Ray: V3": LocData(50150053, "Qwack-O-Ray Upgrades"),
    "Qwack-O-Ray: V4": LocData(50150054, "Qwack-O-Ray Upgrades"),
    "Qwack-O-Ray: V5": LocData(50150055, "Qwack-O-Ray Upgrades"),

    "RY3N0: V2": LocData(50150056, "RY3N0 Upgrades"),
    "RY3N0: V3": LocData(50150057, "RY3N0 Upgrades"),
    "RY3N0: V4": LocData(50150058, "RY3N0 Upgrades"),
    "RY3N0: V5": LocData(50150059, "RY3N0 Upgrades"),

    "Mini-Turret Glove: V2": LocData(50150060, "Mini-Turret Glove Upgrades"),
    "Mini-Turret Glove: V3": LocData(50150061, "Mini-Turret Glove Upgrades"),
    "Mini-Turret Glove: V4": LocData(50150062, "Mini-Turret Glove Upgrades"),
    "Mini-Turret Glove: V5": LocData(50150063, "Mini-Turret Glove Upgrades"),

    "Lava Gun: V2": LocData(50150064, "Lava Gun Upgrades"),
    "Lava Gun: V3": LocData(50150065, "Lava Gun Upgrades"),
    "Lava Gun: V4": LocData(50150066, "Lava Gun Upgrades"),
    "Lava Gun: V5": LocData(50150067, "Lava Gun Upgrades"),

    "Shield Charger: V2": LocData(50150068, "Shield Charger Upgrades"),
    "Shield Charger: V3": LocData(50150069, "Shield Charger Upgrades"),
    "Shield Charger: V4": LocData(50150070, "Shield Charger Upgrades"),
    "Shield Charger: V5": LocData(50150071, "Shield Charger Upgrades"),

    "Bouncer: V2": LocData(50150072, "Bouncer Upgrades"),
    "Bouncer: V3": LocData(50150073, "Bouncer Upgrades"),
    "Bouncer: V4": LocData(50150074, "Bouncer Upgrades"),
    "Bouncer: V5": LocData(50150075, "Bouncer Upgrades"),

    "Plasma Coil: V2": LocData(50150076, "Plasma Coil Upgrades"),
    "Plasma Coil: V3": LocData(50150077, "Plasma Coil Upgrades"),
    "Plasma Coil: V4": LocData(50150078, "Plasma Coil Upgrades"),
    "Plasma Coil: V5": LocData(50150079, "Plasma Coil Upgrades"),

}

nanotech_milestones = {
    "Nanotech Milestone: 11": LocData(50250011, "Nanotech Levels"),
    "Nanotech Milestone: 12": LocData(50250012, "Nanotech Levels"),
    "Nanotech Milestone: 13": LocData(50250013, "Nanotech Levels"),
    "Nanotech Milestone: 14": LocData(50250014, "Nanotech Levels"),
    "Nanotech Milestone: 15": LocData(50250015, "Nanotech Levels"),
    "Nanotech Milestone: 16": LocData(50250016, "Nanotech Levels"),
    "Nanotech Milestone: 17": LocData(50250017, "Nanotech Levels"),
    "Nanotech Milestone: 18": LocData(50250018, "Nanotech Levels"),
    "Nanotech Milestone: 19": LocData(50250019, "Nanotech Levels"),
    "Nanotech Milestone: 20": LocData(50250020, "Nanotech Levels"),
    "Nanotech Milestone: 21": LocData(50250021, "Nanotech Levels"),
    "Nanotech Milestone: 22": LocData(50250022, "Nanotech Levels"),
    "Nanotech Milestone: 23": LocData(50250023, "Nanotech Levels"),
    "Nanotech Milestone: 24": LocData(50250024, "Nanotech Levels"),
    "Nanotech Milestone: 25": LocData(50250025, "Nanotech Levels"),
    "Nanotech Milestone: 26": LocData(50250026, "Nanotech Levels"),
    "Nanotech Milestone: 27": LocData(50250027, "Nanotech Levels"),
    "Nanotech Milestone: 28": LocData(50250028, "Nanotech Levels"),
    "Nanotech Milestone: 29": LocData(50250029, "Nanotech Levels"),
    "Nanotech Milestone: 30": LocData(50250030, "Nanotech Levels"),
    "Nanotech Milestone: 31": LocData(50250031, "Nanotech Levels"),
    "Nanotech Milestone: 32": LocData(50250032, "Nanotech Levels"),
    "Nanotech Milestone: 33": LocData(50250033, "Nanotech Levels"),
    "Nanotech Milestone: 34": LocData(50250034, "Nanotech Levels"),
    "Nanotech Milestone: 35": LocData(50250035, "Nanotech Levels"),
    "Nanotech Milestone: 36": LocData(50250036, "Nanotech Levels"),
    "Nanotech Milestone: 37": LocData(50250037, "Nanotech Levels"),
    "Nanotech Milestone: 38": LocData(50250038, "Nanotech Levels"),
    "Nanotech Milestone: 39": LocData(50250039, "Nanotech Levels"),
    "Nanotech Milestone: 40": LocData(50250040, "Nanotech Levels"),
    "Nanotech Milestone: 41": LocData(50250041, "Nanotech Levels"),
    "Nanotech Milestone: 42": LocData(50250042, "Nanotech Levels"),
    "Nanotech Milestone: 43": LocData(50250043, "Nanotech Levels"),
    "Nanotech Milestone: 44": LocData(50250044, "Nanotech Levels"),
    "Nanotech Milestone: 45": LocData(50250045, "Nanotech Levels"),
    "Nanotech Milestone: 46": LocData(50250046, "Nanotech Levels"),
    "Nanotech Milestone: 47": LocData(50250047, "Nanotech Levels"),
    "Nanotech Milestone: 48": LocData(50250048, "Nanotech Levels"),
    "Nanotech Milestone: 49": LocData(50250049, "Nanotech Levels"),
    "Nanotech Milestone: 50": LocData(50250050, "Nanotech Levels"),
    "Nanotech Milestone: 51": LocData(50250051, "Nanotech Levels"),
    "Nanotech Milestone: 52": LocData(50250052, "Nanotech Levels"),
    "Nanotech Milestone: 53": LocData(50250053, "Nanotech Levels"),
    "Nanotech Milestone: 54": LocData(50250054, "Nanotech Levels"),
    "Nanotech Milestone: 55": LocData(50250055, "Nanotech Levels"),
    "Nanotech Milestone: 56": LocData(50250056, "Nanotech Levels"),
    "Nanotech Milestone: 57": LocData(50250057, "Nanotech Levels"),
    "Nanotech Milestone: 58": LocData(50250058, "Nanotech Levels"),
    "Nanotech Milestone: 59": LocData(50250059, "Nanotech Levels"),
    "Nanotech Milestone: 60": LocData(50250060, "Nanotech Levels"),
    "Nanotech Milestone: 61": LocData(50250061, "Nanotech Levels"),
    "Nanotech Milestone: 62": LocData(50250062, "Nanotech Levels"),
    "Nanotech Milestone: 63": LocData(50250063, "Nanotech Levels"),
    "Nanotech Milestone: 64": LocData(50250064, "Nanotech Levels"),
    "Nanotech Milestone: 65": LocData(50250065, "Nanotech Levels"),
    "Nanotech Milestone: 66": LocData(50250066, "Nanotech Levels"),
    "Nanotech Milestone: 67": LocData(50250067, "Nanotech Levels"),
    "Nanotech Milestone: 68": LocData(50250068, "Nanotech Levels"),
    "Nanotech Milestone: 69": LocData(50250069, "Nanotech Levels"),
    "Nanotech Milestone: 70": LocData(50250070, "Nanotech Levels"),
    "Nanotech Milestone: 71": LocData(50250071, "Nanotech Levels"),
    "Nanotech Milestone: 72": LocData(50250072, "Nanotech Levels"),
    "Nanotech Milestone: 73": LocData(50250073, "Nanotech Levels"),
    "Nanotech Milestone: 74": LocData(50250074, "Nanotech Levels"),
    "Nanotech Milestone: 75": LocData(50250075, "Nanotech Levels"),
    "Nanotech Milestone: 76": LocData(50250076, "Nanotech Levels"),
    "Nanotech Milestone: 77": LocData(50250077, "Nanotech Levels"),
    "Nanotech Milestone: 78": LocData(50250078, "Nanotech Levels"),
    "Nanotech Milestone: 79": LocData(50250079, "Nanotech Levels"),
    "Nanotech Milestone: 80": LocData(50250080, "Nanotech Levels"),
    "Nanotech Milestone: 81": LocData(50250081, "Nanotech Levels"),
    "Nanotech Milestone: 82": LocData(50250082, "Nanotech Levels"),
    "Nanotech Milestone: 83": LocData(50250083, "Nanotech Levels"),
    "Nanotech Milestone: 84": LocData(50250084, "Nanotech Levels"),
    "Nanotech Milestone: 85": LocData(50250085, "Nanotech Levels"),
    "Nanotech Milestone: 86": LocData(50250086, "Nanotech Levels"),
    "Nanotech Milestone: 87": LocData(50250087, "Nanotech Levels"),
    "Nanotech Milestone: 88": LocData(50250088, "Nanotech Levels"),
    "Nanotech Milestone: 89": LocData(50250089, "Nanotech Levels"),
    "Nanotech Milestone: 90": LocData(50250090, "Nanotech Levels"),
    "Nanotech Milestone: 91": LocData(50250091, "Nanotech Levels"),
    "Nanotech Milestone: 92": LocData(50250092, "Nanotech Levels"),
    "Nanotech Milestone: 93": LocData(50250093, "Nanotech Levels"),
    "Nanotech Milestone: 94": LocData(50250094, "Nanotech Levels"),
    "Nanotech Milestone: 95": LocData(50250095, "Nanotech Levels"),
    "Nanotech Milestone: 96": LocData(50250096, "Nanotech Levels"),
    "Nanotech Milestone: 97": LocData(50250097, "Nanotech Levels"),
    "Nanotech Milestone: 98": LocData(50250098, "Nanotech Levels"),
    "Nanotech Milestone: 99": LocData(50250099, "Nanotech Levels"),
    "Nanotech Milestone: 100": LocData(50250100, "Nanotech Levels")
}

rac3_events = {  # Events have no ap_code
    "Cleared Veldin": EventData(None, RAC3REGION.VELDIN),
    "Cleared Florana": EventData(None, RAC3REGION.FLORANA),
    "Cleared Marcadia": EventData(None, RAC3REGION.MARCADIA),
    "Cleared Annihilation Nation 1": EventData(None, RAC3REGION.ANNIHILATION_NATION),
    "Cleared Annihilation Nation 2": EventData(None, RAC3REGION.ANNIHILATION_NATION_2),
    "Cleared Aquatos": EventData(None, RAC3REGION.AQUATOS),
    "Cleared Tyhrranosis": EventData(None, RAC3REGION.TYHRRANOSIS),
    "Cleared Daxx": EventData(None, RAC3REGION.DAXX),
}

location_table: dict[str, LocData] = {
    **rac3_locations,
    **nanotech_milestones
    # **weapon_upgrades
}

weapons: list[str] = [
    "Florana: Received Plasma Whip",
    "Florana: Received N60 Storm",
    "Phoenix: Received Suck Cannon",
    "Phoenix: Received Infector",
    "Marcadia: Received Spitting Hydra",
    "Annihilation: Received Agents of Doom",
    "Aquatos: Received Flux Rifle",
    "Aquatos: Received Mini-Turret Glove",
    "Aquatos: Received Lava Gun",
    "Aquatos: Received Shield Charger",
    "Aquatos: Received Bouncer",
    "Aquatos: Received Plasma Coil",
    "Tyhrranosis: Received Annihilator",
    "Tyhrranosis: Received Holo-Shield Glove",
    "Obani Gemini: Received Disc-Blade Gun",
    "Holostar: Received Rift Inducer",
    "Aridia: Received Qwack-O-Ray",
]

gadgets: list[str] = [
    "Marcadia: Received Refractor",
    "Annihilation: Received Tyhrra-Guise",
    "Daxx: Received Charge Boots",
    "Blackwater City: Received Gravity Boots",
    "Zeldrin Starport: Received Bolt Grabber V2",
    "Aridia: Received Warp Pad",
    "Crash Site: Received Nano-Pak",
    "Qwarks Hideout: Received Gadgetron PDA",
]

rangers: list[str] = [
    "Marcadia: Operation IRON SHIELD: Secure the Area",
    "Marcadia: Operation IRON SHIELD: Air Assault",
    "Marcadia: Operation IRON SHIELD: Turret Command",
    "Marcadia: Operation IRON SHIELD: Under the Gun",
    "Marcadia: Operation IRON SHIELD: Hit n' Run",
    "Marcadia: Received Refractor",
    "Marcadia: Meet Al",
    "Marcadia: Skill Point: Reflect on how to score",
    "Marcadia: T-Bolt: Last Refractor Room",
    "Marcadia: T-Bolt: Ceiling just before Al",
    "Tyhrranosis: Operation ISLAND STRIKE: Assault on Kavu Island",
    "Tyhrranosis: Operation ISLAND STRIKE: Dogfight over Kavu Island",
    "Tyhrranosis: Operation ISLAND STRIKE: Operation Thunderbolt",
    "Tyhrranosis: Operation ISLAND STRIKE: The Final Battle",
    "Blackwater City: Received Gravity Boots",
    "Blackwater City: Infobot: Holostar Studios",
    "Blackwater City: Operation BLACK TIDE: The Battle of Blackwater City",
    "Blackwater City: Operation BLACK TIDE: The Bridge",
    "Blackwater City: Operation BLACK TIDE: Counterattack",
    "Blackwater City: Skill Point: Bash the party",
    "Metropolis: T-Bolt: Tall Tower (Hovership)",
    "Metropolis: Operation URBAN STORM: Countdown",
    "Metropolis: Operation URBAN STORM: Urban Combat",
    "Metropolis: Operation URBAN STORM: Tower Attack",
    "Metropolis: Operation URBAN STORM: Air Superiority",
    "Metropolis: Operation URBAN STORM: Turret Command",
    "Metropolis: Received Map-O-Matic",
    "Aridia: Received Warp Pad",
    "Aridia: T-Bolt: Under the Bridge (Assassination)",
    "Aridia: T-Bolt: Behind the Base (X12 Endgame)",
    "Aridia: Operation DEATH VALLEY: The Tunnels of Outpost X12",
    "Aridia: Operation DEATH VALLEY: Ambush in Red Rock Valley",
    "Aridia: Operation DEATH VALLEY: Assassination",
    "Aridia: Operation DEATH VALLEY: Reclaim the Valley",
    "Aridia: Operation DEATH VALLEY: X12 Endgame",
    "Aridia: Skill Point: Go for hang time",
    "Aridia: Skill Point: Zap back at ya'",
    "Phoenix: Long Term Trophy: Friend of the Rangers"
]

unstable: list[str] = [
    "Phoenix: Received Magna Plate Armor",
    "Phoenix: Received Adamantine Armor",
    "Phoenix: Received Aegis Mark V Armor",
    "Phoenix: Received Infernox Armor",
    "Phoenix: Meet Sasha on the Bridge",
    "Phoenix: Return after winning Grand Prize Bout",
    "Phoenix: Deliver the Star Map to Qwark",
    "Phoenix: VR Training after Noid Queen",
    "Phoenix: T-Bolt: VR Gadget Training",
    "Phoenix: Received Hacker",
    "Phoenix: Received Hypershot",
    "Phoenix: VR: VR Gadget Training",
    "Obani Gemini: Infobot: Blackwater City",
    "Crash Site: Infobot: Aridia"
]

infobots: list[str] = []  # Todo: planet coords

location_groups: dict[str, set[str]] = {
    RAC3REGION.VELDIN: set(loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.VELDIN),
    RAC3REGION.FLORANA: set(loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.FLORANA),
    RAC3REGION.STARSHIP_PHOENIX: set(
        loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.STARSHIP_PHOENIX),
    RAC3REGION.MARCADIA: set(loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.MARCADIA),
    RAC3REGION.ANNIHILATION_NATION: set(loc for loc in location_table.keys() if
                                        location_table[loc].region == RAC3REGION.ANNIHILATION_NATION
                                        or location_table[loc].region == RAC3REGION.ANNIHILATION_NATION_2),
    RAC3REGION.AQUATOS: set(loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.AQUATOS),
    RAC3REGION.TYHRRANOSIS: set(loc for loc in location_table.keys() if
                                location_table[loc].region == RAC3REGION.TYHRRANOSIS
                                or location_table[loc].region == RAC3REGION.TYHRRANOSIS_MISSION),
    RAC3REGION.DAXX: set(loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.DAXX),
    RAC3REGION.OBANI_GEMINI: set(
        loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.OBANI_GEMINI),
    RAC3REGION.BLACKWATER_CITY: set(
        loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.BLACKWATER_CITY),
    RAC3REGION.HOLOSTAR_STUDIOS: set(
        loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.HOLOSTAR_STUDIOS),
    RAC3REGION.OBANI_DRACO: set(
        loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.OBANI_DRACO),
    RAC3REGION.ZELDRIN_STARPORT: set(
        loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.ZELDRIN_STARPORT),
    RAC3REGION.METROPOLIS: set(loc for loc in location_table.keys() if
                               location_table[loc].region == RAC3REGION.METROPOLIS
                               or location_table[loc].region == RAC3REGION.METROPOLIS_MISSION),
    RAC3REGION.CRASH_SITE: set(
        loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.CRASH_SITE),
    RAC3REGION.ARIDIA: set(loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.ARIDIA),
    RAC3REGION.QWARKS_HIDEOUT: set(
        loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.QWARKS_HIDEOUT),
    RAC3REGION.KOROS: set(loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.KOROS),
    RAC3REGION.COMMAND_CENTER: set(
        loc for loc in location_table.keys() if location_table[loc].region == RAC3REGION.COMMAND_CENTER),
    RAC3TAG.SKILLPOINT: set(loc for loc in location_table.keys() if "Skill" in loc),
    RAC3TAG.T_BOLT: set(loc for loc in location_table.keys() if "T-Bolt" in loc),
    RAC3TAG.SEWER: set(loc for loc in location_table.keys() if
                       ("Sewer" in loc) or (loc == "Aquatos: Skill Point: Hit the motherload")),
    RAC3TAG.VIDCOMIC: set(loc for loc in location_table.keys() if "VidComic" in loc),
    RAC3TAG.TROPHY: set(loc for loc in location_table.keys() if "Trophy" in loc),  # All trophies including long term
    RAC3TAG.LONG_TROPHY: set(loc for loc in location_table.keys() if "Long Term" in loc),  # Long Term trophies only
    RAC3TAG.RANGERS: set(loc for loc in rangers),
    RAC3TAG.ARENA: set(loc for loc in location_table.keys() if
                       (50070002 <= location_table[loc].ap_code < 50080000) or ("VR" in loc) or ("Grand" in loc)),
    RAC3TAG.NANOTECH: set(loc for loc in location_table.keys() if "Nanotech" in loc),
    RAC3TAG.UNSTABLE: set(loc for loc in unstable),
    RAC3TAG.WEAPONS: set(loc for loc in weapons),
    RAC3TAG.GADGETS: set(loc for loc in gadgets),
    RAC3TAG.INFOBOT: set(loc for loc in infobots)
}


# class EventData(NamedTuple):
#    name:       str
#    ap_code:    Optional[int] = None
# class LocData(NamedTuple):
#    ap_code: Optional[int]
#    region: Optional[str]
def get_level_locations(region):
    return map(lambda l: l[0], get_level_location_data(region))


def get_level_location_data(region):
    return filter(lambda l: l[1].region == region, location_table.items())
