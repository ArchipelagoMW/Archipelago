class GS2Achievement(Location):
    game: str = "GoldenSun:The Lost Age"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address

achievement_table = {

}