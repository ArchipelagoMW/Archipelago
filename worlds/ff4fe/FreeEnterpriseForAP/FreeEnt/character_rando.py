import os
import pkgutil

from . import rewards
from .address import *
from .spoilers import SpoilerRow
from . import databases


_DEBUG = False

# maps slots to axtors
SLOTS = {
    'dkcecil_slot' : 0x01, 
    'kain1_slot' : 0x02, 
    'crydia_slot' : 0x03, 
    'tellah1_slot' : 0x04,
    'edward_slot' : 0x05, 
    'rosa1_slot' : 0x06, 
    'yang1_slot' : 0x07, 
    'palom_slot' : 0x08,
    'porom_slot' : 0x09, 
    'tellah2_slot' : 0x0A, 
    'yang2_slot' : 0x0D, 
    'cid_slot' : 0x0E, 
    'kain2_slot' : 0x0F, 
    'rosa2_slot' : 0x10, 
    'arydia_slot' : 0x11, 
    'edge_slot' : 0x12,
    'fusoya_slot' : 0x13, 
    'kain3_slot' : 0x14
}

DEFAULTS = {
    'dkcecil_slot' : 'cecil',
    'kain1_slot' : 'kain', 
    'crydia_slot' : 'rydia', 
    'tellah1_slot' : 'tellah',
    'edward_slot' : 'edward', 
    'rosa1_slot' : 'rosa', 
    'yang1_slot' : 'yang', 
    'palom_slot' : 'palom',
    'porom_slot' : 'porom', 
    'tellah2_slot' : 'tellah', 
    'yang2_slot' : 'yang', 
    'cid_slot' : 'cid', 
    'kain2_slot' : 'kain', 
    'rosa2_slot' : 'rosa', 
    'arydia_slot' : 'rydia', 
    'edge_slot' : 'edge',
    'fusoya_slot' : 'fusoya', 
    'kain3_slot' : 'kain'    
}

MUTUALLY_EXCLUSIVE_SLOTS = [
    ['dkcecil_slot', 'kain1_slot'],
    ['palom_slot', 'porom_slot'],
    ['kain2_slot', 'rosa2_slot']
]

# maps characters to corresponding reference actors
CHARACTERS = {
    'cecil' : 0x01, 
    'kain' : 0x02, 
    'rydia' : 0x03, 
    'tellah' : 0x04, 
    'edward' : 0x05, 
    'rosa' : 0x06, 
    'yang' : 0x07, 
    'palom' : 0x08, 
    'porom' : 0x09, 
    'cid' : 0x0E, 
    'edge' : 0x12, 
    'fusoya' : 0x13
}


STARTING_SLOTS = ['dkcecil_slot', 'kain1_slot']
FREE_SLOTS = [
    'tellah1_slot', 'edward_slot', 'palom_slot', 'porom_slot', 'tellah2_slot'
    ]
EASY_SLOTS = ['yang1_slot', 'yang2_slot']
HARD_SLOTS = [s for s in SLOTS if s not in (FREE_SLOTS + EASY_SLOTS + STARTING_SLOTS)]

PREGAME_NAMING_SPRITE_TABLE = [
    0x0E, 0x36, 0xB0, 0x38, 0x16, 0x36, 0xB1, 0x38, 0x0E, 0x3E, 0xB2, 0x38, 0x16, 0x3E, 0xB3, 0x38, 
    0x0E, 0x46, 0xB4, 0x38, 0x16, 0x46, 0xB5, 0x38, 0x0E, 0x56, 0xB6, 0x38, 0x16, 0x56, 0xB7, 0x38, 
    0x0E, 0x5E, 0xB8, 0x38, 0x16, 0x5E, 0xB9, 0x38, 0x0E, 0x66, 0xBA, 0x38, 0x16, 0x66, 0xBB, 0x38, 
    0x0E, 0x76, 0xBC, 0x38, 0x16, 0x76, 0xBD, 0x38, 0x0E, 0x7E, 0xBE, 0x38, 0x16, 0x7E, 0xBF, 0x38, 
    0x0E, 0x86, 0xC0, 0x38, 0x16, 0x86, 0xC1, 0x38, 0x0E, 0x96, 0xC2, 0x38, 0x16, 0x96, 0xC3, 0x38, 
    0x0E, 0x9E, 0xC4, 0x38, 0x16, 0x9E, 0xC5, 0x38, 0x0E, 0xA6, 0xC6, 0x38, 0x16, 0xA6, 0xC7, 0x38, 
    0x5E, 0x36, 0xC8, 0x38, 0x66, 0x36, 0xC9, 0x38, 0x5E, 0x3E, 0xCA, 0x38, 0x66, 0x3E, 0xCB, 0x38, 
    0x5E, 0x46, 0xCC, 0x38, 0x66, 0x46, 0xCD, 0x38, 0x5E, 0x56, 0xCE, 0x38, 0x66, 0x56, 0xCF, 0x38, 
    0x5E, 0x5E, 0xD0, 0x38, 0x66, 0x5E, 0xD1, 0x38, 0x5E, 0x66, 0xD2, 0x38, 0x66, 0x66, 0xD3, 0x38, 
    0x5E, 0x76, 0xD4, 0x38, 0x66, 0x76, 0xD5, 0x38, 0x5E, 0x7E, 0xD6, 0x38, 0x66, 0x7E, 0xD7, 0x38, 
    0x5E, 0x86, 0xD8, 0x38, 0x66, 0x86, 0xD9, 0x38, 0x5E, 0x96, 0xDA, 0x38, 0x66, 0x96, 0xDB, 0x38, 
    0x5E, 0x9E, 0xDC, 0x38, 0x66, 0x9E, 0xDD, 0x38, 0x5E, 0xA6, 0xDE, 0x38, 0x66, 0xA6, 0xDF, 0x38, 
    0xAE, 0x36, 0xE0, 0x38, 0xB6, 0x36, 0xE1, 0x38, 0xAE, 0x3E, 0xE2, 0x38, 0xB6, 0x3E, 0xE3, 0x38, 
    0xAE, 0x46, 0xE4, 0x38, 0xB6, 0x46, 0xE5, 0x38, 0xAE, 0x56, 0xE6, 0x38, 0xB6, 0x56, 0xE7, 0x38, 
    0xAE, 0x5E, 0xE8, 0x38, 0xB6, 0x5E, 0xE9, 0x38, 0xAE, 0x66, 0xEA, 0x38, 0xB6, 0x66, 0xEB, 0x38, 
    0xAE, 0x76, 0xEC, 0x38, 0xB6, 0x76, 0xED, 0x38, 0xAE, 0x7E, 0xEE, 0x38, 0xB6, 0x7E, 0xEF, 0x38, 
    0xAE, 0x86, 0xF0, 0x38, 0xB6, 0x86, 0xF1, 0x38, 0xAE, 0x96, 0xF2, 0x38, 0xB6, 0x96, 0xF3, 0x38, 
    0xAE, 0x9E, 0xF4, 0x38, 0xB6, 0x9E, 0xF5, 0x38, 0xAE, 0xA6, 0xF6, 0x38, 0xB6, 0xA6, 0xF7, 0x38,
]

def apply(env):
    pregame_name_characters = set(CHARACTERS)

    requested_start_characters = []
    disrequested_start_characters = []
    restricted_characters = []
    start_character = None

    for ch in CHARACTERS:
        if env.options.flags.has(f'Cstart:{ch}'):
            requested_start_characters.append(ch)
        if env.options.flags.has(f'Cstart:not_{ch}'):
            disrequested_start_characters.append(ch)
        if env.options.flags.has(f'Crestrict:{ch}'):
            restricted_characters.append(ch)
    
    if not restricted_characters:
        restricted_characters.extend(['fusoya', 'edge'])
        

    if requested_start_characters and disrequested_start_characters:
        raise Exception("Cannot specify both inclusions and exclusions for starting character pool")
    elif requested_start_characters:
        start_character = env.rnd.choice(requested_start_characters)

    assignable_slots = STARTING_SLOTS.copy()
    if not env.options.flags.has('no_earned_characters'):
        assignable_slots.extend(EASY_SLOTS + HARD_SLOTS)
    if not env.options.flags.has('no_free_characters'):
        assignable_slots.extend(FREE_SLOTS)

    if env.options.flags.has('objective_mode_classicgiant'):
        assignable_slots.remove('kain3_slot')

    env.add_substitution('randomizer character count', '{:02X}'.format(len(assignable_slots)))

    if env.options.ap_data is not None:
        assignment = {}
        for slot in SLOTS:
            id = str(SLOTS[slot] + 0x200)
            value = (env.options.ap_data[id]['item_data']['name']).lower()
            assignment[slot] = value

    elif env.options.flags.has('characters_vanilla'):
        assignment = {slot : DEFAULTS[slot] for slot in assignable_slots}
        if start_character is not None:
            assignment['dkcecil_slot'] = start_character
        elif disrequested_start_characters:
            allowed_starting_characters = sorted(set(CHARACTERS) - set(disrequested_start_characters))
            if (not allowed_starting_characters):
                raise Exception("No character can be chosen as the starting character under these flags")
            
            assignment['dkcecil_slot'] = env.rnd.choice(allowed_starting_characters)

        used_characters = set([assignment[slot] for slot in assignment if slot not in STARTING_SLOTS])
        if not set(env.meta['objective_required_characters']).issubset(used_characters):
            raise Exception("Objective required character is not present in vanilla character assignment.")
    else:
        allowed_characters = list(CHARACTERS)
        only_characters = []
        for ch in CHARACTERS:
            if env.options.flags.has(f'Conly:{ch}'):
                only_characters.append(ch)            
            if env.options.flags.has(f'Cno:{ch}'):
                allowed_characters.remove(ch)
        if only_characters:
            allowed_characters = only_characters
        if not allowed_characters:
            # fallback to all characters if user has excluded all characters
            allowed_characters = list(CHARACTERS)

        if start_character is None:
            # pick a starting character now from the allowed pool
            if env.options.flags.has('Cstart:any'):
                allowed_starting_characters = list(CHARACTERS)
            else:
                if env.options.flags.has('characters_standard'):
                    allowed_starting_characters = sorted(list(set(allowed_characters) - set(restricted_characters)))
                    if not allowed_starting_characters:
                        allowed_starting_characters = list(allowed_characters)
                else:
                    allowed_starting_characters = list(allowed_characters)

                if disrequested_start_characters:
                    allowed_starting_characters = sorted(set(allowed_starting_characters) - set(disrequested_start_characters))

            # remove objective required characters from consideration, if able
            if (set(allowed_starting_characters) - set(env.meta['objective_required_characters'])):
                allowed_starting_characters = sorted(set(allowed_starting_characters) - set(env.meta['objective_required_characters']))

            if not allowed_starting_characters:
                raise Exception("No character can be chosen as the starting character under these flags")

            start_character = env.rnd.choice(allowed_starting_characters)

        # ensure characters required by manual objectives are present
        for char in env.meta['objective_required_characters']:
            if char not in allowed_characters:
                allowed_characters.append(char)

        # remove hero from further allowance, if able
        if env.options.flags.has('hero_challenge') and start_character in allowed_characters and len(allowed_characters) > 1 and start_character not in env.meta['objective_required_characters']:
            allowed_characters.remove(start_character)

        pregame_name_characters = set(allowed_characters)

        distinct_count = env.options.flags.get_suffix('Cdistinct:')
        if distinct_count:
            distinct_count = int(distinct_count)
            distinct_characters = set()

            # count objective-required characters against distinct count
            forced_characters = sorted(list(env.meta['objective_required_characters']))
            for c in forced_characters:
                distinct_characters.add(c)

            # count starting character against distinct count
            if start_character is not None:
                distinct_characters.add(start_character)
            
            # pad character list if more distinct characters are needed
            if len(distinct_characters) < distinct_count:
                remaining_characters = [ch for ch in allowed_characters if ch not in distinct_characters]
                for c in env.rnd.sample(remaining_characters, min(len(remaining_characters), distinct_count - len(distinct_characters))):
                    distinct_characters.add(c)

            # after pool is filled, prevent reassignment of starting character if not allowed by flags
            # and not required by objectives
            if start_character is not None and start_character not in forced_characters and start_character not in allowed_characters and len(distinct_characters) > 1:
                distinct_characters.remove(start_character)

            allowed_characters = sorted(list(distinct_characters))

        # remove starting slot if start character specified, but after we've already
        # done the total available character count
        if start_character is not None:
            assignable_slots.remove('dkcecil_slot')

        num_easy_slots = len([s for s in assignable_slots if s not in HARD_SLOTS])

        def subtract_if_able(original_set, subtract_set):
            result = original_set - subtract_set
            if result:
                original_set -= subtract_set

        # create assignments until we find one that satisfies all
        # constraints, or otherwise generate a bunch and take the one
        # violating the fewest constraints
        possible_assignments = []

        for attempt in range(20):
            characters = []
            if not env.options.flags.has('characters_not_guaranteed'):
                characters.extend(allowed_characters)
                if start_character is not None and start_character in characters:
                    characters.remove(start_character)
            else:
                characters.extend(env.meta['objective_required_characters'])

            # pre-cull characters if Cnoearned is on
            if env.options.flags.has('no_earned_characters'):
                valid_restricted_characters = list(restricted_characters)
                while len(characters) > len(assignable_slots):
                    # remove restricted characters first
                    if valid_restricted_characters:
                        ch = env.rnd.choice(valid_restricted_characters)
                        if ch in characters:
                            characters.remove(ch)
                        valid_restricted_characters.remove(ch)
                    else:
                        characters.remove(env.rnd.choice(characters))

            # add characters to the pool as best as we're able
            while len(characters) < len(assignable_slots):        
                character_choices = set(allowed_characters)

                # if weighted, remove restricted characters from pool if
                # we don't have enough characters yet to fill the
                # easy slots
                if not env.options.flags.has('characters_relaxed'):
                    num_unrestricted_characters_chosen = len([ch for ch in characters if ch not in restricted_characters])
                    if num_unrestricted_characters_chosen < num_easy_slots:
                        subtract_if_able(character_choices, set(restricted_characters))

                # if no duplicates, try to ensure that there is 
                # a different starting partner character
                if env.options.flags.has('characters_no_duplicates'):
                    if start_character is None and not characters:
                        subtract_if_able(character_choices, set([start_character]))
                    elif start_character is not None and len(set(characters)) == 1:
                        subtract_if_able(character_choices, set(characters))

                characters.append(env.rnd.choice(sorted(character_choices)))

            cur_assignment = {}
            cur_assignment_score = 0.0
            if start_character is not None:
                cur_assignment['dkcecil_slot'] = start_character

            def calculate_slot_score(slot, ch):
                slot_score = 0.0
                if not env.options.flags.has('characters_relaxed') and ch in restricted_characters and slot not in HARD_SLOTS:
                    slot_score += 1.0

                if env.options.flags.has('characters_no_duplicates'):
                    for mutex_set in MUTUALLY_EXCLUSIVE_SLOTS:
                        if slot in mutex_set:
                            for other_slot in mutex_set:
                                if slot != other_slot and other_slot in cur_assignment and cur_assignment[other_slot] == ch:
                                    slot_score += 0.5
                                    break

                return slot_score

            env.rnd.shuffle(characters)
            if not env.options.flags.has('characters_relaxed'):
                characters.sort(key=lambda ch: (ch not in restricted_characters))

            for ch in characters:
                scored_slots = []
                for slot in assignable_slots:
                    if slot in cur_assignment:
                        continue
                    scored_slots.append( (calculate_slot_score(slot, ch), slot) )

                scored_slots.sort()
                eligible_slots = [pair for pair in scored_slots if pair[0] == scored_slots[0][0]]
                selected_slot = env.rnd.choice(eligible_slots)
                cur_assignment_score += selected_slot[0]
                cur_assignment[selected_slot[1]] = ch

            # reject this assignment if it violates objective requirements
            assignment_impossible = False
            for ch in env.meta['objective_required_characters']:
                character_is_findable = False
                for slot in cur_assignment:
                    if cur_assignment[slot] == ch and slot not in STARTING_SLOTS:
                        character_is_findable = True
                        break
                if not character_is_findable:
                    assignment_impossible = True

            if not assignment_impossible:
                possible_assignments.append( (cur_assignment_score, cur_assignment) )

                if cur_assignment_score == 0.0:
                    # tihs assignment violates no constraints, proceed with it
                    break

        if not possible_assignments:
            raise Exception("Unable to find a possible character assignment after max number of attempts")

        possible_assignments.sort(key=lambda ass: ass[0])
        assignment = possible_assignments[0][1]
        if _DEBUG and possible_assignments[0][0] > 0.0:
            print('***')
            print("*** could not find perfect assignment; this one has violation score {}".format(possible_assignments[0][0]))
            print('***')

    # assign defaults to unassigned slots for safety
    # (also update pregame name screen characters at same time)
    for slot in SLOTS:
        if slot not in assignment:
            assignment[slot] = None
        elif assignment[slot] not in pregame_name_characters:
            pregame_name_characters.add(assignment[slot])

    axtor_map = [0x00] * 0x20

    # build substitutions table accordingly, and set metadata objective purposes
    env.meta['available_characters'] = set()
    env.meta['available_nonstarting_characters'] = set()
    for slot in assignment:
        character = assignment[slot]
        if character is None or character == "none":
            if slot in ['crydia_slot', 'rosa1_slot', 'yang2_slot', 'rosa2_slot', 'kain2_slot']:
                axtor_map[SLOTS[slot]] = 0xFE  # placeholder piggy for required overworld NPCs
            else:
                axtor_map[SLOTS[slot]] = 0x00
        else:
            axtor_map[SLOTS[slot]] = CHARACTERS[character]

        env.meta['available_characters'].add(character)
        if slot not in ['dkcecil_slot', 'kain1_slot']:
            env.meta['available_nonstarting_characters'].add(character)

    env.add_substitution('axtor map', ' '.join([f'{b:02X}' for b in axtor_map]))

    # maximum party size
    max_party_size = env.options.flags.get_suffix('Cparty:')
    if max_party_size:
        max_party_size = int(max_party_size)
    else:
        max_party_size = 5

    env.add_binary(BusAddress(0x21F0FF), [max_party_size])

    # permadeath :S
    if env.options.flags.has('characters_permadeath'):
        env.add_file('scripts/permadeath.f4c')
    elif env.options.flags.has('characters_permadeader'):
        env.add_file('scripts/permadeath.f4c')
        env.add_file('scripts/permadeader.f4c')

    # sub in against-ally battle data
    # TODO: need more complex logic for this so it can be obfuscated
    for slot in ['crydia_slot', 'yang2_slot']:
        ch = assignment[slot]
        if ch is None or ch == "none":
            ch = 'piggy'

        monster_gfx_sprite = CHARACTER_MONSTER_GFX[ch][0]
        monster_gfx_palette = (env.rnd.randint(0x00, 0x0D)) if (ch == 'piggy') else monster_gfx_sprite
        monster_gfx = f'size $4{monster_gfx_sprite:1X} palette $0{monster_gfx_palette:1X}'
        monster_name = CHARACTER_AS_ENEMY_NAMES[ch][0]
        env.add_substitution(slot + ' monster_gfx', monster_gfx)
        env.add_substitution(slot + ' monster_name', monster_name)

        if len(CHARACTER_MONSTER_GFX[ch]) > 1:
            env.add_substitution(slot + ' monster_gfx_alt', 'size $4{0:1X} palette $0{0:1X}'.format(CHARACTER_MONSTER_GFX[ch][1]))
        else:
            env.add_substitution(slot + ' monster_gfx_alt', monster_gfx)

        if len(CHARACTER_AS_ENEMY_NAMES[ch]) > 1:
            env.add_substitution(slot + ' monster_name_alt', CHARACTER_AS_ENEMY_NAMES[ch][1])
        else:
            env.add_substitution(slot + ' monster_name_alt', monster_name)

        if ch in CHARACTER_ALT_FLAGS:
            env.add_substitution(slot + ' monster_alt_check', '[#B #If #Flag {}]'.format(CHARACTER_ALT_FLAGS[ch]))
        else:
            env.add_substitution(slot + ' monster_alt_check', '[#B #If #False 0]')

    # do fashion here too for convenience
    if not env.options.flags.has('vanilla_fashion'):
        fashion_filename = ('fashion_vintage.bin' if env.options.flags.has('vintage') else 'fashion.bin')
        env.add_binary(UnheaderedAddress(0x140000), pkgutil.get_data(__name__, f"assets/fashion/{fashion_filename}"))
        env.add_file('scripts/fashion.f4c')

        NUM_PALETTES = 13
        available_palettes = {c : list(range(NUM_PALETTES)) for c in CHARACTERS}
        resolve_order = list(SLOTS)
        env.rnd.shuffle(resolve_order)
        fashion_codes = [0] * 0x20
        for slot in resolve_order:
            character = assignment[slot]
            if character is None or character == "none":
                continue

            code = env.rnd.choice(available_palettes[character])
            fashion_codes[SLOTS[slot]] = code
            available_palettes[character].remove(code)
            if not available_palettes[character]:
                available_palettes[character] = list(range(NUM_PALETTES))

        env.add_binary(BusAddress(0x21f770), fashion_codes, as_script=True)
    else:
        # write null fashion table
        env.add_binary(BusAddress(0x21f770), [0x00] * 0x20, as_script=True)

    # create distinguisher tag codes for naming
    distinguisher_tiles = list(range(0x42, 0x5C)) + list(range(0x80, 0x8A)) # start with A-Z+0-9
    distinguisher_tiles.remove(0x43) # remove B (ambiguous with 8)
    distinguisher_tiles.remove(0x48) # remove G (ambiguous with 6)
    distinguisher_tiles.remove(0x4A) # remove I (ambiguous with 1)
    distinguisher_tiles.remove(0x50) # remove O (ambiguous with 0)

    env.rnd.shuffle(distinguisher_tiles)
    env.add_substitution('name distinguishers', ' '.join([f'{b:02X}' for b in distinguisher_tiles]))

    SILLY_NAME_CHAR_LISTS = {
        'SillyNames__ConsonantsUpper': [ 0x21d810, "BCDFGHJKLMNPQRSTVWXZ" ],
        'SillyNames__ConsonantsLower': [ 0x21d830, "bcdfgklmnprstvxz" ],
        'SillyNames__VowelsUpper':     [ 0x21d850, "AEIOU" ],
        'SillyNames__VowelsLower':     [ 0x21d858, "aeiouy" ],
        'SillyNames__Digits':          [ 0x21d860, "0123456789" ],
        'SillyNames__Punctuation':     [ 0x21d870, "!?%/:'.-_" ],
    }

    for k in SILLY_NAME_CHAR_LISTS:
        addr, src_chars = SILLY_NAME_CHAR_LISTS[k]
        chars = list(src_chars)
        env.rnd.shuffle(chars)
        chars = ''.join(chars)
        env.add_scripts(
            f'patch(${addr:X} bus) {{ {len(chars):02X} }}',
            f'text(${addr+1:X} bus) {{{chars}}}'
            )

    # alter the sprites table on pregame name screen to exclude known excluded chars
    pregame_sprites = list(PREGAME_NAMING_SPRITE_TABLE)
    for ch_id,ch in enumerate(CHARACTERS):
        if ch not in pregame_name_characters and not env.options.hide_flags:
            sprite_start = ch_id * 6 * 4
            sprite_count = 6
            pregame_sprites[sprite_start:sprite_start + (sprite_count * 4)] = [0xFF, 0xFF, 0x00, 0x00] * sprite_count

    env.add_binary(BusAddress(0x21d880), bytes(pregame_sprites))

    env.update_assignments(assignment)

    # generate character assignment spoilers
    CHARACTER_SLOT_SPOILER_NAMES = {
        s : rewards.REWARD_SLOT_SPOILER_NAMES[rewards.RewardSlot(SLOTS[s])] 
        for s in SLOTS
        }
    character_spoilers = []
    character_spoilers_public = env.options.flags.has_any('-spoil:all', '-spoil:chars')
    for slot in SLOTS:
        if slot in assignment and assignment[slot]:
            char = assignment[slot]
            char = char[0].upper() + char[1:]
        else:
            char = "(not present)"
        character_spoilers.append( SpoilerRow(CHARACTER_SLOT_SPOILER_NAMES[slot], char, obscurable=True) )
    env.spoilers.add_table("CHARACTERS", character_spoilers, public=character_spoilers_public)

    # set starting gear, if needed
    if env.options.flags.has('characters_nekkie'):
        starting_weapon_spoilers = []
        weapons_dbview = databases.get_items_dbview().get_refined_view(lambda it: it.category == 'weapon' and it.subtype != 'arrow' and it.tier in (1,2,3))
        arrows_dbview = databases.get_items_dbview().get_refined_view(lambda it: it.category == 'weapon' and it.subtype == 'arrow' and it.tier in (1,2,3))
        for reference_actor_id in REFERENCE_ACTORS_TO_EQUIP_JOBS:
            job = REFERENCE_ACTORS_TO_EQUIP_JOBS[reference_actor_id]
            weapons = weapons_dbview.find_all(lambda it: job in it.equip)
            weapon = env.rnd.choice(weapons)
            if weapon.subtype == 'bow':
                arrow = env.rnd.choice(arrows_dbview.find_all())
                starting_weapon_spoilers.append(SpoilerRow(REFERENCE_ACTORS_TO_SPOILER_NAMES[reference_actor_id], databases.get_item_spoiler_name(weapon) + ' + ' + databases.get_item_spoiler_name(arrow), obscurable=True))
                main_hand_value = arrow.const + (' 1' if env.meta.get('wacky_challenge') == 'unstackable' else ' 20')
                off_hand_value = weapon.const
            else:
                main_hand_value = weapon.const
                off_hand_value = '$00 0'
                starting_weapon_spoilers.append(SpoilerRow(REFERENCE_ACTORS_TO_SPOILER_NAMES[reference_actor_id], databases.get_item_spoiler_name(weapon), obscurable=True))
            
            if (job in ['kain', 'palom']):
                main_hand = 'left hand'
                off_hand = 'right hand'
            else:
                main_hand = 'right hand'
                off_hand = 'left hand'

            gear_script = (f'actor(${reference_actor_id:02X}) {{\n' +
                f'{ main_hand } { main_hand_value }\n' +
                f'{ off_hand } { off_hand_value }\n' +
                f'head $00\n' +
                f'body $00\n' +
                f'arms $00\n' +
                '}')

            env.add_script(gear_script)

        env.spoilers.add_table('CHARACTER STARTING WEAPONS', starting_weapon_spoilers, ditto_depth=1, public=character_spoilers_public)

    # note starting character in metadata
    env.meta['starting_character'] = assignment['dkcecil_slot']

    # apply extra scripts for hero challenge
    if env.options.flags.has('hero_challenge'):
        env.add_file('scripts/hero_exp.f4c')



CHARACTER_AS_ENEMY_NAMES = {
    'cecil'  : ['D.Knight', 'Paladin'],
    'kain'   : ['Dragoon'],
    'rydia'  : ['Girl', 'Caller'],
    'tellah' : ['Sage'],
    'edward' : ['Bard'],
    'rosa'   : ['W.Wizard'],
    'yang'   : ['Karate'],
    'palom'  : ['B.Wizard'],
    'porom'  : ['W.Wizard'],
    'cid'    : ['Engineer'],
    'edge'   : ['Ninja'],
    'fusoya' : ['Mop'],
    'piggy'  : ['Pig']
}

CHARACTER_MONSTER_GFX = {
    'cecil'  : [0x00, 0x09],
    'kain'   : [0x01],
    'rydia'  : [0x02, 0x0B],
    'tellah' : [0x03],
    'edward' : [0x04],
    'rosa'   : [0x05],
    'yang'   : [0x06],
    'palom'  : [0x07],
    'porom'  : [0x08],
    'cid'    : [0x0A],
    'edge'   : [0x0C],
    'fusoya' : [0x0D],
    'piggy'  : [0x0E]
}

CHARACTER_ALT_FLAGS = {
    'cecil' : '#flag.CecilBecamePaladin',
    'rydia' : '#flag.RydiaRejoined'
}

REFERENCE_ACTORS_TO_EQUIP_JOBS = {
    0x01 : 'dkcecil',
    0x02 : 'kain',
    0x03 : 'crydia',
    0x04 : 'tellah',
    0x05 : 'edward',
    0x06 : 'rosa',
    0x07 : 'yang',
    0x08 : 'palom',
    0x09 : 'porom',
    0x0B : 'pcecil',
    0x0E : 'cid',
    0x11 : 'arydia',
    0x12 : 'edge',
    0x13 : 'fusoya',
}

REFERENCE_ACTORS_TO_SPOILER_NAMES = {
    0x01 : 'Cecil (dark knight)',
    0x02 : 'Kain',
    0x03 : 'Rydia (child)',
    0x04 : 'Tellah',
    0x05 : 'Edward',
    0x06 : 'Rosa',
    0x07 : 'Yang',
    0x08 : 'Palom',
    0x09 : 'Porom',
    0x0B : 'Cecil (paladin)',
    0x0E : 'Cid',
    0x11 : 'Rydia (adult)',
    0x12 : 'Edge',
    0x13 : 'FuSoYa',
}



if __name__ == '__main__':
    import FreeEnt
    import random
    import argparse

    _DEBUG = True

    parser = argparse.ArgumentParser();
    parser.add_argument('flags', nargs='?')
    args = parser.parse_args();

    options = FreeEnt.FreeEntOptions()
    options.flags.load(args.flags if args.flags else 'C')

    rnd = random.Random()
    env = FreeEnt.Environment(options)

    result = randomize(env)
    subs = result['assignments']

    print()
    print('ASSIGNMENTS:')
    width = max([len(k) for k in subs])
    for k in SLOTS:
        if k in subs:
            print(f'{k:{width}} <- {subs[k]}')

    print()
    print('CHARACTER COUNTS:')
    for ch in CHARACTERS:
        char_count = len([k for k in subs if subs[k] == ch])
        print(f'{ch:6} : {char_count}')
