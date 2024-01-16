def has_pipe_right(state, player):
    return state.has_any(["Pipe Traversal - Right", "Pipe Traversal"], player)


def has_pipe_left(state, player):
    return state.has_any(["Pipe Traversal - Left", "Pipe Traversal"], player)


def has_pipe_down(state, player):
    return state.has_any(["Pipe Traversal - Down", "Pipe Traversal"], player)


def has_pipe_up(state, player):
    return state.has_any(["Pipe Traversal - Up", "Pipe Traversal"], player)


def has_level_progression(state, item, player, count=1):
    return state.count(item, player) + (state.count(item + " x2", player) * 2) >= count