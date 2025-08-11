import pkgutil
from io import BytesIO

from kivy.uix.image import CoreImage

from ..apquest.graphics import Graphic

IMAGE_GRAPHICS = {
    Graphic.EMPTY: "empty.png",
    Graphic.WALL: "wall.png",
    Graphic.BUTTON_NOT_ACTIVATED: "button_not_activated.png",
    Graphic.BUTTON_ACTIVATED: "button_activated.png",
    Graphic.KEY_DOOR: "key_door.png",
    Graphic.BUTTON_DOOR: "button_door.png",
    Graphic.CHEST: "chest.png",
    Graphic.BUSH: "bush.png",
    Graphic.NORMAL_ENEMY_3_HEALTH: "normal_enemy_3.png",
    Graphic.NORMAL_ENEMY_2_HEATLH: "normal_enemy_2.png",
    Graphic.NORMAL_ENEMY_1_HEALTH: "normal_enemy_1.png",
    Graphic.BOSS_5_HEALTH: "boss_5.png",
    Graphic.BOSS_4_HEALTH: "boss_4.png",
    Graphic.BOSS_3_HEALTH: "boss_3.png",
    Graphic.BOSS_2_HEALTH: "boss_2.png",
    Graphic.BOSS_1_HEALTH: "boss_1.png",
    Graphic.PLAYER_DOWN: "duck_down.png",
    Graphic.PLAYER_UP: "duck_up.png",
    Graphic.PLAYER_LEFT: "duck_left.png",
    Graphic.PLAYER_RIGHT: "duck_right.png",
    Graphic.KEY: "key.png",
    Graphic.SHIELD: "shield.png",
    Graphic.SWORD: "sword.png",
    Graphic.HEALTH_UPGRADE: "health.png",
    Graphic.CONFETTI_CANNON: "confetti_cannon.png",
    Graphic.REMOTE_ITEM: "ap_item.png",
}

TEXTURES = {
    file_name: CoreImage(BytesIO(pkgutil.get_data(__name__, f"../apquest/graphics/{file_name}")), ext="png").texture
    for file_name in IMAGE_GRAPHICS.values()
    if file_name is not None
}
