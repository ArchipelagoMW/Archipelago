from __future__ import annotations

# isort: off
from kvui import GameManager, MDNavigationItemBase

# isort: on
from typing import TYPE_CHECKING, Any

from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.layout import Layout
from kivymd.uix.recycleview import MDRecycleView

from ..game.game import Game
from .custom_views import APQuestControlsView, APQuestGameView, APQuestGrid, ConfettiView, VolumeSliderView
from .graphics import PlayerSprite, get_texture
from .sounds import SoundManager

if TYPE_CHECKING:
    from .ap_quest_client import APQuestContext


class APQuestManager(GameManager):
    base_title = "APQuest for AP version"
    ctx: APQuestContext

    lower_game_grid: GridLayout
    upper_game_grid: GridLayout

    game_view: MDRecycleView
    game_view_tab: MDNavigationItemBase

    sound_manager: SoundManager

    bottom_image_grid: list[list[Image]]
    top_image_grid: list[list[Image]]
    confetti_view: ConfettiView

    bottom_grid_is_grass: bool

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.sound_manager = SoundManager()
        self.sound_manager.allow_intro_to_play = not self.ctx.delay_intro_song
        self.top_image_grid = []
        self.bottom_image_grid = []
        self.bottom_grid_is_grass = False

    def allow_intro_song(self) -> None:
        self.sound_manager.allow_intro_to_play = True

    def add_confetti(self, position: tuple[float, float], amount: int) -> None:
        self.confetti_view.add_confetti(position, amount)

    def play_jingle(self, audio_filename: str) -> None:
        self.sound_manager.play_jingle(audio_filename)

    def switch_to_tab(self, desired_tab: MDNavigationItemBase) -> None:
        if self.screens.current_tab == desired_tab:
            return
        self.screens.current_tab.active = False
        self.screens.switch_screens(desired_tab)
        desired_tab.active = True

    def switch_to_game_tab(self) -> None:
        self.switch_to_tab(self.game_view_tab)

    def switch_to_regular_tab(self) -> None:
        self.switch_to_tab(self.tabs.children[-1])

    def game_started(self) -> None:
        self.switch_to_game_tab()
        self.sound_manager.game_started = True

    def render(self, game: Game, player_sprite: PlayerSprite) -> None:
        self.setup_game_grid_if_not_setup(game.gameboard.size)

        # This calls game.render(), which needs to happen to update the state of math traps
        self.render_gameboard(game, player_sprite)
        # Only now can we check whether a math problem is active
        self.render_background_game_grid(game.gameboard.size, game.active_math_problem is None)
        self.sound_manager.math_trap_active = game.active_math_problem is not None

        self.render_item_column(game)

    def render_gameboard(self, game: Game, player_sprite: PlayerSprite) -> None:
        rendered_gameboard = game.render()

        for gameboard_row, image_row in zip(rendered_gameboard, self.top_image_grid, strict=False):
            for graphic, image in zip(gameboard_row, image_row[:11], strict=False):
                texture = get_texture(graphic, player_sprite)

                if texture is None:
                    image.opacity = 0
                    image.texture = None
                    continue

                image.texture = texture
                image.opacity = 1

    def render_item_column(self, game: Game) -> None:
        rendered_item_column = game.render_health_and_inventory(vertical=True)
        for item_graphic, image_row in zip(rendered_item_column, self.top_image_grid, strict=False):
            image = image_row[-1]

            texture = get_texture(item_graphic)
            if texture is None:
                image.opacity = 0
                image.texture = None
                continue

            image.texture = texture
            image.opacity = 1

    def render_background_game_grid(self, size: tuple[int, int], grass: bool) -> None:
        if grass == self.bottom_grid_is_grass:
            return

        for row in range(size[1]):
            for column in range(size[0]):
                image = self.bottom_image_grid[row][column]

                if not grass:
                    image.color = (0.3, 0.3, 0.3)
                    image.texture = None
                    continue

                boss_room = (row in (0, 1, 2) and (size[1] - column) in (1, 2, 3)) or (row, column) == (3, size[1] - 2)
                if boss_room:
                    image.color = (0.45, 0.35, 0.1)
                    image.texture = None
                    continue
                image.texture = get_texture("Grass")
                image.color = (1.0, 1.0, 1.0)

        self.bottom_grid_is_grass = grass

    def setup_game_grid_if_not_setup(self, size: tuple[int, int]) -> None:
        if self.upper_game_grid.children:
            return

        self.top_image_grid = []
        self.bottom_image_grid = []

        for _row in range(size[1]):
            self.top_image_grid.append([])
            self.bottom_image_grid.append([])

            for _column in range(size[0]):
                bottom_image = Image(fit_mode="fill", color=(0.3, 0.3, 0.3))
                self.lower_game_grid.add_widget(bottom_image)
                self.bottom_image_grid[-1].append(bottom_image)

                top_image = Image(fit_mode="fill")
                self.upper_game_grid.add_widget(top_image)
                self.top_image_grid[-1].append(top_image)

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

        controls = APQuestControlsView()

        self.add_client_tab("Controls", controls)

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

        volume_slider_container = VolumeSliderView()
        volume_slider = volume_slider_container.ids["volume_slider"]
        volume_slider.value = self.sound_manager.volume_percentage
        volume_slider.bind(value=lambda _, new_volume: self.sound_manager.set_volume_percentage(new_volume))

        self.grid.add_widget(volume_slider_container, index=3)

        Clock.schedule_interval(lambda dt: self.confetti_view.redraw_confetti(dt), 1 / 60)

        return container
