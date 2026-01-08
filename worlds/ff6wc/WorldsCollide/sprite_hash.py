from .constants.entities import name_id
HASH_CHARACTERS = [name_id[x] for x in ["General Leo", "Banon/Duncan", "Esper Terra", "Merchant"]]
# the game reserves space for 22 sprites (14 main characters + imp/leo/banon/ghost/merchant/etc...)
# overwrite some memory reserved for 4 chars which don't appear on save/load/shop/coliseum/party select screens

from typing import NamedTuple
HashSprite = NamedTuple("HashSprite", [("name", str), ("sprite_address", int), ("palette", int), ("y_offset", int)])

hash_sprites = [
    HashSprite("Leo", 0xd66a00, 0, 0),
    HashSprite("Banon", 0xd67f60, 3, 0),
    HashSprite("Gestahl", 0xd6ea40, 3, 0),
    HashSprite("Old Man", 0xd6f120, 0, 0),
    HashSprite("Man", 0xd6f800, 1, 0),
    HashSprite("Interceptor", 0xd6fee0, 4, 1),
    HashSprite("Maria", 0xd705c0, 0, 0),
    HashSprite("Scholar", 0xd70cc0, 1, 0),
    HashSprite("Draco", 0xd713c0, 4, 0),
    HashSprite("Arvis", 0xd71ac0, 4, 0),
    HashSprite("Returner", 0xd72080, 1, 0),
    HashSprite("Ultros", 0xd72640, 5, 1),
    HashSprite("Suit Gau", 0xd72c00, 3, 0),
    HashSprite("Dancer", 0xd731c0, 2, 0),
    HashSprite("Chancellor", 0xd73780, 2, 0),
    HashSprite("Clyde", 0xd73d40, 1, 0),
    HashSprite("Old Woman", 0xd74300, 4, 0),
    HashSprite("Woman", 0xd748c0, 1, 0),
    HashSprite("Boy", 0xd74e80, 1, 0),
    HashSprite("Girl", 0xd75440, 1, 0),
    HashSprite("Bird", 0xd75a00, 4, 1),
    HashSprite("Rachel", 0xd75fc0, 0, 0),
    HashSprite("Katarin", 0xd76580, 4, 0),
    HashSprite("Impresario", 0xd76b40, 4, 0),
    HashSprite("Esper Elder", 0xd77100, 4, 0),
    HashSprite("Yura", 0xd776c0, 4, 0),
    HashSprite("Sigfried", 0xd77c80, 4, 0),
    HashSprite("Cid", 0xd78240, 3, 0),
    HashSprite("Maduin", 0xd78800, 4, 0),
    HashSprite("Bandit", 0xd78dc0, 3, 0),
    HashSprite("Vargas", 0xd792c0, 4, 0),
    HashSprite("Behemoth", 0xd797c0, 2, 0),
    HashSprite("Narshe Guard", 0xd79cc0, 1, 0),
    HashSprite("Conductor", 0xd7a1c0, 4, 0),
    HashSprite("Shopkeeper", 0xd7a6c0, 1, 0),
    HashSprite("Fairy", 0xd7abc0, 2, 0),
    HashSprite("Wolf", 0xd7b0c0, 2, 0),
    HashSprite("Dragon", 0xd7b5c0, 1, 0),
    HashSprite("Fish", 0xd7bac0, 4, 0),
    HashSprite("Figaro Guard", 0xd7bfc0, 2, 0),
    HashSprite("Daryl", 0xd7c4c0, 2, 0),
    HashSprite("Chupon", 0xd7c9c0, 5, 0),
    HashSprite("Royal Guard", 0xd7cec0, 2, 0),
]

def generate_hash(string):
    import hashlib
    hash_string = hashlib.sha256(string.encode('utf-8')).hexdigest()

    hash_result = []
    sub_hash_len = len(hash_string) // len(HASH_CHARACTERS)
    for x in range(0, len(hash_string), sub_hash_len):
        sub_hash = hash_string[x : x + sub_hash_len]
        hash_sprite_index = int(sub_hash, 16) % len(hash_sprites)
        hash_result.append(hash_sprites[hash_sprite_index])

    return hash_result

if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.dirname(__file__))

    from args.arguments import Arguments
    args = Arguments()
    print(", ".join([entry.name for entry in args.sprite_hash]))
