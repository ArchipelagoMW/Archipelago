from typing import Dict, Any
import copy

def _required_option(option: str, options: Dict[str, Any]) -> Any:
    if option not in options:
        raise KeyError(f"Campaign preset is missing required option \"{option}\".")
    return options.pop(option)

def make_golden_path(options: Dict[str, Any]) -> Dict[str, Any]:
    chain_name_options = ['Mar Sara', 'Agria', 'Redstone', 'Meinhoff', 'Haven', 'Tarsonis', 'Valhalla', 'Char',
                          'Umoja', 'Kaldir', 'Zerus', 'Skygeirr Station', 'Dominion Space', 'Korhal',
                          'Aiur', 'Glacius', 'Shakuras', 'Ulnar', 'Slayn',
                          'Antiga', 'Braxis', 'Chau Sara', 'Moria', 'Tyrador', 'Xil', 'Zhakul',
                          'Azeroth', 'Crouton', 'Draenor', 'Sanctuary']
    
    size = max(_required_option("size", options), 2)
    min_chains = 2
    max_chains = 6

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
        campaign.add_mission(0, current_required_missions)
    campaign.add_mission(0, current_required_missions, is_final = True)

    # Create mission order preset out of campaign
    layout_base = {
        "type": "column",
        "display_name": chain_name_options,
        "unique_name": True,
        "missions": [],
    }
    preset = {
        str(chain): copy.deepcopy(layout_base) for chain in range(len(campaign.chain_lengths))
    }
    preset["0"]["exit"] = True
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
            # Main path gets number requirements
            for mission in range(1, len(campaign.required_missions)):
                preset["0"]["missions"].append({
                    "index": mission,
                    "entry_rules": [{
                        "scope": "../..",
                        "amount": campaign.required_missions[mission]
                    }]
                })
        else:
            # Other paths get main path requirements
            for mission in range(length):
                target = padding + mission
                preset[str(chain)]["missions"].append({
                    "index": target,
                    "entry_rules": [{
                        "scope": f"../../0/{target}"
                    }]
                })
    
    return preset
