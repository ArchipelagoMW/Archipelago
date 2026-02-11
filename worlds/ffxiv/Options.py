import sys
from Options import PerGameCommonOptions, FreeText, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, DeathLink, \
    OptionGroup, StartInventoryPool, Visibility, item_and_loc_options, Option
from .hooks.Options import before_options_defined, after_options_defined, before_option_groups_created, after_option_groups_created
from .Data import category_table, game_table, option_table
from .Helpers import convert_to_long_string, format_to_valid_identifier
from .Locations import victory_names
from .Items import item_table
from .Game import starting_items

from dataclasses import make_dataclass
from typing import List, Any, Type
import logging


class FillerTrapPercent(Range):
    """How many fillers will be replaced with traps. 0 means no additional traps, 100 means all fillers are traps."""
    range_end = 100

def createChoiceOptions(values: dict, aliases: dict) -> dict:
    values = {'option_' + i: v for i, v in values.items()}
    aliases = {'alias_' + i: v for i, v in aliases.items()}
    return {**values, **aliases}

def convertOptionVisibility(input) -> Visibility:
    visibility = Visibility.all
    if isinstance(input, list):
        visibility = Visibility.none
        for type in input:
            visibility |= Visibility[type.lower()]

    elif isinstance(input,str):
        if input.startswith('0b'):
            visibility = Visibility(int(input, base=0))
        else:
            visibility = Visibility[input.lower()]

    elif isinstance(input, int):
        visibility = Visibility(input)
    return visibility

def getOriginalOptionArguments(option: Type[Option[Any]]) -> dict:
    args = {}
    args['default'] = option.default
    if hasattr(option, 'display_name'): args['display'] = option.display_name
    args['rich_text_doc'] = option.rich_text_doc
    args['default'] = option.default
    args['visibility'] = option.visibility
    return args

manual_option_groups: dict[str, List[Type[Option[Any]]]] = {}
def addOptionToGroup(option_name: str, group: str):
    if group not in manual_option_groups.keys():
        manual_option_groups[group] = []
    if manual_options.get(option_name) and manual_options[option_name] not in manual_option_groups[group]:
        manual_option_groups[group].append(manual_options[option_name])

######################
# Manual's default options
######################

manual_options: dict[str, Type[Option[Any]]] = before_options_defined({})
manual_options["start_inventory_from_pool"] = StartInventoryPool

if len(victory_names) > 1:
    if manual_options.get('goal'):
        logging.warning("Existing Goal option found created via Hooks, it will be overwritten by Manual's generated Goal option.\nIf you want to support old yaml you will need to add alias in after_options_defined")

    goal: dict[str, Any] = {'option_' + v: i for i, v in enumerate(victory_names)}
    goal['__module__'] = __name__

    manual_options['goal'] = type('goal', (Choice,), dict(goal))
    manual_options['goal'].__doc__ = "Choose your victory condition."


if any(item.get('trap') for item in item_table):
    manual_options["filler_traps"] = FillerTrapPercent

if game_table.get("death_link"):
    manual_options["death_link"] = DeathLink


######################
# Option.json options
######################

for option_name, option in option_table.get('core', {}).items():
    if option_name.startswith('_'): #To allow commenting out options
        continue
    option_display_name = option_name
    option_name = format_to_valid_identifier(option_name)

    if manual_options.get(option_name):
        original_option: Type[Option] = manual_options[option_name]
        original_doc = str(original_option.__doc__)

        if issubclass(original_option, Toggle):
            if option.get('default', None) is not None:
                option_type = DefaultOnToggle if option['default'] else Toggle

                if original_option.__base__ != option_type: #only recreate if needed
                    args = getOriginalOptionArguments(original_option)
                    args['__module__'] = __name__
                    manual_options[option_name] = type(option_name, (option_type,), dict(args)) # Type checker doesn't like having a variable as a base for the type # type: ignore
                    logging.debug(f"Manual: Option.json converted option '{option_display_name}' into a {option_type}")

        elif issubclass(original_option, Choice):
            if option.get("values"):
                raise Exception(f"You cannot modify the values of the '{option_display_name}' option since they cannot have their value changed by Option.json")

            if option.get('aliases'):
                for alias, value in option['aliases'].items():
                    original_option.aliases[alias] = value
                original_option.options.update(original_option.aliases)  #for an alias to be valid it must also be in options

                logging.debug(f"Manual: Option.json modified option '{option_display_name}''s aliases")

        elif issubclass(original_option, Range):
            if option.get('values'): #let user add named values
                args = getOriginalOptionArguments(original_option)
                args['special_range_names'] = {}
                if issubclass(original_option, NamedRange):
                    args['special_range_names'] = dict(original_option.special_range_names)
                args['special_range_names']['default'] = option.get('default', args['special_range_names'].get('default', args['default']))
                args['range_start'] = original_option.range_start
                args['range_end'] = original_option.range_end
                args['special_range_names'] = {**args['special_range_names'], **{l.lower(): v for l, v in option['values'].items()}}

                args['__module__'] = __name__
                manual_options[option_name] = type(option_name, (NamedRange,), dict(args))
                logging.debug(f"Manual: Option.json converted option '{option_display_name}' into a {NamedRange}")

        manual_options[option_name].display_name = option.get('display_name', option_display_name) # type: ignore
        manual_options[option_name].__doc__ = convert_to_long_string(option.get('description', original_doc))
        if option.get('rich_text_doc'):
            manual_options[option_name].rich_text_doc = option["rich_text_doc"]

        if option.get('default'):
            manual_options[option_name].default = option['default']

        if option.get('hidden'):
            manual_options[option_name].visibility = Visibility.none
        elif option.get('visibility'):
            manual_options[option_name].visibility = convertOptionVisibility(option['visibility'])
    else:
        logging.debug(f"Manual: Option.json just tried to modify the option '{option_display_name}' but it doesn't currently exists")


supported_option_types = ["Toggle", "Choice", "Range"]
for option_name, option in option_table.get('user', {}).items():
    if option_name.startswith('_'): #To allow commenting out options
        continue
    option_display_name =  option_name
    option_name = format_to_valid_identifier(option_name)
    if manual_options.get(option_name):
        logging.warning(f"Manual: An option with the name '{option_display_name}' cannot be added since it already exists in Manual Core Options. \nTo modify an existing option move it to the 'core' section of Option.json")

    else:
        option_type = option.get('type', "").title()

        if option_type not in supported_option_types:
            raise Exception(f'Option {option_display_name} in options.json has an invalid type of "{option["type"]}".\nIt must be one of the folowing: {supported_option_types}')

        args = {'display_name': option.get('display_name', option_display_name)}

        # Default to Toggle to prevent hypothetical Unbound option_class
        option_class: Type[Option] = DefaultOnToggle if option.get('default', False) else Toggle

        if option_type == "Choice":
            args = {**args, **createChoiceOptions(option.get('values'), option.get('aliases', {}))}
            option_class = TextChoice if option.get("allow_custom_value", False) else Choice

        elif option_type == "Range":
            args['range_start'] = option.get('range_start', 0)
            args['range_end'] = option.get('range_end', 1)
            if option.get('values'):
                args['special_range_names'] = {l.lower(): v for l, v in option['values'].items()}
                args['special_range_names']['default'] = option.get('default', args['range_start'])
            option_class = NamedRange if option.get('values') else Range

        if option.get('default'):
            args['default'] = option['default']

        if option.get('rich_text_doc',None) is not None:
            args["rich_text_doc"] = option["rich_text_doc"]

        if option.get('hidden'):
            args['visibility'] = Visibility.none
        elif option.get('visibility'):
            args['visibility'] = convertOptionVisibility(option['visibility'])

        args['__module__'] = __name__

        manual_options[option_name] = type(option_name, (option_class,), args ) # Same as the first ignore above # type: ignore
        manual_options[option_name].__doc__ = convert_to_long_string(option.get('description', "an Option"))

    if option.get('group'):
        addOptionToGroup(option_name, option['group'])

######################
# category and starting_items options
######################

for category in category_table:
    for option_name in category_table[category].get("yaml_option", []):
        if option_name[0] == "!":
            option_name = option_name[1:]
        option_name = format_to_valid_identifier(option_name)
        if option_name not in manual_options:
            manual_options[option_name] = type(option_name, (DefaultOnToggle,), {"default": True, "__module__": __name__})
            manual_options[option_name].__doc__ = "Should items/locations linked to this option be enabled?"

if starting_items:
    for starting_items in starting_items:
        if starting_items.get("yaml_option"):
            for option_name in starting_items["yaml_option"]:
                if option_name[0] == "!":
                    option_name = option_name[1:]
                option_name = format_to_valid_identifier(option_name)
                if option_name not in manual_options:
                    manual_options[option_name] = type(option_name, (DefaultOnToggle,), {"default": True, "__module__": __name__})
                    manual_options[option_name].__doc__ = "Should items/locations linked to this option be enabled?"

######################
# OptionGroups Creation
######################

def make_options_group() -> list[OptionGroup]:
    global manual_option_groups
    manual_option_groups = before_option_groups_created(manual_option_groups)
    option_groups: List[OptionGroup] = []

    # For some reason, unless they are added manually, the base item and loc option don't get grouped as they should
    base_item_loc_group = item_and_loc_options

    if manual_option_groups:
        if 'Item & Location Options' in manual_option_groups.keys():
            base_item_loc_group = manual_option_groups.pop('Item & Location Options') #Put the custom options before the base AP options
            base_item_loc_group.extend(item_and_loc_options)

        if 'Game Options' in manual_option_groups.keys():
            # Archipelago automatically assign ungrouped options to this group unless its defined so by deleting it here we let AP recreate it later
            manual_option_groups.pop('Game Options')

        for group, options in manual_option_groups.items():
            option_groups.append(OptionGroup(group, options))

    option_groups.append(OptionGroup('Item & Location Options', base_item_loc_group, True))

    return after_option_groups_created(option_groups)

manual_options_data = make_dataclass('ManualOptionsClass', manual_options.items(), bases=(PerGameCommonOptions,))
after_options_defined(manual_options_data)

# Make the options available in this module for import, needed for WebWorld compatibility
this = sys.modules[__name__]
for name, obj in manual_options.items():
    setattr(this, name, obj)
del this
