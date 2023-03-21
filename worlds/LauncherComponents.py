import os
from json import load as json_load
from enum import Enum, auto
from typing import Optional, Callable, List, Iterable

from Utils import local_path, is_windows


class Type(Enum):
    TOOL = auto()
    FUNC = auto()  # not a real component
    CLIENT = auto()
    ADJUSTER = auto()
    EXTERNAL = auto()


class Component:
    display_name: str
    type: Optional[Type]
    script_name: Optional[str]
    frozen_name: Optional[str]
    icon: str  # just the name, no suffix
    cli: bool
    func: Optional[Callable]
    file_identifier: Optional[Callable[[str], bool]]
    file_path: Optional[str]

    def __init__(self, display_name: str, script_name: Optional[str] = None, frozen_name: Optional[str] = None,
                 cli: bool = False, icon: str = 'icon', component_type: Type = None, func: Optional[Callable] = None,
                 file_identifier: Optional[Callable[[str], bool]] = None, file_path: Optional[str] = None):
        self.display_name = display_name
        self.script_name = script_name
        self.frozen_name = frozen_name or f'Archipelago{script_name}' if script_name else None
        self.icon = icon
        self.cli = cli
        self.type = component_type or \
            None if not display_name else \
            Type.FUNC if func else \
            Type.CLIENT if 'Client' in display_name else \
            Type.ADJUSTER if 'Adjuster' in display_name else \
            Type.EXTERNAL if component_type == Type.EXTERNAL else \
            Type.TOOL
        self.func = func
        self.file_identifier = file_identifier
        self.file_path = file_path

    def handles_file(self, path: str):
        return self.file_identifier(path) if self.file_identifier else False

    def __repr__(self):
        return f"{self.__class__.__name__}({self.display_name})"


class SuffixIdentifier:
    suffixes: Iterable[str]

    def __init__(self, *args: str):
        self.suffixes = args

    def __call__(self, path: str):
        if isinstance(path, str):
            for suffix in self.suffixes:
                if path.endswith(suffix):
                    return True
        return False


components: List[Component] = [
    # Launcher
    Component('', 'Launcher'),
    # Core
    Component('Host', 'MultiServer', 'ArchipelagoServer', cli=True,
              file_identifier=SuffixIdentifier('.archipelago', '.zip')),
    Component('Generate', 'Generate', cli=True),
    Component('Text Client', 'CommonClient', 'ArchipelagoTextClient'),
    # SNI
    Component('SNI Client', 'SNIClient',
              file_identifier=SuffixIdentifier('.apz3', '.apm3', '.apsoe', '.aplttp', '.apsm', '.apsmz3', '.apdkc3',
                                               '.apsmw', '.apl2ac')),
    Component('Links Awakening DX Client', 'LinksAwakeningClient',
              file_identifier=SuffixIdentifier('.apladx')),
    Component('LttP Adjuster', 'LttPAdjuster'),
    # Minecraft
    Component('Minecraft Client', 'MinecraftClient', icon='mcicon', cli=True,
              file_identifier=SuffixIdentifier('.apmc')),
    # Ocarina of Time
    Component('OoT Client', 'OoTClient',
              file_identifier=SuffixIdentifier('.apz5')),
    Component('OoT Adjuster', 'OoTAdjuster'),
    # FF1
    Component('FF1 Client', 'FF1Client'),
    # Pokémon
    Component('Pokemon Client', 'PokemonClient', file_identifier=SuffixIdentifier('.apred', '.apblue')),
    # TLoZ
    Component('Zelda 1 Client', 'Zelda1Client'),
    # ChecksFinder
    Component('ChecksFinder Client', 'ChecksFinderClient'),
    # Starcraft 2
    Component('Starcraft 2 Client', 'Starcraft2Client'),
    # Wargroove
    Component('Wargroove Client', 'WargrooveClient'),
    # Zillion
    Component('Zillion Client', 'ZillionClient',
              file_identifier=SuffixIdentifier('.apzl')),
    #Kingdom Hearts 2
    Component('KH2 Client', "KH2Client"),
]


icon_paths = {
    'icon': local_path('data', 'icon.ico' if is_windows else 'icon.png'),
    'mcicon': local_path('data', 'mcicon.ico')
}


data_files = [os.path.join(root, name)
              for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), "launcher_data"))
              for name in files if name.endswith(".json")]

for file in data_files:
    component_data = json_load(open(file))
    new_component = Component(
        component_data.get("display_name"),
        component_data.get("script_name", None),
        component_data.get("frozen_name", None),
        component_data.get("cli", False),
        component_data.get("icon", "icon"),
        Type.__getitem__(component_data.get("component_type", None)),
        component_data.get("func", None),
        component_data.get("file_identifier", None),
        component_data.get("file_path", None),
    )
    components.append(new_component)
