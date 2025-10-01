"""
This is a tool to write the animation files for each character.
This is needed for craft randomization, where we must set the animation of the original craft ID to the new craft ID.
"""
import os

from worlds.tits_the_3rd.tables.craft_list import default_characters

CHARACTER_NAME_TO_ANIMATION_FILES = {
    "estelle": ["AS04000.as"],
    "joshua": ["AS04250.as"],
    "scherazard": ["AS04240.as"],
    "olivier": ["AS04260.as"],
    "kloe": ["AS04210.as"],
    "agate": ["AS04050.as"],
    "tita": ["AS04060.as"],
    "zin": ["AS04070.as"],
    "kevin": ["AS04080.as"],
    "anelace": ["AS04090.as"],
    "josette": ["AS04100.as"],
    "richard": ["AS04110.as"],
    "mueller": ["AS04570.as"],
    "julia": ["AS04580.as"],
    "ries": ["AS04150.as", "AS04470.as"],
    "renne": ["AS04510.as"],
}

class AnimationWriter:
    def __init__(self, craft_dir: str):
        self.craft_dir = craft_dir
        self.craft_id_to_as_function_name = None
        self.craft_id_to_character_name_mapping = None
        self.craft_id_to_craft_file_name_mapping = None
        self.base_craft_ids = set()
        self._populate_craft_mappings()

    def write_animation(self, source_craft_id: int, destination_craft_id: int) -> None:
        """
        Write the craft animation instructions of the source craft id to the destination craft id.
        Only writes base craft ids. Passing in an upgraded craft ID will result in an NOP.

        Args:
            source_craft_id (int): The craft animation you wish to write.
            destination_craft_id (int): The craft animation you wish to overwrite.

        Returns:
            None
        """
        if (source_craft_id not in self.base_craft_ids) ^ (destination_craft_id not in self.base_craft_ids):
            raise ValueError(f"Invalid craft ID state. Base craft is being replaced by upgraded craft or vice versa. Please report this to the discord thread.")
        if source_craft_id not in self.base_craft_ids:
            return  # NOP, only replace base craft ids, as they share an animation with their base craft.
        data = self._read_craft(source_craft_id)
        self._write_craft(destination_craft_id, data)

    def _populate_craft_mappings(self) -> None:
        """
        Prefill the mappings for later use.

        Returns:
            None
        """
        self.base_craft_ids = set()
        self.craft_id_to_as_function_name = {}
        self.craft_id_to_character_name_mapping = {}
        self.craft_id_to_craft_file_name_mapping = {}
        for character in default_characters:
            character_name = character.name
            for craft in character.swappable_crafts:
                base_craft_name = craft.base_craft_name
                if "taunt" in base_craft_name.lower():
                    taunt_index = base_craft_name.lower().find("taunt")
                    base_craft_name = base_craft_name[:taunt_index + 5]
                craft_file_character_name = character_name
                if craft_file_character_name == "Ries":
                    craft_file_character_name = "ries_hood"
                craft_file_name = f'{craft_file_character_name.lower()}_{base_craft_name.lower().replace(" ", "_").replace(chr(39),"").replace("-","_")}.as'
                self.base_craft_ids.add(craft.base_craft_id)
                self.craft_id_to_as_function_name[craft.base_craft_id] = craft.base_as_function_name
                self.craft_id_to_character_name_mapping[craft.base_craft_id] = character_name
                self.craft_id_to_craft_file_name_mapping[craft.base_craft_id] = craft_file_name

    def _read_craft(self, craft_id: int) -> bytes:
        """
        Read the craft animation instructions from the file.

        Args:
            craft_id (int): The craft animation you wish to read.

        Returns:
            bytes: The data from the craft animation.
        """
        craft_file = self.craft_id_to_craft_file_name_mapping[craft_id]
        input_path = os.path.join(self.craft_dir, craft_file)
        with open(input_path, "r", encoding='utf-8') as f:
            return f.read()

    def _write_craft(self, destination_craft_id: int, data: bytes) -> None:
        """
        Write the craft animation instructions to the file.

        Args:
            destination_craft_id (int): The craft animation you wish to overwrite.
            data (bytes): The data to write to the craft animation.

        Returns:
            None
        """
        destination_craft_function_name = self.craft_id_to_as_function_name[destination_craft_id]
        character_name = self.craft_id_to_character_name_mapping[destination_craft_id]
        file_names = CHARACTER_NAME_TO_ANIMATION_FILES[character_name.lower()]
        for file_name in file_names:
            file_path = os.path.join(self.craft_dir, file_name)

            with open(file_path, 'r', encoding='utf-8') as fp:
                content = fp.read()

            craft_location = content.find(destination_craft_function_name)
            insert_pos = craft_location + len(destination_craft_function_name) + 1
            new_content = content[:insert_pos] + f"\n{data}" + content[insert_pos:]

            with open(file_path, 'w', encoding='utf-8') as fp:
                fp.write(new_content)
