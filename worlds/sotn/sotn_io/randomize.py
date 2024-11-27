# Read, parse options
# Get rng, salt seed
# Call result(data, newNames) = randomizeStats -> append newNames -> Apply result
# Some multithread stuff cores count and create workers
# Call randomizeRelics from util.js
#   Create some workers for async run but every worker from worker.js call randomizeRelics from randomize_relics.js
import traceback, time

from randomize_stats import randomize_stats
from randomize_relics import randomize_relics
from util import apply_results
from errors import SoftLock, PickLock

locations_test = {
    "9": ["HATRNI",],
    "B": ["ML", "MV", "MB", "MP",],
    "f": ["B", "VL", "MP",],
    "E": ["B", "VLM", "VLW", "MP",],
    "e": ["HB", "HVL", "HMP",],
    "p": ["B", "VL", "MP",],
    "s": ["V", "B", "MP",],
    "M": ["L", "V", "B", "MP",],
    "P": ["B", "VL", "MP",],
    "c": ["HB", "HVL", "HMP",],
    "V": ["B", "VL", "MP",],
    "L": ["J", "L", "V", "B", "MP",],
    "y": ["JU",],
    "U": ["J",],
    "b": ["V", "B", "MP",],
    "g": ["B", "VL", "MP",],
    "a": ["V", "B", "MP",],
    "d": ["JL", "JB", "JMP", "JWp", "+B", "+L", "+V", "+MP",],
    "w": ["B", "VL", "MP",],
    "A": ["HB", "HVL", "HMP",],
    "T": ["HB", "HVL", "HMP",],
    "R": ["HB", "HVLM", "HVLW", "HMP",],
    "N": ["HB", "HVL", "HMP",],
    "I": ["HB", "HVL", "HMP",],
    "K": ["JBE",],
    "G": ["JB", "JVL", "JMP",],
    "S": ["JKM",],
    "H": ["SG", "+B", "+VL", "+MP",],
    "Crystal cloak": ["J",],
    "Mormegil": ["JL", "JB", "JMP", "JWp", "+B", "+L", "+V", "+MP",],
    "Dark Blade": ["HB", "HVL", "HMP",],
    "Ring of Arcana": ["HB", "HVL", "HMP",],
    "Holy mail": ["B", "VL", "MP",],
    "Trio": ["HB", "HVL", "HMP",],
    "Jewel sword": ["WB",],
    "Mystic pendant": ["B", "L", "V", "MP", "B", "L", "V", "MP", "B", "L", "V", "MP", "B", "L", "V", "MP",],
    "Ankh of Life": ["B", "L", "V", "MP",],
    "Morningstar": ["B", "L", "V", "MP",],
    "Goggles": ["J", "B", "L", "V", "MP", "J", "B", "L", "V", "MP", "J", "B", "L", "V", "MP", "J", "B", "L", "V",
                "MP",],
    "Silver plate": ["J", "B", "L", "V", "MP",],
    "Cutlass": ["J", "B", "L", "V", "MP",],
    "Platinum mail": ["B", "VL", "MP", "B", "VL", "MP", "B", "VL", "MP", "B", "VL", "MP",],
    "Falchion": ["B", "L", "V", "MP",],
    "Gold plate": ["B", "L", "V", "MP", "B", "L", "V", "MP", "B", "L", "V", "MP", "B", "L", "V", "MP",],
    "Bekatowa": ["B", "V", "MP", "B", "V", "MP", "B", "V", "MP", "B", "V", "MP",],
    "Holy rod": ["L", "B", "V", "MP",],
    "Library Onyx": ["B", "L", "V", "MP",],
    "Alucart sword": ["zB", "zL", "zV", "zMP", "zB", "zL", "zV", "zMP", "zB", "zL", "zV", "zMP", "zB", "zL", "zV",
                      "zMP",],
    "Broadsword": ["B", "L", "V", "MP",],
    "Estoc": ["B", "VL", "MP",],
    "Olrox Garnet": ["B", "VL", "MP",],
    "Blood cloak": ["B", "L", "V", "MP",],
    "Shield rod": ["B", "L", "V", "MP",],
    "Knight shield": ["B", "L", "V", "MP",],
    "Bandanna": ["J",],
    "Nunchaku": ["Jy", "Jy", "Jy", "Jy",],
    "Knuckle duster": ["J",],
    "Caverns Onyx": ["JU", "JB", "JyL", "JMP",],
    "Secret boots": ["JB", "JL", "JMP",],
    "Combat knife": ["JB", "JL", "JMP", "JWp", "+B", "+L", "+V", "+MP",],
    "Ring of Ares": ["JdB", "JdL", "JdMP", "JdWp", "JnB", "JnL", "JnMP", "JnWp", "JdB", "JdL", "JdMP", "JdWp", "JnB",
                     "JnL", "JnMP", "JnWp", "+B", "+L", "+V", "+MP", "+B", "+L", "+V", "+MP", "JdB", "JdL", "JdMP",
                     "JdWp", "JnB", "JnL", "JnMP", "JnWp", "JdB", "JdL", "JdMP", "JdWp", "JnB", "JnL", "JnMP", "JnWp",
                     "+B", "+L", "+V", "+MP", "+B", "+L", "+V", "+MP",],
    "Bloodstone": ["JB", "JL", "JMP", "JWp", "+B", "+L", "+V", "+MP",],
    "Icebrand": ["JB", "JL", "JMP", "+B", "+L", "+V", "+MP",],
    "Walk armor": ["JB", "JL", "JMP", "JWp", "+B", "+L", "+V", "+MP",],
    "Beryl circlet": ["HBW", "HBW", "HBW", "HBW",],
    "Talisman": ["HB", "HVL", "HMP",],
    "Katana": ["HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP",],
    "Goddess shield": ["HB", "HVL", "HMP",],
    "Twilight cloak": ["HMB", "HMVL", "HMP", "HMB", "HMVL", "HMP", "HMB", "HMVL", "HMP", "HMB", "HMVL", "HMP",],
    "Talwar": ["HB", "HVL", "HMP",],
    "Sword of Dawn": ["HB", "HVL", "HMP",],
    "Bastard sword": ["HB", "HVL", "HMP",],
    "Royal cloak": ["HB", "HVL", "HMP",],
    "Lightning mail": ["HB", "HVL", "HMP",],
    "Moon rod": ["HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP",],
    "Sunstone": ["HB", "HVL", "HMP",],
    "Luminus": ["HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP",],
    "Dragon helm": ["HB", "HVL", "HMP",],
    "Shotel": ["HMB", "HMVL", "HMP",],
    "Staurolite": ["HMB", "HMVL", "HMP",],
    "Badelaire": ["HB", "HVL", "HMP",],
    "Forbidden Library Opal": ["HB", "HVL", "HMP",],
    "Reverse Caverns Diamond": ["HB", "HVL", "HMP",],
    "Reverse Caverns Opal": ["HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP",],
    "Reverse Caverns Garnet": ["HB", "HVL", "HMP",],
    "Osafune katana": ["HB", "HVL", "HB", "HVL", "HB", "HVL", "HB", "HVL",],
    "Alucard shield": ["HB", "HVL", "HMP",],
    "Alucard sword": ["HB", "HVL", "HMP",],
    "Necklace of J": ["HB", "HVL", "HMP",],
    "Floating Catacombs Diamond": ["HB", "HVL", "HMP",],
    "Sword of Hador": ["HB", "HVL", "HMP",],
    "Alucard mail": ["HB", "HVL", "HMP",],
    "Gram": ["HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP",],
    "Fury plate": ["HB", "HVL", "HMP",],
    "Confessional": ["J", "L", "V", "B", "MP", "J", "L", "V", "B", "MP", "J", "L", "V", "B", "MP", "J", "L", "V", "B",
                     "MP",],
    "Colosseum Green tea": ["L", "V", "B", "MP", "L", "V", "B", "MP", "L", "V", "B", "MP", "L", "V", "B", "MP",],
    "Clock Tower Cloaked knight": ["L", "V", "B", "MP", "L", "V", "B", "MP", "L", "V", "B", "MP", "L", "V", "B", "MP",],
    "Waterfall Cave": ["J", "J", "J", "J",],
    "Floating Catacombs Elixir": ["HB", "HVLK", "HMP", "HB", "HVLK", "HMP", "HB", "HVLK", "HMP", "HB", "HVLK", "HMP",],
    "Reverse Entrance Antivenom": ["HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP",],
    "Reverse Forbidden Route": ["HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP",],
    "Cave Life apple": ["HBd", "HVLd", "HMPd", "HBn", "HVLn", "HMPn", "HBd", "HVLd", "HMPd", "HBn", "HVLn", "HMPn",
                        "HBd", "HVLd", "HMPd", "HBn", "HVLn", "HMPn", "HBd", "HVLd", "HMPd", "HBn", "HVLn", "HMPn",],
    "Reverse Colosseum Zircon": ["HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP",],
    "Black Marble Gallery Vat": ["HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP",],
    "Black Marble Meal Ticket": ["HBJ", "HVLJ", "HMPJ", "HBJ", "HVLJ", "HMPJ", "HBJ", "HVLJ", "HMPJ", "HBJ", "HVLJ",
                                 "HMPJ",],
    "Reverse Keep High Potion": ["HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP", "HB", "HVL", "HMP",],
    "extension": "guarded",
}


def apply_stats():
    for addr, data in result.items():
        size = data["len"]
        if size == 1:
            original_bin[addr] = data["val"] & 0xff
        elif size == 2:
            bytes_object = [
                data["val"] & 0xff,
                (data["val"] >> 8) & 0xff
            ]
            for i in range(2):
                original_bin[addr + i] = bytes_object[i]
        elif size == 4:
            bytes_object = [
                data["val"] & 0xff,
                (data["val"] >> 8) & 0xff,
                (data["val"] >> 16) & 0xff,
                (data["val"] >> 24) & 0xff,
            ]
            for i in range(4):
                pass
                original_bin[addr + i] = bytes_object[i]
        else:
            print(f"{size} no function for {data}")


if __name__ == "__main__":
    start_time = time.time()
    with open("o.bin", "rb") as in_file:
        original_bin = list(in_file.read())
    result = {}
    # Randomize stats.
    new_names = randomize_stats(result, "", "")
    # check.apply(result.data)
    #apply_results(result, original_bin)
    # Randomize relics.
    rand_try = 1
    while True:
        try:
            result = randomize_relics("", {"relicLocations": locations_test}, new_names)
            break
        except SoftLock:
            print(f"Error: Soft lock on try {rand_try}")
            rand_try += 1
        except PickLock:
            print(f"Error: Soft lock on pick relic try {rand_try}")
            rand_try += 1
        except Exception as e:
            print(traceback.format_exc())
            break
    end_time = time.time()
    print(f"Took {end_time - start_time} seconds")
    print(result)
