import typing
from Options import Option, DefaultOnToggle, Range, Toggle, DeathLink, Choice


class CharacterGate(DefaultOnToggle):
    """Disable for full open mode"""
    display_name = "Enable Character Gate"


class CharacterCount(Range):
    """Sets the number of characters needed to access Kefka's Tower"""
    display_name = "Characters Required"
    range_start = 0
    range_end = 14
    default = 8


class EsperCount(Range):
    """Sets the number of Espers needed to access Kefka's Tower"""
    display_name = "Espers Required"
    range_start = 0
    range_end = 27
    default = 12


class DragonCount(Range):
    """Sets the number of dragons needed to access Kefka's Tower"""
    display_name = "Dragons Required"
    range_start = 0
    range_end = 8
    default = 2

class StartingCharacterCount(Range):
    """Sets the number of starting characters"""
    display_name = "Starting Character Count"
    range_start = 1
    range_end = 4
    default = 2

class StartingCharacter1(Choice):
    """Starting Character 1"""
    display_name = "Starting Character 1"
    option_terra = 0
    option_locke = 1
    option_edgar = 2
    option_sabin = 3
    option_celes = 4
    option_shadow = 5
    option_cyan = 6
    option_gau = 7
    option_setzer = 8
    option_mog = 9
    option_strago = 10
    option_relm = 11
    option_gogo = 12
    option_umaro = 13
    option_random_with_no_gogo_or_umaro = 14
    default = 14

class StartingCharacter2(Choice):
    """Starting Character 2. Only used if Starting Character Count is 2+"""
    display_name = "Starting Character 2"
    option_terra = 0
    option_locke = 1
    option_edgar = 2
    option_sabin = 3
    option_celes = 4
    option_shadow = 5
    option_cyan = 6
    option_gau = 7
    option_setzer = 8
    option_mog = 9
    option_strago = 10
    option_relm = 11
    option_gogo = 12
    option_umaro = 13
    option_none = 14
    option_random_with_no_gogo_or_umaro = 15
    default = 15

class StartingCharacter3(Choice):
    """Starting Character 3. Only used if Starting Character Count is 3+"""
    display_name = "Starting Character 3"
    option_terra = 0
    option_locke = 1
    option_edgar = 2
    option_sabin = 3
    option_celes = 4
    option_shadow = 5
    option_cyan = 6
    option_gau = 7
    option_setzer = 8
    option_mog = 9
    option_strago = 10
    option_relm = 11
    option_gogo = 12
    option_umaro = 13
    option_none = 14
    option_random_with_no_gogo_or_umaro = 15
    default = 14

class StartingCharacter4(Choice):
    """Starting Character 4. Only used if Starting Character Count is 4"""
    display_name = "Starting Character 4"
    option_terra = 0
    option_locke = 1
    option_edgar = 2
    option_sabin = 3
    option_celes = 4
    option_shadow = 5
    option_cyan = 6
    option_gau = 7
    option_setzer = 8
    option_mog = 9
    option_strago = 10
    option_relm = 11
    option_gogo = 12
    option_umaro = 13
    option_none = 14
    option_random_with_no_gogo_or_umaro = 15
    default = 14


ff6wc_options: typing.Dict[str, type(Option)] = {
    "CharacterGate": CharacterGate,
    "CharacterCount": CharacterCount,
    "EsperCount": EsperCount,
    "DragonCount": DragonCount,
    "StartingCharacterCount": StartingCharacterCount,
    "StartingCharacter1": StartingCharacter1,
    "StartingCharacter2": StartingCharacter2,
    "StartingCharacter3": StartingCharacter3,
    "StartingCharacter4": StartingCharacter4,
}
