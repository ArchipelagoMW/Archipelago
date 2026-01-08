
switch_sensitive_entrances = {
    #"ToI B1 Ascent": 0b01
}

switch_logic = [
    # [entrance, exit, normal, *hard, *glitched]
    ["ToI Exit", "ToI 1F Right Staircase", 0b10, 0b11],
    ["ToI Exit", "ToI 1F Descent", 0b11],
    ["ToI Exit", "ToI 1F Ascent", 0b11],
    ["ToI 1F Ascent", "ToI Exit", 0b11],
    ["ToI 1F Ascent", "ToI 1F Switch Staircase", 0b10, 0b11],
    ["ToI 3F Right Staircase", "ToI 3F Key Door Staircase", 0b11],
    ["ToI 3F Key Door Staircase", "ToI 3F Right Staircase", 0b11],
    ["ToI B1 Ascent", "ToI B1 Descent", 0b01, 0b01, 0b11],
    ["ToI B1 Ascent", "ToI B1 Blue Warp", 0b01, 0b01, 0b11],
    ["ToI B1 Ascent", "ToI B1 Boss Staircase", 0b01, 0b01, 0b11],
]

ruins_water = [

]