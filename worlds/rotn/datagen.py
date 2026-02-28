import Utils
import settings
import sys
import os
import yaml
import json
from BaseClasses import logging
from .items import SongData
from typing import Dict, List
logger = logging.getLogger("RotN")

def extractModDataToJson() -> List[dict[str, Dict]]:
        """
        Extracts mod data from YAML files and converts it to SongData
        Taken and modified from the Project Diva Megamix apworld https://github.com/Cynichill/DivaAPworld/blob/main/DataHandler.py#L170
        """

        user_path = Utils.user_path(settings.get_settings().generator.player_files_path)
        folder_path = sys.argv[sys.argv.index("--player_files_path") + 1] if "--player_files_path" in sys.argv else user_path

        logger.debug(f"Checking YAMLs for megamix_mod_data at {folder_path}")

        if not os.path.isdir(folder_path):
            logger.debug(f"The path {folder_path} is not a valid directory. Modded songs are unavailable for this path.")
            return []
        
        game_key = "Rift of the Necrodancer"
        mod_data_key = "rotn_mod_data"

        all_mod_data = []

        for item in os.scandir(folder_path):
            if not item.is_file():
                continue

            try:
                with open(item.path, 'r', encoding='utf-8') as file:
                    file_content = file.read()

                    if mod_data_key not in file_content:
                        continue

                    for single_yaml in yaml.safe_load_all(file_content):
                        mod_data_content = single_yaml.get(game_key, {}).get(mod_data_key, None)

                        if not mod_data_content or isinstance(mod_data_content, dict):
                            continue

                        all_mod_data.append(json.loads(mod_data_content))

            except Exception as e:
                logger.warning(f"Failed to extract mod data from {item.name}: {e}")

        return all_mod_data

def getPlayerSpecificIds(mod_data, remap: dict[int, dict[str, list]]) -> (dict, list, dict):
    try:
        data_dict = json.loads(mod_data)
    except Exception as e:
        logger.warning(f"Failed to extract player specific IDs: {e}")
        return {}, [], {}
    
    flat_songs = {data["song_id"]: name for name, data in data_dict.items()}
    conflicts = remap.keys() & flat_songs.keys()

    player_remapped = {}
    for song_id in conflicts:
        if flat_songs[song_id] in remap[song_id]:
            player_remapped.update({song_id: remap[song_id][flat_songs[song_id]][0]})

    return data_dict, list(flat_songs.keys()), player_remapped 