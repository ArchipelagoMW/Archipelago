from .bases import NothingTestBase

#min settings 
options = {
        "goal": 1800,
        "shop_upgrades": False,
        "shop_colors": False,
        "shop_music": False,
        "shop_sounds": False,
        "gift_coins": False,
        "milestone_interval": 1800,
        "timecap_interval": 1800,
        "Starting_coin_count": 0,
    }
#starting coins
options = {
        "goal": 1800,
        "shop_upgrades": True,
        "shop_colors": True,
        "shop_music": True,
        "shop_sounds": True,
        "gift_coins": False,
        "milestone_interval": 1,
        "timecap_interval": 1,
        "Starting_coin_count": 80,
    }
#no upgrades
options = {
        "goal": 1800,
        "shop_upgrades": False,
        "shop_colors": True,
        "shop_music": True,
        "shop_sounds": True,
        "gift_coins": False,
        "milestone_interval": 1,
        "timecap_interval": 1,
        "Starting_coin_count": 0,
    }
#no milestones
options = {
        "goal": 1800,
        "shop_upgrades": True,
        "shop_colors": True,
        "shop_music": True,
        "shop_sounds": True,
        "gift_coins": False,
        "milestone_interval": 3600,
        "timecap_interval": 3600,
        "Starting_coin_count": 0,
    }

#test for each shop
#test for digits accesiblility with gift coins
#test timecap int greater than milestone int

class TestMaxSettingsLogic(NothingTestBase):

    options = {
        "goal": 86400,
        "shop_upgrades": True,
        "shop_colors": True,
        "shop_music": True,
        "shop_sounds": True,
        "gift_coins": False,
        "milestone_interval": 1,
        "timecap_interval": 1,
        "Starting_coin_count": 0,
    }