# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing

from BaseClasses import Item, ItemClassification


class MeritousLttPText(typing.NamedTuple):
    pedestal: typing.Optional[str]
    sickkid: typing.Optional[str]
    magicshop: typing.Optional[str]
    zora: typing.Optional[str]
    fluteboy: typing.Optional[str]


LttPCreditsText = {
    "Nothing": MeritousLttPText("lack of presence",
                                "Forgot to get you anything",
                                "Thanks for the shroom, sucker",
                                "Bucket o' Nothing for 9999.99",
                                "I can't hear anything"),
    "Reflect Shield upgrade": MeritousLttPText("Protective Aura",
                                               "Safe under the covers",
                                               "Cast a magic circle",
                                               "Psionic aura for sale",
                                               "This tune makes you feel safe"),
    "Circuit Charge upgrade": MeritousLttPText("Psionic Charge",
                                               "This kid's so ready now",
                                               "Expand your mind",
                                               "Psionic energy for sale",
                                               "Synthwave? From a flute?"),
    "Circuit Refill upgrade": MeritousLttPText("Psionic Cleanse",
                                               "All rested up",
                                               "Shrooms for mental floss",
                                               "Psionic refreshment for sale",
                                               "Peaceful little tune"),
    "Map": MeritousLttPText("Twisted Chart",
                            "Abstract artist kid",
                            "Shrooms for pictograms",
                            "Strange imagery for sale",
                            "Just follow the rhythm"),
    "Shield Boost": MeritousLttPText("Heavy Aura",
                                     "Blanket fort kid",
                                     "Shrooms for protection",
                                     "Bigger circles for sale",
                                     "Don't touch the music man"),
    "Crystal Efficiency": MeritousLttPText("Expensive Trinket",
                                           "Investment kid",
                                           "Make your own crystals",
                                           "Invest in someone's future",
                                           "A rich melody"),
    "Circuit Booster": MeritousLttPText("Mental Focus",
                                        "Far-reaching kid",
                                        "I can see through time",
                                        "Finglonger for sale",
                                        "Can you please keep it down"),
    "Metabolism": MeritousLttPText("Energy Drink",
                                   "Zoom-Zoom kid",
                                   "Shrooms for Zooms",
                                   "Speed for sale",
                                   "How does he play so fast"),
    "Dodge Enhancer": MeritousLttPText("Insignificant Dot",
                                       "Evasive kid",
                                       "Still at large",
                                       "Take the money and run",
                                       "Gonna rock and go"),
    "Ethereal Monocle": MeritousLttPText("Weird Glass",
                                         "He can see you coming",
                                         "Okay now I'm seeing things",
                                         "Precognition for sale",
                                         "Like deja vu all over again"),
    "Crystal Gatherer": MeritousLttPText("Attractive Aura",
                                         "Magnetic kid",
                                         "I swear it attracts money",
                                         "Big magnet for sale",
                                         "Works for tips"),
    "Portable Compass": MeritousLttPText("Way Forward",
                                         "Forward-thinking kid",
                                         "Shrooms for Life Advice",
                                         "Moving Needle for sale",
                                         "Sing a tale of adventure"),
    "PSI Key 1": MeritousLttPText("Familiar Artifact",
                                  "Messenger kid",
                                  "The Black Market",
                                  "I've got something good",
                                  "An otherworldly tune"),
    "PSI Key 2": MeritousLttPText("Familiar Artifact",
                                  "Messenger kid",
                                  "The Black Market",
                                  "I've got something good",
                                  "An otherworldly tune"),
    "PSI Key 3": MeritousLttPText("Familiar Artifact",
                                  "Messenger kid",
                                  "The Black Market",
                                  "I've got something good",
                                  "An otherworldly tune"),
    "Cursed Seal": MeritousLttPText("Psionic Anomaly",
                                    "What's this doing here",
                                    "What's this doing here",
                                    "What's this doing here",
                                    "What's this doing here"),
    "Agate Knife": MeritousLttPText("Psionic Anomaly",
                                    "What's this doing here",
                                    "What's this doing here",
                                    "What's this doing here",
                                    "What's this doing here"),
    "Evolution Trap": MeritousLttPText("Awful Curse",
                                       "Dennis the Menace",
                                       "I can make it harder for 'em",
                                       "Pranks for sale",
                                       "This tune sucks, I'm angry now"),
    "Crystals x500": MeritousLttPText("Pile of Rocks",
                                      "Shiny collector kid",
                                      "A backroom exchange",
                                      "Currency conversion here",
                                      "Quarter-full tip jar"),
    "Crystals x1000": MeritousLttPText("Pile of Rocks",
                                       "Shiny collector kid",
                                       "A backroom exchange",
                                       "Currency conversion here",
                                       "Half-full tip jar"),
    "Crystals x2000": MeritousLttPText("Pile of Rocks",
                                       "Shiny collector kid",
                                       "A backroom exchange",
                                       "Currency conversion here",
                                       "This was a real good gig"),
    "Extra Life": MeritousLttPText("Lifesaver",
                                   "Sick kid feels alive again",
                                   "A life-saving concoction",
                                   "Second chance for sale",
                                   "A life-saving melody")
}


class MeritousItem(Item):
    game: str = "Meritous"
    type: str

    def __init__(self, name, advancement, code, player):
        super(MeritousItem, self).__init__(name,
                                           ItemClassification.progression if advancement else ItemClassification.filler,
                                           code, player)
        if code is None:
            self.type = "Event"
        elif "Trap" in name:
            self.type = "Trap"
            self.classification = ItemClassification.trap
        elif "PSI Key" in name:
            self.type = "PSI Key"
        elif "upgrade" in name:
            self.type = "Enhancement"
        elif "Crystals x" in name:
            self.type = "Crystals"
        elif name == "Nothing":
            self.type = "Nothing"
        elif name == "Cursed Seal" or name == "Agate Knife":
            self.type = name
        elif name == "Extra Life":
            self.type = "Other"
        elif self.advancement:
            self.type = "Important Artifact"
        else:
            self.type = "Artifact"
            self.classification = ItemClassification.useful


offset = 593_000

item_table = {
    "Nothing": offset + 0,
    "Reflect Shield upgrade": offset + 1,
    "Circuit Charge upgrade": offset + 2,
    "Circuit Refill upgrade": offset + 3,
    "Map": offset + 4,
    "Shield Boost": offset + 5,
    "Crystal Efficiency": offset + 6,
    "Circuit Booster": offset + 7,
    "Metabolism": offset + 8,
    "Dodge Enhancer": offset + 9,
    "Ethereal Monocle": offset + 10,
    "Crystal Gatherer": offset + 11,
    "Portable Compass": offset + 12,
    "PSI Key 1": offset + 13,
    "PSI Key 2": offset + 14,
    "PSI Key 3": offset + 15,
    "Cursed Seal": offset + 16,
    "Agate Knife": offset + 17,
    "Evolution Trap": offset + 18,
    "Crystals x500": offset + 19,
    "Crystals x1000": offset + 20,
    "Crystals x2000": offset + 21,
    "Extra Life": offset + 22
}

item_groups = {
    "PSI Keys": [f"PSI Key {x}" for x in range(1, 4)],
    "Upgrades": ["Reflect Shield upgrade", "Circuit Charge upgrade", "Circuit Refill upgrade"],
    "Artifacts": ["Map", "Shield Boost", "Crystal Efficiency", "Circuit Booster",
                  "Metabolism", "Dodge Enhancer", "Ethereal Monocle", "Crystal Gatherer",
                  "Portable Compass"],
    "Important Artifacts": ["Shield Boost", "Circuit Booster", "Metabolism", "Dodge Enhancer"],
    "Crystals": ["Crystals x500", "Crystals x1000", "Crystals x2000"]
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
