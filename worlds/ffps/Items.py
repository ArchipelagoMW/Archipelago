from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    setId: str


class FFPSItem(Item):
    game: str = "FFPS"


item_table = {
    "ScrapTrap": ItemData(55500, True, "m3"),
    "Scrap Baby": ItemData(55501, True, "m4"),
    "Lefty": ItemData(55502, True, "m5"),
    "Molten Freddy": ItemData(55503, True, "m2"),
    "Lefty Animatronic": ItemData(55504, False, "411"),
    "Data Archive Decor": ItemData(55505, False, "405"),
    "Balloon Cart Decor": ItemData(55507, False, "401"),
    "Pickles Decor": ItemData(55508, False, "415"),
    "Happy Frog Animatronic": ItemData(55509, False, "211"),
    "Fruit Maze Decor": ItemData(55510, False, "204"),
    "Roller Coaster Decor": ItemData(55511, False, "306"),
    "Confetti Floor": ItemData(55512, False, "402"),
    "Stage Upgrade": ItemData(55513, False, "stage"),
    "Pizza Light Decor": ItemData(55514, False, "404"),
    "Security Puppet Decor": ItemData(55515, False, "410"),
    "Punch Clown Decor": ItemData(55516, False, "308"),
    "Prize King Decor": ItemData(55517, False, "409"),
    "Sanitation Station Decor": ItemData(55518, False, "107"),
    "Gumball Machine Decor": ItemData(55519, False, "206"),
    "Mr Hugs Animatronic": ItemData(55520, False, "112"),
    "Orville Elephant Animatronic": ItemData(55521, False, "408"),
    "Paper Pals Decor": ItemData(55522, False, "115"),
    "Midnight Moterist Decor": ItemData(55523, False, "205"),
    "El Chip Animatronic": ItemData(55524, False, "413"),
    "Pan Stan Animatronic": ItemData(55525, False, "114"),
    "Bucket Bob Animatronic": ItemData(55526, False, "110"),
    "Ladder Tower Decor": ItemData(55527, False, "304"),
    "Music Man Animatronic": ItemData(55528, False, "412"),
    "Medical Station Decor": ItemData(55529, False, "310"),
    "Security Door Decor": ItemData(55530, False, "311"),
    "Stage Light Decor": ItemData(55531, False, "207"),
    "Pig Patch Animatronic": ItemData(55532, False, "214"),
    "Mr Hippo Animatronic": ItemData(55533, False, "212"),
    "Nedd Bear Animatronic": ItemData(55534, False, "213"),
    "Rockstar Bonnie Animatronic": ItemData(55535, False, "313"),
    "Lemonade Clown Decor": ItemData(55536, False, "307"),
    "Funtime Chica Animatronic": ItemData(55537, False, "414"),
    "No. 1 Crate Animatronic": ItemData(55538, False, "113"),
    "Mr Can Do Animatronic": ItemData(55539, False, "111"),
    "Rockstar Freddy Animatronic": ItemData(55540, False, "312"),
    "Gravity Vortex Decor": ItemData(55541, False, "407"),
    "Candy Cadet Decor": ItemData(55542, False, "215"),
    "Jukebox Decor": ItemData(55543, False, "309"),
    "Duck Pond Decor": ItemData(55544, False, "109"),
    "Ballpit Decor": ItemData(55545, False, "102"),
    "Side Stage Upgrade": ItemData(55546, False, "301"),
    "Rockstar Foxy Animatronic": ItemData(55547, False, "315"),
    "Rockstar Chica Animatronic": ItemData(55548, False, "314"),
    "Balloon Barrel Decor": ItemData(55549, False, "101"),
    "Carnival Hoops Decor": ItemData(55550, False, "305"),
    "Ballpit Tower Decor": ItemData(55551, False, "303"),
    "Traffic Light Decor": ItemData(55552, False, "210"),
    "Deluxe Ballpit Decor": ItemData(55553, False, "403"),
    "Cup Upgrade": ItemData(55554, False, "cups"),
    "Speaker Upgrade": ItemData(55555, False, "speakers"),
    "Discount Cooling Unity Decor": ItemData(55556, False, "108"),
}

required_items = {
}

item_frequencies = {

}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
