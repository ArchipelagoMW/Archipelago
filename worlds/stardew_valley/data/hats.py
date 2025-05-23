all_hats = []
all_considered_hats = []


class HatDifficulty:
    easy = 0
    easy_island = 1
    tailoring = 2
    tailoring_island = 3
    medium = 4
    medium_island = 5
    difficult_or_rng = 6
    difficult_or_rng_island = 7
    near_perfection = 8
    post_perfection = 9
    impossible = 999  # For that one chinese-version only hat


class Hat:
    name: str
    difficulty: int
    consider_in_logic: bool = True
    # consider_in_logic exists as a temporary measure because I don't feel like writing out the logic for every single hat at this stage,
    # and I only need some of them for the meme bundle

    def __init__(self, name: str, difficulty: int, consider_in_logic: bool = True):
        self.name = name
        self.difficulty = difficulty
        self.consider_in_logic = consider_in_logic

    def __repr__(self) -> str:
        return f"{self.name} (Difficulty: {self.difficulty})"


def hat(name: str, difficulty: int, consider_in_logic: bool = True) -> Hat:
    hat = Hat(name, difficulty, consider_in_logic)
    all_hats.append(hat)
    if consider_in_logic:
        all_considered_hats.append(hat)
    return hat


class Hats:
    concerned_ape_mask = hat("???", HatDifficulty.post_perfection, False)
    abigails_bow = hat("Abigail's Bow", HatDifficulty.medium, False)
    arcane_hat = hat("Arcane Hat", HatDifficulty.difficult_or_rng, False)
    archers_cap = hat("Archer's Cap", HatDifficulty.near_perfection, False)
    beanie = hat("Beanie", HatDifficulty.tailoring, False)
    blobfish_mask = hat("Blobfish Mask", HatDifficulty.tailoring, False)
    blue_bonnet = hat("Blue Bonnet", HatDifficulty.medium)
    blue_bow = hat("Blue Bow", HatDifficulty.easy, False)
    blue_cowboy_hat = hat("Blue Cowboy Hat", HatDifficulty.medium, False)
    blue_ribbon = hat("Blue Ribbon", HatDifficulty.easy)
    bluebird_mask = hat("Bluebird Mask", HatDifficulty.medium_island, False)
    bowler = hat("Bowler Hat", HatDifficulty.difficult_or_rng)
    bridal_veil = hat("Bridal Veil", HatDifficulty.tailoring, False)
    bucket_hat = hat("Bucket Hat", HatDifficulty.easy)
    butterfly_bow = hat("Butterfly Bow", HatDifficulty.easy, False)
    cat_ears = hat("Cat Ears", HatDifficulty.medium)
    chef_hat = hat("Chef Hat", HatDifficulty.near_perfection, False)
    chicken_mask = hat("Chicken Mask", HatDifficulty.difficult_or_rng)
    cone_hat = hat("Cone Hat", HatDifficulty.easy, False)
    cool_cap = hat("Cool Cap", HatDifficulty.medium)
    copper_pan_hat = hat("Copper Pan (Hat)", HatDifficulty.easy, False)
    cowboy = hat("Cowboy Hat", HatDifficulty.difficult_or_rng)
    cowgal_hat = hat("Cowgal Hat", HatDifficulty.difficult_or_rng)
    cowpoke_hat = hat("Cowpoke Hat", HatDifficulty.difficult_or_rng, False)
    daisy = hat("Daisy", HatDifficulty.easy)
    dark_ballcap = hat("Dark Ballcap", HatDifficulty.difficult_or_rng)
    dark_cowboy_hat = hat("Dark Cowboy Hat", HatDifficulty.medium)
    dark_velvet_bow = hat("Dark Velvet Bow", HatDifficulty.easy, False)
    delicate_bow = hat("Delicate Bow", HatDifficulty.easy)
    deluxe_cowboy_hat = hat("Deluxe Cowboy Hat", HatDifficulty.medium_island, False)
    deluxe_pirate_hat = hat("Deluxe Pirate Hat", HatDifficulty.medium_island)
    dinosaur_hat = hat("Dinosaur Hat", HatDifficulty.tailoring, False)
    earmuffs = hat("Earmuffs", HatDifficulty.medium)
    elegant_turban = hat("Elegant Turban", HatDifficulty.post_perfection, False)
    emilys_magic_hat = hat("Emily's Magic Hat", HatDifficulty.medium, False)
    eye_patch = hat("Eye Patch", HatDifficulty.near_perfection, False)
    fashion_hat = hat("Fashion Hat", HatDifficulty.tailoring, False)
    fedora = hat("Fedora", HatDifficulty.easy, False)
    fishing_hat = hat("Fishing Hat", HatDifficulty.tailoring)
    flat_topped_hat = hat("Flat Topped Hat", HatDifficulty.tailoring, False)
    floppy_beanie = hat("Floppy Beanie", HatDifficulty.tailoring, False)
    foragers_hat = hat("Forager's Hat", HatDifficulty.tailoring_island, False)
    frog_hat = hat("Frog Hat", HatDifficulty.medium_island, False)
    garbage_hat = hat("Garbage Hat", HatDifficulty.difficult_or_rng)
    gils_hat = hat("Gil's Hat", HatDifficulty.difficult_or_rng, False)
    gnomes_cap = hat("Gnome's Cap", HatDifficulty.near_perfection, False)
    goblin_mask = hat("Goblin Mask", HatDifficulty.near_perfection)
    goggles = hat("Goggles", HatDifficulty.tailoring, False)
    gold_pan_hat = hat("Gold Pan (Hat)", HatDifficulty.medium, False)
    golden_helmet = hat("Golden Helmet", HatDifficulty.difficult_or_rng_island)
    golden_mask = hat("Golden Mask", HatDifficulty.tailoring)
    good_ol_cap = hat("Good Ol' Cap", HatDifficulty.easy)
    governors_hat = hat("Governor's Hat", HatDifficulty.easy)
    green_turban = hat("Green Turban", HatDifficulty.medium, False)
    hair_bone = hat("Hair Bone", HatDifficulty.tailoring, False)
    hard_hat = hat("Hard Hat", HatDifficulty.medium, False)
    hunters_cap = hat("Hunter's Cap", HatDifficulty.medium)
    infinity_crown = hat("Infinity Crown", HatDifficulty.difficult_or_rng_island)
    iridium_pan_hat = hat("Iridium Pan (Hat)", HatDifficulty.medium, False)
    jester_hat = hat("Jester Hat", HatDifficulty.easy)
    joja_cap = hat("Joja Cap", HatDifficulty.difficult_or_rng)
    junimo_hat = hat("Junimo Hat", HatDifficulty.post_perfection, False)
    knights_helmet = hat("Knight's Helmet", HatDifficulty.near_perfection, False)
    laurel_wreath_crown = hat("Laurel Wreath Crown", HatDifficulty.difficult_or_rng)
    leprechaun_hat = hat("Leprechaun Hat", HatDifficulty.easy, False)
    living_hat = hat("Living Hat", HatDifficulty.near_perfection)
    logo_cap = hat("Logo Cap", HatDifficulty.tailoring, False)
    lucky_bow = hat("Lucky Bow", HatDifficulty.medium)
    magic_cowboy_hat = hat("Magic Cowboy Hat", HatDifficulty.difficult_or_rng, False)
    magic_turban = hat("Magic Turban", HatDifficulty.difficult_or_rng, False)
    mouse_ears = hat("Mouse Ears", HatDifficulty.easy)
    mr_qis_hat = hat("Mr. Qi's Hat", HatDifficulty.medium_island, False)
    mummy_mask = hat("Mummy Mask", HatDifficulty.easy, False)
    mushroom_cap = hat("Mushroom Cap", HatDifficulty.difficult_or_rng, False)
    mystery_hat = hat("Mystery Hat", HatDifficulty.medium)
    official_cap = hat("Official Cap", HatDifficulty.medium)
    pageboy_cap = hat("Pageboy Cap", HatDifficulty.difficult_or_rng_island, False)
    panda_hat = hat("Panda Hat", HatDifficulty.impossible, False)
    paper_hat = hat("Paper Hat", HatDifficulty.easy_island, False)
    party_hat_blue = hat("Party Hat (Blue)", HatDifficulty.tailoring, False)
    party_hat_green = hat("Party Hat (Green)", HatDifficulty.tailoring, False)
    party_hat_red = hat("Party Hat (Red)", HatDifficulty.tailoring, False)
    pink_bow = hat("Pink Bow", HatDifficulty.easy_island, False)
    pirate_hat = hat("Pirate Hat", HatDifficulty.tailoring, False)
    plum_chapeau = hat("Plum Chapeau", HatDifficulty.medium)
    polka_bow = hat("Polka Bow", HatDifficulty.medium)
    propeller_hat = hat("Propeller Hat", HatDifficulty.tailoring, False)
    pumpkin_mask = hat("Pumpkin Mask", HatDifficulty.tailoring, False)
    qi_mask = hat("Qi Mask", HatDifficulty.tailoring_island, False)
    raccoon_hat = hat("Raccoon Hat", HatDifficulty.medium, False)
    radioactive_goggles = hat("Radioactive Goggles", HatDifficulty.tailoring_island, False)
    red_cowboy_hat = hat("Red Cowboy Hat", HatDifficulty.medium, False)
    red_fez = hat("Red Fez", HatDifficulty.medium, False)
    sailors_cap = hat("Sailor's Cap", HatDifficulty.easy)
    santa_hat = hat("Santa Hat", HatDifficulty.medium)
    skeleton_mask = hat("Skeleton Mask", HatDifficulty.medium, False)
    small_cap = hat("Small Cap", HatDifficulty.easy_island, False)
    sombrero = hat("Sombrero", HatDifficulty.near_perfection)
    souwester = hat("Sou'wester", HatDifficulty.easy)
    space_helmet = hat("Space Helmet", HatDifficulty.medium_island, False)
    sports_cap = hat("Sports Cap", HatDifficulty.medium)
    spotted_headscarf = hat("Spotted Headscarf", HatDifficulty.tailoring)
    squid_hat = hat("Squid Hat", HatDifficulty.easy, False)
    squires_helmet = hat("Squire's Helmet", HatDifficulty.medium, False)
    star_helmet = hat("Star Helmet", HatDifficulty.tailoring, False)
    steel_pan_hat = hat("Steel Pan (Hat)", HatDifficulty.medium, False)
    straw = hat("Straw Hat", HatDifficulty.easy)
    sunglasses = hat("Sunglasses", HatDifficulty.tailoring_island, False)
    swashbuckler_hat = hat("Swashbuckler Hat", HatDifficulty.tailoring_island, False)
    tiara = hat("Tiara", HatDifficulty.easy)
    tiger_hat = hat("Tiger Hat", HatDifficulty.difficult_or_rng_island)
    top_hat = hat("Top Hat", HatDifficulty.easy)
    totem_mask = hat("Totem Mask", HatDifficulty.medium, False)
    tropiclip = hat("Tropiclip", HatDifficulty.easy)
    trucker_hat = hat("Trucker Hat", HatDifficulty.medium)
    warrior_helmet = hat("Warrior Helmet", HatDifficulty.tailoring_island, False)
    watermelon_band = hat("Watermelon Band", HatDifficulty.difficult_or_rng)
    wearable_dwarf_helm = hat("Wearable Dwarf Helm", HatDifficulty.tailoring, False)
    white_bow = hat("White Bow", HatDifficulty.difficult_or_rng)
    white_turban = hat("White Turban", HatDifficulty.tailoring, False)
    witch_hat = hat("Witch Hat", HatDifficulty.tailoring, False)


all_hat_names = [hat.name for hat in all_hats]
all_considered_hat_names = [hat.name for hat in all_considered_hats]