from dataclasses import dataclass
from typing import List, Tuple, Union, Optional

from . import season_data as season
from .game_item import GameItem
from ..strings.monster_names import Monster, MonsterCategory
from ..strings.region_names import Region


@dataclass(frozen=True)
class StardewMonster:
    name: str
    category: str
    locations: Tuple[str]
    difficulty: int

    def __repr__(self):
        return f"{self.name} [{self.category}] (Locations: {self.locations} |" \
               f" Difficulty: {self.difficulty}) |"

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


def create_monster(name: str, category: str, locations: Tuple[str, ...], difficulty: int) -> StardewMonster:
    monster = StardewMonster(name, category, locations, difficulty)
    all_monsters.append(monster)
    return monster


green_slime = create_monster(Monster.green_slime, MonsterCategory.slime, mines_floor_20, 0)
blue_slime = create_monster(Monster.blue_slime, MonsterCategory.slime, mines_floor_60, 1)
red_slime = create_monster(Monster.red_slime, MonsterCategory.slime, mines_floor_100, 2)
purple_slime = create_monster(Monster.purple_slime, MonsterCategory.slime, skull_cavern, 3)
yellow_slime = create_monster(Monster.yellow_slime, MonsterCategory.slime, skull_cavern_high, 4)
black_slime = create_monster(Monster.black_slime, MonsterCategory.slime, slime_hutch, 1)
copper_slime = create_monster(Monster.copper_slime, MonsterCategory.slime, quarry_mine, 1)
iron_slime = create_monster(Monster.iron_slime, MonsterCategory.slime, quarry_mine, 2)
tiger_slime = create_monster(Monster.tiger_slime, MonsterCategory.slime, tiger_slime_grove, 4)

shadow_shaman = create_monster(Monster.shadow_shaman, MonsterCategory.void_spirits, mines_floor_100, 2)
shadow_shaman_dangerous = create_monster(Monster.shadow_shaman_dangerous, MonsterCategory.void_spirits, dangerous_mines_100, 4)
shadow_brute = create_monster(Monster.shadow_brute, MonsterCategory.void_spirits, mines_floor_100, 2)
shadow_brute_dangerous = create_monster(Monster.shadow_brute_dangerous, MonsterCategory.void_spirits, dangerous_mines_100, 4)
shadow_sniper = create_monster(Monster.shadow_sniper, MonsterCategory.void_spirits, dangerous_mines_100, 4)

bat = create_monster(Monster.bat, MonsterCategory.bats, mines_floor_20, 0)
bat_dangerous = create_monster(Monster.bat_dangerous, MonsterCategory.bats, dangerous_mines_20, 4)
frost_bat = create_monster(Monster.frost_bat, MonsterCategory.bats, mines_floor_60, 1)
frost_bat_dangerous = create_monster(Monster.frost_bat_dangerous, MonsterCategory.bats, dangerous_mines_60, 4)
lava_bat = create_monster(Monster.lava_bat, MonsterCategory.bats,mines_floor_100, 2)
iridium_bat = create_monster(Monster.iridium_bat, MonsterCategory.bats, skull_cavern_high, 3)

skeleton = create_monster(Monster.skeleton, MonsterCategory.skeletons, mines_floor_100, 2)
skeleton_dangerous = create_monster(Monster.skeleton_dangerous, MonsterCategory.skeletons, dangerous_mines_100, 4)
skeleton_mage = create_monster(Monster.skeleton_mage, MonsterCategory.skeletons, dangerous_mines_100, 4)

bug = create_monster(Monster.bug, MonsterCategory.cave_insects, mines_floor_20, 0)
bug_dangerous = create_monster(Monster.bug_dangerous, MonsterCategory.cave_insects, dangerous_mines_20, 4)
cave_fly = create_monster(Monster.cave_fly, MonsterCategory.cave_insects, mines_floor_20, 0)
cave_fly_dangerous = create_monster(Monster.cave_fly_dangerous, MonsterCategory.cave_insects, dangerous_mines_60, 4)
grub = create_monster(Monster.grub, MonsterCategory.cave_insects, mines_floor_20, 0)
grub_dangerous = create_monster(Monster.grub_dangerous, MonsterCategory.cave_insects, dangerous_mines_60, 4)
mutant_fly = create_monster(Monster.mutant_fly, MonsterCategory.cave_insects, mutant_bug_lair, 2)
mutant_grub = create_monster(Monster.mutant_grub, MonsterCategory.cave_insects, mutant_bug_lair, 2)
armored_bug = create_monster(Monster.armored_bug, MonsterCategory.cave_insects, skull_cavern, 0) # Requires 'Bug Killer' enchantment
armored_bug_dangerous = create_monster(Monster.armored_bug_dangerous, MonsterCategory.cave_insects, skull_cavern, 2) # Requires 'Bug Killer' enchantment

duggy = create_monster(Monster.duggy, MonsterCategory.duggies, mines_floor_20, 0)
duggy_dangerous = create_monster(Monster.duggy_dangerous, MonsterCategory.duggies, dangerous_mines_20, 3)
magma_duggy = create_monster(Monster.magma_duggy, MonsterCategory.duggies, volcano, 4)

dust_sprite = create_monster(Monster.dust_sprite, MonsterCategory.dust_sprites, mines_floor_60, 0)
dust_sprite_dangerous = create_monster(Monster.dust_sprite_dangerous, MonsterCategory.dust_sprites, dangerous_mines_60, 3)

rock_crab = create_monster(Monster.rock_crab, MonsterCategory.rock_crabs, mines_floor_20, 0)
rock_crab_dangerous = create_monster(Monster.rock_crab_dangerous, MonsterCategory.rock_crabs, dangerous_mines_20, 3)
lava_crab = create_monster(Monster.lava_crab, MonsterCategory.rock_crabs, mines_floor_100, 2)
lava_crab_dangerous = create_monster(Monster.lava_crab_dangerous, MonsterCategory.rock_crabs, dangerous_mines_100, 4)
iridium_crab = create_monster(Monster.iridium_crab, MonsterCategory.rock_crabs, skull_cavern, 3)

mummy = create_monster(Monster.mummy, MonsterCategory.mummies, skull_cavern, 3) # Requires bombs or "Crusader" enchantment
mummy_dangerous = create_monster(Monster.mummy_dangerous, MonsterCategory.mummies, skull_cavern_dangerous, 4) # Requires bombs or "Crusader" enchantment

pepper_rex = create_monster(Monster.pepper_rex, MonsterCategory.pepper_rex, skull_cavern, 3)

serpent = create_monster(Monster.serpent, MonsterCategory.serpents, skull_cavern, 4)
royal_serpent = create_monster(Monster.royal_serpent, MonsterCategory.serpents, skull_cavern_dangerous, 5)

magma_sprite = create_monster(Monster.magma_sprite, MonsterCategory.magma_sprites, volcano, 4)
magma_sparker = create_monster(Monster.magma_sparker, MonsterCategory.magma_sprites, volcano_high, 4)

all_monsters_by_name = {monster.name: monster for monster in all_monsters}
all_monsters_by_category = {}
for monster in all_monsters:
    if monster.category not in all_monsters_by_category:
        all_monsters_by_category[monster.category] = []
    all_monsters_by_category[monster.category].append(monster)
