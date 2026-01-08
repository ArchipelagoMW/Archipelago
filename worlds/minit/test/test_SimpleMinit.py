from .bases import MinitTestBase, selectSeedMinit

can_open_chest = [
    "Dog House - Land is Great Coin",
    "Dog House - Hidden Snake Coin",
    "Dog House - Waterfall Coin",
    "Dog House - Treasure Island Coin",
    "Desert RV - Broken Truck",
    ]

sword_only = [
    "Dog House - House Pot Coin",
    "Dog House - Sewer Island Coin",
    "Dog House - Sewer Coin",
    "Desert RV - Temple Coin",
    "Desert RV - Truck Supplies Coin",
    "Desert RV - Quicksand Coin",
    "Desert RV - Dumpster",
    "Hotel Room - Shrub Arena Coin",
    "Hotel Room - Miner's Chest Coin",
    "Hotel Room - Hotel Backroom Coin",
    "Factory Main - Drill Coin",
    ]

Darkrooms1 = [
    "Desert RV - Fire Bat Coin",
    "Factory Main - ItemMegaSword",
    ]

Darkrooms2 = [
    "Dog House - Hidden Snake Coin",
    "Dog House - Bull Heart",
    "Desert RV - ItemTurboInk",
    "Desert RV - Temple Coin",
    "Desert RV - Quicksand Coin",
    "Desert RV - Octopus Tentacle",
    "Hotel Room - ItemGrinder",
    ]

Darkrooms3 = [
    "Dog House - Sewer Island Coin",
    "Dog House - Sewer Coin",
    "Dog House - Sewer Tentacle",
    "Desert RV - Temple Heart",
    "Hotel Room - Miner's Chest Coin",
    "Underground Tent - ItemTrophy",
    ]

ER_Darkrooms1 = [
    "Hotel Room - ItemGrinder",
    "Factory Main - ItemMegaSword",
    ]

ER_Darkrooms2 = [
    "Dog House - Sewer Coin",
    "Dog House - Hidden Snake Coin",
    "Desert RV - Fire Bat Coin",
    "Desert RV - ItemTurboInk",
    "Desert RV - Quicksand Coin",
    ]

ER_Darkrooms3 = [
    "Dog House - Sewer Tentacle",
    "Desert RV - Temple Heart",
    "Desert RV - Octopus Tentacle",
    "Hotel Room - Miner's Chest Coin",
    ]

# pure_darkrooms = [
#     "Dog House - Sewer Island Coin",
#     "Dog House - Sewer Coin",
#     "Dog House - Hidden Snake Coin",
#     "Dog House - Sewer Tentacle",
#     "Desert RV - ItemTurboInk",
#     "Desert RV - Temple Coin",
#     "Desert RV - Fire Bat Coin",
#     "Desert RV - Quicksand Coin",
#     "Desert RV - Temple Heart",
#     "Desert RV - Octopus Tentacle",
#     "Hotel Room - ItemGrinder",
#     "Hotel Room - Miner's Chest Coin",
#     "Factory Main - ItemMegaSword",
#     ]

# simple_darkrooms = [
#     "Dog House - Sewer Island Coin",
#     "Dog House - Sewer Coin",
#     "Dog House - Hidden Snake Coin",
#     "Dog House - Sewer Tentacle",
#     "Desert RV - ItemTurboInk",
#     "Desert RV - Temple Coin",
#     "Desert RV - Fire Bat Coin",
#     "Desert RV - Quicksand Coin",
#     "Desert RV - Octopus Tentacle",
#     "Hotel Room - ItemGrinder",
#     "Hotel Room - Miner's Chest Coin",
#     "Factory Main - ItemMegaSword",
#     ]


class TestChestAccess(MinitTestBase):

    def test_minit_weapon_chests1(self):
        """Test locations that require any weapon"""
        locations = can_open_chest
        items = [
            ["ItemWateringCan"],
            ["ItemBrokenSword"],
            ["ItemSword"],
            ["ItemMegaSword"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_minit_weapon_chests2(self):
        """Test locations that require any sword"""
        locations = sword_only
        items = [
            ["ItemBrokenSword"],
            ["ItemSword"],
            ["ItemMegaSword"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_minit_weapon_chests3(self):
        """Test locations that require only wateringcan"""
        locations = [
            "Desert RV - Fire Bat Coin",
            "Dog House - Dolphin Heart",
            "Dog House - Plant Heart",
            ]
        items = [
            ["ItemWateringCan"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    # def test_minit_weapon_chests4(self):
    #   """Test locations that do not require a held item"""
    #   locations = ["Hotel Room - Queue","Hotel Room - Inside Truck"]
    #   items = [["ItemWateringCan"]]
    #   self.assertAccessIndependency(locations, items, only_check_listed=True)


class TestDarkroom0(MinitTestBase):
    options = {
        "darkrooms": 0,
    }

    def test_minit_flashlight(self):
        """Test locations that require Flashlight"""
        locations = []
        locations + Darkrooms1
        locations + Darkrooms2
        locations + Darkrooms3
        items = [
            ["ItemFlashLight"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)


class TestDarkroom1(MinitTestBase):
    options = {
        "darkrooms": 1,
    }

    def test_minit_flashlight(self):
        """Test locations that require Flashlight"""
        locations = []
        locations + Darkrooms2
        locations + Darkrooms3
        items = [
            ["ItemFlashLight"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_minit_darkrooms(self):
        """Test locations that do not require Flashlight"""
        locations = []
        locations + Darkrooms1
        items = [
            ["ItemFlashLight"],
            ]
        self.assertAccessWithout(locations, items)


class TestDarkroom2(MinitTestBase):
    options = {
        "darkrooms": 2,
    }

    def test_minit_flashlight(self):
        """Test locations that require Flashlight"""
        locations = []
        locations + Darkrooms3
        items = [
            ["ItemFlashLight"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_minit_darkrooms(self):
        """Test locations that do not require Flashlight"""
        locations = []
        locations + Darkrooms1
        locations + Darkrooms2
        items = [
            ["ItemFlashLight"],
            ]
        self.assertAccessWithout(locations, items)


class TestDarkroom3(MinitTestBase):
    options = {
        "darkrooms": 3,
    }

    def test_minit_darkrooms(self):
        """Test locations that do not require Flashlight"""
        locations = []
        locations + Darkrooms1
        locations + Darkrooms2
        locations + Darkrooms3
        items = [
            ["ItemFlashLight"],
            ]
        self.assertAccessWithout(locations, items)


class TestToiletGoal(MinitTestBase):
    options = {
        "chosen_goal": 1,
    }


class TestAnyGoal(MinitTestBase):
    options = {
        "chosen_goal": 2,
    }


class TestER(MinitTestBase):
    options = {
        "er_option": 1,
    }


class TestERDarkroom0(MinitTestBase):
    options = {
        "darkrooms": 0,
    }

    def test_minit_flashlight(self):
        """Test locations that require Flashlight"""
        locations = []
        locations + ER_Darkrooms1
        locations + ER_Darkrooms2
        locations + ER_Darkrooms3
        items = [
            ["ItemFlashLight"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)


class TestERDarkroom1(MinitTestBase):
    options = {
        "darkrooms": 1,
    }

    def test_minit_flashlight(self):
        """Test locations that require Flashlight"""
        locations = []
        locations + ER_Darkrooms2
        locations + ER_Darkrooms3
        items = [
            ["ItemFlashLight"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_minit_darkrooms(self):
        """Test locations that do not require Flashlight"""
        locations = []
        locations + Darkrooms1
        items = [
            ["ItemFlashLight"],
            ]
        self.assertAccessWithout(locations, items)


class TestERDarkroom2(MinitTestBase):
    options = {
        "darkrooms": 2,
    }

    def test_minit_flashlight(self):
        """Test locations that require Flashlight"""
        locations = []
        locations + ER_Darkrooms3
        items = [
            ["ItemFlashLight"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_minit_darkrooms(self):
        """Test locations that do not require Flashlight"""
        locations = []
        locations + Darkrooms1
        locations + Darkrooms2
        items = [
            ["ItemFlashLight"],
            ]
        self.assertAccessWithout(locations, items)


class TestERDarkroom3(MinitTestBase):
    options = {
        "darkrooms": 3,
    }

    def test_minit_darkrooms(self):
        """Test locations that do not require Flashlight"""
        locations = []
        locations + Darkrooms1
        locations + Darkrooms2
        locations + Darkrooms3
        items = [
            ["ItemFlashLight"],
            ]
        self.assertAccessWithout(locations, items)


class TestERSeed(selectSeedMinit):
    options = {
        "er_option": 1,
    }
    seed = 63716117118555143701


class TestProgressiveChestAccess(MinitTestBase):
    options = {
        "progressive_sword": 0,
    }

    def test_minit_weapon_chests1(self):
        """Test locations that require any weapon"""
        locations = can_open_chest
        items = [
            ["ItemWateringCan"],
            ["Progressive Sword"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_minit_weapon_chests2(self):
        """Test locations that require any sword"""
        locations = sword_only
        items = [
            ["Progressive Sword"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)


class TestRevProgressiveChestAccess(MinitTestBase):
    options = {
        "progressive_sword": 1,
    }

    def test_minit_weapon_chests1(self):
        """Test locations that require any weapon"""
        locations = can_open_chest
        items = [
            ["ItemWateringCan"],
            ["Reverse Progressive Sword"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)

    def test_minit_weapon_chests2(self):
        """Test locations that require any sword"""
        locations = sword_only
        items = [
            ["Reverse Progressive Sword"],
            ]
        self.assertAccessDependency(locations, items, only_check_listed=True)


# class TestStartInventoryFromPool1(MinitTestBase):
#     options = {
#         "start_inventory_from_pool": {"ItemTrophy": 1},
#     }

#     def test_item_removed(self):
#         itempool = [item.name for item in self.multiworld.get_items()]
#         assert "ItemTrophy" not in itempool
#         assert "ItemGrinder" in itempool

#         ct = 0
#         for item in itempool:
#             if item == "HeartPiece":
#                 ct += 1
#         assert ct == 7


# class TestStartInventoryFromPool2(MinitTestBase):
#     options = {
#         "start_inventory_from_pool": {"ItemTrophy": 1,
#                                       "ItemTurboInk": 1},
#     }

#     def test_item_removed(self):
#         itempool = [item.name for item in self.multiworld.get_items()]
#         assert "ItemTrophy" not in itempool
#         assert "ItemTurboInk" not in itempool
#         assert "ItemGrinder" in itempool

#         ct = 0
#         for item in itempool:
#             if item == "HeartPiece":
#                 ct += 1
#         assert ct == 8


# class TestStartInventoryFromPool3(MinitTestBase):
#     options = {
#         "start_inventory_from_pool": {"ItemFlashLight": 1},
#     }

#     def test_item_removed(self):
#         itempool = [item.name for item in self.multiworld.get_items()]
#         assert "ItemFlashLight" not in itempool
#         assert "ItemGrinder" in itempool

#         ct = 0
#         for item in itempool:
#             if item == "HeartPiece":
#                 ct += 1
#         assert ct == 7


# class TestStartInventoryFromPool4(MinitTestBase):
#     options = {
#         "start_inventory": {"ItemFlashLight": 1},
#     }

#     def test_item_removed(self):
#         itempool = [item.name for item in self.multiworld.get_items()]
#         assert "ItemFlashLight" not in itempool
#         assert "ItemGrinder" in itempool

#         ct = 0
#         for item in itempool:
#             if item == "HeartPiece":
#                 ct += 1
#         assert ct == 7


class TestMinHP(MinitTestBase):
    options = {
        "min_hp": True,
    }

    def test_item_removed(self):
        itempool = [item.name for item in self.multiworld.get_items()]
        assert "HeartPiece" not in itempool
        assert "ItemGrinder" in itempool

        ct = 0
        for item in itempool:
            if item == "Coin":
                ct += 1
        assert ct == 25


class TestFullHP(MinitTestBase):
    options = {
        "min_hp": False,
    }

    def test_item_removed(self):
        itempool = [item.name for item in self.multiworld.get_items()]
        assert "HeartPiece" in itempool
        assert "ItemGrinder" in itempool

        ct = 0
        for item in itempool:
            if item == "HeartPiece":
                ct += 1
        assert ct == 6
        ct = 0
        for item in itempool:
            if item == "Coin":
                ct += 1
        assert ct == 19


class TestDamageBoosts(MinitTestBase):
    options = {
        "damage_boosts": True,
    }

    def test_hearts_progression(self):
        state = self.multiworld.get_all_state(False)
        assert "HeartPiece" in state.prog_items[1]
        # heartpiece


class TestDamageBoosts2(MinitTestBase):
    options = {
        "damage_boosts": False,
    }

    def test_hearts_not_progression(self):
        state = self.multiworld.get_all_state(False)
        assert "HeartPiece" not in state.prog_items[1]
        # heartpiece


class TestSeed1(selectSeedMinit):
    seed = 95400472555641845910


class TestSeed2(selectSeedMinit):
    seed = 20545238613336522738


class TestSeed3(selectSeedMinit):
    seed = 40237425953666301908

# 20481966185286985687
# 99382586412933725576
