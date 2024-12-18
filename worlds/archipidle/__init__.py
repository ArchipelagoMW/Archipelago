from BaseClasses import Item, MultiWorld, Region, Location, Entrance, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from datetime import datetime
from .Items import item_table
from .Rules import set_rules


class ArchipIDLEWebWorld(WebWorld):
    theme = 'partyTime'
    tutorials = [
        Tutorial(
            tutorial_name='Setup Guide',
            description='A guide to playing Archipidle',
            language='English',
            file_name='guide_en.md',
            link='guide/en',
            authors=['Farrak Kilhn']
        ),
        Tutorial(
            tutorial_name='Guide d installation',
            description='Un guide pour jouer à Archipidle',
            language='Français',
            file_name='guide_fr.md',
            link='guide/fr',
            authors=['TheLynk']
        )
    ]


class ArchipIDLEWorld(World):
    """
    An idle game which sends a check every thirty to sixty seconds, up to two hundred checks.
    """
    game = "ArchipIDLE"
    topology_present = False
    hidden = (datetime.now().month != 4)  # ArchipIDLE is only visible during April
    web = ArchipIDLEWebWorld()

    item_name_to_id = {}
    start_id = 9000
    for item in item_table:
        item_name_to_id[item] = start_id
        start_id += 1

    location_name_to_id = {}
    start_id = 9000
    for i in range(1, 201):
        location_name_to_id[f"IDLE item number {i}"] = start_id
        start_id += 1

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_item(self, name: str) -> Item:
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_items(self):
        item_pool = [
            ArchipIDLEItem(
                item_table[0],
                ItemClassification.progression,
                self.item_name_to_id[item_table[0]],
                self.player
            )
        ]

        for i in range(40):
            item_pool.append(ArchipIDLEItem(
                item_table[1],
                ItemClassification.progression,
                self.item_name_to_id[item_table[1]],
                self.player
            ))

        for i in range(40):
            item_pool.append(ArchipIDLEItem(
                item_table[2],
                ItemClassification.filler,
                self.item_name_to_id[item_table[2]],
                self.player
            ))

        item_table_copy = list(item_table[3:])
        self.random.shuffle(item_table_copy)
        for i in range(119):
            item_pool.append(ArchipIDLEItem(
                item_table_copy[i],
                ItemClassification.progression if i < 9 else ItemClassification.filler,
                self.item_name_to_id[item_table_copy[i]],
                self.player
            ))

        self.multiworld.itempool += item_pool

    def create_regions(self):
        self.multiworld.regions += [
            create_region(self.multiworld, self.player, 'Menu', None, ['Entrance to IDLE Zone']),
            create_region(self.multiworld, self.player, 'IDLE Zone', self.location_name_to_id)
        ]

        # link up our region with the entrance we just made
        self.multiworld.get_entrance('Entrance to IDLE Zone', self.player)\
            .connect(self.multiworld.get_region('IDLE Zone', self.player))

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(item_table)


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    region = Region(name, player, world)
    if locations:
        for location_name in locations.keys():
            location = ArchipIDLELocation(player, location_name, locations[location_name], region)
            region.locations.append(location)

    if exits:
        for _exit in exits:
            region.exits.append(Entrance(player, _exit, region))

    return region


class ArchipIDLEItem(Item):
    game = "ArchipIDLE"


class ArchipIDLELocation(Location):
    game: str = "ArchipIDLE"
