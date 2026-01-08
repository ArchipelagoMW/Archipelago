from typing import Callable
from BaseClasses import CollectionState


def get_bingo_rule(location, world) -> Callable[[CollectionState], bool]:
    required_keys = extract_bingo_spaces(location)
    return lambda state: all(state.has(key, world.player) for key in required_keys)


def special_rule(world, all_keys) -> Callable[[CollectionState], bool]:
    return lambda state: all(state.has(key, world.player) for key in all_keys)


def can_goal(state, player, required_bingos, board_size) -> bool:

    # Generate all possible Bingo keys for the board
    possible_keys = [f"{chr(row)}{col}" for row in range(ord('A'), ord('A') + board_size) for col in range(1, board_size + 1)]

    possible_bingos = []

    # Generate rows
    possible_bingos += [
        [f"{chr(ord('A') + row)}{col}" for col in range(1, board_size + 1)]
        for row in range(board_size)
    ]

    # Generate columns
    possible_bingos += [
        [f"{chr(ord('A') + row)}{col}" for row in range(board_size)]
        for col in range(1, board_size + 1)
    ]

    # Generate the main diagonal (\) from top-left to bottom-right
    possible_bingos.append([
        f"{chr(ord('A') + i)}{i + 1}" for i in range(board_size)
    ])

    # Generate the anti-diagonal (/) from top-right to bottom-left
    possible_bingos.append([
        f"{chr(ord('A') + i)}{board_size - i}" for i in range(board_size)
    ])

    # Collect keys that the player has
    player_keys = []
    for key in possible_keys:  # possible_keys contains all keys (A1, A2, ..., E5)
        if state.has(key, player):
            player_keys.append(key)

    # Count how many Bingos the player has
    bingo_count = 0
    for bingo in possible_bingos:
        if all(key in player_keys for key in bingo):
            bingo_count += 1

    # Check if the number of completed Bingos meets or exceeds the required amount
    return bingo_count >= required_bingos


def extract_bingo_spaces(location):
    # Extract the content within the brackets
    start, end = location[location.index("(") + 1:location.index(")")].split("-")

    # Determine the range of rows and columns
    start_row = start[0]  # 'A', 'B', 'C', etc.
    start_col = int(start[1:])  # 1, 2, 3, etc.
    end_row = end[0]  # 'A', 'B', 'C', etc.
    end_col = int(end[1:])  # 1, 2, 3, etc.

    spaces = []

    # Generate spaces for horizontal or vertical Bingo
    if start_row == end_row:  # Horizontal Bingo
        col_range = range(start_col, end_col + 1) if start_col < end_col else range(start_col, end_col - 1, -1)
        for col in col_range:
            spaces.append(f"{start_row}{col}")
    elif start_col == end_col:  # Vertical Bingo
        row_range = range(ord(start_row), ord(end_row) + 1) if ord(start_row) < ord(end_row) else range(ord(start_row), ord(end_row) - 1, -1)
        for row in row_range:
            spaces.append(f"{chr(row)}{start_col}")
    else:  # Diagonal Bingo
        row_range = range(ord(start_row), ord(end_row) + 1) if ord(start_row) < ord(end_row) else range(ord(start_row), ord(end_row) - 1, -1)
        col_range = range(start_col, end_col + 1) if start_col < end_col else range(start_col, end_col - 1, -1)
        for row, col in zip(row_range, col_range):
            spaces.append(f"{chr(row)}{col}")

    return spaces
