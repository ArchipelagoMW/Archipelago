from events import ConfettiFired

try:
    from pynput import keyboard
    from pynput.keyboard import Key, KeyCode
except ImportError:
    raise ImportError("In order to play APQuest from console, you have to install pynput.")

from game import Game, Input
from graphics import Graphic
from items import ITEM_TO_GRAPHIC

graphic_to_char = {
    Graphic.EMPTY: " ",
    Graphic.WALL: "W",
    Graphic.BUTTON_NOT_ACTIVATED: "B",
    Graphic.BUTTON_ACTIVATED: "A",
    Graphic.KEY_DOOR: "D",
    Graphic.BUTTON_DOOR: "?",
    Graphic.CHEST: "C",
    Graphic.BUSH: "T",
    Graphic.NORMAL_ENEMY: "E",
    Graphic.BOSS: "F",
    Graphic.PLAYER_DOWN: "v",
    Graphic.PLAYER_UP: "^",
    Graphic.PLAYER_LEFT: "<",
    Graphic.PLAYER_RIGHT: ">",
    Graphic.KEY: "K",
    Graphic.SHIELD: "X",
    Graphic.SWORD: "S",
    Graphic.HEALTH_UPGRADE: "H",
    Graphic.CONFETTI_CANNON: "?"
}


def render_to_console(game: Game) -> None:
    player = game.player
    rendered_graphics = game.render()

    print(f"Health: {player.current_health}/{player.max_health}")

    inventory = []
    for item, count in player.inventory.items():
        for _ in range(count):
            inventory.append(graphic_to_char[ITEM_TO_GRAPHIC[item]])
    inventory.sort()

    print(f"Inventory: {', '.join(inventory)}")

    if player.has_won:
        print("VICTORY!!!")

    while game.queued_events:
        next_event = game.queued_events.pop(0)
        if isinstance(next_event, ConfettiFired):
            print("Confetti fired! You feel motivated :)")

    for row in rendered_graphics:
        print(" ".join(graphic_to_char[graphic] for graphic in row))


if __name__ == "__main__":
    game = Game()
    game.gameboard.fill_default_location_content()

    def input_and_rerender(input_key: Input) -> None:
        game.input(input_key)
        render_to_console(game)

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

    render_to_console(game)

    with keyboard.Listener(on_press=on_press) as listener:
        while True:
            listener.join()
