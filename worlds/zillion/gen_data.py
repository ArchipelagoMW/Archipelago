from dataclasses import dataclass
import json

from zilliandomizer.game import Game as ZzGame


@dataclass
class GenData:
    """ data passed from generation to patcher """

    multi_items: dict[str, tuple[str, str]]
    """ zz_loc_name to (item_name, player_name) """
    zz_game: ZzGame
    game_id: bytes
    """ the byte string used to detect the rom """

    def to_json(self) -> str:
        """ serialized data from generation needed to patch rom """
        jsonable = {
            "multi_items": self.multi_items,
            "zz_game": self.zz_game.to_jsonable(),
            "game_id": list(self.game_id)
        }
        return json.dumps(jsonable)

    @staticmethod
    def from_json(gen_data_str: str) -> "GenData":
        """ the reverse of `to_json` """
        from_json = json.loads(gen_data_str)

        # backwards compatibility for seeds generated before new map_gen options
        room_gen = from_json["zz_game"]["options"].get("room_gen", None)
        if room_gen is not None:
            from_json["zz_game"]["options"]["map_gen"] = {False: "none", True: "rooms"}.get(room_gen, "none")
            del from_json["zz_game"]["options"]["room_gen"]

        return GenData(
            from_json["multi_items"],
            ZzGame.from_jsonable(from_json["zz_game"]),
            bytes(from_json["game_id"])
        )
