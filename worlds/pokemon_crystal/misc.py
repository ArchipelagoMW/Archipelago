from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


def misc_activities(world: "PokemonCrystalWorld"):
    # Randomize Yes/No answers for Radio Card quiz
    for i in range(5):
        world.generated_misc.radio_tower_questions[i] = world.random.choice(["Y", "N"])

    # shuffle positions of trainers in fuchsia gym
    world.random.shuffle(world.generated_misc.fuchsia_gym_trainers)
    # warps/potential warps for each y coord, shuffle these to randomize the path
    for line in world.generated_misc.ecruteak_gym_warps:
        world.random.shuffle(line)

    shuffled_saffron_warps = {}
    for direction in ["NW", "N", "NE", "W", "E", "SW", "SE"]:
        numbers = [1, 2, 3, 4]
        world.random.shuffle(numbers)
        shuffled_saffron_warps[direction] = numbers

    for pair in world.generated_misc.saffron_gym_warps.pairs:
        for i in range(0, 2):
            if pair[i] in ["START", "END"]:
                continue
            direction = pair[i].split("_")[0]
            number = int(pair[i].split("_")[1])
            new_number = shuffled_saffron_warps[direction][number - 1]
            pair[i] = f"{direction}_{new_number}"


def get_misc_spoiler_log(world: "PokemonCrystalWorld", write):
    radio_tower_answers = " -> ".join(
        ["YES" if answer == "Y" else "NO" for answer in world.generated_misc.radio_tower_questions])
    write(f"Radio Tower Quiz Answers:\n\n{radio_tower_answers}\n\n")

    ecruteak_map = []
    # create basic map
    for y in range(0, 10):
        ecruteak_map.append(["  " if x in [1, 2, 3, 4] and y in [3, 5, 7, 9] else "██" for x in range(0, 6)])

    # clear the path through the gym
    # unused (clear) warp locations get shuffled to the end, plus some that are already clear
    clear_tiles = [world.generated_misc.ecruteak_gym_warps[0][-1],
                   world.generated_misc.ecruteak_gym_warps[1][-1],
                   world.generated_misc.ecruteak_gym_warps[2][-2],
                   world.generated_misc.ecruteak_gym_warps[2][-1],
                   world.generated_misc.ecruteak_gym_warps[3][-1],
                   [5, 4], [6, 4], [5, 5], [6, 5]]

    for coords in clear_tiles:
        # don't show left-side clear spots, since they aren't reachable
        if coords[0] != 2:
            ecruteak_map[coords[1] - 4][coords[0] - 2] = "  "

    # add trainers
    trainers = [[5, 1], [0, 3], [5, 5], [1, 9]]
    for coords in trainers:
        ecruteak_map[coords[1]][coords[0]] = "()"

    write("Ecruteak Gym Path:\n\n")
    write("\n".join(["".join(line) for line in ecruteak_map]) + "\n\n")

    saffron_map = []
    # draw the walls in saffron gym
    for y in range(0, 17):
        saffron_map.append(["█" if x in [7, 15] or y in [5, 11] else " " for x in range(0, 23)])

    character = ord("A")  # we will increment this while drawing the warps
    for pair in world.generated_misc.saffron_gym_warps.pairs:
        for warp in pair:
            [x, y] = world.generated_misc.saffron_gym_warps.warps[warp].coords
            # cosmetic fudging
            x = x + 2 if x > 10 else x
            y = y - 2 if warp != "END" else y
            saffron_map[y][x] = chr(character)  # add warp letter
        character += 1  # next letter
    saffron_map[7][9] = "X"  # sabrina
    saffron_map[16][10] = "░"  #
    saffron_map[16][11] = "░"  # entrance
    saffron_map[16][12] = "░"  #

    write("Saffron Gym Warps:\n\n")
    write("\n".join(["".join(line) for line in saffron_map]) + "\n\n")

    # sum of x + y for each position
    fuchsia_positions = {
        11: "South-West",
        12: "Center",
        16: "South",
        13: "North-East",
        6: "North"
    }
    # janine is the first trainer in the list
    position = sum(world.generated_misc.fuchsia_gym_trainers[0])
    if fuchsia_positions[position]:
        write(f"Fuchsia Gym Janine Position: {fuchsia_positions[position]}\n\n")
