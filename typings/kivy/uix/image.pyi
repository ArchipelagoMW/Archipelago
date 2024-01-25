import io

from kivy.graphics.texture import Texture


class CoreImage:
    texture: Texture

    def __init__(self, data: io.BytesIO, ext: str) -> None: ...
