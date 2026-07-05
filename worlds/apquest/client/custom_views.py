from collections.abc import Callable
from dataclasses import dataclass
from math import sqrt
from random import choice, random
from typing import Any

from kivy.core.window import Keyboard, Window
from kivy.graphics import Color, Triangle
from kivy.graphics.instructions import Canvas
from kivy.input import MotionEvent
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.recycleview import MDRecycleView

from CommonClient import logger

from ..game.inputs import Input


INPUT_MAP = {
    "up": Input.UP,
    "w": Input.UP,
    "down": Input.DOWN,
    "s": Input.DOWN,
    "right": Input.RIGHT,
    "d": Input.RIGHT,
    "left": Input.LEFT,
    "a": Input.LEFT,
    "spacebar": Input.ACTION,
    "c": Input.CONFETTI,
    "0": Input.ZERO,
    "1": Input.ONE,
    "2": Input.TWO,
    "3": Input.THREE,
    "4": Input.FOUR,
    "5": Input.FIVE,
    "6": Input.SIX,
    "7": Input.SEVEN,
    "8": Input.EIGHT,
    "9": Input.NINE,
    "backspace": Input.BACKSPACE,
}


class APQuestGameView(MDRecycleView):
    _keyboard: Keyboard | None = None
    input_function: Callable[[Input], None]

    def __init__(self, input_function: Callable[[Input], None], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.input_function = input_function
        self.bind_keyboard()

    def on_touch_down(self, touch: MotionEvent) -> None:
        self.bind_keyboard()

    def bind_keyboard(self) -> None:
        if self._keyboard is not None:
            return
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self) -> None:
        if self._keyboard is None:
            return
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, _: Any, keycode: tuple[int, str], _1: Any, _2: Any) -> bool:
        if keycode[1] in INPUT_MAP:
            self.input_function(INPUT_MAP[keycode[1]])
        return True


class APQuestGrid(GridLayout):
    def check_resize(self, _: int, _1: int) -> None:
        parent_width, parent_height = self.parent.size

        self_width_according_to_parent_height = parent_height * 12 / 11
        self_height_according_to_parent_width = parent_height * 11 / 12

        if self_width_according_to_parent_height > parent_width:
            self.size = parent_width, self_height_according_to_parent_width
        else:
            self.size = self_width_according_to_parent_height, parent_height


CONFETTI_COLORS = [
    (220 / 255, 0, 212 / 255),  # PINK
    (0, 0, 252 / 255),  # BLUE
    (252 / 255, 220 / 255, 0),  # YELLOW
    (0, 184 / 255, 0),  # GREEN
    (252 / 255, 56 / 255, 0),  # ORANGE
]


@dataclass
class Confetti:
    x_pos: float
    y_pos: float
    x_speed: float
    y_speed: float
    color: tuple[float, float, float]
    life: float = 3

    triangle1: Triangle | None = None
    triangle2: Triangle | None = None
    color_instruction: Color | None = None

    def update_speed(self, dt: float) -> None:
        if self.x_speed > 0:
            self.x_speed -= 2.7 * dt
            if self.x_speed < 0:
                self.x_speed = 0
        else:
            self.x_speed += 2.7 * dt
            if self.x_speed > 0:
                self.x_speed = 0

        if self.y_speed > -0.03:
            self.y_speed -= 2.7 * dt
            if self.y_speed < -0.03:
                self.y_speed = -0.03
        else:
            self.y_speed += 2.7 * dt
            if self.y_speed > -0.03:
                self.y_speed = -0.03

    def move(self, dt: float) -> None:
        self.update_speed(dt)

        if self.y_pos > 1:
            self.y_pos = 1
            self.y_speed = 0
        if self.x_pos < 0.01:
            self.x_pos = 0.01
            self.x_speed = 0
        if self.x_pos > 0.99:
            self.x_pos = 0.99
            self.x_speed = 0

        self.x_pos += self.x_speed * dt
        self.y_pos += self.y_speed * dt

    def render(self, offset_x: float, offset_y: float, max_x: int, max_y: int) -> None:
        if self.x_speed == 0 and self.y_speed == 0:
            x_normalized, y_normalized = 0.0, 1.0
        else:
            speed_magnitude = sqrt(self.x_speed**2 + self.y_speed**2)
            x_normalized, y_normalized = self.x_speed / speed_magnitude, self.y_speed / speed_magnitude

        half_top_to_bottom = 0.006
        half_left_to_right = 0.018

        upwards_delta_x = x_normalized * half_top_to_bottom
        upwards_delta_y = y_normalized * half_top_to_bottom
        sideways_delta_x = y_normalized * half_left_to_right
        sideways_delta_y = x_normalized * half_left_to_right

        top_left_x, top_left_y = upwards_delta_x - sideways_delta_x, upwards_delta_y + sideways_delta_y
        bottom_left_x, bottom_left_y = -upwards_delta_x - sideways_delta_x, -upwards_delta_y + sideways_delta_y
        top_right_x, top_right_y = -bottom_left_x, -bottom_left_y
        bottom_right_x, bottom_right_y = -top_left_x, -top_left_y

        top_left_x, top_left_y = top_left_x + self.x_pos, top_left_y + self.y_pos
        bottom_left_x, bottom_left_y = bottom_left_x + self.x_pos, bottom_left_y + self.y_pos
        top_right_x, top_right_y = top_right_x + self.x_pos, top_right_y + self.y_pos
        bottom_right_x, bottom_right_y = bottom_right_x + self.x_pos, bottom_right_y + self.y_pos

        top_left_x, top_left_y = top_left_x * max_x + offset_x, top_left_y * max_y + offset_y
        bottom_left_x, bottom_left_y = bottom_left_x * max_x + offset_x, bottom_left_y * max_y + offset_y
        top_right_x, top_right_y = top_right_x * max_x + offset_x, top_right_y * max_y + offset_y
        bottom_right_x, bottom_right_y = bottom_right_x * max_x + offset_x, bottom_right_y * max_y + offset_y

        points1 = (top_left_x, top_left_y, top_right_x, top_right_y, bottom_left_x, bottom_left_y)
        points2 = (bottom_right_x, bottom_right_y, top_right_x, top_right_y, bottom_left_x, bottom_left_y)

        if self.color_instruction is None:
            self.color_instruction = Color(*self.color)

        if self.triangle1 is None:
            self.triangle1 = Triangle(points=points1)
        else:
            self.triangle1.points = points1

        if self.triangle2 is None:
            self.triangle2 = Triangle(points=points2)
        else:
            self.triangle2.points = points2

    def reduce_life(self, dt: float, canvas: Canvas) -> bool:
        self.life -= dt

        if self.life <= 0:
            if self.color_instruction is not None:
                canvas.remove(self.color_instruction)
            if self.triangle1 is not None:
                canvas.remove(self.triangle1)
            if self.triangle2 is not None:
                canvas.remove(self.triangle2)
            return False

        return True


class ConfettiView(MDRecycleView):
    confetti: list[Confetti]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.confetti = []

    def check_resize(self, _: int, _1: int) -> None:
        parent_width, parent_height = self.parent.size

        self_width_according_to_parent_height = parent_height * 12 / 11
        self_height_according_to_parent_width = parent_height * 11 / 12

        if self_width_according_to_parent_height > parent_width:
            self.size = parent_width, self_height_according_to_parent_width
        else:
            self.size = self_width_according_to_parent_height, parent_height

    def redraw_confetti(self, dt: float) -> None:
        try:
            with self.canvas:
                for confetti in self.confetti:
                    confetti.move(dt)

                self.confetti = [confetti for confetti in self.confetti if confetti.reduce_life(dt, self.canvas)]

                for confetti in self.confetti:
                    confetti.render(self.pos[0], self.pos[1], self.size[0], self.size[1])
        except Exception as e:
            logger.exception(e)

    def add_confetti(self, initial_position: tuple[float, float], amount: int) -> None:
        for i in range(amount):
            self.confetti.append(
                Confetti(
                    initial_position[0],
                    initial_position[1],
                    random() * 3.2 - 1.6 - (initial_position[0] - 0.5) * 1.2,
                    random() * 3.2 - 1.3 - (initial_position[1] - 0.5) * 1.2,
                    choice(CONFETTI_COLORS),
                    3 + i * 0.05,
                )
            )


class VolumeSliderView(BoxLayout):
    pass


class APQuestControlsView(BoxLayout):
    pass
