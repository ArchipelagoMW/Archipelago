from dataclasses import dataclass
from typing import Set, List, FrozenSet, Tuple
from .region_data import SVRegion


@dataclass(frozen=True)
class Villager:
    name: str
    bachelor: bool
    locations: Tuple[str]
    birthday: str
    gifts: Tuple[str]
    available: bool

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
oasis = (SVRegion.desert,)
sewers = (SVRegion.sewers,)
island = (SVRegion.ginger_island,)

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

all_villagers: List[Villager] = []


def villager(name: str, bachelor: bool, locations: Tuple[str, ...], birthday: str, gifts: Tuple[str, ...],
             available: bool) -> Villager:
    npc = Villager(name, bachelor, locations, birthday, gifts, available)
    all_villagers.append(npc)
    return npc


josh = villager("Alex", True, town + alex_house, "Summer", universal_loves + complete_breakfast + salmon_dinner, True)
elliott = villager("Elliott", True, town + beach + elliott_house, "Fall", universal_loves + elliott_loves, True)
harvey = villager("Harvey", True, town + hospital, "Winter", universal_loves + harvey_loves, True)
sam = villager("Sam", True, town, "Summer", universal_loves + sam_loves, True)
sebastian = villager("Sebastian", True, carpenter, "Winter", universal_loves + sebastian_loves, True)
shane = villager("Shane", True, ranch, "Spring", universal_loves + shane_loves, True)
best_girl = villager("Abigail", True, town, "Fall", universal_loves + abigail_loves, True)
emily = villager("Emily", True, town, "Spring", universal_loves + emily_loves, True)
hoe = villager("Haley", True, town, "Spring", universal_loves_no_prismatic_shard + haley_loves, True)
leah = villager("Leah", True, forest, "Winter", universal_loves + leah_loves, True)
nerd = villager("Maru", True, carpenter, "Summer", universal_loves + maru_loves, True)
penny = villager("Penny", True, town, "Fall", universal_loves_no_rabbit_foot + penny_loves, True)
caroline = villager("Caroline", False, town, "Winter", universal_loves + caroline_loves, True)
clint = villager("Clint", False, town, "Winter", universal_loves + clint_loves, True)
demetrius = villager("Demetrius", False, carpenter, "Summer", universal_loves + demetrius_loves, True)
dwarf = villager("Dwarf", False, mines, "Summer", universal_loves + dwarf_loves, False)
gilf = villager("Evelyn", False, town, "Winter", universal_loves + evelyn_loves, True)
boomer = villager("George", False, town, "Fall", universal_loves + george_loves, True)
gus = villager("Gus", False, town, "Summer", universal_loves + gus_loves, True)
jas = villager("Jas", False, ranch, "Summer", universal_loves + jas_loves, True)
jodi = villager("Jodi", False, town, "Fall", universal_loves + jodi_loves, True)
kent = villager("Kent", False, town, "Spring", universal_loves + kent_loves, False)
krobus = villager("Krobus", False, sewers, "Winter", universal_loves + krobus_loves, False)
leo = villager("Leo", False, island, "Summer", universal_loves + leo_loves, False)
lewis = villager("Lewis", False, town, "Spring", universal_loves + lewis_loves, True)
linus = villager("Linus", False, mountain, "Winter", universal_loves + linus_loves, True)
marnie = villager("Marnie", False, ranch, "Fall", universal_loves + marnie_loves, True)
pam = villager("Pam", False, town, "Spring", universal_loves + pam_loves, True)
pierre = villager("Pierre", False, town, "Spring", universal_loves + pierre_loves, True)
milf = villager("Robin", False, carpenter, "Fall", universal_loves + robin_loves, True)
sandy = villager("Sandy", False, oasis, "Fall", universal_loves + sandy_loves, False)
vincent = villager("Vincent", False, town, "Spring", universal_loves + vincent_loves, True)
willy = villager("Willy", False, beach, "Summer", universal_loves + willy_loves, True)
wizard = villager("Wizard", False, forest, "Winter", universal_loves + wizard_loves, True)

all_villagers_by_name = {item.name: item for item in all_villagers}
