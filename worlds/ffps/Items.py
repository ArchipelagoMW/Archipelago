from BaseClasses import Item, ItemClassification
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: any
    setId: str


class FFPSItem(Item):
    game: str = "FFPS"


item_table = {
    "ScrapTrap": ItemData(55500, ItemClassification.progression, "m3"),
    "Scrap Baby": ItemData(55501, ItemClassification.progression, "m4"),
    "Lefty": ItemData(55502, ItemClassification.progression, "m5"),
    "Molten Freddy": ItemData(55503, ItemClassification.progression, "m2"),
    "Lefty Animatronic": ItemData(55604, ItemClassification.useful, "411"),
    "Data Archive Decor": ItemData(55605, ItemClassification.useful, "405"),
    "Balloon Cart Decor": ItemData(55607, ItemClassification.useful, "401"),
    "Pickles Decor": ItemData(55608, ItemClassification.useful, "415"),
    "Happy Frog Animatronic": ItemData(55609, ItemClassification.useful, "211"),
    "Fruit Maze Decor": ItemData(55610, ItemClassification.useful, "204"),
    "Roller Coaster Decor": ItemData(55611, ItemClassification.useful, "306"),
    "Confetti Floor": ItemData(55612, ItemClassification.useful, "402"),
    "Stage Upgrade": ItemData(55613, ItemClassification.useful, "stage"),
    "Pizza Light Decor": ItemData(55614, ItemClassification.useful, "404"),
    "Security Puppet Decor": ItemData(55615, ItemClassification.useful, "410"),
    "Punch Clown Decor": ItemData(55616, ItemClassification.useful, "308"),
    "Prize King Decor": ItemData(55617, ItemClassification.useful, "409"),
    "Sanitation Station Decor": ItemData(55618, ItemClassification.useful, "107"),
    "Gumball Machine Decor": ItemData(55619, ItemClassification.useful, "206"),
    "Mr Hugs Animatronic": ItemData(55620, ItemClassification.useful, "112"),
    "Orville Elephant Animatronic": ItemData(55621, ItemClassification.useful, "408"),
    "Paper Pals Decor": ItemData(55622, ItemClassification.useful, "115"),
    "Midnight Motorist Decor": ItemData(55623, ItemClassification.useful, "205"),
    "El Chip Animatronic": ItemData(55624, ItemClassification.progression, "413"),
    "Pan Stan Animatronic": ItemData(55625, ItemClassification.useful, "114"),
    "Bucket Bob Animatronic": ItemData(55626, ItemClassification.useful, "110"),
    "Ladder Tower Decor": ItemData(55627, ItemClassification.useful, "304"),
    "Music Man Animatronic": ItemData(55628, ItemClassification.progression, "412"),
    "Medical Station Decor": ItemData(55629, ItemClassification.useful, "310"),
    "Security Door Decor": ItemData(55630, ItemClassification.useful, "311"),
    "Stage Light Decor": ItemData(55631, ItemClassification.useful, "207"),
    "Pig Patch Animatronic": ItemData(55632, ItemClassification.useful, "214"),
    "Mr Hippo Animatronic": ItemData(55633, ItemClassification.useful, "212"),
    "Nedd Bear Animatronic": ItemData(55634, ItemClassification.useful, "213"),
    "Rockstar Bonnie Animatronic": ItemData(55635, ItemClassification.useful, "313"),
    "Lemonade Clown Decor": ItemData(55636, ItemClassification.useful, "307"),
    "Funtime Chica Animatronic": ItemData(55637, ItemClassification.progression, "414"),
    "No. 1 Crate Animatronic": ItemData(55638, ItemClassification.useful, "113"),
    "Mr Can Do Animatronic": ItemData(55639, ItemClassification.useful, "111"),
    "Rockstar Freddy Animatronic": ItemData(55640, ItemClassification.useful, "312"),
    "Gravity Vortex Decor": ItemData(55641, ItemClassification.useful, "407"),
    "Candy Cadet Decor": ItemData(55642, ItemClassification.useful, "215"),
    "Jukebox Decor": ItemData(55643, ItemClassification.useful, "309"),
    "Duck Pond Decor": ItemData(55644, ItemClassification.useful, "109"),
    "Ballpit Decor": ItemData(55645, ItemClassification.useful, "102"),
    "Side Stage Upgrade": ItemData(55646, ItemClassification.useful, "301"),
    "Rockstar Foxy Animatronic": ItemData(55647, ItemClassification.useful, "315"),
    "Rockstar Chica Animatronic": ItemData(55648, ItemClassification.useful, "314"),
    "Balloon Barrel Decor": ItemData(55649, ItemClassification.useful, "101"),
    "Carnival Hoops Decor": ItemData(55650, ItemClassification.useful, "305"),
    "Ballpit Tower Decor": ItemData(55651, ItemClassification.useful, "303"),
    "Traffic Light Decor": ItemData(55652, ItemClassification.useful, "210"),
    "Deluxe Ballpit Decor": ItemData(55653, ItemClassification.useful, "403"),
    "Cup Upgrade": ItemData(55654, ItemClassification.useful, "cups"),
    "Speaker Upgrade": ItemData(55655, ItemClassification.useful, "speakers"),
    "Discount Cooling Unit Decor": ItemData(55656, ItemClassification.useful, "108"),
    "Catalogue 2 Unlock": ItemData(55557, ItemClassification.progression, "un1"),
    "Catalogue 3 Unlock": ItemData(55558, ItemClassification.progression, "un2"),
    "Catalogue 4 Unlock": ItemData(55559, ItemClassification.progression, "un3"),
    "Printer Upgrade": ItemData(55560, ItemClassification.useful, "printer"),
    "Handyman Upgrade": ItemData(55561, ItemClassification.useful, "handyman"),
    "Internet Upgrade": ItemData(55562, ItemClassification.useful, "hispeed"),
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
