from worlds.ff6wc.Options import Flagstring


def test_parser() -> None:
    fs = Flagstring("-a b c d -e f -g")

    assert fs.has_flag("-a"), f"{fs.value=}"
    assert fs.has_flag("-e"), f"{fs.value=}"
    assert fs.has_flag("-g"), f"{fs.value=}"

    assert not fs.has_flag("b"), f"{fs.value=}"
    assert not fs.has_flag("b c d"), f"{fs.value=}"
    assert not fs.has_flag("f"), f"{fs.value=}"

    assert fs.get_flag("-a") == "b c d", f"{fs.value=}"
    assert fs.get_flag("-e") == "f", f"{fs.value=}"
    assert fs.get_flag("-g") == "", f"{fs.value=}"


def test_no_hyphen_start() -> None:
    fs = Flagstring("a b c d -e f -g")

    assert not fs.has_flag("-a"), f"{fs.value=}"
    assert fs.has_flag("-e"), f"{fs.value=}"
    assert fs.has_flag("-g"), f"{fs.value=}"

    assert not fs.has_flag("b"), f"{fs.value=}"
    assert not fs.has_flag("b c d"), f"{fs.value=}"
    assert not fs.has_flag("f"), f"{fs.value=}"

    assert fs.get_flag("-e") == "f", f"{fs.value=}"
    assert fs.get_flag("-g") == "", f"{fs.value=}"

def test_replace() -> None:
    fs = Flagstring("-sc1 random -stesp 2 4 -nmc")
    fs.replace_flag("-stesp", "-sen", "2,3,8")

    assert not fs.has_flag("-stesp"), fs.value
    assert fs.get_flag("-sc1") == "random", fs.value
    assert fs.get_flag("-nmc") == "", fs.value
    assert fs.get_flag("-sen") == "2,3,8", fs.value

    assert fs.value == "-sc1 random -sen 2,3,8 -nmc", fs.value


def test_replace_at_end() -> None:
    fs = Flagstring("-sc1 random -nmc -stesp 2 4")
    assert fs.get_flag("-stesp") == "2 4", fs.value
    fs.replace_flag("-stesp", "-sen", "2,3,8")

    assert not fs.has_flag("-stesp"), fs.value
    assert fs.get_flag("-sc1") == "random", fs.value
    assert fs.get_flag("-nmc") == "", fs.value
    assert fs.get_flag("-sen") == "2,3,8", fs.value

    assert fs.value == "-sc1 random -nmc -sen 2,3,8", fs.value

def test_replace_without_value() -> None:
    fs = Flagstring("-sc1 random -nmc -stesp 2 4")
    assert fs.get_flag("-stesp") == "2 4", fs.value
    fs.replace_flag("-stesp", "-sen", "")

    assert not fs.has_flag("-stesp"), fs.value
    assert fs.get_flag("-sc1") == "random", fs.value
    assert fs.get_flag("-nmc") == "", fs.value
    assert fs.get_flag("-sen") == "", fs.value

    assert fs.value == "-sc1 random -nmc -sen", fs.value
