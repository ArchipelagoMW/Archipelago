from random import Random
from .options import NineSolsGameOptions


# these are the in-game GameFlagDescriptable.Title values, *not* user-facing display values, so don't change them
jade_titles = [
    "Qi Thief Jade",
    "Killing Blow Jade",
    "Immovable Jade",
    "Harness Force Jade",
    "Focus Jade",
    "Swift Descent Jade",
    "Medical Jade",
    "Quick Dose Jade",
    "Steely Jade",
    "Stasis Jade",
    "Mob Quell Jade - Yin",
    "Mob Quell Jade - Yang",
    "Bearing Jade",
    "Divine Hand Jade",
    "Iron Skin Jade",
    "Pauper Jade",
    "Swift Blade Jade",
    "Last Stand Jade",
    "Recovery Jade",
    "Breather Jade",
    "Hedgehog Jade",
    "Ricochet Jade",
    "Revival Jade",
    "Soul Reaper Jade",
    "Health Thief Jade",
    "Qi Blade Jade",
    "Qi Swipe Jade",
    "Reciprocation Jade",
    "Cultivation Jade",
    "Avarice Jade",
]


def generate_random_jade_costs(random: Random, options: NineSolsGameOptions) -> dict[str, int]:
    min_cost = options.jade_cost_min.value
    max_cost = options.jade_cost_max.value
    plando = options.jade_cost_plando.value

    costs = {}
    for jade in jade_titles:
        if jade in plando:
            costs[jade] = plando[jade]
        else:
            costs[jade] = random.randint(min_cost, max_cost)
    return costs
