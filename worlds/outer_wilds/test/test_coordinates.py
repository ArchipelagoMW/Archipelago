import json
import unittest

from ..coordinates import get_coordinate_for_number, total_possible_coordinates, validate_coordinate


class TestCoordinateGeneration(unittest.TestCase):
    def test_generate_specific_coordinates(self):
        self.assertListEqual(get_coordinate_for_number(0), [0, 1])
        self.assertListEqual(get_coordinate_for_number(1), [0, 2])
        self.assertListEqual(get_coordinate_for_number(2), [0, 3])
        self.assertListEqual(get_coordinate_for_number(3), [0, 4])
        self.assertListEqual(get_coordinate_for_number(4), [0, 5])
        self.assertListEqual(get_coordinate_for_number(5), [1, 0])
        self.assertListEqual(get_coordinate_for_number(6), [1, 2])

        # jump to where we switch from 2-point to 3-point coords
        self.assertListEqual(get_coordinate_for_number(29), [5, 4])
        self.assertListEqual(get_coordinate_for_number(30), [0, 1, 2])

        # jump to the very end
        self.assertListEqual(get_coordinate_for_number(1949), [5, 4, 3, 2, 1, 0])

    def test_generate_every_coordinate(self):
        all_possible_coordinates = set()

        for coordinate_number in range(0, total_possible_coordinates):
            coordinate = get_coordinate_for_number(coordinate_number)
            all_possible_coordinates.add(json.dumps(coordinate))
            # every coordinate is valid
            validate_coordinate(coordinate)

        # every coordinate is unique
        self.assertEqual(len(all_possible_coordinates), total_possible_coordinates)

    # an attempt was made to iterate through all 1950 coordinates and compare to the get_*() outputs, but
    # it turns out it was far easier to make get_*() correct than this test correct so I abandoned that
    # in case I change my mind, here's how far I got:
    #
    # coordinate = [0, 1]
    # for coordinate_number in range(1, total_possible_coordinates):
    #     index = 1
    #     value = coordinate[-index]
    #     while value in coordinate and index <= len(coordinate):
    #         value += 1
    #         if value > 5:
    #             index += 1
    #             if index > len(coordinate):
    #                 break
    #             value = coordinate[-index]
    #     if index <= len(coordinate):
    #         coordinate[-index] = value
    #         for index in range(index - 1, 0, -1):
    #             coordinate[-index] = 0
    #             while len(set(coordinate)) != len(coordinate):
    #                 coordinate[-index] += 1
    #     else:
    #         coordinate = list(range(0, index))
    #
    #     validate_coordinate(coordinate)
    #     self.assertListEqual(get_coordinate_for_number(coordinate_number), coordinate,
    #                          f"coordinate number {coordinate_number} did not match get_coordinate_for_number")
