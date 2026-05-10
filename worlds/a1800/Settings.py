from settings import Group, UserFolderPath


class A1800Settings(Group):
    class A1800ModsFolderPath(UserFolderPath):
        """Path to the Anno 1800 mods folder"""

    a1800_mods_folder_path: A1800ModsFolderPath = A1800ModsFolderPath(
        "C:/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/games/Anno 1800/mods"
    )
