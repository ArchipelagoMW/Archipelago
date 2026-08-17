from typing import Dict, Any, List
import copy

def _required_option(option: str, options: Dict[str, Any]) -> Any:
    """Returns the option value, or raises an error if the option is not present."""
    if option not in options:
        raise KeyError(f"Campaign preset is missing required option \"{option}\".")
    return options.pop(option)

def _validate_option(option: str, options: Dict[str, str], default: str, valid_values: List[str]) -> str:
    """Returns the option value if it is present and valid, the default if it is not present, or raises an error if it is present but not valid."""
    result = options.pop(option, default)
    if result not in valid_values:
        raise ValueError(f"Preset option \"{option}\" received unknown value \"{result}\".")
    return result

def make_golden_path(options: Dict[str, Any]) -> Dict[str, Any]:
    chain_name_options = ['Mar Sara', 'Agria', 'Redstone', 'Meinhoff', 'Haven', 'Tarsonis', 'Valhalla', 'Char',
                          'Umoja', 'Kaldir', 'Zerus', 'Skygeirr Station', 'Dominion Space', 'Korhal',
                          'Aiur', 'Glacius', 'Shakuras', 'Ulnar', 'Slayn',
                          'Antiga', 'Braxis', 'Chau Sara', 'Moria', 'Tyrador', 'Xil', 'Zhakul',
                          'Azeroth', 'Crouton', 'Draenor', 'Sanctuary']
    
    size = max(_required_option("size", options), 4)
    keys_option_values = ["none", "layouts", "missions", "progressive_layouts", "progressive_missions", "progressive_per_layout"]
    keys_option = _validate_option("keys", options, "none", keys_option_values)
    min_chains = 2
    max_chains = 6
    two_start_positions = options.pop("two_start_positions", False)
    # Compensating for empty mission at start
    if two_start_positions:
        size += 1

    class Campaign:
        def __init__(self, missions_remaining: int):
            self.chain_lengths = [1]
            self.chain_padding = [0]
            self.required_missions = [0]
            self.padding = 0
            self.missions_remaining = missions_remaining
            self.mission_counter = 1
        
        def add_mission(self, chain: int, required_missions: int = 0, *, is_final: bool = False):
            if self.missions_remaining == 0 and not is_final:
                return
            
            self.mission_counter += 1
            self.chain_lengths[chain] += 1
            self.missions_remaining -= 1

            if chain == 0:
                self.padding += 1
                self.required_missions.append(required_missions)

        def add_chain(self):
            self.chain_lengths.append(0)
            self.chain_padding.append(self.padding)
    
    campaign = Campaign(size - 2)
    current_required_missions = 0
    main_chain_length = 0
    while campaign.missions_remaining > 0:
        main_chain_length += 1
        if main_chain_length % 2 == 1:  # Adding branches
            chains_to_make = 0 if len(campaign.chain_lengths) >= max_chains else min_chains if main_chain_length == 1 else 1
            for _ in range(chains_to_make):
                campaign.add_chain()
        # Updating branches
        for side_chain in range(len(campaign.chain_lengths) - 1, 0, -1):
            campaign.add_mission(side_chain)
        # Adding main path mission
        current_required_missions = (campaign.mission_counter * 3) // 4
        if two_start_positions:
            # Compensating for skipped mission at start
            current_required_missions -= 1
        campaign.add_mission(0, current_required_missions)
    campaign.add_mission(0, current_required_missions, is_final = True)

    # Create mission order preset out of campaign
    layout_base = {
        "type": "column",
        "display_name": chain_name_options,
        "unique_name": True,
        "missions": [],
    }
    # Optionally add key requirement to layouts
    if keys_option == "layouts":
        layout_base["entry_rules"] = [{ "items": { "Key": 1 }}]
    elif keys_option == "progressive_layouts":
        layout_base["entry_rules"] = [{ "items": { "Progressive Key": 0 }}]
    preset = {
        str(chain): copy.deepcopy(layout_base) for chain in range(len(campaign.chain_lengths))
    }
    preset["0"]["exit"] = True
    if not two_start_positions:
        preset["0"].pop("entry_rules", [])
    for chain in range(len(campaign.chain_lengths)):
        length = campaign.chain_lengths[chain]
        padding = campaign.chain_padding[chain]
        preset[str(chain)]["size"] = padding + length
        # Add padding to chain
        if padding > 0:
            preset[str(chain)]["missions"].append({
                "index": [pad for pad in range(padding)],
                "empty": True
            })

        if chain == 0:
            if two_start_positions:
                preset["0"]["missions"].append({
                    "index": 0,
                    "empty": True
                })
            # Main path gets number requirements
            for mission in range(1, len(campaign.required_missions)):
                preset["0"]["missions"].append({
                    "index": mission,
                    "entry_rules": [{
                        "scope": "../..",
                        "amount": campaign.required_missions[mission]
                    }]
                })
            # Optionally add key requirements except to the starter mission
            if keys_option == "missions":
                for slot in preset["0"]["missions"]:
                    if "entry_rules" in slot:
                        slot["entry_rules"].append({ "items": { "Key": 1 }})
            elif keys_option == "progressive_missions":
                for slot in preset["0"]["missions"]:
                    if "entry_rules" in slot:
                        slot["entry_rules"].append({ "items": { "Progressive Key": 1 }})
            # No main chain keys for progressive_per_layout keys
        else:
            # Other paths get main path requirements
            if two_start_positions and chain < 3:
                preset[str(chain)].pop("entry_rules", [])
            for mission in range(length):
                target = padding + mission
                if two_start_positions and mission == 0 and chain < 3:
                    preset[str(chain)]["missions"].append({
                        "index": target,
                        "entrance": True
                    })
                else:
                    preset[str(chain)]["missions"].append({
                        "index": target,
                        "entry_rules": [{
                            "scope": f"../../0/{target}"
                        }]
                    })
            # Optionally add key requirements
            if keys_option == "missions":
                for slot in preset[str(chain)]["missions"]:
                    if "entry_rules" in slot:
                        slot["entry_rules"].append({ "items": { "Key": 1 }})
            elif keys_option == "progressive_missions":
                for slot in preset[str(chain)]["missions"]:
                    if "entry_rules" in slot:
                        slot["entry_rules"].append({ "items": { "Progressive Key": 1 }})
            elif keys_option == "progressive_per_layout":
                for slot in preset[str(chain)]["missions"]:
                    if "entry_rules" in slot:
                        slot["entry_rules"].append({ "items": { "Progressive Key": 0 }})
    return preset
