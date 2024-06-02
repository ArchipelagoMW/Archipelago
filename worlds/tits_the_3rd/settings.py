"""Settings definition for Trails in the Sky the 3rd"""
import settings

class TitsThe3rdSettings(settings.Group):
    """Settings definition for Trails in the Sky the 3rd."""
    class GameInstallationPath(settings.UserFolderPath):
        """
        The installation folder of the game from a default steam installation
        """
    game_installation_path: GameInstallationPath = GameInstallationPath("C:/Program Files (x86)/Steam/steamapps/common/Trails in the Sky the 3rd")
