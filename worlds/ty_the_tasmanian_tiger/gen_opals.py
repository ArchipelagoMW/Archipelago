levels = {
    "Two Up": 0x4,
    "WitP": 0x5,
    "Ship Rex": 0x6,
    "BotRT": 0x8,
    "Snow Worries": 0x9,
    "Outback Safari": 0xA,
    "LLPoF": 0xC,
    "BtBS": 0xD,
    "RMtS": 0xE,
}

start_suffix = 0x350
end_opal = 300

with open("opals.txt", "w") as file:
    for level_name, hex_value in levels.items():
        suffix = start_suffix
        for opal in range(1, end_opal + 1):
            file.write(f'"{level_name} - Opal {opal}": LocData(0x875{hex_value:X}{suffix:X}, "{level_name}"),\n')
            suffix += 1