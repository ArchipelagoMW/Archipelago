import typing

from BaseClasses import Tutorial, Group
from worlds.AutoWorld import WebWorld, World
from worlds.clair_obscur.Items import create_item_name_to_ap_id, ClairObscurItem, get_classification
from worlds.clair_obscur.Locations import create_location_name_to_ap_id
from worlds.clair_obscur.Options import OPTIONS_GROUP, ClairObscurOptions


class WebClairObscur(WebWorld):
    """
    Webhost for Clair Obscur Expedition 33.
    """

    theme = "stone"

    setup = Tutorial(
        "Multiworld Setup Guide",
        "Setup guide for Clair Obscur Expedition 33.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Démorck"]
    )

    tutorials = [setup]
    option_groups = OPTIONS_GROUP

class ClairObscurSettings(Group):
    """
    No idea
    """

class ClairObscur(World):
    game = "Clair Obscur Expedition 33"
    web = WebClairObscur()
    topology_present = False

    options_dataclass = ClairObscurOptions
    options = ClairObscurOptions

    item_name_to_id = create_item_name_to_ap_id()
    location_name_to_id = create_location_name_to_ap_id()

    required_client_version = (0, 4, 6)


    settings: typing.ClassVar[ClairObscurSettings]


    def create_item(self, name: str) -> ClairObscurItem:
        return self.create_item_by_id(self.item_name_to_id[name])


    def create_item_by_id(self, ap_id: int) -> ClairObscurItem:
        return ClairObscurItem(
            self.item_id_to_name[ap_id],
            get_classification(ap_id),
            ap_id,
            self.player
        )