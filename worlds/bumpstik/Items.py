# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing

from BaseClasses import Item, ItemClassification
from worlds.alttp import ALTTPWorld


class BumpStikLttPText(typing.NamedTuple):
    pedestal: typing.Optional[str]
    sickkid: typing.Optional[str]
    magicshop: typing.Optional[str]
    zora: typing.Optional[str]
    fluteboy: typing.Optional[str]


LttPCreditsText = {
    "Board Width": BumpStikLttPText("widening",
                                    "Bumper Kid embiggens options",
                                    "Try this shroom for size",
                                    "Extension for sale",
                                    "Next one's a long one"),
    "Board Height": BumpStikLttPText("lengthening",
                                     "Bumper Kid embiggens options",
                                     "Try this shroom for size",
                                     "Extension for sale",
                                     "Telling a tall tale"),
    "Starting Colors Up": BumpStikLttPText("tiny prism",
                                           "Crayola kid colors again",
                                           "The colors Duke! The colors",
                                           "Colorless dot for sale",
                                           "Tasteless language ahead"),
    "Maximum Colors Up": BumpStikLttPText("large prism",
                                          "Crayola kid colors again",
                                          "The colors Duke! The colors",
                                          "Colorful dot for sale",
                                          "Colorful language ahead"),
    "Starting Paint Can": BumpStikLttPText("paint bucket",
                                           "Artsy kid paints again",
                                           "Your rainbow destiny",
                                           "Rainbow for sale",
                                           "Let me paint a picture"),
    "Booster Bumper": BumpStikLttPText("multiplier",
                                       "Math kid multiplies again",
                                       "Growing shrooms",
                                       "Investment opportunity",
                                       "In harmony with themself"),
    "Hazard Bumper": BumpStikLttPText("dull stone",
                                      "...I got better",
                                      "Mischief Maker",
                                      "Whoops for sale",
                                      "Stuck in a moment"),
    "Treasure Bumper": BumpStikLttPText("odd treasure box",
                                        "Interdimensional treasure",
                                        "Shrooms for ???",
                                        "Who knows what this is",
                                        "No hinges no key no lid")
}


class BumpStikItem(Item):
    game = "Bumper Stickers"
    type: str

    def __init__(self, name, classification, code, player):
        super(BumpStikItem, self).__init__(
            name, classification, code, player)

        if code is None:
            self.type = "Event"
        elif "Hazard" in name:
            self.type = "Trap"
            self.classification = ItemClassification.trap
        elif "Board" in name:
            self.type = "Board Size"
            self.classification = ItemClassification.progression
        elif "Color" in name:
            self.type = "Color"
            self.classification = ItemClassification.progression
        elif "Booster" in name:
            self.type = "Booster"
            self.classification = ItemClassification.progression
        else:
            self.type = "Other"


offset = 595_000

item_table = {
    "Board Width": offset + 0,
    "Board Height": offset + 1,
    "Starting Colors Up": offset + 2,
    "Maximum Colors Up": offset + 3,
    "Starting Paint Can": offset + 4,
    "Booster Bumper": offset + 5,
    "Hazard Bumper": offset + 6,
    "Treasure Bumper": offset + 7
}

item_groups = {
    "Board Size": ["Board Width", "Board Height"],
    "Color": ["Starting Colors Up", "Maximum Colors Up"]
}

ALTTPWorld.pedestal_credit_texts.update({item_table[name]: f"and the {texts.pedestal}"
                                         for name, texts in LttPCreditsText.items()})
ALTTPWorld.sickkid_credit_texts.update({item_table[name]: texts.sickkid for name, texts in LttPCreditsText.items()})
ALTTPWorld.magicshop_credit_texts.update({item_table[name]: texts.magicshop for name, texts in LttPCreditsText.items()})
ALTTPWorld.zora_credit_texts.update({item_table[name]: texts.zora for name, texts in LttPCreditsText.items()})
ALTTPWorld.fluteboy_credit_texts.update({item_table[name]: texts.fluteboy for name, texts in LttPCreditsText.items()})
