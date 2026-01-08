from random import Random

two_point_coordinates = 6 * 5                  # 30 = 1.5%
three_point_coordinates = 6 * 5 * 4            # 120 = 6%
four_point_coordinates = 6 * 5 * 4 * 3         # 360 = 18.5%
five_point_coordinates = 6 * 5 * 4 * 3 * 2     # 720 = 37%
six_point_coordinates = 6 * 5 * 4 * 3 * 2 * 1  # 720 = 37%

total_possible_coordinates = (two_point_coordinates + three_point_coordinates + four_point_coordinates +
                              five_point_coordinates + six_point_coordinates)  # 1950

coordinates_with_n_points = {
    2: two_point_coordinates,
    3: three_point_coordinates,
    4: four_point_coordinates,
    5: five_point_coordinates,
    6: six_point_coordinates,
}

# Some Nomai coordinates are nearly identical to English letters, namely: N, I/l and C
# To avoid even the miniscule chance of randomized coordinates resembling a bad word,
# we prevent those specific letter-shaped coordinates from being used.
# Since lists are not hashable, we have to use tuples here.
deny_list = {
    # 0 = Right, 1 = UpperRight, 2 = UpperLeft, 3 = Left, 4 = LowerLeft, 5 = LowerRight
    (4, 2, 5, 1),  # N
    (4, 2),  # I/l (left of center)
    (5, 1),  # I/l (right of center)
    (5, 4, 3, 2, 1)  # C
}


def coordinate_description(coordinate: list[int]) -> str:
    point_descriptions = []
    for point in coordinate:
        if point == 0:
            point_descriptions.append("Right")
        elif point == 1:
            point_descriptions.append("Upper Right")
        elif point == 2:
            point_descriptions.append("Upper Left")
        elif point == 3:
            point_descriptions.append("Left")
        elif point == 4:
            point_descriptions.append("Lower Left")
        elif point == 5:
            point_descriptions.append("Lower Right")
    return str.join(", ", point_descriptions)


def generate_random_coordinates(random: Random) -> list[list[int]]:
    # give each size an equal chance, so coordinates aren't dominated by the more numerous 5- and 6-point shapes
    sizes = [
        random.randint(2, 6),
        random.randint(2, 6),
        random.randint(2, 6),
    ]
    selections = [
        random.randint(0, coordinates_with_n_points[sizes[0]] - 1),
        random.randint(0, coordinates_with_n_points[sizes[1]] - 1),
        random.randint(0, coordinates_with_n_points[sizes[2]] - 1),
    ]
    selected_coordinates = [
        get_coordinate_points_for_number(sizes[0], selections[0]),
        get_coordinate_points_for_number(sizes[1], selections[1]),
        get_coordinate_points_for_number(sizes[2], selections[2]),
    ]

    map(validate_coordinate, selected_coordinates)

    # if we hit the deny list, simply try again
    for c in selected_coordinates:
        if (tuple(c) in deny_list) or (tuple(reversed(c)) in deny_list):
            return generate_random_coordinates(random)
    return selected_coordinates


def validate_coordinate(coordinate: list[int]) -> None:
    assert len(coordinate) >= 2
    assert len(coordinate) <= 6
    assert len(set(coordinate)) == len(coordinate)


# Here, the number represents an index into the list of all possible coordinates of any length
def get_coordinate_for_number(coord_index: int) -> list[int]:
    assert coord_index < total_possible_coordinates

    if coord_index < two_point_coordinates:
        return get_coordinate_points_for_number(2, coord_index)
    coord_index -= two_point_coordinates

    if coord_index < three_point_coordinates:
        return get_coordinate_points_for_number(3, coord_index)
    coord_index -= three_point_coordinates

    if coord_index < four_point_coordinates:
        return get_coordinate_points_for_number(4, coord_index)
    coord_index -= four_point_coordinates

    if coord_index < five_point_coordinates:
        return get_coordinate_points_for_number(5, coord_index)
    coord_index -= five_point_coordinates

    return get_coordinate_points_for_number(6, coord_index)


# Now the number represents an index into the list of all possible coordinates of one specific length
def get_coordinate_points_for_number(point_count: int, coord_index: int) -> list[int]:
    possible_coords = coordinates_with_n_points[point_count]
    points_not_taken = [0, 1, 2, 3, 4, 5]
    coord_points = []
    bucket_size = possible_coords

    while len(coord_points) < point_count:
        bucket_size //= len(points_not_taken)
        point_choice = coord_index // bucket_size

        point_num = points_not_taken[point_choice]
        points_not_taken.remove(point_num)
        coord_points.append(point_num)

        coord_index %= bucket_size

    return coord_points
