import heapq
from typing import Generator

Point = tuple[int, int]


def heuristic(a: Point, b: Point) -> int:
    # Manhattan distance (good for 4-directional grids)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from: dict[Point, Point], current: Point) -> list[Point]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def find_path_or_closest(
    grid: tuple[tuple[bool, ...], ...], source_x: int, source_y: int, target_x: int, target_y: int
) -> list[Point]:
    start = source_x, source_y
    goal = target_x, target_y

    rows, cols = len(grid), len(grid[0])

    def in_bounds(p: Point) -> bool:
        return 0 <= p[0] < rows and 0 <= p[1] < cols

    def passable(p: Point) -> bool:
        return grid[p[1]][p[0]]

    def neighbors(p: Point) -> Generator[Point, None, None]:
        x, y = p
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            np = (x + dx, y + dy)
            if in_bounds(np) and passable(np):
                yield np

    open_heap: list[tuple[int, tuple[int, int]]] = []
    heapq.heappush(open_heap, (0, start))

    came_from: dict[Point, Point] = {}
    g_score = {start: 0}

    # Track best fallback node
    best_node = start
    best_dist = heuristic(start, goal)

    visited = set()

    while open_heap:
        _, current = heapq.heappop(open_heap)

        if current in visited:
            continue
        visited.add(current)

        # Check if we reached the goal
        if current == goal:
            return reconstruct_path(came_from, current)

        # Update "closest node" fallback
        dist = heuristic(current, goal)
        if dist < best_dist or (dist == best_dist and g_score[current] < g_score.get(best_node, float("inf"))):
            best_node = current
            best_dist = dist

        for neighbor in neighbors(current):
            tentative_g = g_score[current] + 1  # cost is 1 per move

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_heap, (f_score, neighbor))

    # Goal not reachable → return path to closest node
    if best_node is not None:
        return reconstruct_path(came_from, best_node)

    return []
