# BGR15 color, 0bbb bbgg gggr rrrr
class BGR15:
    DATA_SIZE = 2

    R_MASK = 0x001f
    G_MASK = 0x03e0
    B_MASK = 0x7c00

    def __init__(self, data = None):
        if data is None:
            data = [0x00] * self.DATA_SIZE
        self.data = data

    @property
    def data(self):
        return list(self.bgr15.to_bytes(self.DATA_SIZE, "little"))

    @data.setter
    def data(self, new_data):
        self.bgr15 = int.from_bytes(bytes(new_data), "little")

    @property
    def bgr15(self):
        return self._bgr15

    @bgr15.setter
    def bgr15(self, new_bgr15):
        self._bgr15 = new_bgr15

        self._red   = ((self._bgr15 & self.R_MASK) >> 0) * 8
        self._green = ((self._bgr15 & self.G_MASK) >> 5) * 8
        self._blue  = ((self._bgr15 & self.B_MASK) >> 10) * 8

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, new_red):
        self._red = new_red
        self._bgr15 = (self._bgr15 & (~self.R_MASK)) | ((new_red // 8) << 0)

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, new_green):
        self._green = new_green
        self._bgr15 = (self._bgr15 & (~self.G_MASK)) | ((new_green // 8) << 5)

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, new_blue):
        self._blue = new_blue
        self._bgr15 = (self._bgr15 & (~self.B_MASK)) | ((new_blue // 8) << 10)

    @property
    def rgb(self):
        return [self._red, self._green, self._blue]

    @rgb.setter
    def rgb(self, new_rgb):
        self.red   = new_rgb[0]
        self.green = new_rgb[1]
        self.blue  = new_rgb[2]

    def __repr__(self):
        return f"0x{hex(self.bgr15)[2:].zfill(4)}: {str(self)}"

    def __str__(self):
        return f"r: {self.red:<2}, g: {self.green:<2}, b: {self.blue:<2}"
