from .game_content import ContentPack

by_mod = {}


def register_mod_content_pack(content_pack: ContentPack):
    by_mod[content_pack.name] = content_pack
