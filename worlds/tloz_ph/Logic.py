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
        ["Menu", "Mercay SW", False, None],

        # ====== Mercay Island ==============

        ["Mercay SW", "Mercay SW Dig Spot", False, "shovel"],
        ["Oshus' House", "Oshus Gem", False, "oshus_gem"],
        ["Oshus' House", "Oshus Phantom Blade", False, "can_make_phantom_sword"],
        ["Oshus Phantom Blade", "Oshus Gem", False, None],
        ["Mercay SW", "Mercay SW Bridge", True, None],
        ["Mercay SW", "Oshus' House", True, None],
        ["Mercay SW", "Apricot's House", True, None],
        ["Mercay SW", "Sword Cave", True, None],
        ["Mercay SW", "Mercay NW Chus", True, False],

        ["Mercay SW Bridge", "Mercay SE", True, None],
        ["Mercay SE", "Tuzi's House", True, None],
        ["Mercay SE", "Milk Bar", True, None],
        ["Mercay SE", "Mercay Shop", True, None],
        ["Mercay Shop", "Island Shop", False, None],
        ["Mercay SE", "Mercay SE Shipyard", False, "has", "_beat_tof"],
            ["Mercay SE Shipyard", "Shipyard", False, "has", "_beat_tof"],
            ["Shipyard", "Mercay SE Shipyard", False, None],
            ["Mercay SE Shipyard", "Mercay SE", False, None],
        ["Mercay SE", "Mercay SE Treasure Teller", False, "courage_crest"],
            ["Mercay SE Treasure Teller", "Treasure Teller", False, "courage_crest"],
            ["Treasure Teller", "Mercay SE Treasure Teller", False, None],
            ["Mercay SE Treasure Teller", "Mercay SE", False, None],
        ["Mercay SE", "Mercay SE Ojibe", False, "courage_crest"],
        ["Mercay SE", "Mercay NE", True, False],
        ["Mercay SE Ledge", "Mercay SE", False, None],

        ["Mercay NW Chus", "Mercay NW Bamboo", True, "can_cut_bamboo"],
        ["Mercay NW Temple", "Eye Bridge Cave North", False, "explosives"],
        ["Eye Bridge Cave North", "Mercay NW Temple", False, None],
        ["Eye Bridge Cave North", "Eye Bridge Cave South", False, "bow"],
        ["Eye Bridge Cave South", "Mercay NE Ledge", True, None],
        ["Mercay NW Temple", "TotOK Lobby", True, None],

        ["Mercay NE", "Long Bridge Cave", False, "explosives"],
        ["Long Bridge Cave", "Mercay NE", False, None],
        ["Long Bridge Cave", "Mercay NW Freedle Island", True, None],
        ["Mercay NW Freedle Island", "Mercay NE", False, None],
        ["Long Bridge Cave", "Long Bridge Cave Chest", False, "range"],
        ["Mercay NW Freedle Island", "Mercay NW Freedle Gift", False, "sea_chart", "SE"],
        ["Mercay NE", "Mercay NW Temple", True, None],
        ["Mercay NE Ledge", "Mercay NE", False, None],
        ["Mercay NE Ledge", "Mercay SE Ledge", True, None],

        ["Mercay NW Temple", "Mercay NW OoB High", False, "scroll_clip"],
        ["Mercay NW OoB High", "Mercay NW Temple", False, None],
        ["Mercay NW OoB High", "Mercay NW OoB Low", False, None],
        ["Mercay NW OoB Low", "Mercay NW Chus", False, None],
        ["Mercay NW OoB Low", "Mercay NW Bamboo", False, None],
        ["Mercay NW OoB High", "Mercay NE OoB", True, None],
        ["Mercay NW OoB High", "Mercay SW OoB High", True, None],
        ["Mercay NW OoB High", "Mercay SW OoB East", True, None],
        ["Mercay NW OoB Low", "Mercay SW OoB Low", True, None],

        ["Mercay SW OoB High", "Mercay SW OoB Low", False, None],
        ["Mercay SW OoB Low", "Mercay SW", False, None],
        ["Mercay SW OoB East", "Mercay SW Bridge", False, None],
        ["Mercay SW OoB East", "Mercay SE OoB", True, None],

        ["Mercay SE OoB", "Mercay SE Ledge", False, None],
        ["Mercay SE OoB", "Mercay NE OoB", True, None],
        ["Mercay NE OoB", "Mercay NE Ledge", False, None],

        # ======== Mountain Passage =========

        ["Mercay NW Bamboo", "Mountain Passage 1", True, None],
        ["Mountain Passage 1", "Mountain Passage 2", False, "can_reach_mp2"],
        ["Mountain Passage 2 Exit", "Mountain Passage 2", False, "can_reach_mp2_top"],
        ["Mountain Passage 1", "Mountain Passage 2 Exit", False, "mp2_bypass_fore"],
        ["Mountain Passage 2 Exit", "Mountain Passage 1", False, "mp2_bypass"],
        ["Mountain Passage 2 Exit", "Mountain Passage 3", True, None],
        ["Mountain Passage 3", "Mountain Passage Rat", False, "mp_rat"],
        ["Mountain Passage 3", "Mountain Passage 4", False, "mp3"],
        ["Mountain Passage 4", "Mountain Passage 3", False, "mp3_back"],
        ["Mountain Passage 4", "Mercay SE", True, None],
        ["Mountain Passage 4", "Mountain Passage 1", False, "hard_logic"],
        ["Mountain Passage 3", "Mountain Passage 1", False, "hard_logic"],

        # ========== TotOK ===================
        ["TotOK Lobby", "TotOK 1F", False, "totok_1f"],

        ["TotOK 1F", "TotOK 1F Chest", False, "totok_1f_chest"],
        ["TotOK 1F", "TotOK 1F Chart", False, "totok_1f_chart"],
        ["TotOK 1F", "TotOK B1", False, "totok_b1"],

        ["TotOK B1", "TotOK B1 Key", False, "totok_b1_key"],
        ["TotOK B1", "TotOK B1 Phantom", False, "totok_b1_phantom"],
        ["TotOK B1", "TotOK B1 Bow", False, "totok_b1_bow"],
        ["TotOK B1", "TotOK B2", False, "totok_b2"],

        ["TotOK B2", "TotOK B2 Key", False, "totok_b2_key"],
        ["TotOK B2", "TotOK B2 Phantom", False, "totok_b2_phantom"],
        ["TotOK B2", "TotOK B2 Chu", False, "totok_b2_chu"],
        ["TotOK B2", "TotOK B3", False, "totok_b3"],

        ["TotOK B3", "TotOK B3 NW Chest", False, "totok_b3_nw"],
        ["TotOK B3", "TotOK B3 SE Chest", False, "totok_b3_se"],
        ["TotOK B3", "TotOK B3 SW Chest", False, "totok_b3_sw"],
        ["TotOK B3", "TotOK B3 Bow", False, "totok_b3_bow"],
        ["TotOK B3", "TotOK B3 Key", False, "totok_b3_key"],
        ["TotOK B3", "TotOK B3 Phantom", False, "totok_b3_phantom"],
        ["TotOK B3", "TotOK B3.5", False, "totok_b35"],
        ["TotOK B3.5", "TotOK B4", False, "totok_b4"],

        ["TotOK B4", "TotOK B4 Key", False, "totok_b4_key"],
        ["TotOK B4", "TotOK B4 Eyes", False, "totok_b4_eyes"],
        ["TotOK B4", "TotOK B4 Phantom", False, "totok_b4_phantom"],
        ["TotOK B4", "TotOK B5", False, "totok_b5"],
        ["TotOK B4", "TotOK B5 Alt Path", False, "totok_b5_alt"],

        ["TotOK B5", "TotOK B5 Chest", False, "totok_b5_chest"],
        ["TotOK B5", "TotOK B6", False, "totok_b6"],
        ["TotOK B5 Alt Path", "TotOK B5 Alt Path Chest", False, "totok_b5_alt_chest"],
        ["TotOK B5 Alt Path", "TotOK B6", False, "totok_b6"],

        ["TotOK B6", "TotOK B6 Bow", False, "totok_b6_bow"],
        ["TotOK B6", "TotOK B6 Phantom", False, "totok_b6_phantom"],
        ["TotOK B6", "TotOK B6 Crest", False, "totok_b6_crest"],
        ["TotOK B6", "TotOK B6 Midway", False, "totok_b7"],
        ["TotOK B6 Midway", "TotOK B7", False, "spirit", "Courage"],

        ["TotOK B7", "TotOK B7 Crystal", False, "totok_b7_crystal"],
        ["TotOK B7", "TotOK B7 Switch", False, "totok_b7_switch_chest"],
        ["TotOK B7", "TotOK B8", False, "totok_b8"],

        ["TotOK B8", "TotOK B8 Phantom", False, "totok_b8_phantom"],
        ["TotOK B8", "TotOK B9", False, "totok_b9"],
        ["TotOK B8", "TotOK B8 2 Crystals Chest", False, "totok_b8_2_crystal_chest"],
        ["TotOK B8", "TotOK B7 Phantom", False, "totok_b7_phantom"],
        ["TotOK B8", "TotOK B9 Corner Chest", False, "totok_b9_corner_chest"],

        ["TotOK B9", "TotOK B9 Phantom", False, "totok_b9_phantom"],
        ["TotOK B9", "TotOK B9 Wizzrobes", False, "totok_b9_ghosts"],

        ["TotOK B9", "TotOK B9.5", False, "totok_b10"],
        ["TotOK B9.5", "TotOK B10", True, None],

        ["TotOK B10", "TotOK B10 Key", False, "totok_b10_key"],
        ["TotOK B10", "TotOK B10 Phantom", False, "totok_b10_phantom"],
        ["TotOK B10", "TotOK B10 Eyes", False, "totok_b10_eye"],
        ["TotOK B10", "TotOK B10 Hammer", False, "totok_b10_hammer"],
        ["TotOK B10", "TotOK B11", False, "totok_b11"],

        ["TotOK B11", "TotOK B11 Phantom", False, "totok_b11_phantom"],
        ["TotOK B11", "TotOK B11 Eyes", False, "totok_b11_eyes"],
        ["TotOK B11", "TotOK B12", False, "totok_b12"],

        ["TotOK B12", "TotOK B12 NW Chest", False, "totok_b12_nw"],
        ["TotOK B12", "TotOK B12 NE Chest", False, "totok_b12_ne"],
        ["TotOK B12", "TotOK B12 Phantom", False, "totok_b12_phantom"],
        ["TotOK B12", "TotOK B12 Ghost", False, "totok_b12_ghost"],
        ["TotOK B12", "TotOK B12 Hammer", False, "totok_b12_hammer"],
        ["TotOK B12", "TotOK B13", False, "totok_b13"],

        ["TotOK B13", "TotOK B13 Chest", False, "totok_b13_chest"],
        ["TotOK B13", "TotOK B14", False, "b13_door"],
        ["TotOK Lobby", "TotOK B14", False, "bellum_warp"],
        # Bellum
        ["TotOK B14", "Bellum", False, "bellum_staircase"],
        ["Bellum", "Ghost Ship Fight", False, "can_beat_bellum"],
        ["Ghost Ship Fight", "Bellumbeck", False, "can_beat_ghost_ship_fight"],

        # ============ Shops ====================

        ["Island Shop", "Island Shop Power Gem", False, "can_buy_gem"],
        ["Island Shop", "Island Shop Quiver", False, "can_buy_quiver"],
        ["Island Shop", "Island Shop Bombchu Bag", False, "can_buy_chu_bag"],
        ["Island Shop", "Island Shop Heart Container", False, "can_buy_heart"],

        ["SW Ocean East", "Beedle", False, None],
        ["SW Ocean West", "Beedle", False, None],
        ["NW Ocean", "Beedle", False, None],
        ["SE Ocean", "Beedle", False, None],
        ["NE Ocean", "Beedle", False, None],

        ["Beedle", "Beedle Gem", False, "beedle_shop", 500],
        ["Beedle", "Beedle Bomb Bag", False, "can_buy_bomb_bag"],
        ["Beedle", "Masked Ship Gem", False, "beedle_shop", 500],
        ["Beedle", "Masked Ship HC", False, "beedle_shop", 500],

        ["Beedle", "Beedle Bronze Membership", False, "can_get_beedle_bronze"],
        ["Beedle", "Beedle Silver Membership", False, "has_beedle_points", 20],
        ["Beedle", "Beedle Gold Membership", False, "has_beedle_points", 50],
        ["Beedle", "Beedle Platinum Membership", False, "has_beedle_points", 100],
        ["Beedle", "Beedle VIP Membership", False, "has_beedle_points", 200],

        # ============ SW Ocean =================

        ["Mercay SE", "Mercay Boat", False, "boat_access"],
            ["Mercay Boat", "Mercay SE", False, "require_chart", "SW"],
            ["Mercay Boat", "SW Ocean East", True, "require_chart", "SW"],
        ["Cannon Boat", "Cannon Island", False, "require_chart", "SW"],
            ["Cannon Island", "Cannon Boat", False, None],
            ["Cannon Boat", "SW Ocean East", True, "require_chart", "SW"],
        ["Ember Boat", "Ember Port", False, "require_chart", "SW"],
            ["Ember Port", "Ember Boat", False, None],
            ["Ember Boat", "SW Ocean East", True, "require_chart", "SW"],
        ["SW Ocean East", "SW Ocean Crest Salvage", False, "salvage_courage_crest"],
        ["SW Ocean East", "SW Ocean West", False, "cannon"],
        ["SW Ocean West", "SW Ocean East", False, "cannon"],
        ["Molida Boat", "Molida South", False, "require_chart", "SW"],
            ["Molida South", "Molida Boat", False, None],
            ["Molida Boat", "SW Ocean West", True, "require_chart", "SW"],
        ["Spirit Boat", "Spirit Island", False, "require_chart", "SW"],
            ["Spirit Island", "Spirit Boat", False, None],
            ["Spirit Boat", "SW Ocean West", True, "require_chart", "SW"],
        ["SW Ocean West", "Nyave", False, "nyave_fight"],
        ["Nyave", "Nyave Trade", False, "guard_notebook"],
        ["SW Ocean West", "SW Ocean Frog Phi", False, "cannon"],
        ["SW Ocean East", "SW Ocean Frog X", False, "cannon"],
        ["SW Ocean West", "Frog Warps", False, None],
        ["SW Ocean East", "Frog Warps", False, None],

        # ============= Frog Warps ==================
        ["Frog Warps", "SW Ocean West", False, "frog_phi"],
        ["Frog Warps", "SW Ocean East", False, "frog_x"],
        ["Frog Warps", "NW Ocean", False, "frog_n"],
        ["Frog Warps", "NE Ocean", False, "frog_square"],
        ["Frog Warps", "SE Ocean", False, "frog_se"],

        # ============ Cannon Island ===============

        ["Cannon Island", "Fuzo's Workshop", True, None],
        ["Cannon Island", "Cannon Island Dig", False, "shovel"],
        ["Cannon Island", "Bomb Flower Cave South", True, None],
        ["Bomb Flower Cave South", "Bomb Flower Cave North", False, None],
        ["Bomb Flower Cave North", "Cannon Bomb Garden", True, None],
        ["Bomb Flower Cave North", "Bomb Flower Cave South", False, "hard_logic"],
        ["Cannon Bomb Garden", "Cannon Outside Eddo", False, None],
        ["Cannon Outside Eddo", "Cannon Bomb Garden", False, "explosives"],
        ["Cannon Bomb Garden", "Cannon Island", False, None],
        ["Cannon Outside Eddo", "Cannon Island", False, "glitched_logic"],
        ["Cannon Outside Eddo", "Eddo's Workshop", True, None],
        ["Fuzo's Workshop", "Eddo's Workshop", True, "has", "_eddo_door"],
        ["Eddo's Workshop", "Eddo Salvage Arm", False, "courage_crest"],
        ["Eddo's Workshop", "Eddo Event", False, None],
        ["Cannon Bomb Garden", "Cannon Bomb Garden Dig", False, "shovel"],

        # =============== Isle of Ember ================

        # ER
        ["Ember Port", "Astrid's House", True, None],
        ["Astrid's House", "Astrid's Basement", True, None],
        ["Astrid's Basement", "Astrid's Basement Dig", False, "spade"],
        ["Ember Port", "Kayo's House", True, None],
        ["Ember Port", "Abandoned House", True, None],
        ["Astrid's House", "Astrid Post ToF", False, "has", "_beat_tof"],

        ["Ember Port", "Ember Grapple", False, "ember_grapple"],
        ["Ember Grapple", "Ember Port", False, "grapple"],
        ["Ember Grapple", "Ember Coast North", True, "grapple"],

        ["Ember Coast North", "Ember Coast East", True, None],
        ["Ember Port", "Ember Coast East", True, None],
        ["Ember Climb West", "Ember Coast East", True, None],
        ["Ember Climb West", "Ember Outside Temple", True, None],
        ["Ember Outside Temple", "ToF 1F", True, None],
        ["Ember Summit West", "Ember Outside Temple", True, None],
        ["Ember Summit West", "Ember Summit East", True, None],
        ["Ember Outside Temple", "Ember Outside Temple Dig", False, "shovel"],

        ["Ember Summit West", "Ember Climb West", False, None],
        ["Ember Summit East", "Ember Outside Temple", False, None],
        ["Ember Climb West", "Ember Port", False, None],
        ["Ember Outside Temple", "Ember Coast East", False, None],

        ["Ember Climb East", "Ember Coast East", True, None],
        ["Ember Summit North", "Ember Summit East", True, None],
        ["Ember Climb East", "Ember Port", True, None],
        ["Ember Summit North", "Ember Summit West", True, None],

        # =============== Temple of Fire =================

        ["ToF 1F", "ToF 1F Keese Arena", False, "can_kill_bat"],
        ["ToF 1F", "ToF 1F Maze", False, "tof_maze"],
        ["ToF 1F Maze", "ToF 2F", False, "can_hit_spin_switches"],
        # 2F
        ["ToF 2F", "ToF 1F West", False, "short_range"],
        ["ToF 1F West", "ToF 1F SW", False, "can_hit_spiral_wall_switches"],
        ["ToF 1F SW", "ToF 2F South", False, "can_kill_bubble"],
        ["ToF 2F South", "ToF 3F", False, "tof_3f"],
        # 3F
        ["ToF 3F", "ToF 3F Key Drop", False, "tof_key_drop"],
        ["ToF 3F", "ToF 3F Key Door", False, "tof_3f_key_door"],
        ["ToF 3F Key Door", "ToF 3F Boss Key", False, "boomerang"],
        ["ToF 3F Key Door", "ToF 4F", True, "tof_bk"],
        ["ToF 4F", "Blaaz", True, None],
        ["ToF 4F", "ToF 1F", False, None],  # warp or S+Q
        ["Blaaz", "Post Blaaz", False, "tof_blaaz"],
        ["Post Blaaz", "Post ToF", False, "tof_blaaz"],

        # =========== Molida Island ===============

        ["Molida South", "Molida Dig", False, "spade"],
        ["Molida South", "Ocara's House", True, None],
        ["Molida South", "Potato's house", True, None],
        ["Molida South", "Molida Shop", True, None],
        ["Molida Shop", "Island Shop", False, None],
        ["Molida South", "Romanos' House", True, None],
        ["Romanos' House", "Archery Game", False, "has", "_beat_toc"],
        ["Molida South", "Sun Lake Cave", True, None],
        ["Molida South", "Sun Lake Cave Upper", False, "shovel"],

        ["Sun Lake Cave Upper", "Sun Lake Cave", False, None],
        ["Sun Lake Cave", "Sun Lake Cave Grapple", False, "grapple"],
        ["Sun Lake Cave", "Sun Lake Cave Geozard", False, None],
        ["Sun Lake Cave Geozard", "Sun Lake Cave Geozard Dig", False, "shovel"],
        ["Sun Lake Cave Geozard", "Sun Lake Cave Defeat Geozard", False, "cave_damage"],
        ["Sun Lake Cave Defeat Geozard", "Sun Lake Cave Post Geozard", False, None],
        ["Sun Lake Cave Post Geozard", "Sun Lake Cave Geozard", False, "has", "_molida_cave_geozard"],
        ["Sun Lake Cave Post Geozard", "Octorok Cave", True, None],
        ["Sun Lake Cave", "Sun Lake Cave Back", False, "bombs"],
        ["Sun Lake Cave Back", "Sun Lake Cave", False, None],
        ["Sun Lake Cave Back", "Octorok Cave", True, None],
        ["Sun Lake Cave Back", "Shovel Hideout", True, None],
        ["Shovel Hideout", "Shovel Hideout Dig", False, "shovel"],
        ["Sun Lake Cave Back", "Molida Cliff North", True, None],

        ["Molida Cliff North", "Molida Cliff South", True, None],
        ["Molida Cliff South", "Molida South", False, None],
        ["Molida Cliff South", "Molida Cucco Dig", False, "cuccoo_dig"],

        ["Sun Lake Cave Upper", "Sun Lake Cave Sun Door", True, "sun_key"],
        ["Molida North", "Sun Lake Cave North Drop", False, "shovel"],
        ["Sun Lake Cave North Drop", "Sun Lake Cave Sun Door", False, None],
        ["Sun Lake Cave Sun Door", "Molida North", True, None],
        ["Molida North", "Molida North Grapple", False, "grapple"],
        ["Molida North", "Molida Temple Doors", False, "enter_toc"],
        ["Molida Temple Doors", "Molida Outside Temple", False, None],
        ["Molida Outside Temple", "ToC 1F", True, None],

        # =============== Temple of Courage ================

        ["ToC 1F", "ToC 1F Bomb Alcove", False, "boom"],
        ["ToC 1F", "ToC B1", False, "toc_door_1"],
        ["ToC 1F", "ToC 1F Hammer Clips", False, "hammer_clip"],
        ["ToC B1", "ToC B1 Grapple", False, "toc_grapple"],
        ["ToC B1", "ToC 1F West", False, "toc_1f_west"],
        ["ToC B1 Grapple", "ToC 1F West", False, "bow"],
        ["ToC 1F Hammer Clips", "ToC 1F West", False, None],
        ["ToC 1F West", "ToC 1F Map Room", False, "boom"],
        ["ToC 1F West", "ToC 2F Beamos Room", False, "toc_door_2"],
        ["ToC 1F West", "ToC B1 Invisible Maze", False, "shape_crystal", "Temple of Courage", "Square", "North"],
        ["ToC 2F Beamos Room", "ToC B1 Invisible Maze", False, "ut_pedestals_vanilla"],
        ["ToC 2F Beamos Room", "ToC South 1F", False, "toc_beamos_ut"],
        ["ToC B1 Grapple", "ToC B1 Invisible Maze", False, None],
        ["ToC B1 Invisible Maze", "ToC South 1F", False, "toc_crystal_south"],

        ["ToC South 1F", "ToC 2F Spike Corridor", False, "boom"],
        ["ToC 2F Spike Corridor", "ToC 2F Moving Platform Room", False, "toc_spike_corridor"],
        ["ToC 1F Hammer Clips", "ToC 2F Spike Corridor", False, None],
        ["ToC South 1F", "ToC 2F Moving Platform Room", False, "bow"],
        ["ToC 2F Spike Corridor", "ToC B1 Torches Platforms", False, "boomerang"],
        ["ToC B1 Torches Platforms", "ToC B1 Torches Chest", False, "bow"],
        ["ToC B1 Torches Platforms", "ToC 1F Pols NW", False, "toc_switch_state"],
        ["ToC 1F Pols NW", "ToC 2F Scribble Platform Room", False, "toc_door_3"],
        ["ToC 2F Scribble Platform Room", "ToC 2F Scribble Platform Chest", False, "bow"],
        ["ToC 2F Scribble Platform Room", "ToC 3F", False, "toc_boss_key"],
        ["ToC 2F Scribble Platform Chest", "ToC 3F", False, "simple_boss_key", "Temple of Courage"],
        ["ToC 3F", "ToC 3F Chest", False, "boom"],
        ["ToC 3F", "Crayk", True, None],
        ["ToC 3F", "ToC 1F", False, None],
        ["Crayk", "Post Crayk", False, "bow"],
        ["Post Crayk", "Post ToC", False, None],

        # ================ Spirit Island =====================

        ["Spirit Island", "Spirit Island Gauntlet", False, "grapple"],
        ["Spirit Island", "Spirit Shrine", True, None],
        ["Spirit Shrine", "Spirit Power 1", False, "spirit_gems", "Power", 10],
        ["Spirit Shrine", "Spirit Power 2", False, "spirit_gems", "Power", 20],
        ["Spirit Shrine", "Spirit Wisdom 1", False, "spirit_gems", "Wisdom", 10],
        ["Spirit Shrine", "Spirit Wisdom 2", False, "spirit_gems", "Wisdom", 20],
        ["Spirit Shrine", "Spirit Courage 1", False, "spirit_gems", "Courage", 10],
        ["Spirit Shrine", "Spirit Courage 2", False, "spirit_gems", "Courage", 20],

        # ============ Ocean NW ===============
        ["SW Ocean West", "NW Ocean", False, "sea_chart", "NW"],
        ["NW Ocean", "SW Ocean West", False, "sea_chart", "SW"],
        ["NW Ocean", "SW Ocean East", False, "sea_chart", "SW"],
        ["NW Ocean", "Frog Warps", False, None],
        ["NW Ocean", "NW Ocean Frog N", False, "cannon"],
        ["Gust South", "Gust Boat", False, None],
            ["Gust Boat", "Gust South", False, "require_chart", "NW"],
            ["Gust Boat", "NW Ocean", True, "require_chart", "NW"],
        ["Bannan Island", "Bannan Boat", False, None],
            ["Bannan Boat", "Bannan Island", False, "require_chart", "NW"],
            ["Bannan Boat", "NW Ocean", True, "bannan_sea_monster"],
        ["Zauz Boat", "NW Ocean", True, "require_chart", "NW"],
            ["Zauz's Island", "Zauz Boat", False, None],
            ["Zauz Boat", "Zauz's Island", False, "require_chart", "NW"],
        ["Uncharted Island", "Uncharted Boat", False, None],
            ["Uncharted Boat", "Uncharted Island", False, "require_chart", "NW"],
            ["Uncharted Boat", "NW Ocean", True, "require_chart", "NW"],
        ["NW Ocean", "Ghost Ship Boat", False, "ghost_ship"],
            ["Ghost Ship Boat", "NW Ocean", False, "require_chart", "NW"],
            ["Ghost Ship Boat", "Ghost Ship 1F", False, "ghost_ship"],
            ["Ghost Ship 1F", "Ghost Ship Boat", False, None],
        ["NW Ocean", "PoRL", False, None],
        ["PoRL", "PoRL Item", False, "sword"],
        ["PoRL", "PoRL Trade", False, "heroes_new_clothes"],

        # ================= Isle of Gust ====================

        ["Gust South", "Tiled Hideout", True, None],
        ["Gust South", "Miniblin Cave", True, None],
        ["Miniblin Cave", "Miniblin Cave Damage", False, "cave_damage"],
        ["Miniblin Cave", "Gust South Cliffs", True, None],
        ["Gust South Cliffs", "Gust South", False, None],
        ["Gust South Cliffs", "Gust South Cliffs Dig", False, "shovel"],
        ["Gust South Cliffs", "Gust North Temple Road", True, None],
        ["Gust South Cliffs", "Gust North Above Temple", True, None],
        ["Gust North Above Temple", "Gust South NW", True, None],
        ["Gust South NW", "Gust South NW Chest", False, "shovel"],
        ["Gust South NW", "Gust South NW Ledge", False, "shovel"],
        ["Gust South NW Ledge", "Gust South NW", False, None],
        ["Gust South NW Ledge", "Gust South NW Chest", False, "grapple"],
        ["Gust South NW Ledge", "Gust North", True, None],
        ["Gust North", "Gust North Dig", False, "shovel"],
        ["Gust North", "Gust North Sandworms", True, "shovel"],
        ["Gust North Sandworms", "Gust North Event", False, None],
        ["Gust North Sandworms", "Gust North Above Temple", True, "has", "_windmills"],
        ["Gust North Above Temple", "Gust North Temple Road", False, None],
        ["Gust North Temple Road", "Gust North Outside Temple", False, "has", "_windmills"],
        ["Gust North Outside Temple", "Gust North Temple Road", False, None],
        ["Gust North Outside Temple", "ToW 1F", True, None],

        # ================= Temple of Wind ====================

        ["ToW 1F", "ToW B1", False, "tow_b1"],
        ["ToW B1", "ToW B2", False, None],
        ["ToW B2", "ToW B2 Dig", False, "shovel"],
        ["ToW B2", "ToW B2 Bombs", False, "explosives"],
        ["ToW B2", "ToW B2 Key", False, "tow_key"],
        ["ToW B2", "ToW 1F NE", False, "bombs"],
        ["ToW 1F", "ToW 2F", False, "tow_cyclok"],
        ["ToW 2F", "Cyclok", True, None],
        ["ToW 2F", "ToW 1F", False, None],
        ["Cyclok", "Post Cyclok", False, None],
        ["Post Cyclok", "Post ToW", False, None],

        # ================= Bannan Island ====================

        ["Bannan Island", "Bannan West Grapple", False, "grapple"],
        ["Bannan Island", "Bannan Dig", False, "shovel"],
        ["Bannan Island", "Wayfarer's House", True, None],
        ["Wayfarer's House", "Wayfarer Event", False, None],
        ["Bannan Island", "Keese Passage West", True, None],
        ["Keese Passage West", "Keese Passage East", True, "bombs"],
        ["Keese Passage East", "Bannan East", True, None],
        ["Bannan East", "Bannan East Grapple", False, "grapple"],
        ["Bannan East Grapple", "Bannan East Grapple Dig", False, "shovel"],
        ["Bannan East", "Bannan Cannon Game", False, "cannon"],
        ["Wayfarer's House", "Wayfarer Trade Quest", False, "bannan_scroll"],
        ["Wayfarer's House", "Wayfarer Give Loovar", False, "loovar"],
        ["Wayfarer's House", "Wayfarer Give Rusty Swordfish", False, "rsf"],
        ["Wayfarer's House", "Wayfarer Give Legendary Neptoona", False, "neptoona"],
        ["Wayfarer's House", "Wayfarer Give Stowfish", False, "stowfish"],
        ["Wayfarer's House", "Joanne Give Letter", False, "jolene_letter"],

        # ================= Zauz's Island ====================

        ["Zauz's Island", "Zauz Dig", False, "shovel"],
        ["Zauz's Island", "Zauz's House", True, None],
        ["Zauz's House", "Zauz's Blade", False, "has_zauz_required_metals"],
        ["Zauz's House", "Zauz's Crest", False, "has", "_beat_ghost_ship"],

        # ================= Uncharted Island ====================

        ["Uncharted Island", "Uncharted Dig", False, "shovel"],
        ["Uncharted Island", "Uncharted Puzzle", False, "sword"],
        ["Uncharted Puzzle", "Uncharted Outside Cave", False, None],
        ["Uncharted Outside Cave", "Descending Cave", True, None],
        ["Descending Cave", "Golden Chief Cave", True, None],
        ["Descending Cave", "Descending Cave Grapple", False, "grapple"],

        # ================= Ghost Ship ====================

        ["Ghost Ship 1F", "Ghost Ship B1", True, None],
        ["Ghost Ship B1", "Ghost Ship B1 Barrel", False, "gs_barrel"],
        ["Ghost Ship B1 Barrel", "Ghost Ship B2", False, "gs_triangle"],
        ["Ghost Ship B2", "Ghost Ship B2 Chests", False, "can_hit_switches"],
        ["Ghost Ship B2 Chests", "Ghost Ship B3", False, "can_kill_bat"],
        ["Ghost Ship B3", "Ghost Ship Warp", False, None],
        ["Ghost Ship Warp", "Cubus Sisters", False, "has", "_rescue_4th_sister"],
        ["Cubus Sisters", "Ghost Ship Warp", False, "sword"],
        ["Ghost Ship Warp", "Ghost Ship 1F", False, None],
        ["Cubus Sisters", "Post Cubus Sisters", False, "sword"],
        ["Ghost Ship B2", "Ghost Ship Tetra", False, "ghost_key"],
        ["Ghost Ship Tetra", "Spawn Pirate Ambush", False, None],

        # ================= SE Ocean ====================

        ["SW Ocean East", "SE Ocean", False, "se_ocean"],
        ["SE Ocean", "SW Ocean East", False, "sea_chart", "SW"],
        ["SE Ocean", "Frog Warps", False, None],
        ["SE Ocean", "SE Ocean Frogs", False, "cannon"],
        ["SE Ocean", "Goron Boat", False, "charty_sea_monster", "SE"],
            ["Goron Boat", "SE Ocean", False, "require_chart", "SE"],
            ["Goron Boat", "Goron SW",False, "charty_sea_monster", "SE"],
            ["Goron SW", "Goron Boat", False, None],
        ["SE Ocean", "SE Ocean Trade", False, "kaleidoscope"],
        ["SE Ocean", "Frost Boat", False, "charty_sea_monster", "SE"],
            ["Frost Boat", "SE Ocean", False, "require_chart", "SE"],
            ["Frost Boat", "Frost SW", False, "charty_sea_monster", "SE"],
            ["Frost SW", "Frost Boat", False, None],
        ["Harrow Island", "Harrow Boat", False, None],
            ["Harrow Boat", "Harrow Island", False, "require_chart", "SE"],
            ["Harrow Boat", "SE Ocean", True, "require_chart", "SE"],
        ["Dee Ess Island", "Dee Ess Boat", False, None],
            ["Dee Ess Boat", "Dee Ess Island", False, "require_chart", "SE"],
            ["Dee Ess Boat", "SE Ocean", True, "require_chart", "SE"],
        ["SE Ocean", "Pirate Ambush", False, "beat_gs"],
        ["SE Ocean", "SS Wayfarer", True, "ss_wayfarer"],
        ["SS Wayfarer", "SS Wayfarer Trade", False, "wood_heart"],
        ["SS Wayfarer Trade", "SS Wayfarer Event", False, None],

        # ================= Goron Island ====================

        ["Goron SW", "Goron House Zero Rocks", True, None],
        ["Goron SW", "Goron Shop", True, None],
        ["Goron Shop", "Island Shop", False, None],
        ["Goron SW", "Goron House Three Rocks", True, None],
        ["Goron SW", "Goron House Left Rock", True, None],
        ["Goron SW", "Goron NW Shortcut", True, None],
        ["Goron SW Chu Ledge", "Goron Chus", False, "goron_chus"],
        ["Goron Chus", "Goron Chus Event", False, None],
        ["Goron SW Chu Ledge", "Goron SW Grapple", False, "grapple"],
        ["Goron SW", "Goron SE NW", True, None],
        ["Goron SW Chu Ledge", "Goron SW", False, None],
        ["Goron SE NW", "Goron SW Chu Ledge", True, None],
        ["Goron SE NW", "Goron House Right Rock", True, None],
        ["Goron SE", "Goron House Two Rocks", True, None],
        ["Goron SE", "Goron Chief House", True, None],
        ["Goron SE NW", "Goron SE Bridge Event", False, None],
        ["Goron SE", "Goron SE NW", False, None],
        ["Goron SE NW", "Goron SE", False, "has", "_goron_bridge"],
        ["Goron Chief House", "Goron Quiz", False, "meet_gorons"],
        ["Goron Quiz", "Goron Chief Post Dungeon", False, "has", "_beat_gt"],
        ["Goron SE", "Goron NE", True, None],

        ["Goron NE", "Goron NE South", False, None],
        ["Goron NE South", "Goron NE Event", False, None],
        ["Goron NE South", "Goron NE", False, "goron_south_reverse"],
        ["Goron NE South", "Goron NW South Dead End", True, None],
        ["Goron NE", "Goron NE Middle", False, None],
        ["Goron NE", "Goron NE Chu Chest", False, "bombchu_switches"],
        ["Goron NE Middle", "Goron NE", False, "goron_south_reverse"],
        ["Goron NE Middle", "Goron NE Coast", True, "explosives"],
        ["Goron NE Middle", "Goron NW North Dead End", True, None],
        ["Goron NE Coast", "Goron NW Like Like", True, None],
        ["Goron NW Like Like", "Goron NW Outside Temple", False, "damage"],
        ["Goron NW Like Like", "Goron NE Spikes", True, None],
        ["Goron NE Spikes", "Goron NE Spike Chest", False, "has", "_goron_maze_switch"],
        ["Goron NW Outside Temple", "Goron NW Like Like", False, "clever_bombs"],  # Hard logic

        ["Goron NW Shortcut", "Goron NW Outside Temple", False, "goron_shortcut"],
        ["Goron NW Outside Temple", "Goron NW Shortcut", False, None],
        ["Goron NW Outside Temple", "GT 1F", True, None],

        # ================= Goron Temple ====================
        ["GT 1F", "GT 1F Upper", False, "shovel"],
        ["GT 1F", "GT 1F NW", False, "goron_entrance"],
        ["GT 1F NW", "GT 1F Bow", False, "bow"],
        ["GT 1F NW", "GT B1", False, "gt_b1"],
        ["GT B1", "GT B2", False, "bombchu_switches"],
        ["GT B2", "GT B3", False, None],
        ["GT B2", "GT B2 Back", False, "gt_b2_back"],
        ["GT B2 Back", "GT B2 Back Chest", False, "chus"],
        ["GT B2", "GT B4", False, "gt_enter_dongo"],
        ["GT B4", "Dongorongo", True, None],
        ["GT B4", "GT 1F", False, None],
        ["Dongorongo", "Post Dongorongo", False, "gt_dongo"],
        ["Post Dongorongo", "Post GT", False, None],

        # ================= Harrow Island ====================

        ["Harrow Island", "Harrow Sword", False, "sword"],
        ["Harrow Sword", "Harrow Minigame", False, "shovel"],
        ["Harrow Minigame", "Harrow Minigame NE Chart", False, "sea_chart", "NE"],

        # ================= Dee Ess Island ====================

        ["Dee Ess Island", "Dee Ess Dig", False, "shovel"],
        ["Dee Ess Island", "Dee Ess Eye Brutes", False, "can_kill_eye_brute"],
        ["Dee Ess Island", "Dee Ess Goron Race", False, "has", "_beat_gt"],

        # ================= Isle of Frost ====================

        ["Frost SW", "Frost SW Grapple", False, "grapple"],
        ["Frost SW", "Frost SW Dig", False, "spade"],
        ["Frost SW", "Smart Anouki's House", True, None],
        ["Frost SW", "Sensitive Anouki's House", True, None],
        ["Frost SW", "Anouki Chief's House", True, None],
        ["Frost SW", "Frost NW", True, None],
        ["Frost SW", "Frozen Cave", True, None],

        ["Frost NW", "Fofo's House", True, None],
        ["Frost NW", "Kumu's House", True, None],
        ["Frost NW", "Dobo's House", True, None],
        ["Frost NW", "Gumo's House", True, None],
        ["Frost NW", "Aroo's House", True, None],
        ["Frost NW", "Mazo's House", True, None],
        ["Frost NW", "Frost NW Dig", False, "shovel"],
        ["Frost NW Dig", "Frost NW Grapple Dig", False, "grapple"],

        ["Frozen Cave", "Frost SE", True, None],
        ["Frost SE", "Frost SE Yook", False, "ice_field"],
        ["Frost SE Yook", "Frost SE Exit", False, None],
        ["Frost SE", "Frost SE Upper East", False, "grapple"],
        ["Frost SE Upper East", "Frost SE", False, None],
        ["Frost SE Upper East", "Frost SE Upper Chests", False, "grapple"],
        ["Frost SE Upper East", "Frost SE East Ledge", False, None],
        ["Frost SE Upper East", "Frost SE Upper North", True, "grapple"],
        ["Frost SE Upper East", "Frost SE Exit", False, None],
        ["Frost SE Upper North", "Frost SE", False, None],
        ["Frost SE Upper North", "Frost SE Exit", False, None],
        ["Frost SE Exit", "Frost SE", False, "has", "_beat_toi"],
        ["Frost SE Upper North", "Frost NE Above Temple West", True, None],
        ["Frost SE Upper East", "Frost NE Above Temple East", True, None],
        ["Frost SE Exit", "Frost NE Outside Arena", True, None],

        ["Frost NE Above Temple East", "Frost NE Outside Arena", False, None],
        ["Frost NE Above Temple West", "Frost NE Outside Arena", False, None],
        ["Frost NE Outside Arena", "Frost NE Arena", False, None],
        ["Frost NE Arena", "Frost NE Outside Arena", False, "dark_yook"],
        ["Frost NE Arena", "Frost NE Outside Temple", False, "dark_yook"],
        ["Frost NE Arena", "Frost NE Above Temple West", False, "grapple"],
        ["Frost NE Outside Temple", "Frost NE Arena", False, None],
        ["Frost NE Outside Temple", "ToI 1F", True, None],

        # ================= Ice Temple ====================

        ["ToI 1F", "ToI 1F Ascent", False, "toi_2f"],
        ["ToI 1F Ascent", "ToI 2F Right", True, None],
        ["ToI 3F Right", "ToI 2F Right", True, None],
        ["ToI 3F Right", "ToI 3F", False, "toi_3f"],
        ["ToI 3F", "ToI 3F Right", False, "range"],
        ["ToI 3F", "ToI 3F Key Door", True, "toi_key_door_1"],
        ["ToI 3F", "ToI 3F Switch State", False, "bombs"],
        ["ToI 3F Switch State", "ToI 3F Boomerang Key", False, "toi_3f_boomerang"],
        ["ToI 3F Key Door", "ToI 2F Arena", True, None],
        ["ToI 2F Arena", "ToI 2F Post Arena", False, "dark_yook"],
        ["ToI 2F Arena", "ToI 2F Left", False, "toi_miniboss"],
        ["ToI 2F Left", "ToI 1F Beetles", True, None],
        ["ToI 1F Beetles", "ToI 1F Shortcut", False, "grapple"],
        ["ToI 1F Shortcut", "ToI 1F Beetles", False, "grapple_glitch"],
        ["ToI 1F", "ToI 1F Shortcut", False, "hammer_clip"],
        ["ToI 1F Shortcut", "ToI 1F", False, None],
        ["ToI 1F Shortcut", "ToI 1F Descent", False, "grapple"],
        ["ToI 1F Descent", "ToI B1 Ascent", True, None],

        ["ToI B1 Ascent", "ToI B1 Shore", False, None],
        ["ToI B1 Shore", "ToI B1 Ascent", False, "hammer_clip"],
        ["ToI B1 Shore", "ToI B1 South", False, "toi_b1"],
        ["ToI B1 South", "ToI B1 Shore", False, None],
        ["ToI B1 South", "ToI B1 Mid", True, "explosives"],
        ["ToI B1 Mid", "ToI B1 Right", False, "grapple"],
        ["ToI B1 Right", "ToI B1 Switch", False, "hammer_clip"],
        ["ToI B1 Right", "ToI B1 Switch Room", False, "toi_key_door_2"],
        ["ToI B1 Switch Room", "ToI B1 Switch", False, "toi_b1_switch"],
        ["ToI B1 Mid", "ToI B1 Boss Door", False, "toi_b2"],
        ["ToI B1 Boss Door", "ToI B1 Mid", False, "grapple"],
        ["ToI B1 Boss Door", "ToI B1 Before Boss", True, "toi_boss_door"],
        ["ToI B1 Before Boss", "Gleeok", True, None],
        ["Gleeok", "Post Gleeok", False, "grapple"],
        ["Post Gleeok", "Post ToI", False, None],
        ["ToI B1 Before Boss", "ToI Blue Warp", True, None],
        ["ToI 1F", "ToI Blue Warp", True, "has", "_toi_blue_warp"],
        ["ToI B1 Boss Door", "ToI B2", True, None],

        ["ToI B2", "ToI B2 North", False, "toi_b2_north"],
        ["ToI B2 North", "ToI B2 BK Chest", False, "hammer_clip"],
        ["ToI B2 North", "ToI B2 East", False, None],
        ["ToI B2 East", "ToI B2 Bow", False, "bow"],
        ["ToI B2 East", "ToI B2 East Arena", False, "toi_key_doors", 3, 3],
        ["ToI B2 East Arena", "ToI B2 BK Chest", False, None],

        # ================= NE Ocean ====================

        ["SE Ocean", "NE Ocean", False, "sea_chart", "NE"],
        ["NE Ocean", "SE Ocean", False, "sea_chart", "SE"],
        ["NE Ocean", "Frog Warps", False, None],
        ["NE Ocean", "NE Ocean Frog", False, "cannon"],
        ["NE Ocean", "NE Ocean Combat", False, "can_kill_blue_chu"],
        ["IotD Boat", "IotD Port", False, "require_chart", "NE"],
            ["IotD Port", "IotD Boat", False, None],
            ["IotD Boat", "NE Ocean", True, "require_chart", "NE"],
        ["Maze Boat", "Maze Island", False, "require_chart", "NE"],
            ["Maze Island", "Maze Boat", False, None],
            ["Maze Boat", "NE Ocean", True, "require_chart", "NE"],
        ["NE Ocean Inner", "Ruins Boat", False, None],
            ["Ruins Boat", "NE Ocean", False, "require_chart", "NE"],
            ["Ruins Boat", "Ruins SW Port", False, "regal_necklace"],
            ["Ruins SW Port", "Ruins Boat", False, None],
        ["NE Ocean", "Pirate Ambush", False, "beat_gs"],

        # ================= IotD ====================

        ["IotD Port", "McNay's Cave", True, None],
        ["Isle of the Dead", "IotD Port", False, None],
        ["McNay's Cave", "Rupoor Cave", False, "bombs"],
        ["Rupoor Cave", "McNay's Cave", False, None],
        ["McNay's Cave", "Isle of the Dead", True, None],
        ["Isle of the Dead", "Brant's Temple", True, None],
        ["Isle of the Dead", "Boulder Tunnel", False, "shovel"],
        ["Boulder Tunnel", "Stone Treasure Cave", False, "bombs"],
        ["Stone Treasure Cave", "Boulder Tunnel", False, None],
        ["Boulder Tunnel", "IotD Face", True, None],
        ["IotD Face", "Isle of the Dead", False, None],
        ["Brant's Temple", "IotD Crown", True, None],
        ["IotD Crown", "Isle of the Dead", False, None],

        # ================= Isle of Ruins ====================

        ["Ruins SW Port", "Sandy Geozard Cave East", True, None],
        ["Sandy Geozard Cave East", "Sandy Geozard Cave West", True, "ruins_geozards"],
        ["Sandy Geozard Cave West", "Ruins SW Maze Upper", True, None],
        ["Ruins SW Maze Upper", "Ruins SW Port", False, None],
        ["Ruins SW Maze Upper", "Ruins SW Maze Lower", False, "ruins_water"],
        ["Ruins SW Port Cliff", "Ruins SW Maze Upper", False, None],
        ["Ruins SW Maze Lower", "Ruins SW Maze Lower Exit", True, "ruins_water"],
        ["Ruins SW Maze Lower Exit", "Ruins NW Maze Lower Exit", True, None],
        ["Ruins SW Maze Upper", "Ruins NW Maze Upper Exit", True, None],
        ["Ruins SW Maze Lower Water", "Ruins NW Maze Lower Water", True, "ruins_water"],  # Separate the water logic from the transition
            ["Ruins SW Maze Lower", "Ruins SW Maze Lower Water", True, "ruins_water"],
            ["Ruins NW Maze Lower Water", "Ruins NW Maze Lower Chest", True, "ruins_water"],

        ["Ruins NW Maze Lower Exit", "Ruins NW Boulders", False, None],
        ["Ruins NW Maze Upper Exit", "Ruins NW Boulders", False, None],
        ["Ruins NW Boulders", "Ruins NW Dig", False, "shovel"],
        ["Ruins NW Port Cliff", "Ruins NW Maze Lower Chest", False, "ruins_water"],
        ["Ruins NW Boulders", "Ruins NW Across Bridge", True, None],
        ["Ruins NW Boulders", "Bremeur's Temple", True, None],
        ["Bremeur's Temple", "Bremeur's Temple Kings Key", False, "kings_key"],
        ["Bremeur's Temple Kings Key", "Bremeur's Temple Event", False, None],
        ["Ruins NW Boulders", "Ruins NW Port Cliff", False, None],
        ["Ruins NW Port Cliff", "Ruins SW Port Cliff", True, None],
        ["Ruins NW Port Cliff", "Ruins NW Port Cliff Tree", False, "ruins_water"],
        ["Ruins NW Boulders", "Ruins NW Lower", False, "ruins_water"],
        ["Ruins NW Across Bridge", "Ruins NW Cave", True, "ruins_water"],
            ["Ruins NW Cave", "Grassy Treasure Cave", False, "ruins_water"],
            ["Grassy Treasure Cave", "Ruins NW Cave", False, None],
        ["Ruins NW Across Bridge", "Ruins NW Alcove", False, "ruins_water"],
        ["Ruins NW Across Bridge", "Ruins NE Enter Upper", True, None],
        ["Ruins NW Return", "Ruins NW Boulders", False, None],
        ["Ruins NW Across Bridge", "Ruins NW Return", False, "hard_logic"],
        ["Ruins NW Lower", "Ruins NW Lower Water", True, "ruins_water"],
            ["Ruins NE Lower Water North", "Ruins NE Lower", True, "ruins_water"],
            ["Ruins NW Lower Water", "Ruins NE Lower Water North", True, "ruins_water"],

        ["Ruins NE Enter Upper", "Ruins NE Doylan Bridge", False, None],
        ["Ruins NE Doylan Bridge", "Ruins NE Lower", False, "ruins_water"],
        ["Ruins NE Doylan Bridge", "Ruins NE Behind Pyramids", True, "ruins_water"],
        ["Ruins NE Doylan Bridge", "Ruins NE Doylan Bridge North", False, "ruins_stalfos_n"],
        ["Ruins NE Doylan Bridge North", "Ruins NE Doylan Bridge", False, "ruins_stalfos_s"],
        ["Ruins NE Doylan Bridge North", "Ruins NW Return", True, None],
        ["Ruins NE Doylan Bridge", "Doylan's Temple", True, None],
        ["Doylan's Temple", "Doylan's Chamber", True, None],
        ["Ruins NE Lower Water South", "Ruins NW Alcove Water", True, "ruins_water"],
            ["Ruins NW Alcove Water", "Ruins NW Alcove", True, "ruins_water"],
            ["Ruins NE Lower", "Ruins NE Lower Water South", True, "ruins_water"],
        ["Ruins NE Lower", "Ruins NE Behind Pyramids", True, "grapple"],
        ["Ruins NE Lower Water Bay", "Ruins SE Lower Water Bay", True, "ruins_water"],
            ["Ruins NE Lower Water Bay", "Ruins NE Lower", True, "ruins_water"],
            ["Ruins SE Lower Water Bay", "Ruins SE Lower", True, "ruins_water"],
        ["Ruins NE Behind Pyramids Water", "Ruins SE Coast Water", True, "ruins_water"],
            ["Ruins NE Behind Pyramids", "Ruins NE Behind Pyramids Water", True, "ruins_water"],
            ["Ruins SE Coast Water", "Ruins SE Coast", True, "ruins_water"],
        ["Ruins NE Outside Temple", "Ruins NE Behind Pyramids", False, "ruins_water"],
        ["Ruins NE Outside Temple", "MT 1F", False, "ruins_water"],
            ["MT 1F", "Ruins NE Outside Temple", False, None],
        ["Ruins NE Outside Temple", "Ruins NE Geozard Arena", False, "ruins_water"],
        ["Ruins NE Geozard Arena", "Ruins NE Outside Temple", False, "damage"],

        ["Ruins SE Lower Water Wall", "Ruins NE Secret Chest Water", True, "ruins_water"],
            ["Ruins NE Secret Chest Water", "Ruins NE Secret Chest", True, "ruins_water"],
            ["Ruins SE Lower", "Ruins SE Lower Water Wall", True, "ruins_water"],
        ["Ruins SE Lower", "Ruins SE Return Bridge East", True, "ruins_water"],
        ["Ruins SE Return Bridge West", "Ruins SE Return Bridge East", False, "hammer"],
        ["Ruins SE Return Bridge East", "Ruins SE Return Bridge West", False, None],
        ["Ruins SE Lower", "Ruins SE Outside Pyramid", True, "ruins_water"],
            ["Ruins SE Outside Pyramid", "Max's Temple", False, "ruins_water"],
            ["Max's Temple", "Ruins SE Outside Pyramid", False, None],
        ["Ruins SE Return Bridge West", "Ruins SW Port Cliff", True, None],
        ["Ruins SE Lower", "Ruins SE King's Road", False, None],
        ["Ruins SE King's Road Water", "Ruins NE Geozards Water", True, "ruins_water"],
            ["Ruins NE Geozards Water", "Ruins NE Geozard Arena", True, "ruins_water"],
            ["Ruins SE King's Road", "Ruins SE King's Road Water", True, "ruins_water"],

        # ================= Mutoh's Temple ====================

        ["MT 1F", "MT Landing", False, "mutoh_entrance"],
        ["MT Landing", "MT Hammer", False, "hammer"],
        ["MT Hammer", "MT Lower Water", False, "mutoh_water"],
        ["MT Lower Water", "MT BK Chest", False, "mutoh_bk_chest"],
        ["MT Lower Water", "MT B3", False, "mutoh_boss_door"],
        ["MT B3", "Eox", True, None],
        ["MT B3", "MT 1F", False, None],
        ["Eox", "Post Eox", False, "hammer"],
        ["Post Eox", "Post MT", False, None],

        # ================= Maze Island ====================

        ["Maze Island", "Maze Island Minigame", False, "sword"],
        ["Maze Island Minigame", "Maze Island Bomb Chest", False, "explosives"],
        ["Maze Island Minigame", "Maze Island Minigame Normal", False, "bow"],
        ["Maze Island Minigame Normal", "Maze Island Minigame Expert", False, "grapple"],
        ["Maze Island Minigame", "Maze Island Dig", False, "shovel"],

        # ========== Fishing ====================

        ["Frog Warps", "Fishing", False, "fishing_rod"],
        ["Fishing", "Fishing Big Catch Lure", False, "big_catch_lure"],
        ["Fishing", "Fishing Rusty Swordfish", False, "can_catch_rsf"],
        ["Fishing", "Fishing Shadows", False, "swordfish_shadows"],
        ["Fishing", "Fishing Stowfish", False, "ut_can_stowfish"],

        # ========== Salvage ==============

        ["SW Ocean West", "SW Ocean West Salvage", False, "salvage"],
        ["SW Ocean East", "SW Ocean East Salvage", False, "salvage"],
        ["NW Ocean", "NW Ocean Salvage", False, "salvage"],
        ["SE Ocean", "SE Ocean Salvage", False, "salvage"],
        ["NE Ocean", "NE Ocean Salvage", False, "salvage"],
        ["NE Ocean", "NE Ocean Inner", False, "regal_necklace"],
        ["NE Ocean Inner", "NE Ocean", False, None],
        ["NE Ocean Inner", "NE Ocean Salvage Inner", False, "salvage"],
        ["NE Ocean", "NW Ocean Corner Salvage", False, "salvage_behind_bannan"],

        ["SW Ocean West Salvage", "Salvage 1", False, "treasure_map", 1],
        ["SW Ocean East Salvage", "Salvage 2", False, "treasure_map", 2],
        ["NW Ocean Salvage", "Salvage 3", False, "treasure_map", 3],
        ["NW Ocean Corner Salvage", "Salvage 4", False, "treasure_map", 4],
        ["SW Ocean West Salvage", "Salvage 5", False, "treasure_map", 5],
        ["NW Ocean Salvage", "Salvage 6", False, "treasure_map", 6],
        ["NW Ocean Salvage", "Salvage 7", False, "treasure_map", 7],
        ["SW Ocean East Salvage", "Salvage 8", False, "treasure_map", 8],
        ["SW Ocean East Salvage", "Salvage 9", False, "treasure_map", 9],
        ["NW Ocean Salvage", "Salvage 10", False, "treasure_map", 10],
        ["NW Ocean Salvage", "Salvage 11", False, "treasure_map", 11],
        ["SE Ocean Salvage", "Salvage 12", False, "treasure_map", 12],
        ["SE Ocean Salvage", "Salvage 13", False, "treasure_map", 13],
        ["SE Ocean Salvage", "Salvage 14", False, "treasure_map", 14],
        ["SE Ocean Salvage", "Salvage 15", False, "treasure_map", 15],
        ["SE Ocean Salvage", "Salvage 16", False, "treasure_map", 16],
        ["SE Ocean Salvage", "Salvage 17", False, "treasure_map", 17],
        ["SW Ocean East Salvage", "Salvage 18", False, "treasure_map", 18],
        ["NW Ocean Salvage", "Salvage 19", False, "treasure_map", 19],
        ["NW Ocean Corner Salvage", "Salvage 20", False, "treasure_map", 20],
        ["SW Ocean West Salvage", "Salvage 21", False, "treasure_map", 21],
        ["SE Ocean Salvage", "Salvage 22", False, "treasure_map", 22],
        ["SE Ocean Salvage", "Salvage 23", False, "treasure_map", 23],
        ["NE Ocean Salvage", "Salvage 24", False, "treasure_map", 24],
        ["NE Ocean Salvage", "Salvage 25", False, "treasure_map", 25],
        ["NE Ocean Salvage Inner", "Salvage 26", False, "treasure_map", 26],
        ["NE Ocean Salvage", "Salvage 27", False, "treasure_map", 27],
        ["NE Ocean Salvage Inner", "Salvage 28", False, "treasure_map", 28],
        ["NE Ocean Salvage", "Salvage 29", False, "treasure_map", 29],
        ["NE Ocean Salvage", "Salvage 30", False, "treasure_map", 30],
        ["NE Ocean Salvage", "Salvage 31", False, "treasure_map", 31],

        # Goal stuff
        ["SW Ocean East", "Bellumbeck", False, "bellumbeck_quick_finish"],
        ["Bellumbeck", "Beat Bellumbeck", False, "can_beat_bellumbeck"],
        ["Beat Bellumbeck", "Goal", False, None],
        ["Goal", "Goal Event", False, None],  # Event stuff
        ["Goal", "Goal Event Triforce", False, None],  # Event stuff
        ["Goal", "Goal Event Bellumbeck", False, None],  # Event stuff
        ["TotOK B6 Midway", "Goal", False, "goal_midway"],
        ["Menu", "Goal", False, "win_on_metals"],

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
    # UT creates alias regions
    if getattr(multiworld, "generation_is_fake", False):
        from .data.Constants import region_aliases
        from .data.Regions import REGIONS
        alias_logic = []
        for region, aliases in region_aliases.items():
            for alias in aliases:
                alias_logic.append([region, alias, False, None])
        all_logic.append(alias_logic)
        all_logic.append([[entr.entrance_region, entr.name, False, None] for entr in ENTRANCES.values() if entr.name not in REGIONS])

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

if __name__ == "__main__":
    for reg1, reg2, _, func, *args in make_overworld_logic():
        if func not in RULE_DICT:
            print(f"{reg1} => {reg2}")