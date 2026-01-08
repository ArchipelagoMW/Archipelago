from random import Random
from .options import OuterWildsGameOptions


# Example output: (
#     ["TH", "BH", "GD", "DB", "HGT"],
#     {"HGT":30, "TH":60, "BH":90, "GD":120, "DB":150, "SS":180, "AR":210, "HL":240, "OPC":270},
#     {"ET":"up", "AT":"down", "TH":"left", "BH":"right"}
# )
def generate_random_orbits(random: Random, options: OuterWildsGameOptions) -> (list[str], dict[str, int]):
    # The Outsider relies on GD and DB coming together at the end of a loop, so they stay in the last two lanes
    if options.enable_outsider_mod:
        inner_planets = ["HGT", "TH", "BH"]
        random.shuffle(inner_planets)
        planet_order = inner_planets + ["GD", "DB"]
    else:
        planet_order = ["HGT", "TH", "BH", "GD", "DB"]
        random.shuffle(planet_order)

    # We want vanilla/flat orbits, angled orbits and vertical orbits to all be reasonably likely,
    # and we want to avoid collisions that would potentially make a location unreachable
    # or kill the player in sudden, unpredictable ways. Specific tests we did include:
    # - There are 4 orbits (listed below) known to collide with The Interloper, so we exclude them.
    # All planet orders were tested at angles 0 and 180, which should cover everything since we
    # aren't editing The Interloper's own orbit.
    # - The Stranger and Dreamworld have a fixed position 45 degrees above the vanilla orbital plane,
    # about the same distance from the sun as Brittle Hollow's vanilla orbit. A planet at 60 degrees
    # may become visible in the Dreamworld "sky", but won't cause any problems.
    # - The black void where Dark Bramble rooms are created has a fixed position at 90 degrees below
    # the Sun. If all orbits are vertical, GD and DB (and the map satellite) intersect this void.

    # Thus, we use multiples of 30 both to avoid the Stranger and to get a decent variety of
    # angles without it being too obvious that we're only using a fixed set of choices.
    all_possible_angles = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]

    orbit_angles: dict[str, int] = {}
    for index, planet in enumerate(planet_order):
        possible_angles = all_possible_angles.copy()

        # The 2 outermost orbits need to be non-vertical to avoid the DB void.
        if index > 2:
            possible_angles.remove(90)
            possible_angles.remove(270)

        # Avoid known collisions with The Interloper.
        if index == 4 and planet == "TH":
            possible_angles.remove(0)
        if index == 3 and planet == "TH":
            possible_angles.remove(180)
        if index == 4 and planet == "GD":
            possible_angles.remove(0)
        if index == 3 and planet == "GD":
            possible_angles.remove(180)

        orbit_angles[planet] = random.choice(possible_angles)

    # The Outsider relies on GD and DB coming together at the end of a loop, so they need matching orbit angles.
    # For some reason that means DB's angle must be the opposite of GD's, not the same.
    if options.enable_outsider_mod:
        orbit_angles["DB"] = -(orbit_angles["GD"])

    # No subtle constraints for the satellite orbits
    for satellite in ("SS", "AR", "HL", "OPC"):
        orbit_angles[satellite] = random.choice(all_possible_angles)

    return planet_order, orbit_angles


def generate_random_rotations(random: Random) -> dict[str, str]:
    # These are static properties of Unity's Vector3 class, e.g. Vector3.up is (0, 1, 0)
    possible_axis_directions = ["up", "down", "left", "right", "forward", "back", "zero"]

    # I couldn't get the HGT as a whole to change rotation, but each of the Ember and Ash Twins
    # can change rotation, so for this part of the code those are two separate "planets".
    # GD and DB do not rotate, and I've heard GD's islands would stop working if it did rotate.
    # The satellites' axes can also be changed, but it's not noticeable enough to bother.
    rotation_axes: dict[str, str] = {}
    for planet in ("ET", "AT", "TH", "BH"):
        rotation_axes[planet] = random.choice(possible_axis_directions)

    return rotation_axes
