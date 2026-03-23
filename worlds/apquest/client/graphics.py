import pkgutil
from collections.abc import Buffer
from enum import Enum
from io import BytesIO
from typing import Literal, NamedTuple, Protocol, cast

from kivy.uix.image import CoreImage

from CommonClient import logger

from .. import game
from ..game.graphics import Graphic


# The import "from kivy.graphics.texture import Texture" does not work correctly.
# We never need the class directly, so we need to use a protocol.
class Texture(Protocol):
    mag_filter: Literal["nearest"]

    def get_region(self, x: int, y: int, w: int, h: int) -> "Texture": ...


class RelatedTexture(NamedTuple):
    base_texture_file: str
    x: int
    y: int
    width: int
    height: int


IMAGE_GRAPHICS: dict[Graphic, str | RelatedTexture] = {
    Graphic.WALL: RelatedTexture("inanimates.png", 16, 32, 16, 16),
    Graphic.BREAKABLE_BLOCK: RelatedTexture("inanimates.png", 32, 32, 16, 16),
    Graphic.CHEST: RelatedTexture("inanimates.png", 0, 16, 16, 16),
    Graphic.BUSH: RelatedTexture("inanimates.png", 16, 16, 16, 16),
    Graphic.KEY_DOOR: RelatedTexture("inanimates.png", 32, 16, 16, 16),
    Graphic.BUTTON_NOT_ACTIVATED: RelatedTexture("inanimates.png", 0, 0, 16, 16),
    Graphic.BUTTON_ACTIVATED: RelatedTexture("inanimates.png", 16, 0, 16, 16),
    Graphic.BUTTON_DOOR: RelatedTexture("inanimates.png", 32, 0, 16, 16),

    Graphic.NORMAL_ENEMY_1_HEALTH: RelatedTexture("normal_enemy.png", 0, 0, 16, 16),
    Graphic.NORMAL_ENEMY_2_HEALTH: RelatedTexture("normal_enemy.png", 16, 0, 16, 16),

    Graphic.BOSS_5_HEALTH: RelatedTexture("boss.png", 16, 16, 16, 16),
    Graphic.BOSS_4_HEALTH: RelatedTexture("boss.png", 0, 16, 16, 16),
    Graphic.BOSS_3_HEALTH: RelatedTexture("boss.png", 32, 32, 16, 16),
    Graphic.BOSS_2_HEALTH: RelatedTexture("boss.png", 16, 32, 16, 16),
    Graphic.BOSS_1_HEALTH: RelatedTexture("boss.png", 0, 32, 16, 16),

    Graphic.EMPTY_HEART: RelatedTexture("hearts.png", 0, 0, 16, 16),
    Graphic.HEART: RelatedTexture("hearts.png", 16, 0, 16, 16),
    Graphic.HALF_HEART: RelatedTexture("hearts.png", 32, 0, 16, 16),

    Graphic.REMOTE_ITEM: RelatedTexture("items.png", 0, 16, 16, 16),
    Graphic.CONFETTI_CANNON: RelatedTexture("items.png", 16, 16, 16, 16),
    Graphic.HAMMER: RelatedTexture("items.png", 32, 16, 16, 16),
    Graphic.KEY: RelatedTexture("items.png", 0, 0, 16, 16),
    Graphic.SHIELD: RelatedTexture("items.png", 16, 0, 16, 16),
    Graphic.SWORD: RelatedTexture("items.png", 32, 0, 16, 16),

    Graphic.ITEMS_TEXT: "items_text.png",

    Graphic.ZERO: RelatedTexture("numbers.png", 0, 16, 16, 16),
    Graphic.ONE: RelatedTexture("numbers.png", 16, 16, 16, 16),
    Graphic.TWO: RelatedTexture("numbers.png", 32, 16, 16, 16),
    Graphic.THREE: RelatedTexture("numbers.png", 48, 16, 16, 16),
    Graphic.FOUR: RelatedTexture("numbers.png", 64, 16, 16, 16),
    Graphic.FIVE: RelatedTexture("numbers.png", 0, 0, 16, 16),
    Graphic.SIX: RelatedTexture("numbers.png", 16, 0, 16, 16),
    Graphic.SEVEN: RelatedTexture("numbers.png", 32, 0, 16, 16),
    Graphic.EIGHT: RelatedTexture("numbers.png", 48, 0, 16, 16),
    Graphic.NINE: RelatedTexture("numbers.png", 64, 0, 16, 16),

    Graphic.LETTER_A: RelatedTexture("letters.png", 0, 16, 16, 16),
    Graphic.LETTER_E: RelatedTexture("letters.png", 16, 16, 16, 16),
    Graphic.LETTER_H: RelatedTexture("letters.png", 32, 16, 16, 16),
    Graphic.LETTER_I: RelatedTexture("letters.png", 0, 0, 16, 16),
    Graphic.LETTER_M: RelatedTexture("letters.png", 16, 0, 16, 16),
    Graphic.LETTER_T: RelatedTexture("letters.png", 32, 0, 16, 16),

    Graphic.DIVIDE: RelatedTexture("symbols.png", 0, 16, 16, 16),
    Graphic.EQUALS: RelatedTexture("symbols.png", 16, 16, 16, 16),
    Graphic.MINUS: RelatedTexture("symbols.png", 32, 16, 16, 16),
    Graphic.PLUS: RelatedTexture("symbols.png", 0, 0, 16, 16),
    Graphic.TIMES: RelatedTexture("symbols.png", 16, 0, 16, 16),
    Graphic.NO: RelatedTexture("symbols.png", 32, 0, 16, 16),

    Graphic.UNKNOWN: RelatedTexture("symbols.png", 32, 0, 16, 16),  # Same as "No"
}

BACKGROUND_TILE = RelatedTexture("inanimates.png", 0, 32, 16, 16)


class PlayerSprite(Enum):
    HUMAN = 0
    DUCK = 1
    HORSE = 2
    CAT = 3
    UNKNOWN = -1


PLAYER_GRAPHICS = {
    Graphic.PLAYER_DOWN: {
        PlayerSprite.HUMAN: RelatedTexture("human.png", 0, 16, 16, 16),
        PlayerSprite.DUCK: RelatedTexture("duck.png", 0, 16, 16, 16),
        PlayerSprite.HORSE: RelatedTexture("horse.png", 0, 16, 16, 16),
        PlayerSprite.CAT: RelatedTexture("cat.png", 0, 16, 16, 16),
    },
    Graphic.PLAYER_UP: {
        PlayerSprite.HUMAN: RelatedTexture("human.png", 16, 0, 16, 16),
        PlayerSprite.DUCK: RelatedTexture("duck.png", 16, 0, 16, 16),
        PlayerSprite.HORSE: RelatedTexture("horse.png", 16, 0, 16, 16),
        PlayerSprite.CAT: RelatedTexture("cat.png", 16, 0, 16, 16),
    },
    Graphic.PLAYER_LEFT: {
        PlayerSprite.HUMAN: RelatedTexture("human.png", 16, 16, 16, 16),
        PlayerSprite.DUCK: RelatedTexture("duck.png", 16, 16, 16, 16),
        PlayerSprite.HORSE: RelatedTexture("horse.png", 16, 16, 16, 16),
        PlayerSprite.CAT: RelatedTexture("cat.png", 16, 16, 16, 16),
    },
    Graphic.PLAYER_RIGHT: {
        PlayerSprite.HUMAN: RelatedTexture("human.png", 0, 0, 16, 16),
        PlayerSprite.DUCK: RelatedTexture("duck.png", 0, 0, 16, 16),
        PlayerSprite.HORSE: RelatedTexture("horse.png", 0, 0, 16, 16),
        PlayerSprite.CAT: RelatedTexture("cat.png", 0, 0, 16, 16),
    },
}

ALL_GRAPHICS = [
    BACKGROUND_TILE,
    *IMAGE_GRAPHICS.values(),
    *[graphic for sub_dict in PLAYER_GRAPHICS.values() for graphic in sub_dict.values()],
]

_textures: dict[str | RelatedTexture, Texture] = {}


def get_texture_by_identifier(texture_identifier: str | RelatedTexture) -> Texture:
    if texture_identifier in _textures:
        return _textures[texture_identifier]

    if isinstance(texture_identifier, str):
        image_data = pkgutil.get_data(game.__name__, f"graphics/{texture_identifier}")
        if image_data is None:
            raise RuntimeError(f'Could not find file "graphics/{texture_identifier}" for texture {texture_identifier}')

        image_bytes = BytesIO(cast(Buffer, image_data))
        texture = cast(Texture, CoreImage(image_bytes, ext="png").texture)
        texture.mag_filter = "nearest"
        _textures[texture_identifier] = texture
        return texture

    base_texture_filename, x, y, w, h = texture_identifier

    base_texture = get_texture_by_identifier(base_texture_filename)

    sub_texture = base_texture.get_region(x, y, w, h)
    sub_texture.mag_filter = "nearest"
    _textures[texture_identifier] = sub_texture
    return sub_texture


def get_texture(graphic: Graphic | Literal["Grass"], player_sprite: PlayerSprite | None = None) -> Texture | None:
    if graphic == Graphic.EMPTY:
        return None

    if graphic == "Grass":
        return get_texture_by_identifier(BACKGROUND_TILE)

    if graphic in IMAGE_GRAPHICS:
        return get_texture_by_identifier(IMAGE_GRAPHICS[graphic])

    if graphic in PLAYER_GRAPHICS:
        if player_sprite is None:
            raise ValueError("Tried to load a player graphic without specifying a player_sprite")

        return get_texture_by_identifier(PLAYER_GRAPHICS[graphic][player_sprite])

    logger.exception(f"Tried to load unknown graphic {graphic}.")
    return get_texture(Graphic.UNKNOWN)
