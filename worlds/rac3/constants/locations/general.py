# Todo: Missions
# "Missions": {
#     "First Ranger gives weapon": 0x001426E0,
#     "Second Ranger gives weapon": 0x001426E1,
#     "Zeldrin starport: Find Nefarious": 0x001426E2,
#     "Save Veldin": 0x001426E3,
#     "Veldin: Eliminate the Enemy Forces": 0x001426E4,
#     "Florana: Find the mysterious man": 0x001426E5,
#     "Florana: Walk the path of death!": 0x001426E6,
#     "Defeat Qwark": 0x001426E7,
#     "Take Qwark to Cage": 0x001426E8,
#     "Meet Sasha bridge": 0x001426E9,
#     "Meet Al on Marcadia": 0x001426EA,
#     "Play VidComic1": 0x001426EB,
#     "Marcadia: Get to the Palace": 0x001426EF,
#     "Marcadia: Repair the LDS": 0x001426F1,
#     "Marcadia: Secure the Area": 0x001426F2,
#     "Annihilation Nation: Return": 0x001426F3,
#     "Phoenix Rescue": 0x001426F4,
#     "Annihilation Nation: Grand Prize Bout": 0x001426F5,
#     "Return to Phoenix after Annihilation Nation 2": 0x001426F6,
#     "Aquatos: Infiltrate the Base": 0x001426F7,
#     "Tyhrranosis: Destroy the Plasma Cannon Turrets": 0x001426F9,
#     "Obani Gemini: ???": 0x00142701,
#     "Save Blackwater City": 0x00142704,
#     "Blackwater: Destroy the Base": 0x00142705,
#     "Metropolis: Defeat Klunk": 0x00142708,
#     "Obani Draco: Defeat Courtney Gears": 0x0014270D,
#     "Defeat Dr Nefarious": 0x0014270F,
#     "Destroy the Biobliterator": 0x00142710,  # Doesn't get written to
#     "Holostar: Film Episode": 0x00142712,
#     "Holostar: Return to your ship": 0x00142713,
#     "Metropolis: Complete Ranger Missions": 0x00142714,
#     "Aquatos: Gather Sewer Crystals": 0x00142715,
#     "Tyhrranosis: Destroy the Encampment": 0x00142717,
#     "Tyhrranosis: Destroy the Momma Tyhrranoid": 0x0014271D,
#
# "Enemies":
#     "First of two noids - Mylon Landing Point": 0x001C169E,
#     "Second of two noids - Mylon Landing Point": 0x001C16F4

class RAC3LOCATION:
    VELDIN_FIRST_RANGER = "Veldin: First Ranger"
    VELDIN_SECOND_RANGER = "Veldin: Second Ranger"
    VELDIN_SAVE_VELDIN = "Veldin: Save Veldin"
    FLORANA_DEFEAT_QWARK = "Florana: Defeat Qwark"
    PHOENIX_MEET_SASHA = "Phoenix: Meet Sasha on the Bridge"
    PHOENIX_ASSAULT = "Phoenix: Post Hideout Assault"
    PHOENIX_GRAND_PRIZE = "Phoenix: Return after winning Grand Prize Bout"
    PHOENIX_STAR_MAP = "Phoenix: Deliver the Star Map to Qwark"
    PHOENIX_HACKER = "Phoenix: Received The Hacker"
    PHOENIX_HYPERSHOT = "Phoenix: Received Hypershot"
    PHOENIX_VR_TRAINING = "Phoenix: VR: VR Gadget Training"
    PHOENIX_VR_WARM_UP = "Phoenix: VR: Warm Up"
    PHOENIX_VR_D_L_D = "Phoenix: VR: Don't Look Down"
    PHOENIX_VR_SPEED_ROUND = "Phoenix: VR: Speed Round"
    PHOENIX_VR_HOT_STEPPER = "Phoenix: VR: Hot Stepper"
    PHOENIX_VR_90_SECOND = "Phoenix: VR: 90 Second Slayer"
    PHOENIX_VR_SHOCKER = "Phoenix: VR: The Shocker"
    PHOENIX_VR_WRENCH = "Phoenix: VR: Wrench Beatdown"
    PHOENIX_VR_NERVES = "Phoenix: VR: Nerves of Titanium"
    PHOENIX_MASTER_PLAN = "Phoenix: Give Al the Master Plan"
    PHOENIX_VID_COMIC_1_CLEAR = "Phoenix: Qwark VidComic 1 Clear"
    PHOENIX_VID_COMIC_2_CLEAR = "Phoenix: Qwark VidComic 2 Clear"
    PHOENIX_VID_COMIC_3_CLEAR = "Phoenix: Qwark VidComic 3 Clear"
    PHOENIX_VID_COMIC_4_CLEAR = "Phoenix: Qwark VidComic 4 Clear"
    PHOENIX_VID_COMIC_5_CLEAR = "Phoenix: Qwark VidComic 5 Clear"
    MARCADIA_RANGERS_1 = "Marcadia: Operation IRON SHIELD 1: Secure the Area"
    MARCADIA_RANGERS_2 = "Marcadia: Operation IRON SHIELD 2: Air Assault"
    MARCADIA_RANGERS_3 = "Marcadia: Operation IRON SHIELD 3: Turret Command"
    MARCADIA_RANGERS_4 = "Marcadia: Operation IRON SHIELD 4: Under the Gun"
    MARCADIA_RANGERS_5 = "Marcadia: Operation IRON SHIELD 5: Hit n' Run"
    MARCADIA_REFRACTOR = "Marcadia: Received Refractor"
    MARCADIA_MEET_AL = "Marcadia: Meet Al"
    NATION_TYHRRA_GUISE = "Annihilation Nation: Received Tyhrra-Guise"
    NATION_GRAND_PRIZE_BOUT = "Annihilation Nation: Grand Prize Bout"
    NATION_THE_TERRIBLE_TWO = "Annihilation Nation: The Terrible Two"
    NATION_ROBOT_RAMPAGE = "Annihilation Nation: Robot Rampage"
    NATION_TWO_MINUTE_WARNING = "Annihilation Nation: Two Minute Warning"
    NATION_90_SECONDS = "Annihilation Nation: 90 Seconds of Carnage"
    NATION_ONSLAUGHT = "Annihilation Nation: Onslaught"
    NATION_WHIP_IT_GOOD = "Annihilation Nation: Whip it Good"
    NATION_HYDRA_N_SEEK = "Annihilation Nation: Hydra'n Seek"
    NATION_CHAMPIONSHIP_BOUT = "Annihilation Nation: Championship Bout"
    NATION_MEET_COURTNEY = "Annihilation Nation 2: Meet Courtney"
    NATION_INFOBOT_HOLOSTAR = "Annihilation Nation 2: Infobot: Holostar Studios"
    NATION_NINJA_CHALLENGE = "Annihilation Nation 2: Ninja Challenge"
    NATION_COUNTING_DUCKS = "Annihilation Nation 2: Counting Ducks"
    NATION_CYCLING_WEAPONS = "Annihilation Nation 2: Cycling Weapons"
    NATION_ONE_HIT_WONDER = "Annihilation Nation 2: One Hit Wonder"
    NATION_TIME_TO_SUCK = "Annihilation Nation 2: Time to Suck"
    NATION_NAPTIME = "Annihilation Nation 2: Naptime"
    NATION_MORE_CYCLING_WEAPONS = "Annihilation Nation 2: More Cycling Weapons"
    NATION_DODGE_THE_TWINS = "Annihilation Nation 2: Dodge the Twins"
    NATION_CHOP_CHOP = "Annihilation Nation 2: Chop Chop"
    NATION_SLEEP_INDUCER = "Annihilation Nation 2: Sleep Inducer"
    NATION_THE_OTHER_WHITE_MEAT = "Annihilation Nation 2: The Other White Meat"
    NATION_CHAMPIONSHIP_BOUT_II = "Annihilation Nation 2: Championship Bout II"
    NATION_QWARKTASTIC_BATTLE = "Annihilation Nation 2: Qwarktastic Battle"
    NATION_HEAT_STREET = "Annihilation Nation: Heat Street"
    NATION_CRISPY_CRITTER = "Annihilation Nation: Crispy Critter"
    NATION_PYRO_PLAYGROUND = "Annihilation Nation: Pyro Playground"
    NATION_SUICIDE_RUN = "Annihilation Nation: Suicide Run"
    NATION_BBQ_BOULEVARD = "Annihilation Nation 2: BBQ Boulevard"
    NATION_MAZE_OF_BLAZE = "Annihilation Nation 2: Maze of Blaze"
    NATION_CREMATION_STATION = "Annihilation Nation 2: Cremation Station"
    NATION_THE_ANNIHILATOR = "Annihilation Nation 2: The Annihilator (Gauntlet)"
    TYHRRANOSIS_INTRO = "Tyhrranosis: Rendezvous on Tyhrranosis"
    TYHRRANOSIS_BOSS = "Tyhrranosis: Destroy the Momma Tyhrranoid"
    TYHRRANOSIS_RANGERS_1 = "Tyhrranosis: Operation ISLAND STRIKE 1: Assault on Kavu Island"
    TYHRRANOSIS_RANGERS_2 = "Tyhrranosis: Operation ISLAND STRIKE 2: Dogfight over Kavu Island"
    TYHRRANOSIS_RANGERS_3 = "Tyhrranosis: Operation ISLAND STRIKE 3: Operation Thunderbolt"
    TYHRRANOSIS_RANGERS_4 = "Tyhrranosis: Operation ISLAND STRIKE 4: The Final Battle"
    DAXX_CHARGE_BOOTS = "Daxx: Received Charge Boots"
    DAXX_FACILITY = "Daxx: Infiltrate Weapons Facility"
    DAXX_GUNSHIP = "Daxx: Gunship"
    OBANI_GEMINI_SKIDD = "Obani Gemini: Infobot: Blackwater City"
    BLACKWATER_CITY_RANGERS_1 = "Blackwater City: Operation BLACK TIDE 1: The Battle of Blackwater City"
    BLACKWATER_CITY_RANGERS_2 = "Blackwater City: Operation BLACK TIDE 2: The Bridge"
    BLACKWATER_CITY_RANGERS_3 = "Blackwater City: Operation BLACK TIDE 3: Counterattack"
    BLACKWATER_CITY_COMPLETE = "Blackwater City: Received Gravity Boots"
    SKIDD_CAPTURED = "Galaxy Burger: Skidd is captured"
    DRACO_COURTNEY = "Obani Draco: Defeat Courtney Gears"
    ZELDRIN_STARPORT_ITEM = "Zeldrin Starport: Received Bolt Grabber V2"
    ZELDRIN_STARPORT_SHIP = "Zeldrin Starport: Escape the Exploding Ship"
    METROPOLIS_METAL_NOIDS = "Metropolis: Metal-Noids"
    METROPOLIS_DEFEAT_KLUNK = "Metropolis: Defeat Klunk"
    METROPOLIS_RANGERS_1 = "Metropolis: Operation URBAN STORM 1: Countdown"
    METROPOLIS_RANGERS_2 = "Metropolis: Operation URBAN STORM 2: Urban Combat"
    METROPOLIS_RANGERS_3 = "Metropolis: Operation URBAN STORM 3: Tower Attack"
    METROPOLIS_RANGERS_4 = "Metropolis: Operation URBAN STORM 4: Air Superiority"
    METROPOLIS_RANGERS_5 = "Metropolis: Operation URBAN STORM 5: Turret Command"
    METROPOLIS_MAP_O_MATIC = "Metropolis: Received Map-O-Matic"
    CRASH_SITE_NANO_PAK = "Crash Site: Received Nano-pak"
    CRASH_SITE_ESCAPE_POD = "Crash Site: Escape Pod"
    CRASH_SITE_INFOBOT_ARIDIA = "Crash Site: Infobot: Aridia"
    ARIDIA_WARP_PAD = "Aridia: Received Warp Pad"
    ARIDIA_RANGERS_1 = "Aridia: Operation DEATH VALLEY 1: The Tunnels of Outpost X12"
    ARIDIA_RANGERS_2 = "Aridia: Operation DEATH VALLEY 2: Ambush in Red Rock Valley"
    ARIDIA_RANGERS_3 = "Aridia: Operation DEATH VALLEY 3: Assassination"
    ARIDIA_RANGERS_4 = "Aridia: Operation DEATH VALLEY 4: Reclaim the Valley"
    ARIDIA_RANGERS_5 = "Aridia: Operation DEATH VALLEY 5: X12 Endgame"
    HIDEOUT_PDA = "Qwarks Hideout: Received PDA"
    HIDEOUT_QWARK = "Qwarks Hideout: Find Qwark"
    KOROS_BASE = "Koros: Infobot: Command Center"
    COMMAND_CENTER_NEFARIOUS = "Command Center: Dr. Nefarious Defeated!"
    COMMAND_CENTER_BIOBLITERATOR = "Command Center: Biobliterator Defeated!"
