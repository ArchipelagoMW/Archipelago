import json
import pkgutil

data_bytes = pkgutil.get_data(__name__, "archipelago.json")
data = json.loads(data_bytes.decode())

def get_version() -> str:
    return f"v{data["world_version"]}"

def get_game_name() -> str:
    return data["game"]
