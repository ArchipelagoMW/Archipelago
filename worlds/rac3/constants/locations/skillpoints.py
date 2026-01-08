class RAC3SKILLPOINT:
    ARIDIA_HANG_TIME = "Aridia: Skillpoint: Go for hang time"  # 0x001D54B0,
    FLORANA_PATH = "Florana: Skillpoint: Stay Squeaky Clean"  # 0x001D54B1,
    PHOENIX_ARCADE = "Phoenix: Skillpoint: Strive for arcade perfection"  # 0x001D54B2,
    PHOENIX_VR_TRAINING = "Phoenix: Skillpoint: Beat Helga's best time"  # 0x001D54B3,
    PHOENIX_ARMOR = "Phoenix: Skillpoint: Turn Up The Heat"  # 0x001D54B4,
    PHOENIX_MONKEY = "Phoenix: Skillpoint: Monkeying around"  # 0x001D54B5,
    MARCADIA_REFLECT = "Marcadia: Skillpoint: Reflect on how to score"  # 0x001D54B6,
    DAXX_BUGS = "Daxx: Skillpoint: Bugs to Birdie"  # 0x001D54B7,
    NATION_BASH = "Annihilation Nation: Skillpoint: Bash the bug"  # 0x001D54B8,
    NATION_EIGHT = "Annihilation Nation: Skillpoint: Be an eight time champ"  # 0x001D54B9,
    NATION_FLEE = "Annihilation Nation: Skillpoint: Flee Flawlessly"  # 0x001D54BA,
    NATION_CAMERA = "Annihilation Nation: Skillpoint: Lights, camera action!"  # 0x001D54BB,
    AQUATOS_SUNKEN = "Aquatos: Skillpoint: Search for sunken treasure"  # 0x001D54BC,
    TYHRRANOSIS_SHARPSHOOTER = "Tyhrranosis: Skillpoint: Be a Sharpshooter"  # 0x001D54BD,
    GEMINI_BELT = "Obani Gemini: Skillpoint: Get to the belt"  # 0x001D54BE,
    BLACKWATER_BASH = "Blackwater City: Skillpoint: Bash the party"  # 0x001D54BF,
    HOLOSTAR_LUCKY = "Holostar: Skillpoint: Feeling Lucky"  # 0x001D54C0,
    KOROS_BREAK = "Koros: Skillpoint: You break it, you win it"  # 0x001D54C1,
    METROPOLIS_GOOD_YEAR = "Metropolis: Skillpoint: 2002 was a good year in the city"  # 0x001D54C2,
    CRASH_SITE_SUCK = "Crash Site: Skillpoint: Suck it up!"  # 0x001D54C3,
    CRASH_SITE_AIM_HIGH = "Crash Site: Skillpoint: Aim High"  # 0x001D54C4,
    ARIDIA_ZAP = "Aridia: Skillpoint: Zap back at ya'"  # 0x001D54C5,
    HIDEOUT_DAN = "Hideout: Skillpoint: Break the Dan"  # 0x001D54C6,
    COMMAND_CENTER_GERMS = "Command Center: Skillpoint: Spread your germs"  # 0x001D54C7,
    SEWER_MOTHERLOAD = "Aquatos Sewer: Skillpoint: Hit the motherload"  # 0x001D54C8,
    PHOENIX_COMIC_1 = "Phoenix: Skillpoint: Pirate booty - set a new record for qwark"  # 0x001D54C9,
    PHOENIX_COMIC_4 = "Phoenix: Skillpoint: Deja Q All over Again - set a new record for qwark"  # 0x001D54CA,
    PHOENIX_COMIC_2 = "Phoenix: Skillpoint: Arriba Amoeba! - set a new record for qwark"  # 0x001D54CB,
    PHOENIX_COMIC_3 = "Phoenix: Skillpoint: Shadow of the robot - set a new record for qwark"  # 0x001D54CC,
    PHOENIX_COMIC_5 = "Phoenix: Skillpoint: The Shaming of the Q - set a new record for qwark"  # 0x001D54CD,

    FLORANA_PATH_SHORT = "Flo: Stay Squeaky Clean"
    PHOENIX_ARCADE_SHORT = "Pho: Strive for arcade perfection"
    PHOENIX_VR_TRAINING_SHORT = "Pho: Beat Helgas best time"
    PHOENIX_ARMOR_SHORT = "Pho: Turn Up The Heat"
    PHOENIX_MONKEY_SHORT = "Pho: Monkeying around"
    MARCADIA_REFLECT_SHORT = "Mar: Reflect on how to score"
    NATION_BASH_SHORT = "Ann: Bash the bug"
    NATION_EIGHT_SHORT = "Ann: Be an eight time champ"
    NATION_FLEE_SHORT = "Ann: Flee Flawlessly"
    NATION_CAMERA_SHORT = "Ann: Lights, camera action!"
    AQUATOS_SUNKEN_SHORT = "Aqu: Search for sunken treasure"
    SEWER_MOTHERLOAD_SHORT = "Aqu: Hit the motherload"
    TYHRRANOSIS_SHARPSHOOTER_SHORT = "Tyh: Be a Sharpshooter"
    DAXX_BUGS_SHORT = "Dax: Bugs to Birdie"
    GEMINI_BELT_SHORT = "Gem: Get to the belt"
    BLACKWATER_BASH_SHORT = "Bla: Bash the party"
    HOLOSTAR_LUCKY_SHORT = "Hol: Feeling Lucky"
    METROPOLIS_GOOD_YEAR_SHORT = "Met: 2002 was a good year in the city"
    CRASH_SITE_SUCK_SHORT = "Cra: Suck it up!"
    CRASH_SITE_AIM_HIGH_SHORT = "Cra: Aim High"
    ARIDIA_ZAP_SHORT = "Ari: Zap back at ya"
    ARIDIA_HANG_TIME_SHORT = "Ari: Go for hang time"
    HIDEOUT_DAN_SHORT = "Qwa: Break the Dan"
    KOROS_BREAK_SHORT = "Kor: You break it, you win it"
    COMMAND_CENTER_GERMS_SHORT = "Com: Spread your germs"
    PHOENIX_COMIC_1_SHORT = "Pho: Pirate booty, set a new record for qwark"
    PHOENIX_COMIC_2_SHORT = "Pho: Arriba Amoeba!, set a new record for qwark"
    PHOENIX_COMIC_3_SHORT = "Pho: Shadow of the robot, set a new record for qwark"
    PHOENIX_COMIC_4_SHORT = "Pho: Deja Q All over Again, set a new record for qwark"
    PHOENIX_COMIC_5_SHORT = "Pho: The Shaming of the Q, set a new record for qwark"


SKILLPOINT_LOCATION_TO_NAME: dict[str, str] = {
    RAC3SKILLPOINT.FLORANA_PATH: RAC3SKILLPOINT.FLORANA_PATH_SHORT,
    RAC3SKILLPOINT.PHOENIX_ARCADE: RAC3SKILLPOINT.PHOENIX_ARCADE_SHORT,
    RAC3SKILLPOINT.PHOENIX_VR_TRAINING: RAC3SKILLPOINT.PHOENIX_VR_TRAINING_SHORT,
    RAC3SKILLPOINT.PHOENIX_ARMOR: RAC3SKILLPOINT.PHOENIX_ARMOR_SHORT,
    RAC3SKILLPOINT.PHOENIX_MONKEY: RAC3SKILLPOINT.PHOENIX_MONKEY_SHORT,
    RAC3SKILLPOINT.MARCADIA_REFLECT: RAC3SKILLPOINT.MARCADIA_REFLECT_SHORT,
    RAC3SKILLPOINT.NATION_BASH: RAC3SKILLPOINT.NATION_BASH_SHORT,
    RAC3SKILLPOINT.NATION_EIGHT: RAC3SKILLPOINT.NATION_EIGHT_SHORT,
    RAC3SKILLPOINT.NATION_FLEE: RAC3SKILLPOINT.NATION_FLEE_SHORT,
    RAC3SKILLPOINT.NATION_CAMERA: RAC3SKILLPOINT.NATION_CAMERA_SHORT,
    RAC3SKILLPOINT.AQUATOS_SUNKEN: RAC3SKILLPOINT.AQUATOS_SUNKEN_SHORT,
    RAC3SKILLPOINT.SEWER_MOTHERLOAD: RAC3SKILLPOINT.SEWER_MOTHERLOAD_SHORT,
    RAC3SKILLPOINT.TYHRRANOSIS_SHARPSHOOTER: RAC3SKILLPOINT.TYHRRANOSIS_SHARPSHOOTER_SHORT,
    RAC3SKILLPOINT.DAXX_BUGS: RAC3SKILLPOINT.DAXX_BUGS_SHORT,
    RAC3SKILLPOINT.GEMINI_BELT: RAC3SKILLPOINT.GEMINI_BELT_SHORT,
    RAC3SKILLPOINT.BLACKWATER_BASH: RAC3SKILLPOINT.BLACKWATER_BASH_SHORT,
    RAC3SKILLPOINT.HOLOSTAR_LUCKY: RAC3SKILLPOINT.HOLOSTAR_LUCKY_SHORT,
    RAC3SKILLPOINT.METROPOLIS_GOOD_YEAR: RAC3SKILLPOINT.METROPOLIS_GOOD_YEAR_SHORT,
    RAC3SKILLPOINT.CRASH_SITE_SUCK: RAC3SKILLPOINT.CRASH_SITE_SUCK_SHORT,
    RAC3SKILLPOINT.CRASH_SITE_AIM_HIGH: RAC3SKILLPOINT.CRASH_SITE_AIM_HIGH_SHORT,
    RAC3SKILLPOINT.ARIDIA_ZAP: RAC3SKILLPOINT.ARIDIA_ZAP_SHORT,
    RAC3SKILLPOINT.ARIDIA_HANG_TIME: RAC3SKILLPOINT.ARIDIA_HANG_TIME_SHORT,
    RAC3SKILLPOINT.HIDEOUT_DAN: RAC3SKILLPOINT.HIDEOUT_DAN_SHORT,
    RAC3SKILLPOINT.KOROS_BREAK: RAC3SKILLPOINT.KOROS_BREAK_SHORT,
    RAC3SKILLPOINT.COMMAND_CENTER_GERMS: RAC3SKILLPOINT.COMMAND_CENTER_GERMS_SHORT,
    RAC3SKILLPOINT.PHOENIX_COMIC_1: RAC3SKILLPOINT.PHOENIX_COMIC_1_SHORT,
    RAC3SKILLPOINT.PHOENIX_COMIC_2: RAC3SKILLPOINT.PHOENIX_COMIC_2_SHORT,
    RAC3SKILLPOINT.PHOENIX_COMIC_3: RAC3SKILLPOINT.PHOENIX_COMIC_3_SHORT,
    RAC3SKILLPOINT.PHOENIX_COMIC_4: RAC3SKILLPOINT.PHOENIX_COMIC_4_SHORT,
    RAC3SKILLPOINT.PHOENIX_COMIC_5: RAC3SKILLPOINT.PHOENIX_COMIC_5_SHORT,
}

NAME_TO_SKILLPOINT_LOCATION: dict[str, str] = {
    v: k for k, v in SKILLPOINT_LOCATION_TO_NAME.items()
}
