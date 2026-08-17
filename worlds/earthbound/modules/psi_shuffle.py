import struct
from ..Options import PSIShuffle
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import EarthBoundWorld
    from .Rom import LocalRom
    

def shuffle_psi(world: "EarthBoundWorld") -> None:
    world.offensive_psi_slots = [
        "Special",
        "Flash",
        "Fire",
        "Freeze",
        "Thunder",
        "Starstorm",
        "Blast",
        "Missile"
    ]

    world.assist_psi_slots = [
        "Hypnosis",
        "Paralysis",
        "Offense Up",
        "Defense Down",
        "Brainshock",
        "Defense up",
        "Drain",
        "Disable",
        "Stop",
        "Neutralize"
    ]

    world.shield_slots = [
        "Shield",
        "PSI Shield"
    ]

    world.jeff_offense_items = []
    world.jeff_assist_items = []

    world.psi_address = {
        "Special": [0x158A5F, 4],
        "Flash": [0x158B4F, 4],
        "Fire": [0x158A9B, 4],
        "Freeze": [0x158AD7, 4],
        "Thunder": [0x158B13, 4],
        "Starstorm": [0x3503FC, 4],

        "Shield": [0x158C21, 4],
        "PSI Shield": [0x158C5D, 4],

        "Hypnosis": [0x158CD5, 2],
        "Paralysis": [0x158D11, 2],
        "Offense Up": [0x158C99, 2],
        "Defense Down": [0x158CB7, 2],
        "Brainshock": [0x158D2F, 2],

        "Blast": [0x35041A, 4],
        "Missile": [0x350456, 4],

        "Defense up": [0x350492, 2],
        "Drain": [0x3504B0, 2],
        "Disable": [0x3504Ce, 2],
        "Stop": [0x3504EC, 2],
        "Neutralize": [0x35050A, 2],
    }

    if world.options.psi_shuffle:
        world.random.shuffle(world.offensive_psi_slots)

        if world.options.psi_shuffle != PSIShuffle.option_extended:
            adjust_psi_list(world.offensive_psi_slots, "Blast", 7)
            adjust_psi_list(world.offensive_psi_slots, "Missile", 7)

        if not world.options.allow_flash_as_favorite_thing:
            if world.offensive_psi_slots[0] == "Flash":
                adjust_psi_list(world.offensive_psi_slots, "Flash", world.random.randint(1, 5)) # Randomize which slot gets Flash

        world.random.shuffle(world.assist_psi_slots)

        if world.options.psi_shuffle != PSIShuffle.option_extended:
            adjust_psi_list(world.assist_psi_slots, "Defense up", 10)
            adjust_psi_list(world.assist_psi_slots, "Drain", 10)
            adjust_psi_list(world.assist_psi_slots, "Disable", 10)
            adjust_psi_list(world.assist_psi_slots, "Stop", 10)
            adjust_psi_list(world.assist_psi_slots, "Neutralize", 10)

        world.jeff_offense_items.extend(world.offensive_psi_slots[-2:])
        world.jeff_assist_items.extend(world.assist_psi_slots[-5:])
        world.offensive_psi_slots = world.offensive_psi_slots[:-2]
        world.assist_psi_slots = world.assist_psi_slots[:-5]

        world.random.shuffle(world.shield_slots)

        shield_data = {key: world.psi_address[key] for key in world.shield_slots}
        assist_data = {key: world.psi_address[key] for key in world.assist_psi_slots}
        assist_data_plus = {key: world.psi_address[key] for key in world.jeff_assist_items}
        offense_data_plus = {key: world.psi_address[key] for key in world.jeff_offense_items}

        world.psi_address = {key: world.psi_address[key] for key in world.offensive_psi_slots}
        world.psi_address.update(shield_data)
        world.psi_address.update(assist_data)
        world.psi_address.update(offense_data_plus)
        world.psi_address.update(assist_data_plus)

    world.psi_slot_data = [
        [[0x09, 0x00], [0x0B, 0x00], [0x0D, 0x00], [0x0F, 0x00]],  # Special
        [[0x09, 0x01], [0x0B, 0x01], [0x0D, 0x01], [0x0F, 0x01]],  # Flash
        [[0x09, 0x00], [0x0B, 0x00], [0x0D, 0x00], [0x0F, 0x00]],  # Fire
        [[0x09, 0x01], [0x0B, 0x01], [0x0D, 0x01], [0x0F, 0x01]],  # Freeze
        [[0x09, 0x02], [0x0B, 0x02], [0x0D, 0x02], [0x0F, 0x02]],  # Thunder
        [[0x09, 0x00], [0x0B, 0x00], [0x0D, 0x00], [0x0F, 0x00]],  # Starstorm

        [[0x09, 0x00], [0x0B, 0x00], [0x0D, 0x00], [0x0F, 0x00]],  # Shield
        [[0x09, 0x00], [0x0B, 0x00], [0x0D, 0x00], [0x0F, 0x00]],  # PSI Shield

        [[0x09, 0x01], [0x0B, 0x01]],  # Hypnosis
        [[0x09, 0x02], [0x0B, 0x02]],  # Paralysis
        [[0x09, 0x01], [0x0B, 0x01]],  # Offense Up
        [[0x09, 0x02], [0x0B, 0x02]],  # Defense Down
        [[0x09, 0x01], [0x0B, 0x01]],  # Brainshock

        [[0x09, 0x00], [0x0B, 0x00], [0x0D, 0x00], [0x0F, 0x00]],  # Blast
        [[0x09, 0x00], [0x0B, 0x00], [0x0D, 0x00], [0x0F, 0x00]],  # Missile

        [[0x09, 0x01], [0x0B, 0x01]],  # Defense up
        [[0x09, 0x02], [0x0B, 0x02]],  # Drain
        [[0x09, 0x01], [0x0B, 0x01]],  # Disable
        [[0x09, 0x02], [0x0B, 0x02]],  # Stop
        [[0x09, 0x01], [0x0B, 0x01]],  # Neutralize
    ]

    world.psi_level_data = [
        [[0x08, 0x00, 0x00], [0x16, 0x00, 0x00], [0x31, 0x00, 0x00], [0x4B, 0x00, 0x00]],  # Special
        [[0x12, 0x00, 0x00], [0x26, 0x00, 0x00], [0x3D, 0x00, 0x00], [0x43, 0x00, 0x00]],  # Flash
        [[0x00, 0x03, 0x00], [0x00, 0x13, 0x00], [0x00, 0x25, 0x00], [0x00, 0x40, 0x00]],  # Fire
        [[0x00, 0x01, 0x01], [0x00, 0x0B, 0x01], [0x00, 0x1F, 0x21], [0x00, 0x2E, 0x00]],  # Freeze
        [[0x00, 0x08, 0x01], [0x00, 0x19, 0x01], [0x00, 0x39, 0x29], [0x00, 0x00, 0x37]],  # Thunder
        [[0x00, 0x00, 0x00], [0x00, 0x00, 0x00], [0x00, 0x00, 0x00], [0x00, 0x00, 0x00]],  # Starstorm

        [[0x0C, 0x00, 0x0E], [0x00, 0x00, 0x0F], [0x22, 0x00, 0x10], [0x00, 0x00, 0x33]],  # Shield
        [[0x00, 0x06, 0x00], [0x00, 0x1B, 0x00], [0x00, 0x33, 0x00], [0x00, 0x3C, 0x00]],  # PSI Shield

        [[0x04, 0x00, 0x00], [0x1B, 0x00, 0x00]],  # Hypnosis
        [[0x0E, 0x00, 0x00], [0x1D, 0x00, 0x00]],  # Paralysis
        [[0x00, 0x15, 0x00], [0x00, 0x28, 0x00]],  # Offense Up
        [[0x00, 0x1D, 0x00], [0x00, 0x36, 0x00]],  # Defense Down
        [[0x00, 0x00, 0x18], [0x00, 0x00, 0x2C]],  # Brainshock

        # Level-up data needs to be zeroed out for these slots
        [[0x00, 0x00, 0x00], [0x00, 0x00, 0x00], [0x00, 0x00, 0x00], [0x00, 0x00, 0x00]],  # Blast
        [[0x00, 0x00, 0x00], [0x00, 0x00, 0x00], [0x00, 0x00, 0x00], [0x00, 0x00, 0x00]],  # Missile

        [[0x00, 0x00, 0x00], [0x00, 0x00, 0x00]],  # Defense up
        [[0x00, 0x00, 0x00], [0x00, 0x00, 0x00]],  # Drain
        [[0x00, 0x00, 0x00], [0x00, 0x00, 0x00]],  # Disable
        [[0x00, 0x00, 0x00], [0x00, 0x00, 0x00]],  # Stop
        [[0x00, 0x00, 0x00], [0x00, 0x00, 0x00]]  # Neutralize
        
    ]

    world.bomb_names = {
        "Special": ["Psycho bomb", "Mad psycho bomb", "Psywave emitter", "Psywave blaster", "Broken radio"],
        "Flash": ["Smoke bomb", "Flashbang", "Flash pan", "Digital camera", "Broken camera"],
        "Freeze": ["Ice bomb", "Dry ice bomb", "Frost ray", "Freeze ray", "Broken minifridge"],
        "Fire": ["Fire bomb", "Napalm bomb", "Blowtorch", "Flamethrower", "Broken grill"],
        "Thunder": ["Electric bomb", "EMP bomb", "Shock coil", "Tesla coil", "Broken spring"],
        "Starstorm": ["Comet bomb", "Nova bomb", "Meteor radar", "Star radar", "Broken radar"],
        "Blast": ["Bomb", "Super bomb", "Bazooka", "Heavy bazooka", "Broken bazooka"],
        "Missile": ["Rocket", "Nitro rocket", "Missile launcher", "Nitro launcher", "Broken vacuum"]
    }

    world.rocket_names = {
        "Special": ["Psionic shard", "Psionic orb", "Psionic crystal"],
        "Flash": ["Flashbulb", "Bright bulb", "Magna bulb"],
        "Freeze": ["LN2 bottle", "LN2 jug", "LN2 bucket"],
        "Fire": ["Flare", "Big flare", "Blitz flare"],
        "Thunder": ["Sparkler", "Big sparkler", "Mega sparkler"],
        "Starstorm": ["Meteor missile", "Star missile", "Nova missile"],
        "Blast": ["Firecracker", "Big firecracker", "Super firecracker"],
        "Missile": ["Bottle rocket", "Big bottle rocket", "Multi bottle rocket"]
    }

    world.spray_names = {
        "Hypnosis": "Chloroform spray",
        "Paralysis": "Nerve spray",
        "Offense Up": "Offense spray",
        "Defense Down": "Weakness spray",
        "Brainshock": "Confusion spray",
        "Defense up": "Defense spray",
        "Drain": "HP-straw",
        "Disable": "Distraction spray",
        "Stop": "Slime spray",
        "Neutralize": "Shield-off spray"
    }
    world.broken_gadgets = {
        "Hypnosis": ["Broken watch", "Broken screen"],
        "Paralysis": ["Broken razor", "Broken fan"],
        "Offense Up": ["Broken faucet", "Broken tuba"],
        "Defense Down": ["Broken sprinkler", "Broken trombone"],
        "Brainshock": ["Broken toaster", "Broken fryer"],
        "Defense up": ["Broken nozzle", "Broken trumpet"],
        "Drain": ["Broken hose", "Broken tube"],
        "Disable": ["Broken machine", "Broken device"],
        "Stop": ["Broken iron", "Broken steamer"],
        "Neutralize": ["Broken pipe", "Broken board"]
    }

    world.broken_desc = {
        "Hypnosis": [0x00EEEBA4, 0x00EEEBCC],
        "Paralysis": [0x00EEEC06, 0x00EEEC28],
        "Offense Up": [0x00EEEC4D, 0x00EEEC75],
        "Defense Down": [0x00EEECA5, 0x00EEECCB],
        "Brainshock": [0x00EEED00, 0x00EEED2B],
        "Defense up": [0x00EEED5A, 0x00C53929],
        "Drain": [0x00EEED8A, 0x00C538E0],
        "Disable": [0x00C53772, 0x00EEEDB2],
        "Stop": [0x00C53870, 0x00EEEE03],
        "Neutralize": [0x00C53897, 0x00EEEE2F]
    }

    world.gadget_names = {
        "Hypnosis": ["Hypno pendulum", "Hypno screen"],
        "Paralysis": ["Nerve taser", "Nerve ray"],
        "Offense Up": ["Offensalizer", "Offense shower"],
        "Defense Down": ["Weakalizer", "Weakness shower"],
        "Brainshock": ["Mind jammer", "Mind fryer"],
        "Defense up": ["Defensalizer", "Defense shower"],
        "Drain": ["HP-sucker", "Hungry HP-sucker"],
        "Disable": ["Counter-PSI unit", "PSI-nullifier unit"],
        "Stop": ["Slime generator", "Slime blaster"],
        "Neutralize": ["Shield killer", "Neutralizer"]
    }

    world.starstorm_address = {
        "Special": [0x002D, 0x003C],
        "Flash": [0x011D, 0x012C],
        "Fire": [0x0069, 0x0078],
        "Freeze": [0x00A5, 0x00B4],
        "Thunder": [0x00E1, 0x00F0],
        "Starstorm": [0x013B, 0x014A],
        "Blast": [0x0438, 0x0447],
        "Missile": [0x0474, 0x0483]
    }

    world.starstorm_spell_id = {
        "Special": [0x03, 0x04],
        "Flash": [0x13, 0x14],
        "Fire": [0x07, 0x08],
        "Freeze": [0x0B, 0x0C],
        "Thunder": [0x0F, 0x10],
        "Starstorm": [0x15, 0x16],
        "Blast": [0x48, 0x49],
        "Missile": [0x4C, 0x4D]
    }

    world.jeff_addresses = [
        0x156665,  # Bomb
        0x15668C,  # Super Bomb
        0x156443,  # Bazooka
        0x15646A,  # Heavy bazooka
        0x1551FB,  # broken bazooka

        0x1565F0,  # Bottle Rocket
        0x156617,  # Big Bottle Rocket
        0x15663E,  # multi Bottle Rocket
    ]

    world.gadget_addresses = [
        [0, 0x1567EB],  # defense shower
        [0x156491, 0x1564B8],  # HP-Sucker
        [0x1563F5],  # Counter-PSI Unit
        [0x156506],  # Slime Generator
        [0x15641C, 0x156DB5],  # Shield Killer
    ]

    world.broken_gadget_addresses = [
        0x155222,
        0x1551D4,
        0x15509C,
        0x15515F,
        0x155186
    ]

    world.bomb_desc = {
        "Special": [0x00EED4D8, 0x00EED521, 0x00EEDA4F, 0x00EEDA6B, 0x00EEDCFB],
        "Flash": [0x00EED538, 0x00EED5AB, 0x00EEDA87, 0x00EEDAD7, 0x00EEDD1D],
        "Fire": [0x00EED659, 0x00EED6CC, 0x00EEDB37, 0x00EEDB68, 0x00EEDD40],
        "Freeze": [0x00EED744, 0x00EED79D, 0x00EEDB85, 0x00EEDBA2, 0x00EEDD64],
        "Thunder": [0x00EED822, 0x00EED88E, 0x00EEDBBF, 0x00EEDBE4, 0x00EEDDA0],
        "Starstorm": [0x00EED4D8, 0x00EED521, 0x00EEDA4F, 0x00EEDCD2, 0x00EEDDC3],
        "Blast": [0x00C54EA7, 0x00C54EF7, 0x00C54AA1, 0x00C54AF5, 0x00C53908],
        "Missile": [0x00EED9A5, 0x00EED9FF, 0x00EEDC09, 0x00EEDC40, 0x00EEDDEE]
    }

    world.rocket_desc = {
        "Special": [0x00EEDE25, 0x00EEDE41, 0x00EEDE80],
        "Flash": [0x00EEDEDC, 0x00EEDF37, 0x00EEDFAE],
        "Fire": [0x00EEE013, 0x00EEE031, 0x00EEE061],
        "Freeze": [0x00EEE098, 0x00EEE0B5, 0x00EEE11E],
        "Thunder": [0x00EEE190, 0x00EEE1B6, 0x00EEE220],
        "Starstorm": [0x00EEE28B, 0x00EEE2A7, 0x00EEE2DB],
        "Blast": [0x00EEE344, 0x00EEE35B, 0x00EEE36E],
        "Missile": [0x00C54E01, 0x00C54E20, 0x00C54E54]
    }

    world.spray_desc = {
        "Hypnosis": 0x00EEE653,
        "Paralysis": 0x00EEE688,
        "Offense Up": 0x00EEE6B9,
        "Defense Down": 0x00EEE705,
        "Brainshock": 0x00EEE751,
        "Defense up": 0x00C2558D,
        "Drain": 0x00EEE802,
        "Disable": 0x00EEE838,
        "Stop": 0x00EEE7D0,
        "Neutralize": 0x00EEE78F
    }

    world.gadget_desc = {
        "Hypnosis": [0x00EEE87B, 0x00EEE8AA],
        "Paralysis": [0x00EEE8DA, 0x00EEE905],
        "Offense Up": [0x00EEE933, 0x00EEE97F],
        "Defense Down": [0x00EEE9C2, 0x00EEEA0E],
        "Brainshock": [0x00EEEA9D, 0x00EEEAD2],
        "Defense up": [0x00EEEA51, 0x00C5519F],
        "Drain": [0x00C54B67, 0x00C54BB0],
        "Disable": [0x00C54A3A, 0x00EEEB5E],
        "Stop": [0x00C54C32, 0x00EEEB09],
        "Neutralize": [0x00C54A6C, 0x00C559D9]
    }

    world.bomb_actions = {
        "Special": [0x01AC, 0x01AD, 0x01CF, 0x01D0],
        "Flash": [0x01AE, 0x01AF, 0x01D1, 0x01D2],
        "Fire": [0x01B0, 0x01B1, 0x01D3, 0x01D4],
        "Freeze": [0x01B2, 0x01B3, 0x01D5, 0x01D6],
        "Thunder": [0x01B4, 0x01B5, 0x01D7, 0x01D8],
        "Starstorm": [0x01B6, 0x01B7, 0x01D9, 0x01DA],
        "Blast": [0x00A7, 0x00A8, 0x0136, 0x0137],
        "Missile": [0x01B8, 0x01B9, 0x01DB, 0x01DC]
    }

    world.missile_actions = {
        "Special": [0x01BA, 0x01BB, 0x01BC],
        "Flash": [0x01BD, 0x01BE, 0x01BF],
        "Fire": [0x01C0, 0x01C1, 0x01C2],
        "Freeze": [0x01C3, 0x01C4, 0x01C5],
        "Thunder": [0x01C6, 0x01C7, 0x01C8],
        "Starstorm": [0x01C9, 0x01CA, 0x01CB],
        "Blast": [0x01CC, 0x01CD, 0x01CE],
        "Missile": [0x00A3, 0x00A4, 0x00A5]
    }

    world.gadget_actions = {
        "Hypnosis": [0x01E7, 0x01E8],
        "Paralysis": [0x01E9, 0x01EA],
        "Offense Up": [0x01EB, 0x01EC],
        "Defense Down": [0x01ED, 0x01EE],
        "Brainshock": [0x01EF, 0x01F0],
        "Defense up": [0x00B7, 0x00B8],
        "Drain": [0x00A1, 0x00B0],
        "Disable": [0x009F, 0x01F1],
        "Stop": [0x00A9, 0x01F2],
        "Neutralize": [0x00A0, 0x00F7]
    }

    world.jeff_item_counts = [
        5,  # Bomb
        3  # Bottle Rocket
    ]

    world.gadget_counts = [
        1,  # defense shower
        2,  # HP-Sucker
        1,  # Counter PSI unit
        1,  # Slime generator
        2  # Neutralizer
    ]

    world.gadget_ids = [
        [0x00, 0x9D],
        [0x87, 0x88],
        [0x83],
        [0x8A],
        [0x84, 0xC3]
    ]

    world.broken_gadget_ids = [
        0x0E,  # Broken trumpet
        0x0C,  # Broken tube
        0x04,  # Broken machine
        0x09,  # Broken iron
        0x0A  # Broken pipe
    ]

    world.jeff_item_names = [
        world.bomb_names,
        world.rocket_names
    ]

    world.jeff_help_text = [
        world.bomb_desc,
        world.rocket_desc
    ]

    world.attack_types = [
        world.bomb_actions,
        world.missile_actions
    ]


def write_psi(world: "EarthBoundWorld", rom: "LocalRom") -> None:
    from ..game_data.text_data import text_encoder
    psi_num = 0
    for spell, (address, levels) in world.psi_address.items():
        for i in range(levels):
            rom.write_bytes(address + 9, bytearray(world.psi_slot_data[psi_num][i]))
            rom.write_bytes(address + 6, bytearray(world.psi_level_data[psi_num][i]))
            if psi_num == 0:
                rom.write_bytes(address, bytearray([0x01]))
            elif psi_num == 5 and i > 1:
                rom.write_bytes(0x01C4AB + (0x9E * (i - 2)), struct.pack("H", world.starstorm_address[spell][i - 2]))  # Menu spells
                rom.write_bytes(0x01C536 + (0x78 * (i - 2)), bytearray([world.starstorm_spell_id[spell][i - 2]]))  # What spell is controlled by the PSI flags
                rom.write_bytes(0x2E957F + (0x11 * (i - 2)), bytearray([world.starstorm_spell_id[spell][i - 2]]))  # The global Poo PSI text
                rom.write_bytes(address + 9, bytearray(world.psi_slot_data[psi_num][i - 2]))

            if spell == "Special" and psi_num != 0:
                rom.write_bytes(address, bytearray([0x12]))

            address += 15
            if spell == "Starstorm" and i == 1:
                address = 0x158B8B
    # todo; expanded psi
    # todo; animation for Starstorm L/D
    # todo; swap enemy actions for Special?
    # todo; cleanup stuff
        psi_num += 1

    # rom.write_bytes(0x2E957F + (0x11 * (i - 2)), bytearray([world.starstorm_spell_id[spell][i - 2]]))
    # Starstorm spell for the item locally
    rom.write_bytes(0x2EAE2E,  bytearray([world.starstorm_spell_id[world.offensive_psi_slots[5]][0]]))
    rom.write_bytes(0x2EAE38,  bytearray([world.starstorm_spell_id[world.offensive_psi_slots[5]][1]]))

    jeff_item_num = 0
    jeff_item_index = 0
    for item in world.jeff_offense_items:
        for i in range(world.jeff_item_counts[jeff_item_num]):
            address = world.jeff_addresses[jeff_item_index]
            jeff_item_index += 1
            name = world.jeff_item_names[jeff_item_num][item][i]
            description = world.jeff_help_text[jeff_item_num][item][i]
            name_encoded = text_encoder(name, 22)
            name_encoded.extend(([0x00]))
            rom.write_bytes(address, name_encoded)
            rom.write_bytes(address + 35, struct.pack("I", description))
            if "Broken" not in name:  # broken items don't need attack data
                attack = world.attack_types[jeff_item_num][item][i]
                rom.write_bytes(address + 29, struct.pack("H", attack))
        jeff_item_num += 1
    jeff_item_num = 0
    name = world.spray_names[world.jeff_assist_items[0]]
    name_encoded = text_encoder(name, 22)
    name_encoded.extend(([0x00]))
    description = world.spray_desc[world.jeff_assist_items[0]]
    address = 0x156887
    action = world.gadget_actions[world.jeff_assist_items[0]][0]
    rom.write_bytes(address, name_encoded)
    rom.write_bytes(address + 35, struct.pack("I", description))
    rom.write_bytes(address + 29, struct.pack("H", action))

    for item in world.jeff_assist_items:
        for i in range(world.gadget_counts[jeff_item_num]):
            if jeff_item_num == 0:
                i = 1
            name = world.gadget_names[item][i]
            name_encoded = text_encoder(name, 22)
            name_encoded.extend(([0x00]))
            description = world.gadget_desc[item][i]
            action = world.gadget_actions[world.jeff_assist_items[jeff_item_num]][i]
            address = world.gadget_addresses[jeff_item_num][i]
            rom.write_bytes(address, name_encoded)
            rom.write_bytes(address + 35, struct.pack("I", description))
            rom.write_bytes(address + 29, struct.pack("H", action))
            rom.write_bytes(description - 0xC00000 + 5, bytearray([world.gadget_ids[jeff_item_num][i]]))
        jeff_item_num += 1

    for i in range(5):
        item = world.jeff_assist_items[i]
        if i < 2:
            level = 1
        else:
            level = 0
        address = world.broken_gadget_addresses[i]
        name = world.broken_gadgets[item][level]
        description = world.broken_desc[item][level]
        name_encoded = text_encoder(name, 22)
        name_encoded.extend(([0x00]))
        rom.write_bytes(address, name_encoded)
        rom.write_bytes(address + 35, struct.pack("I", description))
        rom.write_bytes(description - 0xC00000 + 5, bytearray([world.broken_gadget_ids[i]]))

    rom.write_bytes(0x15A8EB, bytearray(struct.pack("H", world.gadget_actions[world.jeff_assist_items[4]][1])))
    rom.write_bytes(0x15BB45, bytearray(struct.pack("H", world.gadget_actions[world.jeff_assist_items[0]][0])))
    rom.write_bytes(0x15BBA5, bytearray(struct.pack("H", world.gadget_actions[world.jeff_assist_items[4]][0])))
    rom.write_bytes(0x15DF41, bytearray(struct.pack("H", world.gadget_actions[world.jeff_assist_items[4]][0])))
    rom.write_bytes(0x15DF3F, bytearray(struct.pack("H", world.gadget_actions[world.jeff_assist_items[4]][1])))
    rom.write_bytes(0x15BA2B, bytearray(struct.pack("H", world.gadget_actions[world.jeff_assist_items[1]][0])))
    rom.write_bytes(0x15C06D, bytearray(struct.pack("H", world.gadget_actions[world.jeff_assist_items[1]][1])))


def adjust_psi_list(psi_input: list[str], spell: str, index: int) -> None:
    """Move a spell in the PSI table to a different entry/slot"""
    psi_input.insert(index, (psi_input.pop(psi_input.index(spell))))
