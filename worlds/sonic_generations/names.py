class Regions:
    WSClassic       = "White Space - Classic Era"
    WSDreamcast     = "White Space - Dreamcast Era"
    WSModern        = "White Space - Modern Era"
    
    GHZ1            = "Stage - Green Hill Zone (Act 1)"
    GHZ2            = "Stage - Green Hill Zone (Act 2)"
    CPZ1            = "Stage - Chemical Plant Zone (Act 1)"
    CPZ2            = "Stage - Chemical Plant Zone (Act 2)"
    SSZ1            = "Stage - Sky Sanctuary Zone (Act 1)"
    SSZ2            = "Stage - Sky Sanctuary Zone (Act 2)"
    BMS             = "Boss Arena - Metal Sonic"
    BDE             = "Boss Arena - Death Egg Robot"
    SPH1            = "Stage - Speed Highway (Act 1)"
    SPH2            = "Stage - Speed Highway (Act 2)"
    CTE1            = "Stage - City Escape (Act 1)"
    CTE2            = "Stage - City Escape (Act 2)"
    SSH1            = "Stage - Seaside Hill (Act 1)"
    SSH2            = "Stage - Seaside Hill (Act 2)"
    BSD             = "Boss Arena - Shadow the Hedgehog"
    BPC             = "Boss Arena - Perfect Chaos"
    CSC1            = "Stage - Crisis City (Act 1)"
    CSC2            = "Stage - Crisis City (Act 2)"
    EUC1            = "Stage - Rooftop Run (Act 1)"
    EUC2            = "Stage - Rooftop Run (Act 2)"
    PLA1            = "Stage - Planet Wisp (Act 1)"
    PLA2            = "Stage - Planet Wisp (Act 2)"
    BSL             = "Boss Arena - Silver the Hedgehog"
    BNE             = "Boss Arena - Egg Dragoon"
    BLB             = "Boss Arena - Time Eater"

class Items:
    EGreen          = "Chaos Emerald (Green)"
    ERed            = "Chaos Emerald (Red)"
    EBlue           = "Chaos Emerald (Blue)"
    EYellow         = "Chaos Emerald (Yellow)"
    EPurple         = "Chaos Emerald (Purple)"
    ECyan           = "Chaos Emerald (Cyan)"
    EWhite          = "Chaos Emerald (White)"

    Nothing         = "Nothing"

    BKGHZ           = "Boss Key: Green Hill Zone"
    BKCPZ           = "Boss Key: Chemical Plant Zone"
    BKSSZ           = "Boss Key: Sky Sanctuary Zone"
    BKSPH           = "Boss Key: Speed Highway"
    BKCTE           = "Boss Key: City Escape"
    BKSSH           = "Boss Key: Seaside Hill"
    BKCSC           = "Boss Key: Crisis City"
    BKEUC           = "Boss Key: Rooftop Run"
    BKPLA           = "Boss Key: Planet Wisp"

class Locations:
    EGreen          = Items.EGreen
    ERed            = Items.ERed
    EBlue           = Items.EBlue
    EYellow         = Items.EYellow
    EPurple         = Items.EPurple
    ECyan           = Items.ECyan
    EWhite          = Items.EWhite

    BKGHZ           = Items.BKGHZ
    BKCPZ           = Items.BKCPZ
    BKSSZ           = Items.BKSSZ
    BKSPH           = Items.BKSPH
    BKCTE           = Items.BKCTE
    BKSSH           = Items.BKSSH
    BKCSC           = Items.BKCSC
    BKEUC           = Items.BKEUC
    BKPLA           = Items.BKPLA

    ClearGHZ1       = "Stage Clear: Green Hill Zone (Act 1)"
    ClearGHZ2       = "Stage Clear: Green Hill Zone (Act 2)"
    ClearCPZ1       = "Stage Clear: Chemical Plant Zone (Act 1)"
    ClearCPZ2       = "Stage Clear: Chemical Plant Zone (Act 2)"
    ClearSSZ1       = "Stage Clear: Sky Sanctuary Zone (Act 1)"
    ClearSSZ2       = "Stage Clear: Sky Sanctuary Zone (Act 2)"
    ClearBMS        = "Stage Clear: Metal Sonic"
    ClearBDE        = "Stage Clear: Death Egg Robot"
    ClearSPH1       = "Stage Clear: Speed Highway (Act 1)"
    ClearSPH2       = "Stage Clear: Speed Highway (Act 2)"
    ClearCTE1       = "Stage Clear: City Escape (Act 1)"
    ClearCTE2       = "Stage Clear: City Escape (Act 2)"
    ClearSSH1       = "Stage Clear: Seaside Hill (Act 1)"
    ClearSSH2       = "Stage Clear: Seaside Hill (Act 2)"
    ClearBSD        = "Stage Clear: Shadow the Hedgehog"
    ClearBPC        = "Stage Clear: Perfect Chaos"
    ClearCSC1       = "Stage Clear: Crisis City (Act 1)"
    ClearCSC2       = "Stage Clear: Crisis City (Act 2)"
    ClearEUC1       = "Stage Clear: Rooftop Run (Act 1)"
    ClearEUC2       = "Stage Clear: Rooftop Run (Act 2)"
    ClearPLA1       = "Stage Clear: Planet Wisp (Act 1)"
    ClearPLA2       = "Stage Clear: Planet Wisp (Act 2)"
    ClearBSL        = "Stage Clear: Silver the Hedgehog"
    ClearBNE        = "Stage Clear: Egg Dragoon"
    ClearBLB        = "Stage Clear: Time Eater"

def create_entrance_name(eFrom: str, eTo: str) -> str:
    return f"{eFrom} to {eTo}"

GameName:str = "Sonic Generations"