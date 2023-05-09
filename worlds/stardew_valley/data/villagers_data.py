from dataclasses import dataclass
from typing import List, Tuple, Optional
from .region_data import SVRegion


@dataclass(frozen=True)
class Villager:
    name: str
    bachelor: bool
    locations: Tuple[str]
    birthday: str
    gifts: Tuple[str]
    available: bool
    mod_name: str

    def __repr__(self):
        return f"{self.name} [Bachelor: {self.bachelor}] [Available from start: {self.available}]" \
               f"(Locations: {self.locations} |" \
               f" Birthday: {self.birthday} |" \
               f" Gifts: {self.gifts}) "


town = (SVRegion.town,)
beach = (SVRegion.beach,)
forest = (SVRegion.forest,)
mountain = (SVRegion.mountain,)
hospital = (SVRegion.hospital,)
carpenter = (SVRegion.carpenter,)
alex_house = (SVRegion.alex_house,)
elliott_house = (SVRegion.elliott_house,)
ranch = (SVRegion.ranch,)
mines = (SVRegion.mines,)
desert = (SVRegion.desert,)
oasis = (SVRegion.oasis,)
sewers = (SVRegion.sewers,)
island = (SVRegion.island_east,)
secret_woods = (SVRegion.secret_woods,)

golden_pumpkin = ("Golden Pumpkin",)
# magic_rock_candy = ("Magic Rock Candy",)
pearl = ("Pearl",)
prismatic_shard = ("Prismatic Shard",)
rabbit_foot = ("Rabbit's Foot",)
universal_loves = golden_pumpkin + pearl + prismatic_shard + rabbit_foot  # , *magic_rock_candy}
universal_loves_no_prismatic_shard = golden_pumpkin + pearl + rabbit_foot  # , *magic_rock_candy}
universal_loves_no_rabbit_foot = golden_pumpkin + pearl + prismatic_shard  # , *magic_rock_candy}
complete_breakfast = ("Complete Breakfast",)
salmon_dinner = ("Salmon Dinner",)
crab_cakes = ("Crab Cakes",)
duck_feather = ("Duck Feather",)
lobster = ("Lobster",)
pomegranate = ("Pomegranate",)
squid_ink = ("Squid Ink",)
# tom_kha_soup = ("Tom Kha Soup",)
elliott_loves = duck_feather + lobster + pomegranate + squid_ink + crab_cakes  # | tom_kha_soup
coffee = ("Coffee",)
pickles = ("Pickles",)
# super_meal = ("Super Meal",)
truffle_oil = ("Truffle Oil",)
wine = ("Wine",)
harvey_loves = coffee + pickles + truffle_oil + wine  # | super_meal
cactus_fruit = ("Cactus Fruit",)
maple_bar = ("Maple Bar",)
pizza = ("Pizza",)
tigerseye = ("Tigerseye",)
sam_loves = cactus_fruit + maple_bar + pizza + tigerseye
frozen_tear = ("Frozen Tear",)
obsidian = ("Obsidian",)
# pumpkin_soup = ("Pumpkin Soup",)
# sashimi = ("Sashimi",)
void_egg = ("Void Egg",)
sebastian_loves = frozen_tear + obsidian + void_egg  # | pumpkin_soup + sashimi
beer = ("Beer",)
hot_pepper = ("Hot Pepper",)
# pepper_poppers = ("Pepper Poppers",)
shane_loves = beer + hot_pepper + pizza  # | pepper_poppers
amethyst = ("Amethyst",)
# banana_pudding = ("Banana Pudding",)
blackberry_cobbler = ("Blackberry Cobbler",)
chocolate_cake = ("Chocolate Cake",)
pufferfish = ("Pufferfish",)
pumpkin = ("Pumpkin",)
# spicy_eel = ("Spicy Eel",)
abigail_loves = amethyst + blackberry_cobbler + chocolate_cake + pufferfish + pumpkin  # | banana_pudding + spicy_eel
aquamarine = ("Aquamarine",)
cloth = ("Cloth",)
emerald = ("Emerald",)
jade = ("Jade",)
ruby = ("Ruby",)
survival_burger = ("Survival Burger",)
topaz = ("Topaz",)
wool = ("Wool",)
emily_loves = amethyst + aquamarine + cloth + emerald + jade + ruby + survival_burger + topaz + wool
coconut = ("Coconut",)
fruit_salad = ("Fruit Salad",)
pink_cake = ("Pink Cake",)
sunflower = ("Sunflower",)
haley_loves = coconut + fruit_salad + pink_cake + sunflower
goat_cheese = ("Goat Cheese",)
poppyseed_muffin = ("Poppyseed Muffin",)
salad = ("Salad",)
stir_fry = ("Stir Fry",)
truffle = ("Truffle",)
# vegetable_medley = ("Vegetable Medley",)
leah_loves = goat_cheese + poppyseed_muffin + salad + stir_fry + truffle + wine  # | vegetable_medley
battery_pack = ("Battery Pack",)
cauliflower = ("Cauliflower",)
cheese_cauliflower = ("Cheese Cauliflower",)
diamond = ("Diamond",)
gold_bar = ("Gold Bar",)
iridium_bar = ("Iridium Bar",)
miners_treat = ("Miner's Treat",)
pepper_poppers = ("Pepper Poppers",)
radioactive_bar = ("Radioactive Bar",)
rhubarb_pie = ("Rhubarb Pie",)
strawberry = ("Strawberry",)
maru_loves = battery_pack + cauliflower + diamond + gold_bar + iridium_bar + miners_treat + radioactive_bar + strawberry  # | cheese_cauliflower + pepper_poppers + rhubarb_pie
melon = ("Melon",)
poppy = ("Poppy",)
# red_plate = ("Red Plate",)
roots_platter = ("Roots Platter",)
sandfish = ("Sandfish",)
penny_loves = diamond + emerald + melon + poppy + poppyseed_muffin + roots_platter + sandfish  # | tom_kha_soup + red_plate
# fish_taco = ("Fish Taco",)
green_tea = ("Green Tea",)
summer_spangle = ("Summer Spangle",)
tropical_curry = ("Tropical Curry",)
caroline_loves = summer_spangle + tropical_curry  # | fish_taco + green_tea
artichoke_dip = ("Artichoke Dip",)
fiddlehead_risotto = ("Fiddlehead Risotto",)
omni_geode = ("Omni Geode",)
clint_loves = amethyst + aquamarine + artichoke_dip + emerald + fiddlehead_risotto + gold_bar + iridium_bar + jade + \
              omni_geode + ruby + topaz
# bean_hotpot = ("Bean Hotpot",)
ice_cream = ("Ice Cream",)
# rice_pudding = ("Rice Pudding",)
demetrius_loves = ice_cream + strawberry  # | bean_hotpot + rice_pudding
lemon_stone = ("Lemon Stone",)
dwarf_loves = amethyst + aquamarine + emerald + jade + lemon_stone + omni_geode + ruby + topaz
beet = ("Beet",)
fairy_rose = ("Fairy Rose",)
# stuffing = ("Stuffing",)
tulip = ("Tulip",)
evelyn_loves = beet + chocolate_cake + diamond + fairy_rose + tulip  # | stuffing
# fried_mushroom = ("Fried Mushroom",)
leek = ("Leek",)
george_loves = leek  # | fried_mushroom
# escargot = ("Escargot",)
orange = ("Orange",)
gus_loves = diamond + orange + tropical_curry  # | escargot + fish_taco
plum_pudding = ("Plum Pudding",)
jas_loves = fairy_rose + pink_cake + plum_pudding
# crispy_bass = ("Crispy Bass",)
# eggplant_parmesan = ("Eggplant Parmesan",)
# fried_eel = ("Fried Eel",)
pancakes = ("Pancakes",)
jodi_loves = chocolate_cake + diamond + pancakes + rhubarb_pie  # | vegetable_medley + crispy_bass + eggplant_parmesan + fried_eel
roasted_hazelnuts = ("Roasted Hazelnuts",)
kent_loves = fiddlehead_risotto + roasted_hazelnuts
void_mayonnaise = ("Void Mayonnaise",)
wild_horseradish = ("Wild Horseradish",)
krobus_loves = diamond + iridium_bar + pumpkin + void_egg + void_mayonnaise + wild_horseradish
mango = ("Mango",)
ostrich_egg = ("Ostrich Egg",)
# poi = ("Poi",)
leo_loves = duck_feather + mango + ostrich_egg  # | poi
# autumns_bounty = ("Autumn's Bounty",)
glazed_yams = ("Glazed Yams",)
lewis_loves = glazed_yams + green_tea + hot_pepper  # | autumns_bounty + vegetable_medley
# blueberry_tart = ("Blueberry Tart",)
dish_o_the_sea = ("Dish O' The Sea",)
yam = ("Yam",)
linus_loves = cactus_fruit + coconut + dish_o_the_sea + yam  # | blueberry_tart
farmers_lunch = ("Farmer's Lunch",)
pumpkin_pie = ("Pumpkin Pie",)
marnie_loves = diamond + farmers_lunch + pink_cake + pumpkin_pie
mead = ("Mead",)
pale_ale = ("Pale Ale",)
parsnip = ("Parsnip",)
# parsnip_soup = ("Parsnip Soup",)
pina_colada = ("Piña Colada",)
pam_loves = beer + cactus_fruit + glazed_yams + mead + pale_ale + parsnip + pina_colada  # | parsnip_soup
# fried_calamari = ("Fried Calamari",)
pierre_loves = ()  # fried_calamari
peach = ("Peach",)
spaghetti = ("Spaghetti",)
robin_loves = goat_cheese + peach + spaghetti
crocus = ("Crocus",)
daffodil = ("Daffodil",)
# mango_stocky_rice = ("Mango Sticky Rice",)
sweet_pea = ("Sweet Pea",)
sandy_loves = crocus + daffodil + sweet_pea  # | mango_stocky_rice
cranberry_candy = ("Cranberry Candy",)
ginger_ale = ("Ginger Ale",)
grape = ("Grape",)
snail = ("Snail",)
vincent_loves = cranberry_candy + ginger_ale + grape + pink_cake + snail
catfish = ("Catfish",)
octopus = ("Octopus",)
willy_loves = catfish + diamond + iridium_bar + mead + octopus + pumpkin
purple_mushroom = ("Purple Mushroom",)
solar_essence = ("Solar Essence",)
super_cucumber = ("Super Cucumber",)
void_essence = ("Void Essence",)
wizard_loves = purple_mushroom + solar_essence + super_cucumber + void_essence

#Custom NPC Items and Loves

blueberry = ("Blueberry",)
chanterelle = ("Chanterelle",)
garlic = ("Garlic",)
omelet = ("Omelet",)
wild_plum = ("Wild Plum",)
rhubarb = ("Rhubarb",)
fried_mushroom = ("Fried Mushroom",)
eggplant_parmesan = ("Eggplant Parmesan",)
maki_roll = ("Maki Roll",)
red_plate = ("Red Plate",)
baked_fish = ("Baked Fish",)
cheese = ("Cheese",)
eel = ("Eel",)
flounder = ("Flounder",)
salmon = ("Salmon",)
sashimi = ("Sashimi",)
tuna = ("Tuna",)
energy_tonic = ("Energy Tonic",)
kale = ("Kale",)
muscle_remedy = ("Muscle Remedy",)
vegetable_medley = ("Vegetable Medley",)
trilobite = ("Trilobite",)
golden_mask = ("Golden Mask",)
rainbow_shell = ("Rainbow Shell",)
blue_jazz = ("Blue Jazz",)
honey = ("Honey",)
apple = ("Apple",)
dwarf_gadget = ("Dwarf Gadget",)
dwarvish_helm = ("Dwarvish Helm",)
fire_quartz = ("Fire Quartz",)
jasper = ("Jasper",)
opal = ("Opal",)
rare_disc = ("Rare Disc",)
ancient_doll = ("Ancient Doll",)
elvish_jewelry = ("Elvish Jewelry",)
dinosaur_egg = ("Dinosaur Egg",)
strange_doll = ("Strange Doll",)
joja_cola = ("Joja Cola",)
hashbrowns = ("Hashbrowns",)
jelly = ("Jelly",)
ghost_crystal = ("Ghost Crystal",)
prehistoric_scapula = ("Prehistoric Scapula",)
cherry = ("Cherry",)
ayeisha_loves = blackberry_cobbler + blueberry + chanterelle + emerald + omelet + sweet_pea + wild_plum + rhubarb + \
                fried_mushroom + eggplant_parmesan
shiko_loves = maki_roll + red_plate + ruby + salad + wine
wellwick_loves = fairy_rose + solar_essence + void_essence + wine
mister_ginger_loves = baked_fish + cheese + eel + flounder + goat_cheese + lobster + salmon + sashimi + tuna
delores_loves = aquamarine + blueberry + energy_tonic + green_tea + kale + muscle_remedy + red_plate + \
                roots_platter + salad + vegetable_medley
yoba_loves = golden_mask + rainbow_shell
eugene_loves = blue_jazz + fairy_rose + green_tea + honey + poppy + poppyseed_muffin + \
               salad + summer_spangle + sunflower + tulip
jasper_loves = apple + blueberry + diamond + dwarf_gadget + dwarvish_helm + fire_quartz + jasper + \
               miners_treat + opal + rare_disc
juna_loves = ancient_doll + elvish_jewelry + dinosaur_egg + strange_doll + joja_cola + hashbrowns + pancakes + \
             pink_cake + jelly + ghost_crystal + prehistoric_scapula + cherry


all_villagers: List[Villager] = []


def villager(name: str, bachelor: bool, locations: Tuple[str, ...], birthday: str, gifts: Tuple[str, ...],
             available: bool, mod_name: Optional[str]) -> Villager:
    npc = Villager(name, bachelor, locations, birthday, gifts, available, mod_name)
    all_villagers.append(npc)
    return npc


josh = villager("Alex", True, town + alex_house, "Summer", universal_loves + complete_breakfast + salmon_dinner, True, None)
elliott = villager("Elliott", True, town + beach + elliott_house, "Fall", universal_loves + elliott_loves, True, None)
harvey = villager("Harvey", True, town + hospital, "Winter", universal_loves + harvey_loves, True, None)
sam = villager("Sam", True, town, "Summer", universal_loves + sam_loves, True, None)
sebastian = villager("Sebastian", True, carpenter, "Winter", universal_loves + sebastian_loves, True, None)
shane = villager("Shane", True, ranch, "Spring", universal_loves + shane_loves, True, None)
best_girl = villager("Abigail", True, town, "Fall", universal_loves + abigail_loves, True, None)
emily = villager("Emily", True, town, "Spring", universal_loves + emily_loves, True, None)
hoe = villager("Haley", True, town, "Spring", universal_loves_no_prismatic_shard + haley_loves, True, None)
leah = villager("Leah", True, forest, "Winter", universal_loves + leah_loves, True, None)
nerd = villager("Maru", True, carpenter, "Summer", universal_loves + maru_loves, True, None)
penny = villager("Penny", True, town, "Fall", universal_loves_no_rabbit_foot + penny_loves, True, None)
caroline = villager("Caroline", False, town, "Winter", universal_loves + caroline_loves, True, None)
clint = villager("Clint", False, town, "Winter", universal_loves + clint_loves, True, None)
demetrius = villager("Demetrius", False, carpenter, "Summer", universal_loves + demetrius_loves, True, None)
dwarf = villager("Dwarf", False, mines, "Summer", universal_loves + dwarf_loves, False, None)
gilf = villager("Evelyn", False, town, "Winter", universal_loves + evelyn_loves, True, None)
boomer = villager("George", False, town, "Fall", universal_loves + george_loves, True, None)
gus = villager("Gus", False, town, "Summer", universal_loves + gus_loves, True, None)
jas = villager("Jas", False, ranch, "Summer", universal_loves + jas_loves, True, None)
jodi = villager("Jodi", False, town, "Fall", universal_loves + jodi_loves, True, None)
kent = villager("Kent", False, town, "Spring", universal_loves + kent_loves, False, None)
krobus = villager("Krobus", False, sewers, "Winter", universal_loves + krobus_loves, False, None)
leo = villager("Leo", False, island, "Summer", universal_loves + leo_loves, False, None)
lewis = villager("Lewis", False, town, "Spring", universal_loves + lewis_loves, True, None)
linus = villager("Linus", False, mountain, "Winter", universal_loves + linus_loves, True, None)
marnie = villager("Marnie", False, ranch, "Fall", universal_loves + marnie_loves, True, None)
pam = villager("Pam", False, town, "Spring", universal_loves + pam_loves, True, None)
pierre = villager("Pierre", False, town, "Spring", universal_loves + pierre_loves, True, None)
milf = villager("Robin", False, carpenter, "Fall", universal_loves + robin_loves, True, None)
sandy = villager("Sandy", False, oasis, "Fall", universal_loves + sandy_loves, False, None)
vincent = villager("Vincent", False, town, "Spring", universal_loves + vincent_loves, True, None)
willy = villager("Willy", False, beach, "Summer", universal_loves + willy_loves, True, None)
wizard = villager("Wizard", False, forest, "Winter", universal_loves + wizard_loves, True, None)

# Custom NPCs
alec = villager("Alec", True, forest, "Winter", universal_loves + trilobite, True, "Alec Revisited")
ayeisha = villager("Ayeisha", False, town, "Summer", universal_loves + ayeisha_loves, True,
                   "Ayeisha - The Postal Worker (Custom NPC)")
delores = villager("Delores", True, forest, "Winter", universal_loves + delores_loves, True, "Delores - Custom NPC")
eugene = villager("Eugene", True, forest, "Spring", universal_loves + eugene_loves, True, "Custom NPC Eugene")
jasper = villager("Jasper", True, town, "Fall", universal_loves + jasper_loves, True, "Professor Jasper Thomas")
juna = villager("Juna", False, forest, "Summer", universal_loves + juna_loves, True, "Juna - Roommate NPC")
kitty = villager("Mr. Ginger", False, forest, "Summer", universal_loves + mister_ginger_loves, True,
                 "Mister Ginger (cat npc)")
shiko = villager("Shiko", True, town, "Winter", universal_loves + shiko_loves, True, "Shiko - New Custom NPC")
wellwick = villager("Wellwick", True, forest, "Winter", universal_loves + wellwick_loves, True, "'Prophet' Wellwick")
yoba = villager("Yoba", False, secret_woods, "Spring", universal_loves + yoba_loves, False, "Custom NPC - Yoba")

all_villagers_by_name = {item.name: item for item in all_villagers}
