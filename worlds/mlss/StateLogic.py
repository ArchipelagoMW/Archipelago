def canDig(state, player):
    return state.has("Green Goblet", player) and state.has("Hammers", player)


def canMini(state, player):
    return state.has("Red Goblet", player) and state.has("Hammers", player)


def canDash(state, player):
    return state.has("Red Pearl Bean", player) and state.has("Firebrand", player)


def canCrash(state, player):
    return state.has("Green Pearl Bean", player) and state.has("Thunderhand", player)


def hammers(state, player):
    return state.has("Hammers", player)


def super(state, player):
    return state.has("Hammers", player, 2)


def ultra(state, player):
    return state.has("Hammers", player, 3)


def fruits(state, player):
    return state.has("Red Chuckola Fruit", player) and state.has("Purple Chuckola Fruit", player) and state.has(
        "White Chuckola Fruit", player)


def pieces(state, player):
    return state.has("Beanstar Piece 1", player) and state.has("Beanstar Piece 2", player) and state.has(
        "Beanstar Piece 3", player) and state.has("Beanstar Piece 4", player)


def neon(state, player):
    return state.has("Blue Neon Egg", player) and state.has("Red Neon Egg", player) and state.has("Green Neon Egg",
                                                                                                  player) and state.has(
        "Yellow Neon Egg", player) and state.has("Purple Neon Egg", player) and state.has("Orange Neon Egg",
                                                                                          player) and state.has(
        "Azure Neon Egg", player)


def spangle(state, player):
    return state.has("Spangle", player)


def rose(state, player):
    return state.has("Peasley's Rose", player)


def brooch(state, player):
    return state.has("Beanbean Brooch", player)


def thunder(state, player):
    return state.has("Thunderhand", player)


def fire(state, player):
    return state.has("Firebrand", player)


def dressBeanstar(state, player):
    return state.has("Peach's Extra Dress", player) and state.has("Fake Beanstar", player)


def membership(state, player):
    return state.has("Membership Card", player)


def winkle(state, player):
    return state.has("Winkle Card", player)


def beanFruit(state, player):
    return state.has("Bean Fruit 1", player) and state.has("Bean Fruit 2", player) and state.has("Bean Fruit 3", player) and state.has("Bean Fruit 4", player) and state.has("Bean Fruit 5", player) and state.has("Bean Fruit 6", player) and state.has("Bean Fruit 7", player)


def surfable(state, player):
    return ultra(state, player) and ((canDig(state, player) and canMini(state, player)) or (membership(state, player) and fire(state, player)))


def postJokes(state, player):
    return surfable(state, player) and canDig(state, player) and dressBeanstar(state, player) and pieces(state, player) and fruits(state, player) and brooch(state, player) and rose(state, player) and canDash(state, player)


def teehee(state, player):
    return super(state, player) or canDash(state, player)


def castleTown(state, player):
    return fruits(state, player) and brooch(state, player)


def fungitown(state, player):
    return castleTown(state, player) and thunder(state, player) and rose(state, player) and (super(state, player) or canDash(state, player))
