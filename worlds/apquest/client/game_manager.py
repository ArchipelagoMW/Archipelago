# isort: off
from kivy.clock import Clock

from kvui import GameManager, MDNavigationItemBase
# isort: on

from typing import TYPE_CHECKING

from CommonClient import logger
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.layout import Layout
from kivymd.uix.recycleview import MDRecycleView

from ..apquest.game import Game
from ..apquest.graphics import Graphic
from .custom_views import APQuestGameView, APQuestGrid, ConfettiView
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
    confetti_view: ConfettiView

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sound_manager = SoundManager()
        self.sound_manager.allow_intro_to_play = not self.ctx.delay_intro_song
        self.top_image_grid = []
        self.bottom_image_grid = []

    def allow_intro_song(self):
        self.sound_manager.allow_intro_to_play = True

    def add_confetti(self, position: tuple[float, float], amount: int):
        self.confetti_view.add_confetti(position, amount)

    def play_jingle(self, audio_filename: str) -> None:
        self.sound_manager.play_jingle(audio_filename)

    def switch_to_game_tab(self) -> None:
        if self.screens.current_tab == self.game_view_tab:
            return
        self.screens.current_tab.active = False
        self.screens.switch_screens(self.game_view_tab)
        self.game_view_tab.active = True

    def game_started(self) -> None:
        self.switch_to_game_tab()
        self.sound_manager.game_started = True

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

        self.game_view = APQuestGameView(self.ctx.input_and_rerender)

        self.game_view_tab = self.add_client_tab("APQuest", self.game_view)

        game_container = self.game_view.ids["game_container"]
        self.lower_game_grid = APQuestGrid()
        self.upper_game_grid = APQuestGrid()
        self.confetti_view = ConfettiView()
        game_container.add_widget(self.lower_game_grid)
        game_container.add_widget(self.upper_game_grid)
        game_container.add_widget(self.confetti_view)

        game_container.bind(size=self.lower_game_grid.check_resize)
        game_container.bind(size=self.upper_game_grid.check_resize)
        game_container.bind(size=self.confetti_view.check_resize)

        Clock.schedule_interval(lambda dt: self.confetti_view.redraw_confetti(dt), 1 / 60)

        return container
