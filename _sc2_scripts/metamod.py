"""
metamod
A utility for modding the game live prior to loading.
The mod files contain stubs in `Mods/ArchipelagoPatches.SC2Mod/` that we can write to.
"""
from typing import *
import enum
import os

# Result helpers

R = TypeVar('R')
E = TypeVar('E')

class Okay(Generic[R]):
    def __init__(self, data: R) -> None:
        self.data = data
    

class Error(Generic[E]):
    def __init__(self, data: E) -> None:
        self.data = data

Result = Okay[R] | Error[E]

# end of result helpers

class DataFile(enum.Enum):
    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, default_tag: str):
        self.default_tag = default_tag

    Abil = 'CAbilEffectTarget',  # variable
    Actor = 'CActorUnit',        # variable
    Behavior = 'CBehaviorBuff',  # variable
    Button = 'CButton',
    Effect = 'CEffectDamage', # variable
    Model = 'CModel',
    Requirement = 'CRequirement',
    RequirementNode = 'CRequirementCountUpgrade',  # variable
    Sound = 'CSound',
    Turret = 'CTurret',
    Unit = 'CUnit',
    Upgrade = 'CUpgrade',
    Validator = 'CValidatorUnitType',  # variable
    Weapon = 'CWeaponLegacy',


def load_metamod_toml(contents: str) -> Result[dict[str, Any], str]:
    try:
        import tomllib
    except ImportError:
        return Error("Couldn't import tomllib. Requires Python 3.12")
    result = tomllib.loads(contents)
    return Okay(result)


def load_all_metamods() -> Result[Tuple[()], str]:
    with open('metamod_test.toml', 'r') as fp:
        contents = fp.read()
    result = load_metamod_toml(contents)
    if isinstance(result, Error):
        return result
    result = result.data


def xml_key(tag: str, content: dict[str, Any] | list | str | int, indent=2) -> list[str]:
    result: list[str] = []
    if isinstance(content, list):
        for entry in content:
            result.append(xml_key(tag, entry))
    elif isinstance(content, dict):
        attributes = [f' {k}="{v}"' for k, v in content.items() if k[0].islower()]
        children = {k: v for k, v in content.items() if k[0].isupper()}
        result.append(f'{" "*(indent*4)}<{tag}{"".join(attributes)}{"" if children else "/"}>')
        for child in children:
            result.extend(xml_key(child, children[child]))
        if children:
            result.append(f'{" "*(indent*4)}</{tag}>')
    else:
        result.append(f'{" "*(indent*4)}<{tag} value="{content}"/>')
    return result


def format_metamod(mod_data: dict[str, dict[str, Any]], file_type: DataFile) -> str:
    result = ['<?xml version="1.0" encoding="utf-8"?>', '<Catalog>']
    for key, content in mod_data.items():
        tag = content.get('$tag', file_type.default_tag)
        attributes = [f' {k}="{v}"' for k, v in content.items() if k[0].islower()]
        children = {k: v for k, v in content.items() if k[0].isupper()}
        result.append(f'    <{tag} id="{key}"{"".join(attributes)}{"" if children else "/"}>')
        for child in children:
            result.extend(xml_key(child, children[child]))
        if children:
            result.append(f'    </{tag}>')
    result.append('</Catalog>')
    return '\n'.join(result)


def write_metamod(metamod_data: dict[str, Any], sc2_path: str) -> None:
    game_data_dir = os.path.join(sc2_path, 'Mods/ArchipelagoPatches.SC2Mod/GameData')
    os.makedirs(game_data_dir, exist_ok=True)
    for data_file_type in DataFile._member_names_:
        data = metamod_data.get(data_file_type)
        if not data: data = metamod_data.get(data_file_type.lower())
        if not data: data = metamod_data.get(data_file_type + 's')
        if not data: data = metamod_data.get(data_file_type.lower() + 's')
        if not data: continue
        content = format_metamod(data, file_type=DataFile[data_file_type])
        target_file = os.path.join(game_data_dir, f'{data_file_type}Data.xml')
        print(f"Writing {target_file}")
        with open(target_file, 'w') as fp:
            fp.write(content)


if __name__ == '__main__':
    load_all_metamods()
    # todo(mm):
    # metamod merges
    # load from yaml
    # load from json
    # load from url
