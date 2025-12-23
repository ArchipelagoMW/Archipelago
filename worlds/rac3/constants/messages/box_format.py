from worlds.rac3.constants.messages.box_colors import RAC3BOXCOLOR
from worlds.rac3.constants.messages.box_theme import RAC3BOXTHEME


class RAC3BOXFORMAT:
    BACKGROUND: int = RAC3BOXCOLOR.DEFAULT_BACKGROUND
    BOX: int = RAC3BOXCOLOR.DEFAULT_BOX
    TEXT: int = RAC3BOXCOLOR.DEFAULT_TEXT

    def __init__(self,
                 background: int = RAC3BOXCOLOR.DEFAULT_BACKGROUND,
                 box: int = RAC3BOXCOLOR.DEFAULT_BOX,
                 text: int = RAC3BOXCOLOR.DEFAULT_TEXT):
        self.BACKGROUND: int = background
        self.BOX: int = box
        self.TEXT: int = text


THEME_ID_TO_THEME_COLORS = {
    RAC3BOXTHEME.DEFAULT: RAC3BOXFORMAT(RAC3BOXCOLOR.DEFAULT_BACKGROUND, RAC3BOXCOLOR.DEFAULT_BOX,
                                        RAC3BOXCOLOR.DEFAULT_TEXT),
    RAC3BOXTHEME.DEATHLINK: RAC3BOXFORMAT(RAC3BOXCOLOR.DEATHLINK_BACKGROUND, RAC3BOXCOLOR.DEATHLINK_BOX,
                                          RAC3BOXCOLOR.DEATHLINK_TEXT),
    RAC3BOXTHEME.WARNING: RAC3BOXFORMAT(RAC3BOXCOLOR.WARNING_BACKGROUND, RAC3BOXCOLOR.WARNING_BOX,
                                        RAC3BOXCOLOR.WARNING_TEXT),
}
