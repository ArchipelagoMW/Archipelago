from ..graphics.bgr15 import BGR15

class Palette:
    def __init__(self, data = None):
        self.colors = []
        if data is not None:
            self.data = data

    def __len__(self):
        return len(self.colors)

    def __getitem__(self, index):
        return self.colors[index]

    def __setitem__(self, index, color):
        self.colors[index] = color

    def append(self, data):
        self.colors.append(BGR15(data))

    def append_rgb(self, data):
        self.colors.append(BGR15())
        self.colors[-1].rgb = data

    def _get_data(self, data_size, data_getter):
        data = [0x00] * len(self) * data_size
        for color_index, color in enumerate(self.colors):
            data_index = color_index * data_size
            data[data_index : data_index + data_size] = data_getter(color)
        return data

    def _set_data(self, new_data, data_size, data_setter):
        color_count = len(new_data) // data_size
        self.colors = [BGR15() for instance in range(color_count)]

        for color_index, color in enumerate(self.colors):
            data_index = color_index * data_size
            color_data = new_data[data_index : data_index + data_size]
            data_setter.fset(self.colors[color_index], color_data)

    @property
    def data(self):
        return self._get_data(BGR15.DATA_SIZE, lambda color : color.data)

    @data.setter
    def data(self, new_data):
        self._set_data(new_data, BGR15.DATA_SIZE, BGR15.data)

    @property
    def rgb_data(self):
        RGB_DATA_SIZE = 3
        return self._get_data(RGB_DATA_SIZE, lambda color : color.rgb)

    @rgb_data.setter
    def rgb_data(self, new_data):
        RGB_DATA_SIZE = 3
        self._set_data(new_data, RGB_DATA_SIZE, BGR15.rgb)

    @property
    def alpha_rgb_data(self):
        return self.colors[0].rgb

    @alpha_rgb_data.setter
    def alpha_rgb_data(self, rgb):
        self.colors[0].rgb = rgb

    def write_ppm(self, output_file):
        OUTPUT_WIDTH = len(self)
        OUTPUT_HEIGHT = 1
        BITS_PER_VALUE = 8

        from ..graphics.ppm import write_ppm6
        write_ppm6(OUTPUT_WIDTH, OUTPUT_HEIGHT, BITS_PER_VALUE, self.rgb_data, output_file)

    def __repr__(self):
        result = ""
        for color_index in range(len(self)):
            result += f"{repr(self.colors[color_index])}\n"
        return result[:-1]

    def __str__(self):
        result = ""
        for color_index in range(len(self)):
            result += f"{color_index:>2}: {str(self.colors[color_index])}\n"
        return result[:-1]
