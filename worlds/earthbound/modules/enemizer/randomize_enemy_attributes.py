import struct
from .enemy_attributes import (enemy_species, enemy_adjectives, battle_sprites, field_sprites, excluded_enemies,
                               insects, robots, movement_patterns, start_texts, death_texts, weakness_table)
from ...game_data.text_data import calc_pixel_width, text_encoder
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ... import EarthBoundWorld
    from ...Rom import LocalRom
shield_statuses = [
    "phys_1",
    "phys_2",
    "psi_1",
    "psi_2"
]

battle_songs = [
    0x60,
    0x61,
    0x62,
    0x63,
    0x64,
    0x65,
    0x66,
    0x67,
    0x68,
    0x69,
    0x8D,
    0x94
]


def randomize_enemy_attributes(world: "EarthBoundWorld", rom: "LocalRom") -> None:
    """Randomizes various attributes of enemies. This includes the name,
       gender, sprite, color, etc. Data can be found in enemy_attributes."""
    taken_names = []
    for enemy in world.enemies:
        if enemy not in excluded_enemies and " (" not in enemy:
            new_name = "FFFFFFFFFFFFFFFFFFFFFFFFFF"
            pixel_width = calc_pixel_width(new_name)
            species = "Null"
            while not (len(new_name) <= 25 and new_name not in taken_names and pixel_width <= 95):
                species = world.random.choice(enemy_species)
                adjective = world.random.choice(enemy_adjectives)
                new_name = adjective + species
                pixel_width = calc_pixel_width(new_name)
            taken_names.append(new_name)
            sprite = world.random.choice(battle_sprites[species])
            field_sprite = field_sprites[sprite]
            world.enemy_sprites[enemy] = field_sprite
            movement_pattern = movement_patterns[field_sprite]
            palette = world.random.randint(1, 31)
            gender = world.random.randint(1, 3)
            if species in robots:
                enemy_type = 2
            elif species in insects:
                enemy_type = 1
            else:
                enemy_type = 0
            row = world.random.randint(0, 1)
            mirror_chance = world.random.randint(0, 100)
            start_text = world.random.choice(start_texts)
            death_text = world.random.choice(death_texts)
            if species in ["Power Robot", "Reactor Robot", "Sphere"]:
                death_action = 0x0040
            elif species == "Oak":
                death_action = 0x0041
            else:
                death_action = 0x0000
            music = world.random.choice(battle_songs)
            drop_rate = world.random.randint(0, 7)
            base_drop = world.random.choice(world.filler_drops)
            if world.random.randint(1, 100) < 6:
                status = world.random.randint(1, 7)
                if status < 5:
                    world.enemies[enemy].has_shield = shield_statuses[status - 1]
            else:
                status = 0

            if species in ["Party Man", "Reveler"]:
                miss_rate = 6
            elif species == "Boy":
                miss_rate = 8
            elif species == "Bot":
                miss_rate = 5
            else:
                miss_rate = world.random.randint(0, 4)
                
            fire_weakness = get_weakness("Fire", species)

            freeze_weakness = get_weakness("Freeze", species)

            flash_weakness = get_weakness("Flash", species)

            paralysis_weakness = get_weakness("Paralysis", species)

            hypnosis_weakness = get_weakness("Hypnosis", species)

            address = world.enemies[enemy].address
            new_name = text_encoder(new_name, 0x18)
            if len(new_name) < 0x18:
                new_name.extend([0x00])

            if world.enemies[enemy].attack_extensions > 1:
                num_enemies = world.enemies[enemy].attack_extensions
            else:
                num_enemies = 1

            for i in range(num_enemies):
                rom.write_bytes(address, bytearray([0x01]))
                rom.write_bytes(address + 1, new_name)
                rom.write_bytes(address + 0x1A, bytearray([gender]))
                rom.write_bytes(address + 0x1B, bytearray([enemy_type]))
                rom.write_bytes(address + 0x1C, struct.pack("H", sprite))
                rom.write_bytes(address + 0x1E, struct.pack("H", field_sprite))
                rom.write_bytes(address + 0x2B, struct.pack("H", movement_pattern))
                rom.write_bytes(address + 0x2D, struct.pack("I", start_text))
                rom.write_bytes(address + 0x31, struct.pack("I", death_text))
                rom.write_bytes(address + 0x35, bytearray([palette]))
                rom.write_bytes(address + 0x37, bytearray([music]))
                rom.write_bytes(address + 0x3F, bytearray([fire_weakness]))
                rom.write_bytes(address + 0x40, bytearray([freeze_weakness]))
                rom.write_bytes(address + 0x41, bytearray([flash_weakness]))
                rom.write_bytes(address + 0x42, bytearray([paralysis_weakness]))
                rom.write_bytes(address + 0x43, bytearray([hypnosis_weakness]))
                rom.write_bytes(address + 0x43, bytearray([miss_rate]))
                rom.write_bytes(address + 0x4E, struct.pack("H", death_action))
                rom.write_bytes(address + 0x57, bytearray([drop_rate]))
                rom.write_bytes(address + 0x58, bytearray([base_drop]))
                rom.write_bytes(address + 0x59, bytearray([status]))
                rom.write_bytes(address + 0x5B, bytearray([row]))
                rom.write_bytes(address + 0x5D, bytearray([mirror_chance]))
                if world.enemies[enemy].attack_extensions > 1:
                    address = world.enemies[f"{enemy} ({i + 2})"].address
                    enemy = f"{enemy} ({i + 2})"


def get_weakness(element: str, species: str) -> int:
    """Returns a weakness to given element, given the enemy's base species."""
    if species in weakness_table[element]:
        weakness = weakness_table[element][species]
    else:
        weakness = 1
    return weakness
