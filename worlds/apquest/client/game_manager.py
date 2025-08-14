# isort: off
from kivy.input import MotionEvent

from kvui import GameManager, MDNavigationItemBase
# isort: on

from typing import TYPE_CHECKING

from CommonClient import logger
from kivy.core.window import Keyboard, Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.layout import Layout
from kivymd.uix.recycleview import MDRecycleView

from ..apquest.game import Game
from ..apquest.graphics import Graphic
from ..apquest.inputs import Input
from .graphics import IMAGE_GRAPHICS, PLAYER_GRAPHICS, TEXTURES, PlayerSprite
from .sounds import SoundManager

if TYPE_CHECKING:
    from .ap_quest_client import APQuestContext


class APQuestManager(GameManager):
    base_title = "APQuest for AP version"
    ctx: "APQuestContext"

    lower_game_grid: GridLayout
    upper_game_grid: GridLayout

    game_view: MDRecycleView
    game_view_tab: MDNavigationItemBase

    sound_manager: SoundManager

    bottom_image_grid: list[list[Image]]
    top_image_grid: list[list[Image]]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sound_manager = SoundManager()
        self.top_image_grid = []
        self.bottom_image_grid = []

    def play_jingle(self, audio_filename: str) -> None:
        self.sound_manager.play_jingle(audio_filename)

    def switch_to_game_tab(self) -> None:
        if self.screens.current_tab == self.game_view_tab:
            return
        self.screens.current_tab.active = False
        self.screens.switch_screens(self.game_view_tab)
        self.game_view_tab.active = True

    def start_background_music(self) -> None:
        self.sound_manager.start_background_music()

    def render(self, game: Game, player_sprite: PlayerSprite) -> None:
        self.setup_game_grid_if_not_setup(game.gameboard.size)
        self.render_gameboard(game, player_sprite)
        self.render_item_column(game)

    def render_gameboard(self, game: Game, player_sprite: PlayerSprite) -> None:
        rendered_gameboard = game.render()

        for gameboard_row, image_row in zip(rendered_gameboard, self.top_image_grid, strict=False):
            for graphic, image in zip(gameboard_row, image_row[:11], strict=False):
                if graphic in PLAYER_GRAPHICS:
                    image_name = PLAYER_GRAPHICS[graphic].get(player_sprite, IMAGE_GRAPHICS[Graphic.UNKNOWN])
                    if image_name is None:
                        logger.exception(f"Couldn't find player sprite graphics for player sprite {player_sprite}")
                else:
                    image_name = IMAGE_GRAPHICS[graphic]

                if image_name is None:
                    image.opacity = 0
                    image.texture = None
                    continue

                image.texture = TEXTURES.get(image_name, TEXTURES[IMAGE_GRAPHICS[Graphic.UNKNOWN]])
                image.texture.mag_filter = "nearest"
                image.opacity = 1

    def render_item_column(self, game: Game) -> None:
        rendered_item_column = game.render_health_and_inventory(vertical=True)
        for item_graphic, image_row in zip(rendered_item_column, self.top_image_grid, strict=False):
            image = image_row[-1]
            image_name = IMAGE_GRAPHICS[item_graphic]
            if image_name is None:
                image.opacity = 0
                image.texture = None
                continue

            image.texture = TEXTURES.get(image_name, TEXTURES[IMAGE_GRAPHICS[Graphic.UNKNOWN]])
            image.texture.mag_filter = "nearest"
            image.opacity = 1

    def setup_game_grid_if_not_setup(self, size: tuple[int, int]) -> None:
        if self.upper_game_grid.children:
            return

        self.top_image_grid = []

        for row in range(size[1]):
            self.top_image_grid.append([])
            for column in range(size[0]):
                boss_room = (row in (0, 1, 2) and (size[1] - column) in (1, 2, 3)) or (row, column) == (3, size[1] - 2)

                if boss_room:
                    # "boss room"
                    image = Image(fit_mode="fill", color=(0.45, 0.35, 0.1))
                else:
                    image = Image(fit_mode="fill", texture=TEXTURES["grass.png"])
                    image.texture.mag_filter = "nearest"
                self.lower_game_grid.add_widget(image)

                image2 = Image(fit_mode="fill")

                self.upper_game_grid.add_widget(image2)

                self.top_image_grid[-1].append(image2)

            # Right side: Inventory
            image = Image(fit_mode="fill", color=(0.3, 0.3, 0.3))
            self.lower_game_grid.add_widget(image)

            image2 = Image(fit_mode="fill", opacity=0)
            self.upper_game_grid.add_widget(image2)

            self.top_image_grid[-1].append(image2)

    def build(self) -> Layout:
        container = super().build()

        input_and_rerender = self.ctx.input_and_rerender

        class APQuestGameView(MDRecycleView):
            _keyboard: Keyboard | None = None

            def __init__(self, **kwargs) -> None:
                super().__init__(**kwargs)
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

            def _on_keyboard_down(self, _, keycode, _1, _2) -> bool:
                if keycode[1] == "up":
                    input_and_rerender(Input.UP)
                elif keycode[1] == "down":
                    input_and_rerender(Input.DOWN)
                elif keycode[1] == "left":
                    input_and_rerender(Input.LEFT)
                elif keycode[1] == "right":
                    input_and_rerender(Input.RIGHT)
                elif keycode[1] == "spacebar":
                    input_and_rerender(Input.ACTION)
                elif keycode[1] == "c":
                    input_and_rerender(Input.CONFETTI)
                return True

        class APQuestGrid(GridLayout):
            def __init__(self, **kwargs) -> None:
                super().__init__(**kwargs)

            def check_resize(self, _: int, _1: int) -> None:
                parent_width, parent_height = self.parent.size

                self_width_according_to_parent_height = parent_height * 12 / 11
                self_height_according_to_parent_width = parent_height * 11 / 12

                if self_width_according_to_parent_height > parent_width:
                    self.size = parent_width, self_height_according_to_parent_width
                else:
                    self.size = self_width_according_to_parent_height, parent_height

        self.game_view = APQuestGameView()

        self.game_view_tab = self.add_client_tab("APQuest", self.game_view)

        game_container = self.game_view.ids["game_container"]
        self.lower_game_grid = APQuestGrid()
        self.upper_game_grid = APQuestGrid()
        game_container.add_widget(self.lower_game_grid)
        game_container.add_widget(self.upper_game_grid)

        game_container.bind(size=self.lower_game_grid.check_resize)
        game_container.bind(size=self.upper_game_grid.check_resize)

        return container
