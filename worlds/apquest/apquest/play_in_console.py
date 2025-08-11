from .events import ConfettiFired

try:
    from pynput import keyboard
    from pynput.keyboard import Key, KeyCode
except ImportError as e:
    raise ImportError("In order to play APQuest from console, you have to install pynput.") from e

from .game import Game
from .graphics import Graphic
from .inputs import Input
from .items import ITEM_TO_GRAPHIC

graphic_to_char = {
    Graphic.EMPTY: " ",
    Graphic.WALL: "W",
    Graphic.BUTTON_NOT_ACTIVATED: "B",
    Graphic.BUTTON_ACTIVATED: "A",
    Graphic.KEY_DOOR: "D",
    Graphic.BUTTON_DOOR: "?",
    Graphic.CHEST: "C",
    Graphic.BUSH: "T",
    Graphic.NORMAL_ENEMY_3_HEALTH: "3",
    Graphic.NORMAL_ENEMY_2_HEATLH: "2",
    Graphic.NORMAL_ENEMY_1_HEALTH: "1",
    Graphic.BOSS_5_HEALTH: "5",
    Graphic.BOSS_4_HEALTH: "4",
    Graphic.BOSS_3_HEALTH: "3",
    Graphic.BOSS_2_HEALTH: "2",
    Graphic.BOSS_1_HEALTH: "1",
    Graphic.PLAYER_DOWN: "v",
    Graphic.PLAYER_UP: "^",
    Graphic.PLAYER_LEFT: "<",
    Graphic.PLAYER_RIGHT: ">",
    Graphic.KEY: "K",
    Graphic.SHIELD: "X",
    Graphic.SWORD: "S",
    Graphic.HEALTH_UPGRADE: "H",
    Graphic.CONFETTI_CANNON: "?",
    Graphic.REMOTE_ITEM: "I",
}


def render_to_text(game: Game) -> str:
    player = game.player
    rendered_graphics = game.render()

    output_string = f"Health: {player.current_health}/{player.max_health}\n"

    inventory = []
    for item, count in player.inventory.items():
        inventory += [graphic_to_char[ITEM_TO_GRAPHIC[item]] for _ in range(count)]
    inventory.sort()

    output_string += f"Inventory: {', '.join(inventory)}\n"

    if player.has_won:
        output_string += "VICTORY!!!\n"

    while game.queued_events:
        next_event = game.queued_events.pop(0)
        if isinstance(next_event, ConfettiFired):
            output_string += "Confetti fired! You feel motivated :)\n"

    for row in rendered_graphics:
        output_string += " ".join(graphic_to_char[graphic] for graphic in row)
        output_string += "\n"

    return output_string


if __name__ == "__main__":
    hard_mode = input("Do you want to play hard mode? (Y/N)").lower().strip() in ("y", "yes")

    game = Game(hard_mode)
    game.gameboard.fill_default_location_content()

    def input_and_rerender(input_key: Input) -> None:
        game.input(input_key)
        print(render_to_text(game))

    def on_press(key: Key | KeyCode | None) -> None:
        if key == keyboard.KeyCode.from_char("w"):
            input_and_rerender(Input.UP)
        if key == keyboard.KeyCode.from_char("s"):
            input_and_rerender(Input.DOWN)
        if key == keyboard.KeyCode.from_char("a"):
            input_and_rerender(Input.LEFT)
        if key == keyboard.KeyCode.from_char("d"):
            input_and_rerender(Input.RIGHT)
        if key == Key.space:
            input_and_rerender(Input.ACTION)
        if key == keyboard.KeyCode.from_char("c"):
            input_and_rerender(Input.CONFETTI)

    print(render_to_text(game))

    with keyboard.Listener(on_press=on_press) as listener:
        while True:
            listener.join()
