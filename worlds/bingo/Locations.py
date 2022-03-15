
def get_location_table():
    locations = {}
    for c in range(0, 80):
        locations.update({
            f"Bingo Card {c+1}": 1960 + c,
            f"Bingo Card {c+1} Horizontal 1": 1000+(c*12),
            f"Bingo Card {c+1} Horizontal 2": 1001+(c*12),
            f"Bingo Card {c+1} Horizontal 3": 1002+(c*12),
            f"Bingo Card {c+1} Horizontal 4": 1003+(c*12),
            f"Bingo Card {c+1} Horizontal 5": 1004+(c*12),
            f"Bingo Card {c+1} Vertical 1": 1005+(c*12),
            f"Bingo Card {c+1} Vertical 2": 1006+(c*12),
            f"Bingo Card {c+1} Vertical 3": 1007+(c*12),
            f"Bingo Card {c+1} Vertical 4": 1008+(c*12),
            f"Bingo Card {c+1} Vertical 5": 1009+(c*12),
            f"Bingo Card {c+1} Diagonal 1": 1010+(c*12),
            f"Bingo Card {c+1} Diagonal 2": 1011+(c*12),
        })
    locations.update({"Completed Cards": None})
    return locations


location_table = get_location_table()
