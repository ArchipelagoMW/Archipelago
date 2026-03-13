from dataclasses import dataclass
from typing import List, Tuple, Dict, Callable

from .game_item import Source
from ..mods.mod_data import ModNames
from ..mods.mod_monster_locations import modded_monsters_locations
from ..strings.monster_names import Monster, MonsterCategory
from ..strings.performance_names import Performance
from ..strings.region_names import Region


@dataclass(frozen=True)
class StardewMonster:
    name: str
    category: str
    locations: Tuple[str, ...]
    difficulty: str

    def __repr__(self):
        return f"{self.name} [{self.category}] (Locations: {self.locations} |" \
               f" Difficulty: {self.difficulty}) |"


@dataclass(frozen=True, kw_only=True)
class MonsterSource(Source):
    monsters: Tuple[StardewMonster, ...]
    amount_tier: int = 0


slime_hutch = (Region.slime_hutch,)
mines_floor_20 = (Region.mines_floor_20,)
mines_floor_60 = (Region.mines_floor_60,)
mines_floor_100 = (Region.mines_floor_100,)
dangerous_mines_20 = (Region.dangerous_mines_20,)
dangerous_mines_60 = (Region.dangerous_mines_60,)
dangerous_mines_100 = (Region.dangerous_mines_100,)
quarry_mine = (Region.quarry_mine,)
mutant_bug_lair = (Region.mutant_bug_lair,)
skull_cavern = (Region.skull_cavern_25,)
skull_cavern_high = (Region.skull_cavern_75,)
skull_cavern_dangerous = (Region.dangerous_skull_cavern,)
tiger_slime_grove = (Region.island_west,)
volcano = (Region.volcano_floor_5,)
volcano_high = (Region.volcano_floor_10,)

all_monsters: List[StardewMonster] = []
monster_modifications_by_mod: Dict[str, Dict[str, Callable[[str, StardewMonster], StardewMonster]]] = {}


def create_monster(name: str, category: str, locations: Tuple[str, ...], difficulty: str) -> StardewMonster:
    monster = StardewMonster(name, category, locations, difficulty)
    all_monsters.append(monster)
    return monster


def update_monster_locations(mod_name: str, monster: StardewMonster):
    new_locations = modded_monsters_locations[mod_name][monster.name]
    total_locations = tuple(sorted(set(monster.locations + new_locations)))
    return StardewMonster(monster.name, monster.category, total_locations, monster.difficulty)


def register_monster_modification(mod_name: str, monster: StardewMonster, modification_function):
    if mod_name not in monster_modifications_by_mod:
        monster_modifications_by_mod[mod_name] = {}
    monster_modifications_by_mod[mod_name][monster.name] = modification_function


green_slime = create_monster(Monster.green_slime, MonsterCategory.slime, mines_floor_20, Performance.basic)
blue_slime = create_monster(Monster.blue_slime, MonsterCategory.slime, mines_floor_60, Performance.decent)
red_slime = create_monster(Monster.red_slime, MonsterCategory.slime, mines_floor_100, Performance.good)
purple_slime = create_monster(Monster.purple_slime, MonsterCategory.slime, skull_cavern, Performance.great)
yellow_slime = create_monster(Monster.yellow_slime, MonsterCategory.slime, skull_cavern_high, Performance.galaxy)
black_slime = create_monster(Monster.black_slime, MonsterCategory.slime, slime_hutch, Performance.decent)
copper_slime = create_monster(Monster.copper_slime, MonsterCategory.slime, quarry_mine, Performance.decent)
iron_slime = create_monster(Monster.iron_slime, MonsterCategory.slime, quarry_mine, Performance.good)
tiger_slime = create_monster(Monster.tiger_slime, MonsterCategory.slime, tiger_slime_grove, Performance.galaxy)

shadow_shaman = create_monster(Monster.shadow_shaman, MonsterCategory.void_spirits, mines_floor_100, Performance.good)
shadow_shaman_dangerous = create_monster(Monster.shadow_shaman_dangerous, MonsterCategory.void_spirits, dangerous_mines_100, Performance.galaxy)
shadow_brute = create_monster(Monster.shadow_brute, MonsterCategory.void_spirits, mines_floor_100, Performance.good)
shadow_brute_dangerous = create_monster(Monster.shadow_brute_dangerous, MonsterCategory.void_spirits, dangerous_mines_100, Performance.galaxy)
shadow_sniper = create_monster(Monster.shadow_sniper, MonsterCategory.void_spirits, dangerous_mines_100, Performance.galaxy)

bat = create_monster(Monster.bat, MonsterCategory.bats, mines_floor_20, Performance.basic)
bat_dangerous = create_monster(Monster.bat_dangerous, MonsterCategory.bats, dangerous_mines_20, Performance.galaxy)
frost_bat = create_monster(Monster.frost_bat, MonsterCategory.bats, mines_floor_60, Performance.decent)
frost_bat_dangerous = create_monster(Monster.frost_bat_dangerous, MonsterCategory.bats, dangerous_mines_60, Performance.galaxy)
lava_bat = create_monster(Monster.lava_bat, MonsterCategory.bats, mines_floor_100, Performance.good)
iridium_bat = create_monster(Monster.iridium_bat, MonsterCategory.bats, skull_cavern_high, Performance.great)

skeleton = create_monster(Monster.skeleton, MonsterCategory.skeletons, mines_floor_100, Performance.good)
skeleton_dangerous = create_monster(Monster.skeleton_dangerous, MonsterCategory.skeletons, dangerous_mines_100, Performance.galaxy)
skeleton_mage = create_monster(Monster.skeleton_mage, MonsterCategory.skeletons, dangerous_mines_100, Performance.galaxy)

bug = create_monster(Monster.bug, MonsterCategory.cave_insects, mines_floor_20, Performance.basic)
bug_dangerous = create_monster(Monster.bug_dangerous, MonsterCategory.cave_insects, dangerous_mines_20, Performance.galaxy)
cave_fly = create_monster(Monster.cave_fly, MonsterCategory.cave_insects, mines_floor_20, Performance.basic)
cave_fly_dangerous = create_monster(Monster.cave_fly_dangerous, MonsterCategory.cave_insects, dangerous_mines_60, Performance.galaxy)
grub = create_monster(Monster.grub, MonsterCategory.cave_insects, mines_floor_20, Performance.basic)
grub_dangerous = create_monster(Monster.grub_dangerous, MonsterCategory.cave_insects, dangerous_mines_60, Performance.galaxy)
mutant_fly = create_monster(Monster.mutant_fly, MonsterCategory.cave_insects, mutant_bug_lair, Performance.good)
mutant_grub = create_monster(Monster.mutant_grub, MonsterCategory.cave_insects, mutant_bug_lair, Performance.good)
armored_bug = create_monster(Monster.armored_bug, MonsterCategory.cave_insects, skull_cavern, Performance.basic)  # Requires 'Bug Killer' enchantment
armored_bug_dangerous = create_monster(Monster.armored_bug_dangerous, MonsterCategory.cave_insects, skull_cavern,
                                       Performance.good)  # Requires 'Bug Killer' enchantment

metal_head = create_monster(Monster.metal_head, MonsterCategory.metal_heads, mines_floor_100, Performance.good)

duggy = create_monster(Monster.duggy, MonsterCategory.duggies, mines_floor_20, Performance.basic)
duggy_dangerous = create_monster(Monster.duggy_dangerous, MonsterCategory.duggies, dangerous_mines_20, Performance.great)
magma_duggy = create_monster(Monster.magma_duggy, MonsterCategory.duggies, volcano, Performance.galaxy)

dust_sprite = create_monster(Monster.dust_sprite, MonsterCategory.dust_sprites, mines_floor_60, Performance.basic)
dust_sprite_dangerous = create_monster(Monster.dust_sprite_dangerous, MonsterCategory.dust_sprites, dangerous_mines_60, Performance.great)

rock_crab = create_monster(Monster.rock_crab, MonsterCategory.rock_crabs, mines_floor_20, Performance.basic)
rock_crab_dangerous = create_monster(Monster.rock_crab_dangerous, MonsterCategory.rock_crabs, dangerous_mines_20, Performance.great)
lava_crab = create_monster(Monster.lava_crab, MonsterCategory.rock_crabs, mines_floor_100, Performance.good)
lava_crab_dangerous = create_monster(Monster.lava_crab_dangerous, MonsterCategory.rock_crabs, dangerous_mines_100, Performance.galaxy)
iridium_crab = create_monster(Monster.iridium_crab, MonsterCategory.rock_crabs, skull_cavern, Performance.great)

mummy = create_monster(Monster.mummy, MonsterCategory.mummies, skull_cavern, Performance.great)  # Requires bombs or "Crusader" enchantment
mummy_dangerous = create_monster(Monster.mummy_dangerous, MonsterCategory.mummies, skull_cavern_dangerous,
                                 Performance.maximum)  # Requires bombs or "Crusader" enchantment

pepper_rex = create_monster(Monster.pepper_rex, MonsterCategory.pepper_rex, skull_cavern, Performance.great)

serpent = create_monster(Monster.serpent, MonsterCategory.serpents, skull_cavern, Performance.galaxy)
royal_serpent = create_monster(Monster.royal_serpent, MonsterCategory.serpents, skull_cavern_dangerous, Performance.maximum)

magma_sprite = create_monster(Monster.magma_sprite, MonsterCategory.magma_sprites, volcano, Performance.galaxy)
magma_sparker = create_monster(Monster.magma_sparker, MonsterCategory.magma_sprites, volcano_high, Performance.galaxy)

haunted_skull = create_monster(Monster.haunted_skull, MonsterCategory.none, quarry_mine, Performance.great)

register_monster_modification(ModNames.sve, shadow_brute_dangerous, update_monster_locations)
register_monster_modification(ModNames.sve, shadow_sniper, update_monster_locations)
register_monster_modification(ModNames.sve, shadow_shaman_dangerous, update_monster_locations)
register_monster_modification(ModNames.sve, mummy_dangerous, update_monster_locations)
register_monster_modification(ModNames.sve, royal_serpent, update_monster_locations)
register_monster_modification(ModNames.sve, skeleton_dangerous, update_monster_locations)
register_monster_modification(ModNames.sve, skeleton_mage, update_monster_locations)
register_monster_modification(ModNames.sve, dust_sprite_dangerous, update_monster_locations)

register_monster_modification(ModNames.deepwoods, shadow_brute, update_monster_locations)
register_monster_modification(ModNames.deepwoods, cave_fly, update_monster_locations)
register_monster_modification(ModNames.deepwoods, green_slime, update_monster_locations)

register_monster_modification(ModNames.boarding_house, pepper_rex, update_monster_locations)
register_monster_modification(ModNames.boarding_house, shadow_brute, update_monster_locations)
register_monster_modification(ModNames.boarding_house, iridium_bat, update_monster_locations)
register_monster_modification(ModNames.boarding_house, frost_bat, update_monster_locations)
register_monster_modification(ModNames.boarding_house, cave_fly, update_monster_locations)
register_monster_modification(ModNames.boarding_house, bat, update_monster_locations)
register_monster_modification(ModNames.boarding_house, grub, update_monster_locations)
register_monster_modification(ModNames.boarding_house, bug, update_monster_locations)


def all_monsters_by_name_given_content_packs(mods: set[str]) -> dict[str, StardewMonster]:
    monsters_by_name = {}
    for monster in all_monsters:
        current_monster = monster
        for mod in monster_modifications_by_mod:
            if mod not in mods or monster.name not in monster_modifications_by_mod[mod]:
                continue
            modification_function = monster_modifications_by_mod[mod][monster.name]
            current_monster = modification_function(mod, current_monster)
        monsters_by_name[monster.name] = current_monster
    return monsters_by_name


def all_monsters_by_category_given_content_packs(mods: set[str]) -> dict[str, Tuple[StardewMonster, ...]]:
    monsters_by_category = {}
    for monster in all_monsters:
        current_monster = monster
        for mod in monster_modifications_by_mod:
            if mod not in mods or monster.name not in monster_modifications_by_mod[mod]:
                continue
            modification_function = monster_modifications_by_mod[mod][monster.name]
            current_monster = modification_function(mod, current_monster)
        if current_monster.category not in monsters_by_category:
            monsters_by_category[monster.category] = ()
        monsters_by_category[current_monster.category] = monsters_by_category[current_monster.category] + (current_monster,)
    return monsters_by_category
