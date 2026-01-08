from ..constants.entities import TERRA, LOCKE, CYAN, SHADOW, EDGAR, SABIN, CELES, STRAGO, RELM, SETZER, MOG, GAU, GOGO, UMARO
from ..data.event_bit import TEMP_SONG_OVERRIDE
from ..instruction import field

character_to_song = {
    TERRA: 0x06,
    SHADOW: 0x07,
    STRAGO: 0x08,
    GAU: 0x09,
    EDGAR: 0x0a,
    SABIN: 0x0a,
    CYAN: 0x0c,
    LOCKE: 0x0d,
    RELM: 0x0f,
    SETZER: 0x10,
    CELES: 0x12,
    GOGO: 0x2d,
    UMARO: 0x30,
    MOG: 0x31
}

# Return id for character theme given a character id
def get_character_theme(char_id):
    return character_to_song[char_id]
