import heapq
from dataclasses import dataclass

MAX_DISTANCE = 1000000000


@dataclass
class Vertex:
    x: int
    y: int
    euclidean_distance_to_target: float
    distance: int = MAX_DISTANCE
    prev: "Vertex | None" = None

    def __lt__(self, other: "Vertex") -> bool:
        return self.distance < other.distance


def find_path_or_closest(
    traversibility_grid: tuple[tuple[bool, ...], ...], source_x: int, source_y: int, target_x: int, target_y: int
) -> list[tuple[int, int]]:
    vertex_grid = [
        [Vertex(x, y, (x - target_x) ** 2 + (y - target_y) ** 2) for x in range(len(traversibility_grid[0]))]
        for y in range(len(traversibility_grid))
    ]
    vertex_grid[source_y][source_x].distance = 0

    vertices = [vertex for row in vertex_grid for vertex in row]

    heapq.heapify(vertices)

    while vertices:
        vertex = heapq.heappop(vertices)

        if vertex.distance == MAX_DISTANCE:
            break

        for neighbor_x, neighbor_y in (
            (vertex.x + 1, vertex.y),
            (vertex.x - 1, vertex.y),
            (vertex.x, vertex.y + 1),
            (vertex.x, vertex.y - 1),
        ):
            if neighbor_x < 0:
                continue
            if neighbor_y < 0:
                continue
            if neighbor_x >= len(traversibility_grid[0]):
                continue
            if neighbor_y >= len(traversibility_grid):
                continue

            if not traversibility_grid[neighbor_y][neighbor_x]:
                continue

            other_vertex = vertex_grid[neighbor_y][neighbor_x]

            new_distance = vertex.distance + 1

            if new_distance < other_vertex.distance:
                other_vertex.distance = new_distance
                other_vertex.prev = vertex

            heapq.heapify(vertices)

    closest_vertex = min(
        (vertex for row in vertex_grid for vertex in row if vertex.distance < MAX_DISTANCE),
        key=lambda vertex: (vertex.euclidean_distance_to_target, vertex.distance),
    )

    path: list[tuple[int, int]] = []

    while closest_vertex.prev is not None:
        path.append((closest_vertex.x, closest_vertex.y))

        closest_vertex = closest_vertex.prev

    path.append((source_x, source_y))
    path.reverse()

    return path
