import pkgutil
from enum import Enum
from io import BytesIO

from kivy.uix.image import CoreImage

from .. import game
from ..game.graphics import Graphic

IMAGE_GRAPHICS = {
    Graphic.EMPTY: None,
    Graphic.WALL: "wall.png",
    Graphic.BUTTON_NOT_ACTIVATED: "button_not_activated.png",
    Graphic.BUTTON_ACTIVATED: "button_activated.png",
    Graphic.KEY_DOOR: "key_door.png",
    Graphic.BUTTON_DOOR: "button_door.png",
    Graphic.CHEST: "chest.png",
    Graphic.BUSH: "bush.png",
    Graphic.BREAKABLE_BLOCK: "breakable_wall.png",
    Graphic.NORMAL_ENEMY_2_HEATLH: "normal_enemy_2.png",
    Graphic.NORMAL_ENEMY_1_HEALTH: "normal_enemy_1.png",
    Graphic.BOSS_5_HEALTH: "boss_5.png",
    Graphic.BOSS_4_HEALTH: "boss_4.png",
    Graphic.BOSS_3_HEALTH: "boss_3.png",
    Graphic.BOSS_2_HEALTH: "boss_2.png",
    Graphic.BOSS_1_HEALTH: "boss_1.png",
    Graphic.KEY: "key.png",
    Graphic.SHIELD: "shield.png",
    Graphic.HAMMER: "hammer.png",
    Graphic.SWORD: "sword.png",
    Graphic.HEART: "full_heart.png",
    Graphic.HALF_HEART: "half_heart.png",
    Graphic.EMPTY_HEART: "empty_heart.png",
    Graphic.CONFETTI_CANNON: "confetti_cannon.png",
    Graphic.REMOTE_ITEM: "ap_item.png",
    Graphic.ITEMS_TEXT: "items_text.png",
    Graphic.UNKNOWN: "unknown.png",
    Graphic.ZERO: "Number_0.png",
    Graphic.ONE: "Number_1.png",
    Graphic.TWO: "Number_2.png",
    Graphic.THREE: "Number_3.png",
    Graphic.FOUR: "Number_4.png",
    Graphic.FIVE: "Number_5.png",
    Graphic.SIX: "Number_6.png",
    Graphic.SEVEN: "Number_7.png",
    Graphic.EIGHT: "Number_8.png",
    Graphic.NINE: "Number_9.png",
    Graphic.LETTER_M: "Letter_M.png",
    Graphic.LETTER_A: "Letter_A.png",
    Graphic.LETTER_T: "Letter_T.png",
    Graphic.LETTER_H: "Letter_H.png",
    Graphic.LETTER_I: "Letter_I.png",
    Graphic.LETTER_E: "Letter_E.png",
    Graphic.PLUS: "Symbol_Plus.png",
    Graphic.MINUS: "Symbol_Minus.png",
    Graphic.TIMES: "Symbol_Times.png",
    Graphic.DIVIDE: "Symbol_Divide.png",
    Graphic.EQUALS: "Symbol_Equals.png",
    Graphic.NO: "No.png",
}

BACKGROUND_TILE = "grass.png"


class PlayerSprite(Enum):
    HUMAN = 0
    DUCK = 1
    HORSE = 2
    CAT = 3
    UNKNOWN = -1


PLAYER_GRAPHICS = {
    Graphic.PLAYER_DOWN: {
        PlayerSprite.HUMAN: "human_down.png",
        PlayerSprite.DUCK: "duck_down.png",
        PlayerSprite.HORSE: "horse_down.png",
        PlayerSprite.CAT: "cat_down.png",
    },
    Graphic.PLAYER_UP: {
        PlayerSprite.HUMAN: "human_up.png",
        PlayerSprite.DUCK: "duck_up.png",
        PlayerSprite.HORSE: "horse_up.png",
        PlayerSprite.CAT: "cat_up.png",
    },
    Graphic.PLAYER_LEFT: {
        PlayerSprite.HUMAN: "human_left.png",
        PlayerSprite.DUCK: "duck_left.png",
        PlayerSprite.HORSE: "horse_left.png",
        PlayerSprite.CAT: "cat_left.png",
    },
    Graphic.PLAYER_RIGHT: {
        PlayerSprite.HUMAN: "human_right.png",
        PlayerSprite.DUCK: "duck_right.png",
        PlayerSprite.HORSE: "horse_right.png",
        PlayerSprite.CAT: "cat_right.png",
    },
}

ALL_GRAPHICS = [
    BACKGROUND_TILE,
    *IMAGE_GRAPHICS.values(),
    *[graphic for sub_dict in PLAYER_GRAPHICS.values() for graphic in sub_dict.values()],
]

TEXTURES = {
    file_name: CoreImage(BytesIO(pkgutil.get_data(game.__name__, f"graphics/{file_name}")), ext="png").texture
    for file_name in ALL_GRAPHICS
    if file_name is not None
}
