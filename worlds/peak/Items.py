import typing
from BaseClasses import Item, ItemClassification


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification
    quantity: int = 1


class PeakItem(Item):
    game: str = "PEAK"

    def __init__(self, name: str, classification: ItemClassification, code: int = None, player: int = None):
        super(PeakItem, self).__init__(name, classification, code, player)

class PeakLttPText(typing.NamedTuple):
    pedestal: typing.Optional[str]
    sickkid: typing.Optional[str]
    magicshop: typing.Optional[str]
    zora: typing.Optional[str]
    fluteboy: typing.Optional[str]

LttPCreditsText = {
    "Progressive Ascent": PeakLttPText("Another difficult climb",
                                "Hope its not too STEEP",
                                "Climb higher for 9999.99",
                                "I need to go UP",
                                "What dangers await?"),
    "Progressive Endurance": PeakLttPText("Endurance increased",
                                  "You look more STAMINAous",
                                  "Stamina upgraded for 9999.99",
                                  "You seem more ENDURANT",
                                  "Increased stamina capacity!"),
    "Progressive Mountain": PeakLttPText("A new mountain appears",
                                 "Another PEAK to conquer",
                                 "New mountain unlocked for 9999.99",
                                 "A new MOUNTAIN has formed",
                                 "New mountain unlocked!"),
    "Progressive Stamina Bar": PeakLttPText("Stamina bar increased",
                                        "Your stamina looks BIGGER",
                                        "That's a lot of bars!",
                                        "You ready for a marathon?",
                                        "Wow you must be really fit now!"),
}


progression_table = {
    "Progressive Ascent": ItemData(76019, ItemClassification.progression),
    "Progressive Endurance": ItemData(76026, ItemClassification.progression),
    "Progressive Mountain": ItemData(76050, ItemClassification.progression),
    #"Ascent 2 Unlock": ItemData(76020, ItemClassification.progression),
    #"Ascent 3 Unlock": ItemData(76021, ItemClassification.progression),
    #"Ascent 4 Unlock": ItemData(76022, ItemClassification.progression),
    #"Ascent 5 Unlock": ItemData(76023, ItemClassification.progression),
    #"Ascent 6 Unlock": ItemData(76024, ItemClassification.progression),
    #"Ascent 7 Unlock": ItemData(76025, ItemClassification.progression),
}

useful_table = {
    "Progressive Stamina Bar":      ItemData(78001, ItemClassification.progression_skip_balancing),
    "Rope Spool":                   ItemData(77000, ItemClassification.useful),
    "Rope Cannon":                  ItemData(77001, ItemClassification.useful),
    "Anti-Rope Spool":              ItemData(77002, ItemClassification.useful),
    "Anti-Rope Cannon":             ItemData(77003, ItemClassification.useful),
    "Chain Launcher":               ItemData(76007, ItemClassification.useful),
    "Piton":                        ItemData(77005, ItemClassification.useful),
    "Magic Bean":                   ItemData(77006, ItemClassification.useful),
    "Parasol":                      ItemData(77007, ItemClassification.useful),
    "Balloon":                      ItemData(77008, ItemClassification.useful),
    "Balloon Bunch":                ItemData(77009, ItemClassification.useful),
    "Scout Cannon":                 ItemData(77010, ItemClassification.useful),
    "Flying Disc":                  ItemData(77020, ItemClassification.useful),
    "Rescue Claw":                  ItemData(77084, ItemClassification.useful),
    "Lantern":                      ItemData(77013, ItemClassification.useful),
    "Flare":                        ItemData(77014, ItemClassification.useful),
    "Torch":                        ItemData(77015, ItemClassification.useful),
    "Faerie Lantern":               ItemData(77026, ItemClassification.useful),
    "Cactus":                       ItemData(77016, ItemClassification.useful),
    "Compass":                      ItemData(77017, ItemClassification.useful),
    "Pirate's Compass":             ItemData(77018, ItemClassification.useful),
    "Binoculars":                   ItemData(77019, ItemClassification.useful),
    "Guidebook":                    ItemData(77065, ItemClassification.useful),
    "Portable Stove":               ItemData(77011, ItemClassification.useful),
    "Checkpoint Flag":              ItemData(77012, ItemClassification.useful),
    "Scout Effigy":                 ItemData(77030, ItemClassification.useful),
    "First-Aid Kit":                ItemData(77022, ItemClassification.useful),
    "Antidote":                     ItemData(77023, ItemClassification.useful),
    "Heat Pack":                    ItemData(77024, ItemClassification.useful),
    "Cure-All":                     ItemData(77025, ItemClassification.useful),
    "Remedy Fungus":                ItemData(77027, ItemClassification.useful),
    "Medicinal Root":               ItemData(77036, ItemClassification.useful),
    "Aloe Vera":                    ItemData(77028, ItemClassification.useful),
    "Sunscreen":                    ItemData(77029, ItemClassification.useful),
    "Marshmallow":                  ItemData(77082, ItemClassification.useful),
    "Glizzy":                       ItemData(77083, ItemClassification.useful),
    "Fortified Milk":               ItemData(77085, ItemClassification.useful),
    "Pandora's Lunchbox":           ItemData(77032, ItemClassification.useful),
    "Ancient Idol":                 ItemData(77033, ItemClassification.useful),
    "Bugle of Friendship":          ItemData(77034, ItemClassification.useful),
    "Bugle":                        ItemData(77035, ItemClassification.useful),
    "Book of Bones":                ItemData(77075, ItemClassification.useful),
    "Strange Gem":                  ItemData(77066, ItemClassification.useful),
    "Shelf Shroom":                 ItemData(77037, ItemClassification.useful),
    "Bounce Shroom":                ItemData(77038, ItemClassification.useful),
    "Button Shroom":                ItemData(77046, ItemClassification.useful),
    "Bugle Shroom":                 ItemData(77047, ItemClassification.useful),
    "Cluster Shroom":               ItemData(77048, ItemClassification.useful),
    "Chubby Shroom":                ItemData(77049, ItemClassification.useful),
    "Cloud Fungus":                 ItemData(77086, ItemClassification.useful),
    "Airline Food":                 ItemData(77042, ItemClassification.useful),
    "Energy Drink":                 ItemData(77043, ItemClassification.useful),
    "Sports Drink":                 ItemData(77044, ItemClassification.useful),
    "Big Lollipop":                 ItemData(77045, ItemClassification.useful),
    "Honeycomb":                    ItemData(77069, ItemClassification.useful),
    "Bing Bong":                    ItemData(77053, ItemClassification.useful),
    "Orange Winterberry":           ItemData(77063, ItemClassification.useful),
    "Speed Upgrade":                ItemData(76031, ItemClassification.useful),
    "Scoutmaster's Bugle":          ItemData(77100, ItemClassification.useful),
    "Napberry":                     ItemData(77096, ItemClassification.useful),
    "Blowgun":                      ItemData(77122, ItemClassification.useful),
}

filler_table = {
    "Bandages":                     ItemData(77021, ItemClassification.filler),
    "Granola Bar":                  ItemData(77040, ItemClassification.filler),
    "Trail Mix":                    ItemData(77039, ItemClassification.filler),
    "Scout Cookies":                ItemData(77041, ItemClassification.filler),
    "Red Crispberry":               ItemData(77054, ItemClassification.filler),
    "Green Crispberry":             ItemData(77055, ItemClassification.filler),
    "Conch":                        ItemData(77050, ItemClassification.filler),
    "Yellow Crispberry":            ItemData(77056, ItemClassification.filler),
    "Yellow Winterberry":           ItemData(77064, ItemClassification.filler),
    "Red Prickleberry":             ItemData(77071, ItemClassification.filler),
    "Gold Prickleberry":            ItemData(77072, ItemClassification.filler),
    "Brown Berrynana":              ItemData(77059, ItemClassification.filler),
    "Pink Berrynana":               ItemData(77061, ItemClassification.filler),
    "Yellow Berrynana":             ItemData(77062, ItemClassification.filler),
    "Red Shroomberry":              ItemData(77076, ItemClassification.filler),
    "Blue Shroomberry":             ItemData(77077, ItemClassification.filler),
    "Yellow Shroomberry":           ItemData(77078, ItemClassification.filler),
    "Green Shroomberry":            ItemData(77079, ItemClassification.filler),
    "Purple Shroomberry":           ItemData(77080, ItemClassification.filler),
    "Egg":                          ItemData(77067, ItemClassification.filler),
    "Big Egg":                      ItemData(77073, ItemClassification.filler),
    "Cooked Bird":                  ItemData(77068, ItemClassification.filler),
    "Beehive":                      ItemData(77070, ItemClassification.filler),
    "Coconut Half":                 ItemData(77058, ItemClassification.filler),
    "Coconut":                      ItemData(77057, ItemClassification.filler),
    "Cursed Skull":                 ItemData(77031, ItemClassification.filler),
    "Blue Berrynana":               ItemData(77060, ItemClassification.filler),
    "Purple Kingberry":             ItemData(77093, ItemClassification.filler),
    "Yellow Kingberry":             ItemData(77094, ItemClassification.filler),
    "Green Kingberry":              ItemData(77095, ItemClassification.filler),
    "Black Clusterberry":           ItemData(77097, ItemClassification.filler),
    "Red Clusterberry":             ItemData(77098, ItemClassification.filler),
    "Yellow Clusterberry":          ItemData(77099, ItemClassification.filler),
    "Tick":                         ItemData(77121, ItemClassification.filler)

}

trap_table = {
    "Banana Peel Trap":           ItemData(76005, ItemClassification.trap),
    "Minor Poison Trap":          ItemData(76032, ItemClassification.trap),
    "Slip Trap":                  ItemData(76041, ItemClassification.trap),
    "Cactus Ball Trap":           ItemData(76039, ItemClassification.trap),
    "Scorpion":                   ItemData(77074, ItemClassification.trap),
    "Mandrake":                   ItemData(77081, ItemClassification.trap),
    "Spawn Bee Swarm":            ItemData(76027, ItemClassification.trap),
    "Destroy Held Item":          ItemData(76029, ItemClassification.trap),
    "Poison Trap":                ItemData(76033, ItemClassification.trap),
    "Nap Time Trap":              ItemData(76036, ItemClassification.trap),
    "Balloon Trap":               ItemData(76037, ItemClassification.trap),
    "Hungry Hungry Camper Trap":  ItemData(76038, ItemClassification.trap),
    "Freeze Trap":                ItemData(76040, ItemClassification.trap),
    "Cold Trap":                  ItemData(76048, ItemClassification.trap),
    "Hot Trap":                   ItemData(76049, ItemClassification.trap),
    "Yeet Trap":                  ItemData(76042, ItemClassification.trap),
    "Gust Trap":                  ItemData(76045, ItemClassification.trap),
    "Mandrake Trap":              ItemData(76046, ItemClassification.trap),
    "Fungal Infection Trap":      ItemData(76047, ItemClassification.trap),
    "Dynamite":                   ItemData(77052, ItemClassification.trap),
    "Swap Trap":                  ItemData(76030, ItemClassification.trap),
    "Deadly Poison Trap":         ItemData(76034, ItemClassification.trap),
    "Tornado Trap":               ItemData(76035, ItemClassification.trap),
    "Tumbleweed Trap":            ItemData(76043, ItemClassification.trap),
    "Zombie Horde Trap":          ItemData(76044, ItemClassification.trap),
    "Pokemon Trivia Trap":        ItemData(77087, ItemClassification.trap),
    "Items to Bombs":             ItemData(77088, ItemClassification.trap),
    "Instant Death Trap":         ItemData(76028, ItemClassification.trap),
    "Blackout Trap":              ItemData(77089, ItemClassification.trap),
    "Fear Trap":                  ItemData(77090, ItemClassification.trap),
    "Injury Trap":                ItemData(77091, ItemClassification.trap),
    "Scoutmaster Trap":           ItemData(77092, ItemClassification.trap),
    "Zoom Trap":                  ItemData(77051, ItemClassification.trap),
    "Screen Flip Trap":           ItemData(77101, ItemClassification.trap),
    "Drop Everything Trap":       ItemData(77102, ItemClassification.trap),
    "Pixel Trap":                 ItemData(77103, ItemClassification.trap),
    "Eruption Trap":              ItemData(77104, ItemClassification.trap),
    "Beetle Horde Trap":          ItemData(77105, ItemClassification.trap),
    "Custom Trivia Trap":         ItemData(77120, ItemClassification.trap),
}

item_table = {
    **progression_table,
    **useful_table,
    **filler_table,
    **trap_table,
}

lookup_id_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code
}

item_groups: typing.Dict[str, typing.List[str]] = {
    "Progression":      list(progression_table.keys()),
    "Useful":           list(useful_table.keys()),
    "Filler":           list(filler_table.keys()),
    "Traps":            list(trap_table.keys()),
}

try:
    from worlds.alttp import ALTTPWorld
    ALTTPWorld.pedestal_credit_texts.update({item_table[name]: f"and the {texts.pedestal}"
                                             for name, texts in LttPCreditsText.items()})
    ALTTPWorld.sickkid_credit_texts.update({item_table[name]: texts.sickkid for name, texts in LttPCreditsText.items()})
    ALTTPWorld.magicshop_credit_texts.update({item_table[name]: texts.magicshop for name, texts in LttPCreditsText.items()})
    ALTTPWorld.zora_credit_texts.update({item_table[name]: texts.zora for name, texts in LttPCreditsText.items()})
    ALTTPWorld.fluteboy_credit_texts.update({item_table[name]: texts.fluteboy for name, texts in LttPCreditsText.items()})
except ModuleNotFoundError:
    pass