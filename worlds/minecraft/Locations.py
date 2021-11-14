from BaseClasses import Location
import typing


class AdvData(typing.NamedTuple):
    id: typing.Optional[int]
    region: str


class MinecraftAdvancement(Location):
    game: str = "Minecraft"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address


advancement_table = {
    "Who is Cutting Onions?": AdvData(42000, 'Overworld'),
    "Oh Shiny": AdvData(42001, 'Overworld'),
    "Suit Up": AdvData(42002, 'Overworld'),
    "Very Very Frightening": AdvData(42003, 'Overworld'),
    "Hot Stuff": AdvData(42004, 'Overworld'),
    "Free the End": AdvData(42005, 'The End'),
    "A Furious Cocktail": AdvData(42006, 'Nether Fortress'),
    "Best Friends Forever": AdvData(42007, 'Overworld'),
    "Bring Home the Beacon": AdvData(42008, 'Nether Fortress'),
    "Not Today, Thank You": AdvData(42009, 'Overworld'),
    "Isn't It Iron Pick": AdvData(42010, 'Overworld'),
    "Local Brewery": AdvData(42011, 'Nether Fortress'),
    "The Next Generation": AdvData(42012, 'The End'),
    "Fishy Business": AdvData(42013, 'Overworld'),
    "Hot Tourist Destinations": AdvData(42014, 'The Nether'),
    "This Boat Has Legs": AdvData(42015, 'The Nether'),
    "Sniper Duel": AdvData(42016, 'Overworld'),
    "Nether": AdvData(42017, 'The Nether'),
    "Great View From Up Here": AdvData(42018, 'End City'),
    "How Did We Get Here?": AdvData(42019, 'Nether Fortress'),
    "Bullseye": AdvData(42020, 'Overworld'),
    "Spooky Scary Skeleton": AdvData(42021, 'Nether Fortress'),
    "Two by Two": AdvData(42022, 'The Nether'),
    "Stone Age": AdvData(42023, 'Overworld'),
    "Two Birds, One Arrow": AdvData(42024, 'Overworld'),
    "We Need to Go Deeper": AdvData(42025, 'The Nether'),
    "Who's the Pillager Now?": AdvData(42026, 'Pillager Outpost'),
    "Getting an Upgrade": AdvData(42027, 'Overworld'),
    "Tactical Fishing": AdvData(42028, 'Overworld'),
    "Zombie Doctor": AdvData(42029, 'Overworld'),
    "The City at the End of the Game": AdvData(42030, 'End City'),
    "Ice Bucket Challenge": AdvData(42031, 'Overworld'),
    "Remote Getaway": AdvData(42032, 'The End'),
    "Into Fire": AdvData(42033, 'Nether Fortress'),
    "War Pigs": AdvData(42034, 'Bastion Remnant'),
    "Take Aim": AdvData(42035, 'Overworld'),
    "Total Beelocation": AdvData(42036, 'Overworld'),
    "Arbalistic": AdvData(42037, 'Overworld'),
    "The End... Again...": AdvData(42038, 'The End'),
    "Acquire Hardware": AdvData(42039, 'Overworld'),
    "Not Quite \"Nine\" Lives": AdvData(42040, 'The Nether'),
    "Cover Me With Diamonds": AdvData(42041, 'Overworld'),
    "Sky's the Limit": AdvData(42042, 'End City'),
    "Hired Help": AdvData(42043, 'Overworld'),
    "Return to Sender": AdvData(42044, 'The Nether'),
    "Sweet Dreams": AdvData(42045, 'Overworld'),
    "You Need a Mint": AdvData(42046, 'The End'),
    "Adventure": AdvData(42047, 'Overworld'),
    "Monsters Hunted": AdvData(42048, 'Overworld'),
    "Enchanter": AdvData(42049, 'Overworld'),
    "Voluntary Exile": AdvData(42050, 'Pillager Outpost'),
    "Eye Spy": AdvData(42051, 'Overworld'),
    "The End": AdvData(42052, 'The End'),
    "Serious Dedication": AdvData(42053, 'The Nether'),
    "Postmortal": AdvData(42054, 'Village'),
    "Monster Hunter": AdvData(42055, 'Overworld'),
    "Adventuring Time": AdvData(42056, 'Overworld'),
    "A Seedy Place": AdvData(42057, 'Overworld'),
    "Those Were the Days": AdvData(42058, 'Bastion Remnant'),
    "Hero of the Village": AdvData(42059, 'Village'),
    "Hidden in the Depths": AdvData(42060, 'The Nether'),
    "Beaconator": AdvData(42061, 'Nether Fortress'),
    "Withering Heights": AdvData(42062, 'Nether Fortress'),
    "A Balanced Diet": AdvData(42063, 'Village'),
    "Subspace Bubble": AdvData(42064, 'The Nether'),
    "Husbandry": AdvData(42065, 'Overworld'),
    "Country Lode, Take Me Home": AdvData(42066, 'The Nether'),
    "Bee Our Guest": AdvData(42067, 'Overworld'),
    "What a Deal!": AdvData(42068, 'Village'),
    "Uneasy Alliance": AdvData(42069, 'The Nether'),
    "Diamonds!": AdvData(42070, 'Overworld'),
    "A Terrible Fortress": AdvData(42071, 'Nether Fortress'),
    "A Throwaway Joke": AdvData(42072, 'Overworld'),
    "Minecraft": AdvData(42073, 'Overworld'),
    "Sticky Situation": AdvData(42074, 'Overworld'),
    "Ol' Betsy": AdvData(42075, 'Overworld'),
    "Cover Me in Debris": AdvData(42076, 'The Nether'),
    "The End?": AdvData(42077, 'The End'),
    "The Parrots and the Bats": AdvData(42078, 'Overworld'),
    "A Complete Catalogue": AdvData(42079, 'Village'),
    "Getting Wood": AdvData(42080, 'Overworld'),
    "Time to Mine!": AdvData(42081, 'Overworld'),
    "Hot Topic": AdvData(42082, 'Overworld'),
    "Bake Bread": AdvData(42083, 'Overworld'),
    "The Lie": AdvData(42084, 'Overworld'),
    "On a Rail": AdvData(42085, 'Overworld'),
    "Time to Strike!": AdvData(42086, 'Overworld'),
    "Cow Tipper": AdvData(42087, 'Overworld'),
    "When Pigs Fly": AdvData(42088, 'Overworld'),
    "Overkill": AdvData(42089, 'Nether Fortress'),
    "Librarian": AdvData(42090, 'Overworld'),
    "Overpowered": AdvData(42091, 'Bastion Remnant'),

    "Blaze Spawner": AdvData(None, 'Nether Fortress'),
    "Ender Dragon": AdvData(None, 'The End')
}

exclusion_table = {
    "hard": {
        "Very Very Frightening",
        "A Furious Cocktail",
        "Two by Two",
        "Two Birds, One Arrow",
        "Arbalistic",
        "Monsters Hunted",
        "Beaconator",
        "A Balanced Diet",
        "Uneasy Alliance",
        "Cover Me in Debris",
        "A Complete Catalogue",
    },
    "insane": {
        "How Did We Get Here?",
        "Adventuring Time",
    },
    "postgame": {
        "Free the End",
        "The Next Generation",
        "The End... Again...",
        "You Need a Mint",
        "Monsters Hunted",
    }
}

events_table = {
    "Ender Dragon": "Victory"
}

lookup_id_to_name: typing.Dict[int, str] = {loc_data.id: loc_name for loc_name, loc_data in advancement_table.items() if
                                            loc_data.id}
