
from enum import IntEnum


class MovementSpeed(IntEnum):
    WALK = 2    # Original FF6 walk speed
    SPRINT = 3  # Original FF6 sprint speed
    DASH = 4    # Custom, move twice as fast as sprint.

ORIGINAL = 'og'
AUTO_SPRINT = 'as'
B_DASH = 'bd'
SPRINT_SHOES_B_DASH = 'ssbd'

name_key = {
    # WALK by default
    # SPRINT with sprint shoes equipped
    'ORIGINAL' : ORIGINAL,
    # SPRINT by default
    # WALK when holding B
    'AUTO_SPRINT' : AUTO_SPRINT,
    # SPRINT by default
    # DASH when holding B
    'B-DASH' : B_DASH,
    # SPRINT by default
    # DASH when holding B with sprint shoes equipped
    # WALK when holding B without sprint shoes equipped
    'SPR SHOE B-DASH' : SPRINT_SHOES_B_DASH,
}

key_name = {v: k for k, v in name_key.items()}

ALL = [ORIGINAL, AUTO_SPRINT, B_DASH, SPRINT_SHOES_B_DASH]

