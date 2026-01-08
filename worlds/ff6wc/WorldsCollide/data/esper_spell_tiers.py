from ..data.spell_names import name_id

tiers = [
    [
        name_id["Cure"],
    ],
    [
        name_id["Cure 2"],
        name_id["Life"],
    ],
    [
        name_id["Cure 3"],
        name_id["Life 2"],
        name_id["Life 3"],
    ],

    [
        name_id["Ice"],
        name_id["Bolt"],
        name_id["Poison"],
        name_id["Drain"],
        name_id["Demi"],
        name_id["Quartr"],
        name_id["W Wind"],
        name_id["Scan"],
        name_id["Rasp"],
        name_id["Haste"],
        name_id["Rflect"],
        name_id["Haste2"],
        name_id["Dispel"],
        name_id["Antdot"],
        name_id["Regen"],
    ],
    [
        name_id["Fire"],
        name_id["Bio"],
        name_id["Break"],
        name_id["Quake"],
        name_id["Slow"],
        name_id["Safe"],
        name_id["Float"],
        name_id["Shell"],
        name_id["Vanish"],
        name_id["Slow 2"],
        name_id["Remedy"],
    ],
    [
        name_id["Fire 2"],
        name_id["Ice 2"],
        name_id["Bolt 2"],
        name_id["Doom"],
        name_id["Meteor"],
        name_id["Mute"],
        name_id["Sleep"],
        name_id["Muddle"],
        name_id["Bserk"],
        name_id["Imp"],
        name_id["Osmose"],
        name_id["Warp"],
    ],
    [
        name_id["Fire 3"],
        name_id["Ice 3"],
        name_id["Bolt 3"],
        name_id["Pearl"],
        name_id["Flare"],
        name_id["X-Zone"],
        name_id["Stop"],
    ],
    [
        name_id["Merton"],
        name_id["Quick"],
        name_id["Ultima"],
    ],
]
weights = [0.04, 0.08, 0.04, 0.23, 0.22, 0.28, 0.095, 0.015]

tier_s_distribution = [
    (name_id["Merton"], 0.6),
    (name_id["Quick"],  0.3),
    (name_id["Ultima"], 0.1),
]

top_spells = tiers[7]
top_spells.extend(tiers[6])
top_spells.extend(tiers[2])
