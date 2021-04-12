from BaseClasses import Region, Entrance, Location, MultiWorld, Item
import typing

class AdvancementData(typing.NamedTuple): 
    address: int
    hard_advancement: bool

class MinecraftAdvancement(Location): 
    game: str = "Minecraft"
    def __init__(self, player: int, name: str, address: int, parent, hard_advancement: bool):
        super().__init__(player, name, address, parent)
        self.hard_advancement = hard_advancement

advancement_table = {
    "Who is Cutting Onions?": AdvancementData(42000, False),
    "Oh Shiny": AdvancementData(42001, False),
    "Suit Up": AdvancementData(42002, False),
    "Very Very Frightening": AdvancementData(42003, True),
    "Hot Stuff": AdvancementData(42004, False),
    "Free the End": AdvancementData(42005, False),
    "A Furious Cocktail": AdvancementData(42006, False),
    "Best Friends Forever": AdvancementData(42007, False),
    "Bring Home the Beacon": AdvancementData(42008, False),
    "Not Today, Thank You": AdvancementData(42009, False),
    "Isn't It Iron Pick": AdvancementData(42010, False),
    "Local Brewery": AdvancementData(42011, False),
    "The Next Generation": AdvancementData(42012, False),
    "Fishy Business": AdvancementData(42013, False),
    "Hot Tourist Destinations": AdvancementData(42014, False),
    "This Boat Has Legs": AdvancementData(42015, False),
    "Sniper Duel": AdvancementData(42016, False),
    "Nether": AdvancementData(42017, False),
    "Great View From Up Here": AdvancementData(42018, False),
    "How Did We Get Here?": AdvancementData(42019, True),
    "Bullseye": AdvancementData(42020, False),
    "Spooky Scary Skeleton": AdvancementData(42021, False),
    "Two by Two": AdvancementData(42022, True),
    "Stone Age": AdvancementData(42023, False),
    "Two Birds, One Arrow": AdvancementData(42024, True),
    "We Need to Go Deeper": AdvancementData(42025, False),
    "Who's the Pillager Now?": AdvancementData(42026, False),
    "Getting an Upgrade": AdvancementData(42027, False),
    "Tactical Fishing": AdvancementData(42028, False),
    "Zombie Doctor": AdvancementData(42029, False),
    "The City at the End of the Game": AdvancementData(42030, False),
    "Ice Bucket Challenge": AdvancementData(42031, False),
    "Remote Getaway": AdvancementData(42032, False),
    "Into Fire": AdvancementData(42033, False),
    "War Pigs": AdvancementData(42034, False),
    "Take Aim": AdvancementData(42035, False),
    "Total Beelocation": AdvancementData(42036, False),
    "Arbalistic": AdvancementData(42037, True),
    "The End... Again...": AdvancementData(42038, False),
    "Acquire Hardware": AdvancementData(42039, False),
    "Not Quite \"Nine\" Lives": AdvancementData(42040, False),
    "Cover Me With Diamonds": AdvancementData(42041, False),
    "Sky's the Limit": AdvancementData(42042, False),
    "Hired Help": AdvancementData(42043, False),
    "Return to Sender": AdvancementData(42044, False),
    "Sweet Dreams": AdvancementData(42045, False),
    "You Need a Mint": AdvancementData(42046, False),
    "Adventure": AdvancementData(42047, False),
    "Monsters Hunted": AdvancementData(42048, True),
    "Enchanter": AdvancementData(42049, False),
    "Voluntary Exile": AdvancementData(42050, False),
    "Eye Spy": AdvancementData(42051, False),
    "The End": AdvancementData(42052, False),
    "Serious Dedication": AdvancementData(42053, True),
    "Postmortal": AdvancementData(42054, True),
    "Monster Hunter": AdvancementData(42055, False),
    "Adventuring Time": AdvancementData(42056, True),
    "A Seedy Place": AdvancementData(42057, False),
    "Those Were the Days": AdvancementData(42058, False),
    "Hero of the Village": AdvancementData(42059, False),
    "Hidden in the Depths": AdvancementData(42060, False),
    "Beaconator": AdvancementData(42061, True),
    "Withering Heights": AdvancementData(42062, False),
    "A Balanced Diet": AdvancementData(42063, True),
    "Subspace Bubble": AdvancementData(42064, False),
    "Husbandry": AdvancementData(42065, False),
    "Country Lode, Take Me Home": AdvancementData(42066, True),
    "Bee Our Guest": AdvancementData(42067, False),
    "What a Deal!": AdvancementData(42068, False),
    "Uneasy Alliance": AdvancementData(42069, True),
    "Diamonds!": AdvancementData(42070, False),
    "A Terrible Fortress": AdvancementData(42071, False),
    "A Throwaway Joke": AdvancementData(42072, False),
    "Minecraft": AdvancementData(42073, False),
    "Sticky Situation": AdvancementData(42074, False),
    "Ol' Betsy": AdvancementData(42075, False),
    "Cover Me in Debris": AdvancementData(42076, True),
    "The End?": AdvancementData(42077, False),
    "The Parrots and the Bats": AdvancementData(42078, False),
    "A Complete Catalogue": AdvancementData(42079, True)
}
'''
hard_advancement_vanilla = {
    "Very Very Frightening": "100 XP",
    "How Did We Get Here?": "500 XP",
    "Two By Two": "100 XP",
    "Two Birds, One Arrow": "50 XP",
    "Arbalistic": "100 XP",
    "Monsters Hunted": "100 XP",
    "Postmortal": "100 XP",
    "Adventuring Time": "500 XP",
    "Beaconator": "100 XP",
    "A Balanced Diet": "100 XP",
    "Uneasy Alliance": "100 XP",
    "Cover Me In Debris": "100 XP",
    "A Complete Catalogue": "50 XP"
}

postgame_advancement_vanilla = {
    "The Next Generation": "50 XP",
    "The End... Again...": "50 XP",
    "You Need a Mint": "50 XP"
}
'''