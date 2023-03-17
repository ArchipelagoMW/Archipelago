import datetime

from s2clientprotocol import score_pb2 as score_pb

from sc2.position import Point2


class Renderer:

    def __init__(self, client, map_size, minimap_size):
        self._client = client

        self._window = None
        self._map_size = map_size
        self._map_image = None
        self._minimap_size = minimap_size
        self._minimap_image = None
        self._mouse_x, self._mouse_y = None, None
        self._text_supply = None
        self._text_vespene = None
        self._text_minerals = None
        self._text_score = None
        self._text_time = None

    async def render(self, observation):
        render_data = observation.observation.render_data

        map_size = render_data.map.size
        map_data = render_data.map.data
        minimap_size = render_data.minimap.size
        minimap_data = render_data.minimap.data

        map_width, map_height = map_size.x, map_size.y
        map_pitch = -map_width * 3

        minimap_width, minimap_height = minimap_size.x, minimap_size.y
        minimap_pitch = -minimap_width * 3

        if not self._window:
            # pylint: disable=C0415
            from pyglet.image import ImageData
            from pyglet.text import Label
            from pyglet.window import Window

            self._window = Window(width=map_width, height=map_height)
            self._window.on_mouse_press = self._on_mouse_press
            self._window.on_mouse_release = self._on_mouse_release
            self._window.on_mouse_drag = self._on_mouse_drag
            self._map_image = ImageData(map_width, map_height, "RGB", map_data, map_pitch)
            self._minimap_image = ImageData(minimap_width, minimap_height, "RGB", minimap_data, minimap_pitch)
            self._text_supply = Label(
                "",
                font_name="Arial",
                font_size=16,
                anchor_x="right",
                anchor_y="top",
                x=self._map_size[0] - 10,
                y=self._map_size[1] - 10,
                color=(200, 200, 200, 255),
            )
            self._text_vespene = Label(
                "",
                font_name="Arial",
                font_size=16,
                anchor_x="right",
                anchor_y="top",
                x=self._map_size[0] - 130,
                y=self._map_size[1] - 10,
                color=(28, 160, 16, 255),
            )
            self._text_minerals = Label(
                "",
                font_name="Arial",
                font_size=16,
                anchor_x="right",
                anchor_y="top",
                x=self._map_size[0] - 200,
                y=self._map_size[1] - 10,
                color=(68, 140, 255, 255),
            )
            self._text_score = Label(
                "",
                font_name="Arial",
                font_size=16,
                anchor_x="left",
                anchor_y="top",
                x=10,
                y=self._map_size[1] - 10,
                color=(219, 30, 30, 255),
            )
            self._text_time = Label(
                "",
                font_name="Arial",
                font_size=16,
                anchor_x="right",
                anchor_y="bottom",
                x=self._minimap_size[0] - 10,
                y=self._minimap_size[1] + 10,
                color=(255, 255, 255, 255),
            )
        else:
            self._map_image.set_data("RGB", map_pitch, map_data)
            self._minimap_image.set_data("RGB", minimap_pitch, minimap_data)
            self._text_time.text = str(datetime.timedelta(seconds=(observation.observation.game_loop * 0.725) // 16))
            if observation.observation.HasField("player_common"):
                self._text_supply.text = f"{observation.observation.player_common.food_used} / {observation.observation.player_common.food_cap}"
                self._text_vespene.text = str(observation.observation.player_common.vespene)
                self._text_minerals.text = str(observation.observation.player_common.minerals)
            if observation.observation.HasField("score"):
                # pylint: disable=W0212
                self._text_score.text = f"{score_pb._SCORE_SCORETYPE.values_by_number[observation.observation.score.score_type].name} score: {observation.observation.score.score}"

        await self._update_window()

        if self._client.in_game and (not observation.player_result) and self._mouse_x and self._mouse_y:
            await self._client.move_camera_spatial(Point2((self._mouse_x, self._minimap_size[0] - self._mouse_y)))
            self._mouse_x, self._mouse_y = None, None

    async def _update_window(self):
        self._window.switch_to()
        self._window.dispatch_events()

        self._window.clear()

        self._map_image.blit(0, 0)
        self._minimap_image.blit(0, 0)
        self._text_time.draw()
        self._text_score.draw()
        self._text_minerals.draw()
        self._text_vespene.draw()
        self._text_supply.draw()

        self._window.flip()

    def _on_mouse_press(self, x, y, button, _modifiers):
        if button != 1:  # 1: mouse.LEFT
            return
        if x > self._minimap_size[0] or y > self._minimap_size[1]:
            return
        self._mouse_x, self._mouse_y = x, y

    def _on_mouse_release(self, x, y, button, _modifiers):
        if button != 1:  # 1: mouse.LEFT
            return
        if x > self._minimap_size[0] or y > self._minimap_size[1]:
            return
        self._mouse_x, self._mouse_y = x, y

    def _on_mouse_drag(self, x, y, _dx, _dy, buttons, _modifiers):
        if not buttons & 1:  # 1: mouse.LEFT
            return
        if x > self._minimap_size[0] or y > self._minimap_size[1]:
            return
        self._mouse_x, self._mouse_y = x, y
