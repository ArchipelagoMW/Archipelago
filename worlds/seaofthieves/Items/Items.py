import typing
from BaseClasses import Item
from .DefineItem import Define

class SOTItem(Item):
    game: str = "Sea of Thieves"




class Items:
    gold_50 = Define.Money.gold(50)
    gold_100 = Define.Money.gold(100)
    gold_500 = Define.Money.gold(500)
    dabloons_25 = Define.Money.dabloon(25)
    ancient_coins_10 = Define.Money.ancient_coin(10)

    kraken = Define.Trap.kraken()

    sail = Define.Item.Ship.sail()
    sail_inferno = Define.Item.Ship.sail_inferno()
    stove = Define.Item.Ship.stove()
    barrel_food = Define.Item.Ship.food_barrel()
    barrel_cannon = Define.Item.Ship.cannon_barrel()
    barrel_wood = Define.Item.Ship.wood_barrel()

    voyage_fortress = Define.Item.Voyage.fortress()
    voyages_gh = Define.Item.Voyage.gh()
    voyages_ma = Define.Item.Voyage.ma()
    voyages_oos = Define.Item.Voyage.oos()
    voyages_af = Define.Item.Voyage.af()
    voyages_rb = Define.Item.Voyage.rb()
    voyages_tt = Define.Item.Voyage.tt()
    voyage_of_destiny = Define.Item.Voyage.destiny()

    emissary_gh = Define.Item.Emissary.gh()
    emissary_ma = Define.Item.Emissary.ma()
    emissary_oos = Define.Item.Emissary.oos()
    emissary_af = Define.Item.Emissary.af()
    emissary_rb = Define.Item.Emissary.rb()

    seal_gh = Define.Item.Seal.gh()
    seal_ma = Define.Item.Seal.ma()
    seal_oos = Define.Item.Seal.oos()
    seal_af = Define.Item.Seal.af()
    seal_rb = Define.Item.Seal.rb()

    personal_weapons = Define.Item.Weapon.personal()
    ship_weapons = Define.Item.Weapon.ship()

    fishing_rod = Define.Item.Equipment.fishing_rod()
    shovel = Define.Item.Equipment.shovel()
    wallet = Define.Item.Equipment.wallet()

    pirate_legend = Define.Victory.pirate_legend()

    cat_as = Define.Shop.ancient_spire()
    cat_dt = Define.Shop.dagger_tooth()
    cat_gg = Define.Shop.galleons_grave()
    cat_mp = Define.Shop.morrows_peak()
    cat_p = Define.Shop.plunder()
    cat_s = Define.Shop.sanctuary()




