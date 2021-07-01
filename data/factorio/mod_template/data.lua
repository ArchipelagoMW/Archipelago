{% from "macros.lua" import dict_to_lua %}
data.raw["map-gen-presets"].default["archipelago"] = {{ dict_to_lua({"default": False, "order": "a", "basic_settings": world_gen}) }}