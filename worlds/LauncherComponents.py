import weakref
from enum import Enum, auto
from typing import Optional, Callable, List, Iterable

from Utils import local_path


class Type(Enum):
    TOOL = auto()
    MISC = auto()
    CLIENT = auto()
    ADJUSTER = auto()
    FUNC = auto()  # do not use anymore
    HIDDEN = auto()


class Component:
    display_name: str
    type: Type
    script_name: Optional[str]
    frozen_name: Optional[str]
    icon: str  # just the name, no suffix
    cli: bool
    func: Optional[Callable]
    file_identifier: Optional[Callable[[str], bool]]

    def __init__(self, display_name: str, script_name: Optional[str] = None, frozen_name: Optional[str] = None,
                 cli: bool = False, icon: str = 'icon', component_type: Optional[Type] = None,
                 func: Optional[Callable] = None, file_identifier: Optional[Callable[[str], bool]] = None):
        self.display_name = display_name
        self.script_name = script_name
        self.frozen_name = frozen_name or f'Archipelago{script_name}' if script_name else None
        self.icon = icon
        self.cli = cli
        if component_type == Type.FUNC:
            from Utils import deprecate
            deprecate(f"Launcher Component {self.display_name} is using Type.FUNC Type, which is pending removal.")
            component_type = Type.MISC

        self.type = component_type or (
            Type.CLIENT if "Client" in display_name else
            Type.ADJUSTER if "Adjuster" in display_name else Type.MISC)
        self.func = func
        self.file_identifier = file_identifier

    def handles_file(self, path: str):
        return self.file_identifier(path) if self.file_identifier else False

    def __repr__(self):
        return f"{self.__class__.__name__}({self.display_name})"

processes = weakref.WeakSet()

def launch_subprocess(func: Callable, name: str = None):
    global processes
    import multiprocessing
    process = multiprocessing.Process(target=func, name=name)
    process.start()
    processes.add(process)

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


def launch_textclient():
    import CommonClient
    launch_subprocess(CommonClient.run_as_textclient, name="TextClient")


components: List[Component] = [
    # Launcher
    Component('Launcher', 'Launcher', component_type=Type.HIDDEN),
    # Core
    Component('Host', 'MultiServer', 'ArchipelagoServer', cli=True,
              file_identifier=SuffixIdentifier('.archipelago', '.zip')),
    Component('Generate', 'Generate', cli=True),
    Component('Text Client', 'CommonClient', 'ArchipelagoTextClient', func=launch_textclient),
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
    # TLoZ
    Component('Zelda 1 Client', 'Zelda1Client', file_identifier=SuffixIdentifier('.aptloz')),
    # ChecksFinder
    Component('ChecksFinder Client', 'ChecksFinderClient'),
    # Starcraft 2
    Component('Starcraft 2 Client', 'Starcraft2Client'),
    # Wargroove
    Component('Wargroove Client', 'WargrooveClient'),
    # Zillion
    Component('Zillion Client', 'ZillionClient',
              file_identifier=SuffixIdentifier('.apzl')),

    #MegaMan Battle Network 3
    Component('MMBN3 Client', 'MMBN3Client', file_identifier=SuffixIdentifier('.apbn3'))
]


icon_paths = {
    'icon': local_path('data', 'icon.png'),
    'mcicon': local_path('data', 'mcicon.png'),
    'discord': local_path('data', 'discord-mark-blue.png'),
}
