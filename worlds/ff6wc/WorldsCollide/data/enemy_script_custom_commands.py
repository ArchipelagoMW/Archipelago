from ..memory.space import Bank, START_ADDRESS_SNES, Reserve, Allocate, Write
from ..instruction import asm as asm

# 0xf0 custom argument values (e.g. FIRE1 = randomly choose from fire category with tier +1)
FIRE0, FIRE1, FIRE2, ICE0, ICE1, ICE2, BOLT0, BOLT1, BOLT2, EARTH0, EARTH1, EARTH2, WIND0, WIND1, WIND2, WATER0, WATER1, WATER2, POISON0, POISON1, POISON2, PEARL0, PEARL1, PEARL2, NON_ELEMENTAL0, NON_ELEMENTAL1, NON_ELEMENTAL2 = range(0x36, 0x51)
# NOTE: gap in range here to keep original skean/edge/storm argument ids
CURE0, CURE1, CURE2, TEK0, TEK1, TEK2, DAMAGE0, DAMAGE1, DAMAGE2, SPECIAL0, SPECIAL1, SPECIAL2 = range(0x55, 0x61)
# NOTE: 0x61 to 0x63 still available

def get_custom_ability_tier(category_tier):
    if category_tier >= 0x55:
        category_tier -= 1
    return category_tier % 3

class EnemyScriptCommands:
    def __init__(self, rom, args, enemy_scripts, enemies):
        self.rom = rom
        self.args = args
        self.enemy_scripts = enemy_scripts
        self.enemies = enemies

    def hp_check_command_mod(self):
        # modify script command [0xfc, 0x06, target, hp_value]
        # change hp_value to a percentage of the target's maximum hp

        # NOTE: small rounding errors can occur from division
        src = [
            asm.LDA(0x3a2f, asm.ABS),   # a = percent
            asm.STA(0xe8, asm.DIR),     # $e8 = percent
            asm.A16(),
            asm.LDA(0x3c1c, asm.ABS_Y), # a = max_hp
            asm.PHX(),
            asm.LDX(0x64, asm.IMM8),    # x = 100
            asm.CMP(0x028f, asm.IMM16), # compare max_hp with 655 (prevent 2 byte multiplication overflow)
            asm.BCC("HP < 655"),        # branch if max_hp < 655 (safe for 16 bit hp and 8 bit percent multiply)

            "HP >= 655",
            asm.JSR(0x4792, asm.ABS),   # a = max_hp / 100
            asm.JSR(0x47b7, asm.ABS),   # $e8 = (max_hp / 100) * percent
            asm.LDA(0xe8, asm.DIR),     # a = (max_hp / 100) * percent
            asm.BRA("RETURN"),

            "HP < 655",
            asm.JSR(0x47b7, asm.ABS),   # $e8 = max_hp * percent
            asm.LDA(0xe8, asm.DIR),     # a = max_hp * percent
            asm.JSR(0x4792, asm.ABS),   # a = (max_hp * percent) / 100

            "RETURN",
            asm.PLX(),
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "enemy script calculate percent of max hp")
        hp_percent_calculate = space.start_address

        space = Reserve(0x21bbd, 0x21bc3, "enemy script command 0xfc 0x06 calculate hp threshold", asm.NOP())
        space.write(
            asm.JSR(hp_percent_calculate, asm.ABS),
        )

    def hp_conditions_mod(self):
        # change hp value checks to hp percent checks

        # enemies and the number of hp checks they have
        enemy_checks = [("Intangir", 1), ("Vargas", 2), ("TunnelArmr", 1), ("Dadaluma", 1), ("Umaro", 1), ("AtmaWeapon", 3),
                        ("SrBehemoth", 1), ("Dullahan", 1), ("Doom", 1), ("Goddess", 1), ("Poltrgeist", 1), ("Kefka (Final)", 4),
                        ("Ultros 3", 2), ("Laser Gun", 1), ("MissileBay", 1), ("Chadarnook (Demon)", 1),
                        ("Storm Drgn", 1), ("Blue Drgn", 1), ("Red Dragon", 1), ("Short Arm", 1), ("Long Arm", 1), ("Face", 1),
                        ("Tiger", 1), ("Tools", 1), ("Magic", 4), ("Sleep", 2), ("Ultros 4", 1), ("Phunbaba 2", 1),
                        ("Phunbaba 3", 1), ("Atma", 1)]

        import math
        from ..data import enemy_script_commands as ai_instr
        for enemy_name, check_count in enemy_checks:
            enemy_id = self.enemies.get_enemy(enemy_name)
            enemy = self.enemies.enemies[enemy_id]
            script = self.enemy_scripts.scripts[enemy_id]

            search_start = 0
            replacement_count = 0
            hp_check_prefix = [0xfc, 0x06, 0x36] # check hp of self (self was only target i found used)
            for instruction_index, instruction in enumerate(script.instructions):
                values = instruction()
                if values[:len(hp_check_prefix)] == hp_check_prefix:
                    hp_value = values[3]
                    hp_percent = min(100, math.ceil(((hp_value * 128) / enemy.original_hp) * 100))
                    values[3] = hp_percent

                    script.instructions[instruction_index] = ai_instr.If(*values[1 : ])
                    replacement_count += 1
            assert(replacement_count == check_count)

    def random_tiered_ability_mod(self, space):
        # modify script command [0xf0, possible_id, possible_id, possible_id]
        # returns a random tiered spell if possible_id is an esper/swdtech/blitz id

        # tier = min(enemy level / levels_per_tier, 8) + (argument offset) + (random offset in range [-2, 2])
        # e.g. with a level 10 enemy, 5 = levels_per_tier and argument offset +1 the tier will be between 1 and 5
        # arguments now indicate the category as well as a tier offset of either +0, +1, or +2
        #   original argument ids still valid as long as not esper/swdtech/blitz id

        # for special attacks there are 16 damage tiers in vanilla, this function sets them dynamically
        # tier = min(enemy_level / 4, 11) + (argument offset) + (random offset in range [-2, 2])

        from ..data.spells import Spells
        from ..data.spell_names import name_id
        from ..data import enemy_ability_tiers as ability_tiers
        from ..instruction import c4 as c4

        # max tier reachable based only on enemy level (can be increased further from argument/distortion)
        MAX_ENEMY_LEVEL_TIER = 8
        ENEMY_LEVELS_PER_TIER = self.args.ability_scaling_factor + 3
        MAX_ENEMY_LEVEL_SPECIAL_TIER = 11
        ENEMY_LEVELS_PER_SPECIAL_TIER = 4
        MAX_SPECIAL_TIER = 15

        categories = [ability_tiers.fire, ability_tiers.ice, ability_tiers.bolt, ability_tiers.earth,
                      ability_tiers.wind, ability_tiers.water, ability_tiers.poison, ability_tiers.pearl,
                      ability_tiers.non_elemental, ability_tiers.cure, ability_tiers.tek, ability_tiers.damage]

        tier_addresses = []
        for category in categories:
            for tier in category:
                tier_addresses.append(space.next_address)
                space.write(tier)
        tier_addresses.append(space.next_address)

        tier_table_pointers = space.next_address
        for address in tier_addresses:
            space.write(address.to_bytes(3, "little")[:2]),

        # ability tier is distorted by between [-2, 2], the distortion amounts are weighted
        # store thresholds for mapping 0-255 random number generator to distribution
        tier_distribution_thresholds = [
            0x00, #   0 -  24 = tier-2 (~10%)
            0x19, #  25 -  88 = tier-1 (~25%)
            0x59, #  89 - 177 = tier   (~35%)
            0xb2, # 178 - 241 = tier+1 (~25%)
            0xf2, # 242 - 255 = tier+2 (~05%)
        ]
        tier_distribution_table = space.next_address
        space.write(tier_distribution_thresholds)

        get_tier_distortion = space.next_address
        space.write(
            # distort the tier based on tier_distribution_table
            asm.JSR(c4.battle_rng, asm.ABS),# a = random number (0-255)
            asm.LDX(len(tier_distribution_thresholds) - 1, asm.IMM8),

            "THRESHOLD_LOOP_START",
            asm.CMP(tier_distribution_table + START_ADDRESS_SNES, asm.LNG_X),
            asm.BGE("THRESHOLD_LOOP_EXIT"), # branch if random value >= tier_threshold[x]
            asm.DEX(),
            asm.BPL("THRESHOLD_LOOP_START"),# branch if x >= 0

            "THRESHOLD_LOOP_EXIT",
            asm.TXA(),                      # a = random_tier_offset + 2 (not shifted to [-2, 2] range yet)
            asm.CLC(),
            asm.ADC(0xee, asm.DIR),         # a = random_tier_offset + 2 + current offset
            asm.CMP(0x02, asm.IMM8),        # check if shifting random tier offset will result in negative value
            asm.BGE("MIN_CHECKED"),         # branch if final tier >= 2
            asm.LDA(0x02, asm.IMM8),        # shifting random_tier_offset will result in negative tier, clamp to zero

            "MIN_CHECKED",
            asm.DEC(),                      # subtract 2 (convert random_tier_offset range to [-2, 2])
            asm.DEC(),
            asm.RTS(),
        )

        # tier based on enemy level (0 to 8) + random offset (-2 to 2) + argument offset (0 to 2)
        get_random_tiered_spell = space.next_address
        space.write(
            asm.SEC(),
            asm.SBC(Spells.SPELL_COUNT, asm.IMM8),  # convert argument to 0 based index
            asm.CMP(0x1b, asm.IMM8),
            asm.BLT("GET_CATEGORY"),                # branch if id < 0x1b (args < 0x1b now 0 based)

            # the randomization flags are not contiguous because of skean/edge/storm
            # if id comes after 0x50 then subtract another 4 from the argument to make the indices contigous
            asm.SEC(),
            asm.SBC(0x04, asm.IMM8),                # convert argument to 0 based index

            # 0 based argument indicates category and an offset (+0, +1, or +2)
            "GET_CATEGORY",
            asm.LDX(0x03, asm.IMM8),                # a = divisor (number of values per category: +0, +1, +2)
            asm.JSR(c4.divide, asm.ABS),            # a = argument / 3 = category (e.g. fire/ice/cure/tek/damage/...)
            asm.STX(0xee, asm.DIR),                 # $ee = argument % 3 = offset (+0, +1, or +2)
            asm.XBA(),                              # b = category
            asm.LDA(ability_tiers.TIER_COUNT, asm.IMM8),
            asm.JSR(c4.multiply, asm.ABS),          # a = num addresses * category (i.e. index of tier 0 for category)
            asm.PHA(),                              # push index of tier 0 for category

            # add the enemy tier to the above category tier offset
            asm.LDA(0x3b18, asm.ABS_Y),             # a = enemy's level
            asm.CMP(int(ENEMY_LEVELS_PER_TIER * MAX_ENEMY_LEVEL_TIER), asm.IMM8),
            asm.BLT("TIER<MAX"),                    # branch if enemy tier is < max tier (no high level overflow)
            asm.LDA(MAX_ENEMY_LEVEL_TIER, asm.IMM8),# clamp enemy tier to max enemy tier
            asm.BRA("TIER_OFFSET"),

            "TIER<MAX",
            asm.ASL(),                              # a = enemy level * 2
            asm.LDX(int(ENEMY_LEVELS_PER_TIER * 2), asm.IMM8),  # doubled to allow 0.5 increments
            asm.JSR(c4.divide, asm.ABS),            # a = (enemy level * 2) / (levels per tier * 2)

            "TIER_OFFSET",
            asm.CLC(),
            asm.ADC(0xee, asm.DIR),                 # a = enemy tier + argument tier offset
            asm.STA(0xee, asm.DIR),

            asm.JSR(get_tier_distortion, asm.ABS),  # a = enemy tier + argument tier offset + random offset
            asm.CMP(ability_tiers.TIER_COUNT, asm.IMM8),
            asm.BLT("MAX_CHECKED"),                 # branch if final tier < max tier + 1
            asm.LDA(ability_tiers.TIER_COUNT - 1, asm.IMM8),    # clamp final tier to max tier

            "MAX_CHECKED",
            asm.STA(0xee, asm.DIR),                 # $ee = final tier = random offset + enemy tier + argument offset

            # find index of category's final tier in tier_table_pointers
            asm.PLA(),                              # a = index of tier 0 for category
            asm.CLC(),
            asm.ADC(0xee, asm.DIR),                 # a = final tier + index of tier 0 for category

            # find number of elements in tier and pick one of them randomly
            asm.AXY16(),
            asm.ASL(),                              # multiply tier by 2 (pointers are 2 bytes each in table)
            asm.TAX(),                              # x = tier pointer offset
            asm.LDA(tier_table_pointers + START_ADDRESS_SNES, asm.LNG_X),
            asm.STA(0xee, asm.DIR),                 # $ee = tier table pointer
            asm.INX(),
            asm.INX(),
            asm.LDA(tier_table_pointers + START_ADDRESS_SNES, asm.LNG_X),
            asm.SEC(),
            asm.SBC(0xee, asm.DIR),                 # a = (tier+1 pointer) - (tier pointer) = number abilities in tier
            asm.JSR(c4.battle_rng_a, asm.ABS),      # a = random number (0 to number abilities in tier - 1)
            asm.CLC(),
            asm.ADC(0xee, asm.DIR),                 # a = tier pointer + index of random ability in tier
            asm.TAX(),
            asm.LDA(0xc40000, asm.LNG_X),           # a = randomly chosen spell id from the tier
            asm.AXY8(),
            asm.RTL(),
        )

        get_random_tiered_special = space.next_address
        space.write(
            asm.SEC(),
            asm.SBC(SPECIAL0, asm.IMM8),            # convert argument to 0, 1, or 2
            asm.STA(0xee, asm.DIR),                 # $ee = argument tier

            asm.LDA(0x3b18, asm.ABS_Y),             # a = enemy's level
            asm.LDX(ENEMY_LEVELS_PER_SPECIAL_TIER, asm.IMM8),
            asm.JSR(c4.divide, asm.ABS),            # a = enemy's level / ENEMY_LEVELS_PER_SPECIAL_TIER
            asm.CMP(MAX_ENEMY_LEVEL_SPECIAL_TIER + 1, asm.IMM8),
            asm.BLT("TIER<MAX_SPECIAL+1"),          # branch if enemy tier is < max tier + 1
            asm.LDA(MAX_ENEMY_LEVEL_SPECIAL_TIER, asm.IMM8),    # clamp enemy tier to max enemy special tier

            "TIER<MAX_SPECIAL+1",
            asm.CLC(),
            asm.ADC(0xee, asm.DIR),                 # a = enemy tier + argument tier offset
            asm.STA(0xee, asm.DIR),

            asm.JSR(get_tier_distortion, asm.ABS),  # a = enemy tier + argument tier offset + random offset
            asm.CMP(MAX_SPECIAL_TIER + 1, asm.IMM8),# compare final tier with (max tier + 1)
            asm.BLT("MAX_SPECIAL_CHECKED"),         # branch if final tier < max tier + 1
            asm.LDA(MAX_SPECIAL_TIER, asm.IMM8),    # clamp final tier to max tier

            "MAX_SPECIAL_CHECKED",
            asm.STA(0xee, asm.DIR),                 # $ee = final tier = random offset + enemy tier + argument offset

            asm.LDA(0x33a8, asm.ABS_Y),             # a = enemy id
            asm.ASL(),
            asm.ASL(),
            asm.ASL(),
            asm.ASL(),
            asm.ASL(),                              # a = enemy id * 32 (enemy data is 32 bytes each)
            asm.TAX(),                              # x = enemy id * 32
            asm.A8(),

            asm.LDA(0xcf001f, asm.LNG_X),           # a = enemy special attack data
            asm.AND(0x0c, asm.IMM8),                # extract no damage/always hit flags
            asm.STA(0x322d, asm.ABS_Y),
            asm.LDA(0xee, asm.DIR),                 # a = tier
            asm.ADC(0x20, asm.IMM8),                # add index of effects tier 0 (convert tier to effects value)
            asm.ORA(0x322d, asm.ABS_Y),             # or tier with no damage/always hit flags
            asm.STA(0x322d, asm.ABS_Y),             # store tier + no damage/always hit flags

            asm.XY8(),
            asm.LDA(0x06, asm.IMM8),                # a = attack type (6 = special attack)
            asm.STA(0x3412, asm.ABS),               # store special attack type to show attack name at top of screen

            asm.LDA(name_id["Special"], asm.IMM8),  # a = special attack id to execute chosen/stored special
            asm.RTL(),
        )

        space = Reserve(0x2a76a, 0x2a7af, "enemy script parse 0xf0 command arguments and return ability id")
        get_ability_id = space.next_address
        space.write(
            asm.LDA(0x3a2c, asm.ABS),               # a = current enemy command
            asm.CMP(0xf0, asm.IMM8),                # compare to 0xf0 (lowest command value)
            asm.BLT("GET_ABILITY_ID"),              # branch if current command < 0xf0 (it is a single spell id)

            asm.LDA(0x03, asm.IMM8),                # a = number of arguments
            asm.JSR(0x4b65, asm.ABS),               # pick random argument index
            asm.TAX(),
            asm.LDA(0x3a2d, asm.ABS_X),             # a = random argument
            asm.CMP(0xfe, asm.IMM8),                # compare with do nothing argument
            asm.BNE("GET_ABILITY_ID"),              # branch if not do nothing

            asm.PLA(),
            asm.PLA(),                              # pull return address from stack
            asm.JMP(0x1ab4, asm.ABS),               # jump to skip executing this command and continue with ai script

            "GET_ABILITY_ID",
            asm.CMP(Spells.SPELL_COUNT, asm.IMM8),
            asm.BLT("RETURN"),                      # branch if a contains a regular spell id

            # use 0x36 to 0x50 as elemental/non-elemental flags instead of esper ids
            asm.CMP(name_id["Fire Skean"], asm.IMM8),
            asm.BLT("RANDOM_SPELL"),                # branch if a is a random elemental/non-elemental spell

            # elemental skean/edge ids are used by some scripts (and storm could be used)
            # do not use them as flags for randomization, skip them
            asm.CMP(name_id["Storm"] + 1, asm.IMM8),
            asm.BLT("RETURN"),                      # branch if a is fire skean, water edge, bolt edge, or storm

            # use 0x55 to 0x64 as cure/tek/damage/special flags instead of swdtech/blitz ids
            asm.CMP(SPECIAL0, asm.IMM8),
            asm.BLT("RANDOM_SPELL"),                # branch if a is a cure/tek/damage spell

            asm.CMP(SPECIAL2 + 1, asm.IMM8),
            asm.BLT("RANDOM_SPECIAL"),              # branch if a is a random special enemy ability

            "RETURN",
            asm.RTS(),

            "RANDOM_SPELL",
            asm.JSL(get_random_tiered_spell + START_ADDRESS_SNES),
            asm.RTS(),

            "RANDOM_SPECIAL",
            asm.JSL(get_random_tiered_special + START_ADDRESS_SNES),
            asm.RTS(),
        )

        space = Reserve(0x21b22, 0x21b24, "enemy script 0xf0, call custom get ability", asm.NOP())
        random_attack_command = space.next_address
        space.write(
            asm.JSR(get_ability_id, asm.ABS),
        )

        # vanilla spell ids branch to 0xf0 after the random one is chosen
        # instead, branch to the start of customized 0xf0 which can execute random abilities
        space = Reserve(0x21afd, 0x21afd, "enemy script spell id, call custom get ability")
        space.add_label("RANDOM ATTACK COMMAND", random_attack_command)
        space.write(
            space.label_distance("RANDOM ATTACK COMMAND") - 1,
        )

    def mod(self):
        self.hp_check_command_mod()
        self.hp_conditions_mod()

        scaling_space = Allocate(Bank.C4, 946, "enemy script get random tiered ability")
        if self.args.ability_scaling:
            self.random_tiered_ability_mod(scaling_space)
