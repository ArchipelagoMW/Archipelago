from typing import Dict, Set, Tuple, NamedTuple

class ItemData(NamedTuple):
    category: str
    code: int
    amount: int = 1
    progression: bool = False
    progression_skip_balancing: bool = False
    useful: bool = False
    trap: bool = False

item_table: Dict[str, ItemData] = {
        #Rome
    "Gladiator's Spear": ItemData('Artifacts', 0x198401, progression=True),
    'Coins from the Trevi Fountain': ItemData('Artifacts', 0x198402, progression=True),
    'Sistine Chapel Ceiling': ItemData('Artifacts', 0x198403, progression=True),
        #Paris
    'Notre Dame Bell': ItemData('Artifacts', 0x198404, progression=True),
    'Eternal Flame': ItemData('Artifacts', 0x198405, progression=True),
    'Tricolor': ItemData('Artifacts', 0x198406, progression=True),
        #London
    'Crown Jewels': ItemData('Artifacts', 0x198407, progression=True),
    'Bust of Shakespeare': ItemData('Artifacts', 0x198408, progression=True),
    "Big Ben's Minute Hand": ItemData('Artifacts', 0x198409, progression=True),
        #New York
    'King Kong': ItemData('Artifacts', 0x19840A, progression=True),
    'Statue of Liberty Torch': ItemData('Artifacts', 0x19840B, progression=True),
    "Statue of Prometheus": ItemData('Artifacts', 0x19840C, progression=True),
        #San Francisco
    'Golden Gate Bridge Foghorn': ItemData('Artifacts', 0x19840D, progression=True),
    'Window from Coit Tower': ItemData('Artifacts', 0x19840E, progression=True),
    "Top of the Transamerica Pyramid": ItemData('Artifacts', 0x19840F, progression=True),
        #Athens
    'Caryatid': ItemData('Artifacts', 0x198410, progression=True),
    'Brass Plaque': ItemData('Artifacts', 0x198411, progression=True),
    "Parthenon Column": ItemData('Artifacts', 0x198412, progression=True),
        #Sydney
    'Surfboard from Bondi Beach': ItemData('Artifacts', 0x198413, progression=True),
    'Taronga Zoo Koala': ItemData('Artifacts', 0x198414, progression=True),
    "Sydney Opera Sheet Music": ItemData('Artifacts', 0x198415, progression=True),
        #Tokyo
    "Great Buddha's Orange": ItemData('Artifacts', 0x198416, progression=True),
    'Sensoji Temple Latern': ItemData('Artifacts', 0x198417, progression=True),
    "Sumo Apron": ItemData('Artifacts', 0x198418, progression=True),
        #Nairobi
    'Baby Elephant': ItemData('Artifacts', 0x198419, progression=True),
    'Maasai Headdress': ItemData('Artifacts', 0x19841A, progression=True),
    "Human Skull": ItemData('Artifacts', 0x19841B, progression=True),
        #Rio de Janeiro
    'Spotlight from Christ the Redeemer Statue': ItemData('Artifacts', 0x19841C, progression=True),
    'Copacabana Beach Seashell': ItemData('Artifacts', 0x19841D, progression=True),
    "Sugar Loaf Mountain Cable Car": ItemData('Artifacts', 0x19841E, progression=True),
        #Cairo
    'Top Brick of the Great Pyramid': ItemData('Artifacts', 0x19841F, progression=True),
    'Gingerbread Clock': ItemData('Artifacts', 0x198420, progression=True),
    "Klaft of the Sphinx": ItemData('Artifacts', 0x198421, progression=True),
        #Moscow
    "Cannonball from the Emperor's Cannon": ItemData('Artifacts', 0x198422, progression=True),
    'Cathedral Dome': ItemData('Artifacts', 0x198423, progression=True),
    "Bolshoi Ballet Slipper": ItemData('Artifacts', 0x198424, progression=True),
        #Beijing
    'Hall of Good Harvest': ItemData('Artifacts', 0x198425, progression=True),
    'Stone from the Great Wall': ItemData('Artifacts', 0x198426, progression=True),
    "Gate of Heavenly Peace": ItemData('Artifacts', 0x198427, progression=True),
        #Buenos Aires
    'Flute from the Teatro Colon': ItemData('Artifacts', 0x198428, progression=True),
    'Boleadoras': ItemData('Artifacts', 0x198429, progression=True),
    "Stone from the Obelisk": ItemData('Artifacts', 0x19842A, progression=True),
        #Mexico City
    'Angel': ItemData('Artifacts', 0x19842B, progression=True),
    'Diego Rivera Mural': ItemData('Artifacts', 0x19842C, progression=True),
    "Fine Arts Catalog": ItemData('Artifacts', 0x19842D, progression=True),

    "Castle Floor Key": ItemData('Other', 0x19842E, 2, progression=True),
    "Newspaper": ItemData('Other', 0x19842F),
    "Mario": ItemData('Events', None, 0, progression=True),
    "Artifact Secured": ItemData('Events', None, 0, progression=True),
    "Photograph": ItemData('Other', 0x198430),
    "Advice": ItemData('Other', 0x198431)

}

filler_items: Tuple[str, ...] = (
    'Photograph',
    'Newspaper',
    'Advice'
)

artifacts: Tuple[str, ...] = (
    "Gladiator's Spear"
    "Coins from the Trevi Fountain"
    "Sistine Chapel Ceiling"
    "Notre Dame Bell"
    "Eternal Flame"
    "Tricolor"
)

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        if data.category != "Events":
            categories.setdefault(data.category, set()).add(name)

    return categories
