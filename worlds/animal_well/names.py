from enum import Enum


class RegionNames(str, Enum):
    def __str__(self) -> str:
        return self.value

    menu = "Menu"
    fast_travel_fake = "Fast Travel Mid-Warp"  # for the purpose of not putting all the entrances at the starting region
    starting_area = "Squirrel Main"
    bulb_bunny_spot = "Squirrel Bulb Bunny Spot"
    s_disc_area = "Squirrel S. Medal Area"
    starting_after_ghost = "Squirrel After Ghost"
    fast_travel = "Fast Travel Room"
    fast_travel_fish_teleport = "Fast Travel Fish Teleport Spot"
    bird_area = "Bird Area"  # the central portion of the map
    bird_capybara_waterfall = "Bird Capybara Waterfall"  # up and right of the ladder
    bird_below_mouse_statues = "Bird Below Mouse Statues"  # on the way to frog area, need yoyo
    candle_area = "Squirrel Candle Area"
    match_above_egg_room = "Match Above Egg Room"  # its own region since you can use the dog elevator
    bird_flute_chest = "Bird Flute Chest Room"  # since you can technically get weird with the logic here
    water_spike_bunny_spot = "Water Spike Bunny Spot"

    fish_upper = "Fish Upper"  # everything prior to the bubble wand chest
    fish_lower = "Fish Lower"
    fish_boss_1 = "Fish Boss Arena Part 1"  # just the whale
    fish_boss_2 = "Fish Boss Arena Part 2"  # whale + seahorse
    fish_wand_pit = "Fish B.Wand Chest Pit"
    fish_west = "Fish Warp Room"  # after the b. wand chest, rename
    fish_tube_room = "Fish Pipe Maze"  # rename?

    abyss = "Bone Fish Area"
    abyss_lower = "Bone Fish Arena"
    uv_lantern_spot = "UV Lantern Spot"

    bear_area_entry = "Bear Main Entry"
    bear_capybara_and_below = "Bear Main Area"
    bear_future_egg_room = "Bear Future Egg Room"
    bear_chinchilla_song_room = "Bear Chinchilla Song Room"  # where the bunny is
    bear_dark_maze = "Bear Dark Maze"
    bear_chameleon_room_1 = "Bear Chameleon Room 1"  # first chameleon encounter with the chinchilla
    bear_ladder_after_chameleon = "Bear Ladder after Chameleon 1"
    bear_slink_room = "Bear Slink Room"  # the room you get slink
    bear_slink_room_doors = "Bear Slink Room after opening doors"
    bear_transcendental = "Bear Transcendental Egg Room"
    bear_kangaroo_waterfall = "Bear Kangaroo Waterfall and adjacent rooms"  # up left from entry point, need slink
    bear_middle_phone_room = "Bear Middle Phone Room"  # after the previous region, has the fast travel, monkey room
    bear_crow_rooms = "Bear Crow Rooms"  # the room with a lot of crows, the room with 8 crows, and the room with 4 crows
    bear_shadow_egg_spot = "Bear Shadow Egg Chest Spot"  # since you can get here from above with top
    bear_hedgehog_square = "Bear Hedgehog on the Square Room"  # the one where the hedgehog presses 4 buttons
    bear_connector_passage = "Bear Connector Passage"  # connects capybara save room, upper bear
    bear_match_chest_spot = "Bear Match Chest Spot"  # where the match chest is, it's weird okay
    bear_upper_phone_room = "Bear Upper Phone Room"
    bear_above_chameleon = "Bear Above Chameleon Boss"  # right above the chameleon boss before the flame
    bear_chameleon_room_2 = "Bear Chameleon Boss Room before Flame"
    bear_razzle_egg_spot = "Bear Razzle Egg Spot"
    bear_truth_egg_spot = "Bear Truth Egg Spot"
    bear_map_bunny_spot = "Bear Map Bunny Spot"

    dog_area = "Dog Main"
    dog_chinchilla_skull = "Dog Chinchilla Skull Room"
    dog_at_mock_disc = "Dog at Mock Disc Chest"
    dog_upper = "Dog Area Upper"  # rename this variable and name
    dog_upper_past_lake = "Dog Area Upper past Lake"
    dog_upper_above_switch_lines = "Dog Area Upper above Switch Lines"  # rename, that spot where you go up the levels?
    dog_upper_above_switch_lines_to_upper_east = "Dog Area Upper above Switch Lines to Upper East"  # where the button is
    dog_upper_east = "Dog Area Upper East"  # to the right of the area above the switch lines
    bobcat_room = "Bobcat Room"
    chest_on_spikes_region = "Chest on Spikes Region"
    dog_elevator = "Dog Elevator"  # east of the flame
    dog_many_switches = "Dog Switches and Bat"  # west of spike room
    dog_upside_down_egg_spot = "Dog Upside Down Egg Spot"
    dog_bat_room = "Dog Bat Room"
    dog_under_fast_travel_room = "Dog Room under Fast Travel Door Room"
    dog_fast_travel_room = "Dog Room with Fast Travel Door"
    dog_swordfish_lake_ledge = "Dog Left side of Swordfish Lake"
    behind_kangaroo = "Vertical Passage behind Kangaroo Room"
    dog_above_fast_travel = "Dog Above Fast Travel Room"  # has some of those breakout blocks
    dog_mock_disc_shrine = "Dog Mock Disc Shrine"  # and the rooms to the left of it
    kangaroo_room = "Kangaroo Room"
    kangaroo_blocks = "Kangaroo Room Blocks"
    dog_wheel = "Dog Wheel"  # doggo getting swole af
    dog_elevator_upper = "Dog Elevator Upper"  # top of the elevator going up
    dog_elevator_middle = "Dog Elevator Middle" # east of the flame, above the crow slink route

    frog_near_wombat = "Frog Area near Groundhog"  # first part of the frog area after you drop down the hole
    frog_under_ostrich_statue = "Frog Area under Ostrich Statue"  # just the dark room basically
    frog_pre_ostrich_attack = "Frog before Ostrich Attack"  # left of dark room, right of ostrich, above dynamite
    frog_ostrich_attack = "Frog Ostrich Attack"  # and also the little area above it
    frog_worm_shaft_top = "Frog Worm Shaft Top"  # where the fire egg is
    frog_worm_shaft_bottom = "Frog Worm Shaft Bottom"  # save point after ostrich chase
    frog_bird_after_yoyo_1 = "Frog Bird Area after Yoyo 1"  # the first two bird rooms after you get yoyo
    frog_bird_after_yoyo_2 = "Frog Bird Area after Yoyo 2"  # the area after the previous one (rewrite comment)
    frog_dark_room = "Wave Room"  # the dark room with the frog, and also the wave room
    frog_ruby_egg_ledge = "Ruby Egg Ledge"  # the ledge with the ruby egg in the frog dark room
    frog_east_of_fast_travel = "Frog East of Fast Travel"  # one screen to the right of the fast travel spot
    frog_elevator_and_ostrich_wheel = "Frog Elevator and Ostrich Wheel Section"  # interdependent, so one big region
    frog_travel_egg_spot = "Frog Travel Egg Spot"

    hippo_entry = "Hippo Entry"  # the beginning of the end
    hippo_manticore_room = "Hippo Manticore Room"  # the 4 rooms you evade the manticore in for the first ending
    hippo_skull_room = "Hippo Skull Room"  # B. B. Wand and the skull pile
    hippo_fireworks = "Hippo Fireworks Room"  # the first ending

    home = "Home"
    barcode_bunny = "Barcode Bunny"  # barcode bunny is gotten in two places
    top_of_the_well = "Top of the Well"  # where the warp song takes you, right of the house
    chocolate_egg_spot = "Chocolate Egg Spot"
    value_egg_spot = "Value Egg Spot" 
    match_center_well_spot = "Center Well Match Spot"  # in the shaft, across from chocolate egg
    zen_egg_spot = "Zen Egg Spot"  # contains zen egg and universal basic egg


class ItemNames(str, Enum):
    def __str__(self) -> str:
        return self.value

    # major unique items
    bubble = "B. Wand"
    flute = "Animal Flute"
    slink = "Slink"
    yoyo = "Yoyo"
    m_disc = "Mock Disc"
    disc = "Disc"
    lantern = "Lantern"
    ball = "B. Ball"
    remote = "Remote"
    uv = "UV Lantern"
    wheel = "Wheel"
    top = "Top"
    bubble_long_real = "B.B. Wand"
    firecrackers = "Firecrackers"
    house_key = "House Key"
    office_key = "Office Key"
    fanny_pack = "F. Pack"
    k_shard = "K. Shard"
    k_medal = "K. Medal"  # a fake item. 3 K. Shards exist in pool
    s_medal = "S. Medal"
    e_medal = "E. Medal"

    match = "Match"
    matchbox = "Matchbox"  # potentially an item if we want to simplify logic

    key = "Key"
    key_ring = "Key Ring"  # potentially an item if we want to simplify logic

    # flames
    blue_flame = "B. Flame"  # seahorse
    green_flame = "G. Flame"  # ostritch
    pink_flame = "P. Flame"  # ghost dog
    violet_flame = "V. Flame"  # chameleon

    # eggs, in a particular order but not one that actually matters
    egg_forbidden = "Forbidden Egg"
    egg_vanity = "Vanity Egg"
    egg_reference = "Reference Egg"
    egg_brown = "Brown Egg"
    egg_service = "Egg As A Service"
    egg_upside_down = "Upside Down Egg"
    egg_red = "Red Egg"
    egg_friendship = "Friendship Egg"
    egg_plant = "Plant Egg"
    egg_future = "Future Egg"
    egg_raw = "Raw Egg"
    egg_evil = "Evil Egg"
    egg_orange = "Orange Egg"
    egg_depraved = "Depraved Egg"
    egg_sour = "Sour Egg"
    egg_sweet = "Sweet Egg"
    egg_crystal = "Crystal Egg"
    egg_big = "Big Egg"
    egg_pickled = "Pickled Egg"
    egg_chocolate = "Chocolate Egg"
    egg_post_modern = "Post Modern Egg"
    egg_truth = "Truth Egg"
    egg_transcendental = "Transcendental Egg"
    egg_swan = "Swan Egg"
    egg_shadow = "Shadow Egg"
    egg_chaos = "Chaos Egg"
    egg_value = "Value Egg"
    egg_zen = "Zen Egg"
    egg_razzle = "Razzle Egg"
    egg_lf = "Laissez-faire Egg"
    egg_universal = "Universal Basic Egg"
    egg_rain = "Rain Egg"
    egg_holiday = "Holiday Egg"
    egg_virtual = "Virtual Egg"
    egg_great = "Great Egg"
    egg_mystic = "Mystic Egg"
    egg_normal = "Normal Egg"
    egg_dazzle = "Dazzle Egg"
    egg_magic = "Magic Egg"
    egg_ancient = "Ancient Egg"
    egg_galaxy = "Galaxy Egg"
    egg_sunset = "Sunset Egg"
    egg_goodnight = "Goodnight Egg"
    egg_brick = "Brick Egg"
    egg_clover = "Clover Egg"
    egg_neon = "Neon Egg"
    egg_ice = "Ice Egg"
    egg_iridescent = "Iridescent Egg"
    egg_gorgeous = "Gorgeous Egg"
    egg_dream = "Dream Egg"
    egg_travel = "Travel Egg"
    egg_planet = "Planet Egg"
    egg_bubble = "Bubble Egg"
    egg_moon = "Moon Egg"
    egg_promise = "Promise Egg"
    egg_fire = "Fire Egg"
    egg_sapphire = "Sapphire Egg"
    egg_ruby = "Ruby Egg"
    egg_rust = "Rust Egg"
    egg_jade = "Jade Egg"
    egg_desert = "Desert Egg"
    egg_scarlet = "Scarlet Egg"
    egg_obsidian = "Obsidian Egg"
    egg_golden = "Golden Egg"

    egg_65 = "65th Egg"

    # event items
    activated_bird_fast_travel = "Activated Bird Fast Travel"
    activated_bear_fast_travel = "Activated Bear Fast Travel"
    activated_frog_fast_travel = "Activated Frog Fast Travel"
    activated_squirrel_fast_travel = "Activated Squirrel Fast Travel"
    activated_fish_fast_travel = "Activated Fish Fast Travel"
    activated_dog_fast_travel = "Activated Dog Fast Travel"
    activated_hippo_fast_travel = "Activated Hippo Fast Travel"
    activated_bonefish_fast_travel = "Activated Bone Fish Fast Travel"
    defeated_chameleon = "Defeated Chameleon"
    switch_for_post_modern_egg = "Activated Switch for Post Modern Egg"
    switch_next_to_bat_room = "Activated Switch next to Bat Room"  # for getting up to the fast travel spot in dog area
    dog_wheel_flip = "Flipped Dog Wheel"

    victory = "Victory"

    event_candle_first = "Lit the First Candle"  # rename
    event_candle_dog_dark = "Lit the Dog Area's Dark Room Candle"
    event_candle_dog_switch_box = "Lit the Dog Area's Candle in the Switch Box"
    event_candle_dog_many_switches = "Lit the Dog Area's Candle by Many Switches"
    event_candle_dog_disc_switches = "Lit the Dog Area's Candle in Disc Switch Maze"
    event_candle_dog_bat = "Lit the Dog Area's Candle in the Bat Room"
    event_candle_penguin = "Lit the Candle by the Penguins"
    event_candle_frog = "Lit the Frog Area Candle"
    event_candle_bear = "Lit the Bear Area Candle"

    can_use_matches = "Can Use Matches"  # for when you get all of the matches, consumables logic is cool
    can_use_keys = "Can Use Keys"  # for when you get all of the keys, consumables logic is cool

    # fake items, for the purposes of rules
    bubble_short = "Bubble Jumping - Short"
    bubble_long = "Bubble Jumping - Long"
    can_break_spikes = "Can Break Spikes"
    can_break_spikes_below = "Can Break Spikes Below"  # can break spikes but without disc basically
    can_open_flame = "Can Open Flame"  # you can break this with the flute and other items, need to verify which
    disc_hop = "Disc Jumping"  # hopping on a disc in midair without it bouncing first
    disc_hop_hard = "Consecutive Disc Jumps"  # hopping on a disc multiple times, or after a bubble jump
    wheel_hop = "Wheel Hop"  # expanding and retracting wheel midair to grant a double jump
    wheel_climb = "Wheel Climb"  # hugging a wall and mashing the jump button to get vertical
    wheel_hard = "Advanced Wheel Techniques"  # using other wheel exploits, such as wall stalls, to get access to areas that wheel jumps/climbs can't do alone
    flute_jump = "Flute Jumps"  # use flute as you are sliding off of a ledge to effectively extend coyote time
    can_distract_dogs = "Can Distract Dogs"
    can_defeat_ghost = "Can Defeat Ghost"
    # rename tanking_damage's string when we have enough spots to make it viable as an option or something
    tanking_damage = "Tanking Damage"  # for spots you can get to by taking up to 3 hearts of damage
    ball_trick_easy = "Ball Throwing - Easy"  # logic for throwing the ball at anything other than a block or a spike
    ball_trick_medium = "Ball Throwing - Medium"  # at the moment, does NOT imply the existence of ball. Ball needs to be written separately in logic
    ball_trick_hard = "Ball Throwing - Hard"
    obscure_tricks = "Obscure Tricks"  # solutions that are weird but not necessarily difficult
    precise_tricks = "Precise Tricks"  # solutions that are difficult but not necessarily weird
    water_bounce = "Water Bounce"  # tricks that use Yoyo, B.Ball, or some other way to generate a splash effect to bounce off the water

    # songs, to potentially be randomized
    song_home = "Top of the Well Song"
    song_egg = "Egg Song"
    song_chinchilla = "Chinchilla Song"  # the warp to the chinchilla vine platform bunny
    song_bobcat = "Bobcat Song"  # idk what we should do with this, but it kinda sucks as it is
    song_fish = "Skeleton Fish Song"  # teleports you to the right side of the lower screen of the fast travel room
    song_barcode = "Barcode Song"  # for barcode bunny


class LocationNames(str, Enum):
    def __str__(self) -> str:
        return self.value

    # major unique items
    map_chest = "Map Chest - R9C10"
    stamp_chest = "Stamp Chest - R7C8"
    pencil_chest = "Pencil Chest - R7C7"

    b_wand_chest = "B. Wand Chest - R10C2"
    flute_chest = "Animal Flute Chest - R7C6"
    slink_chest = "Slink Chest - R5C12"
    yoyo_chest = "Yoyo Chest - R15C13"
    mock_disc_chest = "Mock Disc Chest - R5C7"
    disc_spot = "Wolf Disc Shrine - R6C7"
    lantern_chest = "Lantern Chest - R11C10"
    b_ball_chest = "B. Ball Chest - R4C1"
    remote_chest = "Remote Chest - R13C7"
    uv_lantern_chest = "UV Lantern Chest - R16C1"
    wheel_chest = "Wheel Chest - R12C1"
    top_chest = "Top Chest - R7C7"
    bb_wand_chest = "B.B. Wand Chest - R15C5"
    # firecracker_first = "Pick Up Firecrackers"
    fanny_pack_chest = "Fanny Pack Chest - R16C7"
    key_house = "House Key Drop - R16C6"
    key_office = "Office Key Chest - R6C9"
    # medal_k = "K. Medal Shard Bag"  # you need three to open the kangaroo door
    medal_s = "S. Medal Chest - R6C12"
    medal_e = "E. Medal Chest - R14C5"

    # minor unique items
    mama_cha = "Mama Cha Chest - R3C5"  # the same place as the barcode bunny at grass bowl

    # match chests
    match_start_ceiling = "Match in Tutorial Chest - R10C6"
    match_fish_mural = "Match in Fish Mural Room Chest - R8C7"
    match_dog_switch_bounce = "Match in Switch-Bounce Room Chest - R3C7"  # in that spot where you throw between the levers
    match_dog_upper_east = "Match by Dog Fish Pipe Chest - R4C9"
    match_bear = "Match in Bear Area - R3C12"
    match_above_egg_room = "Match Above Egg Room - R6C9"  # the one to the right of the dog lower entrance
    match_center_well = "Match in Center Well Chest - R4C10"  # the one high up in the shaft
    match_guard_room = "Match in Guard Room Chest - R12C11"
    match_under_mouse_statue = "Match under Mouse Statue - R9C13"  # east bird area, need yoyo to get in

    # candle checks
    candle_first = "Squirrel First Candle - R10C9"  # the obvious first one
    candle_dog_dark = "Dog Dark Room Candle - R6C5"  # the one in the dark room a few rooms after your first dog encounter
    candle_dog_switch_box = "Dog Boxed Candle - R4C5"
    candle_dog_many_switches = "Dog Candle in Many Switches Room - R4C3"
    candle_dog_disc_switches = "Dog Candle in Disc Switch Maze - R3C7"
    candle_dog_bat = "Dog Candle in Bat Room - R3C3"
    candle_fish = "Fish Candle in Penguin Room - R10C4"
    candle_frog = "Frog Candle Switch Carousel - R10C15"  # to screens to the right of the wombat save point
    candle_bear = "Bear Candle in Dark Maze - R6C14"

    # candle checks - event versions
    candle_first_event = "Squirrel First Candle - R10C9 Event"  # the obvious first one
    candle_dog_dark_event = "Dog Dark Room Candle - R6C5 Event"  # in the dark room a few rooms after your first dog encounter
    candle_dog_switch_box_event = "Dog Boxed Candle - R4C5 Event"
    candle_dog_many_switches_event = "Dog Candle in Many Switches Room - R4C3 Event"
    candle_dog_disc_switches_event = "Dog Candle in Disc Switch Maze - R3C7 Event"
    candle_dog_bat_event = "Dog Candle in Bat Room - R3C3 Event"
    candle_fish_event = "Fish Candle in Penguin Room - R10C4 Event"
    candle_frog_event = "Frog Candle Switch Carousel - R10C15 Event"  # to screens to the right of the wombat save point
    candle_bear_event = "Bear Candle in Dark Maze - R6C14 Event"

    # key chests
    key_bear_lower = "Key Chest in Lower Bear - R7C16"  # early in the green area
    key_bear_upper = "Key Chest in Upper Bear - R5C14"  # get the chest to land on the chinchilla, maybe rename these two
    key_chest_mouse_head_lever = "Key Chest by Mouse Head Hitting Lever - R9C12"  # rename definitely
    key_frog_guard_room_west = "Key Chest in West Frog Guard Room - R12C12"
    key_frog_guard_room_east = "Key Chest in East Frog Guard Room - R12C14"
    key_dog = "Key Chest in Dog with Chinchilla Crank - R4C2"  # maybe rename

    # flames
    flame_blue = "B. Flame - R14C2"  # fish area
    flame_green = "G. Flame - R16C16"  # frog area
    flame_pink = "P. Flame - R2C9"  # dog area
    flame_violet = "V. Flame - R2C11"  # bear area

    # eggs, not in any particular order
    egg_forbidden = "Forbidden Egg Chest - R2C1"  # swordfish lake
    egg_vanity = "Vanity Egg Chest - R3C1"  # kangaroo breakout
    egg_reference = "Reference Egg Chest - R1C2"  # dog region disc with fans puzzle
    egg_brown = "Brown Egg Chest - R1C3"  # next to Reference Egg
    egg_service = "Egg As A Service Chest - R3C2"  # behind Bat room
    egg_upside_down = "Upside Down Egg Chest - R4C3"  # dog many switches room
    egg_red = "Red Egg Chest - R5C2"  # dog double chinchilla puzzle
    egg_friendship = "Friendship Egg Chest - R6C2"  # dark room from pipe maze
    egg_plant = "Plant Egg Chest - R5C1"  # two boxes with disc puzzle
    egg_future = "Future Egg Chest - R6C1"  # dark room behind chinchilla vines
    egg_raw = "Raw Egg Chest - R1C6"  # dog slinky box puzzle
    egg_evil = "Evil Egg Chest - R4C6"  # turtle flute pool
    egg_orange = "Orange Egg Chest - R5C6"  # dog egg under telephone
    egg_depraved = "Depraved Egg Chest - R3C7"  # dog switch maze
    egg_sour = "Sour Egg Chest - R5C9"  # daschund tunnels
    egg_sweet = "Sweet Egg Chest - R4C9"  # above dog wheel
    egg_crystal = "Crystal Egg Chest - R16C4"  # dog wheel puzzle at bottom of the map
    egg_big = "Big Egg Chest - R1C10b"  # near Mock Disc Shrine
    egg_pickled = "Pickled Egg Chest - R1C10a"  # hidden spot in well wall
    egg_chocolate = "Chocolate Egg Chest - R4C10"  # behind well wall switch blocks
    egg_post_modern = "Post Modern Egg Chest - R5C10"  # well wall behind top dirt
    egg_truth = "Truth Egg Chest - R6C11"  # bear above bottom left crow
    egg_transcendental = "Transcendental Egg Chest - R6C12"  # below slink chest
    egg_swan = "Swan Egg Chest - R1C13"  # bear next to Chameleon final boss entrance
    egg_shadow = "Shadow Egg Chest - R2C16"  # near above arrow lift bridge
    egg_chaos = "Chaos Egg Chest - R3C16"  # monke room
    egg_value = "Value Egg Chest - R4C16"  # bear top hedgehog buttons
    egg_zen = "Zen Egg Chest - R5C14"  # bear next to upper key
    egg_razzle = "Razzle Egg Chest - R7C14"  # behind lowest chameleon
    egg_lf = "Laissez-faire Egg Chest - R5C13b"  # bear spook chinchilla room. Internal name may be bad but the full name is worse.
    egg_universal = "Universal Basic Egg Chest - R5C13a"  # next to Zen Egg
    egg_rain = "Rain Egg Chest - R7C9b"  # top dirt outside egg house
    egg_holiday = "Holiday Egg Chest - R7C9a"  # alcove outside egg house
    egg_virtual = "Virtual Egg Chest - R8C8"  # behind Fish Mural switch blocks
    egg_great = "Great Egg Chest - R9C7"  # after flamingos, not to be confused with Big Egg
    egg_mystic = "Mystic Egg Chest - R7C5"  # top of bubble column room
    egg_normal = "Normal Egg Chest - R9C4"  # betwen bubble rooms
    egg_dazzle = "Dazzle Egg Chest - R8C3"  # fish bubble puzzle by top telephone
    egg_magic = "Magic Egg Chest - R7C2"  # fish pipe maze
    egg_ancient = "Ancient Egg Chest - R7C1"  # fish top left room
    egg_galaxy = "Galaxy Egg Chest - R10C1"  # fish below warp room
    egg_sunset = "Sunset Egg Chest - R10C2"  # above B Wand Chest
    egg_goodnight = "Goodnight Egg Chest - R10C4"  # first penguin room
    egg_brick = "Brick Egg Chest - R13C5"  # fish wheel rooms
    egg_clover = "Clover Egg Chest - R12C5"  # left of start
    egg_neon = "Neon Egg Chest - R13C6"  # snake area breakout reward
    egg_ice = "Ice Egg Chest - R11C8"  # top of snake area
    egg_iridescent = "Iridescent Egg Chest - R13C8"  # snake game reward
    egg_gorgeous = "Gorgeous Egg Chest - R9C9"  # above first candle
    egg_dream = "Dream Egg Chest - R10C12"  # below mouse head lever key
    egg_travel = "Travel Egg Chest - R10C13"  # behind Groundhog locked door
    egg_planet = "Planet Egg Chest - R9C13"  # hidden behind spikes by mouse head auto-lever
    egg_bubble = "Bubble Egg Chest - R11C14"  # dark room below mouse statue
    egg_moon = "Moon Egg Chest - R9C16"  # mouse head spam room
    egg_promise = "Promise Egg Chest - R10C16"  # three ghost birds in mouse area
    egg_fire = "Fire Egg Chest - R11C11"  # other side of chasm to frog area
    egg_sapphire = "Sapphire Egg Chest - R14C12"  # below left ghost birds in frog area
    egg_ruby = "Ruby Egg Chest - R14C13"  # below right ghost birds in frog area
    egg_rust = "Rust Egg Chest - R13C13"  # between the sapphire and ruby eggs
    egg_jade = "Jade Egg Chest - R14C14"  # annoying light curve puzzle
    egg_desert = "Desert Egg Chest - R11C16"  # top of rat lab
    egg_scarlet = "Scarlet Egg Chest - R13C16"  # by the momma cat, in spikes
    egg_obsidian = "Obsidian Egg Chest - R14C15"  # behind fish pipe to lower rat lab
    egg_golden = "Golden Egg Chest - R16C11"  # ostrich wheel puzzle

    egg_65 = "65th Egg Chest - R7C7"  # move to Major Items if Eggsanity becomes a setting

    # bnuuy
    bunny_mural = "Community Bunny - R8C12"
    bunny_map = "Doodle Bunny - R3C11"
    bunny_uv = "Invisible Bunny"
    bunny_fish = "Fish Bunny - R9C7"
    bunny_face = "Face Bunny - R11C6"
    bunny_crow = "Singing Bunny - R2C14"
    bunny_duck = "Illusion Bunny - R8C11"
    bunny_dream = "Imaginary Bunny"
    bunny_lava = "Lava Bunny - R3C6"  # floor is lava
    bunny_tv = "Flashing Bunny - R16C7"
    bunny_ghost_dog = "Statue Bunny - R4C13"  # ghost dog bunny
    bunny_disc_spike = "Disc Spike Bunny - R1C1"
    bunny_water_spike = "Water Spike Bunny - R9C9"
    bunny_barcode = "Paper Bunny - R3C5"  # printer or barcode both get you it
    bunny_chinchilla_vine = "Chinchilla Bunny - R6C1"  # the one where the code is covered by vines
    bunny_file_bud = "Flowering Bunny - R10C5"  # bunny from file start codes

    # event locations
    activate_bird_fast_travel = "Activate Bird Fast Travel"
    activate_bear_fast_travel = "Activate Bear Fast Travel"
    activate_frog_fast_travel = "Activate Frog Fast Travel"
    activate_squirrel_fast_travel = "Activate Squirrel Fast Travel"
    activate_fish_fast_travel = "Activate Fish Fast Travel"
    activate_dog_fast_travel = "Activate Dog Fast Travel"
    activate_hippo_fast_travel = "Activate Hippo Fast Travel"
    activate_bonefish_fast_travel = "Activate Bone Fish Fast Travel"
    defeated_chameleon = "Defeated Chameleon"
    switch_for_post_modern_egg = "Switch for Post Modern Egg"
    switch_next_to_bat_room = "Switch next to Bat Room"  # for getting up to the fast travel spot in dog area
    dog_wheel_flip = "Can Flip Dog Wheel"  # item for you having access to the dog wheel
    light_all_candles = "Light All Candles"
    got_all_matches = "Received All Matches"  # for when you get all of the matches, consumables logic is cool
    got_all_keys = "Received All Keys"  # for when you get all of the keys, consumables logic is cool
    upgraded_wand = "Upgraded to B.B. Wand"  # for when you get your second b wand, this is a hack
    k_medal = "Assembled the K. Medal"
    kangaroo_first_spot = "Kangaroo First Spot"  # first spot the kangaroo appears
    victory_first = "Fireworks Launched"
    victory_egg_hunt = "Final Egg Door Opened"

    # fruits, by row and column, top left room is R1C1
    fruit_0 = "Big Blue Fruit before Disc Spike Bunny - R1C1a"  # big blue fruit, disc spike room
    fruit_1 = "Big Blue Fruit after Disc Spike Bunny - R1C1b"  # big blue fruit, disc spike room
    fruit_2 = "Pink Fruit by Brown Egg Chest - R1C3"
    fruit_3 = "Blue Fruit above Dog Fast Travel - R1C4"  # blue fruit
    fruit_4 = "Blue Fruit by Raw Egg Puzzle Entrance - R1C6a"  # blue fruit
    fruit_5 = "Pink Fruit below Raw Egg Puzzle Entrance - R1C6b"
    fruit_6 = "Pink Fruit left of Mock Disc Shrine - R1C7"
    fruit_7 = "Blue Fruit in Top of Dog Elevator - R1C9"  # blue fruit
    fruit_8 = "Pink Fruit in Bear Upper Phone Room Left - R1C11a"
    fruit_9 = "Pink Fruit in Bear Upper Phone Room Right - R1C11b"
    fruit_10 = "Pink Fruit right of Otters - R1C15"
    fruit_11 = "Pink Fruit by Swordfish Lake - R2C3"
    fruit_12 = "Pink Fruit by Dog Fast Travel - R2C4"
    fruit_13 = "Blue Fruit by P. Flame - R2C9"  # blue fruit
    fruit_14 = "Pink Fruit in Dog Elevator near P. Flame Right - R2C10"
    fruit_15 = "Blue Fruit by V. Flame - R2C11"  # blue fruit
    fruit_16 = "Pink Fruit in Second Chameleon Fight - R2C12"
    fruit_17 = "Pink Fruit in Bat Room - R3C3"
    fruit_18 = "Pink Fruit by Barcode Bunny - R3C5"
    fruit_19 = "Blue Fruit in Dog Switch Maze - R3C7"  # blue fruit
    fruit_20 = "Pink Fruit right of Dog Switch Maze Left - R3C8a"
    fruit_21 = "Pink Fruit right of Dog Switch Maze Right - R3C8b"
    fruit_22 = "Pink Fruit in Dog Elevator near P. Flame Left - R3C10"
    fruit_23 = "Pink Fruit in Bear Middle Phone Room - R3C12"
    fruit_24 = "Pink Fruit by Monkey - R3C16"
    fruit_25 = "Blue Fruit in Kangaroo Room Hand - R4C1a"  # blue fruit upper
    fruit_26 = "Blue Fruit in Kangaroo Room Tail - R4C1b"  # blue fruit lower
    fruit_27 = "Pink Fruit in Kangaroo Room Foot - R4C1c"
    fruit_28 = "Pink Fruit by Turtle Pool - R4C6"
    fruit_29 = "Pink Fruit before Bear Middle Phone Room - R4C11"
    fruit_30 = "Pink Fruit by Statue Bunny - R4C13"
    fruit_31 = "Blue Fruit in Capybara Room Top Left - R4C15a"  # blue fruit top left
    fruit_32 = "Blue Fruit in Capybara Room Top Right - R4C15b"  # blue fruit top right
    fruit_33 = "Pink Fruit in Capybara Room Bottom Right - R4C15c"  # pink fruit bottom right
    fruit_34 = "Pink Fruit in Capybara Room Bottom Left - R4C15d"  # pink fruit bottom left
    fruit_35 = "Blue Fruit above Plant Egg Chest - R5C1"  # blue fruit
    fruit_36 = "Pink Fruit right of Chinchilla Skull Room - R5C3"
    fruit_37 = "Pink Fruit before Mock Disc Chest - R5C4"
    fruit_38 = "Pink Fruit in Mock Disc Phone Room - R5C6"
    fruit_39 = "Blue Fruit by Dog Wheel - R5C9"  # blue fruit
    fruit_40 = "Blue Fruit above Bear Kangaroo Waterfall - R5C11"  # blue fruit
    fruit_41 = "Blue Fruit by Universal Basic Egg Chest - R5C13"  # blue fruit
    fruit_42 = "Pink Fruit in Dog Dark Room - R6C5"
    fruit_43 = "Blue Fruit after Dachshund Tunnels - R6C9a"  # blue fruit
    fruit_44 = "Pink Fruit above Egg Room - R6C9b"
    fruit_45 = "Pink Fruit before Truth Egg - R6C10a"
    fruit_46 = "Pink Fruit in Bottom of Dog Elevator - R6C10b"
    fruit_47 = "Pink Fruit by Bear Kangaroo Waterfall - R6C11"
    fruit_48 = "Blue Fruit after First Chameleon Fight - R6C12"  # blue fruit
    fruit_49 = "Blue Fruit in Bear Dark Maze Right - R6C14a"  # blue fruit, verified
    fruit_50 = "Pink Fruit in Bear Dark Maze Left - R6C14b"
    fruit_51 = "Pink Fruit below Capybara Room - R6C15"
    fruit_52 = "Pink Fruit in Chinchilla Vines Room - R6C16"
    fruit_53 = "Blue Fruit by Ancient Egg Chest Right - R7C1a"  # blue fruit, verified
    fruit_54 = "Pink Fruit by Ancient Egg Chest Left - R7C1b"
    fruit_55 = "Pink Fruit in Fish Pipe Maze Left - R7C2"
    fruit_56 = "Blue Fruit in Fish Pipe Maze Right - R7C3a"  # blue fruit, verified
    fruit_57 = "Pink Fruit in Fish Pipe Maze Middle - R7C3b"
    fruit_58 = "Pink Fruit by Fireball Thrower - R7C4"
    fruit_59 = "Pink Fruit by Flute Chest - R7C6"
    fruit_60 = "Blue Fruit behind Entry Chameleon - R7C14"  # blue fruit
    fruit_61 = "Pink Fruit left of Lower Bear Key Room - R7C15"
    fruit_62 = "Pink Fruit by Lower Bear Key Chest - R7C16"
    fruit_63 = "Pink Fruit above Fish Fast Travel - R8C1"
    fruit_64 = "Pink Fruit in Fish Upper Phone Room Top - R8C2a"
    fruit_65 = "Pink Fruit in Fish Upper Phone Room Bottom - R8C2b"
    fruit_66 = "Pink Fruit Left of Hub Left - R8C9a"
    fruit_67 = "Pink Fruit Left of Hub Right - R8C9b"
    fruit_68 = "Pink Fruit by Mural Bunny - R813"
    fruit_69 = "Pink Fruit by Fish Fast Travel - R9C1"
    fruit_70 = "Pink Fruit below Fish Upper Phone Room Top - R9C2"
    fruit_71 = "Pink Fruit before First Seahorse Fight - R9C3a"
    fruit_72 = "Blue Fruit below Fish Upper Phone Room Bottom - R9C3b"  # blue fruit, verified
    fruit_73 = "Pink Fruit in Bottom Left of Fish Bubble Column - R9C4"
    fruit_74 = "Pink Fruit in Bottom Right of Fish Bubble Column - R9C5"
    fruit_75 = "Big Blue Fruit after Cranes - R9C7"  # big blue fruit, right of cranes
    fruit_76 = "Pink Fruit by Water Spike Bunny - R9C9"
    fruit_77 = "Pink Fruit by Planet Egg Chest Left - R9C13a"
    fruit_78 = "Pink Fruit by Planet Egg Chest Right - R9C13b"
    fruit_79 = "Pink Fruit by First Mouse Head Hitting Lever - R9C14"
    fruit_80 = "Pink Fruit by Frog Switch Carousel Top - R9C15"
    fruit_81 = "Blue Fruit by B. Wand Chest - R10C2"  # blue fruit
    fruit_82 = "Pink Fruit by Penguin Candle Top - R10C4a"
    fruit_83 = "Blue Fruit by Penguin Candle Bottom - R10C4b"  # blue fruit
    fruit_84 = "Pink Fruit above First Ostrich Fight - R10C12"
    fruit_85 = "Blue Fruit behind Groundhog - R10C13a"  # blue fruit, verified
    fruit_86 = "Pink Fruit by Groundhog - R10C13b"
    fruit_87 = "Pink Fruit by Fish Lower Phone Room - R11C3"
    fruit_88 = "Blue Fruit in Miasma Above Lantern Chest - R11C10a"  # blue fruit, verified
    fruit_89 = "Pink Fruit by Lantern Chest - R11C10b"
    fruit_90 = "Blue Fruit after First Ostrich Fight - R11C11"  # blue fruit
    fruit_91 = "Pink Fruit in First Ostrich Fight - R11C12"
    fruit_92 = "Blue Fruit by Bubble Egg Chest - R11C14"  # blue fruit
    fruit_93 = "Pink Fruit by Frog Switch Carousel Bottom - R11C15"
    fruit_94 = "Pink Fruit in Frog Between Guard Rooms Top - R12C13a"
    fruit_95 = "Pink Fruit in Frog Between Guard Rooms Bottom - R12C13b"
    fruit_96 = "Pink Fruit in Frog East Guard Room - R12C14"
    fruit_97 = "Pink Fruit above Frog Kangaroo Encounter Left - R12C15"
    fruit_98 = "Pink Fruit above Frog Kangaroo Encounter Right - R12C16"
    fruit_99 = "Blue Fruit in Whale Fight - R13C2"  # blue fruit, beware of whale
    fruit_100 = "Blue Fruit by Breakout Game Left - R13C6a"  # blue fruit, verified
    fruit_101 = "Pink Fruit above Remote Chest - R13C6b"
    fruit_102 = "Pink Fruit by Breakout Game Right - R13C6c"
    fruit_103 = "Pink Fruit in Manticore Room Left - R14C8"
    fruit_104 = "Pink Fruit in Manticore Room Right - R14C9"
    fruit_105 = "Big Blue Fruit behind Manticore Wheel - R14C10"  # big blue fruit, in manticore area
    fruit_106 = "Pink Fruit by Groveling Toad - R14C13"
    fruit_107 = "Pink Fruit by Rat Elevators - R14C16"
    fruit_108 = "Pink Fruit in Bonefish Abyss - R15C3"
    fruit_109 = "Pink Fruit in Frog Worm Shaft Bottom - R15C11"
    fruit_110 = "Pink Fruit by Caged Cats - R15C15"
    fruit_111 = "Blue Fruit by Fireworks - R16C6"  # blue fruit, right next to fireworks box
    fruit_112 = "Pink Fruit right of Second Ostrich Fight - R16C15"
    fruit_113 = "Pink Fruit by G. Flame Top - R16C16a"
    fruit_114 = "Blue Fruit by G. Flame Bottom - R16C16b"  # blue fruit, verified
