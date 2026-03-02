import json

# Input file from Client
json_path = r"f:/pythonProjects/PokepelagoClient/src/data/pokemon_metadata.json"
output_path = r"f:/pythonProjects/ArchipelagoPokepelago/worlds/pokepelago/pokemon_data_gen9.txt"

with open(json_path, 'r', encoding='utf-8') as f:
    metadata = json.load(f)

def format_name(raw_name):
    if raw_name == "nidoran-f": return "Nidoran F"
    if raw_name == "nidoran-m": return "Nidoran M"
    if raw_name == "mr-mime": return "Mr. Mime"
    if raw_name == "mime-jr": return "Mime Jr."
    if raw_name == "farfetchd": return "Farfetch'd"
    if raw_name == "ho-oh": return "Ho-Oh"
    if raw_name == "porygon-z": return "Porygon-Z"
    
    parts = raw_name.split('-')
    return " ".join(p.capitalize() for p in parts)

# Generation 9 ends at 1025
pokemon_list = []
for i in range(1, 1026):
    str_id = str(i)
    if str_id in metadata:
        mon = metadata[str_id]
        
        # Format types nicely with uppercase first letter
        types = [t.capitalize() for t in mon.get('types', [])]
        
        # Format name properly
        formatted_name = format_name(mon['name'])
        name = formatted_name.replace('\'', '\\\'') if '\'' in formatted_name else formatted_name
        name_str = f'"{name}"' if "'" not in name else f'"{name}"' # Just use double quotes for the string
        
        pokemon_list.append(f'    {{"id": {i}, "name": {name_str}, "types": {json.dumps(types)}}},')

with open(output_path, 'w', encoding='utf-8') as out_f:
    out_f.write("POKEMON_DATA = [\n")
    for line in pokemon_list:
        out_f.write(line + "\n")
    out_f.write("]\n")

print(f"Successfully wrote {len(pokemon_list)} Pokémon to {output_path}")
