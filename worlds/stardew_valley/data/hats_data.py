from dataclasses import dataclass
from functools import cached_property
from typing import List

from worlds.stardew_valley.strings.ap_names.ap_option_names import HatsanityOptionName

hat_clarifier = " (Hat)"


@dataclass(frozen=True)
class HatItem:
    name: str
    difficulty: frozenset[str]
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


def create_hat(name: str, difficulty: List[str] | str, need_clarifier: bool = False) -> HatItem:
    if isinstance(difficulty, str):
        difficulty = [difficulty]
    return HatItem(name, frozenset(difficulty), need_clarifier)


all_hats: list[HatItem] = []


class Hats:
    abigails_bow = create_hat("Abigail's Bow", HatsanityOptionName.rng)
    arcane_hat = create_hat("Arcane Hat", HatsanityOptionName.near_perfection)
    archers_cap = create_hat("Archer's Cap", HatsanityOptionName.near_perfection)
    beanie = create_hat("Beanie", HatsanityOptionName.tailoring)
    blobfish_mask = create_hat("Blobfish Mask", HatsanityOptionName.tailoring)
    blue_bonnet = create_hat("Blue Bonnet", HatsanityOptionName.medium)
    blue_bow = create_hat("Blue Bow", HatsanityOptionName.easy)
    blue_cowboy_hat = create_hat("Blue Cowboy Hat", HatsanityOptionName.rng)
    blue_ribbon = create_hat("Blue Ribbon", HatsanityOptionName.medium)
    bluebird_mask = create_hat("Bluebird Mask", HatsanityOptionName.medium)
    bowler = create_hat("Bowler Hat", HatsanityOptionName.difficult)
    bridal_veil = create_hat("Bridal Veil", HatsanityOptionName.tailoring)
    bucket_hat = create_hat("Bucket Hat", HatsanityOptionName.medium)
    butterfly_bow = create_hat("Butterfly Bow", HatsanityOptionName.easy)
    cat_ears = create_hat("Cat Ears", HatsanityOptionName.medium)
    chef_hat = create_hat("Chef Hat", HatsanityOptionName.near_perfection)
    chicken_mask = create_hat("Chicken Mask", HatsanityOptionName.near_perfection)
    concerned_ape_mask = create_hat("???", HatsanityOptionName.post_perfection)
    cone_hat = create_hat("Cone Hat", HatsanityOptionName.easy)
    cool_cap = create_hat("Cool Cap", HatsanityOptionName.medium)
    copper_pan_hat = create_hat("Copper Pan", HatsanityOptionName.easy, need_clarifier=True)
    cowboy = create_hat("Cowboy Hat", HatsanityOptionName.near_perfection)
    cowgal_hat = create_hat("Cowgal Hat", HatsanityOptionName.difficult)
    cowpoke_hat = create_hat("Cowpoke Hat", HatsanityOptionName.difficult)
    daisy = create_hat("Daisy", HatsanityOptionName.easy)
    dark_ballcap = create_hat("Dark Ballcap", HatsanityOptionName.rng)
    dark_cowboy_hat = create_hat("Dark Cowboy Hat", HatsanityOptionName.rng)
    dark_velvet_bow = create_hat("Dark Velvet Bow", HatsanityOptionName.easy)
    delicate_bow = create_hat("Delicate Bow", HatsanityOptionName.easy)
    deluxe_cowboy_hat = create_hat("Deluxe Cowboy Hat", HatsanityOptionName.medium)
    deluxe_pirate_hat = create_hat("Deluxe Pirate Hat", HatsanityOptionName.rng)
    dinosaur_hat = create_hat("Dinosaur Hat", HatsanityOptionName.tailoring)
    earmuffs = create_hat("Earmuffs", HatsanityOptionName.medium)
    elegant_turban = create_hat("Elegant Turban", HatsanityOptionName.post_perfection)
    emilys_magic_hat = create_hat("Emily's Magic Hat", HatsanityOptionName.medium)
    eye_patch = create_hat("Eye Patch", HatsanityOptionName.near_perfection)
    fashion_hat = create_hat("Fashion Hat", HatsanityOptionName.tailoring)
    fedora = create_hat("Fedora", HatsanityOptionName.easy)
    fishing_hat = create_hat("Fishing Hat", HatsanityOptionName.tailoring)
    flat_topped_hat = create_hat("Flat Topped Hat", HatsanityOptionName.tailoring)
    floppy_beanie = create_hat("Floppy Beanie", HatsanityOptionName.tailoring)
    foragers_hat = create_hat("Forager's Hat", HatsanityOptionName.tailoring)
    frog_hat = create_hat("Frog Hat", HatsanityOptionName.medium)
    garbage_hat = create_hat("Garbage Hat", HatsanityOptionName.rng)
    gils_hat = create_hat("Gil's Hat", HatsanityOptionName.difficult)
    gnomes_cap = create_hat("Gnome's Cap", HatsanityOptionName.near_perfection)
    goblin_mask = create_hat("Goblin Mask", HatsanityOptionName.near_perfection)
    goggles = create_hat("Goggles", HatsanityOptionName.tailoring)
    gold_pan_hat = create_hat("Gold Pan", HatsanityOptionName.easy, need_clarifier=True)
    golden_helmet = create_hat("Golden Helmet", HatsanityOptionName.rng)
    golden_mask = create_hat("Golden Mask", HatsanityOptionName.tailoring, need_clarifier=True)
    good_ol_cap = create_hat("Good Ol' Cap", HatsanityOptionName.easy)
    governors_hat = create_hat("Governor's Hat", HatsanityOptionName.medium)
    green_turban = create_hat("Green Turban", HatsanityOptionName.medium)
    hair_bone = create_hat("Hair Bone", HatsanityOptionName.tailoring)
    hard_hat = create_hat("Hard Hat", HatsanityOptionName.difficult)
    hunters_cap = create_hat("Hunter's Cap", HatsanityOptionName.medium)
    infinity_crown = create_hat("Infinity Crown", HatsanityOptionName.difficult)
    iridium_pan_hat = create_hat("Iridium Pan", HatsanityOptionName.easy, need_clarifier=True)
    jester_hat = create_hat("Jester Hat", HatsanityOptionName.easy)
    joja_cap = create_hat("Joja Cap", HatsanityOptionName.rng)
    junimo_hat = create_hat("Junimo Hat", HatsanityOptionName.post_perfection)
    knights_helmet = create_hat("Knight's Helmet", HatsanityOptionName.near_perfection)
    laurel_wreath_crown = create_hat("Laurel Wreath Crown", HatsanityOptionName.rng)
    leprechaun_hat = create_hat("Leprechaun Hat", HatsanityOptionName.easy)
    living_hat = create_hat("Living Hat", HatsanityOptionName.rng)
    logo_cap = create_hat("Logo Cap", HatsanityOptionName.tailoring)
    lucky_bow = create_hat("Lucky Bow", HatsanityOptionName.medium)
    magic_cowboy_hat = create_hat("Magic Cowboy Hat", HatsanityOptionName.difficult)
    magic_turban = create_hat("Magic Turban", HatsanityOptionName.difficult)
    mouse_ears = create_hat("Mouse Ears", HatsanityOptionName.easy)
    mr_qis_hat = create_hat("Mr. Qi's Hat", HatsanityOptionName.medium)
    mummy_mask = create_hat("Mummy Mask", HatsanityOptionName.easy)
    mushroom_cap = create_hat("Mushroom Cap", HatsanityOptionName.rng)
    mystery_hat = create_hat("Mystery Hat", HatsanityOptionName.rng)
    official_cap = create_hat("Official Cap", HatsanityOptionName.medium)
    pageboy_cap = create_hat("Pageboy Cap", HatsanityOptionName.near_perfection)
    panda_hat = create_hat("Panda Hat", "Impossible")
    paper_hat = create_hat("Paper Hat", HatsanityOptionName.easy)
    party_hat_blue = create_hat("Party Hat (Blue)", HatsanityOptionName.tailoring)
    party_hat_green = create_hat("Party Hat (Green)", HatsanityOptionName.tailoring)
    party_hat_red = create_hat("Party Hat (Red)", HatsanityOptionName.tailoring)
    pink_bow = create_hat("Pink Bow", HatsanityOptionName.easy)
    pirate_hat = create_hat("Pirate Hat", HatsanityOptionName.tailoring)
    plum_chapeau = create_hat("Plum Chapeau", HatsanityOptionName.difficult)
    polka_bow = create_hat("Polka Bow", HatsanityOptionName.medium)
    propeller_hat = create_hat("Propeller Hat", HatsanityOptionName.tailoring)
    pumpkin_mask = create_hat("Pumpkin Mask", HatsanityOptionName.tailoring)
    qi_mask = create_hat("Qi Mask", HatsanityOptionName.tailoring)
    raccoon_hat = create_hat("Raccoon Hat", HatsanityOptionName.medium)
    radioactive_goggles = create_hat("Radioactive Goggles", HatsanityOptionName.tailoring)
    red_cowboy_hat = create_hat("Red Cowboy Hat", HatsanityOptionName.rng)
    red_fez = create_hat("Red Fez", HatsanityOptionName.medium)
    sailors_cap = create_hat("Sailor's Cap", HatsanityOptionName.easy)
    santa_hat = create_hat("Santa Hat", HatsanityOptionName.medium)
    skeleton_mask = create_hat("Skeleton Mask", HatsanityOptionName.medium)
    small_cap = create_hat("Small Cap", HatsanityOptionName.medium)
    sombrero = create_hat("Sombrero", HatsanityOptionName.near_perfection)
    souwester = create_hat("Sou'wester", HatsanityOptionName.easy)
    space_helmet = create_hat("Space Helmet", HatsanityOptionName.difficult)
    sports_cap = create_hat("Sports Cap", HatsanityOptionName.medium)
    spotted_headscarf = create_hat("Spotted Headscarf", HatsanityOptionName.tailoring)
    squid_hat = create_hat("Squid Hat", HatsanityOptionName.medium)
    squires_helmet = create_hat("Squire's Helmet", HatsanityOptionName.rng)
    star_helmet = create_hat("Star Helmet", HatsanityOptionName.tailoring)
    steel_pan_hat = create_hat("Steel Pan", HatsanityOptionName.easy, need_clarifier=True)
    straw = create_hat("Straw Hat", HatsanityOptionName.medium)
    sunglasses = create_hat("Sunglasses", HatsanityOptionName.tailoring)
    swashbuckler_hat = create_hat("Swashbuckler Hat", HatsanityOptionName.tailoring)
    tiara = create_hat("Tiara", HatsanityOptionName.easy)
    tiger_hat = create_hat("Tiger Hat", HatsanityOptionName.rng)
    top_hat = create_hat("Top Hat", HatsanityOptionName.easy)
    totem_mask = create_hat("Totem Mask", HatsanityOptionName.tailoring)
    tricorn = create_hat("Tricorn Hat", HatsanityOptionName.rng)
    tropiclip = create_hat("Tropiclip", HatsanityOptionName.easy)
    trucker_hat = create_hat("Trucker Hat", HatsanityOptionName.medium)
    warrior_helmet = create_hat("Warrior Helmet", HatsanityOptionName.tailoring)
    watermelon_band = create_hat("Watermelon Band", HatsanityOptionName.difficult)
    wearable_dwarf_helm = create_hat("Wearable Dwarf Helm", HatsanityOptionName.tailoring)
    white_bow = create_hat("White Bow", HatsanityOptionName.difficult)
    white_turban = create_hat("White Turban", HatsanityOptionName.tailoring)
    witch_hat = create_hat("Witch Hat", HatsanityOptionName.tailoring)
