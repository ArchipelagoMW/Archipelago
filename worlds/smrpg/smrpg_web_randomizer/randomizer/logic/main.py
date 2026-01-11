# Main randomizer logic module that the front end calls.

import collections
import hashlib
import random
import re
import binascii


from ...randomizer import data
from . import bosses
from . import bosses_overworld
from . import credits
from . import characters
from . import chests
from . import dialogs
from . import doors
from . import enemies
from . import flags
from . import games
from . import items
from . import keys
from . import map
from . import spells
from . import utils
from .patch import Patch
from .battleassembler import assemble_battle_scripts

# Current version number
VERSION = '8.2.10'


class Settings:
    def __init__(self, mode, debug_mode=False, flag_string=''):
        """Provide either form data fields or flag string to set flags on creation.

        Args:
            mode (str): Should be standard or open.
            debug_mode (bool): Debug flag.
            flag_string (str): Flag string if parsing flags from string.
        """
        self._mode = mode
        self._debug_mode = debug_mode
        self._enabled_flags = set()

        # If flag string provided, make fake form data based on it to parse.
        flag_data = {}
        for flag in flag_string.strip().split():
            if flag.startswith('-'):
                # Solo flag that begins with a dash.
                flag_data[flag] = True
            elif flag:
                # Flag that may have a subsection of choices and/or options.
                if flag[0] not in flag_data:
                    flag_data[flag[0]] = []
                flag_data[flag[0]] += [c for c in flag[1:]]

        # Get flags from form data.
        for category in flags.CATEGORIES:
            for flag in category.flags:
                self._check_flag_from_form_data(flag, flag_data)

        # Sanity check.
        if debug_mode:
            provided_parts = set(flag_string.strip().split())
            parsed_parts = set(self.flag_string.split())
            if provided_parts != parsed_parts:
                raise ValueError("Generated flags {!r} don't match provided {!r} - difference: {!r}".format(
                    parsed_parts, provided_parts, provided_parts - parsed_parts))

    def _check_flag_from_form_data(self, flag, flag_data):
        """

        Args:
            flag (randomizer.logic.flags.Flag): Flag to check if enabled.
            flag_data (dict): Form data dictionary.

        """
        if flag.available_in_mode(self.mode):
            if flag.value.startswith('-'):
                # Solo flag that begins with a dash.
                if flag_data.get(flag.value):
                    self._enabled_flags.add(flag)
            else:
                # Flag that may be on its own with choices and/or suboptions.
                if flag.value.startswith('@'):
                    if flag.value[1] in flag_data:
                        self._enabled_flags.add(flag)
                else:
                    char = flag.value[0]
                    rest = flag.value[1:]

                    # Single character flag, just check if it's enabled.  Otherwise, make sure the small char is there.
                    if rest:
                        if rest in flag_data.get(char, []):
                            self._enabled_flags.add(flag)
                    elif char in flag_data:
                        self._enabled_flags.add(flag)

            # If flag was enabled, check choices/options recursively.
            if self.is_flag_enabled(flag):
                for choice in flag.choices:
                    self._check_flag_from_form_data(choice, flag_data)
                for option in flag.options:
                    self._check_flag_from_form_data(option, flag_data)

    @property
    def mode(self):
        """:rtype: str"""
        return self._mode

    @property
    def debug_mode(self):
        """:rtype: bool"""
        return self._debug_mode

    def _build_flag_string_part(self, flag, flag_strings):
        """

        Args:
            flag (randomizer.logic.flags.Flag): Flag to process.
            flag_strings (dict): Dictionary for flag strings.

        Returns:
            str: Flag string piece for this flag.

        """
        if self.is_flag_enabled(flag):
            # Solo flag that begins with a dash.
            if flag.value.startswith('-'):
                flag_strings[flag.value] = True
            # Flag that may have a subsection of choices and/or options.
            else:
                rest = ''
                if flag.value.startswith('@'):
                    char = flag.value[1]
                    flag_strings['@'].append(char)
                else:
                    char = flag.value[0]
                    rest = flag.value[1:]

                # Check if this key is in the map yet.
                if char not in flag_strings:
                    flag_strings[char] = []
                if rest:
                    flag_strings[char].append(rest)

                for choice in flag.choices:
                    self._build_flag_string_part(choice, flag_strings)

                for option in flag.options:
                    self._build_flag_string_part(option, flag_strings)

    @property
    def flag_string(self):
        """
        Returns:
            str: Computed flag string for these settings.
        """
        flag_strings = collections.OrderedDict()
        flag_strings['@'] = []

        for category in flags.CATEGORIES:
            for flag in category.flags:
                self._build_flag_string_part(flag, flag_strings)

        flag_string = ''
        for key, vals in flag_strings.items():
            if key != '@':
                if key.startswith('-'):
                    flag_string += key + ' '
                elif vals or key not in flag_strings['@']:
                    flag_string += key + ''.join(vals) + ' '

        return flag_string.strip()

    def is_flag_enabled(self, flag):
        """
        Args:
            flag: Flag class to check.

        Returns:
            bool: True if flag is enabled, False otherwise.
        """
        return flag in self._enabled_flags

    def get_flag_choice(self, flag):
        """
        Args:
            flag: Flag class to get choice for.

        Returns:
            randomizer.logic.flags.Flag: Selected choice for this flag.
        """
        for choice in flag.choices:
            if self.is_flag_enabled(choice):
                return choice
        return None


class GameWorld:
    """Master container class representing the entire game world to be randomized.  This class doesn't do much on its
    own, but it holds all the data being randomized so the actual logic can look at and change different things across
    a single instance of the world.
    """

    def __init__(self, seed, settings):
        """
        :type seed: int
        :type settings: randomizer.logic.main.Settings
        """
        self.seed = seed
        self.settings = settings
        self.file_select_character = 'Mario'
        self.file_select_hash = 'MARIO1 / MARIO2 / MARIO3 / MARIO4'
        self._rebuild_hash()

        # Bundt palette swap flag.
        self.chocolate_cake = False

        # *** Get vanilla data for randomizing.
        # Characters
        self.characters = data.characters.get_default_characters(self)
        self.character_join_order = self.characters[:]
        self.meta_join_order = self.character_join_order.copy()
        self.levelup_xps = data.characters.LevelUpExps()

        # Spells
        self.spells = data.spells.get_default_spells(self)
        self.spells_dict = dict([(s.index, s) for s in self.spells])

        # Starting FP.
        self.starting_fp = data.spells.STARTING_FP

        # Items
        self.items = data.items.get_default_items(self)
        self.items_dict = dict([(i.index, i) for i in self.items])

        # Shops
        self.shops = data.items.get_default_shops(self)

        # Enemies
        self.enemies = data.enemies.get_default_enemies(self)
        self.enemies_dict = dict([(e.index, e) for e in self.enemies])

        # Get enemy attack data.
        self.enemy_attacks = data.attacks.get_default_enemy_attacks(self)

        # Get enemy formation data.
        self.enemy_formations, self.formation_packs = data.formations.get_default_enemy_formations(self)
        self.enemy_formations_dict = dict((f.index, f) for f in self.enemy_formations)
        self.formation_packs_dict = dict((p.index, p) for p in self.formation_packs)

        # Get item location data.
        self.key_locations = data.keys.get_default_key_item_locations(self)
        self.chest_locations = data.chests.get_default_chests(self)

        # Get boss location data.
        self.boss_locations = data.bosses.get_default_boss_locations(self)

        # Minigame data.
        self.ball_solitaire = data.games.BallSolitaireGame(self)
        self.magic_buttons = data.games.MagicButtonsGame(self)

        # String data.
        self.wishes = data.dialogs.Wishes(self)
        self.quiz = data.dialogs.Quiz(self)

    @property
    def open_mode(self):
        """Check if this game world is Open mode.

        Returns:
            bool:

        """
        return self.settings.mode == 'open'

    @property
    def debug_mode(self):
        """Get debug mode flag.

        Returns:
            bool:

        """
        return self.settings.debug_mode

    def get_item_instance(self, cls):
        """
        Args:
            cls: Item class to get this world's instance of.

        Returns:
            randomizer.data.items.Item: Item instance for this world.
        """
        return self.items_dict[cls.index]

    def get_enemy_instance(self, cls):
        """
        Args:
            cls: Enemy class to get this world's instance of.

        Returns:
            randomizer.data.enemies.Enemy: Enemy instance for this world.
        """
        return self.enemies_dict[cls.index]

    def get_enemy_formation_by_index(self, index):
        """
        :type index: int
        :rtype: randomizer.data.formations.EnemyFormation
        """
        return self.enemy_formations_dict[index]

    def get_formation_pack_by_index(self, index):
        """
        :type index: int
        :rtype: randomizer.data.formations.FormationPack
        """
        return self.formation_packs_dict[index]

    def randomize(self, ap_data):
        """Randomize this entire game world instance."""
        # Seed the PRNG at the start.
        random.seed(self.seed)

        characters.randomize_all(self)
        spells.randomize_all(self)
        items.randomize_all(self, ap_data)
        enemies.randomize_all(self)
        bosses.randomize_all(self, ap_data)
        keys.randomize_all(self, ap_data)
        chests.randomize_all(self, ap_data)
        games.randomize_all(self)
        dialogs.randomize_all(self)

        # Rebuild hash after randomization.
        self._rebuild_hash()

    def _rebuild_hash(self):
        """Build hash value for choosing file select character and file name hash.
        Use the same version, seed, mode, and flags used for the database hash.
        """
        final_seed = bytearray()
        final_seed += VERSION.encode('utf-8')
        final_seed += self.seed.to_bytes(4, 'big')
        final_seed += self.settings.mode.encode('utf-8')
        final_seed += self.settings.flag_string.encode('utf-8')
        self.hash = hashlib.md5(final_seed).hexdigest()

    def build_patch(self):
        """Build patch data for this instance.

        :rtype: randomizer.logic.patch.Patch
        """
        patch = Patch()

        # Characters
        for character in self.characters:
            patch += character.get_patch()

        # Update party join script events for the final order.  These are different for standard vs open mode.
        if self.open_mode:
            # Add characters to Mushroom Way and Moleville when NFC is turned on
            if self.settings.is_flag_enabled(flags.NoFreeCharacters):
                addresses = [0x1ef86c, 0x1ffd82, 0x1fc4f1, 0x1e6d58, 0x1e8b71]
            else:
                addresses = [0x1ef86c, 0x1ef86e, 0x1ef870, 0x1fc4f1, 0x1e8b71]
            dialogue_iterator = 0
            for addr, character in zip(addresses, self.meta_join_order):
                dialogue_iterator += 1
                # Character joins and dialogues are 0x9B by default, replaced with this code when populated
                if character is not None:
                    # Write message stating who joined
                    if character.palette is not None and character.palette.rename_character:
                        message = '"' + character.palette.name + '" (' + character.original_name + ') joins!'
                    else:
                        message = character.original_name + " joins!"
                    messagestring = binascii.hexlify(bytes(message, encoding='ascii'))
                    messagebytes = [int(messagestring[i:i + 2], 16) for i in range(0, len(messagestring), 2)]
                    messagebytes.append(0x00)
                    # Append character join event and corresponding message to code
                    if self.settings.is_flag_enabled(flags.NoFreeCharacters):
                        if dialogue_iterator == 2:
                            patch.add_data(0x242c52, messagebytes)
                            patch.add_data(0x1ffd84, [0x60, 0xac, 0xac, 0x00])
                        if dialogue_iterator == 3:
                            patch.add_data(0x221475, messagebytes)
                            patch.add_data(0x1fc8dd, [0x60, 0x48, 0xa2, 0x00])
                            # show character walking around forest maze
                        if dialogue_iterator == 4:
                            patch.add_data(0x242238, messagebytes)
                            patch.add_data(0x1e6d5a, [0x60, 0x89, 0xac, 0x00])
                        if dialogue_iterator == 5:
                            patch.add_data(0x23abf2, messagebytes)
                            patch.add_data(0x1e8b49, [0x60, 0xff, 0xaa, 0x00])
                    else:
                        if dialogue_iterator == 4:
                            patch.add_data(0x242c52, messagebytes)
                            patch.add_data(0x1fc8dd, [0x60, 0xac, 0xac, 0x00])
                        if dialogue_iterator == 5:
                            patch.add_data(0x221475, messagebytes)
                            patch.add_data(0x1e8b49, [0x60, 0x48, 0xa2, 0x00])
                    patch.add_data(addr, [0x36, 0x80 + character.index])
            dialogue_iterator = 0
            for character in self.character_join_order:
                dialogue_iterator += 1
                # replace overworld characters in recruitment spots - there are no partitions identical to 89 that have
                # CBC set to 3 instead of 4, so modify 89 since it's only used by this room

                if self.settings.is_flag_enabled(flags.NoFreeCharacters) and dialogue_iterator == 2:
                    # mushroom way
                    patch.add_data(0x14b3BC, character.mway_1_npc_id)
                    patch.add_data(0x14b411, character.mway_2_npc_id)
                    patch.add_data(0x14b452, character.mway_3_npc_id)
                    # change partition to accommodate mallow's sprite in mway
                    if character.name == "Mallow":
                        patch.add_data(0x1ddf67, 0x80)
                if ((dialogue_iterator == 4 and not self.settings.is_flag_enabled(flags.NoFreeCharacters)) or
                        (self.settings.is_flag_enabled(flags.NoFreeCharacters) and dialogue_iterator == 3)):
                    # forest maze
                    patch.add_data(0x14b8eb, character.forest_maze_sprite_id)
                    if character.name == "Mario":
                        patch.add_data(0x215e4f, 0x42)
                        patch.add_data(0x215e56, 0x12)
                if self.settings.is_flag_enabled(flags.NoFreeCharacters) and dialogue_iterator == 4:
                    # moleville
                    patch.add_data(0x14c491, character.moleville_sprite_id)
                    if character.name in ["Mario", "Peach", "Geno"]:
                        # patch moleville minecart room partition
                        patch.add_data(0x1DDF45, 0x81)
                        if character.name == "Mario":
                            patch.add_data(0x1DB801, 0x00)
                    # make cutscene look less weird
                    if character.name != "Bowser":
                        patch.add_data(0x201F04, [0x3D, 0x02, 0x63])
                        if character.name == "Mario":
                            patch.add_data(0x201F07, 0x09)
                        elif character.name == "Peach":
                            patch.add_data(0x201F07, 0x0F)
                        elif character.name == "Mallow":
                            patch.add_data(0x201F07, 0x0E)
                        else:
                            patch.add_data(0x201F07, 0x0C)
                    patch.add_data(0x201F5B, 0x00)
                if dialogue_iterator == 5:
                    # show character in marrymore
                    patch.add_data(0x14a94d, character.forest_maze_sprite_id)
                    patch.add_data(0x148f91, character.forest_maze_sprite_id)
                    # fix booster hill solidity
                    if character.name == "Mallow":
                        patch.add_data(0x1DB819, [0x56, 0x2C])
                    elif character.name == "Geno":
                        patch.add_data(0x1DB820, 0x56)
                    elif character.name == "Mario":
                        patch.add_data(0x1DB804, 0x56)
                    elif character.name == "Peach":
                        patch.add_data(0x1DB80B, 0x56)
                    if character.name != "Peach":
                        # marrymore sequence
                        if character.name == "Mario":
                            # surprised
                            patch.add_data(0x20d338, [0x08, 0x43, 0x00])
                            # on ground
                            patch.add_data(0x20d34e, [0x08, 0x4B, 0x01])
                            # sitting
                            patch.add_data(0x20d43b, [0x08, 0x4a, 0x1f])
                            # looking down
                            patch.add_data(0x20d445, [0x08, 0x48, 0x06])
                            patch.add_data(0x20d459, [0x08, 0x48, 0x06])
                            # crying
                            patch.add_data(0x20d464, [0x10, 0x80])
                            patch.add_data(0x20d466, [0x08, 0x43, 0x03])
                            # surprised
                            patch.add_data(0x20d48c, [0x08, 0x43, 0x00])
                            # looking down
                            patch.add_data(0x20d4d4, [0x08, 0x48, 0x06])
                            # crying
                            patch.add_data(0x20d4d9, [0x10, 0x80])
                            patch.add_data(0x20d4db, [0x08, 0x43, 0x03])
                            # surprised reversed
                            patch.add_data(0x20d5d8, [0x08, 0x43, 0x80])
                            # crying in other direction
                            patch.add_data(0x20d5e3, [0x08, 0x43, 0x84])
                            # booster hill
                            patch.add_data(0x207147, [0x08, 0x43, 0x89])
                            patch.add_data(0x20714E, [0x08, 0x43, 0x09])
                            patch.add_data(0x207160, [0x08, 0x43, 0x89])
                            patch.add_data(0x207165, [0x08, 0x43, 0x88])
                            patch.add_data(0x206b1a, [0x08, 0x43, 0x88])
                            patch.add_data(0x206d19, [0x08, 0x43, 0x89])
                            patch.add_data(0x206d20, [0x08, 0x43, 0x09])
                            patch.add_data(0x206d34, [0x08, 0x43, 0x89])
                            patch.add_data(0x206d39, [0x08, 0x43, 0x88])
                        else:
                            # surprised
                            patch.add_data(0x20d338, [0x08, 0x42, 0x00])
                            patch.add_data(0x20d48c, [0x08, 0x42, 0x00])
                            # surprised reversed
                            patch.add_data(0x20d5d8, [0x08, 0x42, 0x80])
                            # sitting
                            patch.add_data(0x20d43b, [0x08, 0x49, 0x1f])
                            #booster hill
                            patch.add_data(0x207147, [0x08, 0x42, 0x09])
                            patch.add_data(0x20714E, [0x08, 0x42, 0x89])
                            patch.add_data(0x207160, [0x08, 0x42, 0x09])
                            patch.add_data(0x207165, [0x08, 0x42, 0x88])
                            patch.add_data(0x206b1a, [0x08, 0x42, 0x88])
                            patch.add_data(0x206d19, [0x08, 0x42, 0x09])
                            patch.add_data(0x206d20, [0x08, 0x42, 0x89])
                            patch.add_data(0x206d34, [0x08, 0x42, 0x09])
                            patch.add_data(0x206d39, [0x08, 0x42, 0x88])
                            patch.add_data(0x206F40, [0x08, 0x42, 0x09])
                            if character.name == "Geno":
                                # crying
                                patch.add_data(0x20d464, [0x10, 0x80])
                                patch.add_data(0x20d466, [0x08, 0x40, 0x0B])
                                # surprised
                                patch.add_data(0x20d48c, [0x08, 0x42, 0x00])
                                # looking down
                                patch.add_data(0x20d4d4, [0x08, 0x48, 0x06])
                                # crying
                                patch.add_data(0x20d4d9, [0x10, 0x80])
                                patch.add_data(0x20d4db, [0x08, 0x40, 0x0B])
                                # surprised reversed
                                patch.add_data(0x20d5d8, [0x08, 0x42, 0x80])
                                # crying in other direction
                                patch.add_data(0x20d5e3, [0x08, 0x40, 0x8C])
                            else:
                                # surprised
                                patch.add_data(0x20d338, [0x08, 0x42, 0x00])
                                patch.add_data(0x20d48c, [0x08, 0x42, 0x00])
                                # surprised reversed
                                patch.add_data(0x20d5d8, [0x08, 0x42, 0x80])
                                # sitting
                                patch.add_data(0x20d43b, [0x08, 0x49, 0x1f])

        else:
            # For standard mode, Mario is the first character.  Update the other four only.
            addresses = [0x1e2155, 0x1fc506, 0x1edf98, 0x1e8b79]
            for addr, character in zip(addresses, self.character_join_order[1:]):
                patch.add_data(addr, 0x80 + character.index)

            # Update other battle scripts so Belome eats the first one to join.
            for addr in (
                    0x394b4d,
                    0x394b70,
                    0x394b74,
                    0x394b7d,
                    0x394b7f,
                    0x394b83,
                    0x3ab93f,
                    0x3ab95a,
            ):
                patch.add_data(addr, self.character_join_order[1].index)

        # Use first character to join as file select cursor.
        cursor_id = 0
        for character in self.character_join_order:
            if character is not None:
                cursor_id = character.index
                break

        # Learned spells and level-up exp.
        patch += self.levelup_xps.get_patch()

        # Spells
        for spell in self.spells:
            patch += spell.get_patch()

        #These spells are ignored when returning world.spells, so i'm applying the patch here to fix animation lag when randomized spells is turned on
        if self.settings.is_flag_enabled(flags.EnemySpells):
            patch.add_data(0x351415, [0x0a, 0x0a, 0x0a])
            patch.add_data(0x35142d, 0x0a)
            patch.add_data(0x35142f, [0x0a, 0x0a, 0x0a])
            patch.add_data(0x351449, 0x0a)
            patch.add_data(0x35144b, [0x0a, 0x0a, 0x0a])
            patch.add_data(0x351465, 0x0a)
            patch.add_data(0x351467, [0x0a, 0x0a, 0x0a])
            patch.add_data(0x351481, 0x0a)

        # Starting FP (twice for starting/max FP)
        patch.add_data(0x3a00dd, utils.ByteField(self.starting_fp).as_bytes() * 2)

        # For debug mode, start with 9999 coins and 99 frog coins.
        if self.debug_mode or self.settings.is_flag_enabled(flags.FreeShops):
            patch.add_data(0x3a00db, utils.ByteField(9999, num_bytes=2).as_bytes())
            patch.add_data(0x3a00df, utils.ByteField(99, num_bytes=2).as_bytes())

        # No Mack Skip flag
        if self.settings.is_flag_enabled(flags.NoMackSkip):
            patch.add_data(0x14ca6c, bytes([0xA5]))

        # Items
        for item in self.items:
            patch += item.get_patch()
        patch += data.items.Item.build_descriptions_patch(self)

        # Shops
        for shop in self.shops:
            patch += shop.get_patch()

        # Enemies
        for enemy in self.enemies:
            patch += enemy.get_patch()
            enemy.patch_script()
        patch += data.enemies.Enemy.build_psychopath_patch(self)

        # Enemy attacks
        for attack in self.enemy_attacks:
            patch += attack.get_patch()

        # Enemy formations
        for formation in self.enemy_formations:
            patch += formation.get_patch()

        # Open mode specific data.
        if self.open_mode:
            # Item locations.
            # FIXME
            # for location in self.key_locations + self.chest_locations:
            #     print(">>>>>>>> {}".format(location))

            for location in self.key_locations:
                patch += location.get_patch()

            for location in self.chest_locations:
                patch += location.get_patch()

            # Boss locations.
            for boss in self.boss_locations:
                # FIXME
                # print(">>>>>>>>>>>>>>>> {}".format(boss))
                patch += boss.get_patch()

            # Set flags for seven star mode and Bowser's Keep.
            if self.settings.is_flag_enabled(flags.SevenStarHunt):
                patch.add_data(0x1fd341, utils.ByteField(0xa2).as_bytes())

            if self.settings.is_flag_enabled(flags.BowsersKeepOpen):
                patch.add_data(0x1fd343, utils.ByteField(0xa2).as_bytes())

            # If star piece exp progression is on, set exp values for each star piece number and enable flag.
            choice = self.settings.get_flag_choice(flags.StarExpChallenge)
            if choice:
                if choice is flags.StarExp1:
                    exps = (2, 4, 5, 6, 8, 9, 11)
                elif choice is flags.StarExp2:
                    exps = (1, 2, 3, 5, 6, 7, 11)
                elif choice is flags.StarExp3:
                    exps = (0, 0, 0, 0, 0, 0, 0)
                else:
                    raise ValueError("Got unrecognized value for star exp challenge: {!r}".format(choice))

                patch.add_data(0x39bc44, utils.ByteField(exps[0]).as_bytes())  # 0 stars
                patch.add_data(0x39bc46, utils.ByteField(exps[1]).as_bytes())  # 1 star
                patch.add_data(0x39bc48, utils.ByteField(exps[2]).as_bytes())  # 2 stars
                patch.add_data(0x39bc4a, utils.ByteField(exps[3]).as_bytes())  # 3 stars
                patch.add_data(0x39bc4c, utils.ByteField(exps[4]).as_bytes())  # 4 stars
                patch.add_data(0x39bc4e, utils.ByteField(exps[5]).as_bytes())  # 5 stars
                patch.add_data(0x39bc52, utils.ByteField(exps[6]).as_bytes())  # 6/7 stars
                patch.add_data(0x1fd32d, utils.ByteField(0xa0).as_bytes())  # Enable flag

            # Minigames
            patch += self.ball_solitaire.get_patch()
            patch += self.magic_buttons.get_patch()

            # Dialogs
            patch += self.wishes.get_patch()
            patch += self.quiz.get_patch()

            # FIXME
            # print(">>>>>>>> WISHES")
            # for wish in self.wishes.wishes:
            #     print(">>>>>>>>>>>>>>>> {}".format(wish))

            # print(">>>>>>>> QUIZ")
            # for question in self.quiz.questions:
            #     print(">>>>>>>>>>>>>>>> {}".format(question))

        # Unlock the whole map if in debug mode in standard.
        if self.debug_mode and not self.open_mode:
            patch += map.unlock_world_map()

        # Bowser's Keep doors
        patch += doors.patch_bowser_doors(self)

        # factory warp
        if self.settings.is_flag_enabled(flags.CasinoWarp):
            # patch the event jump
            # event 2637

            # star piece event check
            # sometimes lazy shell can cause some weirdness with addresses, but we know this event began at 0x1FF451
            # and our custom code should start +3 after that

            # if R7 is turned on, we want this to be a check for 7 star pieces, not 6

            if self.settings.is_flag_enabled(flags.SevenStarHunt):
                patch.add_data(0x1FF454, [0xE0, 0x35, 0x07, 0x5C, 0xF4])
            else:
                patch.add_data(0x1FF454, [0xE0, 0x35, 0x06, 0x5C, 0xF4])

            patch.add_data(0x1FF459, [0xD2, 0x67, 0xF4, 0xD0, 0x48, 0x08])

            original_event_address = 0x1FF467
            start9_b_address = 0x1FF45F
            i = start9_b_address
            while i < original_event_address:
                patch.add_data(i, 0x9B)
                i += 1

            # event 2120
            patch.add_data(0x1F7A4D,
                           [0x60, 0x80, 0xAB, 0xC0, 0x66, 0x58, 0x7A, 0xD2, 0x67, 0xF4, 0xFE, 0x74, 0xD0, 0xCF, 0x0E,
                            0xFE])
            original_end_address = 0x1F7A90
            start9_b_address = 0x1F7A5D
            i = start9_b_address
            while i <= original_end_address:
                patch.add_data(i, 0x9B)
                i += 1

            # Dialog
            patch.add_data(0x23D3CE, [0x44, 0x6F, 0x0F, 0x20, 0x77, 0x61, 0x6E, 0x74, 0x11, 0x67, 0x6F, 0x11, 0x53,
                                      0x6D, 0x69, 0x74, 0x68, 0x79, 0x3F, 0x02, 0x08, 0x07, 0x20, 0x28, 0x4E, 0x6F,
                                      0x29, 0x01, 0x08, 0x07, 0x20, 0x28, 0x59, 0x65, 0x73, 0x29, 0x00])

        # Overworld boss sprites
        if self.open_mode:
            patch += bosses_overworld.patch_overworld_bosses(self)

        # Patch removes ANDing by current party from shop menu code.
        # Replaces it with ANDing by #$1F, which is all party members.
        if self.settings.is_flag_enabled(flags.ShowEquips):
            patch.add_data(0x033B6D, bytes([0x29, 0x1F, 0xEA]))

        # This needs to happen after all battle script randomization.
        patch += assemble_battle_scripts(self)

        # Credit update
        patch += credits.update_credits(self)

        # Choose character for the file select screen.
        i = cursor_id
        file_select_char_bytes = [0, 7, 13, 25, 19]
        self.file_select_character = [c for c in self.characters if c.index == i][0].__class__.__name__

        # Change file select character graphic, if not Mario.
        if i != 0:
            addresses = [0x34757, 0x3489a, 0x34ee7, 0x340aa, 0x3501e]
            for addr, value in zip(addresses, [0, 1, 0, 0, 1]):
                patch.add_data(addr, file_select_char_bytes[i] + value)

        # Possible names we can use for the hash values on the file select screen.  Needs to be 6 characters or less.
        file_entry_names = {
            'MARIO',
            'MALLOW',
            'GENO',
            'BOWSER',
            'PEACH',
        }
        # Also use enemy names, if they're 6 characters or less.
        for e in self.enemies:
            if isinstance(e, data.enemies.K9):
                name = e.name
            else:
                name = re.sub(r'[^A-Za-z]', '', e.name.upper())
            if len(name) <= 6:
                file_entry_names.add(name)
        file_entry_names = sorted(file_entry_names)

        # Replace file select names with "hash" values for seed verification.
        file_select_names = [
            file_entry_names[int(self.hash[0:8], 16) % len(file_entry_names)],
            file_entry_names[int(self.hash[8:16], 16) % len(file_entry_names)],
            file_entry_names[int(self.hash[16:24], 16) % len(file_entry_names)],
            file_entry_names[int(self.hash[24:32], 16) % len(file_entry_names)],
        ]
        for i, name in enumerate(file_select_names):
            addr = 0x3ef528 + (i * 7)
            val = name.encode().ljust(7, b'\x00')
            patch.add_data(addr, val)

        # Save file select hash text to show the user on the website, but the game uses '}' instead of dash.
        self.file_select_hash = ' / '.join(file_select_names).replace('}', '-')

        # Update ROM title and version.
        title = 'SMRPG-R {}'.format(self.seed).ljust(20)
        if len(title) > 20:
            title = title[:19] + '?'

        # Add version number on name entry screen.
        version_text = ('v' + VERSION + " AP").ljust(10)
        if len(version_text) > 10:
            raise ValueError("Version text is too long: {!r}".format(version_text))
        patch.add_data(0x3ef140, version_text)

        # Add title and major version number to SNES header data.
        patch.add_data(0x7fc0, title)
        v = VERSION.split('.')
        patch.add_data(0x7fdb, int(v[0]))

        return patch

    @property
    def spoiler(self):
        """

        Returns:
            dict: Spoiler for current game world state in JSON object form (Python dictionary).

        """
        # TODO: Build spoilers that are in all modes first.
        spoiler = {}

        # TODO: Open mode only spoilers.
        if self.open_mode:
            spoiler['Boss Locations'] = bosses.get_spoiler(self)
            spoiler['Item Locations'] = items.get_spoiler(self)

        return spoiler
