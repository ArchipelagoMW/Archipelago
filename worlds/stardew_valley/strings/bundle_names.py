class CCRoom:
    pantry = "Pantry"
    crafts_room = "Crafts Room"
    fish_tank = "Fish Tank"
    bulletin_board = "Bulletin Board"
    vault = "Vault"
    boiler_room = "Boiler Room"
    abandoned_joja_mart = "Abandoned Joja Mart"
    raccoon_requests = "Raccoon Requests"


all_cc_bundle_names = []


def cc_bundle(name: str) -> str:
    all_cc_bundle_names.append(name)
    return name


class BundleName:
    spring_foraging = cc_bundle("Spring Foraging Bundle")
    summer_foraging = cc_bundle("Summer Foraging Bundle")
    fall_foraging = cc_bundle("Fall Foraging Bundle")
    winter_foraging = cc_bundle("Winter Foraging Bundle")
    construction = cc_bundle("Construction Bundle")
    exotic_foraging = cc_bundle("Exotic Foraging Bundle")
    beach_foraging = cc_bundle("Beach Foraging Bundle")
    mines_foraging = cc_bundle("Mines Foraging Bundle")
    desert_foraging = cc_bundle("Desert Foraging Bundle")
    island_foraging = cc_bundle("Island Foraging Bundle")
    sticky = cc_bundle("Sticky Bundle")
    forest = cc_bundle("Forest Bundle")
    green_rain = cc_bundle("Green Rain Bundle")
    wild_medicine = cc_bundle("Wild Medicine Bundle")
    quality_foraging = cc_bundle("Quality Foraging Bundle")
    spring_crops = cc_bundle("Spring Crops Bundle")
    summer_crops = cc_bundle("Summer Crops Bundle")
    fall_crops = cc_bundle("Fall Crops Bundle")
    quality_crops = cc_bundle("Quality Crops Bundle")
    animal = cc_bundle("Animal Bundle")
    artisan = cc_bundle("Artisan Bundle")
    rare_crops = cc_bundle("Rare Crops Bundle")
    fish_farmer = cc_bundle("Fish Farmer's Bundle")
    garden = cc_bundle("Garden Bundle")
    brewer = cc_bundle("Brewer's Bundle")
    orchard = cc_bundle("Orchard Bundle")
    island_crops = cc_bundle("Island Crops Bundle")
    agronomist = cc_bundle("Agronomist's Bundle")
    slime_farmer = cc_bundle("Slime Farmer Bundle")
    sommelier = cc_bundle("Sommelier Bundle")
    dry = cc_bundle("Dry Bundle")
    river_fish = cc_bundle("River Fish Bundle")
    lake_fish = cc_bundle("Lake Fish Bundle")
    ocean_fish = cc_bundle("Ocean Fish Bundle")
    night_fish = cc_bundle("Night Fishing Bundle")
    crab_pot = cc_bundle("Crab Pot Bundle")
    trash = cc_bundle("Trash Bundle")
    recycling = cc_bundle("Recycling Bundle")
    specialty_fish = cc_bundle("Specialty Fish Bundle")
    spring_fish = cc_bundle("Spring Fishing Bundle")
    summer_fish = cc_bundle("Summer Fishing Bundle")
    fall_fish = cc_bundle("Fall Fishing Bundle")
    winter_fish = cc_bundle("Winter Fishing Bundle")
    rain_fish = cc_bundle("Rain Fishing Bundle")
    quality_fish = cc_bundle("Quality Fish Bundle")
    master_fisher = cc_bundle("Master Fisher's Bundle")
    legendary_fish = cc_bundle("Legendary Fish Bundle")
    island_fish = cc_bundle("Island Fish Bundle")
    deep_fishing = cc_bundle("Deep Fishing Bundle")
    tackle = cc_bundle("Tackle Bundle")
    bait = cc_bundle("Master Baiter Bundle")
    specific_bait = cc_bundle("Specific Fishing Bundle")
    fish_smoker = cc_bundle("Fish Smoker Bundle")
    blacksmith = cc_bundle("Blacksmith's Bundle")
    geologist = cc_bundle("Geologist's Bundle")
    adventurer = cc_bundle("Adventurer's Bundle")
    treasure_hunter = cc_bundle("Treasure Hunter's Bundle")
    engineer = cc_bundle("Engineer's Bundle")
    demolition = cc_bundle("Demolition Bundle")
    paleontologist = cc_bundle("Paleontologist's Bundle")
    archaeologist = cc_bundle("Archaeologist's Bundle")
    chef = cc_bundle("Chef's Bundle")
    dye = cc_bundle("Dye Bundle")
    field_research = cc_bundle("Field Research Bundle")
    fodder = cc_bundle("Fodder Bundle")
    enchanter = cc_bundle("Enchanter's Bundle")
    children = cc_bundle("Children's Bundle")
    forager = cc_bundle("Forager's Bundle")
    home_cook = cc_bundle("Home Cook's Bundle")
    helper = cc_bundle("Helper's Bundle")
    spirit_eve = cc_bundle("Spirit's Eve Bundle")
    winter_star = cc_bundle("Winter Star Bundle")
    bartender = cc_bundle("Bartender's Bundle")
    calico = cc_bundle("Calico Bundle")
    raccoon = cc_bundle("Raccoon Bundle")
    money_2500 = cc_bundle("2,500g Bundle")
    money_5000 = cc_bundle("5,000g Bundle")
    money_10000 = cc_bundle("10,000g Bundle")
    money_25000 = cc_bundle("25,000g Bundle")
    gambler = cc_bundle("Gambler's Bundle")
    carnival = cc_bundle("Carnival Bundle")
    walnut_hunter = cc_bundle("Walnut Hunter Bundle")
    qi_helper = cc_bundle("Qi's Helper Bundle")
    missing_bundle = "The Missing Bundle"
    raccoon_fish = "Raccoon Fish"
    raccoon_artisan = "Raccoon Artisan"
    raccoon_food = "Raccoon Food"
    raccoon_foraging = "Raccoon Foraging"
