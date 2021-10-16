from BaseClasses import Location
import typing


class AchieveData(typing.NamedTuple):
    id: typing.Optional[int]
    region: str


class TerrariaAchievement(Location):
    game: str = "Terraria"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address


achievement_table = {
    "Timber!!": AchieveData(1, "Overworld"),
    "No Hobo": AchieveData(2, "Overworld"),
    "Stop! Hammer Time!": AchieveData(3, "Overworld"),
    "Ooo! Shiny!": AchieveData(4, "Overworld"),
    "Heart Breaker": AchieveData(5, "Overworld"),
    "Heavy Metal": AchieveData(6, "Overworld"),
    "I Am Loot!": AchieveData(7, "Overworld"),
    "Star Power": AchieveData(8, "Overworld"),
    "Hold on Tight!": AchieveData(9, "Overworld"),
    "Eye on You": AchieveData(10, "Overworld"),
    "Smashing, Poppet!": AchieveData(11, "Overworld"),
    "Worm Fodder": AchieveData(12, "Corruption"),
    "Mastermind": AchieveData(13, "Crimson"),
    "Where's My Honey?": AchieveData(14, "Jungle"),
    "Sting Operation": AchieveData(15, "Jungle"),
    "Boned": AchieveData(16, "Overworld"),
    "Dungeon Heist": AchieveData(17, "Dungeon"),
    "It's Getting Hot in Here": AchieveData(18, "Underworld"),
    "Miner for Fire": AchieveData(19, "Underworld"),
    "Still Hungry": AchieveData(20, "Underworld"),
    "It's Hard!": AchieveData(21, "Underworld"),
    "Begone, Evil!": AchieveData(22, "Hardmode"),
    "Extra Shiny!": AchieveData(23, "Hardmode"),
    "Head in the Clouds": AchieveData(24, "Hardmode"),
    "Like a Boss": AchieveData(25, "Overworld"),
    "Buckets of Bolts": AchieveData(26, "Hardmode"),
    "Drax Attax": AchieveData(27, "Hardmode"),
    "Photosynthesis": AchieveData(28, "Hardmode Jungle"),
    "Get a Life": AchieveData(29, "Hardmode Jungle"),
    "The Great Southern Plantkill": AchieveData(30, "Hardmode Jungle"),
    "Temple Raider": AchieveData(31, "Post-Plantera"),
    "Lihzahrdian Idol": AchieveData(32, "Post-Plantera"),
    "Robbing the Grave": AchieveData(33, "Post-Plantera"),
    "Big Booty": AchieveData(34, "Post-Plantera"),
    "Fish Out of Water": AchieveData(35, "Overworld"),
    "Obsessive Devotion": AchieveData(36, "Post-Golem"),
    "Star Destroyer": AchieveData(37, "Post-Golem"),
    "Champion of Terraria": AchieveData(38, "Post-Golem"),
    "Bloodbath": AchieveData(39, "Overworld"),
    "Slippery Shinobi": AchieveData(40, "Overworld"),
    "Goblin Punter": AchieveData(41, "Overworld"),
    "Walk the Plank": AchieveData(42, "Hardmode"),
    "Kill the Sun": AchieveData(43, "Hardmode"),
    "Do You Want to Slay a Snowman?": AchieveData(44, "Hardmode"),
    "Tin-Foil Hatter": AchieveData(45, "Post-Golem"),
    "Baleful Harvest": AchieveData(46, "Post-Plantera"),
    "Ice Scream": AchieveData(47, "Post-Plantera"),
    "Sticky Situation": AchieveData(48, "Overworld"),
    "Real Estate Agent": AchieveData(49, "Postgame"),
    "Not the Bees!": AchieveData(50, "Jungle"),
    "Jeepers Creepers": AchieveData(51, "Overworld"),
    "Funkytown": AchieveData(52, "Overworld"),
    "Into Orbit": AchieveData(53, "Overworld"),
    "Rock Bottom": AchieveData(54, "Underworld"),
    "Mecha Mayhem": AchieveData(55, "Hardmode"),
    "Gelatin World Tour": AchieveData(56, "Postgame"),
    "Fashion Statement": AchieveData(57, "Overworld"),
    "Vehicular Manslaughter": AchieveData(58, "Overworld"),
    "Bulldozer": AchieveData(59, "Overworld"),
    "There are Some Who Call Him...": AchieveData(60, "Overworld"),
    "Deceiver of Fools": AchieveData(61, "Overworld"),
    "Sword of the Hero": AchieveData(62, "Hardmode"),
    "Lucky Break": AchieveData(63, "Overworld"),
    "Throwing Lines": AchieveData(64, "Overworld"),
    "Dye Hard": AchieveData(65, "Overworld"),
    "Sick Throw": AchieveData(66, "Postgame"),
    "The Frequent Flyer": AchieveData(67, "Overworld"),
    "The Cavalry": AchieveData(68, "Overworld"),
    "Completely Awesome": AchieveData(69, "Overworld"),
    "Til Death...": AchieveData(70, "Overworld"),
    "Archaeologist": AchieveData(71, "Jungle"),
    "Pretty in Pink": AchieveData(72, "Overworld"),
    "Rainbows and Unicorns": AchieveData(73, "Hardmode"),
    "You and What Army?": AchieveData(74, "Hardmode"),
    "Prismancer": AchieveData(75, "Hardmode"),
    "It Can Talk?!": AchieveData(76, "Hardmode"),
    "Watch Your Step!": AchieveData(77, "Overworld"),
    "Marathon Medalist": AchieveData(78, "Overworld"),
    "Glorious Golden Pole": AchieveData(79, "Overworld"),
    "Servant-in-Training": AchieveData(80, "Overworld"),
    "Good Little Slave": AchieveData(81, "Overworld"),
    "Trout Monkey": AchieveData(82, "Overworld"),
    "Fast and Fishious": AchieveData(83, "Overworld"),
    "Supreme Helper Minion!": AchieveData(84, "Overworld"),
    "Topped Off": AchieveData(85, "Hardmode"),
    "Slayer of Worlds": AchieveData(86, "Postgame"),
    "You Can Do It!": AchieveData(87, "Overworld"),
    "Matching Attire": AchieveData(88, "Overworld"),
}

exclusion_table = {
    "hardmode": {
        "It's Hard!",
        "Extra Shiny!",
        "Head in the Clouds",
        "Buckets of Bolts",
        "Drax Attax",
        "Photosynthesis",
        "Get a Life",
        "The Great Southern Plantkill",
        "Temple Raider",
        "Lihzahrdian Idol",
        "Robbing the Grave",
        "Big Booty",
        "Fish Out of Water",
        "Obsessive Devotion",
        "Star Destroyer",
        "Champion of Terraria",
        "Walk the Plank",
        "Kill the Sun",
        "Do You Want to Slay a Snowman?",
        "Tin-Foil Hatter",
        "Baleful Harvest",
        "Ice Scream",
        "Real Estate Agent",
        "Mecha Mayhem",
        "Gelatin World Tour",
        "Sword of the Hero",
        "Sick Throw",
        "Rainbows and Unicorns",
        "You and What Army?",
        "Prismancer",
        "It Can Talk?!",
        "Topped Off",
        "Slayer of Worlds",
    },
    "insane": {
        "Gelatin World Tour",
        "Fast and Fishious",
        "Supreme Helper Minion!",
        "Real Estate Agent",
        "Mecha Mayhem",
        "Bulldozer",
        "Marathon Medalist",
        "Slayer of Worlds",
    },
    "postgame": {
        "Slayer of Worlds",
        "Sick Throw",
    }
}

events_table = {
    "Still Hungry": "Victory"
}

lookup_id_to_name: typing.Dict[int, str] = {loc_data.id: loc_name for loc_name, loc_data in achievement_table.items() if
                                            loc_data.id}
