# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing

from BaseClasses import Item, ItemClassification


class BumpStikLttPText(typing.NamedTuple):
    pedestal: typing.Optional[str]
    sickkid: typing.Optional[str]
    magicshop: typing.Optional[str]
    zora: typing.Optional[str]
    fluteboy: typing.Optional[str]


LttPCreditsText = {

}


class BumpStikItem(Item):
    game = "Bumper Stickers"

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
            self.type = "Board Size"
            self.classification = ItemClassification.progression
        elif "Booster" in name:
            self.type = "Booster"
            self.classification = ItemClassification.progression
        else:
            self.type = "Other"

        if name in LttPCreditsText:
            lttp = LttPCreditsText[name]
            self.pedestal_credit_text = f"and the {lttp.pedestal}"
            self.sickkid_credit_text = lttp.sickkid
            self.magicshop_credit_text = lttp.magicshop
            self.zora_credit_text = lttp.zora
            self.fluteboy_credit_text = lttp.fluteboy


# TODO: pick an offset
offset = 0

item_table = {
    "Board Width": offset + 0,
    "Board Height": offset + 1,
    "Starting Colors Up": offset + 2,
    "Maximum Colors Up": offset + 3,
    "Starting Paint Can": offset + 4,
    "Booster Bumper": offset + 5,
    "Hazard Bumper": offset + 6
}

item_groups = {
    "Board Size": ["Board Width", "Board Height"],
    "Color": ["Starting Colors Up", "Maximum Colors Up"]
}
