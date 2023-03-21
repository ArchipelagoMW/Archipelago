import os
import json

from worlds.LauncherComponents import Component, components

data_files = [os.path.join(root, name)
              for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), "data"))
              for name in files if name.endswith(".json")]

for file in data_files:
    component_data = json.load(open(file))
    new_component = Component(
        component_data.get("display_name"),
        component_data.get("script_name", None),
        component_data.get("frozen_name", None),
        component_data.get("cli", False),
        component_data.get("icon", "icon"),
        component_data.get("component_type", None),
        component_data.get("func", None),
        component_data.get("file_identifier", None),
        component_data.get("file_path", None),
    )
    components.append(new_component)
