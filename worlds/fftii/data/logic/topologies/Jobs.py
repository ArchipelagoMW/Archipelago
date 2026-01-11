from ..Requirements import *
from ..FFTLocation import FFTLocation, LocationNames

from ..regions.Jobs import *

Squire.locations = [
    FFTLocation(LocationNames.SQUIRE_UNLOCK, [], battle_level=0)
]

Chemist.locations = [
    FFTLocation(LocationNames.CHEMIST_UNLOCK, [], battle_level=0)
]

Knight.locations = [
    FFTLocation(LocationNames.KNIGHT_UNLOCK, [Requirement(["Squire"])], battle_level=0)
]

Archer.locations = [
    FFTLocation(LocationNames.ARCHER_UNLOCK, [Requirement(["Squire"])], battle_level=0)
]

Monk.locations = [
    FFTLocation(LocationNames.MONK_UNLOCK, [Requirement(["Knight"])], battle_level=0)
]

Thief.locations = [
    FFTLocation(LocationNames.THIEF_UNLOCK, [Requirement(["Archer"])], battle_level=0)
]

Lancer.locations = [
    FFTLocation(LocationNames.LANCER_UNLOCK, [Requirement(["Thief"])], battle_level=0)
]

Geomancer.locations = [
    FFTLocation(LocationNames.GEOMANCER_UNLOCK, [Requirement(["Monk"])], battle_level=0)
]

Samurai.locations = [
    FFTLocation(LocationNames.SAMURAI_UNLOCK, [Requirement(["Knight", "Monk", "Lancer"])], battle_level=0)
]

Ninja.locations = [
    FFTLocation(LocationNames.NINJA_UNLOCK, [Requirement(["Archer", "Thief", "Geomancer"])], battle_level=0)
]

Dancer.locations = [
    FFTLocation(LocationNames.DANCER_UNLOCK, [Requirement(["Lancer", "Geomancer"])], battle_level=0)
]

Priest.locations = [
    FFTLocation(LocationNames.PRIEST_UNLOCK, [Requirement(["Chemist"])], battle_level=0)
]

Wizard.locations = [
    FFTLocation(LocationNames.WIZARD_UNLOCK, [Requirement(["Chemist"])], battle_level=0)
]

Oracle.locations = [
    FFTLocation(LocationNames.ORACLE_UNLOCK, [Requirement(["Priest"])], battle_level=0)
]

TimeMage.locations = [
    FFTLocation(LocationNames.TIME_MAGE_UNLOCK, [Requirement(["Wizard"])], battle_level=0)
]

Mediator.locations = [
    FFTLocation(LocationNames.MEDIATOR_UNLOCK, [Requirement(["Oracle"])], battle_level=0)
]

Summoner.locations = [
    FFTLocation(LocationNames.SUMMONER_UNLOCK, [Requirement(["Time Mage"])], battle_level=0)
]

Calculator.locations = [
    FFTLocation(LocationNames.CALCULATOR_UNLOCK, [Requirement(["Priest", "Wizard", "Oracle", "Time Mage"])], battle_level=0)
]

Bard.locations = [
    FFTLocation(LocationNames.BARD_UNLOCK, [Requirement(["Mediator", "Summoner"])], battle_level=0)
]

Mime.locations = [
    FFTLocation(LocationNames.MIME_UNLOCK, [
        Requirement(["Squire", "Chemist", "Lancer", "Geomancer", "Mediator", "Summoner"])
    ], battle_level=0)
]