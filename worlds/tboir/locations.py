from worlds.tboir.options import AdditionalItemLocationsPerStage

def location_list(data):
    locations = []

    for name, floor in data["regions"].items():
        if "rooms" in floor:
            for room in floor["rooms"]:
                locations.append(f'{name} - {room}')
    
    for boss, reward in data["boss_rewards"].items():
        for i in range(reward["amount"]):
            locations.append(f'{boss} Reward #{i+1}')

    for stage in AdditionalItemLocationsPerStage.valid_keys:
        for i in range(10):
            locations.append(f'{stage} - Item #{i+1}')

    return locations