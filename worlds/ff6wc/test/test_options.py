from worlds.ff6wc.Options import StartingCharacter1


def test_char_1_from_any_override() -> None:
    """ making sure the from_any override works like I think it does """
    for _ in range(30):
        x = StartingCharacter1.from_any("random")
        assert isinstance(x, StartingCharacter1)
        assert x.value not in {StartingCharacter1.option_gogo, StartingCharacter1.option_umaro}
    x = StartingCharacter1.from_any("Mog")
    assert isinstance(x, StartingCharacter1)
    assert x.value == StartingCharacter1.option_mog
