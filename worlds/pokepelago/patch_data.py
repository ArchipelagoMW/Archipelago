import re

data_file = r"f:/pythonProjects/ArchipelagoPokepelago/worlds/pokepelago/data.py"
gen9_file = r"f:/pythonProjects/ArchipelagoPokepelago/worlds/pokepelago/pokemon_data_gen9.txt"

with open(data_file, "r", encoding="utf-8") as f:
    text = f.read()

with open(gen9_file, "r", encoding="utf-8") as f:
    new_data = f.read()

# Replace everything from POKEMON_DATA = [ to ]
# Using regex to match the block
pattern = re.compile(r'POKEMON_DATA = \[\n.*?^\]\n', re.MULTILINE | re.DOTALL)
new_text = pattern.sub(new_data, text)

with open(data_file, "w", encoding="utf-8") as f:
    f.write(new_text)

print("data.py patched successfully.")
