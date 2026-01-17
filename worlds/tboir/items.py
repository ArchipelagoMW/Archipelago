def item_list(data):
    items = []

    for name in data['unlocks'].keys():
        items.append(f'{name} Unlock')

    for item in data['items']:
        items.append(item)

    return items