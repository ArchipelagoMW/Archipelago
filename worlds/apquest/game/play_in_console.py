from .events import ConfettiFired, MathProblemSolved

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
    Graphic.BREAKABLE_BLOCK: "~",
    Graphic.NORMAL_ENEMY_2_HEALTH: "2",
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
    Graphic.HAMMER: "H",
    Graphic.HEART: "♡",
    Graphic.CONFETTI_CANNON: "?",
    Graphic.REMOTE_ITEM: "I",
    Graphic.UNKNOWN: "ß",
    Graphic.ZERO: "0",
    Graphic.ONE: "1",
    Graphic.TWO: "2",
    Graphic.THREE: "3",
    Graphic.FOUR: "4",
    Graphic.FIVE: "5",
    Graphic.SIX: "6",
    Graphic.SEVEN: "7",
    Graphic.EIGHT: "8",
    Graphic.NINE: "9",
    Graphic.PLUS: "+",
    Graphic.MINUS: "-",
    Graphic.TIMES: "x",
    Graphic.DIVIDE: "/",
    Graphic.LETTER_A: "A",
    Graphic.LETTER_E: "E",
    Graphic.LETTER_H: "H",
    Graphic.LETTER_I: "I",
    Graphic.LETTER_M: "M",
    Graphic.LETTER_T: "T",
    Graphic.EQUALS: "=",
    Graphic.NO: "X",
}

KEY_CONVERSION = {
    keyboard.KeyCode.from_char("w"): Input.UP,
    Key.up: Input.UP,
    keyboard.KeyCode.from_char("s"): Input.DOWN,
    Key.down: Input.DOWN,
    keyboard.KeyCode.from_char("a"): Input.LEFT,
    Key.left: Input.LEFT,
    keyboard.KeyCode.from_char("d"): Input.RIGHT,
    Key.right: Input.RIGHT,
    Key.space: Input.ACTION,
    keyboard.KeyCode.from_char("c"): Input.CONFETTI,
    keyboard.KeyCode.from_char("0"): Input.ZERO,
    keyboard.KeyCode.from_char("1"): Input.ONE,
    keyboard.KeyCode.from_char("2"): Input.TWO,
    keyboard.KeyCode.from_char("3"): Input.THREE,
    keyboard.KeyCode.from_char("4"): Input.FOUR,
    keyboard.KeyCode.from_char("5"): Input.FIVE,
    keyboard.KeyCode.from_char("6"): Input.SIX,
    keyboard.KeyCode.from_char("7"): Input.SEVEN,
    keyboard.KeyCode.from_char("8"): Input.EIGHT,
    keyboard.KeyCode.from_char("9"): Input.NINE,
    Key.backspace: Input.BACKSPACE,
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
        if isinstance(next_event, MathProblemSolved):
            output_string += "Math problem solved!\n"

    for row in rendered_graphics:
        output_string += " ".join(graphic_to_char[graphic] for graphic in row)
        output_string += "\n"

    return output_string


if __name__ == "__main__":
    hard_mode = input("Do you want to play hard mode? (Y/N)").lower().strip() in ("y", "yes")
    hammer_exists = input("Do you want the hammer to exist in the game? (Y/N)").lower().strip() in ("y", "yes")
    extra_chest = input("Do you want the extra starting chest to exist in the game?").lower().strip() in ("y", "yes")
    math_trap_percentage = int(input("What should the percentage of math traps be?"))

    game = Game(hard_mode, hammer_exists, extra_chest)
    game.gameboard.fill_default_location_content(math_trap_percentage)

    def input_and_rerender(input_key: Input) -> None:
        game.input(input_key)
        print(render_to_text(game))

    def on_press(key: Key | KeyCode | None) -> None:
        if key in KEY_CONVERSION:
            input_and_rerender(KEY_CONVERSION[key])

    print(render_to_text(game))

    with keyboard.Listener(on_press=on_press) as listener:
        while True:
            listener.join()
