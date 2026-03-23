# This file is auto generated. More info: https://github.com/Daivuk/apdoom

from typing import List
from BaseClasses import TypedDict

class ConnectionDict(TypedDict, total=False):
    target: str
    pro: bool

class RegionDict(TypedDict, total=False):
    name: str
    connects_to_hub: bool
    episode: int
    connections: List[ConnectionDict]


regions:List[RegionDict] = [
    # Entryway (MAP01)
    {"name":"Entryway (MAP01) Main",
     "connects_to_hub":True,
     "episode":1,
     "connections":[]},

    # Underhalls (MAP02)
    {"name":"Underhalls (MAP02) Main",
     "connects_to_hub":True,
     "episode":1,
     "connections":[{"target":"Underhalls (MAP02) Red","pro":False}]},
    {"name":"Underhalls (MAP02) Blue",
     "connects_to_hub":False,
     "episode":1,
     "connections":[{"target":"Underhalls (MAP02) Red","pro":False}]},
    {"name":"Underhalls (MAP02) Red",
     "connects_to_hub":False,
     "episode":1,
     "connections":[
        {"target":"Underhalls (MAP02) Blue","pro":False},
        {"target":"Underhalls (MAP02) Main","pro":False}]},

    # The Gantlet (MAP03)
    {"name":"The Gantlet (MAP03) Main",
     "connects_to_hub":True,
     "episode":1,
     "connections":[
        {"target":"The Gantlet (MAP03) Blue","pro":False},
        {"target":"The Gantlet (MAP03) Blue Pro Jump","pro":True}]},
    {"name":"The Gantlet (MAP03) Blue",
     "connects_to_hub":False,
     "episode":1,
     "connections":[
        {"target":"The Gantlet (MAP03) Main","pro":False},
        {"target":"The Gantlet (MAP03) Red","pro":False},
        {"target":"The Gantlet (MAP03) Blue Pro Jump","pro":False}]},
    {"name":"The Gantlet (MAP03) Red",
     "connects_to_hub":False,
     "episode":1,
     "connections":[]},
    {"name":"The Gantlet (MAP03) Blue Pro Jump",
     "connects_to_hub":False,
     "episode":1,
     "connections":[{"target":"The Gantlet (MAP03) Blue","pro":False}]},

    # The Focus (MAP04)
    {"name":"The Focus (MAP04) Main",
     "connects_to_hub":True,
     "episode":1,
     "connections":[
        {"target":"The Focus (MAP04) Red","pro":False},
        {"target":"The Focus (MAP04) Blue","pro":False}]},
    {"name":"The Focus (MAP04) Blue",
     "connects_to_hub":False,
     "episode":1,
     "connections":[{"target":"The Focus (MAP04) Main","pro":False}]},
    {"name":"The Focus (MAP04) Yellow",
     "connects_to_hub":False,
     "episode":1,
     "connections":[{"target":"The Focus (MAP04) Red","pro":False}]},
    {"name":"The Focus (MAP04) Red",
     "connects_to_hub":False,
     "episode":1,
     "connections":[
        {"target":"The Focus (MAP04) Yellow","pro":False},
        {"target":"The Focus (MAP04) Main","pro":False}]},

    # The Waste Tunnels (MAP05)
    {"name":"The Waste Tunnels (MAP05) Main",
     "connects_to_hub":False,
     "episode":1,
     "connections":[
        {"target":"The Waste Tunnels (MAP05) Red","pro":False},
        {"target":"The Waste Tunnels (MAP05) Blue","pro":False},
        {"target":"The Waste Tunnels (MAP05) Start","pro":False}]},
    {"name":"The Waste Tunnels (MAP05) Blue",
     "connects_to_hub":False,
     "episode":1,
     "connections":[
        {"target":"The Waste Tunnels (MAP05) Yellow","pro":False},
        {"target":"The Waste Tunnels (MAP05) Main","pro":False}]},
    {"name":"The Waste Tunnels (MAP05) Yellow",
     "connects_to_hub":False,
     "episode":1,
     "connections":[{"target":"The Waste Tunnels (MAP05) Blue","pro":False}]},
    {"name":"The Waste Tunnels (MAP05) Red",
     "connects_to_hub":False,
     "episode":1,
     "connections":[{"target":"The Waste Tunnels (MAP05) Main","pro":False}]},
    {"name":"The Waste Tunnels (MAP05) Start",
     "connects_to_hub":True,
     "episode":1,
     "connections":[{"target":"The Waste Tunnels (MAP05) Main","pro":False}]},

    # The Crusher (MAP06)
    {"name":"The Crusher (MAP06) Main",
     "connects_to_hub":True,
     "episode":1,
     "connections":[{"target":"The Crusher (MAP06) Blue","pro":False}]},
    {"name":"The Crusher (MAP06) Blue",
     "connects_to_hub":False,
     "episode":1,
     "connections":[
        {"target":"The Crusher (MAP06) Red","pro":False},
        {"target":"The Crusher (MAP06) Main","pro":False}]},
    {"name":"The Crusher (MAP06) Yellow",
     "connects_to_hub":False,
     "episode":1,
     "connections":[{"target":"The Crusher (MAP06) Red","pro":False}]},
    {"name":"The Crusher (MAP06) Red",
     "connects_to_hub":False,
     "episode":1,
     "connections":[
        {"target":"The Crusher (MAP06) Yellow","pro":False},
        {"target":"The Crusher (MAP06) Blue","pro":False},
        {"target":"The Crusher (MAP06) Main","pro":False}]},

    # Dead Simple (MAP07)
    {"name":"Dead Simple (MAP07) Main",
     "connects_to_hub":False,
     "episode":1,
     "connections":[{"target":"Dead Simple (MAP07) Start","pro":False}]},
    {"name":"Dead Simple (MAP07) Start",
     "connects_to_hub":True,
     "episode":1,
     "connections":[{"target":"Dead Simple (MAP07) Main","pro":False}]},

    # Tricks and Traps (MAP08)
    {"name":"Tricks and Traps (MAP08) Main",
     "connects_to_hub":True,
     "episode":1,
     "connections":[
        {"target":"Tricks and Traps (MAP08) Red","pro":False},
        {"target":"Tricks and Traps (MAP08) Yellow","pro":False}]},
    {"name":"Tricks and Traps (MAP08) Yellow",
     "connects_to_hub":False,
     "episode":1,
     "connections":[{"target":"Tricks and Traps (MAP08) Main","pro":False}]},
    {"name":"Tricks and Traps (MAP08) Red",
     "connects_to_hub":False,
     "episode":1,
     "connections":[{"target":"Tricks and Traps (MAP08) Main","pro":False}]},

    # The Pit (MAP09)
    {"name":"The Pit (MAP09) Main",
     "connects_to_hub":False,
     "episode":1,
     "connections":[
        {"target":"The Pit (MAP09) Yellow","pro":False},
        {"target":"The Pit (MAP09) Blue","pro":False},
        {"target":"The Pit (MAP09) Start","pro":False}]},
    {"name":"The Pit (MAP09) Blue",
     "connects_to_hub":False,
     "episode":1,
     "connections":[]},
    {"name":"The Pit (MAP09) Yellow",
     "connects_to_hub":False,
     "episode":1,
     "connections":[{"target":"The Pit (MAP09) Main","pro":False}]},
    {"name":"The Pit (MAP09) Start",
     "connects_to_hub":True,
     "episode":1,
     "connections":[{"target":"The Pit (MAP09) Main","pro":False}]},

    # Refueling Base (MAP10)
    {"name":"Refueling Base (MAP10) Main",
     "connects_to_hub":False,
     "episode":1,
     "connections":[
        {"target":"Refueling Base (MAP10) Yellow","pro":False},
        {"target":"Refueling Base (MAP10) Start","pro":False}]},
    {"name":"Refueling Base (MAP10) Yellow",
     "connects_to_hub":False,
     "episode":1,
     "connections":[
        {"target":"Refueling Base (MAP10) Main","pro":False},
        {"target":"Refueling Base (MAP10) Yellow Blue","pro":False}]},
    {"name":"Refueling Base (MAP10) Yellow Blue",
     "connects_to_hub":False,
     "episode":1,
     "connections":[{"target":"Refueling Base (MAP10) Yellow","pro":False}]},
    {"name":"Refueling Base (MAP10) Start",
     "connects_to_hub":True,
     "episode":1,
     "connections":[{"target":"Refueling Base (MAP10) Main","pro":False}]},

    # Circle of Death (MAP11)
    {"name":"Circle of Death (MAP11) Main",
     "connects_to_hub":True,
     "episode":1,
     "connections":[
        {"target":"Circle of Death (MAP11) Blue","pro":False},
        {"target":"Circle of Death (MAP11) Red","pro":False},
        {"target":"Circle of Death (MAP11) Ending","pro":True}]},
    {"name":"Circle of Death (MAP11) Blue",
     "connects_to_hub":False,
     "episode":1,
     "connections":[{"target":"Circle of Death (MAP11) Main","pro":False}]},
    {"name":"Circle of Death (MAP11) Red",
     "connects_to_hub":False,
     "episode":1,
     "connections":[
        {"target":"Circle of Death (MAP11) Main","pro":False},
        {"target":"Circle of Death (MAP11) Ending","pro":False}]},
    {"name":"Circle of Death (MAP11) Ending",
     "connects_to_hub":False,
     "episode":1,
     "connections":[{"target":"Circle of Death (MAP11) Main","pro":False}]},

    # The Factory (MAP12)
    {"name":"The Factory (MAP12) Indoors",
     "connects_to_hub":False,
     "episode":2,
     "connections":[
        {"target":"The Factory (MAP12) Yellow","pro":False},
        {"target":"The Factory (MAP12) Blue","pro":False},
        {"target":"The Factory (MAP12) Main","pro":False}]},
    {"name":"The Factory (MAP12) Blue",
     "connects_to_hub":False,
     "episode":2,
     "connections":[{"target":"The Factory (MAP12) Indoors","pro":False}]},
    {"name":"The Factory (MAP12) Yellow",
     "connects_to_hub":False,
     "episode":2,
     "connections":[]},
    {"name":"The Factory (MAP12) Outdoors",
     "connects_to_hub":True,
     "episode":2,
     "connections":[{"target":"The Factory (MAP12) Main","pro":False}]},
    {"name":"The Factory (MAP12) Main",
     "connects_to_hub":False,
     "episode":2,
     "connections":[
        {"target":"The Factory (MAP12) Indoors","pro":False},
        {"target":"The Factory (MAP12) Outdoors","pro":False}]},

    # Downtown (MAP13)
    {"name":"Downtown (MAP13) Main",
     "connects_to_hub":True,
     "episode":2,
     "connections":[
        {"target":"Downtown (MAP13) Yellow","pro":False},
        {"target":"Downtown (MAP13) Red","pro":False},
        {"target":"Downtown (MAP13) Blue","pro":False}]},
    {"name":"Downtown (MAP13) Blue",
     "connects_to_hub":False,
     "episode":2,
     "connections":[{"target":"Downtown (MAP13) Main","pro":False}]},
    {"name":"Downtown (MAP13) Yellow",
     "connects_to_hub":False,
     "episode":2,
     "connections":[{"target":"Downtown (MAP13) Main","pro":False}]},
    {"name":"Downtown (MAP13) Red",
     "connects_to_hub":False,
     "episode":2,
     "connections":[{"target":"Downtown (MAP13) Main","pro":False}]},

    # The Inmost Dens (MAP14)
    {"name":"The Inmost Dens (MAP14) Main",
     "connects_to_hub":True,
     "episode":2,
     "connections":[{"target":"The Inmost Dens (MAP14) Red","pro":False}]},
    {"name":"The Inmost Dens (MAP14) Blue",
     "connects_to_hub":False,
     "episode":2,
     "connections":[
        {"target":"The Inmost Dens (MAP14) Main","pro":False},
        {"target":"The Inmost Dens (MAP14) Red East","pro":False}]},
    {"name":"The Inmost Dens (MAP14) Red",
     "connects_to_hub":False,
     "episode":2,
     "connections":[
        {"target":"The Inmost Dens (MAP14) Main","pro":False},
        {"target":"The Inmost Dens (MAP14) Red South","pro":False},
        {"target":"The Inmost Dens (MAP14) Red East","pro":False}]},
    {"name":"The Inmost Dens (MAP14) Red East",
     "connects_to_hub":False,
     "episode":2,
     "connections":[
        {"target":"The Inmost Dens (MAP14) Blue","pro":False},
        {"target":"The Inmost Dens (MAP14) Main","pro":False}]},
    {"name":"The Inmost Dens (MAP14) Red South",
     "connects_to_hub":False,
     "episode":2,
     "connections":[{"target":"The Inmost Dens (MAP14) Main","pro":False}]},

    # Industrial Zone (MAP15)
    {"name":"Industrial Zone (MAP15) Main",
     "connects_to_hub":True,
     "episode":2,
     "connections":[
        {"target":"Industrial Zone (MAP15) Yellow East","pro":False},
        {"target":"Industrial Zone (MAP15) Yellow West","pro":False}]},
    {"name":"Industrial Zone (MAP15) Blue",
     "connects_to_hub":False,
     "episode":2,
     "connections":[{"target":"Industrial Zone (MAP15) Yellow East","pro":False}]},
    {"name":"Industrial Zone (MAP15) Yellow East",
     "connects_to_hub":False,
     "episode":2,
     "connections":[
        {"target":"Industrial Zone (MAP15) Blue","pro":False},
        {"target":"Industrial Zone (MAP15) Main","pro":False}]},
    {"name":"Industrial Zone (MAP15) Yellow West",
     "connects_to_hub":False,
     "episode":2,
     "connections":[{"target":"Industrial Zone (MAP15) Main","pro":False}]},

    # Suburbs (MAP16)
    {"name":"Suburbs (MAP16) Main",
     "connects_to_hub":True,
     "episode":2,
     "connections":[
        {"target":"Suburbs (MAP16) Red","pro":False},
        {"target":"Suburbs (MAP16) Blue","pro":False},
        {"target":"Suburbs (MAP16) Pro Exit","pro":True}]},
    {"name":"Suburbs (MAP16) Blue",
     "connects_to_hub":False,
     "episode":2,
     "connections":[{"target":"Suburbs (MAP16) Main","pro":False}]},
    {"name":"Suburbs (MAP16) Red",
     "connects_to_hub":False,
     "episode":2,
     "connections":[
        {"target":"Suburbs (MAP16) Main","pro":False},
        {"target":"Suburbs (MAP16) Pro Exit","pro":False}]},
    {"name":"Suburbs (MAP16) Pro Exit",
     "connects_to_hub":False,
     "episode":2,
     "connections":[{"target":"Suburbs (MAP16) Red","pro":False}]},

    # Tenements (MAP17)
    {"name":"Tenements (MAP17) Main",
     "connects_to_hub":True,
     "episode":2,
     "connections":[{"target":"Tenements (MAP17) Red","pro":False}]},
    {"name":"Tenements (MAP17) Blue",
     "connects_to_hub":False,
     "episode":2,
     "connections":[{"target":"Tenements (MAP17) Red","pro":False}]},
    {"name":"Tenements (MAP17) Yellow",
     "connects_to_hub":False,
     "episode":2,
     "connections":[
        {"target":"Tenements (MAP17) Red","pro":False},
        {"target":"Tenements (MAP17) Blue","pro":False}]},
    {"name":"Tenements (MAP17) Red",
     "connects_to_hub":False,
     "episode":2,
     "connections":[
        {"target":"Tenements (MAP17) Yellow","pro":False},
        {"target":"Tenements (MAP17) Blue","pro":False},
        {"target":"Tenements (MAP17) Main","pro":False}]},

    # The Courtyard (MAP18)
    {"name":"The Courtyard (MAP18) Main",
     "connects_to_hub":True,
     "episode":2,
     "connections":[
        {"target":"The Courtyard (MAP18) Yellow","pro":False},
        {"target":"The Courtyard (MAP18) Blue","pro":False}]},
    {"name":"The Courtyard (MAP18) Blue",
     "connects_to_hub":False,
     "episode":2,
     "connections":[{"target":"The Courtyard (MAP18) Main","pro":False}]},
    {"name":"The Courtyard (MAP18) Yellow",
     "connects_to_hub":False,
     "episode":2,
     "connections":[{"target":"The Courtyard (MAP18) Main","pro":False}]},

    # The Citadel (MAP19)
    {"name":"The Citadel (MAP19) Main",
     "connects_to_hub":True,
     "episode":2,
     "connections":[{"target":"The Citadel (MAP19) Red","pro":False}]},
    {"name":"The Citadel (MAP19) Red",
     "connects_to_hub":False,
     "episode":2,
     "connections":[{"target":"The Citadel (MAP19) Main","pro":False}]},

    # Gotcha! (MAP20)
    {"name":"Gotcha! (MAP20) Main",
     "connects_to_hub":True,
     "episode":2,
     "connections":[]},

    # Nirvana (MAP21)
    {"name":"Nirvana (MAP21) Main",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"Nirvana (MAP21) Yellow","pro":False}]},
    {"name":"Nirvana (MAP21) Yellow",
     "connects_to_hub":False,
     "episode":3,
     "connections":[
        {"target":"Nirvana (MAP21) Main","pro":False},
        {"target":"Nirvana (MAP21) Magenta","pro":False},
        {"target":"Nirvana (MAP21) Pro Magenta","pro":True}]},
    {"name":"Nirvana (MAP21) Magenta",
     "connects_to_hub":False,
     "episode":3,
     "connections":[
        {"target":"Nirvana (MAP21) Yellow","pro":False},
        {"target":"Nirvana (MAP21) Pro Magenta","pro":False}]},
    {"name":"Nirvana (MAP21) Start",
     "connects_to_hub":True,
     "episode":3,
     "connections":[{"target":"Nirvana (MAP21) Main","pro":False}]},
    {"name":"Nirvana (MAP21) Pro Magenta",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"Nirvana (MAP21) Magenta","pro":False}]},

    # The Catacombs (MAP22)
    {"name":"The Catacombs (MAP22) Main",
     "connects_to_hub":False,
     "episode":3,
     "connections":[
        {"target":"The Catacombs (MAP22) Blue","pro":False},
        {"target":"The Catacombs (MAP22) Red","pro":False},
        {"target":"The Catacombs (MAP22) Early","pro":False}]},
    {"name":"The Catacombs (MAP22) Blue",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"The Catacombs (MAP22) Main","pro":False}]},
    {"name":"The Catacombs (MAP22) Red",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"The Catacombs (MAP22) Main","pro":False}]},
    {"name":"The Catacombs (MAP22) Early",
     "connects_to_hub":True,
     "episode":3,
     "connections":[{"target":"The Catacombs (MAP22) Main","pro":False}]},

    # Barrels o' Fun (MAP23)
    {"name":"Barrels o' Fun (MAP23) Main",
     "connects_to_hub":True,
     "episode":3,
     "connections":[{"target":"Barrels o' Fun (MAP23) Yellow","pro":False}]},
    {"name":"Barrels o' Fun (MAP23) Yellow",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"Barrels o' Fun (MAP23) Main","pro":False}]},

    # The Chasm (MAP24)
    {"name":"The Chasm (MAP24) Main",
     "connects_to_hub":True,
     "episode":3,
     "connections":[
        {"target":"The Chasm (MAP24) Blue","pro":False},
        {"target":"The Chasm (MAP24) Blue Pro","pro":True}]},
    {"name":"The Chasm (MAP24) Red",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"The Chasm (MAP24) Blue","pro":False}]},
    {"name":"The Chasm (MAP24) Blue",
     "connects_to_hub":False,
     "episode":3,
     "connections":[
        {"target":"The Chasm (MAP24) Red","pro":False},
        {"target":"The Chasm (MAP24) Main","pro":False},
        {"target":"The Chasm (MAP24) Blue Pro","pro":False}]},
    {"name":"The Chasm (MAP24) Blue Pro",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"The Chasm (MAP24) Blue","pro":False}]},

    # Bloodfalls (MAP25)
    {"name":"Bloodfalls (MAP25) Main",
     "connects_to_hub":False,
     "episode":3,
     "connections":[
        {"target":"Bloodfalls (MAP25) Blue","pro":False},
        {"target":"Bloodfalls (MAP25) Start","pro":False}]},
    {"name":"Bloodfalls (MAP25) Blue",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"Bloodfalls (MAP25) Main","pro":False}]},
    {"name":"Bloodfalls (MAP25) Start",
     "connects_to_hub":True,
     "episode":3,
     "connections":[{"target":"Bloodfalls (MAP25) Main","pro":False}]},

    # The Abandoned Mines (MAP26)
    {"name":"The Abandoned Mines (MAP26) Main",
     "connects_to_hub":True,
     "episode":3,
     "connections":[
        {"target":"The Abandoned Mines (MAP26) Yellow","pro":False},
        {"target":"The Abandoned Mines (MAP26) Red","pro":False},
        {"target":"The Abandoned Mines (MAP26) Blue","pro":False}]},
    {"name":"The Abandoned Mines (MAP26) Blue",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"The Abandoned Mines (MAP26) Main","pro":False}]},
    {"name":"The Abandoned Mines (MAP26) Yellow",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"The Abandoned Mines (MAP26) Main","pro":False}]},
    {"name":"The Abandoned Mines (MAP26) Red",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"The Abandoned Mines (MAP26) Main","pro":False}]},

    # Monster Condo (MAP27)
    {"name":"Monster Condo (MAP27) Main",
     "connects_to_hub":True,
     "episode":3,
     "connections":[
        {"target":"Monster Condo (MAP27) Yellow","pro":False},
        {"target":"Monster Condo (MAP27) Red","pro":False},
        {"target":"Monster Condo (MAP27) Blue","pro":False}]},
    {"name":"Monster Condo (MAP27) Blue",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"Monster Condo (MAP27) Main","pro":False}]},
    {"name":"Monster Condo (MAP27) Yellow",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"Monster Condo (MAP27) Main","pro":False}]},
    {"name":"Monster Condo (MAP27) Red",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"Monster Condo (MAP27) Main","pro":False}]},

    # The Spirit World (MAP28)
    {"name":"The Spirit World (MAP28) Main",
     "connects_to_hub":True,
     "episode":3,
     "connections":[
        {"target":"The Spirit World (MAP28) Yellow","pro":False},
        {"target":"The Spirit World (MAP28) Red","pro":False}]},
    {"name":"The Spirit World (MAP28) Yellow",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"The Spirit World (MAP28) Main","pro":False}]},
    {"name":"The Spirit World (MAP28) Red",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"The Spirit World (MAP28) Main","pro":False}]},

    # The Living End (MAP29)
    {"name":"The Living End (MAP29) Main",
     "connects_to_hub":True,
     "episode":3,
     "connections":[]},

    # Icon of Sin (MAP30)
    {"name":"Icon of Sin (MAP30) Main",
     "connects_to_hub":False,
     "episode":3,
     "connections":[{"target":"Icon of Sin (MAP30) Start","pro":False}]},
    {"name":"Icon of Sin (MAP30) Start",
     "connects_to_hub":True,
     "episode":3,
     "connections":[{"target":"Icon of Sin (MAP30) Main","pro":False}]},

    # Wolfenstein (MAP31)
    {"name":"Wolfenstein (MAP31) Main",
     "connects_to_hub":True,
     "episode":4,
     "connections":[]},

    # Grosse (MAP32)
    {"name":"Grosse (MAP32) Main",
     "connects_to_hub":False,
     "episode":4,
     "connections":[{"target":"Grosse (MAP32) Start","pro":False}]},
    {"name":"Grosse (MAP32) Start",
     "connects_to_hub":True,
     "episode":4,
     "connections":[{"target":"Grosse (MAP32) Main","pro":False}]},
]
