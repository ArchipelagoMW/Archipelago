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
    "Lefty Animatronic": ItemData(55504, ItemClassification.useful, "411"),
    "Data Archive Decor": ItemData(55505, ItemClassification.useful, "405"),
    "Balloon Cart Decor": ItemData(55507, ItemClassification.useful, "401"),
    "Pickles Decor": ItemData(55508, ItemClassification.useful, "415"),
    "Happy Frog Animatronic": ItemData(55509, ItemClassification.useful, "211"),
    "Fruit Maze Decor": ItemData(55510, ItemClassification.useful, "204"),
    "Roller Coaster Decor": ItemData(55511, ItemClassification.useful, "306"),
    "Confetti Floor": ItemData(55512, ItemClassification.useful, "402"),
    "Stage Upgrade": ItemData(55513, ItemClassification.useful, "stage"),
    "Pizza Light Decor": ItemData(55514, ItemClassification.useful, "404"),
    "Security Puppet Decor": ItemData(55515, ItemClassification.useful, "410"),
    "Punch Clown Decor": ItemData(55516, ItemClassification.useful, "308"),
    "Prize King Decor": ItemData(55517, ItemClassification.useful, "409"),
    "Sanitation Station Decor": ItemData(55518, ItemClassification.useful, "107"),
    "Gumball Machine Decor": ItemData(55519, ItemClassification.useful, "206"),
    "Mr Hugs Animatronic": ItemData(55520, ItemClassification.useful, "112"),
    "Orville Elephant Animatronic": ItemData(55521, ItemClassification.useful, "408"),
    "Paper Pals Decor": ItemData(55522, ItemClassification.useful, "115"),
    "Midnight Moterist Decor": ItemData(55523, ItemClassification.useful, "205"),
    "El Chip Animatronic": ItemData(55524, ItemClassification.useful, "413"),
    "Pan Stan Animatronic": ItemData(55525, ItemClassification.useful, "114"),
    "Bucket Bob Animatronic": ItemData(55526, ItemClassification.useful, "110"),
    "Ladder Tower Decor": ItemData(55527, ItemClassification.useful, "304"),
    "Music Man Animatronic": ItemData(55528, ItemClassification.useful, "412"),
    "Medical Station Decor": ItemData(55529, ItemClassification.useful, "310"),
    "Security Door Decor": ItemData(55530, ItemClassification.useful, "311"),
    "Stage Light Decor": ItemData(55531, ItemClassification.useful, "207"),
    "Pig Patch Animatronic": ItemData(55532, ItemClassification.useful, "214"),
    "Mr Hippo Animatronic": ItemData(55533, ItemClassification.useful, "212"),
    "Nedd Bear Animatronic": ItemData(55534, ItemClassification.useful, "213"),
    "Rockstar Bonnie Animatronic": ItemData(55535, ItemClassification.useful, "313"),
    "Lemonade Clown Decor": ItemData(55536, ItemClassification.useful, "307"),
    "Funtime Chica Animatronic": ItemData(55537, ItemClassification.useful, "414"),
    "No. 1 Crate Animatronic": ItemData(55538, ItemClassification.useful, "113"),
    "Mr Can Do Animatronic": ItemData(55539, ItemClassification.useful, "111"),
    "Rockstar Freddy Animatronic": ItemData(55540, ItemClassification.useful, "312"),
    "Gravity Vortex Decor": ItemData(55541, ItemClassification.useful, "407"),
    "Candy Cadet Decor": ItemData(55542, ItemClassification.useful, "215"),
    "Jukebox Decor": ItemData(55543, ItemClassification.useful, "309"),
    "Duck Pond Decor": ItemData(55544, ItemClassification.useful, "109"),
    "Ballpit Decor": ItemData(55545, ItemClassification.useful, "102"),
    "Side Stage Upgrade": ItemData(55546, ItemClassification.useful, "301"),
    "Rockstar Foxy Animatronic": ItemData(55547, ItemClassification.useful, "315"),
    "Rockstar Chica Animatronic": ItemData(55548, ItemClassification.useful, "314"),
    "Balloon Barrel Decor": ItemData(55549, ItemClassification.useful, "101"),
    "Carnival Hoops Decor": ItemData(55550, ItemClassification.useful, "305"),
    "Ballpit Tower Decor": ItemData(55551, ItemClassification.useful, "303"),
    "Traffic Light Decor": ItemData(55552, ItemClassification.useful, "210"),
    "Deluxe Ballpit Decor": ItemData(55553, ItemClassification.useful, "403"),
    "Cup Upgrade": ItemData(55554, ItemClassification.useful, "cups"),
    "Speaker Upgrade": ItemData(55555, ItemClassification.useful, "speakers"),
    "Discount Cooling Unit Decor": ItemData(55556, ItemClassification.useful, "108"),
    "Catalogue 2 Unlock": ItemData(None, ItemClassification.progression, ""),
    "Catalogue 3 Unlock": ItemData(None, ItemClassification.progression, ""),
    "Catalogue 4 Unlock": ItemData(None, ItemClassification.progression, ""),
}

required_items = {
}

item_frequencies = {

}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
