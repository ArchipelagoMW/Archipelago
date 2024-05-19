def misc_activities(generated_misc, random):
    new_ra = [random.choice(["Y", "N"]) for _ in generated_misc.ra]
    generated_misc = generated_misc._replace(ra=new_ra)

    random.shuffle(generated_misc.fu)
    for line in generated_misc.ec:
        random.shuffle(line)

    shuffled_warps = {}
    for direction in ["NW", "N", "NE", "W", "E", "SW", "SE"]:
        numbers = [1, 2, 3, 4]
        random.shuffle(numbers)
        shuffled_warps[direction] = numbers

    for pair in generated_misc.sa.pairs:
        for i in range(0, 2):
            if pair[i] in ["START", "END"]:
                continue
            direction = pair[i].split("_")[0]
            number = int(pair[i].split("_")[1])
            new_number = shuffled_warps[direction][number - 1]
            pair[i] = f"{direction}_{new_number}"

    return generated_misc


def get_misc_spoiler_log(generated_misc, write):
    ra_answers = " -> ".join(["YES" if ra == "Y" else "NO" for ra in generated_misc.ra])
    write(f"Radio Tower Quiz Answers:\n\n{ra_answers}\n\n")

    ecruteak_map = []
    for y in range(0, 10):
        ecruteak_map.append(["  " if x in [1, 2, 3, 4] and y in [3, 5, 7, 9] else "██" for x in range(0, 6)])

    clear_tiles = [generated_misc.ec[0][-1], generated_misc.ec[1][-1], generated_misc.ec[2][-2],
                   generated_misc.ec[2][-1], generated_misc.ec[3][-1], [5, 4], [6, 4], [5, 5], [6, 5]]

    for coords in clear_tiles:
        if coords[0] != 2:  # dont show left-side clear spots
            ecruteak_map[coords[1] - 4][coords[0] - 2] = "  "

    trainers = [[1, 9], [5, 5], [0, 7], [5, 3]]
    for coords in trainers:
        ecruteak_map[coords[1]][coords[0]] = "()"

    write("Ecruteak Gym Path:\n\n")
    write("\n".join(["".join(line) for line in ecruteak_map]) + "\n\n")

    saffron_map = []
    for y in range(0, 17):
        saffron_map.append(["█" if x in [7, 15] or y in [5, 11] else " " for x in range(0, 23)])
    character = ord("A")
    for pair in generated_misc.sa.pairs:
        for warp in pair:
            [x, y] = generated_misc.sa.warps[warp].coords
            # cosmetic fudging
            x = x + 2 if x > 10 else x
            y = y - 2 if warp != "END" else y
            saffron_map[y][x] = chr(character)
        character += 1
    saffron_map[7][9] = "X"  # sabrina
    saffron_map[16][10] = "░"  # entrance
    saffron_map[16][11] = "░"
    saffron_map[16][12] = "░"

    write("Saffron Gym Warps:\n\n")
    write("\n".join(["".join(line) for line in saffron_map]) + "\n\n")

    fuchsia_positions = {
        11: "South-West",
        12: "Center",
        16: "South",
        13: "North-East",
        6: "North"
    }
    position = sum(generated_misc.fu[0])
    if fuchsia_positions[position]:
        write(f"Fuchsia Gym Janine Position: {fuchsia_positions[position]}\n\n")
