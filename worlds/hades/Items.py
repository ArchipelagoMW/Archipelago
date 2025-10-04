from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification


class ItemData(NamedTuple):
    code: Optional[int]
    progression: bool
    event: bool = False
    trap: bool = False


hades_base_item_id = 666100

item_table_pacts: Dict[str, ItemData] = {  
    "Hard Labor Pact Level": ItemData(hades_base_item_id, True),
    "Lasting Consequences Pact Level": ItemData(hades_base_item_id + 1, True),
    "Convenience Fee Pact Level": ItemData(hades_base_item_id + 2, True),
    "Jury Summons Pact Level": ItemData(hades_base_item_id + 3, True),
    "Extreme Measures Pact Level": ItemData(hades_base_item_id + 4, True),
    "Calisthenics Program Pact Level": ItemData(hades_base_item_id + 5, True),
    "Benefits Package Pact Level": ItemData(hades_base_item_id + 6, True),
    "Middle Management Pact Level": ItemData(hades_base_item_id + 7, True),
    "Underworld Customs Pact Level": ItemData(hades_base_item_id + 8, True),
    "Forced Overtime Pact Level": ItemData(hades_base_item_id + 9, True),
    "Heightened Security Pact Level": ItemData(hades_base_item_id + 10, True),
    "Routine Inspection Pact Level": ItemData(hades_base_item_id + 11, True),
    "Damage Control Pact Level": ItemData(hades_base_item_id + 12, True),
    "Approval Process Pact Level": ItemData(hades_base_item_id + 13, True),
    "Tight Deadline Pact Level": ItemData(hades_base_item_id + 14, True),
    "Personal Liability Pact Level": ItemData(hades_base_item_id + 15, True),
}

items_table_event: Dict[str, ItemData] = {
    "Meg Victory": ItemData(None, True, True),
    "Lernie Victory": ItemData(None, True, True),
    "Bros Victory": ItemData(None, True, True),
    "Hades Victory": ItemData(None, True, True),
    "Hades Victory Sword Weapon": ItemData(None, True, True),
    "Meg Victory Sword Weapon": ItemData(None, True, True),
    "Lernie Victory Sword Weapon": ItemData(None, True, True),
    "Bros Victory Sword Weapon": ItemData(None, True, True),
    "Hades Victory Bow Weapon": ItemData(None, True, True),
    "Meg Victory Bow Weapon": ItemData(None, True, True),
    "Lernie Victory Bow Weapon": ItemData(None, True, True),
    "Bros Victory Bow Weapon": ItemData(None, True, True),
    "Hades Victory Spear Weapon": ItemData(None, True, True),
    "Meg Victory Spear Weapon": ItemData(None, True, True),
    "Lernie Victory Spear Weapon": ItemData(None, True, True),
    "Bros Victory Spear Weapon": ItemData(None, True, True),
    "Hades Victory Shield Weapon": ItemData(None, True, True),
    "Meg Victory Shield Weapon": ItemData(None, True, True),
    "Lernie Victory Shield Weapon": ItemData(None, True, True),
    "Bros Victory Shield Weapon": ItemData(None, True, True),
    "Hades Victory Fist Weapon": ItemData(None, True, True),
    "Meg Victory Fist Weapon": ItemData(None, True, True),
    "Lernie Victory Fist Weapon": ItemData(None, True, True),
    "Bros Victory Fist Weapon": ItemData(None, True, True),
    "Hades Victory Gun Weapon": ItemData(None, True, True),
    "Meg Victory Gun Weapon": ItemData(None, True, True),
    "Lernie Victory Gun Weapon": ItemData(None, True, True),
    "Bros Victory Gun Weapon": ItemData(None, True, True),
}

items_table_fates_completion: Dict[str, ItemData] = {
    "Is There No Escape? Event Item": ItemData(None, True, True),
    "Distant Relatives Event Item": ItemData(None, True, True),
    "Chthonic Colleagues Event Item": ItemData(None, True, True),
    "The Reluctant Musician Event Item": ItemData(None, True, True),
    "Goddess Of Wisdom Event Item": ItemData(None, True, True),
    "God Of The Heavens Event Item": ItemData(None, True, True),
    "God Of The Sea Event Item": ItemData(None, True, True),
    "Goddess Of Love Event Item": ItemData(None, True, True),
    "God Of War Event Item": ItemData(None, True, True),
    "Goddess Of The Hunt Event Item": ItemData(None, True, True),
    "God Of Wine Event Item": ItemData(None, True, True),
    "God Of Swiftness Event Item": ItemData(None, True, True),
    "Goddess Of Seasons Event Item": ItemData(None, True, True),
    "Power Without Equal Event Item": ItemData(None, True, True),
    "Divine Pairings Event Item": ItemData(None, True, True),
    "Primordial Boons Event Item": ItemData(None, True, True),
    "Primordial Banes Event Item": ItemData(None, True, True),
    "Infernal Arms Event Item": ItemData(None, True, True),
    "The Stygian Blade Event Item": ItemData(None, True, True),
    "The Heart Seeking Bow Event Item": ItemData(None, True, True),
    "The Shield Of Chaos Event Item": ItemData(None, True, True),
    "The Eternal Spear Event Item": ItemData(None, True, True),
    "The Twin Fists Event Item": ItemData(None, True, True),
    "The Adamant Rail Event Item": ItemData(None, True, True),
    "Master Of Arms Event Item": ItemData(None, True, True),
    "A Violent Past Event Item": ItemData(None, True, True),
    "Harsh Conditions Event Item": ItemData(None, True, True),
    "Slashed Benefits Event Item": ItemData(None, True, True),
    "Wanton Ransacking Event Item": ItemData(None, True, True),
    "A Simple Job Event Item": ItemData(None, True, True),
    "Chthonic Knowledge Event Item": ItemData(None, True, True),
    "Customer Loyalty Event Item": ItemData(None, True, True),
    "Dark Reflections Event Item": ItemData(None, True, True),
    "Close At Heart Event Item": ItemData(None, True, True),
    "Denizens Of The Deep Event Item": ItemData(None, True, True),
    "The Useless Trinket Event Item": ItemData(None, True, True),
}

item_table_filler: Dict[str, ItemData] = {
    "Darkness": ItemData(hades_base_item_id + 16, False),
    "Keys": ItemData(hades_base_item_id + 17, False),
    "Gemstones": ItemData(hades_base_item_id + 18, False),
    "Diamonds": ItemData(hades_base_item_id + 19, False),
    "TitanBlood": ItemData(hades_base_item_id + 20, False),
    "Nectar": ItemData(hades_base_item_id + 21, False),
    "Ambrosia": ItemData(hades_base_item_id + 22, False)
}

item_table_keepsake: Dict[str, ItemData] = {
    "Cerberus Keepsake": ItemData(hades_base_item_id + 23, True),
    "Achilles Keepsake": ItemData(hades_base_item_id + 24, True),
    "Nyx Keepsake": ItemData(hades_base_item_id + 25, True),
    "Thanatos Keepsake": ItemData(hades_base_item_id + 26, True),
    "Charon Keepsake": ItemData(hades_base_item_id + 27, True),
    "Hypnos Keepsake": ItemData(hades_base_item_id + 28, True),
    "Megaera Keepsake": ItemData(hades_base_item_id + 29, True),
    "Orpheus Keepsake": ItemData(hades_base_item_id + 30, True),
    "Dusa Keepsake": ItemData(hades_base_item_id + 31, True),
    "Skelly Keepsake": ItemData(hades_base_item_id + 32, True),
    "Zeus Keepsake": ItemData(hades_base_item_id + 33, True),
    "Poseidon Keepsake": ItemData(hades_base_item_id + 34, True),
    "Athena Keepsake": ItemData(hades_base_item_id + 35, True),
    "Aphrodite Keepsake": ItemData(hades_base_item_id + 36, True),
    "Ares Keepsake": ItemData(hades_base_item_id + 37, True),
    "Artemis Keepsake": ItemData(hades_base_item_id + 38, True),
    "Dionysus Keepsake": ItemData(hades_base_item_id + 39, True),
    "Hermes Keepsake": ItemData(hades_base_item_id + 40, True),
    "Demeter Keepsake": ItemData(hades_base_item_id + 41, True),
    "Chaos Keepsake": ItemData(hades_base_item_id + 42, True),
    "Sisyphus Keepsake": ItemData(hades_base_item_id + 43, True),
    "Eurydice Keepsake": ItemData(hades_base_item_id + 44, True),
    "Patroclus Keepsake": ItemData(hades_base_item_id + 45, True),
}

item_table_weapons: Dict[str, ItemData] = {
    "Sword Weapon Unlock Item": ItemData(hades_base_item_id + 46, True),
    "Bow Weapon Unlock Item": ItemData(hades_base_item_id + 47, True),
    "Spear Weapon Unlock Item": ItemData(hades_base_item_id + 48, True),
    "Shield Weapon Unlock Item": ItemData(hades_base_item_id + 49, True),
    "Fist Weapon Unlock Item": ItemData(hades_base_item_id + 50, True),
    "Gun Weapon Unlock Item": ItemData(hades_base_item_id + 51, True),
}

item_table_store: Dict[str, ItemData] = {
    "Fountain Upgrade1 Item": ItemData(hades_base_item_id + 52, True),
    "Fountain Upgrade2 Item": ItemData(hades_base_item_id + 53, True),
    "Fountain Tartarus Item": ItemData(hades_base_item_id + 54, True),
    "Fountain Asphodel Item": ItemData(hades_base_item_id + 55, True),
    "Fountain Elysium Item": ItemData(hades_base_item_id + 56, True),
    "Urns Of Wealth1 Item": ItemData(hades_base_item_id + 57, True),
    "Urns Of Wealth2 Item": ItemData(hades_base_item_id + 58, True),
    "Urns Of Wealth3 Item": ItemData(hades_base_item_id + 59, True),
    "Infernal Trove1 Item": ItemData(hades_base_item_id + 60, True),
    "Infernal Trove2 Item": ItemData(hades_base_item_id + 61, True),
    "Infernal Trove3 Item": ItemData(hades_base_item_id + 62, True),
    "Keepsake Collection Item": ItemData(hades_base_item_id + 63, True),
    "Deluxe Contractor Desk Item": ItemData(hades_base_item_id + 64, True),
    "Vanquishers Keep Item": ItemData(hades_base_item_id + 65, True),
    "Fishing Rod Item": ItemData(hades_base_item_id + 66, True),
    "Court Musician Sentence Item": ItemData(hades_base_item_id + 67, True),
    "Court Musician Stand Item": ItemData(hades_base_item_id + 68, True),
    "Pitch Black Darkness Item": ItemData(hades_base_item_id + 69, True),
    "Fated Keys Item": ItemData(hades_base_item_id + 70, True),
    "Brilliant Gemstones Item": ItemData(hades_base_item_id + 71, True),
    "Vintage Nectar Item": ItemData(hades_base_item_id + 72, True),
    "Darker Thirst Item": ItemData(hades_base_item_id + 73, True),
}

item_table_hidden_aspects: Dict[str, ItemData] = {
    "Sword Hidden Aspect": ItemData(hades_base_item_id + 74, True),
    "Bow Hidden Aspect": ItemData(hades_base_item_id + 75, True),
    "Spear Hidden Aspect": ItemData(hades_base_item_id + 76, True),
    "Shield Hidden Aspect": ItemData(hades_base_item_id + 77, True),
    "Fist Hidden Aspect": ItemData(hades_base_item_id + 78, True),
    "Gun Hidden Aspect": ItemData(hades_base_item_id + 79, True)
}

item_table_traps: Dict[str, ItemData] = {
    "Money Punishment": ItemData(hades_base_item_id + 80, False, False, True),
    "Health Punishment": ItemData(hades_base_item_id + 81, False, False, True),
}

item_table_helpers: Dict[str, ItemData] = {
    "Max Health Helper": ItemData(hades_base_item_id + 82, False, False, False),
    "Boon Boost Helper": ItemData(hades_base_item_id + 83, False, False, False),
    "Initial Money Helper": ItemData(hades_base_item_id + 84, False, False, False),
}


def create_filler_pool_options(options):
    item_filler_options = []
    if options.darkness_pack_value.value:
        item_filler_options.append("Darkness")
    if options.keys_pack_value.value:
        item_filler_options.append("Keys")
    if options.gemstones_pack_value.value:
        item_filler_options.append("Gemstones")
    if options.diamonds_pack_value.value:
        item_filler_options.append("Diamonds")
    if options.titan_blood_pack_value.value:
        item_filler_options.append("TitanBlood")
    if options.nectar_pack_value.value:
        item_filler_options.append("Nectar")
    if options.ambrosia_pack_value.value:
        item_filler_options.append("Ambrosia")
    if not item_filler_options:
        item_filler_options.append("Darkness")
    return item_filler_options


def create_trap_pool():
    return [trap for trap in item_table_traps.keys()]


def create_pact_pool_amount(options) -> Dict[str, int]:
    item_pool_pacts = {
        "Hard Labor Pact Level": int(options.hard_labor_pact_amount),
        "Lasting Consequences Pact Level": int(options.lasting_consequences_pact_amount),
        "Convenience Fee Pact Level": int(options.convenience_fee_pact_amount),
        "Jury Summons Pact Level": int(options.jury_summons_pact_amount),
        "Extreme Measures Pact Level": int(options.extreme_measures_pact_amount),
        "Calisthenics Program Pact Level": int(options.calisthenics_program_pact_amount),
        "Benefits Package Pact Level": int(options.benefits_package_pact_amount),
        "Middle Management Pact Level": int(options.middle_management_pact_amount),
        "Underworld Customs Pact Level": int(options.underworld_customs_pact_amount),
        "Forced Overtime Pact Level": int(options.forced_overtime_pact_amount),
        "Heightened Security Pact Level": int(options.heightened_security_pact_amount),
        "Routine Inspection Pact Level": int(options.routine_inspection_pact_amount),
        "Damage Control Pact Level": int(options.damage_control_pact_amount),
        "Approval Process Pact Level": int(options.approval_process_pact_amount),
        "Tight Deadline Pact Level": int(options.tight_deadline_pact_amount),
        "Personal Liability Pact Level": int(options.personal_liability_pact_amount),
    }
    return item_pool_pacts


event_item_pairs: Dict[str, str] = {
    "Beat Hades": "Hades Victory",
    "Beat Meg": "Meg Victory",
    "Beat Lernie": "Lernie Victory",
    "Beat Bros": "Bros Victory",
    "Is There No Escape? Event": "Is There No Escape? Event Item",
    "Distant Relatives Event": "Distant Relatives Event Item",
    "Chthonic Colleagues Event": "Chthonic Colleagues Event Item",
    "The Reluctant Musician Event": "The Reluctant Musician Event Item",
    "Goddess Of Wisdom Event": "Goddess Of Wisdom Event Item",
    "God Of The Heavens Event": "God Of The Heavens Event Item",
    "God Of The Sea Event": "God Of The Sea Event Item",
    "Goddess Of Love Event": "Goddess Of Love Event Item",
    "God Of War Event": "God Of War Event Item",
    "Goddess Of The Hunt Event": "Goddess Of The Hunt Event Item",
    "God Of Wine Event": "God Of Wine Event Item",
    "God Of Swiftness Event": "God Of Swiftness Event Item",
    "Goddess Of Seasons Event": "Goddess Of Seasons Event Item",
    "Power Without Equal Event": "Power Without Equal Event Item",
    "Divine Pairings Event": "Divine Pairings Event Item",
    "Primordial Boons Event": "Primordial Boons Event Item",
    "Primordial Banes Event": "Primordial Banes Event Item",
    "Infernal Arms Event": "Infernal Arms Event Item",
    "The Stygian Blade Event": "The Stygian Blade Event Item",
    "The Heart Seeking Bow Event": "The Heart Seeking Bow Event Item",
    "The Shield Of Chaos Event": "The Shield Of Chaos Event Item",
    "The Eternal Spear Event": "The Eternal Spear Event Item",
    "The Twin Fists Event": "The Twin Fists Event Item",
    "The Adamant Rail Event": "The Adamant Rail Event Item",
    "Master Of Arms Event": "Master Of Arms Event Item",
    "A Violent Past Event": "A Violent Past Event Item",
    "Harsh Conditions Event": "Harsh Conditions Event Item",
    "Slashed Benefits Event": "Slashed Benefits Event Item",
    "Wanton Ransacking Event": "Wanton Ransacking Event Item",
    "A Simple Job Event": "A Simple Job Event Item",
    "Chthonic Knowledge Event": "Chthonic Knowledge Event Item",
    "Customer Loyalty Event": "Customer Loyalty Event Item",
    "Dark Reflections Event": "Dark Reflections Event Item",
    "Close At Heart Event": "Close At Heart Event Item",
    "Denizens Of The Deep Event": "Denizens Of The Deep Event Item",
    "The Useless Trinket Event": "The Useless Trinket Event Item", 
}

event_item_pairs_weapon_mode: Dict[str, str] = {
    "Is There No Escape? Event": "Is There No Escape? Event Item",
    "Distant Relatives Event": "Distant Relatives Event Item",
    "Chthonic Colleagues Event": "Chthonic Colleagues Event Item",
    "The Reluctant Musician Event": "The Reluctant Musician Event Item",
    "Goddess Of Wisdom Event": "Goddess Of Wisdom Event Item",
    "God Of The Heavens Event": "God Of The Heavens Event Item",
    "God Of The Sea Event": "God Of The Sea Event Item",
    "Goddess Of Love Event": "Goddess Of Love Event Item",
    "God Of War Event": "God Of War Event Item",
    "Goddess Of The Hunt Event": "Goddess Of The Hunt Event Item",
    "God Of Wine Event": "God Of Wine Event Item",
    "God Of Swiftness Event": "God Of Swiftness Event Item",
    "Goddess Of Seasons Event": "Goddess Of Seasons Event Item",
    "Power Without Equal Event": "Power Without Equal Event Item",
    "Divine Pairings Event": "Divine Pairings Event Item",
    "Primordial Boons Event": "Primordial Boons Event Item",
    "Primordial Banes Event": "Primordial Banes Event Item",
    "Infernal Arms Event": "Infernal Arms Event Item",
    "The Stygian Blade Event": "The Stygian Blade Event Item",
    "The Heart Seeking Bow Event": "The Heart Seeking Bow Event Item",
    "The Shield Of Chaos Event": "The Shield Of Chaos Event Item",
    "The Eternal Spear Event": "The Eternal Spear Event Item",
    "The Twin Fists Event": "The Twin Fists Event Item",
    "The Adamant Rail Event": "The Adamant Rail Event Item",
    "Master Of Arms Event": "Master Of Arms Event Item",
    "A Violent Past Event": "A Violent Past Event Item",
    "Harsh Conditions Event": "Harsh Conditions Event Item",
    "Slashed Benefits Event": "Slashed Benefits Event Item",
    "Wanton Ransacking Event": "Wanton Ransacking Event Item",
    "A Simple Job Event": "A Simple Job Event Item",
    "Chthonic Knowledge Event": "Chthonic Knowledge Event Item",
    "Customer Loyalty Event": "Customer Loyalty Event Item",
    "Dark Reflections Event": "Dark Reflections Event Item",
    "Close At Heart Event": "Close At Heart Event Item",
    "Denizens Of The Deep Event": "Denizens Of The Deep Event Item",
    "The Useless Trinket Event": "The Useless Trinket Event Item", 
    "Beat Hades Sword Weapon": "Hades Victory Sword Weapon",
    "Beat Meg Sword Weapon": "Meg Victory Sword Weapon",
    "Beat Lernie Sword Weapon": "Lernie Victory Sword Weapon",
    "Beat Bros Sword Weapon": "Bros Victory Sword Weapon",
    "Beat Hades Bow Weapon": "Hades Victory Bow Weapon",
    "Beat Meg Bow Weapon": "Meg Victory Bow Weapon",
    "Beat Lernie Bow Weapon": "Lernie Victory Bow Weapon",
    "Beat Bros Bow Weapon": "Bros Victory Bow Weapon",
    "Beat Hades Spear Weapon": "Hades Victory Spear Weapon",
    "Beat Meg Spear Weapon": "Meg Victory Spear Weapon",
    "Beat Lernie Spear Weapon": "Lernie Victory Spear Weapon",
    "Beat Bros Spear Weapon": "Bros Victory Spear Weapon",
    "Beat Hades Shield Weapon": "Hades Victory Shield Weapon",
    "Beat Meg Shield Weapon": "Meg Victory Shield Weapon",
    "Beat Lernie Shield Weapon": "Lernie Victory Shield Weapon",
    "Beat Bros Shield Weapon": "Bros Victory Shield Weapon",
    "Beat Hades Fist Weapon": "Hades Victory Fist Weapon",
    "Beat Meg Fist Weapon": "Meg Victory Fist Weapon",
    "Beat Lernie Fist Weapon": "Lernie Victory Fist Weapon",
    "Beat Bros Fist Weapon": "Bros Victory Fist Weapon",
    "Beat Hades Gun Weapon": "Hades Victory Gun Weapon",
    "Beat Meg Gun Weapon": "Meg Victory Gun Weapon",
    "Beat Lernie Gun Weapon": "Lernie Victory Gun Weapon",
    "Beat Bros Gun Weapon": "Bros Victory Gun Weapon",
}


item_table = {
    **item_table_pacts,
    **items_table_event,
    **items_table_fates_completion,
    **item_table_filler,
    **item_table_keepsake,
    **item_table_weapons,
    **item_table_store,
    **item_table_hidden_aspects,
    **item_table_traps,
    **item_table_helpers,
}

group_pacts = {"pacts": item_table_pacts.keys()}
group_fillers = {"fillers": item_table_filler.keys()}
group_contractor = {"contractor": item_table_store.keys()}
group_weapons = {"weapons": item_table_weapons.keys()}
group_aspects = {"aspects": item_table_hidden_aspects.keys()}
group_keepsakes = {"keepsakes": item_table_keepsake.keys()}

item_name_groups = {
    **group_pacts,
    **group_fillers,
    **group_contractor,
    **group_weapons,
    **group_aspects,
    **group_keepsakes,
}


class HadesItem(Item):
    game = "Hades"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        if item_data.progression:
            itemClass = ItemClassification.progression
        elif item_data.trap:
            itemClass = ItemClassification.trap
        else:
            itemClass = ItemClassification.filler
            
        super(HadesItem, self).__init__(
            name,
            itemClass,
            item_data.code, player
        )

    def is_progression(self):
        return self.classification == ItemClassification.progression
