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
    "Timber!!": AchieveData(0, "Overworld"),
    "No Hobo": AchieveData(1, "Overworld"),
    "Stop! Hammer Time!": AchieveData(2, "Overworld"),
    "Ooo! Shiny!": AchieveData(3, "Overworld"),
    "Heart Breaker": AchieveData(4, "Overworld"),
    "Heavy Metal": AchieveData(5, "Overworld"),
    "I Am Loot!": AchieveData(6, "Overworld"),
    "Star Power": AchieveData(7, "Overworld"),
    "Hold on Tight!": AchieveData(8, "Overworld"),
    "Eye on You": AchieveData(9, "Overworld"),
    "Smashing, Poppet!": AchieveData(10, "Overworld"),
    "Worm Fodder": AchieveData(11, "Corruption"),
    "Mastermind": AchieveData(12, "Crimson"),
    "Where's My Honey?": AchieveData(13, "Jungle"),
    "Sting Operation": AchieveData(14, "Jungle"),
    "Boned": AchieveData(15, "Overworld"),
    "Dungeon Heist": AchieveData(16, "Dungeon"),
    "It's Getting Hot in Here": AchieveData(17, "Underworld"),
    "Miner for Fire": AchieveData(18, "Underworld"),
    "Still Hungry": AchieveData(19, "Underworld"),
    "It's Hard!": AchieveData(20, "Underworld"),
    "Begone, Evil!": AchieveData(21, "Hardmode"),
    "Extra Shiny!": AchieveData(22, "Hardmode"),
    "Head in the Clouds": AchieveData(23, "Hardmode"),
    "Like a Boss": AchieveData(24, "Overworld"),
    "Buckets of Bolts": AchieveData(25, "Hardmode"),
    "Drax Attax": AchieveData(26, "Hardmode"),
    "Photosynthesis": AchieveData(27, "Hardmode Jungle"),
    "Get a Life": AchieveData(28, "Hardmode Jungle"),
    "The Great Southern Plantkill": AchieveData(29, "Hardmode Jungle"),
    "Temple Raider": AchieveData(30, "Post-Plantera"),
    "Lihzahrdian Idol": AchieveData(31, "Post-Plantera"),
    "Robbing the Grave": AchieveData(32, "Post-Plantera"),
    "Big Booty": AchieveData(33, "Post-Plantera"),
    "Fish Out of Water": AchieveData(34, "Overworld"),
    "Obsessive Devotion": AchieveData(35, "Post-Golem"),
    "Star Destroyer": AchieveData(36, "Post-Golem"),
    "Champion of Terraria": AchieveData(37, "Post-Golem"),
    "Bloodbath": AchieveData(38, "Overworld"),
    "Slippery Shinobi": AchieveData(39, "Overworld"),
    "Goblin Punter": AchieveData(40, "Overworld"),
    "Walk the Plank": AchieveData(41, "Hardmode"),
    "Kill the Sun": AchieveData(42, "Hardmode"),
    "Do You Want to Slay a Snowman?": AchieveData(43, "Hardmode"),
    "Tin-Foil Hatter": AchieveData(44, "Post-Golem"),
    "Baleful Harvest": AchieveData(45, "Post-Plantera"),
    "Ice Scream": AchieveData(46, "Post-Plantera"),
    "Sticky Situation": AchieveData(47, "Overworld"),
    "Real Estate Agent": AchieveData(48, "Postgame"),
    "Not the Bees!": AchieveData(49, "Jungle"),
    "Jeepers Creepers": AchieveData(50, "Overworld"),
    "Funkytown": AchieveData(51, "Overworld"),
    "Into Orbit": AchieveData(52, "Overworld"),
    "Rock Bottom": AchieveData(53, "Underworld"),
    "Mecha Mayhem": AchieveData(54, "Hardmode"),
    "Gelatin World Tour": AchieveData(55, "Postgame"),
    "Fashion Statement": AchieveData(56, "Overworld"),
    "Vehicular Manslaughter": AchieveData(57, "Overworld"),
    "Bulldozer": AchieveData(58, "Overworld"),
    "There are Some Who Call Him...": AchieveData(59, "Overworld"),
    "Deceiver of Fools": AchieveData(60, "Overworld"),
    "Sword of the Hero": AchieveData(61, "Hardmode"),
    "Lucky Break": AchieveData(62, "Overworld"),
    "Throwing Lines": AchieveData(63, "Overworld"),
    "Dye Hard": AchieveData(64, "Overworld"),
    "Sick Throw": AchieveData(65, "Postgame"),
    "The Frequent Flyer": AchieveData(66, "Overworld"),
    "The Cavalry": AchieveData(67, "Overworld"),
    "Completely Awesome": AchieveData(68, "Overworld"),
    "Til Death...": AchieveData(69, "Overworld"),
    "Archaeologist": AchieveData(70, "Jungle"),
    "Pretty in Pink": AchieveData(71, "Overworld"),
    "Rainbows and Unicorns": AchieveData(72, "Hardmode"),
    "You and What Army?": AchieveData(73, "Hardmode"),
    "Prismancer": AchieveData(74, "Hardmode"),
    "It Can Talk?!": AchieveData(75, "Hardmode"),
    "Watch Your Step!": AchieveData(76, "Overworld"),
    "Marathon Medalist": AchieveData(77, "Overworld"),
    "Glorious Golden Pole": AchieveData(78, "Overworld"),
    "Servant-in-Training": AchieveData(79, "Overworld"),
    "Good Little Slave": AchieveData(80, "Overworld"),
    "Trout Monkey": AchieveData(81, "Overworld"),
    "Fast and Fishious": AchieveData(82, "Overworld"),
    "Supreme Helper Minion!": AchieveData(83, "Overworld"),
    "Topped Off": AchieveData(84, "Hardmode"),
    "Slayer of Worlds": AchieveData(85, "Postgame"),
    "You Can Do It!": AchieveData(86, "Overworld"),
    "Matching Attire": AchieveData(87, "Overworld"),
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
