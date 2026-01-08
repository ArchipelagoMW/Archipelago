from worlds.subversion.patch_utils import ItemRomData, patch_item_sprites


def test_patch_tables_does_not_crash() -> None:
    data = ItemRomData(1, False, {1: "me", 2: "other"})
    # TODO: make some dummy locations and items to register
    data.patch_tables(b"")


def test_patch_item_sprites_does_not_crash() -> None:
    patch_item_sprites(b"")
