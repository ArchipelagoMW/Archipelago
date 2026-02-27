all_ring_names = []


def ring(name: str) -> str:
    all_ring_names.append(name)
    return name


class Ring:
    slime_charmer = ring("Slime Charmer Ring")
    ring_of_yoba = ring("Ring of Yoba")
    sturdy = ring("Sturdy Ring")
    burglar = ring("Burglar's Ring")
    iridium_band = ring("Iridium Band")
    napalm = ring("Napalm Ring")
    hot_java = ring("Hot Java Ring")