from . import linkedTestHK, WorldTestBase
from Options import ItemLinks


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
    expected_grubs = 46 + 9  # the count of grubs + half skills removed from item links

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