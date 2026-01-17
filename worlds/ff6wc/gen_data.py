from dataclasses import asdict, dataclass
import json


@dataclass
class GenData:
    """ data passed from generation to patcher """

    locations: dict[str, str]
    flag_string: list[str]

    def to_json(self) -> str:
        """ serialized data from generation needed to patch rom """
        jsonable = asdict(self)
        return json.dumps(jsonable)

    @staticmethod
    def from_json(gen_data_str: str) -> "GenData":
        """ the reverse of `to_json` """
        from_json = json.loads(gen_data_str)
        return GenData(**from_json)
