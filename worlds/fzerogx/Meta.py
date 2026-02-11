
from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld
from .Data import meta_table

##############
# Meta Classes
##############
class ManualWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up manual game integration for Archipelago multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Fuzzy"]
    )]

######################################
# Convert meta.json data to properties
######################################
def set_world_description(base_doc: str) -> str:
    if meta_table.get("docs", {}).get("apworld_description", None) is None:
        return base_doc

    if isinstance(meta_table["docs"]["apworld_description"], str):
        base_doc = meta_table["docs"]["apworld_description"]
    else:
        fullstring = ""
        for line in meta_table["docs"]["apworld_description"]:
            fullstring += "\n" + line
        base_doc = fullstring
    return base_doc

def set_world_webworld(web: WebWorld) -> WebWorld:
    if meta_table.get("docs", {}).get("web", {}):
        Web_Config = meta_table["docs"]["web"]

        web.theme = Web_Config.get("theme", web.theme)
        web.game_info_languages = Web_Config.get("game_info_languages", web.game_info_languages)
        web.options_presets = Web_Config.get("options_presets", web.options_presets)
        web.options_page = Web_Config.get("options_page", web.options_page)
        if hasattr(web, 'bug_report_page'):
            web.bug_report_page = Web_Config.get("bug_report_page", web.bug_report_page)
        else:
            web.bug_report_page = Web_Config.get("bug_report_page", None)

        if Web_Config.get("tutorials", []):
            tutorials = []
            for tutorial in Web_Config.get("tutorials", []):
                # Converting json to Tutorials
                tutorials.append(Tutorial(
                    tutorial.get("name", "Multiworld Setup Guide"),
                    tutorial.get("description", "A guide to setting up manual game integration for Archipelago multiworld games."),
                    tutorial.get("language", "English"),
                    tutorial.get("file_name", "setup_en.md"),
                    tutorial.get("link", "setup/en"),
                    tutorial.get("authors", [meta_table.get("creator", meta_table.get("player", "Unknown"))])
                ))
            web.tutorials = tutorials
    return web

#################
# Meta Properties
#################
world_description: str = set_world_description("""
    Manual games allow you to set custom check locations and custom item names that will be rolled into a multiworld.
    This allows any variety of game -- PC, console, board games, Microsoft Word memes... really anything -- to be part of a multiworld randomizer.
    The key component to including these games is some level of manual restriction. Since the items are not actually withheld from the player,
    the player must manually refrain from using these gathered items until the tracker shows that they have been acquired or sent.
    """)
world_webworld: ManualWeb = set_world_webworld(ManualWeb())

enable_region_diagram = bool(meta_table.get("enable_region_diagram", False))
