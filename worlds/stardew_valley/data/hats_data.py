from dataclasses import dataclass


class HatDifficulty:
    easy = 0
    easy_island = 0
    tailoring = 2
    tailoring_island = 2
    medium = 4
    medium_island = 4
    difficult_or_rng = 6
    difficult_or_rng_island = 6
    near_perfection = 8
    post_perfection = 10
    impossible = 999  # For that one chinese-version only hat


@dataclass(frozen=True)
class HatItem:
    name: str
    difficulty: int

    def __repr__(self) -> str:
        return f"{self.name} (Difficulty: {self.difficulty})"


all_hats: list[HatItem] = []


def hat(name: str, difficulty: int, consider: bool = True) -> HatItem:
    hat_item = HatItem(name, difficulty)
    all_hats.append(hat_item)
    return hat_item


class Hats:
    concerned_ape_mask = hat("???", HatDifficulty.post_perfection)
    abigails_bow = hat("Abigail's Bow", HatDifficulty.medium)
    arcane_hat = hat("Arcane Hat", HatDifficulty.difficult_or_rng)
    archers_cap = hat("Archer's Cap", HatDifficulty.near_perfection)
    beanie = hat("Beanie", HatDifficulty.tailoring)
    blobfish_mask = hat("Blobfish Mask", HatDifficulty.tailoring)
    blue_bonnet = hat("Blue Bonnet", HatDifficulty.medium)
    blue_bow = hat("Blue Bow", HatDifficulty.easy)
    blue_cowboy_hat = hat("Blue Cowboy Hat", HatDifficulty.medium)
    blue_ribbon = hat("Blue Ribbon", HatDifficulty.easy)
    bluebird_mask = hat("Bluebird Mask", HatDifficulty.medium_island)
    bowler = hat("Bowler Hat", HatDifficulty.difficult_or_rng)
    bridal_veil = hat("Bridal Veil", HatDifficulty.tailoring)
    bucket_hat = hat("Bucket Hat", HatDifficulty.easy)
    butterfly_bow = hat("Butterfly Bow", HatDifficulty.easy)
    cat_ears = hat("Cat Ears", HatDifficulty.medium)
    chef_hat = hat("Chef Hat", HatDifficulty.near_perfection)
    chicken_mask = hat("Chicken Mask", HatDifficulty.difficult_or_rng)
    cone_hat = hat("Cone Hat", HatDifficulty.easy)
    cool_cap = hat("Cool Cap", HatDifficulty.medium)
    copper_pan_hat = hat("Copper Pan (Hat)", HatDifficulty.easy)
    cowboy = hat("Cowboy Hat", HatDifficulty.difficult_or_rng)
    cowgal_hat = hat("Cowgal Hat", HatDifficulty.difficult_or_rng)
    cowpoke_hat = hat("Cowpoke Hat", HatDifficulty.difficult_or_rng)
    daisy = hat("Daisy", HatDifficulty.easy)
    dark_ballcap = hat("Dark Ballcap", HatDifficulty.difficult_or_rng)
    dark_cowboy_hat = hat("Dark Cowboy Hat", HatDifficulty.medium)
    dark_velvet_bow = hat("Dark Velvet Bow", HatDifficulty.easy)
    delicate_bow = hat("Delicate Bow", HatDifficulty.easy)
    deluxe_cowboy_hat = hat("Deluxe Cowboy Hat", HatDifficulty.medium_island)
    deluxe_pirate_hat = hat("Deluxe Pirate Hat", HatDifficulty.medium_island)
    dinosaur_hat = hat("Dinosaur Hat", HatDifficulty.tailoring)
    earmuffs = hat("Earmuffs", HatDifficulty.medium)
    elegant_turban = hat("Elegant Turban", HatDifficulty.post_perfection)
    emilys_magic_hat = hat("Emily's Magic Hat", HatDifficulty.medium)
    eye_patch = hat("Eye Patch", HatDifficulty.near_perfection)
    fashion_hat = hat("Fashion Hat", HatDifficulty.tailoring)
    fedora = hat("Fedora", HatDifficulty.easy)
    fishing_hat = hat("Fishing Hat", HatDifficulty.tailoring)
    flat_topped_hat = hat("Flat Topped Hat", HatDifficulty.tailoring)
    floppy_beanie = hat("Floppy Beanie", HatDifficulty.tailoring)
    foragers_hat = hat("Forager's Hat", HatDifficulty.tailoring_island)
    frog_hat = hat("Frog Hat", HatDifficulty.medium_island)
    garbage_hat = hat("Garbage Hat", HatDifficulty.difficult_or_rng)
    gils_hat = hat("Gil's Hat", HatDifficulty.difficult_or_rng)
    gnomes_cap = hat("Gnome's Cap", HatDifficulty.near_perfection)
    goblin_mask = hat("Goblin Mask", HatDifficulty.near_perfection)
    goggles = hat("Goggles", HatDifficulty.tailoring)
    gold_pan_hat = hat("Gold Pan (Hat)", HatDifficulty.medium)
    golden_helmet = hat("Golden Helmet", HatDifficulty.difficult_or_rng_island)
    golden_mask = hat("Golden Mask (Hat)", HatDifficulty.tailoring)
    good_ol_cap = hat("Good Ol' Cap", HatDifficulty.easy)
    governors_hat = hat("Governor's Hat", HatDifficulty.easy)
    green_turban = hat("Green Turban", HatDifficulty.medium, False)
    hair_bone = hat("Hair Bone", HatDifficulty.tailoring)
    hard_hat = hat("Hard Hat", HatDifficulty.medium, False)
    hunters_cap = hat("Hunter's Cap", HatDifficulty.medium)
    infinity_crown = hat("Infinity Crown", HatDifficulty.difficult_or_rng_island)
    iridium_pan_hat = hat("Iridium Pan (Hat)", HatDifficulty.medium)
    jester_hat = hat("Jester Hat", HatDifficulty.easy)
    joja_cap = hat("Joja Cap", HatDifficulty.difficult_or_rng)
    junimo_hat = hat("Junimo Hat", HatDifficulty.post_perfection, False)
    knights_helmet = hat("Knight's Helmet", HatDifficulty.near_perfection, False)
    laurel_wreath_crown = hat("Laurel Wreath Crown", HatDifficulty.difficult_or_rng)
    leprechaun_hat = hat("Leprechaun Hat", HatDifficulty.easy, False)
    living_hat = hat("Living Hat", HatDifficulty.near_perfection)
    logo_cap = hat("Logo Cap", HatDifficulty.tailoring)
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
    party_hat_blue = hat("Party Hat (Blue)", HatDifficulty.tailoring)
    party_hat_green = hat("Party Hat (Green)", HatDifficulty.tailoring)
    party_hat_red = hat("Party Hat (Red)", HatDifficulty.tailoring)
    pink_bow = hat("Pink Bow", HatDifficulty.easy_island, False)
    pirate_hat = hat("Pirate Hat", HatDifficulty.tailoring)
    plum_chapeau = hat("Plum Chapeau", HatDifficulty.medium)
    polka_bow = hat("Polka Bow", HatDifficulty.medium)
    propeller_hat = hat("Propeller Hat", HatDifficulty.tailoring)
    pumpkin_mask = hat("Pumpkin Mask", HatDifficulty.tailoring)
    qi_mask = hat("Qi Mask", HatDifficulty.tailoring_island)
    raccoon_hat = hat("Raccoon Hat", HatDifficulty.medium, False)
    radioactive_goggles = hat("Radioactive Goggles", HatDifficulty.tailoring_island)
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
    star_helmet = hat("Star Helmet", HatDifficulty.tailoring)
    steel_pan_hat = hat("Steel Pan (Hat)", HatDifficulty.medium)
    straw = hat("Straw Hat", HatDifficulty.easy)
    sunglasses = hat("Sunglasses", HatDifficulty.tailoring_island)
    swashbuckler_hat = hat("Swashbuckler Hat", HatDifficulty.tailoring_island)
    tiara = hat("Tiara", HatDifficulty.easy)
    tiger_hat = hat("Tiger Hat", HatDifficulty.difficult_or_rng_island)
    top_hat = hat("Top Hat", HatDifficulty.easy)
    totem_mask = hat("Totem Mask", HatDifficulty.medium, False)
    tropiclip = hat("Tropiclip", HatDifficulty.easy)
    trucker_hat = hat("Trucker Hat", HatDifficulty.medium)
    warrior_helmet = hat("Warrior Helmet", HatDifficulty.tailoring_island)
    watermelon_band = hat("Watermelon Band", HatDifficulty.difficult_or_rng)
    wearable_dwarf_helm = hat("Wearable Dwarf Helm", HatDifficulty.tailoring)
    white_bow = hat("White Bow", HatDifficulty.difficult_or_rng)
    white_turban = hat("White Turban", HatDifficulty.tailoring)
    witch_hat = hat("Witch Hat", HatDifficulty.tailoring)

