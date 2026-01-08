from enum import Enum
from ..world import PSOWorld

class ConnectionStatus:
    REFUSED_GAME = "Dolphin failed to connect. Please load a randomized ROM for PSO I&II Plus. Trying again in 5 seconds..."
    REFUSED_SAVE = "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
    LOST = "Dolphin connection was lost. Please restart your emulator and make sure PSO I&II Plus is running."
    CONNECTED = "Dolphin connected successfully."
    INITIAL = "Dolphin connection has not been initiated."


class DeathMessage(Enum):
    MAG = "'s Mag didn't love them enough."
    SCAPE_DOLL = " didn't bring enough Scape Dolls."
    PIONEER_2 = " went back to Pioneer 2 the hard way."

def get_death_message() -> str:
    """
    Randomly select a death message to send along with a player's DeathLink
    """
    idx = PSOWorld.random.randint(0, len(DeathMessage))
    return list(DeathMessage)[idx]
