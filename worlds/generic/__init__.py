from typing import NamedTuple, Union
import logging

from BaseClasses import Item, Tutorial, ItemClassification

from ..AutoWorld import World, WebWorld
from NetUtils import SlotType


class GenericWeb(WebWorld):
    # English Language
    advanced_settings_en = Tutorial('Advanced YAML Guide',
                                 'A guide to reading YAML files and editing them to fully customize your game.',
                                 'English', 'advanced_settings_en.md', 'advanced_settings/en',
                                 ['alwaysintreble', 'Alchav'])
    commands_en = Tutorial('Archipelago Server and Client Commands',
                        'A guide detailing the commands available to the user when participating in an Archipelago session.',
                        'English', 'commands_en.md', 'commands/en', ['jat2980', 'Ijwu'])
    mac_en = Tutorial('Archipelago Setup Guide for Mac', 'A guide detailing how to run Archipelago clients on macOS.', 
                   'English', 'mac_en.md','mac/en', ['Bicoloursnake'])
    plando_en = Tutorial('Archipelago Plando Guide', 'A guide to understanding and using plando for your game.',
                      'English', 'plando_en.md', 'plando/en', ['alwaysintreble', 'Alchav'])
    setup_en = Tutorial('Getting Started',
                     'A guide to setting up the Archipelago software, and generating, hosting, and connecting to '
                     'multiworld games.',
                     'English', 'setup_en.md', 'setup/en', ['alwaysintreble'])
    triggers_en = Tutorial('Archipelago Triggers Guide', 'A guide to setting up and using triggers in your game settings.',
                        'English', 'triggers_en.md', 'triggers/en', ['alwaysintreble'])
    # French Language
    advanced_settings_fr = Tutorial('Guide YAML avancé',
                                 'Un guide pour lire les fichiers YAML et les éditer afin de personnaliser entièrement votre jeu.',
                                 'Français', 'advanced_settings_fr.md', 'advanced_settings/fr',
                                 ['Deoxis'])
    commands_fr = Tutorial('Commandes du serveur et du client Archipelago',
                        'Un guide détaillant les commandes disponibles pour l\'utilisateur lorsqu\'il participe à une session d\'Archipelago.',
                        'Français', 'commands_fr.md', 'commands/fr', ['Deoxis'])
    mac_fr = Tutorial('Guide d\'installation d\'Archipelago pour Mac', 'Un guide détaillant comment faire fonctionner les clients Archipelago sur macOS.', 
                   'Français', 'mac_fr.md','mac/fr', ['Deoxis'])
    plando_fr = Tutorial('Guide du Plando d\'Archipelago', 'Un guide pour comprendre et utiliser le plando pour votre jeu.',
                      'Français', 'plando_fr.md', 'plando/fr', ['Deoxis'])
    setup_fr = Tutorial('Pour commencer',
                     'Un guide pour configurer le logiciel Archipelago, et générer, héberger et se connecter à des parties MultiWorld.',
                     'Français', 'setup_fr.md', 'setup/fr', ['Deoxis'])
    triggers_fr = Tutorial('Guide des Triggers d\'Archipelago', 'Un guide pour configurer et utiliser les triggers dans les paramètres de votre jeu.',
                        'Français', 'triggers_fr.md', 'triggers/fr', ['Deoxis'])
    tutorials = [setup_en, mac_en, commands_en, advanced_settings_en, triggers_en, plando_en, setup_fr, mac_fr, commands_fr, advanced_settings_fr, triggers_fr, plando_fr]


class GenericWorld(World):
    game = "Archipelago"
    topology_present = False
    item_name_to_id = {
        "Nothing": -1
    }
    location_name_to_id = {
        "Cheat Console": -1,
        "Server": -2
    }
    hidden = True
    web = GenericWeb()
    data_version = 1

    def generate_early(self):
        self.multiworld.player_types[self.player] = SlotType.spectator  # mark as spectator

    def create_item(self, name: str) -> Item:
        if name == "Nothing":
            return Item(name, ItemClassification.filler, -1, self.player)
        raise KeyError(name)


class PlandoItem(NamedTuple):
    item: str
    location: str
    world: Union[bool, str] = False  # False -> own world, True -> not own world
    from_pool: bool = True  # if item should be removed from item pool
    force: str = 'silent'  # false -> warns if item not successfully placed. true -> errors out on failure to place item.

    def warn(self, warning: str):
        if self.force in ['true', 'fail', 'failure', 'none', 'false', 'warn', 'warning']:
            logging.warning(f'{warning}')
        else:
            logging.debug(f'{warning}')

    def failed(self, warning: str, exception=Exception):
        if self.force in ['true', 'fail', 'failure']:
            raise exception(warning)
        else:
            self.warn(warning)


class PlandoConnection(NamedTuple):
    entrance: str
    exit: str
    direction: str  # entrance, exit or both
