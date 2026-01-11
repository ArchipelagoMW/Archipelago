from BaseClasses import MultiWorld, Item, Entrance, EntranceType
from .data import LOCATIONS_DATA
from .data.LogicPredicates import *
from .Options import PhantomHourglassOptions
from .data.Entrances import ENTRANCES
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Subclasses import PHRegion

def make_overworld_logic():
    overworld_logic = [

        # Randomized start
        ["menu", "mercay sw", False, None],

        # ====== Mercay Island ==============

        ["mercay sw", "mercay dig spot", False, "shovel"],
        ["mercay oshus", "mercay oshus gem", False, "oshus_gem"],
        ["mercay oshus", "mercay oshus phantom blade", False, "can_make_phantom_sword"],
        ["mercay oshus phantom blade", "mercay oshus gem", False, None],
        ["mercay sw", "mercay sw bridge", True, None],
        ["mercay sw", "mercay oshus", True, None],
        ["mercay sw", "mercay apricot", True, None],
        ["mercay sw", "mercay sword cave", True, None],
        ["mercay sw", "mercay nw chus", True, False],

        ["mercay sw bridge", "mercay se", True, None],
        ["mercay se", "mercay tuzi", True, None],
        ["mercay se", "mercay milk bar", True, None],
        ["mercay se", "mercay shop", True, None],
        ["mercay shop", "island shop", False, None],
        ["mercay se", "mercay shipyard", False, "has", "_beat_tof"],
        ["mercay shipyard", "mercay se", False, None],
        ["mercay se", "mercay treasure teller", False, "courage_crest"],
        ["mercay treasure teller", "mercay se", False, None],
        ["mercay se", "mercay yellow guy", False, "courage_crest"],
        ["mercay se", "mercay ne", True, False],
        ["mercay se ledge", "mercay se", False, None],

        ["mercay nw chus", "mercay nw bamboo", True, "can_cut_bamboo"],
        ["mercay nw temple", "mercay geozard cave north", False, "explosives"],
        ["mercay geozard cave north", "mercay nw temple", False, None],
        ["mercay geozard cave north", "mercay geozard cave south", False, "bow"],
        ["mercay geozard cave south", "mercay ne ledge", True, None],
        ["mercay nw temple", "totok", True, None],

        ["mercay ne", "mercay freedle tunnel", False, "explosives"],
        ["mercay freedle tunnel", "mercay ne", False, None],
        ["mercay freedle tunnel", "mercay freedle island", True, None],
        ["mercay freedle island", "mercay ne", False, None],
        ["mercay freedle tunnel", "mercay freedle tunnel chest", False, "range"],
        ["mercay freedle island", "mercay freedle gift", False, "sea_chart", "SE"],
        ["mercay ne", "mercay nw temple", True, None],
        ["mercay ne ledge", "mercay ne", False, None],
        ["mercay ne ledge", "mercay se ledge", True, None],

        ["mercay nw temple", "mercay nw oob high", False, "scroll_clip"],
        ["mercay nw oob high", "mercay nw temple", False, None],
        ["mercay nw oob high", "mercay nw oob low", False, None],
        ["mercay nw oob low", "mercay nw chus", False, None],
        ["mercay nw oob low", "mercay nw bamboo", False, None],
        ["mercay nw oob high", "mercay ne oob", True, None],
        ["mercay nw oob high", "mercay sw oob high", True, None],
        ["mercay nw oob high", "mercay sw oob east", True, None],
        ["mercay nw oob low", "mercay sw oob low", True, None],

        ["mercay sw oob high", "mercay sw oob low", False, None],
        ["mercay sw oob low", "mercay sw", False, None],
        ["mercay sw oob east", "mercay sw bridge", False, None],
        ["mercay sw oob east", "mercay se oob", True, None],

        ["mercay se oob", "mercay se ledge", False, None],
        ["mercay se oob", "mercay ne oob", True, None],
        ["mercay ne oob", "mercay ne ledge", False, None],

        # ======== Mountain Passage =========

        ["mercay nw bamboo", "mercay passage 1", True, None],
        ["mercay passage 1", "mercay passage 2", False, "can_reach_mp2"],
        ["mercay passage 2 exit", "mercay passage 2", False, "can_reach_mp2_top"],
        ["mercay passage 1", "mercay passage 2 exit", False, "mp2_bypass_fore"],
        ["mercay passage 2 exit", "mercay passage 1", False, "mp2_bypass"],
        ["mercay passage 2 exit", "mercay passage 3", True, None],
        ["mercay passage 3", "mercay passage rat", False, "mp_rat"],
        ["mercay passage 3", "mercay passage 4", False, "mp3"],
        ["mercay passage 4", "mercay passage 3", False, "mp3_back"],
        ["mercay passage 4", "mercay se", True, None],
        ["mercay passage 4", "mercay passage 1", False, "hard_logic"],  # Savewarp

        # ========== TotOK ===================
        ["totok", "totok 1f", False, "totok_1f"],

        ["totok 1f", "totok 1f chest", False, "totok_1f_chest"],
        ["totok 1f", "totok 1f chart", False, "totok_1f_chart"],
        ["totok 1f", "totok b1", False, "totok_b1"],

        ["totok b1", "totok b1 key", False, "totok_b1_key"],
        ["totok b1", "totok b1 phantom", False, "totok_b1_phantom"],
        ["totok b1", "totok b1 bow", False, "totok_b1_bow"],
        ["totok b1", "totok b2", False, "totok_b2"],

        ["totok b2", "totok b2 key", False, "totok_b2_key"],
        ["totok b2", "totok b2 phantom", False, "totok_b2_phantom"],
        ["totok b2", "totok b2 chu", False, "totok_b2_chu"],
        ["totok b2", "totok b3", False, "totok_b3"],

        ["totok b3", "totok b3 nw", False, "totok_b3_nw"],
        ["totok b3", "totok b3 se", False, "totok_b3_se"],
        ["totok b3", "totok b3 sw", False, "totok_b3_sw"],
        ["totok b3", "totok b3 bow", False, "totok_b3_bow"],
        ["totok b3", "totok b3 key", False, "totok_b3_key"],
        ["totok b3", "totok b3 phantom", False, "totok_b3_phantom"],
        ["totok b3", "totok b35", False, "totok_b35"],

        ["totok b35", "totok b4", False, "totok_b4"],
        ["totok b4", "totok b4 key", False, "totok_b4_key"],
        ["totok b4", "totok b4 eyes", False, "totok_b4_eyes"],
        ["totok b4", "totok b4 phantom", False, "totok_b4_phantom"],
        ["totok b4", "totok b5", False, "totok_b5"],
        ["totok b4", "totok b5 alt", False, "totok_b5_alt"],

        ["totok b5", "totok b5 chest", False, "totok_b5_chest"],
        ["totok b5", "totok b6", False, "totok_b6"],
        ["totok b5 alt", "totok b5 alt chest", False, "totok_b5_alt_chest"],
        ["totok b5 alt", "totok b6", False, "totok_b6"],

        ["totok b6", "totok b6 bow", False, "totok_b6_bow"],
        ["totok b6", "totok b6 phantom", False, "totok_b6_phantom"],
        ["totok b6", "totok b6 crest", False, "totok_b6_crest"],
        ["totok b6", "totok midway", False, "totok_b7"],
        ["totok midway", "totok b7", False, "spirit", "Courage"],

        ["totok b7", "totok b7 crystal", False, "totok_b7_crystal"],
        ["totok b7", "totok b7 switch", False, "totok_b7_switch_chest"],
        ["totok b7", "totok b8", False, "totok_b8"],

        ["totok b8", "totok b8 phantom", False, "totok_b8_phantom"],
        ["totok b8", "totok b9", False, "totok_b9"],
        ["totok b8", "totok b8 2c chest", False, "totok_b8_2_crystal_chest"],
        ["totok b8", "totok b7 phantom", False, "totok_b7_phantom"],
        ["totok b8", "totok b9 corner chest", False, "totok_b9_corner_chest"],

        ["totok b9", "totok b9 phantom", False, "totok_b9_phantom"],
        ["totok b9", "totok b9 ghosts", False, "totok_b9_ghosts"],

        ["totok b9", "totok b95", False, "totok_b10"],
        ["totok b95", "totok b10", True, None],

        ["totok b10", "totok b10 key", False, "totok_b10_key"],
        ["totok b10", "totok b10 phantom", False, "totok_b10_phantom"],
        ["totok b10", "totok b10 eye", False, "totok_b10_eye"],
        ["totok b10", "totok b10 hammer", False, "totok_b10_hammer"],
        ["totok b10", "totok b11", False, "totok_b11"],

        ["totok b11", "totok b11 phantom", False, "totok_b11_phantom"],
        ["totok b11", "totok b11 eyes", False, "totok_b11_eyes"],
        ["totok b11", "totok b12", False, "totok_b12"],

        ["totok b12", "totok b12 nw", False, "totok_b12_nw"],
        ["totok b12", "totok b12 ne", False, "totok_b12_ne"],
        ["totok b12", "totok b12 phantom", False, "totok_b12_phantom"],
        ["totok b12", "totok b12 ghost", False, "totok_b12_ghost"],
        ["totok b12", "totok b12 hammer", False, "totok_b12_hammer"],
        ["totok b12", "totok b13", False, "totok_b13"],

        ["totok b13", "totok b13 chest", False, "totok_b13_chest"],
        ["totok b13", "totok before bellum", False, "b13_door"],
        ["totok", "totok before bellum", False, "bellum_warp"],
        # Bellum
        ["totok before bellum", "bellum 1", False, "bellum_staircase"],
        ["bellum 1", "ghost ship fight", False, "can_beat_bellum"],
        ["ghost ship fight", "bellumbeck", False, "can_beat_ghost_ship_fight"],

        # ============ Shops ====================

        ["island shop", "shop power gem", False, "can_buy_gem"],
        ["island shop", "shop quiver", False, "can_buy_quiver"],
        ["island shop", "shop bombchu bag", False, "can_buy_chu_bag"],
        ["island shop", "shop heart container", False, "can_buy_heart"],

        ["sw ocean east", "beedle", False, None],
        ["sw ocean west", "beedle", False, None],
        ["nw ocean", "beedle", False, None],
        ["se ocean", "beedle", False, None],
        ["ne ocean", "beedle", False, None],
        ["beedle", "beedle gem", False, "beedle_shop", 500],
        ["beedle", "beedle bomb bag", False, "can_buy_bomb_bag"],
        ["beedle", "masked ship gem", False, "beedle_shop", 500],
        ["beedle", "masked ship hc", False, "beedle_shop", 500],

        ["beedle", "beedle bronze", False, "can_get_beedle_bronze"],
        ["beedle", "beedle silver", False, "has_beedle_points", 20],
        ["beedle", "beedle gold", False, "has_beedle_points", 50],
        ["beedle", "beedle plat", False, "has_beedle_points", 100],
        ["beedle", "beedle vip", False, "has_beedle_points", 200],


        # ============ SW Ocean =================

        ["mercay se", "mercay boat", False, "boat_access"],
        ["mercay boat", "mercay se", False, None],
        ["mercay boat", "sw ocean east", True, "require_chart", "SW"],
        ["cannon boat", "cannon island", True, None],
        ["cannon boat", "sw ocean east", True, "require_chart", "SW"],
        ["ember boat", "ember port", True, None],
        ["ember boat", "sw ocean east", True, "require_chart", "SW"],
        ["sw ocean east", "sw ocean crest salvage", False, "salvage_courage_crest"],
        ["sw ocean east", "sw ocean west", False, "cannon"],
        ["sw ocean west", "sw ocean east", False, "cannon"],
        ["molida boat", "molida island", True, None],
        ["molida boat", "sw ocean west", True, "require_chart", "SW"],
        ["spirit boat", "spirit island", True, None],
        ["spirit boat", "sw ocean west", True, "require_chart", "SW"],
        ["sw ocean west", "sw ocean nyave", False, "nyave_fight"],
        ["sw ocean nyave", "sw ocean nyave trade", False, "guard_notebook"],
        ["sw ocean west", "sw ocean frog phi", False, "cannon"],
        ["sw ocean east", "sw ocean frog x", False, "cannon"],
        ["sw ocean west", "frog warps", False, None],
        ["sw ocean east", "frog warps", False, None],

        # ============= Frog Warps ==================
        ["frog warps", "sw ocean west", False, "frog_phi"],
        ["frog warps", "sw ocean east", False, "frog_x"],
        ["frog warps", "nw ocean", False, "frog_n"],
        ["frog warps", "ne ocean", False, "frog_square"],
        ["frog warps", "se ocean", False, "frog_se"],

        # ============ Cannon Island ===============

        ["cannon island", "cannon fuzo", True, None],
        ["cannon island", "cannon island dig", False, "shovel"],
        ["cannon island", "cannon cave south", True, None],
        ["cannon cave south", "cannon cave north", False, None],
        ["cannon cave north", "cannon bomb garden", True, None],
        ["cannon bomb garden", "cannon outside eddo", False, None],
        ["cannon outside eddo", "cannon bomb garden", False, "explosives"],
        ["cannon bomb garden", "cannon island", False, None],
        ["cannon outside eddo", "cannon island", False, "glitched_logic"],
        ["cannon outside eddo", "cannon eddo", True, None],
        ["cannon fuzo", "cannon eddo", True, "has", "_eddo_door"],
        ["cannon eddo", "cannon island salvage arm", False, "courage_crest"],
        ["cannon bomb garden", "cannon bomb garden dig", False, "shovel"],

        # =============== Isle of Ember ================

        # ER
        ["ember port", "ember astrid", True, None],
        ["ember astrid", "ember astrid basement", True, None],
        ["ember astrid basement", "ember astrid basement dig", False, "spade"],
        ["ember port", "ember kayo", True, None],
        ["ember port", "ember port house", True, None],
        ["ember astrid", "ember astrid post tof", False, "has", "_beat_tof"],

        ["ember port", "ember grapple", False, "ember_grapple"],
        ["ember grapple", "ember port", False, "grapple"],
        ["ember grapple", "ember coast north", True, "grapple"],

        ["ember coast north", "ember coast east", True, None],
        ["ember port", "ember coast east", True, None],
        ["ember climb west", "ember coast east", True, None],
        ["ember climb west", "ember outside tof", True, None],
        ["ember outside tof", "tof 1f", True, None],
        ["ember summit west", "ember outside tof", True, None],
        ["ember summit west", "ember summit east", True, None],
        ["ember outside tof", "ember outside tof dig", False, "shovel"],

        ["ember summit west", "ember climb west", False, None],
        ["ember summit east", "ember outside tof", False, None],
        ["ember climb west", "ember port", False, None],
        ["ember outside tof", "ember coast east", False, None],

        ["ember climb east", "ember coast east", True, None],
        ["ember summit north", "ember summit east", True, None],
        ["ember climb east", "ember port", True, None],
        ["ember summit north", "ember summit west", True, None],



        # =============== Temple of Fire =================

        ["tof 1f", "tof 1f keese", False, "can_kill_bat"],
        ["tof 1f", "tof 1f maze", False, "tof_maze"],
        ["tof 1f maze", "tof 2f", False, "can_hit_spin_switches"],
        # 2F
        ["tof 2f", "tof 1f west", False, "short_range"],
        ["tof 1f west", "tof 1f sw", False, "can_hit_spiral_wall_switches"],
        ["tof 1f sw", "tof 2f south", False, "can_kill_bubble"],
        ["tof 2f south", "tof 3f", False, "tof_3f"],
        # 3F
        ["tof 3f", "tof 3f key drop", False, "tof_key_drop"],
        ["tof 3f", "tof 3f key door", False, "tof_3f_key_door"],
        ["tof 3f key door", "tof 3f boss key", False, "boomerang"],
        ["tof 3f key door", "tof before blaaz", False, "tof_bk"],  # Includes UT
        ["tof before blaaz", "tof blaaz", True, None],
        ["tof blaaz", "post blaaz", False, "tof_blaaz"],
        ["post blaaz", "post tof", False, "tof_blaaz"],  # Used for events

        # =========== Molida Island ===============

        ["molida island", "molida dig", False, "spade"],
        ["molida island", "molida port house", True, None],
        ["molida island", "molida potato house", True, None],
        ["molida island", "molida shop", True, None],
        ["molida shop", "island shop", False, None],
        ["molida island", "molida romaros", True, None],
        ["molida romaros", "molida archery", False, "has", "_beat_toc"],
        ["molida island", "molida cave", True, None],
        ["molida island", "molida cave upper", False, "shovel"],

        ["molida cave upper", "molida cave", False, None],
        ["molida cave", "molida cave grapple", False, "grapple"],
        ["molida cave", "molida cave geozard", False, None],
        ["molida cave geozard", "molida cave geozard dig", False, "shovel"],
        ["molida cave geozard", "molida cave post geozard", False, "cave_damage"],
        ["molida cave post geozard", "molida cave octos", True, None],
        ["molida cave", "molida cave back", False, "bombs"],
        ["molida cave back", "molida cave", False, None],
        ["molida cave back", "molida cave octos", True, None],
        ["molida cave back", "molida shovel cave", True, None],
        ["molida shovel cave", "molida shovel cave dig", False, "shovel"],
        ["molida cave back", "molida cliff north", True, None],

        ["molida cliff north", "molida cliff south", True, None],
        ["molida cliff south", "molida island", False, None],
        ["molida cliff south", "molida cuccoo dig", False, "cuccoo_dig"],

        ["molida cave upper", "molida cave sun door", True, "sun_key"],
        ["molida north", "molida cave drop", False, "shovel"],
        ["molida cave drop", "molida cave sun door", False, None],
        ["molida cave sun door", "molida north", True, None],
        ["molida north", "molida north grapple", False, "grapple"],
        ["molida north", "toc gates", False, "enter_toc"],
        ["toc gates", "toc", True, None],

        # =============== Temple of Courage ================

        ["toc", "toc bomb alcove", False, "boom"],
        ["toc", "toc b1", False, "toc_door_1"],
        ["toc", "toc hammer clips", False, "hammer_clip"],
        ["toc b1", "toc b1 grapple", False, "toc_grapple"],
        ["toc b1", "toc 1f west", False, "toc_1f_west"],
        ["toc b1 grapple", "toc 1f west", False, "bow"],
        ["toc hammer clips", "toc 1f west", False, None],
        ["toc 1f west", "toc map room", False, "boom"],
        ["toc 1f west", "toc 2f beamos", False, "toc_door_2"],
        ["toc 1f west", "toc b1 maze", False, "shape_crystal", "Temple of Courage", "Square", "North"],
        ["toc 2f beamos", "toc b1 maze", False, "ut_pedestals_vanilla"],  # UT Crystal
        ["toc 2f beamos", "toc south 1f", False, "toc_beamos_ut"],  # UT Crystal South
        ["toc b1 grapple", "toc b1 maze", False, None],
        ["toc b1 maze", "toc south 1f", False, "toc_crystal_south"],

        ["toc south 1f", "toc 2f spike corridor", False, "boom"],
        ["toc 2f spike corridor", "toc 2f platforms", False, "toc_spike_corridor"],
        ["toc hammer clips", "toc 2f spike corridor", False, None],
        ["toc south 1f", "toc 2f platforms", False, "bow"],
        ["toc 2f spike corridor", "toc torches", False, "boomerang"],
        ["toc torches", "toc torches chest", False, "bow"],
        ["toc torches", "toc pols 2", False, "toc_switch_state"],
        ["toc pols 2", "toc bk room", False, "toc_door_3"],
        ["toc bk room", "toc bk chest", False, "bow"],
        ["toc bk room", "toc before boss", False, "toc_boss_key"],
        ["toc bk chest", "toc before boss", False, "simple_boss_key", "Temple of Courage"],
        ["toc before boss", "toc before boss chest", False, "boom"],
        ["toc before boss", "toc crayk", True, None],
        ["toc crayk", "post crayk", False, "bow"],
        ["post crayk", "post toc", False, None],  # Used for events

        # ================ Spirit Island =====================

        ["spirit island", "spirit island gauntlet", False, "grapple"],
        ["spirit island", "spirit cave", True, None],
        ["spirit cave", "spirit power 1", False, "spirit_gems", "Power", 10],
        ["spirit cave", "spirit power 2", False, "spirit_gems",  "Power", 20],
        ["spirit cave", "spirit wisdom 1", False, "spirit_gems",  "Wisdom", 10],
        ["spirit cave", "spirit wisdom 2", False, "spirit_gems",  "Wisdom", 20],
        ["spirit cave", "spirit courage 1", False, "spirit_gems",  "Courage", 10],
        ["spirit cave", "spirit courage 2", False, "spirit_gems",  "Courage", 20],

        # ============ Ocean NW ===============
        ["sw ocean west", "nw ocean", False, "sea_chart", "NW"],
        ["nw ocean", "sw ocean west", False, "sea_chart", "SW"],
        ["nw ocean", "sw ocean east", False, "sea_chart", "SW"],
        ["nw ocean", "frog warps", False, None],
        ["nw ocean", "nw ocean frog n", False, "cannon"],
        ["gust boat", "gust south", True, None],
        ["gust boat", "nw ocean", True, "require_chart", "NW"],
        ["bannan boat", "bannan", True, None],
        ["bannan boat", "nw ocean", True, "require_chart", "NW"],
        ["zauz boat", "zauz", True, None],
        ["zauz boat", "nw ocean", True, "require_chart", "NW"],
        ["uncharted boat", "uncharted", True, None],
        ["uncharted boat", "nw ocean", True, "require_chart", "NW"],
        ["nw ocean", "ghost ship deck", False, "ghost_ship"],
        ["ghost ship deck", "nw ocean", False, None],
        ["nw ocean", "porl", False, None],
        ["porl", "porl item", False, "sword"],
        ["porl", "porl trade", False, "heroes_new_clothes"],

        # ================= Isle of Gust ====================

        ["gust south", "gust hideout", True, None],
        ["gust south", "gust cave", True, None],
        ["gust cave", "gust cave damage", False, "cave_damage"],
        ["gust cave", "gust cliffs", True, None],
        ["gust cliffs", "gust south", False, None],
        ["gust cliffs", "gust cliffs dig", False, "shovel"],
        ["gust cliffs", "gust temple road", True, None],
        ["gust cliffs", "gust above temple", True, None],
        ["gust above temple", "gust west", True, None],
        ["gust west", "gust west chest", False, "shovel"],
        ["gust west", "gust west ledge", False, "shovel"],
        ["gust west ledge", "gust west", False, None],
        ["gust west ledge", "gust nw", True, None],
        ["gust nw", "gust nw dig", False, "shovel"],
        ["gust nw", "gust sandworms", True, "shovel"],
        ["gust sandworms", "gust above temple", True, "has", "_windmills"],
        ["gust above temple", "gust temple road", False, None],
        ["gust temple road", "gust outside temple", False,  "has", "_windmills"],
        ["gust outside temple", "gust temple road", False, None],
        ["gust outside temple", "tow", True, None],

        # ================= Temple of Wind ====================

        ["tow", "tow b1", False, "tow_b1"],
        ["tow b1", "tow b2", False, None],
        ["tow b2", "tow b2 dig", False, "shovel"],
        ["tow b2", "tow b2 bombs", False, "explosives"],
        ["tow b2", "tow b2 key", False, "tow_key"],
        ["tow b2", "tow bk chest", False, "bombs"],
        ["tow", "tow before boss", False, "tow_cyclok"],
        ["tow before boss", "tow cyclok", True, None],
        ["tow cyclok", "post cyclok", False, None],
        ["post cyclok", "post tow", False, None],

        # ================= Bannan Island ====================

        ["bannan", "bannan grapple", False, "grapple"],
        ["bannan", "bannan dig", False, "shovel"],
        ["bannan", "bannan wayfarer", True, None],
        ["bannan", "bannan cave west", True, None],
        ["bannan cave west", "bannan cave east", True, "bombs"],
        ["bannan cave east", "bannan east", True, None],
        ["bannan east", "bannan east grapple", False, "grapple"],
        ["bannan east grapple", "bannan east grapple dig", False, "shovel"],
        ["bannan east", "bannan cannon game", False, "cannon"],
        ["bannan wayfarer", "bannan scroll", False, "bannan_scroll"],
        ["bannan wayfarer", "bannan loovar", False, "loovar"],
        ["bannan wayfarer", "bannan rsf", False, "rsf"],
        ["bannan wayfarer", "bannan neptoona", False, "neptoona"],
        ["bannan wayfarer", "bannan stowfish", False, "stowfish"],
        ["bannan wayfarer", "bannan letter", False, "jolene_letter"],

        # ================= Zauz's Island ====================

        ["zauz", "zauz dig", False, "shovel"],
        ["zauz", "zauz house", True, None],
        ["zauz house", "zauz blade", False, "has_zauz_required_metals"],
        ["zauz house", "zauz crest", False, "has", "_beat_ghost_ship"],

        # ================= Uncharted Island ====================

        ["uncharted", "uncharted dig", False, "shovel"],
        ["uncharted", "uncharted outside cave", False, "sword"],
        ["uncharted outside cave", "uncharted cave", True, None],
        ["uncharted cave", "uncharted inner cave", True, None],
        ["uncharted cave", "uncharted grapple", False, "grapple"],

        # ================= Ghost Ship ====================

        ["ghost ship deck", "ghost ship", True, None],
        ["ghost ship", "ghost ship barrel", False, "gs_barrel"],
        ["ghost ship barrel", "ghost ship b2", False, "gs_triangle"],
        ["ghost ship b2", "ghost ship b2 chests", False, "can_hit_switches"],
        ["ghost ship b2 chests", "ghost ship b3", False, "can_kill_bat"],
        ["ghost ship b3", "ghost ship cubus", True, None],
        ["ghost ship cubus", "ghost ship post cubus", False, "sword"],
        ["ghost ship b2", "ghost ship tetra", False, "ghost_key"],
        ["ghost ship tetra", "spawn pirate ambush", False, None],

        # ================= SE Ocean ====================

        ["sw ocean east", "se ocean", False, "se_ocean"],
        ["se ocean", "sw ocean east", False, "sea_chart", "SW"],
        ["se ocean", "frog warps", False, None],
        ["se ocean", "se ocean frogs", False, "cannon"],
        ["se ocean", "goron boat", False, "can_pass_sea_monsters"],
        ["goron boat", "se ocean", False, "require_chart", "SE"],
        ["goron sw", "goron boat", True, None],
        ["se ocean", "se ocean trade", False, "kaleidoscope"],
        ["se ocean", "frost boat", False, "can_pass_sea_monsters"],
        ["frost boat", "se ocean", False, "require_chart", "SE"],
        ["frost boat", "frost", True, None],
        ["harrow boat", "harrow", True, None],
        ["harrow boat", "se ocean", True, "require_chart", "SE"],
        ["ds boat", "ds", True, None],
        ["ds boat", "se ocean", True, "require_chart", "SE"],
        ["se ocean", "pirate ambush", False, "beat_gs"],

        # ================= Goron Island ====================

        ["goron sw", "goron port house", True, None],
        ["goron sw", "goron shop", True, None],
        ["goron shop", "island shop", False, None],
        ["goron sw", "goron rock house", True, None],
        ["goron sw", "goron chu house", True, None],
        ["goron sw", "goron shortcut", True, None],
        ["goron chu ledge", "goron chus", False, "goron_chus"],
        ["goron chu ledge", "goron grapple", False, "grapple"],
        ["goron sw", "goron se", True, None],
        ["goron chu ledge", "goron sw", False, None],
        ["goron se", "goron chu ledge", True, None],
        ["goron se", "goron mountain house", True, None],
        ["goron se", "goron se house", True, None],
        ["goron se", "goron chief house", True, None],
        ["goron chief house", "goron quiz", False, "has", "_goron_chus"],
        ["goron quiz", "goron chief 2", False, "has", "_beat_gt"],
        ["goron se", "goron ne", True, None],

        ["goron ne", "goron maze south", False, None],
        ["goron maze south", "goron ne", False, "explosives"],
        ["goron maze south", "goron maze south dead end", True, None],
        ["goron ne", "goron maze north", False, None],
        ["goron ne", "goron maze chu chest", False, "bombchu_switches"],
        ["goron maze north", "goron ne", False, "explosives"],
        ["goron maze north", "goron maze nw", True, "explosives"],
        ["goron maze north", "goron maze north dead end", True, None],
        ["goron maze nw", "goron like like", True, None],
        ["goron like like", "goron outside temple", False, "damage"],
        ["goron like like", "goron maze spikes", True, None],
        ["goron maze spikes", "goron maze spike chest", False, "has", "_goron_maze_switch"],
        ["goron outside temple", "goron like like", False, "clever_bombs"],  # Hard logic

        ["goron shortcut", "goron outside temple", False, "hammer_clip"],
        ["goron outside temple", "goron shortcut", False, None],
        ["goron outside temple", "gt", True, None],

        # ================= Goron Temple ====================
        ["gt", "gt 2", False, "goron_entrance"],
        ["gt 2", "gt bow", False, "bow"],
        ["gt 2", "gt b1", False, "gt_b1"],
        ["gt b1", "gt b2", False, "bombchu_switches"],
        ["gt b2", "gt b3", False, None],
        ["gt b2", "gt b2 back", False, "gt_b2_back"],
        ["gt b2 back", "gt bk chest", False, "chus"],
        ["gt b2", "gt before dongo", False, "gt_enter_dongo"],
        ["gt before dongo", "gt dongo", True, None],
        ["gt dongo", "post dongo", False, "gt_dongo"],
        ["post dongo", "post gt", False, None],

        # ================= Harrow Island ====================

        ["harrow", "harrow sword", False, "sword"],
        ["harrow sword", "harrow dig", False, "shovel"],
        ["harrow dig", "harrow dig 2", False, "sea_chart", "NE"],

        # ================= Dee Ess Island ====================

        ["ds", "ds dig", False, "shovel"],
        ["ds", "ds combat", False, "can_kill_eye_brute"],
        ["ds", "ds race", False, "has", "_beat_gt"],

        # ================= Isle of Frost ====================

        ["frost", "frost grapple", False, "grapple"],
        ["frost", "frost dig", False, "spade"],
        ["frost", "frost smart house", True, None],
        ["frost", "frost sensitive house", True, None],
        ["frost", "frost chief house", True, None],
        ["frost", "frost estate", True, None],
        ["frost", "frost cave", True, None],

        ["frost estate", "frost fofo", True, None],
        ["frost estate", "frost kumu", True, None],
        ["frost estate", "frost dobo", True, None],
        ["frost estate", "frost gumo", True, None],
        ["frost estate", "frost aroo", True, None],
        ["frost estate", "frost mazo", True, None],
        ["frost estate", "frost estate dig", False, "shovel"],
        ["frost estate dig", "frost estate grapple dig", False, "grapple"],

        ["frost cave", "frost field", True, None],
        ["frost field", "frost field exit", False, "ice_field"],
        ["frost field", "frost field upper se", False, "grapple"],
        ["frost field upper se", "frost field", False, None],
        ["frost field upper se", "frost field upper chests", False, "grapple"],
        ["frost field upper se", "frost field east ledge", False, None],
        ["frost field upper se", "frost field upper north", True, "grapple"],
        ["frost field upper se", "frost field exit", False, None],
        ["frost field upper north", "frost field", False, None],
        ["frost field upper north", "frost field exit", False, None],
        ["frost field upper north", "frost above temple west", True, None],
        ["frost field upper se", "frost above temple east", True, None],
        ["frost field exit", "frost outside arena", True, None],

        ["frost above temple east", "frost outside arena", False, None],
        ["frost above temple west", "frost outside arena", False, None],
        ["frost outside arena", "frost arena", False, None],
        ["frost arena", "frost outside arena", False, "dark_yook"],
        ["frost arena", "frost outside temple", False, "dark_yook"],
        ["frost arena", "frost above temple west", False, "grapple"],
        ["frost outside temple", "frost arena", False, None],
        ["frost outside temple", "toi", True, None],

        # ================= Ice Temple ====================

        ["toi", "toi 1f ascent", False, "toi_2f"],
        ["toi 1f ascent", "toi 2f right", True, None],
        ["toi 3f right", "toi 2f right", True, None],
        ["toi 3f right", "toi 3f", False, "toi_3f"],
        ["toi 3f", "toi 3f right", False, "range"],
        ["toi 3f", "toi 3f key door", True, "toi_key_door_1"],  # TODO: Key logic
        ["toi 3f", "toi 3f switch state", False, "bombs"],  # TODO: Switch state logic
        ["toi 3f switch state", "toi 3f boomerang key", False, "toi_3f_boomerang"],
        ["toi 3f key door", "toi 2f arena", True, None],
        ["toi 2f arena", "toi 2f post arena", False, "dark_yook"],
        ["toi 2f arena", "toi 2f left", False, "toi_miniboss"],
        ["toi 2f left", "toi 1f beetles", True, None],
        ["toi 1f beetles", "toi 1f shortcut", False, "grapple"],
        ["toi 1f shortcut", "toi 1f beetles", False, "grapple_glitch"],
        ["toi", "toi 1f shortcut", False, "hammer_clip"],
        ["toi 1f shortcut", "toi", False, None],
        ["toi 1f shortcut", "toi 1f descent", False, "grapple"],
        ["toi 1f descent", "toi b1 ascent", True, None],

        ["toi b1 ascent", "toi b1 shore", False, None],  # TODO: Switch state logic
        ["toi b1 shore", "toi b1 ascent", False, "hammer_clip"],
        ["toi b1 shore", "toi b1 south", False, "toi_b1"],
        ["toi b1 south", "toi b1 shore", False, None],
        ["toi b1 south", "toi b1 mid", True, "explosives"],
        ["toi b1 mid", "toi b1 right", False, "grapple"],
        ["toi b1 right", "toi b1 switch", False, "hammer_clip"],
        ["toi b1 right", "toi b1 switch room", False, "toi_key_door_2"],  # TODO: Key logic, and also backwards switch logic?
        ["toi b1 switch room", "toi b1 switch", False, "toi_b1_switch"],
        ["toi b1 mid", "toi b1 boss door", False, "toi_b2"],
        ["toi b1 boss door", "toi b1 mid", False, "grapple"],  # TODO: Switch state red
        ["toi b1 boss door", "toi b1 before boss", True, "toi_boss_door"],  # TODO: do ER logic
        ["toi b1 before boss", "gleeok", True, None],
        ["gleeok", "beat gleeok", False, "grapple"],
        ["beat gleeok", "post toi", False, None],
        ["toi b1 before boss", "toi blue warp", True, None],
        ["toi", "toi blue warp", True, "has", "_toi_blue_warp"],
        ["toi b1 boss door", "toi b2", True, None],

        ["toi b2", "toi b2 north", False, "toi_b2_north"],
        ["toi b2 north", "toi b2 bk chest", False, "hammer_clip"],
        ["toi b2 north", "toi b2 east", False, None],
        ["toi b2 east", "toi b2 bow", False, "bow"],
        ["toi b2 east", "toi b2 east arena", False, "toi_key_doors", 3, 3],  # TODO: Key logic
        ["toi b2 east arena", "toi b2 bk chest", False, None],

        # ================= NE Ocean ====================

        ["se ocean", "ne ocean", False, "sea_chart", "NE"],
        ["ne ocean", "se ocean", False, "sea_chart", "SE"],
        ["ne ocean", "frog warps", False, None],
        ["ne ocean", "ne ocean frog", False, "cannon"],
        ["ne ocean", "ne ocean combat", False, "can_kill_blue_chu"],
        ["dead boat", "iotd port", True, None],
        ["dead boat", "ne ocean", True, "require_chart", "NE"],
        ["maze boat", "maze", True, None],
        ["maze boat", "ne ocean", True, "require_chart", "NE"],
        ["ne ocean inner", "ruins boat", True, "require_chart", "NE"],
        ["ruins boat", "ruins port", True, None],
        ["ne ocean", "pirate ambush", False, "beat_gs"],

        # ================= IotD ====================

        ["iotd port", "iotd cave", True, None],
        ["iotd", "iotd port", False, None],
        ["iotd cave", "iotd rupoor", False, "bombs"],
        ["iotd rupoor", "iotd cave", False, None],
        ["iotd cave", "iotd", True, None],
        ["iotd", "iotd temple", True, None],
        ["iotd", "iotd tunnel", False, "shovel"],
        ["iotd tunnel", "iotd tunnel cave", False, "bombs"],
        ["iotd tunnel cave", "iotd tunnel", False, None],
        ["iotd tunnel", "iotd face", True, None],
        ["iotd face", "iotd", False, None],
        ["iotd temple", "iotd crown", True, None],
        ["iotd crown", "iotd", False, None],

        # ================= Isle of Ruins ====================

        ["ruins port", "ruins geozard cave east", True, None],
        ["ruins geozard cave east", "ruins geozard cave west", True, "ruins_geozards"],
        ["ruins geozard cave west", "ruins sw maze upper", True, None],
        ["ruins sw maze upper", "ruins port", False, None],
        ["ruins sw maze upper", "ruins sw maze lower", False, "ruins_water"],
        ["ruins sw port cliff", "ruins sw maze upper", False, None],
        ["ruins sw maze lower", "ruins sw maze lower exit", True, "ruins_water"],
        ["ruins sw maze lower exit", "ruins nw maze lower exit", True, None],
        ["ruins sw maze upper", "ruins nw maze upper exit", True, None],
        ["ruins sw maze lower", "ruins nw maze lower chest", True, "ruins_water"],

        ["ruins nw maze lower exit", "ruins nw boulders", False, None],
        ["ruins nw maze upper exit", "ruins nw boulders", False, None],
        ["ruins nw boulders", "ruins nw dig", False, "shovel"],
        ["ruins nw port cliff", "ruins nw maze lower chest", False, "ruins_water"],
        ["ruins nw boulders", "ruins nw across bridge", True, None],
        ["ruins nw boulders", "bremeur", True, None],
        ["bremeur", "bremeur kings key", False, "kings_key"],
        ["ruins nw boulders", "ruins nw port cliff", False, None],
        ["ruins nw port cliff", "ruins sw port cliff", True, None],
        ["ruins nw port cliff", "ruins nw port cliff tree", True, "ruins_water"],
        ["ruins nw boulders", "ruins nw lower", False, "ruins_water"],
        ["ruins nw across bridge", "ruins nw cave", True, "ruins_water"],
        ["ruins nw cave", "ruins rupee cave", True, None],
        ["ruins nw across bridge", "ruins nw alcove", False, "ruins_water"],
        ["ruins nw across bridge", "ruins ne enter upper", True, None],
        ["ruins nw return", "ruins nw boulders", False, None],
        ["ruins nw across bridge", "ruins nw return",  False, "hard_logic"],
        ["ruins nw lower", "ruins ne lower", True, "ruins_water"],

        ["ruins ne enter upper", "ruins ne doylan bridge", False, None],
        ["ruins ne doylan bridge", "ruins ne lower", False, "ruins_water"],
        ["ruins ne doylan bridge", "ruins ne behind temple", True, "ruins_water"],
        ["ruins ne doylan bridge", "ruins nw return", True, None],
        ["ruins ne doylan bridge", "doylan temple", True, None],
        ["doylan temple", "doylan chamber", True, None],
        ["ruins ne lower", "ruins nw alcove", True, "ruins_water"],
        ["ruins ne lower", "ruins ne behind temple", True, "grapple"],
        ["ruins ne lower", "ruins se lower", True, "ruins_water"],
        ["ruins ne behind temple", "ruins se coast", True, "ruins_water"],
        ["ruins ne outside temple", "ruins ne behind temple", False, "ruins_water"],
        ["ruins ne outside temple", "mutoh", True, None],
        ["ruins ne outside temple", "ruins ne geozards", False, "ruins_water"],
        ["ruins ne geozards", "ruins ne outside temple", False, "damage"],

        ["ruins se lower", "ruins ne secret chest", True, "ruins_water"],
        ["ruins se lower", "ruins se return bridge east", True, "ruins_water"],
        ["ruins se return bridge west", "ruins se return bridge east", False, "hammer"],
        ["ruins se return bridge east", "ruins se return bridge west", False, None],
        ["ruins se lower", "ruins se outside max", True, "ruins_water"],
        ["ruins se return bridge west", "ruins sw port cliff", True, None],
        ["ruins se outside max", "max", True, None],
        ["ruins se lower", "ruins se path to temple", False, None],
        ["ruins se path to temple", "ruins ne geozards", True, "ruins_water"],

        # ================= Mutoh's Temple ====================

        ["mutoh", "mutoh landing", False, "mutoh_entrance"],
        ["mutoh landing", "mutoh hammer", False, "hammer"],
        ["mutoh hammer", "mutoh water", False, "mutoh_water"],
        ["mutoh water", "mutoh bk chest", False, "mutoh_bk_chest"],
        ["mutoh water", "mutoh before eox", False, "mutoh_boss_door"],
        ["mutoh before eox", "mutoh eox", True, None],
        ["mutoh eox", "mutoh post eox", False, "hammer"],
        ["mutoh bk chest", "mutoh before eox", False, "is_ut"],

        # ================= Maze Island ====================

        ["maze", "maze sword", False, "sword"],
        ["maze sword", "maze east", False, "explosives"],
        ["maze sword", "maze normal", False, "bow"],
        ["maze normal", "maze expert", False, "grapple"],
        ["maze sword", "maze dig", False, "shovel"],

        # ========== Fishing ====================

        ["frog warps", "fishing", False, "fishing_rod"],
        ["fishing", "fishing bcl", False, "big_catch_lure"],
        ["fishing", "fishing rsf", False, "can_catch_rsf"],
        ["fishing", "fishing shadows", False, "swordfish_shadows"],
        ["fishing", "fishing stowfish", False, "ut_can_stowfish"],

        # ========== Salvage ==============

        ["sw ocean west", "sw ocean west salvage", False, "salvage"],
        ["sw ocean east", "sw ocean east salvage", False, "salvage"],
        ["nw ocean", "nw ocean salvage", False, "salvage"],
        ["se ocean", "se ocean salvage", False, "salvage"],
        ["ne ocean", "ne ocean salvage", False, "salvage"],
        ["ne ocean", "ne ocean inner", False, "regal_necklace"],
        ["ne ocean inner", "ne ocean", False, None],
        ["ne ocean inner", "ne ocean salvage inner", False, "salvage"],
        ["ne ocean", "nw ocean corner salvage", False, "salvage_behind_bannan"],

        ["sw ocean west salvage", "salvage 1", False, "treasure_map", 1],
        ["sw ocean east salvage", "salvage 2", False, "treasure_map", 2],
        ["nw ocean salvage", "salvage 3", False, "treasure_map", 3],
        ["nw ocean corner salvage", "salvage 4", False, "treasure_map", 4],
        ["sw ocean west salvage", "salvage 5", False, "treasure_map", 5],
        ["nw ocean salvage", "salvage 6", False, "treasure_map", 6],
        ["nw ocean salvage", "salvage 7", False, "treasure_map", 7],
        ["sw ocean east salvage", "salvage 8", False, "treasure_map", 8],
        ["sw ocean east salvage", "salvage 9", False, "treasure_map", 9],
        ["nw ocean salvage", "salvage 10", False, "treasure_map", 10],
        ["nw ocean salvage", "salvage 11", False, "treasure_map", 11],
        ["se ocean salvage", "salvage 12", False, "treasure_map", 12],
        ["se ocean salvage", "salvage 13", False, "treasure_map", 13],
        ["se ocean salvage", "salvage 14", False, "treasure_map", 14],
        ["se ocean salvage", "salvage 15", False, "treasure_map", 15],
        ["se ocean salvage", "salvage 16", False, "treasure_map", 16],
        ["se ocean salvage", "salvage 17", False, "treasure_map", 17],
        ["sw ocean east salvage", "salvage 18", False, "treasure_map", 18],
        ["nw ocean salvage", "salvage 19", False, "treasure_map", 19],
        ["nw ocean corner salvage", "salvage 20", False, "treasure_map", 20],
        ["sw ocean west salvage", "salvage 21", False, "treasure_map", 21],
        ["se ocean salvage", "salvage 22", False, "treasure_map", 22],
        ["se ocean salvage", "salvage 23", False, "treasure_map", 23],
        ["ne ocean salvage", "salvage 24", False, "treasure_map", 24],
        ["ne ocean salvage", "salvage 25", False, "treasure_map", 25],
        ["ne ocean salvage inner", "salvage 26", False, "treasure_map", 26],
        ["ne ocean salvage", "salvage 27", False, "treasure_map", 27],
        ["ne ocean salvage inner", "salvage 28", False, "treasure_map", 28],
        ["ne ocean salvage", "salvage 29", False, "treasure_map", 29],
        ["ne ocean salvage", "salvage 30", False, "treasure_map", 30],
        ["ne ocean salvage", "salvage 31", False, "treasure_map", 31],

        # Goal stuff
        ["sw ocean east", "bellumbeck", False, "bellumbeck_quick_finish"],
        ["bellumbeck", "beat bellumbeck", False, "can_beat_bellumbeck"],
        ["beat bellumbeck", "goal", False, None],
        ["totok midway", "goal", False, "goal_midway"],
        ["menu", "goal", False, "win_on_metals"],

    ]

    return overworld_logic


def is_item(item: Item, player: int, item_name: str):
    return item.player == player and item.name == item_name


def create_connections(multiworld: MultiWorld, player: int, origin_name: str, options):
    def create_entrance(r1: "PHRegion", r2: "PHRegion", *arguments):
        entrance_key = (r1.name, r2.name)
        name = None
        if entrance_key in test_entrances:
            entrance_data = test_entrances[entrance_key]
            name = entrance_data.name
        if rule_lookup:
            rule_func = RULE_DICT[rule_lookup]
            entrance = r1.connect(r2, name, lambda state: rule_func(state, player, *arguments))
        else:
            entrance = r1.connect(r2, name, None)

        if entrance_key in test_entrances:
            # Set entrance data
            entrance_data = test_entrances[entrance_key]
            rando_type_bool = entrance_data.two_way
            entrance.randomization_type = EntranceType.TWO_WAY if rando_type_bool else EntranceType.ONE_WAY
            entrance.randomization_group = entrance_data.direction | entrance_data.category_group | entrance_data.island
            entrance.name = entrance_data.name
            multiworld.worlds[player].entrances[entrance.name] = entrance
            uncreated_entrances.remove(entrance.name)

    all_logic = [
        make_overworld_logic()
    ]

    test_entrances = {(e.entrance_region, e.exit_region): e for e in ENTRANCES.values()}
    uncreated_entrances = [e.name for e in ENTRANCES.values()]

    # Create connections
    for logic_array in all_logic:
        for entrance_desc in logic_array:
            reg1, reg2, is_two_way, rule_lookup, *args = entrance_desc
            region_1 = multiworld.get_region(reg1, player)
            region_2 = multiworld.get_region(reg2, player)

            create_entrance(region_1, region_2, *args)
            if is_two_way:
                create_entrance(region_2, region_1, *args)


    # print(f"Some entrances had no logical matches: ")
    # for i in uncreated_entrances:
    #     print(f"\t{i}")

