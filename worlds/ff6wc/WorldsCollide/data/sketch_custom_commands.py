from ..data.bosses import name_enemy
from ..data.spell_names import name_id

# This dictionary contains sketch command overrides for specific enemies
# Each array is in the order of [Rare (25%), Common (75%)]
custom_commands = {
    name_enemy["Vargas"]             : [name_id["Gale Cut"]  , name_id["Special"]],
    name_enemy["TunnelArmr"]         : [name_id["Tek Laser"] , name_id["Special"]],
    name_enemy["GhostTrain"]         : [name_id["Scar Beam"] , name_id["Special"]],
    name_enemy["Dadaluma"]           : [name_id["Shock Wave"], name_id["Special"]],
    name_enemy["Shiva"]              : [name_id["Rflect"]    , name_id["Special"]],
    name_enemy["Number 024"]         : [name_id["Cure 2"]    , name_id["Scan"]],
    name_enemy["Number 128"]         : [name_id["Net"]       , name_id["Special"]],
    name_enemy["Inferno"]            : [name_id["Bolt 3"]    , name_id["TekBarrier"]],
    name_enemy["Left Crane"]         : [name_id["TekBarrier"], name_id["Special"]],
    name_enemy["Right Crane"]        : [name_id["TekBarrier"], name_id["Special"]],
    name_enemy["AtmaWeapon"]         : [name_id["Bio"]       , name_id["Special"]],
    name_enemy["KatanaSoul"]         : [name_id["Special"]   , name_id["Shock Wave"]],
    name_enemy["Red Dragon"]         : [name_id["Flare"]     , name_id["L? Pearl"]],   # L? Pearl is a vanilla sketch
    name_enemy["Blue Drgn"]          : [name_id["Slow"]      , name_id["Ice 3"]],      # Ice 3 is a vanilla sketch
    name_enemy["Skull Drgn"]         : [name_id["Elf Fire"]  , name_id["Rasp"]],       # Rasp is a vanilla sketch
    name_enemy["Gold Drgn"]          : [name_id["Ice 3"]     , name_id["Rflect"]],     # Ice 3 is a vanilla sketch
    name_enemy["Storm Drgn"]         : [name_id["Aero"]      , name_id["Pearl Wind"]], # vanilla sketches; just reversed. Useful for Lore.
    name_enemy["Whelk"]              : [name_id["Mega Volt"] , name_id["Mega Volt"]],
    name_enemy["Presenter"]          : [name_id["Magnitude8"], name_id["Blow Fish"]],
    name_enemy["Air Force"]          : [name_id["WaveCannon"], name_id["Tek Laser"]],
    name_enemy["Laser Gun"]          : [name_id["Diffuser"]  , name_id["Tek Laser"]],
    name_enemy["FlameEater"]         : [name_id["Flare"]     , name_id["Rflect"]],
    name_enemy["Nerapa"]             : [name_id["Condemned"] , name_id["Condemned"]],
    name_enemy["SrBehemoth"]         : [name_id["Meteo"]     , name_id["Pearl"]],
    name_enemy["Dullahan"]           : [name_id["Pearl"]     , name_id["Cure 2"]],
    name_enemy["Doom Gaze"]          : [name_id["Aero"]      , name_id["Aero"]],
    name_enemy["Curley"]             : [name_id["Fire 3"]    , name_id["Pearl Wind"]],
    name_enemy["Larry"]              : [name_id["Ice 3"]     , name_id["Rflect"]],
    name_enemy["Moe"]                : [name_id["Bolt 3"]    , name_id["Shell"]],
    name_enemy["Wrexsoul"]           : [name_id["Bolt 3"]    , name_id["Bolt 3"]],
    name_enemy["Hidon"]              : [name_id["GrandTrain"], name_id["Poison"]],     # Poison will be more common, and heal. May be worth it to learn GrandTrain
    name_enemy["Doom"]               : [name_id["Special"]   , name_id["ForceField"]],
    name_enemy["Goddess"]            : [name_id["Quasar"]    , name_id["Bolt 3"]],     # Bolt 3 will be more common and heal. May be worth it to learn Quasar
    name_enemy["Poltrgeist"]         : [name_id["Meteo"]     , name_id["Shrapnel"]],
    name_enemy["Ultros 1"]           : [name_id["Special"]   , name_id["Tentacle"]],
    name_enemy["Ultros 2"]           : [name_id["Special"]   , name_id["Tentacle"]],
    name_enemy["Ultros 4"]           : [name_id["Special"]   , name_id["Tentacle"]],
    name_enemy["Striker"]            : [name_id["Shrapnel"]  , name_id["Special"]],
    name_enemy["Tritoch"]            : [name_id["Rasp"]      , name_id["Rasp"]],
    name_enemy["Chadarnook (Demon)"] : [name_id["Flash Rain"], name_id["Flash Rain"]],
    name_enemy["Kefka (Narshe)"]     : [name_id["Ice 2"]     , name_id["Ice 2"]],
    name_enemy["Rizopas"]            : [name_id["Mega Volt"] , name_id["Special"]],
    name_enemy["MagiMaster"]         : [name_id["Fire 3"]    , name_id["Ice 3"]],      # Powerful abilities, but may heal
    name_enemy["Naughty"]            : [name_id["Cold Dust"] , name_id["Mute"]],
    name_enemy["Phunbaba 3"]         : [name_id["Special"]   , name_id["Blow Fish"]],
    name_enemy["Phunbaba 4"]         : [name_id["Special"]   , name_id["Blow Fish"]],
    name_enemy["Atma"]               : [name_id["Flare Star"], name_id["S. Cross"]],
}