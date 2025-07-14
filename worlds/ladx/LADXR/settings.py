from typing import List, Tuple, Optional, Union
import os


class Setting:
    def __init__(self, key: str,
                 category: str, short_key: str, label: str, *,
                 description: str, multiworld: bool = True, aesthetic: bool = False, options: Optional[List[Tuple[str, str, str]]] = None,
                 default: Optional[Union[bool, float, str]] = None, placeholder: Optional[str] = None):
        if options:
            assert default in [option_key for option_key, option_short, option_label in options], f"{default} not in {options}"
            short_options = set()
            for option_key, option_short, option_label in options:
                assert option_short != "" or option_key == default, f"No short option for non default {label}:{option_key}"
                assert option_short not in short_options, "Duplicate short option value..."
                short_options.add(option_short)

        self.key = key
        self.category = category
        self.short_key = short_key
        self.label = label
        self.description = description
        self.multiworld = multiworld
        self.aesthetic = aesthetic
        self.options = options
        self.default = default
        self.placeholder = placeholder

        self.value = default

    def set(self, value):
        if isinstance(self.default, bool):
            if not isinstance(value, bool):
                value = bool(int(value))
        elif not isinstance(value, type(self.default)):
            try:
                value = type(self.default)(value)
            except ValueError:
                raise ValueError(f"{value} is not an accepted value for {self.key} setting")
        if self.options:
            if value not in [k for k, s, v in self.options]:
                raise ValueError(f"{value} is not an accepted value for {self.key} setting")
        self.value = value

    def getShortValue(self):
        if self.options:
            for option_key, option_short, option_label in self.options:
                if self.value == option_key:
                    return option_short
        return self.value + ">"

    def toJson(self):
        result = {
            "key": self.key,
            "category": self.category,
            "short_key": self.short_key,
            "label": self.label,
            "description": self.description,
            "multiworld": self.multiworld,
            "aesthetic": self.aesthetic,
            "default": self.default,
        }
        if self.options:
            result["options"] = [{"key": option_key, "short": option_short, "label": option_label} for option_key, option_short, option_label in self.options]
        if self.placeholder:
            result["placeholder"] = self.placeholder
        return result


class Settings:
    def __init__(self, ap_options):
        self.__all = [
            Setting('seed', 'Main', '<', 'Seed', placeholder='Leave empty for random seed', default="", multiworld=False,
                description="""For multiple people to generate the same randomization result, enter the generated seed number here.
Note, not all strings are valid seeds."""),
            Setting('logic', 'Main', 'L', 'Logic', options=[('casual', 'c', 'Casual'), ('normal', 'n', 'Normal'), ('hard', 'h', 'Hard'), ('glitched', 'g', 'Glitched'), ('hell', 'H', 'Hell')], default='normal',
                description="""Affects where items are allowed to be placed.
[Casual] Same as normal, except that a few more complex options are removed, like removing bushes with powder and killing enemies with powder or bombs.
[Normal] playable without using any tricks or glitches. Requires nothing to be done outside of normal item usage.
[Hard] More advanced techniques may be required, but glitches are not. Examples include tricky jumps, killing enemies with only pots and skipping keys with smart routing.
[Glitched] Advanced glitches and techniques may be required, but extremely difficult or tedious tricks are not required. Examples include Bomb Triggers, Super Jumps and Jesus Jumps.
[Hell] Obscure and hard techniques may be required. Examples include featherless jumping with boots and/or hookshot, sequential pit buffers and unclipped superjumps. Things in here can be extremely hard to do or very time consuming. Only insane people go for this."""),
            Setting('forwardfactor', 'Main', 'F', 'Forward Factor', default=0.0,
                description="Forward item weight adjustment factor, lower values generate more rear heavy seeds while higher values generate front heavy seeds. Default is 0.5."),
            Setting('accessibility', 'Main', 'A', 'Accessibility', options=[('all', 'a', '100% Locations'), ('goal', 'g', 'Beatable')], default='all',
                description="""
[100% Locations] guaranteed that every single item can be reached and gained.
[Beatable] only guarantees that the game is beatable. Certain items/chests might never be reachable."""),
            Setting('race', 'Main', 'V', 'Race mode', default=False, multiworld=False,
                description="""
Spoiler logs can not be generated for ROMs generated with race mode enabled, and seed generation is slightly different."""),
#             Setting('spoilerformat', 'Main', 'Spoiler Format', options=[('none', 'None'), ('text', 'Text'), ('json', 'JSON')], default='none', multiworld=False,
#                 description="""Affects how the spoiler log is generated.
# [None] No spoiler log is generated. One can still be manually dumped later.
# [Text] Creates a .txt file meant for a human to read.
# [JSON] Creates a .json file with a little more information and meant for a computer to read.""")
            Setting('heartpiece', 'Items', 'h', 'Randomize heart pieces', default=True,
                description='Includes heart pieces in the item pool'),
            Setting('seashells', 'Items', 's', 'Randomize hidden seashells', default=True,
                description='Randomizes the secret sea shells hiding in the ground/trees. (chest are always randomized)'),
            Setting('heartcontainers', 'Items', 'H', 'Randomize heart containers', default=True,
                description='Includes boss heart container drops in the item pool'),
            Setting('instruments', 'Items', 'I', 'Randomize instruments', default=False,
                description='Instruments are placed on random locations, dungeon goal will just contain a random item.'),
            Setting('tradequest', 'Items', 'T', 'Randomize trade quest', default=True,
                description='Trade quest items are randomized, each NPC takes its normal trade quest item, but gives a random item'),
            Setting('witch', 'Items', 'W', 'Randomize item given by the witch', default=True,
                description='Adds both the toadstool and the reward for giving the toadstool to the witch to the item pool'),
            Setting('rooster', 'Items', 'R', 'Add the rooster', default=True,
                description='Adds the rooster to the item pool. Without this option, the rooster spot is still a check giving an item. But you will never find the rooster. Any rooster spot is accessible without rooster by other means.'),
            Setting('boomerang', 'Items', 'Z', 'Boomerang trade', options=[('default', 'd', 'Normal'), ('trade', 't', 'Trade'), ('gift', 'g', 'Gift')], default='gift',
                description="""
[Normal], requires magnifier to get the boomerang.
[Trade], allows to trade an inventory item for a random other inventory item boomerang is shuffled.
[Gift], You get a random gift of any item, and the boomerang is shuffled."""),
            Setting('randomstartlocation', 'Gameplay', 'r', 'Random start location', default=False,
                description='Randomize where your starting house is located'),
            Setting('dungeonshuffle', 'Gameplay', 'u', 'Dungeon shuffle', default=False,
                description='Randomizes the dungeon that each dungeon entrance leads to'),
            Setting('entranceshuffle', 'Gameplay', 'E', 'Entrance randomizer', options=[("none", '', "Default"), ("simple", 's', "Simple"), ("advanced", 'a', "Advanced"), ("expert", 'E', "Expert"), ("insanity", 'I', "Insanity")], default='none',
                description="""Randomizes where overworld entrances lead to.
[Simple] single entrance caves that contain items are randomized
[Advanced] Connector caves are also randomized
[Expert] Caves/houses without items are also randomized
[Insanity] A few very annoying entrances will be randomized as well.
If random start location and/or dungeon shuffle is enabled, then these will be shuffled with all the entrances.
Note, some entrances can lead into water, use the warp-to-home from the save&quit menu to escape this."""),
            Setting('boss', 'Gameplay', 'B', 'Boss shuffle', options=[('default', '', 'Normal'), ('shuffle', 's', 'Shuffle'), ('random', 'r', 'Randomize')], default='default',
                description='Randomizes the dungeon bosses that each dungeon has'),
            Setting('miniboss', 'Gameplay', 'b', 'Miniboss shuffle', options=[('default', '', 'Normal'), ('shuffle', 's', 'Shuffle'), ('random', 'r', 'Randomize')], default='default',
                description='Randomizes the dungeon minibosses that each dungeon has'),
            Setting('goal', 'Gameplay', 'G', 'Goal', options=[('8', '8', '8 instruments'), ('7', '7', '7 instruments'), ('6', '6', '6 instruments'),
                                                         ('5', '5', '5 instruments'), ('4', '4', '4 instruments'), ('3', '3', '3 instruments'),
                                                         ('2', '2', '2 instruments'), ('1', '1', '1 instrument'), ('0', '0', 'No instruments'),
                                                         ('open', 'O', 'Egg already open'), ('random', 'R', 'Random instrument count'),
                                                         ('open-4', '<', 'Random short game (0-4)'), ('5-8', '>', 'Random long game (5-8)'),
                                                         ('seashells', 'S', 'Seashell hunt (20)'), ('bingo', 'b', 'Bingo!'),
                                                         ('bingo-full', 'B', 'Bingo-25!')], default='8',
                description="""Changes the goal of the game.
[1-8 instruments], number of instruments required to open the egg.
[No instruments] open the egg without instruments, still requires the ocarina with the balled of the windfish
[Egg already open] the egg is already open, just head for it once you have the items needed to defeat the boss.
[Randomized instrument count] random number of instruments required to open the egg, between 0 and 8.
[Random short/long game] random number of instruments required to open the egg, chosen between 0-4 and 5-8 respectively.
[Seashell hunt] egg will open once you collected 20 seashells. Instruments are replaced by seashells and shuffled.
[Bingo] Generate a 5x5 bingo board with various goals. Complete one row/column or diagonal to win!
[Bingo-25] Bingo, but need to fill the whole bingo card to win!"""),
            Setting('itempool', 'Gameplay', 'P', 'Item pool', options=[('', '', 'Normal'), ('casual', 'c', 'Casual'), ('pain', 'p', 'Path of Pain'), ('keyup', 'k', 'More keys')], default='',
                description="""Effects which items are shuffled.
[Casual] places more inventory and key items so the seed is easier.
[More keys] adds more small keys and extra nightmare keys so dungeons are easier.
[Path of pain]... just find out yourself."""),
            Setting('hpmode', 'Gameplay', 'm', 'Health mode', options=[('default', '', 'Normal'), ('inverted', 'i', 'Inverted'), ('1', '1', 'Start with 1 heart'), ('low', 'l', 'Low max')], default='default',
                description="""
[Normal} health works as you would expect.
[Inverted] you start with 9 heart containers, but killing a boss will take a heartcontainer instead of giving one.
[Start with 1] normal game, you just start with 1 heart instead of 3.
[Low max] replace heart containers with heart pieces."""),
            Setting('hardmode', 'Gameplay', 'X', 'Hard mode', options=[('none', '', 'Disabled'), ('oracle', 'O', 'Oracle'), ('hero', 'H', 'Hero'), ('ohko', '1', 'One hit KO')], default='none',
                description="""
[Oracle] Less iframes and heath from drops. Bombs damage yourself. Water damages you without flippers. No piece of power or acorn.
[Hero] Switch version hero mode, double damage, no heart/fairy drops.
[One hit KO] You die on a single hit, always."""),
            Setting('steal', 'Gameplay', 't', 'Stealing from the shop',
                options=[('inlogic', 'a', 'In logic'), ('disabled', 'n', 'Disabled'), ('outoflogic', '', 'Out of logic')], default='outoflogic',
                description="""Effects when you can steal from the shop and if it is in logic.
[Normal] requires the sword before you can steal.
[Always] you can always steal from the shop
[Never] you can never steal from the shop."""),
            Setting('bowwow', 'Special', 'g', 'Good boy mode', options=[('normal', '', 'Disabled'), ('always', 'a', 'Enabled'), ('swordless', 's', 'Enabled (swordless)')], default='normal',
                description='Allows BowWow to be taken into any area, damage bosses and more enemies. If enabled you always start with bowwow. Swordless option removes the swords from the game and requires you to beat the game without a sword and just bowwow.'),
            Setting('overworld', 'Special', 'O', 'Overworld', options=[('normal', '', 'Normal'), ('dungeondive', 'D', 'Dungeon dive'), ('nodungeons', 'N', 'No dungeons'), ('random', 'R', 'Randomized'), ('openmabe', 'M', 'Open Mabe')], default='normal',
                description="""
[Dungeon Dive] Create a different overworld where all the dungeons are directly accessible and almost no chests are located in the overworld.
[No dungeons] All dungeons only consist of a boss fight and a instrument reward. Rest of the dungeon is removed.
[Random] Creates a randomized overworld WARNING: This will error out often during generation, work in progress."""),
            Setting('owlstatues', 'Special', 'o', 'Owl statues', options=[('', '', 'Never'), ('dungeon', 'D', 'In dungeons'), ('overworld', 'O', 'On the overworld'), ('both', 'B', 'Dungeons and Overworld')], default='',
                description='Replaces the hints from owl statues with additional randomized items'),
            Setting('superweapons', 'Special', 'q', 'Enable super weapons', default=False,
                description='All items will be more powerful, faster, harder, bigger stronger. You name it.'),
            Setting('quickswap', 'User options', 'Q', 'Quickswap', options=[('none', '', 'Disabled'), ('a', 'a', 'Swap A button'), ('b', 'b', 'Swap B button')], default='none',
                description='Adds that the select button swaps with either A or B. The item is swapped with the top inventory slot. The map is not available when quickswap is enabled.',
                aesthetic=True),
            Setting('textmode', 'User options', 'f', 'Text mode', options=[('fast', '', 'Fast'), ('normal', 'd', 'Normal'), ('none', 'n', 'No-text')], default='fast',
                description="""[Fast] makes text appear twice as fast.
[No-Text] removes all text from the game""", aesthetic=True),
            Setting('lowhpbeep', 'User options', 'p', 'Low HP beeps', options=[('none', 'D', 'Disabled'), ('slow', 'S', 'Slow'), ('default', 'N', 'Normal')], default='slow',
                description='Slows or disables the low health beeping sound', aesthetic=True),
            Setting('noflash', 'User options', 'l', 'Remove flashing lights', default=True,
                description='Remove the flashing light effects from Mamu, shopkeeper and MadBatter. Useful for capture cards and people that are sensitive for these things.',
                aesthetic=True),
            Setting('nagmessages', 'User options', 'S', 'Show nag messages', default=False,
                description='Enables the nag messages normally shown when touching stones and crystals',
                aesthetic=True),
            Setting('gfxmod', 'User options', 'c', 'Graphics', default='',
                description='Generally affects at least Link\'s sprite, but can alter any graphics in the game',
                aesthetic=True),
            Setting('linkspalette', 'User options', 'C', "Link's color",
                options=[('-1', '-', 'Normal'), ('0', '0', 'Green'), ('1', '1', 'Yellow'), ('2', '2', 'Red'), ('3', '3', 'Blue'),
                         ('4', '4', '?? A'), ('5', '5', '?? B'), ('6', '6', '?? C'), ('7', '7', '?? D')], default='-1', aesthetic=True,
                description="""Allows you to force a certain color on link.
[Normal] color of link depends on the tunic.
[Green/Yellow/Red/Blue] forces link into one of these colors.
[?? A/B/C/D] colors of link are usually inverted and color depends on the area you are in."""),
            Setting('music', 'User options', 'M', 'Music', options=[('', '', 'Default'), ('random', 'r', 'Random'), ('off', 'o', 'Disable')], default='',
                description="""
[Random] Randomizes overworld and dungeon music'
[Disable] no music in the whole game""",
                aesthetic=True),
        ]
        self.__by_key = {s.key: s for s in self.__all}

        # Make sure all short keys are unique
        short_keys = set()
        for s in self.__all:
            assert s.short_key not in short_keys, s.label
            short_keys.add(s.short_key)
            self.ap_options = ap_options

        for option in self.ap_options.values():
            if not hasattr(option, 'to_ladxr_option'):
                continue
            name, value = option.to_ladxr_option(self.ap_options)
            if value == "true":
                value = 1
            elif value == "false":
                value = 0

            if name:
                self.set( f"{name}={value}")
    
    def __getattr__(self, item):
        return self.__by_key[item].value

    def __setattr__(self, key, value):
        if not key.startswith("_") and key in self.__by_key:
            self.__by_key[key].set(value)
        else:
            super().__setattr__(key, value)

    def loadShortString(self, value):
        for setting in self.__all:
            if isinstance(setting.default, bool):
                setting.value = False
        index = 0
        while index < len(value):
            key = value[index]
            index += 1
            for setting in self.__all:
                if setting.short_key != key:
                    continue
                if isinstance(setting.default, bool):
                    setting.value = True
                elif setting.options:
                    for option_key, option_short, option_label in setting.options:
                        if option_key != setting.default and value[index:].startswith(option_short):
                            setting.value = option_key
                            index += len(option_short)
                            break
                else:
                    end_of_param = value.find(">", index)
                    setting.value = value[index:end_of_param]
                    index = end_of_param + 1

    def getShortString(self):
        result = ""
        for setting in self.__all:
            if isinstance(setting.default, bool):
                if setting.value:
                    result += setting.short_key
            elif setting.value != setting.default:
                result += setting.short_key + setting.getShortValue()
        return result

    def validate(self):
        def req(setting: str, value: str, message: str) -> None:
            if getattr(self, setting) != value:
                print("Warning: %s (setting adjusted automatically)" % message)
                setattr(self, setting, value)

        def dis(setting: str, value: str, new_value: str, message: str) -> None:
            if getattr(self, setting) == value:
                print("Warning: %s (setting adjusted automatically)" % message)
                setattr(self, setting, new_value)

        if self.goal in ("bingo", "bingo-full"):
            req("overworld", "normal", "Bingo goal does not work with dungeondive")
            req("accessibility", "all", "Bingo goal needs 'all' accessibility")
            dis("steal", "disabled", "default", "With bingo goal, stealing should be allowed")
            dis("boss", "random", "shuffle", "With bingo goal, bosses need to be on normal or shuffle")
            dis("miniboss", "random", "shuffle", "With bingo goal, minibosses need to be on normal or shuffle")
        if self.overworld == "dungeondive":
            dis("goal", "seashells", "8", "Dungeon dive does not work with seashell goal")
        if self.overworld == "nodungeons":
            dis("goal", "seashells", "8", "No dungeons does not work with seashell goal")
        if self.overworld == "random":
            self.goal = "4"  # Force 4 dungeon goal for random overworld right now.

    def set(self, value: str) -> None:
        if "=" in value:
            key, value = value.split("=", 1)
        else:
            key, value = value, "1"
        if key not in self.__by_key:
            raise ValueError(f"Setting {key} not found")
        self.__by_key[key].set(value)

    def toJson(self):
        return [s.toJson() for s in self.__all]

    def __iter__(self):
        return iter(self.__all)
