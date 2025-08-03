from typing import Dict

from .InternalLocationNames import InternalLocationName, ids_by_py_name

class LocationName(InternalLocationName):
    Alhafra_32_coins = "Alhafra - Outside Mayor's House East Box"
    Alhafran_Cave_Power_Bread = "Alhafra - Jail - Jar"
    Garoh_Nut = "Garoh - North-West Ledge - Barrel"
    Idejima_Shamans_Rod = "Felix - Shaman's Rod"
    Idejima_Mind_Read = "Sheba - Mind Read"
    Idejima_Whirlwind = "Sheba - Whirlwind"
    Idejima_Growth = "Felix - Growth"
    Contigo_Carry_Stone = "Mia - Carry Stone"
    Contigo_Lifting_Gem = "Ivan - Lifting Gem"
    Contigo_Orb_of_Force = "Garet - Orb of Force"
    Contigo_Catch_Beads = "Isaac - Catch Beads"
    Kibombo_Douse_Drop = "Piers - Douse Drop"
    Kibombo_Frost_Jewel = "Piers - Frost Jewel"
    Contigo_Isaac = "Contigo - Recruit Isaac"
    Contigo_Garet = "Contigo - Recruit Garet"
    Contigo_Ivan = "Contigo - Recruit Ivan"
    Contigo_Mia = "Contigo - Recruit Mia"
    Idejima_Jenna = "Idejima - Recruit Jenna"
    Idejima_Sheba = "Idejima - Recruit Sheba"
    Kibombo_Piers = "Kibombo - Recruit Piers"
    

    Flint = "4th Party Member - Venus Djinni Flint"
    Granite = "5th Party Member - Venus Djinni Granite"
    Quartz = "6th Party Member - Venus Djinni Quartz"
    Vine = "7th Party Member - Venus Djinni Vine"
    Sap = "7th Party Member - Venus Djinni Sap"
    Ground = "8th Party Member - Venus Djinni Ground"
    Bane = "Treasure Isle - Venus Djinni Bane"
    Echo = "South of Daila - Venus Djinni Echo"
    Iron = "West of Madra - Venus Djinni Iron"
    Steel = "Gabomba Statue - Venus Djinni Steel"
    Mud = "Gabomba Catacombs - Venus Djinni Mud"
    Flower = "Taopa Swamp - Venus Djinni Flower"
    Meld = "Islet Cave - Venus Djinni Meld"
    Petra = "Northeast Of Shaman Village - Venus Djinni Petra"
    Salt = "Contigo - Venus Djinni Salt"
    Geode = "Atteka Inlet - Venus Djinni Geode"
    Mold = "Prox - Venus Djinni Mold"
    Crystal = "Yampi Desert Cave - Venus Djinni Crystal"
    

    Fizz = "5th Party Member - Mercury Djinni Fizz"
    Sleet = "6th Party Member - Mercury Djinni Sleet"
    Mist = "6th Party Member - Mercury Djinni Mist"
    Spritz = "7th Party Member - Mercury Djinni Spritz"
    Hail = "7th Party Member - Mercury Djinni Hail"
    Tonic = "8th Party Member - Mercury Djinni Tonic"
    Dew = "Prox - Mercury Djinni Dew"
    Fog = "Kandorean Temple - Mercury Djinni Fog"
    Sour = "Northeast of Mikasalla - Mercury Djinni Sour"
    Spring = "3rd Party Member - Mercury Djinni Spring"
    Shade = "3rd Party Member - Mercury Djinni Shade"
    Chill = "Southwest of Naribwe - Mercury Djinni Chill"
    Steam = "Aqua Rock - Mercury Djinni Steam"
    Rime = "Ancient Lemuria - Mercury Djinni Rime"
    Gel = "Kalt Island - Mercury Djinni Gel"
    Eddy = "Shaman Village Cave - Mercury Djinni Eddy"
    Balm = "Mars Lighthouse - Mercury Djinni Balm"
    Serac = "Islet Cave - Mercury Djinni Serac"
    

    Forge = "4th Party Member - Mars Djinni Forge"
    Fever = "5th Party Member - Mars Djinni Fever"
    Corona = "6th Party Member - Mars Djinni Corona"
    Scorch = "7th Party Member - Mars Djinni Scorch"
    Ember = "8th Party Member - Mars Djinni Ember"
    Flash = "8th Party Member - Mars Djinni Flash"
    Torch = "Magma Rock - Mars Djinni Torch"
    Cannon = "Dehkan Plateau - Mars Djinni Cannon"
    Spark = "Mikasalla - Mars Djinni Spark"
    Kindle = "Gondowan Cliffs - Mars Djinni Kindle"
    Char = "Madra - Mars Djinni Char"
    Coal = "Izumo - Mars Djinni Coal"
    Reflux = "Tundaria Tower - Mars Djinni Reflux"
    Core = "West of Contigo - Mars Djinni Core"
    Tinder = "Hesperia Settlement - Mars Djinni Tinder"
    Shine = "Contigo - Mars Djinni Shine"
    Fury = "Magma Rock - Mars Djinni Fury"
    Fugue = "Mars Lighthouse - Mars Djinni Fugue"
    

    Gust = "4th Party Member - Jupiter Djinni Gust"
    Breeze = "5th Party Member - Jupiter Djinni Breeze"
    Zephyr = "6th Party Member - Jupiter Djinni Zephyr"
    Smog = "7th Party Member - Jupiter Djinni Smog"
    Kite = "8th Party Member - Jupiter Djinni Kite"
    Squall = "8th Party Member - Jupiter Djinni Squall"
    Luff = "SW Atteka Islet - Jupiter Djinni Luff"
    Breath = "Shrine of the Sea God - Jupiter Djinni Breath"
    Blitz = "Yampi Desert - Jupiter Djinni Blitz"
    Ether = "Garoh - Jupiter Djinni Ether"
    Waft = "Kibombo Mountains - Jupiter Djinni Waft"
    Haze = "Apojii Islands - Jupiter Djinni Haze"
    Wheeze = "Southwest of Tundaria Tower - Jupiter Djinni Wheeze"
    Aroma = "Shaman Village - Jupiter Djinni Aroma"
    Whorl = "Jupiter Lighthouse - Jupiter Djinni Whorl"
    Gasp = "Shaman Village - Trial Road Side Path - Jupiter Djinni Gasp"
    Lull = "Loho - Jupiter Djinni Lull"
    Gale = "Treasure Isle - Jupiter Djinni Gale"

ids_by_loc_name: Dict[str, int] = {
    getattr(LocationName, key): value
    for key, value in ids_by_py_name.items()
}

loc_names_by_id: Dict[int, str] = {
    value: key for key, value in ids_by_loc_name.items()
}

option_name_to_goal_name = {
    "Chestbeaters": LocationName.Kandorean_Temple_Chestbeaters,
    "King Scorpion": LocationName.Yampi_Desert_King_Scorpion,
    "Briggs": LocationName.Alhafra_Briggs,
    "Aqua Hydra": LocationName.Lemurian_Ship_Aqua_Hydra,
    "Poseidon": LocationName.Sea_of_Time_Poseidon,
    "Serpent": LocationName.Gaia_Rock_Serpent,
    "Avimander": LocationName.Champa_Avimander,
    "Moapa": LocationName.Shaman_Village_Moapa,
    "Reunion": LocationName.Contigo_Reunion,
    "Flame Dragons": LocationName.Mars_Lighthouse_Flame_Dragons,
    "Doom Dragon": LocationName.Mars_Lighthouse_Doom_Dragon,
    "Star Magician": LocationName.Treasure_Isle_Star_Magician,
    "Sentinel": LocationName.Islet_Cave_Sentinel,
    "Valukar": LocationName.Yampi_Desert_Cave_Valukar,
    "Dullahan": LocationName.Anemos_Inner_Sanctum_Dullahan,
}