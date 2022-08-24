
from BaseClasses import Location
from .rom_addresses import rom_addresses
loc_id_start = 17200000
locations = []


class LocationData:
    def __init__(self, region, name, original_item, rom_address=None, ram_address=None, rule=lambda state: True,
                 event=False, item_rule=lambda state: True):
        self.region = region
        if "Route" in region:
            region = " ".join(region.split()[:2])
        self.name = region + " - " + name
        self.rule = rule
        self.original_item = original_item
        self.rom_address = rom_address
        self.ram_address = ram_address
        self.event = event
        self.item_rule = item_rule
        locations.append(self)


class EventFlag:
    def __init__(self, flag):
        self.byte = int(flag / 8)
        self.bit = flag % 8
        self.flag = flag


class Missable:
    def __init__(self, flag):
        self.byte = int(flag / 8)
        self.bit = flag % 8
        self.flag = flag


class Hidden:
    def __init__(self, flag):
        self.byte = int(flag / 8)
        self.bit = flag % 8
        self.flag = flag


class Rod:
    def __init__(self, flag):
        self.byte = 0
        self.bit = flag
        self.flag = flag


def get_locations(player=None):
    # Event flags
    locations = [

        LocationData("Vermilion City", "Fishing Guru", "Old Rod", rom_addresses["Rod_Vermilion_City_Fishing_Guru"], Rod(3)),
        LocationData("Fuchsia City", "Fishing Guru's Brother", "Good Rod", rom_addresses["Rod_Fuchsia_City_Fishing_Brother"], Rod(4)),
        LocationData("Route 12 South", "Fishing Guru's Brother", "Super Rod", rom_addresses["Rod_Route_12_Fishing_Brother"], Rod(5)),

        LocationData("Pallet Town", "Player's PC", "Potion", rom_addresses['PC_Item'], EventFlag(1),
                     item_rule=lambda i: i.player == player and "Badge" not in i.name),
        LocationData("Celadon City", "Mansion Lady", "Tea", rom_addresses["Event_Mansion_Lady"], EventFlag(2)),
        LocationData("Pallet Town", "Rival's Sister", "Town Map", rom_addresses["Event_Rivals_Sister"], EventFlag(24),
                     lambda state: state.has("Oak's Parcel", player)),
        LocationData("Pallet Town", "Oak's Gift", "Poke Ball", rom_addresses["Event_Oaks_Gift"], EventFlag(36),
                     lambda state: state.has("Oak's Parcel", player)),
        LocationData("Route 1", "Free Sample Man", "Potion", rom_addresses["Event_Free_Sample"], EventFlag(960)),
        LocationData("Viridian City", "Sleepy Guy", "TM42 Dream Eater", rom_addresses["Event_Sleepy_Guy"],
                     EventFlag(41), lambda state: state._pokemon_rb_can_cut(player) or state._pokemon_rb_can_surf(player)),
        LocationData("Viridian City", "Pokemart Quest", "Oak's Parcel", rom_addresses["Event_Pokemart_Quest"],
                     EventFlag(57)),
        LocationData("Viridian Gym", "Giovanni 2", "TM27 Fissure", rom_addresses["Event_Viridian_Gym"], EventFlag(80)),
        LocationData("Route 2 East", "Oak's Aide", "HM05 Flash", rom_addresses["Event_Route_2_Oaks_Aide"],
                     EventFlag(984), item_rule=lambda i: not i.advancement),
        LocationData("Pewter City", "Museum", "Old Amber", rom_addresses["Event_Museum"], EventFlag(105), lambda state: state._pokemon_rb_can_cut(player)),
        LocationData("Pewter Gym", "Brock 2", "TM34 Bide", rom_addresses["Event_Pewter_Gym"], EventFlag(118)),
        LocationData("Cerulean City", "Bicycle Shop", "Bicycle", rom_addresses["Event_Bicycle_Shop"], EventFlag(192),
                     lambda state: state.has("Bike Voucher", player)),
        LocationData("Cerulean Gym", "Misty 2", "TM11 Bubble Beam", rom_addresses["Event_Cerulean_Gym"],
                     EventFlag(190)),
        LocationData("Route 24", "Nugget Bridge", "Nugget", rom_addresses["Event_Nugget_Bridge"], EventFlag(1344)),
        LocationData("Route 25", "Bill", "S.S. Ticket", rom_addresses["Event_Bill"], EventFlag(1372)),
        LocationData("Lavender Town", "Mr. Fuji", "Poke Flute", rom_addresses["Event_Fuji"], EventFlag(296), lambda state: state.has("Fuji Saved", player)),
        LocationData("Route 12 North", "Mourning Girl", "TM39 Swift", rom_addresses["Event_Mourning_Girl"],
                     EventFlag(1152)),
        LocationData("Vermilion City", "Pokemon Fan Club", "Bike Voucher", rom_addresses["Event_Pokemon_Fan_Club"],
                     EventFlag(337)),
        LocationData("Vermilion Gym", "Lt. Surge 2", "TM24 Thunderbolt", rom_addresses["Event_Vermillion_Gym"],
                     EventFlag(358), lambda state: state._pokemon_rb_can_cut(player or state._pokemon_rb_can_surf(player))),
        LocationData("S.S. Anne 2F", "Captain", "HM01 Cut", rom_addresses["Event_SS_Anne_Captain"], EventFlag(1504)),
        LocationData("Route 11 East", "Oak's Aide", "Item Finder", rom_addresses["Event_Rt11_Oaks_Aide"],
                     EventFlag(1151), item_rule=lambda i: not i.advancement),
        LocationData("Celadon City", "Stranded Man", "TM41 Soft Boiled", rom_addresses["Event_Stranded_Man"],
                     EventFlag(384), lambda state: state._pokemon_rb_can_surf(player)),
        LocationData("Celadon City", "Thirsty Girl Gets Water", "TM13 Ice Beam",
                     rom_addresses["Event_Thirsty_Girl_Lemonade"], EventFlag(396)),
        LocationData("Celadon City", "Thirsty Girl Gets Soda Pop", "TM48 Rock Slide",
                     rom_addresses["Event_Thirsty_Girl_Soda"], EventFlag(397)),
        LocationData("Celadon City", "Thirsty Girl Gets Lemonade", "TM49 Tri Attack",
                     rom_addresses["Event_Thirsty_Girl_Water"], EventFlag(398)),
        LocationData("Celadon City", "Counter Man", "TM18 Counter", rom_addresses["Event_Counter"], EventFlag(399)),
        LocationData("Celadon City", "Gambling Addict", "Coin Case", rom_addresses["Event_Gambling_Addict"],
                     EventFlag(480)),
        LocationData("Celadon Gym", "Erika 2", "TM21 Mega Drain", rom_addresses["Event_Celadon_Gym"], EventFlag(424)),
        LocationData("Silph Co 11F", "Silph Co President", "Master Ball", rom_addresses["Event_Silph_Co_President"],
                     EventFlag(1933), lambda state: state.has("Card Key", player)),
        LocationData("Silph Co 2F", "Woman", "TM36 Self Destruct", rom_addresses["Event_Scared_Woman"],
                     EventFlag(1791)),
        LocationData("Route 16", "House Woman", "HM02 Fly", rom_addresses["Event_Rt16_House_Woman"], EventFlag(1230),
                     lambda state: state._pokemon_rb_can_cut(player)),
        LocationData("Fuchsia City", "Oak's Aide", "Exp. All", rom_addresses["Event_Rt_15_Oaks_Aide"], EventFlag(1200), item_rule=lambda i: not i.advancement),
        LocationData("Fuchsia City", "Safari Zone Warden", "HM04 Strength", rom_addresses["Event_Warden"], EventFlag(568)),
        LocationData("Fuchsia Gym", "Koga 2", "TM06 Toxic", rom_addresses["Event_Fuschia_Gym"], EventFlag(600)),
        LocationData("Safari Zone West", "Secret House", "HM03 Surf", rom_addresses["Event_Safari_Zone_Secret_House"], EventFlag(2176)),
        LocationData("Cinnabar Island", "Lab Scientist", "TM35 Metronome", rom_addresses["Event_Lab_Scientist"], EventFlag(727)),
        LocationData("Cinnabar Gym", "Blaine 2", "TM38 Fire Blast", rom_addresses["Event_Cinnabar_Gym"],
                     EventFlag(664), lambda state: state.has("Secret Key", player)),
        LocationData("Copycat's House", "Copycat", "TM31 Mimic", rom_addresses["Event_Copycat"], EventFlag(832)),
        LocationData("Saffron City", "Mr. Psychic", "TM29 Psychic", rom_addresses["Event_Mr_Psychic"], EventFlag(944)),
        LocationData("Saffron Gym", "Sabrina 2", "TM46 Psywave", rom_addresses["Event_Saffron_Gym"], EventFlag(864)),
        LocationData("Cerulean City", "Rocket Thief", "TM28 Dig", rom_addresses["Event_Rocket_Thief"],
                     Missable(6)),
        LocationData("Route 2 East", "South Item", "Moon Stone", rom_addresses["Missable_Route_2_Item_1"],
                     Missable(25)),
        LocationData("Route 2 East", "North Item", "HP Up", rom_addresses["Missable_Route_2_Item_2"], Missable(26)),
        LocationData("Route 4", "Item", "TM04 Whirlwind", rom_addresses["Missable_Route_4_Item"], Missable(27)),
        LocationData("Route 9", "Item", "TM30 Teleport", rom_addresses["Missable_Route_9_Item"], Missable(28)),
        LocationData("Route 12 North", "Item 1", "TM16 Pay Day", rom_addresses["Missable_Route_12_Item_1"], Missable(30)),
        LocationData("Route 12 South", "Item 2", "Iron", rom_addresses["Missable_Route_12_Item_2"], Missable(31),
                     lambda state: state._pokemon_rb_can_cut(player)),
        LocationData("Route 15", "Item", "TM20 Rage", rom_addresses["Missable_Route_15_Item"], Missable(32), lambda state: state._pokemon_rb_can_cut(player)),
        LocationData("Route 24", "Item", "TM45 Thunder Wave", rom_addresses["Missable_Route_24_Item"], Missable(37)),
        LocationData("Route 25", "Item", "TM19 Seismic Toss", rom_addresses["Missable_Route_25_Item"], Missable(38), lambda state: state._pokemon_rb_can_cut(player)),
        LocationData("Viridian Gym", "Item", "Revive", rom_addresses["Missable_Viridian_Gym_Item"], Missable(51)),
        LocationData("Cerulean Cave 1F", "Item 1", "Full Restore", rom_addresses["Missable_Cerulean_Cave_1F_Item_1"],
                     Missable(53)),
        LocationData("Cerulean Cave 1F", "Item 2", "Max Elixir", rom_addresses["Missable_Cerulean_Cave_1F_Item_2"],
                     Missable(54)),
        LocationData("Cerulean Cave 1F", "Item 3", "Nugget", rom_addresses["Missable_Cerulean_Cave_1F_Item_3"],
                     Missable(55)),
        LocationData("Pokemon Tower 3F", "Item", "Escape Rope", rom_addresses["Missable_Pokemon_Tower_3F_Item"],
                     Missable(57)),
        LocationData("Pokemon Tower 4F", "Item 1", "Elixir", rom_addresses["Missable_Pokemon_Tower_4F_Item_1"],
                     Missable(58)),
        LocationData("Pokemon Tower 4F", "Item 2", "Awakening", rom_addresses["Missable_Pokemon_Tower_4F_Item_2"],
                     Missable(59)),
        LocationData("Pokemon Tower 4F", "Item 3", "HP Up", rom_addresses["Missable_Pokemon_Tower_4F_Item_3"],
                     Missable(60)),
        LocationData("Pokemon Tower 5F", "Item", "Nugget", rom_addresses["Missable_Pokemon_Tower_5F_Item"],
                     Missable(61)),
        LocationData("Pokemon Tower 6F", "Item 1", "Rare Candy", rom_addresses["Missable_Pokemon_Tower_6F_Item_1"],
                     Missable(62)),
        LocationData("Pokemon Tower 6F", "Item 2", "X Accuracy", rom_addresses["Missable_Pokemon_Tower_6F_Item_2"],
                     Missable(63)),
        LocationData("Fuchsia City", "Warden's House Item", "Rare Candy", rom_addresses["Missable_Wardens_House_Item"],
                     Missable(71), lambda state: state._pokemon_rb_can_strength(player)),
        LocationData("Pokemon Mansion 1F", "Item 1", "Escape Rope",
                     rom_addresses["Missable_Pokemon_Mansion_1F_Item_1"], Missable(72)),
        LocationData("Pokemon Mansion 1F", "Item 2", "Carbos", rom_addresses["Missable_Pokemon_Mansion_1F_Item_2"],
                     Missable(73)),
        LocationData("Power Plant", "Item 1", "Carbos", rom_addresses["Missable_Power_Plant_Item_1"], Missable(86)),
        LocationData("Power Plant", "Item 2", "HP Up", rom_addresses["Missable_Power_Plant_Item_2"], Missable(87)),
        LocationData("Power Plant", "Item 3", "Rare Candy", rom_addresses["Missable_Power_Plant_Item_3"],
                     Missable(88)),
        LocationData("Power Plant", "Item 4", "TM25 Thunder", rom_addresses["Missable_Power_Plant_Item_4"],
                     Missable(89)),
        LocationData("Power Plant", "Item 5", "TM33 Reflect", rom_addresses["Missable_Power_Plant_Item_5"],
                     Missable(90)),
        LocationData("Victory Road 2F", "Item 1", "TM17 Submission", rom_addresses["Missable_Victory_Road_2F_Item_1"],
                     Missable(92)),
        LocationData("Victory Road 2F", "Item 2", "Full Heal", rom_addresses["Missable_Victory_Road_2F_Item_2"],
                     Missable(93)),
        LocationData("Victory Road 2F", "Item 3", "TM05 Mega Kick", rom_addresses["Missable_Victory_Road_2F_Item_3"],
                     Missable(94)),
        LocationData("Victory Road 2F", "Item 4", "Guard Spec", rom_addresses["Missable_Victory_Road_2F_Item_4"],
                     Missable(95)),
        LocationData("Viridian Forest", "East Item", "Antidote", rom_addresses["Missable_Viridian_Forest_Item_1"],
                     Missable(100)),
        LocationData("Viridian Forest", "Northwest Item", "Potion", rom_addresses["Missable_Viridian_Forest_Item_2"],
                     Missable(101)),
        LocationData("Viridian Forest", "Southwest Item", "Poke Ball",
                     rom_addresses["Missable_Viridian_Forest_Item_3"], Missable(102)),
        LocationData("Mt Moon 1F", "West Item", "Potion", rom_addresses["Missable_Mt_Moon_1F_Item_1"], Missable(103)),
        LocationData("Mt Moon 1F", "Northwest Item", "Moon Stone", rom_addresses["Missable_Mt_Moon_1F_Item_2"], Missable(104)),
        LocationData("Mt Moon 1F", "Southeast Item", "Rare Candy", rom_addresses["Missable_Mt_Moon_1F_Item_3"], Missable(105)),
        LocationData("Mt Moon 1F", "East Item", "Escape Rope", rom_addresses["Missable_Mt_Moon_1F_Item_4"],
                     Missable(106)),
        LocationData("Mt Moon 1F", "South Item", "Potion", rom_addresses["Missable_Mt_Moon_1F_Item_5"], Missable(107)),
        LocationData("Mt Moon 1F", "Southwest Item", "TM12 Water Gun", rom_addresses["Missable_Mt_Moon_1F_Item_6"],
                     Missable(108)),
        #LocationData("Mt Moon B2F", "Fossil 1", "HP Up", rom_addresses[""], Missable(109)),
        #LocationData("Mt Moon B2F", "Fossil 2", "TM01 Mega Punch", rom_addresses[""],
        #             Missable(110)),
        LocationData("Mt Moon B2F", "Item 1", "HP Up", rom_addresses["Missable_Mt_Moon_B2F_Item_1"], Missable(111)),
        LocationData("Mt Moon B2F", "Item 2", "TM01 Mega Punch", rom_addresses["Missable_Mt_Moon_B2F_Item_2"],
                     Missable(112)),
        LocationData("S.S. Anne 1F", "Item", "TM08 Body Slam", rom_addresses["Missable_SS_Anne_1F_Item"],
                     Missable(114)),
        LocationData("S.S. Anne 2F", "Item 1", "Max Ether", rom_addresses["Missable_SS_Anne_2F_Item_1"],
                     Missable(115)),
        LocationData("S.S. Anne 2F", "Item 2", "Rare Candy", rom_addresses["Missable_SS_Anne_2F_Item_2"],
                     Missable(116)),
        LocationData("S.S. Anne B1F", "Item 1", "Ether", rom_addresses["Missable_SS_Anne_B1F_Item_1"], Missable(117)),
        LocationData("S.S. Anne B1F", "Item 2", "TM44 Rest", rom_addresses["Missable_SS_Anne_B1F_Item_2"],
                     Missable(118)),
        LocationData("S.S. Anne B1F", "Item 3", "Max Potion", rom_addresses["Missable_SS_Anne_B1F_Item_3"],
                     Missable(119)),
        LocationData("Victory Road 3F", "Item 1", "Max Revive", rom_addresses["Missable_Victory_Road_3F_Item_1"],
                     Missable(120)),
        LocationData("Victory Road 3F", "Item 2", "TM47 Explosion", rom_addresses["Missable_Victory_Road_3F_Item_2"],
                     Missable(121)),
        LocationData("Rocket Hideout B1F", "Item 1", "Escape Rope",
                     rom_addresses["Missable_Rocket_Hideout_B1F_Item_1"], Missable(123)),
        LocationData("Rocket Hideout B1F", "Item 2", "Hyper Potion",
                     rom_addresses["Missable_Rocket_Hideout_B1F_Item_2"], Missable(124)),
        LocationData("Rocket Hideout B2F", "Item 1", "Moon Stone", rom_addresses["Missable_Rocket_Hideout_B2F_Item_1"],
                     Missable(125)),
        LocationData("Rocket Hideout B2F", "Item 2", "Nugget", rom_addresses["Missable_Rocket_Hideout_B2F_Item_2"],
                     Missable(126)),
        LocationData("Rocket Hideout B2F", "Item 3", "TM07 Horn Drill",
                     rom_addresses["Missable_Rocket_Hideout_B2F_Item_3"], Missable(127)),
        LocationData("Rocket Hideout B2F", "Item 4", "Super Potion",
                     rom_addresses["Missable_Rocket_Hideout_B2F_Item_4"], Missable(128)),
        LocationData("Rocket Hideout B3F", "Item 1", "TM10 Double Edge",
                     rom_addresses["Missable_Rocket_Hideout_B3F_Item_1"], Missable(129)),
        LocationData("Rocket Hideout B3F", "Item 2", "Rare Candy", rom_addresses["Missable_Rocket_Hideout_B3F_Item_2"],
                     Missable(130)),
        LocationData("Rocket Hideout B4F", "Item 1", "HP Up", rom_addresses["Missable_Rocket_Hideout_B4F_Item_1"],
                     Missable(132)),
        LocationData("Rocket Hideout B4F", "Item 2", "TM02 Razor Wind",
                     rom_addresses["Missable_Rocket_Hideout_B4F_Item_2"], Missable(133)),
        LocationData("Rocket Hideout B4F", "Item 3", "Iron", rom_addresses["Missable_Rocket_Hideout_B4F_Item_3"],
                     Missable(134), lambda state: state.has("Lift Key", player)),
        LocationData("Rocket Hideout B4F", "Giovanni Item", "Silph Scope",
                     rom_addresses["Missable_Rocket_Hideout_B4F_Item_4"], EventFlag(0x6A7), lambda state: state.has("Lift Key", player)), # Missable(135)
        LocationData("Rocket Hideout B4F", "Rocket Grunt Item", "Lift Key", rom_addresses["Missable_Rocket_Hideout_B4F_Item_5"],
                     EventFlag(0x6A6)), # Missable(136)
        LocationData("Silph Co 3F", "Item", "Hyper Potion", rom_addresses["Missable_Silph_Co_3F_Item"], Missable(144),
                     lambda state: state.has("Card Key", player)),
        LocationData("Silph Co 4F", "Item 1", "Full Heal", rom_addresses["Missable_Silph_Co_4F_Item_1"],
                     Missable(148), lambda state: state.has("Card Key", player)),
        LocationData("Silph Co 4F", "Item 2", "Max Revive", rom_addresses["Missable_Silph_Co_4F_Item_2"],
                     Missable(149), lambda state: state.has("Card Key", player)),
        LocationData("Silph Co 4F", "Item 3", "Escape Rope", rom_addresses["Missable_Silph_Co_4F_Item_3"],
                     Missable(150), lambda state: state.has("Card Key", player)),
        LocationData("Silph Co 5F", "Item 1", "TM09 Take Down", rom_addresses["Missable_Silph_Co_5F_Item_1"],
                     Missable(155)),
        LocationData("Silph Co 5F", "Item 2", "Protein", rom_addresses["Missable_Silph_Co_5F_Item_2"], Missable(156),
                     lambda state: state.has("Card Key", player)),
        LocationData("Silph Co 5F", "Item 3", "Card Key", rom_addresses["Missable_Silph_Co_5F_Item_3"], Missable(157)),
        LocationData("Silph Co 6F", "Item 1", "HP Up", rom_addresses["Missable_Silph_Co_6F_Item_1"], Missable(161),
                     lambda state: state.has("Card Key", player)),
        LocationData("Silph Co 6F", "Item 2", "X Accuracy", rom_addresses["Missable_Silph_Co_6F_Item_2"],
                     Missable(162), lambda state: state.has("Card Key", player)),
        LocationData("Silph Co 7F", "Item 1", "Calcium", rom_addresses["Missable_Silph_Co_7F_Item_1"], Missable(168)),
        LocationData("Silph Co 7F", "Item 2", "TM03 Swords Dance", rom_addresses["Missable_Silph_Co_7F_Item_2"],
                     Missable(169), lambda state: state.has("Card Key", player)),
        LocationData("Silph Co 10F", "Item 1", "TM26 Earthquake", rom_addresses["Missable_Silph_Co_10F_Item_1"],
                     Missable(180)),
        LocationData("Silph Co 10F", "Item 2", "Rare Candy", rom_addresses["Missable_Silph_Co_10F_Item_2"],
                     Missable(181)),
        LocationData("Silph Co 10F", "Item 3", "Carbos", rom_addresses["Missable_Silph_Co_10F_Item_3"], Missable(182)),
        LocationData("Pokemon Mansion 2F", "Item", "Calcium", rom_addresses["Missable_Pokemon_Mansion_2F_Item"],
                     Missable(187)),
        LocationData("Pokemon Mansion 3F", "Item 1", "Max Potion", rom_addresses["Missable_Pokemon_Mansion_3F_Item_1"],
                     Missable(188)),
        LocationData("Pokemon Mansion 3F", "Item 2", "Iron", rom_addresses["Missable_Pokemon_Mansion_3F_Item_2"],
                     Missable(189)),
        LocationData("Pokemon Mansion B1F", "Item 1", "Rare Candy",
                     rom_addresses["Missable_Pokemon_Mansion_B1F_Item_1"], Missable(190)),
        LocationData("Pokemon Mansion B1F", "Item 2", "Full Restore",
                     rom_addresses["Missable_Pokemon_Mansion_B1F_Item_2"], Missable(191)),
        LocationData("Pokemon Mansion B1F", "Item 3", "TM14 Blizzard",
                     rom_addresses["Missable_Pokemon_Mansion_B1F_Item_3"], Missable(192)),
        LocationData("Pokemon Mansion B1F", "Item 4", "TM22 Solar Beam",
                     rom_addresses["Missable_Pokemon_Mansion_B1F_Item_4"], Missable(193)),
        LocationData("Pokemon Mansion B1F", "Item 5", "Secret Key",
                     rom_addresses["Missable_Pokemon_Mansion_B1F_Item_5"], Missable(194)),
        LocationData("Safari Zone East", "Item 1", "Full Restore", rom_addresses["Missable_Safari_Zone_East_Item_1"],
                     Missable(195)),
        LocationData("Safari Zone East", "Item 2", "Max Potion", rom_addresses["Missable_Safari_Zone_East_Item_2"],
                     Missable(196)),
        LocationData("Safari Zone East", "Item 3", "Carbos", rom_addresses["Missable_Safari_Zone_East_Item_3"],
                     Missable(197)),
        LocationData("Safari Zone East", "Item 4", "TM37 Egg Bomb", rom_addresses["Missable_Safari_Zone_East_Item_4"],
                     Missable(198)),
        LocationData("Safari Zone North", "Item 1", "Protein", rom_addresses["Missable_Safari_Zone_North_Item_1"],
                     Missable(199)),
        LocationData("Safari Zone North", "Item 2", "TM40 Skull Bash",
                     rom_addresses["Missable_Safari_Zone_North_Item_2"], Missable(200)),
        LocationData("Safari Zone West", "Item 1", "Max Potion", rom_addresses["Missable_Safari_Zone_West_Item_1"],
                     Missable(201)),
        LocationData("Safari Zone West", "Item 2", "TM32 Double Team",
                     rom_addresses["Missable_Safari_Zone_West_Item_2"], Missable(202)),
        LocationData("Safari Zone West", "Item 3", "Max Revive", rom_addresses["Missable_Safari_Zone_West_Item_3"],
                     Missable(203)),
        LocationData("Safari Zone West", "Item 4", "Gold Teeth", rom_addresses["Missable_Safari_Zone_West_Item_4"],
                     Missable(204)),
        LocationData("Safari Zone Center", "Item", "Nugget", rom_addresses["Missable_Safari_Zone_Center_Item"],
                     Missable(205), lambda state: state._pokemon_rb_can_surf(player)),
        LocationData("Cerulean Cave 2F", "Item 1", "PP Up", rom_addresses["Missable_Cerulean_Cave_2F_Item_1"],
                     Missable(206)),
        LocationData("Cerulean Cave 2F", "Item 2", "Ultra Ball", rom_addresses["Missable_Cerulean_Cave_2F_Item_2"],
                     Missable(207), lambda state: state._pokemon_rb_can_surf(player)),
        LocationData("Cerulean Cave 2F", "Item 3", "Full Restore", rom_addresses["Missable_Cerulean_Cave_2F_Item_3"],
                     Missable(208), lambda state: state._pokemon_rb_can_surf(player)),
        LocationData("Cerulean Cave B1F", "Item 1", "Ultra Ball", rom_addresses["Missable_Cerulean_Cave_B1F_Item_1"],
                     Missable(210)),
        LocationData("Cerulean Cave B1F", "Item 2", "Max Revive", rom_addresses["Missable_Cerulean_Cave_B1F_Item_2"],
                     Missable(211)),
        LocationData("Victory Road 1F", "Item 1", "TM43 Sky Attack", rom_addresses["Missable_Victory_Road_1F_Item_1"],
                     Missable(212)),
        LocationData("Victory Road 1F", "Item 2", "Rare Candy", rom_addresses["Missable_Victory_Road_1F_Item_2"],
                     Missable(213)),

        LocationData("Pewter Gym", "Brock 1", "Boulder Badge", rom_addresses['Badge_Pewter_Gym'], EventFlag(0x8A0)),
        LocationData("Cerulean Gym", "Misty 1", "Cascade Badge", rom_addresses['Badge_Cerulean_Gym'], EventFlag(0x8A1)),
        LocationData("Vermilion Gym", "Lt. Surge 1", "Thunder Badge", rom_addresses['Badge_Vermilion_Gym'], EventFlag(0x8A2)),
        LocationData("Celadon Gym", "Erika 1", "Rainbow Badge", rom_addresses['Badge_Celadon_Gym'], EventFlag(0x8A3)),
        LocationData("Fuchsia Gym", "Koga 1", "Soul Badge", rom_addresses['Badge_Fuchsia_Gym'], EventFlag(0x8A4)),
        LocationData("Saffron Gym", "Sabrina 1", "Marsh Badge", rom_addresses['Badge_Saffron_Gym'], EventFlag(0x8A5)),
        LocationData("Cinnabar Gym", "Blaine 1", "Volcano Badge", rom_addresses['Badge_Cinnabar_Gym'], EventFlag(0x8A6)),
        LocationData("Viridian Gym", "Giovanni 1", "Earth Badge", rom_addresses['Badge_Viridian_Gym'], EventFlag(0x8A7)),

        LocationData("Viridian Forest", "Hidden Item Northwest by Trainer", "Potion", rom_addresses['Hidden_Item_Viridian_Forest_1'], Hidden(0), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Viridian Forest", "Hidden Item Entrance Tree", "Antidote", rom_addresses['Hidden_Item_Viridian_Forest_2'], Hidden(1), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Mt Moon B2F", "Hidden Item Dead End Before Fossils", "Moon Stone", rom_addresses['Hidden_Item_MtMoonB2F_1'], Hidden(2), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 25", "Hidden Item Fence Outside Bill's House", "Ether", rom_addresses['Hidden_Item_Route_25_1'], Hidden(3), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 9", "Hidden Item Rock By Grass", "Ether", rom_addresses['Hidden_Item_Route_9'], Hidden(4), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("S.S. Anne 1F", "Hidden Item Kitchen Trash", "Great Ball", rom_addresses['Hidden_Item_SS_Anne_Kitchen'], Hidden(5), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("S.S. Anne B1F", "Hidden Item Under Pillow", "Hyper Potion", rom_addresses['Hidden_Item_SS_Anne_B1F'], Hidden(6), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 10 North", "Hidden Item Behind Rock Tunnel Entrance Bush", "Super Potion", rom_addresses['Hidden_Item_Route_10_1'], Hidden(7), lambda state: state._pokemon_rb_can_get_hidden_items(player) and state._pokemon_rb_can_cut(player)),
        LocationData("Route 10 South", "Hidden Item Rock", "Max Ether", rom_addresses['Hidden_Item_Route_10_2'], Hidden(8), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Rocket Hideout B1F", "Hidden Item Pot Plant", "PP Up", rom_addresses['Hidden_Item_Rocket_Hideout_B1F'], Hidden(9), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Rocket Hideout B3F", "Hidden Item Near Item", "Nugget", rom_addresses['Hidden_Item_Rocket_Hideout_B3F'], Hidden(10), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Rocket Hideout B4F", "Hidden Item Behind Giovanni", "Super Potion", rom_addresses['Hidden_Item_Rocket_Hideout_B4F'], Hidden(11), lambda state: state._pokemon_rb_can_get_hidden_items(player) and state.has("Lift Key", player)),
        LocationData("Pokemon Tower 5F", "Hidden Item Near West Staircase", "Elixir", rom_addresses['Hidden_Item_Pokemon_Tower_5F'], Hidden(12), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 13", "Hidden Item Dead End Boulder", "PP Up", rom_addresses['Hidden_Item_Route_13_1'], Hidden(13), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 13", "Hidden Item Dead End By Water Corner", "Calcium", rom_addresses['Hidden_Item_Route_13_2'], Hidden(14), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Pokemon Mansion B1F", "Hidden Item Secret Key Room Corner", "Rare Candy", rom_addresses['Hidden_Item_Pokemon_Mansion_B1F'], Hidden(15), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Safari Zone Gate", "Hidden Item", "Nugget", rom_addresses['Hidden_Item_Safari_Zone_Gate'], Hidden(16), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Safari Zone West", "Hidden Item Secret House Statue", "Revive", rom_addresses['Hidden_Item_Safari_Zone_West'], Hidden(17), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Silph Co 5F", "Hidden Item Pot Plant", "Elixir", rom_addresses['Hidden_Item_Silph_Co_5F'], Hidden(18), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Silph Co 9F", "Hidden Item Nurse Bed", "Max Potion", rom_addresses['Hidden_Item_Silph_Co_9F'], Hidden(19), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Copycat's House", "Hidden Item Desk", "Nugget", rom_addresses['Hidden_Item_Copycats_House'], Hidden(20), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Cerulean Cave 1F", "Hidden Item Center Rocks", "Rare Candy", rom_addresses['Hidden_Item_Cerulean_Cave_1F'], Hidden(21), lambda state: state._pokemon_rb_can_get_hidden_items(player) and state._pokemon_rb_can_surf(player)),
        LocationData("Cerulean Cave B1F", "Hidden Item Northeast Rocks", "Ultra Ball", rom_addresses['Hidden_Item_Cerulean_Cave_B1F'], Hidden(22), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Power Plant", "Hidden Item Central Dead End", "Max Elixir", rom_addresses['Hidden_Item_Power_Plant_1'], Hidden(23), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Power Plant", "Hidden Item Before Zapdos", "PP Up", rom_addresses['Hidden_Item_Power_Plant_2'], Hidden(24), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Seafoam Islands B2F", "Hidden Item Rock", "Nugget", rom_addresses['Hidden_Item_Seafoam_Islands_B2F'], Hidden(25), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Seafoam Islands B4F", "Hidden Item Corner Island", "Ultra Ball", rom_addresses['Hidden_Item_Seafoam_Islands_B4F'], Hidden(26), lambda state: state._pokemon_rb_can_get_hidden_items(player) and state._pokemon_rb_can_surf(player)),
        LocationData("Pokemon Mansion 1F", "Hidden Item Block Near Entrance Carpet", "Moon Stone", rom_addresses['Hidden_Item_Pokemon_Mansion_1F'], Hidden(27), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Pokemon Mansion 3F", "Hidden Item Behind Burglar", "Max Revive", rom_addresses['Hidden_Item_Pokemon_Mansion_3F'], Hidden(28), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 23 North", "Hidden Item Rocks Before Final Guard", "Full Restore", rom_addresses['Hidden_Item_Route_23_1'], Hidden(29), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 23 North", "Hidden Item East Tree After Water", "Ultra Ball", rom_addresses['Hidden_Item_Route_23_2'], Hidden(30), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 23 South", "Hidden Item On Island", "Max Ether", rom_addresses['Hidden_Item_Route_23_3'], Hidden(31), lambda state: state._pokemon_rb_can_get_hidden_items(player) and state._pokemon_rb_can_surf(player) and state.has("Soul Badge", player)),
        LocationData("Victory Road 2F", "Hidden Item Rock Before Moltres", "Ultra Ball", rom_addresses['Hidden_Item_Victory_Road_2F_1'], Hidden(32), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Victory Road 2F", "Hidden Item Rock In Final Room", "Full Restore", rom_addresses['Hidden_Item_Victory_Road_2F_2'], Hidden(33), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Vermilion City", "Hidden Item The Truck", "Full Restore", rom_addresses['Hidden_Item_Unused_6F'], Hidden(34), lambda state: state._pokemon_rb_can_get_hidden_items(player) and state._pokemon_rb_can_surf(player) and state.has("S.S. Ticket", player)),
        LocationData("Viridian City", "Hidden Item Cuttable Tree", "Potion", rom_addresses['Hidden_Item_Viridian_City'], Hidden(35), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 11", "Hidden Item Isolated Tree Near Gate", "Potion", rom_addresses['Hidden_Item_Route_11'], Hidden(36), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 12 West", "Hidden Item Tree Near Gate", "Hyper Potion", rom_addresses['Hidden_Item_Route_12'], Hidden(37), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 17", "Hidden Item In Grass", "Rare Candy", rom_addresses['Hidden_Item_Route_17_1'], Hidden(38), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 17", "Hidden Item Near Northernmost Sign", "Full Restore", rom_addresses['Hidden_Item_Route_17_2'], Hidden(39), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 17", "Hidden Item East Center", "PP Up", rom_addresses['Hidden_Item_Route_17_3'], Hidden(40), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 17", "Hidden Item West Center", "Max Revive", rom_addresses['Hidden_Item_Route_17_4'], Hidden(41), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 17", "Hidden Item Before Final Bridge", "Max Elixir", rom_addresses['Hidden_Item_Route_17_5'], Hidden(42), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Underground Tunnel North-South", "Hidden Item Near Northern Stairs", "Full Restore", rom_addresses['Hidden_Item_Underground_Path_NS_1'], Hidden(43), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Underground Tunnel North-South", "Hidden Item Near Southern Stairs", "X Special", rom_addresses['Hidden_Item_Underground_Path_NS_2'], Hidden(44), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Underground Tunnel West-East", "Hidden Item West", "Nugget", rom_addresses['Hidden_Item_Underground_Path_WE_1'], Hidden(45), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Underground Tunnel West-East", "Hidden Item East", "Elixir", rom_addresses['Hidden_Item_Underground_Path_WE_2'], Hidden(46), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Celadon City", "Hidden Item Dead End Near Cuttable Bush", "PP Up", rom_addresses['Hidden_Item_Celadon_City'], Hidden(47), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 25", "Hidden Item Northeast Of Grass", "Elixir", rom_addresses['Hidden_Item_Route_25_2'], Hidden(48), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Mt Moon B2F", "Hidden Item Lone Rock", "Ether", rom_addresses['Hidden_Item_MtMoonB2F_2'], Hidden(49), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Seafoam Islands B3F", "Hidden Item Rock", "Max Elixir", rom_addresses['Hidden_Item_Seafoam_Islands_B3F'], Hidden(50), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Vermilion City", "Hidden Item In Water Near Fan Club", "Max Ether", rom_addresses['Hidden_Item_Vermilion_City'], Hidden(51), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Cerulean City", "Hidden Item Gym Badge Guy's Backyard", "Rare Candy", rom_addresses['Hidden_Item_Cerulean_City'], Hidden(52), lambda state: state._pokemon_rb_can_get_hidden_items(player)),
        LocationData("Route 4", "Hidden Item Plateau East Of Mt Moon", "Great Ball", rom_addresses['Hidden_Item_Route_4'], Hidden(53), lambda state: state._pokemon_rb_can_get_hidden_items(player)),

        LocationData("Indigo Plateau", "Become Champion", "Become Champion", event=True),
        LocationData("Pokemon Tower 7F", "Fuji Saved", "Fuji Saved", event=True),
        LocationData("Silph Co 11F", "Silph Co Liberated", "Silph Co Liberated", rule=lambda state: state.has("Card Key", player), event=True)

    ]
    addresses = set()
    for i, location in enumerate(locations):
        if location.event or location.rom_address is None:
            location.address = None
        else:
            location.address = loc_id_start + i
            if location.rom_address in addresses:
                breakpoint()
            else:
                addresses.add(location.rom_address)
    return locations

class PokemonRBLocation(Location):
    game = "Pokemon Red - Blue"

    def __init__(self, player, name, address, rom_address, access_rule, item_rule):
        super(PokemonRBLocation, self).__init__(
            player, name,
            address
        )
        self.rom_address = rom_address
        self.access_rule = access_rule
        self.item_rule = item_rule