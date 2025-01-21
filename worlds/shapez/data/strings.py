
class OTHER:
    game_name = "shapez"


class SLOTDATA:
    goal = "goal"
    maxlevel = "maxlevel"
    finaltier = "finaltier"
    req_shapes_mult = "required_shapes_multiplier"
    allow_float_layers = "allow_floating_layers"
    rand_level_req = "randomize_level_requirements"
    rand_upgrade_req = "randomize_upgrade_requirements"
    rand_level_logic = "randomize_level_logic"
    rand_upgrade_logic = "randomize_upgrade_logic"
    throughput_levels_ratio = "throughput_levels_ratio"
    comp_growth_gradient = "complexity_growth_gradient"
    same_late = "same_late_upgrade_requirements"
    toolbar_shuffling = "toolbar_shuffling"
    seed = "seed"
    shapesanity = "shapesanity"

    @staticmethod
    def level_building(number: int) -> str:
        return f"Level building {number}"

    @staticmethod
    def upgrade_building(number: int) -> str:
        return f"Upgrade building {number}"

    @staticmethod
    def phase_length(number: int) -> str:
        return f"Phase {number} length"

    @staticmethod
    def cat_buildings_amount(category: str) -> str:
        return f"{category} category buildings amount"


class GOALS:
    vanilla = "vanilla"
    mam = "mam"
    even_fasterer = "even_fasterer"
    efficiency_iii = "efficiency_iii"


class CATEGORY:
    belt = "Belt"
    miner = "Miner"
    processors = "Processors"
    painting = "Painting"
    belt_low = "belt"
    miner_low = "miner"
    processors_low = "processors"
    painting_low = "painting"
    big = "Big"
    small = "Small"


class OPTIONS:
    logic_vanilla = "vanilla"
    logic_stretched = "stretched"
    logic_quick = "quick"
    logic_random_steps = "random_steps"
    logic_hardcore = "hardcore"
    logic_dopamine = "dopamine"
    logic_dopamine_overflow = "dopamine_overflow"
    logic_vanilla_like = "vanilla_like"
    logic_linear = "linear"
    logic_category = "category"
    logic_category_random = "category_random"
    logic_shuffled = "shuffled"
    sphere_1 = "sphere_1"


class REGIONS:
    menu = "Menu"
    main = "Main"
    levels_1 = "Levels with 1 Building"
    levels_2 = "Levels with 2 Buildings"
    levels_3 = "Levels with 3 Buildings"
    levels_4 = "Levels with 4 Buildings"
    levels_5 = "Levels with 5 Buildings"
    upgrades_1 = "Upgrades with 1 Building"
    upgrades_2 = "Upgrades with 2 Buildings"
    upgrades_3 = "Upgrades with 3 Buildings"
    upgrades_4 = "Upgrades with 4 Buildings"
    upgrades_5 = "Upgrades with 5 Buildings"
    paint = "Painted Shape Achievements"
    cut = "Cut Shape Achievements"
    rotate = "Rotated Shape Achievements"
    stack = "Stacked Shape Achievements"
    store = "Stored Shape Achievements"
    all_buildings = "All Buildings Shapes"
    trash = "Trashed Shape Achievements"
    blueprint = "Blueprint Achievements"
    wiring = "Wiring Achievements"
    mam = "MAM needed"
    full = "Full"
    half = "Half"
    piece = "Piece"
    stitched = "Stitched"
    east_wind = "East Windmill"
    half_half = "Half-Half"
    col_east_wind = "Colorful East Windmill"
    col_half_half = "Colorful Half-Half"
    col_full = "Colorful Full"
    col_half = "Colorful Half"
    uncol = "Uncolored"
    san_paint = "Painted"
    mixed = "Mixed"
    uncol_circle = "Uncolored Circle"
    uncol_square = "Uncolored Square"
    uncol_star = "Uncolored Star"
    uncol_wind = "Uncolored Windmill"

    @staticmethod
    def sanity(processing: str, coloring: str):
        return f"Shapesanity {processing} {coloring}"


class LOCATIONS:
    my_eyes = "My eyes no longer hurt"
    painter = "Painter"
    cutter = "Cutter"
    rotater = "Rotater"
    wait_they_stack = "Wait, they stack?"
    wires = "Wires"
    storage = "Storage"
    freedom = "Freedom"
    the_logo = "The logo!"
    to_the_moon = "To the moon"
    its_piling_up = "It's piling up"
    use_it_later = "I'll use it later"
    efficiency_1 = "Efficiency 1"
    preparing_to_launch = "Preparing to launch"
    spacey = "SpaceY"
    stack_overflow = "Stack overflow"
    its_a_mess = "It's a mess"
    faster = "Faster"
    even_faster = "Even faster"
    get_rid_of_them = "Get rid of them"
    a_long_time = "It's been a long time"
    addicted = "Addicted"
    cant_stop = "Can't stop"
    is_this_the_end = "Is this the end?"
    getting_into_it = "Getting into it"
    now_its_easy = "Now it's easy"
    computer_guy = "Computer Guy"
    speedrun_master = "Speedrun Master"
    speedrun_novice = "Speedrun Novice"
    not_idle_game = "Not an idle game"
    efficiency_2 = "Efficiency 2"
    branding_1 = "Branding specialist 1"
    branding_2 = "Branding specialist 2"
    king_of_inefficiency = "King of Inefficiency"
    its_so_slow = "It's so slow"
    mam = "MAM (Make Anything Machine)"
    perfectionist = "Perfectionist"
    next_dimension = "The next dimension"
    oops = "Oops"
    copy_pasta = "Copy-Pasta"
    ive_seen_that_before = "I've seen that before ..."
    memories = "Memories from the past"
    i_need_trains = "I need trains"
    a_bit_early = "A bit early?"
    gps = "GPS"

    @staticmethod
    def level(number: int, additional: int = 0) -> str:
        if not additional:
            return f"Level {number}"
        elif additional == 1:
            return f"Level {number} Additional"
        else:
            return f"Level {number} Additional {additional}"

    @staticmethod
    def upgrade(category: str, tier: str) -> str:
        return f"{category} Upgrade Tier {tier}"

    @staticmethod
    def shapesanity(number: int) -> str:
        return f"Shapesanity {number}"


class ITEMS:
    cutter = "Cutter"
    cutter_quad = "Quad Cutter"
    rotator = "Rotator"
    rotator_ccw = "Rotator (CCW)"
    rotator_180 = "Rotator (180°)"
    stacker = "Stacker"
    painter = "Painter"
    painter_double = "Double Painter"
    painter_quad = "Quad Painter"
    color_mixer = "Color Mixer"

    belt = "Belt"
    extractor = "Extractor"
    extractor_chain = "Chaining Extractor"
    balancer = "Balancer"
    comp_merger = "Compact Merger"
    comp_splitter = "Compact Splitter"
    tunnel = "Tunnel"
    tunnel_tier_ii = "Tunnel Tier II"
    trash = "Trash"

    belt_reader = "Belt Reader"
    storage = "Storage"
    switch = "Switch"
    item_filter = "Item Filter"
    display = "Display"
    wires = "Wires"
    const_signal = "Constant Signal"
    logic_gates = "Logic Gates"
    virtual_proc = "Virtual Processing"
    blueprints = "Blueprints"

    upgrade_big_belt = "Big Belt Upgrade"
    upgrade_big_miner = "Big Miner Upgrade"
    upgrade_big_proc = "Big Processors Upgrade"
    upgrade_big_paint = "Big Painting Upgrade"
    upgrade_small_belt = "Small Belt Upgrade"
    upgrade_small_miner = "Small Miner Upgrade"
    upgrade_small_proc = "Small Processors Upgrade"
    upgrade_small_paint = "Small Painting Upgrade"

    @staticmethod
    def upgrade(size: str, category: str) -> str:
        return f"{size} {category} Upgrade"

    bundle_blueprint = "Blueprint Shapes Bundle"
    bundle_level = "Level Shapes Bundle"
    bundle_upgrade = "Upgrade Shapes Bundle"

    trap_locked = "Locked Building Trap"
    trap_throttled = "Throttled Building Trap"
    trap_malfunction = "Malfunctioning Trap"
    trap_inflation = "Inflation Trap"
    trap_draining_inv = "Inventory Draining Trap"
    trap_draining_blueprint = "Blueprint Shapes Draining Trap"
    trap_draining_level = "Level Shapes Draining Trap"
    trap_draining_upgrade = "Upgrade Shapes Draining Trap"
