import json

def location_list(data):
    locations = []

    for name, floor in data["floors"].items():
        for room in floor["rooms"]:
            locations.append(f'{name} - {room}')
    
    for boss, reward in data["boss_rewards"].items():
        for i in range(reward):
            locations.append(f'{boss} Reward #{i+1}')

    for i in range(1, 301):
        locations.append(f'Item Pickup #{i}')

    for boss in data["boss_rewards"].keys():
        locations.append(f'Defeat {boss}')

    return locations