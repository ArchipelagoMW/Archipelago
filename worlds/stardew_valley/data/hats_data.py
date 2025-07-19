from dataclasses import dataclass
from functools import cached_property

hat_clarifier = " (Hat)"


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
    need_clarifier: bool = False

    def __post_init__(self):
        all_hats.append(self)

    @cached_property
    def clarified_name(self) -> str:
        if self.need_clarifier:
            return self.name + hat_clarifier
        return self.name

    def __repr__(self) -> str:
        return f"{self.name} (Difficulty: {self.difficulty})"


all_hats: list[HatItem] = []


class Hats:
    concerned_ape_mask = HatItem("???", HatDifficulty.post_perfection)
    abigails_bow = HatItem("Abigail's Bow", HatDifficulty.difficult_or_rng)
    arcane_hat = HatItem("Arcane Hat", HatDifficulty.near_perfection)
    archers_cap = HatItem("Archer's Cap", HatDifficulty.near_perfection)
    beanie = HatItem("Beanie", HatDifficulty.tailoring)
    blobfish_mask = HatItem("Blobfish Mask", HatDifficulty.tailoring)
    blue_bonnet = HatItem("Blue Bonnet", HatDifficulty.medium)
    blue_bow = HatItem("Blue Bow", HatDifficulty.easy)
    blue_cowboy_hat = HatItem("Blue Cowboy Hat", HatDifficulty.difficult_or_rng)
    blue_ribbon = HatItem("Blue Ribbon", HatDifficulty.easy)
    bluebird_mask = HatItem("Bluebird Mask", HatDifficulty.medium_island)
    bowler = HatItem("Bowler Hat", HatDifficulty.difficult_or_rng)
    bridal_veil = HatItem("Bridal Veil", HatDifficulty.tailoring)
    bucket_hat = HatItem("Bucket Hat", HatDifficulty.easy)
    butterfly_bow = HatItem("Butterfly Bow", HatDifficulty.easy)
    cat_ears = HatItem("Cat Ears", HatDifficulty.medium)
    chef_hat = HatItem("Chef Hat", HatDifficulty.near_perfection)
    chicken_mask = HatItem("Chicken Mask", HatDifficulty.difficult_or_rng)
    cone_hat = HatItem("Cone Hat", HatDifficulty.easy)
    cool_cap = HatItem("Cool Cap", HatDifficulty.medium)
    copper_pan_hat = HatItem("Copper Pan", HatDifficulty.easy, need_clarifier=True)
    cowboy = HatItem("Cowboy Hat", HatDifficulty.near_perfection)
    cowgal_hat = HatItem("Cowgal Hat", HatDifficulty.difficult_or_rng)
    cowpoke_hat = HatItem("Cowpoke Hat", HatDifficulty.difficult_or_rng)
    daisy = HatItem("Daisy", HatDifficulty.easy)
    dark_ballcap = HatItem("Dark Ballcap", HatDifficulty.difficult_or_rng)
    dark_cowboy_hat = HatItem("Dark Cowboy Hat", HatDifficulty.difficult_or_rng)
    dark_velvet_bow = HatItem("Dark Velvet Bow", HatDifficulty.easy)
    delicate_bow = HatItem("Delicate Bow", HatDifficulty.easy)
    deluxe_cowboy_hat = HatItem("Deluxe Cowboy Hat", HatDifficulty.medium_island)
    deluxe_pirate_hat = HatItem("Deluxe Pirate Hat", HatDifficulty.difficult_or_rng_island)
    dinosaur_hat = HatItem("Dinosaur Hat", HatDifficulty.tailoring)
    earmuffs = HatItem("Earmuffs", HatDifficulty.medium)
    elegant_turban = HatItem("Elegant Turban", HatDifficulty.post_perfection)
    emilys_magic_hat = HatItem("Emily's Magic Hat", HatDifficulty.medium)
    eye_patch = HatItem("Eye Patch", HatDifficulty.near_perfection)
    fashion_hat = HatItem("Fashion Hat", HatDifficulty.tailoring)
    fedora = HatItem("Fedora", HatDifficulty.easy)
    fishing_hat = HatItem("Fishing Hat", HatDifficulty.tailoring)
    flat_topped_hat = HatItem("Flat Topped Hat", HatDifficulty.tailoring)
    floppy_beanie = HatItem("Floppy Beanie", HatDifficulty.tailoring)
    foragers_hat = HatItem("Forager's Hat", HatDifficulty.tailoring_island)
    frog_hat = HatItem("Frog Hat", HatDifficulty.medium_island)
    garbage_hat = HatItem("Garbage Hat", HatDifficulty.difficult_or_rng)
    gils_hat = HatItem("Gil's Hat", HatDifficulty.difficult_or_rng)
    gnomes_cap = HatItem("Gnome's Cap", HatDifficulty.near_perfection)
    goblin_mask = HatItem("Goblin Mask", HatDifficulty.near_perfection)
    goggles = HatItem("Goggles", HatDifficulty.tailoring)
    gold_pan_hat = HatItem("Gold Pan", HatDifficulty.medium, need_clarifier=True)
    golden_helmet = HatItem("Golden Helmet", HatDifficulty.difficult_or_rng_island)
    golden_mask = HatItem("Golden Mask", HatDifficulty.tailoring, need_clarifier=True)
    good_ol_cap = HatItem("Good Ol' Cap", HatDifficulty.easy)
    governors_hat = HatItem("Governor's Hat", HatDifficulty.easy)
    green_turban = HatItem("Green Turban", HatDifficulty.medium)
    hair_bone = HatItem("Hair Bone", HatDifficulty.tailoring)
    hard_hat = HatItem("Hard Hat", HatDifficulty.difficult_or_rng)
    hunters_cap = HatItem("Hunter's Cap", HatDifficulty.medium)
    infinity_crown = HatItem("Infinity Crown", HatDifficulty.difficult_or_rng_island)
    iridium_pan_hat = HatItem("Iridium Pan", HatDifficulty.medium, need_clarifier=True)
    jester_hat = HatItem("Jester Hat", HatDifficulty.easy)
    joja_cap = HatItem("Joja Cap", HatDifficulty.difficult_or_rng)
    junimo_hat = HatItem("Junimo Hat", HatDifficulty.post_perfection)
    knights_helmet = HatItem("Knight's Helmet", HatDifficulty.near_perfection)
    laurel_wreath_crown = HatItem("Laurel Wreath Crown", HatDifficulty.difficult_or_rng)
    leprechaun_hat = HatItem("Leprechaun Hat", HatDifficulty.easy)
    living_hat = HatItem("Living Hat", HatDifficulty.near_perfection)
    logo_cap = HatItem("Logo Cap", HatDifficulty.tailoring)
    lucky_bow = HatItem("Lucky Bow", HatDifficulty.medium)
    magic_cowboy_hat = HatItem("Magic Cowboy Hat", HatDifficulty.difficult_or_rng)
    magic_turban = HatItem("Magic Turban", HatDifficulty.difficult_or_rng)
    mouse_ears = HatItem("Mouse Ears", HatDifficulty.easy)
    mr_qis_hat = HatItem("Mr. Qi's Hat", HatDifficulty.medium_island)
    mummy_mask = HatItem("Mummy Mask", HatDifficulty.easy)
    mushroom_cap = HatItem("Mushroom Cap", HatDifficulty.difficult_or_rng)
    mystery_hat = HatItem("Mystery Hat", HatDifficulty.medium)
    official_cap = HatItem("Official Cap", HatDifficulty.medium)
    pageboy_cap = HatItem("Pageboy Cap", HatDifficulty.difficult_or_rng_island)
    panda_hat = HatItem("Panda Hat", HatDifficulty.impossible)
    paper_hat = HatItem("Paper Hat", HatDifficulty.easy_island)
    party_hat_blue = HatItem("Party Hat (Blue)", HatDifficulty.tailoring)
    party_hat_green = HatItem("Party Hat (Green)", HatDifficulty.tailoring)
    party_hat_red = HatItem("Party Hat (Red)", HatDifficulty.tailoring)
    pink_bow = HatItem("Pink Bow", HatDifficulty.easy_island)
    pirate_hat = HatItem("Pirate Hat", HatDifficulty.tailoring)
    plum_chapeau = HatItem("Plum Chapeau", HatDifficulty.medium)
    polka_bow = HatItem("Polka Bow", HatDifficulty.medium)
    propeller_hat = HatItem("Propeller Hat", HatDifficulty.tailoring)
    pumpkin_mask = HatItem("Pumpkin Mask", HatDifficulty.tailoring)
    qi_mask = HatItem("Qi Mask", HatDifficulty.tailoring_island)
    raccoon_hat = HatItem("Raccoon Hat", HatDifficulty.medium)
    radioactive_goggles = HatItem("Radioactive Goggles", HatDifficulty.tailoring_island)
    red_cowboy_hat = HatItem("Red Cowboy Hat", HatDifficulty.difficult_or_rng)
    red_fez = HatItem("Red Fez", HatDifficulty.medium)
    sailors_cap = HatItem("Sailor's Cap", HatDifficulty.easy)
    santa_hat = HatItem("Santa Hat", HatDifficulty.medium)
    skeleton_mask = HatItem("Skeleton Mask", HatDifficulty.medium)
    small_cap = HatItem("Small Cap", HatDifficulty.easy_island)
    sombrero = HatItem("Sombrero", HatDifficulty.near_perfection)
    souwester = HatItem("Sou'wester", HatDifficulty.easy)
    space_helmet = HatItem("Space Helmet", HatDifficulty.medium_island)
    sports_cap = HatItem("Sports Cap", HatDifficulty.medium)
    spotted_headscarf = HatItem("Spotted Headscarf", HatDifficulty.tailoring)
    squid_hat = HatItem("Squid Hat", HatDifficulty.easy)
    squires_helmet = HatItem("Squire's Helmet", HatDifficulty.medium)
    star_helmet = HatItem("Star Helmet", HatDifficulty.tailoring_island)
    steel_pan_hat = HatItem("Steel Pan", HatDifficulty.medium, need_clarifier=True)
    straw = HatItem("Straw Hat", HatDifficulty.easy)
    sunglasses = HatItem("Sunglasses", HatDifficulty.tailoring_island)
    swashbuckler_hat = HatItem("Swashbuckler Hat", HatDifficulty.tailoring_island)
    tiara = HatItem("Tiara", HatDifficulty.easy)
    tiger_hat = HatItem("Tiger Hat", HatDifficulty.difficult_or_rng_island)
    top_hat = HatItem("Top Hat", HatDifficulty.easy)
    totem_mask = HatItem("Totem Mask", HatDifficulty.tailoring)
    tricorn = HatItem("Tricorn Hat", HatDifficulty.difficult_or_rng)
    tropiclip = HatItem("Tropiclip", HatDifficulty.easy)
    trucker_hat = HatItem("Trucker Hat", HatDifficulty.medium)
    warrior_helmet = HatItem("Warrior Helmet", HatDifficulty.tailoring_island)
    watermelon_band = HatItem("Watermelon Band", HatDifficulty.difficult_or_rng)
    wearable_dwarf_helm = HatItem("Wearable Dwarf Helm", HatDifficulty.tailoring)
    white_bow = HatItem("White Bow", HatDifficulty.difficult_or_rng)
    white_turban = HatItem("White Turban", HatDifficulty.tailoring)
    witch_hat = HatItem("Witch Hat", HatDifficulty.tailoring)
