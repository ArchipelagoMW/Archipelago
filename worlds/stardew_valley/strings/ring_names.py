all_ring_names = []


def ring(name: str) -> str:
    all_ring_names.append(name)
    return name


class Ring:
    burglar = ring("Burglar")
