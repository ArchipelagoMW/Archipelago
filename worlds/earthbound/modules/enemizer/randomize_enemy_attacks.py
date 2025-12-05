import struct
from .enemy_attributes import excluded_enemies
from ..enemy_data import spell_breaks
from ..enemy_shuffler import enemy_ids
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ... import EarthBoundWorld
    from ...Rom import LocalRom

battle_actions = {  # Actions in camel case are scaled
    "Attack": 0x04,
    "Shoot": 0x05,
    "Spy": 0x06,
    "Defend": 0x08,
    "None": 0x09,
    "Magnet Alpha": 0x36,
    "Magnet Omega": 0x37,
    "Call": 0x3E,
    "Sow Seeds": 0x3F,
    "Steal": 0x42,
    "Freeze in Time": 0x43,
    "diamond_eyes": 0x44,
    "Strange Beam": 0x46,
    "nauseous_breath": 0x47,
    "poison_stinger": 0x48,
    "kiss_of_death": 0x49,
    "Arctic Breath": 0x4A,
    "Mushroom Spores": 0x4B,
    "Possess": 0x4C,
    "Sprinkle Powder": 0x4D,
    "Mold Spores": 0x4E,
    "Binding Attack": 0x4F,
    "Sticky Mucus": 0x50,
    "Spew Fly Honey": 0x51,
    "Shoot Silk": 0x52,
    "Say Something Scary": 0x53,
    "Do Something Mysterious": 0x54,
    "Disrupt Sense": 0x55,
    "Size Up Situation": 0x56,
    "Exhale Stinky": 0x57,
    "summon_storm": 0x58,
    "scalding_espresso": 0x59,
    "Haunting Melody": 0x5A,
    "extinguishing_blast": 0x5B,
    "crashing_boom_bang": 0x5C,
    "spray_fire": 0x5D,
    "breathe_fire": 0x5E,
    "Spin Around": 0x5F,
    "Lose Temper": 0x60,
    "Say Nasty": 0x61,
    "Vacuum Attack": 0x62,
    # "Replenish Fuel",
    "poisonous_fangs": 0x64,
    # Dizzy Missile
    "Continuous Attack": 0x66,
    "Guard": 0x67,
    "flaming_fireball": 0x68,
    "Intertwine": 0x69,
    "Crushing Chop": 0x6A,
    "Submission Hold": 0x6B,
    "Rev and Accelerate": 0x6C,
    "Brandish a Knife": 0x6D,
    "Tear Into": 0x6E,
    "Bite": 0x6F,
    "Claw with Nails": 0x70,
    "Swing Tail": 0x71,
    "Lunge": 0x72,
    "Shopping Bag": 0x73,
    "Swing Club": 0x74,
    "Tornado": 0x75,
    "Spray Water": 0x76,
    "Flash a Menacing Smile": 0x77,
    "Laugh Hysterically": 78,
    "Edge Closer": 0x79,
    "Whisper 3": 0x7A,
    "Murmur 2": 0x7B,
    "Mutter 1": 0x7C,
    "Fall down": 0x7D,
    "Be Absentminded": 0x7E,
    "Burst of Steam": 0x7F,
    "Wobble": 0x80,
    "Reel": 0x81,
    "Big Grin": 0x82,
    "Take Breath": 0x83,
    "Greeting": 0x84,
    "Howl": 0x85,
    "Tick Tock": 0x86,
    # "Eat Food": 0x8A,
    "PSI Food": 0x8E,
    # Counter PSI: 0x9F World.gadget actions?
    # Shield Killer
    # HP Sucker
    "Yogurt Dispenser": 0xAA,
    "Toothbrush": 0xAE,
    "Sudden Guts": 0xB6,
    "Ruler": 0xBA,
    "Protractor": 0xBB,
    "Fly Honey": 0xBD,
    "glorious_light": 0xC9,
    "electrical_shock": 0xCA,
    "paralyzing_pollen": 0xCB,
    "Icy Hand": 0xCC,
    "poison_flute": 0xCD,
    "Exhaust Fumes": 0xCE,
    "Laugh Maniacally": 0xCF,
    "Breathe Flute": 0xD0,
    "Leap and Spread Wings": 0xD1,
    "Become Friendly": 0xD2,
    "Rumble": 0xD3,
    "Give Hug": 0xD4,
    "hacking_cough": 0xD5,
    "Misery Attack": 0xD6,
    "Paint Attack": 0xD7,
    "Come Out Swinging": 0xD8,
    "Scratch with Claws": 0xD9,
    "Peck at Eyes": 0xDA,
    "Ram and Trample": 0xDB,
    "Punch": 0xDC,
    "Spit Seeds": 0xDD,
    "Fire a Beam": 0xDE,
    "Spear": 0xDF,
    "Stomp with Foot": 0xE0,
    "Hula Hoop": 0xE1,
    "Charge Forward": 0xE2,
    "Shred on Skateboard": 0xE3,
    "diamond_bite": 0xE4,
    "Grumble": 0xE5,
    "Lecture": 0xE6,
    "Scow": 0xE7,
    "Vent Odor": 0xE8,
    "Shout": 0xE9,
    "Shriek": 0xEA,
    "Knit Brow": 0xEB,
    "scatter_spores": 0xED,
    "Bite Attack": 0xEE,
    "stuffiness_beam": 0xF1,
    "Coil Around": 0xF2,
    "Emit Light": 0xF8,
    "Homesick": 0xFB,
    "Fake PSI": 0x0100,
    "Bark": 0x0108,
    "Chant": 0x0109,
    "Scratch Head": 0x010B,
    "Discharge Gas": 0x0111,
    "Monkey Love": 0x011B,
    "Lost Bolts": 0x013A,
    "Clean Area": 0x013C,
    "Want Battery": 0x013D,
    "throw_bomb": 0x01FC,
    "shoot_rocket": 0x0203

}

needs_argument = {
    "PSI Food": [0xCF, 0xF7, 0x6E, 0xF6, 0x63, 0x62],
    "Ruler": [0x8C],
    "Protractor": [0x8F],
    "Toothbrush": [0x9A],
    "Monkey Love": [0xD1],
    "Sudden Guts": [0x9F],
    "Shield Alpha": [0x1F],
    "Shield Beta": [0x21],
    "PSI Shield Alpha": [0x23],
    "PSI Shield Beta": [0x25],
    "Offense Up Alpha": [0x27],
    "Offense Up Omega": [0x28],
    "Defense Down Alpha": [0x29],
    "Defense Down Omega": [0x2A],
    "Hypnosis Alpha": [0x2B],
    "Hypnosis Omega": [0x2C],
    "Brainshock": [0x31],
    "Magnet Alpha": [0x2D],
    "Magnet Omega": [0x2E],
    "Yogurt Dispenser": [0x8B],
    "Fake PSI": [0x55, 0x04, 0x14, 0x16, 0x30, 0x32, 0x4D, 0x57]
}

psi_actions = {
    "special": 0x0A,
    "fire": 0x0E,
    "freeze": 0x12,
    "thunder": 0x16,
    "flash": 0x1A,
    "starstorm": 0x1E,
    "lifeup": 0x20,
    "healing": 0x24,
    "Shield Alpha": 0x28,
    "Shield Beta": 0x29,
    "PSI Shield Alpha": 0x2C,
    "PSI Shield Beta": 0x2D,
    "Offense Up Alpha": 0x30,
    "Offense Up Omega": 0x31,
    "Defense Down Alpha": 0x32,
    "Defense Down Omega": 0x33,
    "Hypnosis Alpha": 0x34,
    "Hypnosis Omega": 0x35,
    "paralysis": 0x38,
    "Brainshock": 0x3A,
    "blast": 0x01A4,
    "missile": 0x01A8
}



def randomize_enemy_attacks(world: "EarthBoundWorld", rom: "LocalRom") -> None:
    """Generates random attacks for enemies.
       Certain attacks need to have an argument variable attached.
       PSI moves have a 19% chance of being rolled only if the enemy has a non-zero max PP stat."""
    for enemy in world.enemies:
        if enemy not in excluded_enemies:
            enemy_ai = world.random.randint(0, 3)
            world.enemy_psi[enemy] = ["null", "null", "null", "null"]
            max_calls = 0
            for i in range(4):
                if world.enemies[enemy].pp and world.random.randint(1, 100) < 20:
                    attack = world.random.choice(list(psi_actions.keys()))
                    attack_id = psi_actions[attack]
                else:
                    attack = world.random.choice(list(battle_actions.keys()))
                    attack_id = battle_actions[attack]
                if attack in spell_breaks:
                    world.enemy_psi[enemy][i] = attack
                
                if attack in needs_argument:
                    argument = world.random.choice(needs_argument[attack])
                elif attack in ["Sow Seeds", "Call"]:
                    argument = enemy_ids[enemy]
                    max_calls = world.random.randint(1, 4)
                else:
                    argument = 0
                
                rom.write_bytes(world.enemies[enemy].address + (0x46 + (i * 2)), struct.pack("H", attack_id))
                rom.write_bytes(world.enemies[enemy].address + (0x50 + (i)), bytearray([argument]))
                rom.write_bytes(world.enemies[enemy].address + 0x5C, bytearray([max_calls]))
                rom.write_bytes(world.enemies[enemy].address + 0x45, bytearray([enemy_ai]))
                # Todo; attack extenders?
