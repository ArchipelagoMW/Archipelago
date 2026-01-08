class MenuCharacterSprite:
    class MenuOAMSprite:
        DATA_SIZE = 4

        def __init__(self, data):
            self.x_position      = data[0]
            self.y_position      = data[1]
            self.start_tile      = data[2] | ((data[3] & 0x01) << 8)
            self.palette         = (data[3] & 0x0e) >> 1
            self.priority_layer  = (data[3] & 0x30) >> 4
            self.horizontal_flip = (data[3] & 0x40) >> 6
            self.vertical_flip   = (data[3] & 0x80) >> 7

        def data(self):
            data = [0x00] * self.DATA_SIZE

            data[0]     = self.x_position
            data[1]     = self.y_position
            data[2]     = self.start_tile & 0xff
            data[3]     = (self.start_tile & 0x100) >> 8
            data[3]    |= self.palette          << 1
            data[3]    |= self.priority_layer   << 4
            data[3]    |= self.horizontal_flip  << 6
            data[3]    |= self.vertical_flip    << 7

            return data

    def __init__(self, id, data):
        self.id = id
        self.size = data[0]

        # sprites are broken up into a top and bottom half for menus
        self.sprites = []
        for index in range(self.size):
            data_start = 1 + index * self.MenuOAMSprite.DATA_SIZE
            self.sprites.append(self.MenuOAMSprite(data[data_start : data_start + self.MenuOAMSprite.DATA_SIZE]))

    def set_palette(self, new_palette):
        # menu palettes: 0 = config menu? unused?, 1 = grayscale, 2-5 = 0-7 but last 4 colors invalid
        for sprite in self.sprites:
            sprite.palette = new_palette

    def oam_data(self):
        data = []

        data.append(self.size)
        for sprite in self.sprites:
            data.extend(sprite.data())

        return data
