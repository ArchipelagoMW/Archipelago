def canDig(player):
    return lambda state: state.has("Green Goblet", player) and state.has("Hammers", player)


def canMini(player):
    return lambda state: state.has("Red Goblet", player) and state.has("Hammers", player)


def canDash(player):
    return lambda state: state.has("Red Pearl Bean", player) and state.has("Firebrand", player)


def canCrash(player):
    return lambda state: state.has("Green Pearl Bean", player) and state.has("Thunderhand", player)


def hammers(player):
    return lambda state: state.has("Hammers", player)


def super(player):
    return lambda state: state.has("Hammers", player, 2)


def ultra(player):
    return lambda state: state.has("Hammers", player, 3)


def fruits(player):
    return lambda state: (state.has("Red Chuckola Fruit", player)
                          and state.has("Purple Chuckola Fruit", player)
                          and state.has("White Chuckola Fruit", player))


def pieces(player):
    return lambda state: (
                         state.has("Beanstar Piece 1", player)
                         and state.has("Beanstar Piece 2", player)
                         and state.has("Beanstar Piece 3", player)
                         and state.has("Beanstar Piece 4", player)
                        )


def neon(player):
    return lambda state: (
                          state.has("Blue Neon Egg", player)
                          and state.has("Red Neon Egg", player)
                          and state.has("Green Neon Egg", player)
                          and state.has("Yellow Neon Egg", player)
                          and state.has("Purple Neon Egg", player)
                          and state.has("Orange Neon Egg", player)
                          and state.has("Azure Neon Egg", player)
                          )


def spangle(player):
    return lambda state: state.has("Spangle", player)


def rose(player):
    return lambda state: state.has("Peasley's Rose", player)


def brooch(player):
    return lambda state: state.has("Beanbean Brooch", player)


def thunder(player):
    return lambda state: state.has("Thunderhand", player)


def fire(player):
    return lambda state: state.has("Firebrand", player)


def dressBeanstar(player):
    return lambda state: state.has("Peach's Extra Dress", player) and state.has("Fake Beanstar", player)


def membership(player):
    return lambda state: state.has("Membership Card", player)


def winkle(player):
    return lambda state: state.has("Winkle Card", player)


def beanFruit(player):
    return lambda state: (
                          state.has("Bean Fruit 1", player)
                          and state.has("Bean Fruit 2", player)
                          and state.has("Bean Fruit 3", player)
                          and state.has("Bean Fruit 4", player)
                          and state.has("Bean Fruit 5", player)
                          and state.has("Bean Fruit 6", player)
                          and state.has("Bean Fruit 7", player)
                          )


def surfable(player):
    return lambda state: (
                        ultra(player)
                        and ((canDig(player) and canMini(player))
                        or (membership(player) and fire(player)))
                        )


def postJokes(player):
    return lambda state: (
                          surfable(player)
                          and canDig(player)
                          and dressBeanstar(player)
                          and pieces(player)
                          and fruits(player)
                          and brooch(player)
                          and rose(player)
                          and canDash(player)
                          )


def teehee(player):
    return lambda state: super(player) or canDash(player)


def castleTown(player):
    return lambda state: fruits(player) and brooch(player)


def fungitown(player):
    return lambda state: castleTown(player) and thunder(player) and rose(player) and (super(player) or canDash(player))

def piranha_shop(player):
    return lambda state: state.can_reach("Shop Mom Piranha Flag", "Region", player)

def fungitown_shop(player):
    return lambda state: state.can_reach("Shop Enter Fungitown Flag", "Region", player)

def star_shop(player):
    return lambda state: state.can_reach("Shop Beanstar Complete Flag", "Region", player)

def birdo_shop(player):
    return lambda state: state.can_reach("Shop Birdo Flag", "Region", player)

def fungitown_birdo_shop(player):
    return lambda state: state.can_reach("Fungitown Shop Birdo Flag", "Region", player)
