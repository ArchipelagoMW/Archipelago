from test.bases import WorldTestBase
from Options import ItemLinks
from . import linkedTestHK


class test_grubcount_limited(linkedTestHK, WorldTestBase):
    options = {
        "RandomizeGrubs": True,
        "GrubHuntGoal": 20,
        "Goal": "any",
    }
    item_link_group = [{
        "name": "ItemLinkTest",
        "item_pool": ["Grub"],
        "link_replacement": True,
        "replacement_item": "Grub",
    }]
    expected_grubs = 20


class test_grubcount_default(linkedTestHK, WorldTestBase):
    options = {
        "RandomizeGrubs": True,
        "Goal": "any",
    }
    item_link_group = [{
        "name": "ItemLinkTest",
        "item_pool": ["Grub"],
        "link_replacement": True,
        "replacement_item": "Grub",
    }]
    expected_grubs = 46


class test_grubcount_all_unlinked(linkedTestHK, WorldTestBase):
    options = {
        "RandomizeGrubs": True,
        "GrubHuntGoal": "all",
        "Goal": "any",
    }
    item_link_group = []
    expected_grubs = 46


class test_grubcount_all_linked(linkedTestHK, WorldTestBase):
    options = {
        "RandomizeGrubs": True,
        "GrubHuntGoal": "all",
        "Goal": "any",
    }
    item_link_group = [{
        "name": "ItemLinkTest",
        "item_pool": ["Grub"],
        "link_replacement": True,
        "replacement_item": "Grub",
    }]
    expected_grubs = 46 + 23


class test_replacement_only(linkedTestHK, WorldTestBase):
    options = {
        "RandomizeGrubs": True,
        "GrubHuntGoal": "all",
        "Goal": "any",
    }
    expected_grubs = 46 + 18  # the count of grubs + skills removed from item links

    def setup_item_links(self, args):
        setattr(args, "item_links",
                {
                    1: ItemLinks.from_any([{
                        "name": "ItemLinkTest",
                        "item_pool": ["Skills"],
                        "link_replacement": True,
                        "replacement_item": "Grub",
                    }]),
                    2: ItemLinks.from_any([{
                        "name": "ItemLinkTest",
                        "item_pool": ["Skills"],
                        "link_replacement": True,
                        "replacement_item": "Grub",
                    }])
                })
        return args


class test_replacement_only_unlinked(linkedTestHK, WorldTestBase):
    options = {
        "RandomizeGrubs": True,
        "GrubHuntGoal": "all",
        "Goal": "any",
    }
    expected_grubs = 46 + 9  # Player1s replacement Grubs

    def setup_item_links(self, args):
        setattr(args, "item_links",
                {
                    1: ItemLinks.from_any([{
                        "name": "ItemLinkTest",
                        "item_pool": ["Skills"],
                        "link_replacement": False,
                        "replacement_item": "Grub",
                    }]),
                    2: ItemLinks.from_any([{
                        "name": "ItemLinkTest",
                        "item_pool": ["Skills"],
                        "link_replacement": False,
                        "replacement_item": "Grub",
                    }])
                })
        return args


class test_ignore_others(linkedTestHK, WorldTestBase):
    options = {
        "RandomizeGrubs": True,
        "GrubHuntGoal": "all",
        "Goal": "any",
    }
    # player2 has more than 46 grubs but they are unlinked so player1s grubs are vanilla
    expected_grubs = 46

    def setup_item_links(self, args):
        setattr(args, "item_links",
                {
                    1: ItemLinks.from_any([{
                        "name": "ItemLinkTest",
                        "item_pool": ["Skills"],
                        "link_replacement": False,
                        "replacement_item": "One_Geo",
                    }]),
                    2: ItemLinks.from_any([{
                        "name": "ItemLinkTest",
                        "item_pool": ["Skills"],
                        "link_replacement": False,
                        "replacement_item": "Grub",
                    }])
                })
        return args


class test_replacement_only_linked(linkedTestHK, WorldTestBase):
    options = {
        "RandomizeGrubs": True,
        "GrubHuntGoal": "all",
        "Goal": "any",
    }
    expected_grubs = 46 + 9  # Player2s linkreplacement grubs

    def setup_item_links(self, args):
        setattr(args, "item_links",
                {
                    1: ItemLinks.from_any([{
                        "name": "ItemLinkTest",
                        "item_pool": ["Skills"],
                        "link_replacement": True,
                        "replacement_item": "One_Geo",
                    }]),
                    2: ItemLinks.from_any([{
                        "name": "ItemLinkTest",
                        "item_pool": ["Skills"],
                        "link_replacement": True,
                        "replacement_item": "Grub",
                    }])
                })
        return args
