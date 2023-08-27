from ..tileset import open_tiles


def plot_line(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    error = dx + dy

    yield x0, y0
    while True:
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * error
        if e2 >= dy:
            error = error + dy
            x0 = x0 + sx
            yield x0, y0
        if e2 <= dx:
            error = error + dx
            y0 = y0 + sy
            yield x0, y0

    yield x1, y1


class RoomType:
    def __init__(self, room):
        self.room = room
        room.room_type = self

    def seed(self, wfc, x, y):
        open_points = []
        r = self.room.edge_left.get_open_range()
        if r:
            open_points.append((x + 1, y + (r[0] + r[1]) // 2))
        r = self.room.edge_right.get_open_range()
        if r:
            open_points.append((x + 8, y + (r[0] + r[1]) // 2))
        r = self.room.edge_up.get_open_range()
        if r:
            open_points.append((x + (r[0] + r[1]) // 2, y + 1))
        r = self.room.edge_down.get_open_range()
        if r:
            open_points.append((x + (r[0] + r[1]) // 2, y + 6))
        if len(open_points) < 2:
            return
        mid_x = sum([x for x, y in open_points]) // len(open_points)
        mid_y = sum([y for x, y in open_points]) // len(open_points)

        for x0, y0 in open_points:
            for px, py in plot_line(x0, y0, mid_x, mid_y):
                wfc.cell_data[(px, py)].init_options.intersection_update(open_tiles)
