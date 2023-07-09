from BaseClasses import Location



class GS2Achievement(Location):
    game: str = "GoldenSun:The Lost Age"

    def __init__(self, player: int, name: str, address, parent):
        super().__init__(player, name, address, parent)
        self.event = not address

all_locations = {

}

scoutable_locations = {

}