from BaseClasses import MultiWorld


def connect_regions(multiworld: MultiWorld, player: int) -> None:
    """Connect all regions according to the world layout"""

    # I Tried creating a connection dictionary to then loop over to create the connections, but it would skip over connections so it hard coded.
    # This way does allow for easier lookups / changes

    multiworld.get_region("Arbiters Grounds Entrance", player).connect(
        multiworld.get_region("Outside Arbiters Grounds", player),
        "Arbiters Grounds Entrance -> Outside Arbiters Grounds",
    )

    multiworld.get_region("Arbiters Grounds Entrance", player).connect(
        multiworld.get_region("Arbiters Grounds Lobby", player),
        "Arbiters Grounds Entrance -> Arbiters Grounds Lobby",
    )

    multiworld.get_region("Arbiters Grounds Lobby", player).connect(
        multiworld.get_region("Arbiters Grounds Entrance", player),
        "Arbiters Grounds Lobby -> Arbiters Grounds Entrance",
    )

    multiworld.get_region("Arbiters Grounds Lobby", player).connect(
        multiworld.get_region("Arbiters Grounds East Wing", player),
        "Arbiters Grounds Lobby -> Arbiters Grounds East Wing",
    )

    multiworld.get_region("Arbiters Grounds Lobby", player).connect(
        multiworld.get_region("Arbiters Grounds West Wing", player),
        "Arbiters Grounds Lobby -> Arbiters Grounds West Wing",
    )

    multiworld.get_region("Arbiters Grounds Lobby", player).connect(
        multiworld.get_region("Arbiters Grounds After Poe Gate", player),
        "Arbiters Grounds Lobby -> Arbiters Grounds After Poe Gate",
    )

    multiworld.get_region("Arbiters Grounds East Wing", player).connect(
        multiworld.get_region("Arbiters Grounds Lobby", player),
        "Arbiters Grounds East Wing -> Arbiters Grounds Lobby",
    )

    multiworld.get_region("Arbiters Grounds West Wing", player).connect(
        multiworld.get_region("Arbiters Grounds Lobby", player),
        "Arbiters Grounds West Wing -> Arbiters Grounds Lobby",
    )

    multiworld.get_region("Arbiters Grounds After Poe Gate", player).connect(
        multiworld.get_region("Arbiters Grounds Lobby", player),
        "Arbiters Grounds After Poe Gate -> Arbiters Grounds Lobby",
    )

    multiworld.get_region("Arbiters Grounds After Poe Gate", player).connect(
        multiworld.get_region("Arbiters Grounds Boss Room", player),
        "Arbiters Grounds After Poe Gate -> Arbiters Grounds Boss Room",
    )

    multiworld.get_region("Arbiters Grounds Boss Room", player).connect(
        multiworld.get_region("Mirror Chamber Lower", player),
        "Arbiters Grounds Boss Room -> Mirror Chamber Lower",
    )

    multiworld.get_region("City in The Sky Boss Room", player).connect(
        multiworld.get_region("City in The Sky Entrance", player),
        "City in The Sky Boss Room -> City in The Sky Entrance",
    )

    multiworld.get_region("City in The Sky Central Tower Second Floor", player).connect(
        multiworld.get_region("City in The Sky West Wing", player),
        "City in The Sky Central Tower Second Floor -> City in The Sky West Wing",
    )

    multiworld.get_region("City in The Sky Central Tower Second Floor", player).connect(
        multiworld.get_region("City in The Sky Lobby", player),
        "City in The Sky Central Tower Second Floor -> City in The Sky Lobby",
    )

    multiworld.get_region("City in The Sky East Wing", player).connect(
        multiworld.get_region("City in The Sky Lobby", player),
        "City in The Sky East Wing -> City in The Sky Lobby",
    )

    multiworld.get_region("City in The Sky Entrance", player).connect(
        multiworld.get_region("Lake Hylia", player),
        "City in The Sky Entrance -> Lake Hylia",
    )

    multiworld.get_region("City in The Sky Entrance", player).connect(
        multiworld.get_region("City in The Sky Lobby", player),
        "City in The Sky Entrance -> City in The Sky Lobby",
    )

    multiworld.get_region("City in The Sky Lobby", player).connect(
        multiworld.get_region("City in The Sky Entrance", player),
        "City in The Sky Lobby -> City in The Sky Entrance",
    )

    multiworld.get_region("City in The Sky Lobby", player).connect(
        multiworld.get_region("City in The Sky East Wing", player),
        "City in The Sky Lobby -> City in The Sky East Wing",
    )

    multiworld.get_region("City in The Sky Lobby", player).connect(
        multiworld.get_region("City in The Sky West Wing", player),
        "City in The Sky Lobby -> City in The Sky West Wing",
    )

    multiworld.get_region("City in The Sky Lobby", player).connect(
        multiworld.get_region("City in The Sky Central Tower Second Floor", player),
        "City in The Sky Lobby -> City in The Sky Central Tower Second Floor",
    )

    multiworld.get_region("City in The Sky Lobby", player).connect(
        multiworld.get_region("City in The Sky North Wing", player),
        "City in The Sky Lobby -> City in The Sky North Wing",
    )

    multiworld.get_region("City in The Sky North Wing", player).connect(
        multiworld.get_region("City in The Sky Lobby", player),
        "City in The Sky North Wing -> City in The Sky Lobby",
    )

    multiworld.get_region("City in The Sky North Wing", player).connect(
        multiworld.get_region("City in The Sky Boss Room", player),
        "City in The Sky North Wing -> City in The Sky Boss Room",
    )

    multiworld.get_region("City in The Sky West Wing", player).connect(
        multiworld.get_region("City in The Sky Lobby", player),
        "City in The Sky West Wing -> City in The Sky Lobby",
    )

    multiworld.get_region("City in The Sky West Wing", player).connect(
        multiworld.get_region("City in The Sky Central Tower Second Floor", player),
        "City in The Sky West Wing -> City in The Sky Central Tower Second Floor",
    )

    multiworld.get_region("Forest Temple Boss Room", player).connect(
        multiworld.get_region("South Faron Woods", player),
        "Forest Temple Boss Room -> South Faron Woods",
    )

    multiworld.get_region("Forest Temple East Wing", player).connect(
        multiworld.get_region("Forest Temple Lobby", player),
        "Forest Temple East Wing -> Forest Temple Lobby",
    )

    multiworld.get_region("Forest Temple East Wing", player).connect(
        multiworld.get_region("Forest Temple North Wing", player),
        "Forest Temple East Wing -> Forest Temple North Wing",
    )

    multiworld.get_region("Forest Temple Entrance", player).connect(
        multiworld.get_region("North Faron Woods", player),
        "Forest Temple Entrance -> North Faron Woods",
    )

    multiworld.get_region("Forest Temple Entrance", player).connect(
        multiworld.get_region("Forest Temple Lobby", player),
        "Forest Temple Entrance -> Forest Temple Lobby",
    )

    multiworld.get_region("Forest Temple Lobby", player).connect(
        multiworld.get_region("Forest Temple Entrance", player),
        "Forest Temple Lobby -> Forest Temple Entrance",
    )

    multiworld.get_region("Forest Temple Lobby", player).connect(
        multiworld.get_region("Forest Temple East Wing", player),
        "Forest Temple Lobby -> Forest Temple East Wing",
    )

    multiworld.get_region("Forest Temple Lobby", player).connect(
        multiworld.get_region("Forest Temple West Wing", player),
        "Forest Temple Lobby -> Forest Temple West Wing",
    )

    multiworld.get_region("Forest Temple Lobby", player).connect(
        multiworld.get_region("Ook", player),
        "Forest Temple Lobby -> Ook",
    )

    multiworld.get_region("Forest Temple North Wing", player).connect(
        multiworld.get_region("Forest Temple East Wing", player),
        "Forest Temple North Wing -> Forest Temple East Wing",
    )

    multiworld.get_region("Forest Temple North Wing", player).connect(
        multiworld.get_region("Forest Temple Boss Room", player),
        "Forest Temple North Wing -> Forest Temple Boss Room",
    )

    multiworld.get_region("Forest Temple West Wing", player).connect(
        multiworld.get_region("Forest Temple Lobby", player),
        "Forest Temple West Wing -> Forest Temple Lobby",
    )

    multiworld.get_region("Forest Temple West Wing", player).connect(
        multiworld.get_region("Ook", player),
        "Forest Temple West Wing -> Ook",
    )

    multiworld.get_region("Ook", player).connect(
        multiworld.get_region("Forest Temple West Wing", player),
        "Ook -> Forest Temple West Wing",
    )

    multiworld.get_region("Goron Mines Boss Room", player).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Goron Mines Boss Room -> Lower Kakariko Village",
    )

    multiworld.get_region("Goron Mines Crystal Switch Room", player).connect(
        multiworld.get_region("Goron Mines Magnet Room", player),
        "Goron Mines Crystal Switch Room -> Goron Mines Magnet Room",
    )

    multiworld.get_region("Goron Mines Crystal Switch Room", player).connect(
        multiworld.get_region("Goron Mines North Wing", player),
        "Goron Mines Crystal Switch Room -> Goron Mines North Wing",
    )

    multiworld.get_region("Goron Mines Entrance", player).connect(
        multiworld.get_region("Death Mountain Sumo Hall Goron Mines Tunnel", player),
        "Goron Mines Entrance -> Death Mountain Sumo Hall Goron Mines Tunnel",
    )

    multiworld.get_region("Goron Mines Entrance", player).connect(
        multiworld.get_region("Goron Mines Magnet Room", player),
        "Goron Mines Entrance -> Goron Mines Magnet Room",
    )

    multiworld.get_region("Goron Mines Lower West Wing", player).connect(
        multiworld.get_region("Goron Mines Magnet Room", player),
        "Goron Mines Lower West Wing -> Goron Mines Magnet Room",
    )

    multiworld.get_region("Goron Mines Magnet Room", player).connect(
        multiworld.get_region("Goron Mines Entrance", player),
        "Goron Mines Magnet Room -> Goron Mines Entrance",
    )

    multiworld.get_region("Goron Mines Magnet Room", player).connect(
        multiworld.get_region("Goron Mines Lower West Wing", player),
        "Goron Mines Magnet Room -> Goron Mines Lower West Wing",
    )

    multiworld.get_region("Goron Mines Magnet Room", player).connect(
        multiworld.get_region("Goron Mines Crystal Switch Room", player),
        "Goron Mines Magnet Room -> Goron Mines Crystal Switch Room",
    )

    multiworld.get_region("Goron Mines North Wing", player).connect(
        multiworld.get_region("Goron Mines Crystal Switch Room", player),
        "Goron Mines North Wing -> Goron Mines Crystal Switch Room",
    )

    multiworld.get_region("Goron Mines North Wing", player).connect(
        multiworld.get_region("Goron Mines Upper East Wing", player),
        "Goron Mines North Wing -> Goron Mines Upper East Wing",
    )

    multiworld.get_region("Goron Mines North Wing", player).connect(
        multiworld.get_region("Goron Mines Boss Room", player),
        "Goron Mines North Wing -> Goron Mines Boss Room",
    )

    multiworld.get_region("Goron Mines Upper East Wing", player).connect(
        multiworld.get_region("Goron Mines North Wing", player),
        "Goron Mines Upper East Wing -> Goron Mines North Wing",
    )

    multiworld.get_region("Goron Mines Upper East Wing", player).connect(
        multiworld.get_region("Goron Mines Magnet Room", player),
        "Goron Mines Upper East Wing -> Goron Mines Magnet Room",
    )

    multiworld.get_region("Ganondorf Castle", player).connect(
        multiworld.get_region("Hyrule Castle Tower Climb", player),
        "Ganondorf Castle -> Hyrule Castle Tower Climb",
    )

    multiworld.get_region("Hyrule Castle Entrance", player).connect(
        multiworld.get_region("Castle Town North Inside Barrier", player),
        "Hyrule Castle Entrance -> Castle Town North Inside Barrier",
    )

    multiworld.get_region("Hyrule Castle Entrance", player).connect(
        multiworld.get_region("Hyrule Castle Main Hall", player),
        "Hyrule Castle Entrance -> Hyrule Castle Main Hall",
    )

    multiworld.get_region("Hyrule Castle Entrance", player).connect(
        multiworld.get_region("Hyrule Castle Outside West Wing", player),
        "Hyrule Castle Entrance -> Hyrule Castle Outside West Wing",
    )

    multiworld.get_region("Hyrule Castle Entrance", player).connect(
        multiworld.get_region("Hyrule Castle Outside East Wing", player),
        "Hyrule Castle Entrance -> Hyrule Castle Outside East Wing",
    )

    multiworld.get_region("Hyrule Castle Graveyard", player).connect(
        multiworld.get_region("Hyrule Castle Outside East Wing", player),
        "Hyrule Castle Graveyard -> Hyrule Castle Outside East Wing",
    )

    multiworld.get_region("Hyrule Castle Inside East Wing", player).connect(
        multiworld.get_region("Hyrule Castle Main Hall", player),
        "Hyrule Castle Inside East Wing -> Hyrule Castle Main Hall",
    )

    multiworld.get_region("Hyrule Castle Inside East Wing", player).connect(
        multiworld.get_region("Hyrule Castle Third Floor Balcony", player),
        "Hyrule Castle Inside East Wing -> Hyrule Castle Third Floor Balcony",
    )

    multiworld.get_region("Hyrule Castle Inside West Wing", player).connect(
        multiworld.get_region("Hyrule Castle Main Hall", player),
        "Hyrule Castle Inside West Wing -> Hyrule Castle Main Hall",
    )

    multiworld.get_region("Hyrule Castle Inside West Wing", player).connect(
        multiworld.get_region("Hyrule Castle Third Floor Balcony", player),
        "Hyrule Castle Inside West Wing -> Hyrule Castle Third Floor Balcony",
    )

    multiworld.get_region("Hyrule Castle Main Hall", player).connect(
        multiworld.get_region("Hyrule Castle Entrance", player),
        "Hyrule Castle Main Hall -> Hyrule Castle Entrance",
    )

    multiworld.get_region("Hyrule Castle Main Hall", player).connect(
        multiworld.get_region("Hyrule Castle Inside East Wing", player),
        "Hyrule Castle Main Hall -> Hyrule Castle Inside East Wing",
    )

    multiworld.get_region("Hyrule Castle Main Hall", player).connect(
        multiworld.get_region("Hyrule Castle Inside West Wing", player),
        "Hyrule Castle Main Hall -> Hyrule Castle Inside West Wing",
    )

    multiworld.get_region("Hyrule Castle Outside East Wing", player).connect(
        multiworld.get_region("Hyrule Castle Entrance", player),
        "Hyrule Castle Outside East Wing -> Hyrule Castle Entrance",
    )

    multiworld.get_region("Hyrule Castle Outside East Wing", player).connect(
        multiworld.get_region("Hyrule Castle Graveyard", player),
        "Hyrule Castle Outside East Wing -> Hyrule Castle Graveyard",
    )

    multiworld.get_region("Hyrule Castle Outside West Wing", player).connect(
        multiworld.get_region("Hyrule Castle Entrance", player),
        "Hyrule Castle Outside West Wing -> Hyrule Castle Entrance",
    )

    multiworld.get_region("Hyrule Castle Third Floor Balcony", player).connect(
        multiworld.get_region("Hyrule Castle Inside West Wing", player),
        "Hyrule Castle Third Floor Balcony -> Hyrule Castle Inside West Wing",
    )

    multiworld.get_region("Hyrule Castle Third Floor Balcony", player).connect(
        multiworld.get_region("Hyrule Castle Inside East Wing", player),
        "Hyrule Castle Third Floor Balcony -> Hyrule Castle Inside East Wing",
    )

    multiworld.get_region("Hyrule Castle Third Floor Balcony", player).connect(
        multiworld.get_region("Hyrule Castle Tower Climb", player),
        "Hyrule Castle Third Floor Balcony -> Hyrule Castle Tower Climb",
    )

    multiworld.get_region("Hyrule Castle Tower Climb", player).connect(
        multiworld.get_region("Hyrule Castle Third Floor Balcony", player),
        "Hyrule Castle Tower Climb -> Hyrule Castle Third Floor Balcony",
    )

    multiworld.get_region("Hyrule Castle Tower Climb", player).connect(
        multiworld.get_region("Hyrule Castle Treasure Room", player),
        "Hyrule Castle Tower Climb -> Hyrule Castle Treasure Room",
    )

    multiworld.get_region("Hyrule Castle Tower Climb", player).connect(
        multiworld.get_region("Ganondorf Castle", player),
        "Hyrule Castle Tower Climb -> Ganondorf Castle",
    )

    multiworld.get_region("Hyrule Castle Treasure Room", player).connect(
        multiworld.get_region("Hyrule Castle Tower Climb", player),
        "Hyrule Castle Treasure Room -> Hyrule Castle Tower Climb",
    )

    multiworld.get_region("Lakebed Temple Boss Room", player).connect(
        multiworld.get_region("Lake Hylia Lanayru Spring", player),
        "Lakebed Temple Boss Room -> Lake Hylia Lanayru Spring",
    )

    multiworld.get_region("Lakebed Temple Central Room", player).connect(
        multiworld.get_region("Lakebed Temple Entrance", player),
        "Lakebed Temple Central Room -> Lakebed Temple Entrance",
    )

    multiworld.get_region("Lakebed Temple Central Room", player).connect(
        multiworld.get_region("Lakebed Temple East Wing Second Floor", player),
        "Lakebed Temple Central Room -> Lakebed Temple East Wing Second Floor",
    )

    multiworld.get_region("Lakebed Temple Central Room", player).connect(
        multiworld.get_region("Lakebed Temple East Wing First Floor", player),
        "Lakebed Temple Central Room -> Lakebed Temple East Wing First Floor",
    )

    multiworld.get_region("Lakebed Temple Central Room", player).connect(
        multiworld.get_region("Lakebed Temple West Wing", player),
        "Lakebed Temple Central Room -> Lakebed Temple West Wing",
    )

    multiworld.get_region("Lakebed Temple Central Room", player).connect(
        multiworld.get_region("Lakebed Temple Boss Room", player),
        "Lakebed Temple Central Room -> Lakebed Temple Boss Room",
    )

    multiworld.get_region("Lakebed Temple East Wing First Floor", player).connect(
        multiworld.get_region("Lakebed Temple Central Room", player),
        "Lakebed Temple East Wing First Floor -> Lakebed Temple Central Room",
    )

    multiworld.get_region("Lakebed Temple East Wing Second Floor", player).connect(
        multiworld.get_region("Lakebed Temple Central Room", player),
        "Lakebed Temple East Wing Second Floor -> Lakebed Temple Central Room",
    )

    multiworld.get_region("Lakebed Temple East Wing Second Floor", player).connect(
        multiworld.get_region("Lakebed Temple East Wing First Floor", player),
        "Lakebed Temple East Wing Second Floor -> Lakebed Temple East Wing First Floor",
    )

    multiworld.get_region("Lakebed Temple Entrance", player).connect(
        multiworld.get_region("Lake Hylia Lakebed Temple Entrance", player),
        "Lakebed Temple Entrance -> Lake Hylia Lakebed Temple Entrance",
    )

    multiworld.get_region("Lakebed Temple Entrance", player).connect(
        multiworld.get_region("Lakebed Temple Central Room", player),
        "Lakebed Temple Entrance -> Lakebed Temple Central Room",
    )

    multiworld.get_region("Lakebed Temple West Wing", player).connect(
        multiworld.get_region("Lakebed Temple Central Room", player),
        "Lakebed Temple West Wing -> Lakebed Temple Central Room",
    )

    multiworld.get_region("Palace of Twilight Entrance", player).connect(
        multiworld.get_region("Mirror Chamber Upper", player),
        "Palace of Twilight Entrance -> Mirror Chamber Upper",
    )

    multiworld.get_region("Palace of Twilight Entrance", player).connect(
        multiworld.get_region("Palace of Twilight West Wing", player),
        "Palace of Twilight Entrance -> Palace of Twilight West Wing",
    )

    multiworld.get_region("Palace of Twilight Entrance", player).connect(
        multiworld.get_region("Palace of Twilight East Wing", player),
        "Palace of Twilight Entrance -> Palace of Twilight East Wing",
    )

    multiworld.get_region("Palace of Twilight Entrance", player).connect(
        multiworld.get_region("Palace of Twilight Central First Room", player),
        "Palace of Twilight Entrance -> Palace of Twilight Central First Room",
    )

    multiworld.get_region("Palace of Twilight West Wing", player).connect(
        multiworld.get_region("Palace of Twilight Entrance", player),
        "Palace of Twilight West Wing -> Palace of Twilight Entrance",
    )

    multiworld.get_region("Palace of Twilight East Wing", player).connect(
        multiworld.get_region("Palace of Twilight Entrance", player),
        "Palace of Twilight East Wing -> Palace of Twilight Entrance",
    )

    multiworld.get_region("Palace of Twilight Central First Room", player).connect(
        multiworld.get_region("Palace of Twilight Entrance", player),
        "Palace of Twilight Central First Room -> Palace of Twilight Entrance",
    )

    multiworld.get_region("Palace of Twilight Central First Room", player).connect(
        multiworld.get_region("Palace of Twilight Outside Room", player),
        "Palace of Twilight Central First Room -> Palace of Twilight Outside Room",
    )

    multiworld.get_region("Palace of Twilight Outside Room", player).connect(
        multiworld.get_region("Palace of Twilight Central First Room", player),
        "Palace of Twilight Outside Room -> Palace of Twilight Central First Room",
    )

    multiworld.get_region("Palace of Twilight Outside Room", player).connect(
        multiworld.get_region("Palace of Twilight North Tower", player),
        "Palace of Twilight Outside Room -> Palace of Twilight North Tower",
    )

    multiworld.get_region("Palace of Twilight North Tower", player).connect(
        multiworld.get_region("Palace of Twilight Outside Room", player),
        "Palace of Twilight North Tower -> Palace of Twilight Outside Room",
    )

    multiworld.get_region("Palace of Twilight North Tower", player).connect(
        multiworld.get_region("Palace of Twilight Boss Room", player),
        "Palace of Twilight North Tower -> Palace of Twilight Boss Room",
    )

    multiworld.get_region("Palace of Twilight Boss Room", player).connect(
        multiworld.get_region("Palace of Twilight Entrance", player),
        "Palace of Twilight Boss Room -> Palace of Twilight Entrance",
    )

    multiworld.get_region("Snowpeak Ruins Left Door", player).connect(
        multiworld.get_region("Snowpeak Ruins Entrance", player),
        "Snowpeak Ruins Left Door -> Snowpeak Ruins Entrance",
    )

    multiworld.get_region("Snowpeak Ruins Left Door", player).connect(
        multiworld.get_region("Snowpeak Summit Lower", player),
        "Snowpeak Ruins Left Door -> Snowpeak Summit Lower",
    )

    multiworld.get_region("Snowpeak Ruins Right Door", player).connect(
        multiworld.get_region("Snowpeak Ruins Entrance", player),
        "Snowpeak Ruins Right Door -> Snowpeak Ruins Entrance",
    )

    multiworld.get_region("Snowpeak Ruins Right Door", player).connect(
        multiworld.get_region("Snowpeak Summit Lower", player),
        "Snowpeak Ruins Right Door -> Snowpeak Summit Lower",
    )

    multiworld.get_region("Snowpeak Ruins Boss Room", player).connect(
        multiworld.get_region("Snowpeak Summit Lower", player),
        "Snowpeak Ruins Boss Room -> Snowpeak Summit Lower",
    )

    multiworld.get_region("Snowpeak Ruins Caged Freezard Room", player).connect(
        multiworld.get_region("Snowpeak Ruins Yeto and Yeta", player),
        "Snowpeak Ruins Caged Freezard Room -> Snowpeak Ruins Yeto and Yeta",
    )

    multiworld.get_region("Snowpeak Ruins Caged Freezard Room", player).connect(
        multiworld.get_region("Snowpeak Ruins Second Floor Mini Freezard Room", player),
        "Snowpeak Ruins Caged Freezard Room -> Snowpeak Ruins Second Floor Mini Freezard Room",
    )

    multiworld.get_region("Snowpeak Ruins Caged Freezard Room", player).connect(
        multiworld.get_region("Snowpeak Ruins Wooden Beam Room", player),
        "Snowpeak Ruins Caged Freezard Room -> Snowpeak Ruins Wooden Beam Room",
    )

    multiworld.get_region("Snowpeak Ruins Caged Freezard Room", player).connect(
        multiworld.get_region("Snowpeak Ruins West Courtyard", player),
        "Snowpeak Ruins Caged Freezard Room -> Snowpeak Ruins West Courtyard",
    )

    multiworld.get_region("Snowpeak Ruins Caged Freezard Room", player).connect(
        multiworld.get_region("Snowpeak Ruins Chapel", player),
        "Snowpeak Ruins Caged Freezard Room -> Snowpeak Ruins Chapel",
    )
    multiworld.get_region("Snowpeak Ruins Caged Freezard Room", player).connect(
        multiworld.get_region("Snowpeak Ruins Boss Room", player),
        "Snowpeak Ruins Caged Freezard Room -> Snowpeak Ruins Boss Room",
    )
    multiworld.get_region("Snowpeak Ruins Caged Freezard Room", player).connect(
        multiworld.get_region("Snowpeak Ruins Caged Freezard Room Lower", player),
        "Snowpeak Ruins Caged Freezard Room -> Snowpeak Ruins Caged Freezard Room Lower",
    )

    multiworld.get_region("Snowpeak Ruins Caged Freezard Room Lower", player).connect(
        multiworld.get_region("Snowpeak Ruins Caged Freezard Room", player),
        "Snowpeak Ruins Caged Freezard Room Lower -> Snowpeak Ruins Caged Freezard Room",
    )

    multiworld.get_region("Snowpeak Ruins Caged Freezard Room Lower", player).connect(
        multiworld.get_region("Snowpeak Ruins Entrance", player),
        "Snowpeak Ruins Caged Freezard Room Lower -> Snowpeak Ruins Entrance",
    )

    multiworld.get_region("Snowpeak Ruins Chapel", player).connect(
        multiworld.get_region("Snowpeak Ruins West Courtyard", player),
        "Snowpeak Ruins Chapel -> Snowpeak Ruins West Courtyard",
    )

    multiworld.get_region("Snowpeak Ruins Darkhammer Room", player).connect(
        multiworld.get_region("Snowpeak Ruins West Courtyard", player),
        "Snowpeak Ruins Darkhammer Room -> Snowpeak Ruins West Courtyard",
    )

    multiworld.get_region("Snowpeak Ruins East Courtyard", player).connect(
        multiworld.get_region("Snowpeak Ruins Yeto and Yeta", player),
        "Snowpeak Ruins East Courtyard -> Snowpeak Ruins Yeto and Yeta",
    )

    multiworld.get_region("Snowpeak Ruins East Courtyard", player).connect(
        multiworld.get_region("Snowpeak Ruins West Courtyard", player),
        "Snowpeak Ruins East Courtyard -> Snowpeak Ruins West Courtyard",
    )

    multiworld.get_region("Snowpeak Ruins East Courtyard", player).connect(
        multiworld.get_region(
            "Snowpeak Ruins Northeast Chilfos Room First Floor", player
        ),
        "Snowpeak Ruins East Courtyard -> Snowpeak Ruins Northeast Chilfos Room First Floor",
    )

    multiworld.get_region("Snowpeak Ruins Entrance", player).connect(
        multiworld.get_region("Snowpeak Ruins Left Door", player),
        "Snowpeak Ruins Entrance -> Snowpeak Ruins Left Door",
    )

    multiworld.get_region("Snowpeak Ruins Entrance", player).connect(
        multiworld.get_region("Snowpeak Ruins Right Door", player),
        "Snowpeak Ruins Entrance -> Snowpeak Ruins Right Door",
    )

    multiworld.get_region("Snowpeak Ruins Entrance", player).connect(
        multiworld.get_region("Snowpeak Ruins Yeto and Yeta", player),
        "Snowpeak Ruins Entrance -> Snowpeak Ruins Yeto and Yeta",
    )

    multiworld.get_region("Snowpeak Ruins Entrance", player).connect(
        multiworld.get_region("Snowpeak Ruins Caged Freezard Room Lower", player),
        "Snowpeak Ruins Entrance -> Snowpeak Ruins Caged Freezard Room Lower",
    )

    multiworld.get_region(
        "Snowpeak Ruins Northeast Chilfos Room First Floor", player
    ).connect(
        multiworld.get_region("Snowpeak Ruins East Courtyard", player),
        "Snowpeak Ruins Northeast Chilfos Room First Floor -> Snowpeak Ruins East Courtyard",
    )
    multiworld.get_region(
        "Snowpeak Ruins Northeast Chilfos Room First Floor", player
    ).connect(
        multiworld.get_region(
            "Snowpeak Ruins Northeast Chilfos Room Second Floor", player
        ),
        "Snowpeak Ruins Northeast Chilfos Room First Floor -> Snowpeak Ruins Northeast Chilfos Room Second Floor",
    )

    multiworld.get_region(
        "Snowpeak Ruins Northeast Chilfos Room First Floor", player
    ).connect(
        multiworld.get_region("Snowpeak Ruins Yeto and Yeta", player),
        "Snowpeak Ruins Northeast Chilfos Room First Floor -> Snowpeak Ruins Yeto and Yeta",
    )

    multiworld.get_region(
        "Snowpeak Ruins Northeast Chilfos Room Second Floor", player
    ).connect(
        multiworld.get_region(
            "Snowpeak Ruins Northeast Chilfos Room First Floor", player
        ),
        "Snowpeak Ruins Northeast Chilfos Room Second Floor -> Snowpeak Ruins Northeast Chilfos Room First Floor",
    )

    multiworld.get_region(
        "Snowpeak Ruins Northeast Chilfos Room Second Floor", player
    ).connect(
        multiworld.get_region("Snowpeak Ruins Yeto and Yeta", player),
        "Snowpeak Ruins Northeast Chilfos Room Second Floor -> Snowpeak Ruins Yeto and Yeta",
    )

    multiworld.get_region(
        "Snowpeak Ruins Second Floor Mini Freezard Room", player
    ).connect(
        multiworld.get_region("Snowpeak Ruins Entrance", player),
        "Snowpeak Ruins Second Floor Mini Freezard Room -> Snowpeak Ruins Entrance",
    )
    multiworld.get_region(
        "Snowpeak Ruins Second Floor Mini Freezard Room", player
    ).connect(
        multiworld.get_region("Snowpeak Ruins Yeto and Yeta", player),
        "Snowpeak Ruins Second Floor Mini Freezard Room -> Snowpeak Ruins Yeto and Yeta",
    )

    multiworld.get_region(
        "Snowpeak Ruins Second Floor Mini Freezard Room", player
    ).connect(
        multiworld.get_region("Snowpeak Ruins East Courtyard", player),
        "Snowpeak Ruins Second Floor Mini Freezard Room -> Snowpeak Ruins East Courtyard",
    )

    multiworld.get_region(
        "Snowpeak Ruins Second Floor Mini Freezard Room", player
    ).connect(
        multiworld.get_region(
            "Snowpeak Ruins Northeast Chilfos Room Second Floor", player
        ),
        "Snowpeak Ruins Second Floor Mini Freezard Room -> Snowpeak Ruins Northeast Chilfos Room Second Floor",
    )

    multiworld.get_region(
        "Snowpeak Ruins Second Floor Mini Freezard Room", player
    ).connect(
        multiworld.get_region("Snowpeak Ruins Caged Freezard Room", player),
        "Snowpeak Ruins Second Floor Mini Freezard Room -> Snowpeak Ruins Caged Freezard Room",
    )

    multiworld.get_region("Snowpeak Ruins West Cannon Room", player).connect(
        multiworld.get_region("Snowpeak Ruins West Courtyard", player),
        "Snowpeak Ruins West Cannon Room -> Snowpeak Ruins West Courtyard",
    )

    multiworld.get_region("Snowpeak Ruins West Cannon Room", player).connect(
        multiworld.get_region("Snowpeak Ruins Wooden Beam Room", player),
        "Snowpeak Ruins West Cannon Room -> Snowpeak Ruins Wooden Beam Room",
    )

    multiworld.get_region("Snowpeak Ruins West Courtyard", player).connect(
        multiworld.get_region("Snowpeak Ruins Yeto and Yeta", player),
        "Snowpeak Ruins West Courtyard -> Snowpeak Ruins Yeto and Yeta",
    )

    multiworld.get_region("Snowpeak Ruins West Courtyard", player).connect(
        multiworld.get_region("Snowpeak Ruins East Courtyard", player),
        "Snowpeak Ruins West Courtyard -> Snowpeak Ruins East Courtyard",
    )

    multiworld.get_region("Snowpeak Ruins West Courtyard", player).connect(
        multiworld.get_region("Snowpeak Ruins West Cannon Room", player),
        "Snowpeak Ruins West Courtyard -> Snowpeak Ruins West Cannon Room",
    )

    multiworld.get_region("Snowpeak Ruins West Courtyard", player).connect(
        multiworld.get_region("Snowpeak Ruins Chapel", player),
        "Snowpeak Ruins West Courtyard -> Snowpeak Ruins Chapel",
    )

    multiworld.get_region("Snowpeak Ruins West Courtyard", player).connect(
        multiworld.get_region("Snowpeak Ruins Darkhammer Room", player),
        "Snowpeak Ruins West Courtyard -> Snowpeak Ruins Darkhammer Room",
    )

    multiworld.get_region("Snowpeak Ruins West Courtyard", player).connect(
        multiworld.get_region("Snowpeak Ruins Boss Room", player),
        "Snowpeak Ruins West Courtyard -> Snowpeak Ruins Boss Room",
    )

    multiworld.get_region("Snowpeak Ruins Wooden Beam Room", player).connect(
        multiworld.get_region("Snowpeak Ruins West Cannon Room", player),
        "Snowpeak Ruins Wooden Beam Room -> Snowpeak Ruins West Cannon Room",
    )

    multiworld.get_region("Snowpeak Ruins Yeto and Yeta", player).connect(
        multiworld.get_region("Snowpeak Ruins Entrance", player),
        "Snowpeak Ruins Yeto and Yeta -> Snowpeak Ruins Entrance",
    )

    multiworld.get_region("Snowpeak Ruins Yeto and Yeta", player).connect(
        multiworld.get_region("Snowpeak Ruins Caged Freezard Room", player),
        "Snowpeak Ruins Yeto and Yeta -> Snowpeak Ruins Caged Freezard Room",
    )

    multiworld.get_region("Snowpeak Ruins Yeto and Yeta", player).connect(
        multiworld.get_region("Snowpeak Ruins West Courtyard", player),
        "Snowpeak Ruins Yeto and Yeta -> Snowpeak Ruins West Courtyard",
    )

    multiworld.get_region("Snowpeak Ruins Yeto and Yeta", player).connect(
        multiworld.get_region("Snowpeak Ruins East Courtyard", player),
        "Snowpeak Ruins Yeto and Yeta -> Snowpeak Ruins East Courtyard",
    )

    multiworld.get_region("Temple of Time Armos Antechamber", player).connect(
        multiworld.get_region("Temple of Time Central Mechanical Platform", player),
        "Temple of Time Armos Antechamber -> Temple of Time Central Mechanical Platform",
    )

    multiworld.get_region("Temple of Time Boss Room", player).connect(
        multiworld.get_region("Sacred Grove Past", player),
        "Temple of Time Boss Room -> Sacred Grove Past",
    )

    multiworld.get_region("Temple of Time Central Mechanical Platform", player).connect(
        multiworld.get_region("Temple of Time Connecting Corridors", player),
        "Temple of Time Central Mechanical Platform -> Temple of Time Connecting Corridors",
    )

    multiworld.get_region("Temple of Time Central Mechanical Platform", player).connect(
        multiworld.get_region("Temple of Time Armos Antechamber", player),
        "Temple of Time Central Mechanical Platform -> Temple of Time Armos Antechamber",
    )

    multiworld.get_region("Temple of Time Central Mechanical Platform", player).connect(
        multiworld.get_region("Temple of Time Moving Wall Hallways", player),
        "Temple of Time Central Mechanical Platform -> Temple of Time Moving Wall Hallways",
    )

    multiworld.get_region("Temple of Time Connecting Corridors", player).connect(
        multiworld.get_region("Temple of Time Entrance", player),
        "Temple of Time Connecting Corridors -> Temple of Time Entrance",
    )

    multiworld.get_region("Temple of Time Connecting Corridors", player).connect(
        multiworld.get_region("Temple of Time Central Mechanical Platform", player),
        "Temple of Time Connecting Corridors -> Temple of Time Central Mechanical Platform",
    )

    multiworld.get_region("Temple of Time Crumbling Corridor", player).connect(
        multiworld.get_region("Temple of Time Entrance", player),
        "Temple of Time Crumbling Corridor -> Temple of Time Entrance",
    )

    multiworld.get_region("Temple of Time Crumbling Corridor", player).connect(
        multiworld.get_region("Temple of Time Boss Room", player),
        "Temple of Time Crumbling Corridor -> Temple of Time Boss Room",
    )

    multiworld.get_region("Temple of Time Darknut Arena", player).connect(
        multiworld.get_region("Temple of Time Upper Spike Trap Corridor", player),
        "Temple of Time Darknut Arena -> Temple of Time Upper Spike Trap Corridor",
    )

    multiworld.get_region("Temple of Time Entrance", player).connect(
        multiworld.get_region("Sacred Grove Past Behind Window", player),
        "Temple of Time Entrance -> Sacred Grove Past Behind Window",
    )

    multiworld.get_region("Temple of Time Entrance", player).connect(
        multiworld.get_region("Temple of Time Connecting Corridors", player),
        "Temple of Time Entrance -> Temple of Time Connecting Corridors",
    )

    multiworld.get_region("Temple of Time Entrance", player).connect(
        multiworld.get_region("Temple of Time Crumbling Corridor", player),
        "Temple of Time Entrance -> Temple of Time Crumbling Corridor",
    )

    multiworld.get_region("Temple of Time Floor Switch Puzzle Room", player).connect(
        multiworld.get_region("Temple of Time Scales of Time", player),
        "Temple of Time Floor Switch Puzzle Room -> Temple of Time Scales of Time",
    )

    multiworld.get_region("Temple of Time Moving Wall Hallways", player).connect(
        multiworld.get_region("Temple of Time Central Mechanical Platform", player),
        "Temple of Time Moving Wall Hallways -> Temple of Time Central Mechanical Platform",
    )

    multiworld.get_region("Temple of Time Moving Wall Hallways", player).connect(
        multiworld.get_region("Temple of Time Scales of Time", player),
        "Temple of Time Moving Wall Hallways -> Temple of Time Scales of Time",
    )

    multiworld.get_region("Temple of Time Scales of Time", player).connect(
        multiworld.get_region("Temple of Time Moving Wall Hallways", player),
        "Temple of Time Scales of Time -> Temple of Time Moving Wall Hallways",
    )

    multiworld.get_region("Temple of Time Scales of Time", player).connect(
        multiworld.get_region("Temple of Time Floor Switch Puzzle Room", player),
        "Temple of Time Scales of Time -> Temple of Time Floor Switch Puzzle Room",
    )

    multiworld.get_region("Temple of Time Scales of Time", player).connect(
        multiworld.get_region("Temple of Time Upper Spike Trap Corridor", player),
        "Temple of Time Scales of Time -> Temple of Time Upper Spike Trap Corridor",
    )

    multiworld.get_region("Temple of Time Upper Spike Trap Corridor", player).connect(
        multiworld.get_region("Temple of Time Scales of Time", player),
        "Temple of Time Upper Spike Trap Corridor -> Temple of Time Scales of Time",
    )

    multiworld.get_region("Temple of Time Upper Spike Trap Corridor", player).connect(
        multiworld.get_region("Temple of Time Darknut Arena", player),
        "Temple of Time Upper Spike Trap Corridor -> Temple of Time Darknut Arena",
    )

    multiworld.get_region("Death Mountain Near Kakariko", player).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Death Mountain Near Kakariko -> Lower Kakariko Village",
    )

    multiworld.get_region("Death Mountain Near Kakariko", player).connect(
        multiworld.get_region("Death Mountain Trail", player),
        "Death Mountain Near Kakariko -> Death Mountain Trail",
    )

    multiworld.get_region("Death Mountain Trail", player).connect(
        multiworld.get_region("Death Mountain Near Kakariko", player),
        "Death Mountain Trail -> Death Mountain Near Kakariko",
    )

    multiworld.get_region("Death Mountain Trail", player).connect(
        multiworld.get_region("Death Mountain Volcano", player),
        "Death Mountain Trail -> Death Mountain Volcano",
    )

    multiworld.get_region("Death Mountain Volcano", player).connect(
        multiworld.get_region("Death Mountain Trail", player),
        "Death Mountain Volcano -> Death Mountain Trail",
    )

    multiworld.get_region("Death Mountain Volcano", player).connect(
        multiworld.get_region("Death Mountain Outside Sumo Hall", player),
        "Death Mountain Volcano -> Death Mountain Outside Sumo Hall",
    )

    multiworld.get_region("Death Mountain Volcano", player).connect(
        multiworld.get_region("Death Mountain Elevator Lower", player),
        "Death Mountain Volcano -> Death Mountain Elevator Lower",
    )

    multiworld.get_region("Death Mountain Outside Sumo Hall", player).connect(
        multiworld.get_region("Death Mountain Volcano", player),
        "Death Mountain Outside Sumo Hall -> Death Mountain Volcano",
    )

    multiworld.get_region("Death Mountain Outside Sumo Hall", player).connect(
        multiworld.get_region("Death Mountain Sumo Hall", player),
        "Death Mountain Outside Sumo Hall -> Death Mountain Sumo Hall",
    )

    multiworld.get_region("Death Mountain Elevator Lower", player).connect(
        multiworld.get_region("Death Mountain Volcano", player),
        "Death Mountain Elevator Lower -> Death Mountain Volcano",
    )

    multiworld.get_region("Death Mountain Elevator Lower", player).connect(
        multiworld.get_region("Death Mountain Sumo Hall Elevator", player),
        "Death Mountain Elevator Lower -> Death Mountain Sumo Hall Elevator",
    )

    multiworld.get_region("Death Mountain Sumo Hall", player).connect(
        multiworld.get_region("Death Mountain Outside Sumo Hall", player),
        "Death Mountain Sumo Hall -> Death Mountain Outside Sumo Hall",
    )

    multiworld.get_region("Death Mountain Sumo Hall", player).connect(
        multiworld.get_region("Death Mountain Sumo Hall Elevator", player),
        "Death Mountain Sumo Hall -> Death Mountain Sumo Hall Elevator",
    )

    multiworld.get_region("Death Mountain Sumo Hall", player).connect(
        multiworld.get_region("Death Mountain Sumo Hall Goron Mines Tunnel", player),
        "Death Mountain Sumo Hall -> Death Mountain Sumo Hall Goron Mines Tunnel",
    )

    multiworld.get_region("Death Mountain Sumo Hall Elevator", player).connect(
        multiworld.get_region("Death Mountain Elevator Lower", player),
        "Death Mountain Sumo Hall Elevator -> Death Mountain Elevator Lower",
    )

    multiworld.get_region("Death Mountain Sumo Hall Elevator", player).connect(
        multiworld.get_region("Death Mountain Sumo Hall", player),
        "Death Mountain Sumo Hall Elevator -> Death Mountain Sumo Hall",
    )

    multiworld.get_region(
        "Death Mountain Sumo Hall Goron Mines Tunnel", player
    ).connect(
        multiworld.get_region("Death Mountain Sumo Hall", player),
        "Death Mountain Sumo Hall Goron Mines Tunnel -> Death Mountain Sumo Hall",
    )

    multiworld.get_region(
        "Death Mountain Sumo Hall Goron Mines Tunnel", player
    ).connect(
        multiworld.get_region("Goron Mines Entrance", player),
        "Death Mountain Sumo Hall Goron Mines Tunnel -> Goron Mines Entrance",
    )

    multiworld.get_region("Hidden Village", player).connect(
        multiworld.get_region("Eldin Field Outside Hidden Village", player),
        "Hidden Village -> Eldin Field Outside Hidden Village",
    )

    multiworld.get_region("Hidden Village", player).connect(
        multiworld.get_region("Hidden Village Impaz House", player),
        "Hidden Village -> Hidden Village Impaz House",
    )

    multiworld.get_region("Hidden Village Impaz House", player).connect(
        multiworld.get_region("Hidden Village", player),
        "Hidden Village Impaz House -> Hidden Village",
    )

    multiworld.get_region("Kakariko Gorge", player).connect(
        multiworld.get_region("Kakariko Gorge Cave Entrance", player),
        "Kakariko Gorge -> Kakariko Gorge Cave Entrance",
    )

    multiworld.get_region("Kakariko Gorge", player).connect(
        multiworld.get_region("Kakariko Gorge Behind Gate", player),
        "Kakariko Gorge -> Kakariko Gorge Behind Gate",
    )

    multiworld.get_region("Kakariko Gorge", player).connect(
        multiworld.get_region("Faron Field", player),
        "Kakariko Gorge -> Faron Field",
    )

    multiworld.get_region("Kakariko Gorge", player).connect(
        multiworld.get_region("Eldin Field", player),
        "Kakariko Gorge -> Eldin Field",
    )

    multiworld.get_region("Kakariko Gorge", player).connect(
        multiworld.get_region("Kakariko Gorge Keese Grotto", player),
        "Kakariko Gorge -> Kakariko Gorge Keese Grotto",
    )

    multiworld.get_region("Kakariko Gorge Cave Entrance", player).connect(
        multiworld.get_region("Kakariko Gorge", player),
        "Kakariko Gorge Cave Entrance -> Kakariko Gorge",
    )

    multiworld.get_region("Kakariko Gorge Cave Entrance", player).connect(
        multiworld.get_region("Eldin Lantern Cave", player),
        "Kakariko Gorge Cave Entrance -> Eldin Lantern Cave",
    )

    multiworld.get_region("Kakariko Gorge Behind Gate", player).connect(
        multiworld.get_region("Kakariko Gorge", player),
        "Kakariko Gorge Behind Gate -> Kakariko Gorge",
    )

    multiworld.get_region("Kakariko Gorge Behind Gate", player).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Kakariko Gorge Behind Gate -> Lower Kakariko Village",
    )

    multiworld.get_region("Eldin Lantern Cave", player).connect(
        multiworld.get_region("Kakariko Gorge Cave Entrance", player),
        "Eldin Lantern Cave -> Kakariko Gorge Cave Entrance",
    )

    multiworld.get_region("Kakariko Gorge Keese Grotto", player).connect(
        multiworld.get_region("Kakariko Gorge", player),
        "Kakariko Gorge Keese Grotto -> Kakariko Gorge",
    )

    multiworld.get_region("Eldin Field", player).connect(
        multiworld.get_region("Eldin Field Near Castle Town", player),
        "Eldin Field -> Eldin Field Near Castle Town",
    )

    multiworld.get_region("Eldin Field", player).connect(
        multiworld.get_region("Eldin Field Lava Cave Ledge", player),
        "Eldin Field -> Eldin Field Lava Cave Ledge",
    )

    multiworld.get_region("Eldin Field", player).connect(
        multiworld.get_region("Eldin Field From Lava Cave Lower", player),
        "Eldin Field -> Eldin Field From Lava Cave Lower",
    )

    multiworld.get_region("Eldin Field", player).connect(
        multiworld.get_region("Kakariko Gorge", player),
        "Eldin Field -> Kakariko Gorge",
    )

    multiworld.get_region("Eldin Field", player).connect(
        multiworld.get_region("Kakariko Village Behind Gate", player),
        "Eldin Field -> Kakariko Village Behind Gate",
    )

    multiworld.get_region("Eldin Field", player).connect(
        multiworld.get_region("North Eldin Field", player),
        "Eldin Field -> North Eldin Field",
    )

    multiworld.get_region("Eldin Field", player).connect(
        multiworld.get_region("Eldin Field Bomskit Grotto", player),
        "Eldin Field -> Eldin Field Bomskit Grotto",
    )

    multiworld.get_region("Eldin Field", player).connect(
        multiworld.get_region("Eldin Field Water Bomb Fish Grotto", player),
        "Eldin Field -> Eldin Field Water Bomb Fish Grotto",
    )

    multiworld.get_region("Eldin Field Near Castle Town", player).connect(
        multiworld.get_region("Eldin Field", player),
        "Eldin Field Near Castle Town -> Eldin Field",
    )

    multiworld.get_region("Eldin Field Near Castle Town", player).connect(
        multiworld.get_region("Outside Castle Town East", player),
        "Eldin Field Near Castle Town -> Outside Castle Town East",
    )

    multiworld.get_region("Eldin Field Lava Cave Ledge", player).connect(
        multiworld.get_region("Eldin Field", player),
        "Eldin Field Lava Cave Ledge -> Eldin Field",
    )

    multiworld.get_region("Eldin Field Lava Cave Ledge", player).connect(
        multiworld.get_region("Eldin Field Lava Cave Upper", player),
        "Eldin Field Lava Cave Ledge -> Eldin Field Lava Cave Upper",
    )

    multiworld.get_region("Eldin Field From Lava Cave Lower", player).connect(
        multiworld.get_region("Eldin Field", player),
        "Eldin Field From Lava Cave Lower -> Eldin Field",
    )

    multiworld.get_region("Eldin Field From Lava Cave Lower", player).connect(
        multiworld.get_region("Eldin Field Lava Cave Lower", player),
        "Eldin Field From Lava Cave Lower -> Eldin Field Lava Cave Lower",
    )

    multiworld.get_region("North Eldin Field", player).connect(
        multiworld.get_region("Eldin Field", player),
        "North Eldin Field -> Eldin Field",
    )

    multiworld.get_region("North Eldin Field", player).connect(
        multiworld.get_region("Eldin Field Outside Hidden Village", player),
        "North Eldin Field -> Eldin Field Outside Hidden Village",
    )

    multiworld.get_region("North Eldin Field", player).connect(
        multiworld.get_region("Eldin Field Grotto Platform", player),
        "North Eldin Field -> Eldin Field Grotto Platform",
    )

    multiworld.get_region("North Eldin Field", player).connect(
        multiworld.get_region("Lanayru Field", player),
        "North Eldin Field -> Lanayru Field",
    )

    multiworld.get_region("Eldin Field Outside Hidden Village", player).connect(
        multiworld.get_region("North Eldin Field", player),
        "Eldin Field Outside Hidden Village -> North Eldin Field",
    )

    multiworld.get_region("Eldin Field Outside Hidden Village", player).connect(
        multiworld.get_region("Hidden Village", player),
        "Eldin Field Outside Hidden Village -> Hidden Village",
    )

    multiworld.get_region("Eldin Field Grotto Platform", player).connect(
        multiworld.get_region("North Eldin Field", player),
        "Eldin Field Grotto Platform -> North Eldin Field",
    )

    multiworld.get_region("Eldin Field Grotto Platform", player).connect(
        multiworld.get_region("Eldin Field Stalfos Grotto", player),
        "Eldin Field Grotto Platform -> Eldin Field Stalfos Grotto",
    )

    multiworld.get_region("Eldin Field Lava Cave Upper", player).connect(
        multiworld.get_region("Eldin Field Lava Cave Ledge", player),
        "Eldin Field Lava Cave Upper -> Eldin Field Lava Cave Ledge",
    )

    multiworld.get_region("Eldin Field Lava Cave Upper", player).connect(
        multiworld.get_region("Eldin Field Lava Cave Lower", player),
        "Eldin Field Lava Cave Upper -> Eldin Field Lava Cave Lower",
    )

    multiworld.get_region("Eldin Field Lava Cave Lower", player).connect(
        multiworld.get_region("Eldin Field From Lava Cave Lower", player),
        "Eldin Field Lava Cave Lower -> Eldin Field From Lava Cave Lower",
    )

    multiworld.get_region("Eldin Field Bomskit Grotto", player).connect(
        multiworld.get_region("Eldin Field", player),
        "Eldin Field Bomskit Grotto -> Eldin Field",
    )

    multiworld.get_region("Eldin Field Water Bomb Fish Grotto", player).connect(
        multiworld.get_region("Eldin Field", player),
        "Eldin Field Water Bomb Fish Grotto -> Eldin Field",
    )

    multiworld.get_region("Eldin Field Stalfos Grotto", player).connect(
        multiworld.get_region("Eldin Field Grotto Platform", player),
        "Eldin Field Stalfos Grotto -> Eldin Field Grotto Platform",
    )

    multiworld.get_region("Lower Kakariko Village", player).connect(
        multiworld.get_region("Upper Kakariko Village", player),
        "Lower Kakariko Village -> Upper Kakariko Village",
    )

    multiworld.get_region("Lower Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Village Behind Gate", player),
        "Lower Kakariko Village -> Kakariko Village Behind Gate",
    )

    multiworld.get_region("Lower Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Gorge Behind Gate", player),
        "Lower Kakariko Village -> Kakariko Gorge Behind Gate",
    )

    multiworld.get_region("Lower Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Graveyard", player),
        "Lower Kakariko Village -> Kakariko Graveyard",
    )

    multiworld.get_region("Lower Kakariko Village", player).connect(
        multiworld.get_region("Death Mountain Near Kakariko", player),
        "Lower Kakariko Village -> Death Mountain Near Kakariko",
    )

    multiworld.get_region("Lower Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Renados Sanctuary Front Left Door", player),
        "Lower Kakariko Village -> Kakariko Renados Sanctuary Front Left Door",
    )

    multiworld.get_region("Lower Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Renados Sanctuary Front Right Door", player),
        "Lower Kakariko Village -> Kakariko Renados Sanctuary Front Right Door",
    )

    multiworld.get_region("Lower Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Renados Sanctuary Back Left Door", player),
        "Lower Kakariko Village -> Kakariko Renados Sanctuary Back Left Door",
    )

    multiworld.get_region("Lower Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Renados Sanctuary Back Right Door", player),
        "Lower Kakariko Village -> Kakariko Renados Sanctuary Back Right Door",
    )

    multiworld.get_region("Lower Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Malo Mart", player),
        "Lower Kakariko Village -> Kakariko Malo Mart",
    )

    multiworld.get_region("Lower Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Elde Inn Left Door", player),
        "Lower Kakariko Village -> Kakariko Elde Inn Left Door",
    )

    multiworld.get_region("Lower Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Elde Inn Right Door", player),
        "Lower Kakariko Village -> Kakariko Elde Inn Right Door",
    )

    multiworld.get_region("Lower Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Bug House Door", player),
        "Lower Kakariko Village -> Kakariko Bug House Door",
    )

    multiworld.get_region("Lower Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Bug House Ceiling Hole", player),
        "Lower Kakariko Village -> Kakariko Bug House Ceiling Hole",
    )

    multiworld.get_region("Lower Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Barnes Bomb Shop Lower", player),
        "Lower Kakariko Village -> Kakariko Barnes Bomb Shop Lower",
    )

    multiworld.get_region("Upper Kakariko Village", player).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Upper Kakariko Village -> Lower Kakariko Village",
    )

    multiworld.get_region("Upper Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Top of Watchtower", player),
        "Upper Kakariko Village -> Kakariko Top of Watchtower",
    )

    multiworld.get_region("Upper Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Barnes Bomb Shop Upper", player),
        "Upper Kakariko Village -> Kakariko Barnes Bomb Shop Upper",
    )

    multiworld.get_region("Upper Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Watchtower Lower Door", player),
        "Upper Kakariko Village -> Kakariko Watchtower Lower Door",
    )

    multiworld.get_region("Upper Kakariko Village", player).connect(
        multiworld.get_region("Kakariko Watchtower Dig Spot", player),
        "Upper Kakariko Village -> Kakariko Watchtower Dig Spot",
    )

    multiworld.get_region("Kakariko Top of Watchtower", player).connect(
        multiworld.get_region("Upper Kakariko Village", player),
        "Kakariko Top of Watchtower -> Upper Kakariko Village",
    )

    multiworld.get_region("Kakariko Top of Watchtower", player).connect(
        multiworld.get_region("Kakariko Watchtower Upper Door", player),
        "Kakariko Top of Watchtower -> Kakariko Watchtower Upper Door",
    )

    multiworld.get_region("Kakariko Village Behind Gate", player).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Kakariko Village Behind Gate -> Lower Kakariko Village",
    )

    multiworld.get_region("Kakariko Village Behind Gate", player).connect(
        multiworld.get_region("Eldin Field", player),
        "Kakariko Village Behind Gate -> Eldin Field",
    )

    multiworld.get_region("Kakariko Renados Sanctuary Front Left Door", player).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Kakariko Renados Sanctuary Front Left Door -> Lower Kakariko Village",
    )

    multiworld.get_region("Kakariko Renados Sanctuary Front Left Door", player).connect(
        multiworld.get_region("Kakariko Renados Sanctuary", player),
        "Kakariko Renados Sanctuary Front Left Door -> Kakariko Renados Sanctuary",
    )

    multiworld.get_region(
        "Kakariko Renados Sanctuary Front Right Door", player
    ).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Kakariko Renados Sanctuary Front Right Door -> Lower Kakariko Village",
    )

    multiworld.get_region(
        "Kakariko Renados Sanctuary Front Right Door", player
    ).connect(
        multiworld.get_region("Kakariko Renados Sanctuary", player),
        "Kakariko Renados Sanctuary Front Right Door -> Kakariko Renados Sanctuary",
    )

    multiworld.get_region("Kakariko Renados Sanctuary Back Left Door", player).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Kakariko Renados Sanctuary Back Left Door -> Lower Kakariko Village",
    )

    multiworld.get_region("Kakariko Renados Sanctuary Back Left Door", player).connect(
        multiworld.get_region("Kakariko Renados Sanctuary", player),
        "Kakariko Renados Sanctuary Back Left Door -> Kakariko Renados Sanctuary",
    )

    multiworld.get_region("Kakariko Renados Sanctuary Back Right Door", player).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Kakariko Renados Sanctuary Back Right Door -> Lower Kakariko Village",
    )

    multiworld.get_region("Kakariko Renados Sanctuary Back Right Door", player).connect(
        multiworld.get_region("Kakariko Renados Sanctuary", player),
        "Kakariko Renados Sanctuary Back Right Door -> Kakariko Renados Sanctuary",
    )

    multiworld.get_region("Kakariko Renados Sanctuary", player).connect(
        multiworld.get_region("Kakariko Renados Sanctuary Front Left Door", player),
        "Kakariko Renados Sanctuary -> Kakariko Renados Sanctuary Front Left Door",
    )

    multiworld.get_region("Kakariko Renados Sanctuary", player).connect(
        multiworld.get_region("Kakariko Renados Sanctuary Front Right Door", player),
        "Kakariko Renados Sanctuary -> Kakariko Renados Sanctuary Front Right Door",
    )

    multiworld.get_region("Kakariko Renados Sanctuary", player).connect(
        multiworld.get_region("Kakariko Renados Sanctuary Back Left Door", player),
        "Kakariko Renados Sanctuary -> Kakariko Renados Sanctuary Back Left Door",
    )

    multiworld.get_region("Kakariko Renados Sanctuary", player).connect(
        multiworld.get_region("Kakariko Renados Sanctuary Back Right Door", player),
        "Kakariko Renados Sanctuary -> Kakariko Renados Sanctuary Back Right Door",
    )

    multiworld.get_region("Kakariko Renados Sanctuary", player).connect(
        multiworld.get_region("Kakariko Renados Sanctuary Basement", player),
        "Kakariko Renados Sanctuary -> Kakariko Renados Sanctuary Basement",
    )

    multiworld.get_region("Kakariko Renados Sanctuary Basement", player).connect(
        multiworld.get_region("Kakariko Renados Sanctuary", player),
        "Kakariko Renados Sanctuary Basement -> Kakariko Renados Sanctuary",
    )

    multiworld.get_region("Kakariko Malo Mart", player).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Kakariko Malo Mart -> Lower Kakariko Village",
    )

    multiworld.get_region("Kakariko Elde Inn Left Door", player).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Kakariko Elde Inn Left Door -> Lower Kakariko Village",
    )

    multiworld.get_region("Kakariko Elde Inn Left Door", player).connect(
        multiworld.get_region("Kakariko Elde Inn", player),
        "Kakariko Elde Inn Left Door -> Kakariko Elde Inn",
    )

    multiworld.get_region("Kakariko Elde Inn Right Door", player).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Kakariko Elde Inn Right Door -> Lower Kakariko Village",
    )

    multiworld.get_region("Kakariko Elde Inn Right Door", player).connect(
        multiworld.get_region("Kakariko Elde Inn", player),
        "Kakariko Elde Inn Right Door -> Kakariko Elde Inn",
    )

    multiworld.get_region("Kakariko Elde Inn", player).connect(
        multiworld.get_region("Kakariko Elde Inn Left Door", player),
        "Kakariko Elde Inn -> Kakariko Elde Inn Left Door",
    )

    multiworld.get_region("Kakariko Elde Inn", player).connect(
        multiworld.get_region("Kakariko Elde Inn Right Door", player),
        "Kakariko Elde Inn -> Kakariko Elde Inn Right Door",
    )

    multiworld.get_region("Kakariko Bug House Door", player).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Kakariko Bug House Door -> Lower Kakariko Village",
    )

    multiworld.get_region("Kakariko Bug House Door", player).connect(
        multiworld.get_region("Kakariko Bug House", player),
        "Kakariko Bug House Door -> Kakariko Bug House",
    )

    multiworld.get_region("Kakariko Bug House Ceiling Hole", player).connect(
        multiworld.get_region("Kakariko Bug House", player),
        "Kakariko Bug House Ceiling Hole -> Kakariko Bug House",
    )

    multiworld.get_region("Kakariko Bug House Ceiling Hole", player).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Kakariko Bug House Ceiling Hole -> Lower Kakariko Village",
    )

    multiworld.get_region("Kakariko Bug House", player).connect(
        multiworld.get_region("Kakariko Bug House Door", player),
        "Kakariko Bug House -> Kakariko Bug House Door",
    )

    multiworld.get_region("Kakariko Bug House", player).connect(
        multiworld.get_region("Kakariko Bug House Ceiling Hole", player),
        "Kakariko Bug House -> Kakariko Bug House Ceiling Hole",
    )

    multiworld.get_region("Kakariko Barnes Bomb Shop Lower", player).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Kakariko Barnes Bomb Shop Lower -> Lower Kakariko Village",
    )

    multiworld.get_region("Kakariko Barnes Bomb Shop Lower", player).connect(
        multiworld.get_region("Kakariko Barnes Bomb Shop Upper", player),
        "Kakariko Barnes Bomb Shop Lower -> Kakariko Barnes Bomb Shop Upper",
    )

    multiworld.get_region("Kakariko Barnes Bomb Shop Upper", player).connect(
        multiworld.get_region("Upper Kakariko Village", player),
        "Kakariko Barnes Bomb Shop Upper -> Upper Kakariko Village",
    )

    multiworld.get_region("Kakariko Barnes Bomb Shop Upper", player).connect(
        multiworld.get_region("Kakariko Barnes Bomb Shop Lower", player),
        "Kakariko Barnes Bomb Shop Upper -> Kakariko Barnes Bomb Shop Lower",
    )

    multiworld.get_region("Kakariko Watchtower Lower Door", player).connect(
        multiworld.get_region("Upper Kakariko Village", player),
        "Kakariko Watchtower Lower Door -> Upper Kakariko Village",
    )

    multiworld.get_region("Kakariko Watchtower Lower Door", player).connect(
        multiworld.get_region("Kakariko Watchtower", player),
        "Kakariko Watchtower Lower Door -> Kakariko Watchtower",
    )

    multiworld.get_region("Kakariko Watchtower Dig Spot", player).connect(
        multiworld.get_region("Upper Kakariko Village", player),
        "Kakariko Watchtower Dig Spot -> Upper Kakariko Village",
    )

    multiworld.get_region("Kakariko Watchtower Dig Spot", player).connect(
        multiworld.get_region("Kakariko Watchtower", player),
        "Kakariko Watchtower Dig Spot -> Kakariko Watchtower",
    )

    multiworld.get_region("Kakariko Watchtower Upper Door", player).connect(
        multiworld.get_region("Kakariko Top of Watchtower", player),
        "Kakariko Watchtower Upper Door -> Kakariko Top of Watchtower",
    )

    multiworld.get_region("Kakariko Watchtower Upper Door", player).connect(
        multiworld.get_region("Kakariko Watchtower", player),
        "Kakariko Watchtower Upper Door -> Kakariko Watchtower",
    )

    multiworld.get_region("Kakariko Watchtower", player).connect(
        multiworld.get_region("Kakariko Watchtower Lower Door", player),
        "Kakariko Watchtower -> Kakariko Watchtower Lower Door",
    )

    multiworld.get_region("Kakariko Watchtower", player).connect(
        multiworld.get_region("Kakariko Watchtower Dig Spot", player),
        "Kakariko Watchtower -> Kakariko Watchtower Dig Spot",
    )

    multiworld.get_region("Kakariko Watchtower", player).connect(
        multiworld.get_region("Kakariko Watchtower Upper Door", player),
        "Kakariko Watchtower -> Kakariko Watchtower Upper Door",
    )

    multiworld.get_region("Kakariko Graveyard", player).connect(
        multiworld.get_region("Lower Kakariko Village", player),
        "Kakariko Graveyard -> Lower Kakariko Village",
    )

    multiworld.get_region("Kakariko Graveyard", player).connect(
        multiworld.get_region("Lake Hylia", player),
        "Kakariko Graveyard -> Lake Hylia",
    )

    multiworld.get_region("South Faron Woods", player).connect(
        multiworld.get_region("South Faron Woods Behind Gate", player),
        "South Faron Woods -> South Faron Woods Behind Gate",
    )

    multiworld.get_region("South Faron Woods", player).connect(
        multiworld.get_region("South Faron Woods Owl Statue Area", player),
        "South Faron Woods -> South Faron Woods Owl Statue Area",
    )

    multiworld.get_region("South Faron Woods", player).connect(
        multiworld.get_region("Ordon Bridge", player),
        "South Faron Woods -> Ordon Bridge",
    )

    multiworld.get_region("South Faron Woods", player).connect(
        multiworld.get_region("Faron Field", player),
        "South Faron Woods -> Faron Field",
    )

    multiworld.get_region("South Faron Woods", player).connect(
        multiworld.get_region("Faron Woods Coros House Lower", player),
        "South Faron Woods -> Faron Woods Coros House Lower",
    )

    multiworld.get_region("South Faron Woods Behind Gate", player).connect(
        multiworld.get_region("South Faron Woods", player),
        "South Faron Woods Behind Gate -> South Faron Woods",
    )

    multiworld.get_region("South Faron Woods Behind Gate", player).connect(
        multiworld.get_region("Faron Woods Cave Southern Entrance", player),
        "South Faron Woods Behind Gate -> Faron Woods Cave Southern Entrance",
    )

    multiworld.get_region("South Faron Woods Coros Ledge", player).connect(
        multiworld.get_region("South Faron Woods", player),
        "South Faron Woods Coros Ledge -> South Faron Woods",
    )

    multiworld.get_region("South Faron Woods Coros Ledge", player).connect(
        multiworld.get_region("Faron Woods Coros House Upper", player),
        "South Faron Woods Coros Ledge -> Faron Woods Coros House Upper",
    )

    multiworld.get_region("South Faron Woods Owl Statue Area", player).connect(
        multiworld.get_region("South Faron Woods", player),
        "South Faron Woods Owl Statue Area -> South Faron Woods",
    )

    multiworld.get_region("South Faron Woods Owl Statue Area", player).connect(
        multiworld.get_region("South Faron Woods Above Owl Statue", player),
        "South Faron Woods Owl Statue Area -> South Faron Woods Above Owl Statue",
    )

    multiworld.get_region("South Faron Woods Above Owl Statue", player).connect(
        multiworld.get_region("South Faron Woods Owl Statue Area", player),
        "South Faron Woods Above Owl Statue -> South Faron Woods Owl Statue Area",
    )

    multiworld.get_region("South Faron Woods Above Owl Statue", player).connect(
        multiworld.get_region("Mist Area Near Owl Statue Chest", player),
        "South Faron Woods Above Owl Statue -> Mist Area Near Owl Statue Chest",
    )

    multiworld.get_region("Faron Woods Coros House Lower", player).connect(
        multiworld.get_region("Faron Woods Coros House Upper", player),
        "Faron Woods Coros House Lower -> Faron Woods Coros House Upper",
    )

    multiworld.get_region("Faron Woods Coros House Lower", player).connect(
        multiworld.get_region("South Faron Woods", player),
        "Faron Woods Coros House Lower -> South Faron Woods",
    )

    multiworld.get_region("Faron Woods Coros House Upper", player).connect(
        multiworld.get_region("Faron Woods Coros House Lower", player),
        "Faron Woods Coros House Upper -> Faron Woods Coros House Lower",
    )

    multiworld.get_region("Faron Woods Coros House Upper", player).connect(
        multiworld.get_region("South Faron Woods Coros Ledge", player),
        "Faron Woods Coros House Upper -> South Faron Woods Coros Ledge",
    )

    multiworld.get_region("Faron Woods Cave Southern Entrance", player).connect(
        multiworld.get_region("South Faron Woods Behind Gate", player),
        "Faron Woods Cave Southern Entrance -> South Faron Woods Behind Gate",
    )

    multiworld.get_region("Faron Woods Cave Southern Entrance", player).connect(
        multiworld.get_region("Faron Woods Cave", player),
        "Faron Woods Cave Southern Entrance -> Faron Woods Cave",
    )

    multiworld.get_region("Faron Woods Cave", player).connect(
        multiworld.get_region("Faron Woods Cave Southern Entrance", player),
        "Faron Woods Cave -> Faron Woods Cave Southern Entrance",
    )

    multiworld.get_region("Faron Woods Cave", player).connect(
        multiworld.get_region("Faron Woods Cave Northern Entrance", player),
        "Faron Woods Cave -> Faron Woods Cave Northern Entrance",
    )

    multiworld.get_region("Mist Area Near Faron Woods Cave", player).connect(
        multiworld.get_region("Mist Area Inside Mist", player),
        "Mist Area Near Faron Woods Cave -> Mist Area Inside Mist",
    )

    multiworld.get_region("Mist Area Near Faron Woods Cave", player).connect(
        multiworld.get_region("Mist Area Under Owl Statue Chest", player),
        "Mist Area Near Faron Woods Cave -> Mist Area Under Owl Statue Chest",
    )

    multiworld.get_region("Mist Area Near Faron Woods Cave", player).connect(
        multiworld.get_region("Faron Woods Cave Northern Entrance", player),
        "Mist Area Near Faron Woods Cave -> Faron Woods Cave Northern Entrance",
    )

    multiworld.get_region("Mist Area Inside Mist", player).connect(
        multiworld.get_region("Mist Area Near Faron Woods Cave", player),
        "Mist Area Inside Mist -> Mist Area Near Faron Woods Cave",
    )

    multiworld.get_region("Mist Area Inside Mist", player).connect(
        multiworld.get_region("Mist Area Under Owl Statue Chest", player),
        "Mist Area Inside Mist -> Mist Area Under Owl Statue Chest",
    )

    multiworld.get_region("Mist Area Inside Mist", player).connect(
        multiworld.get_region("Mist Area Outside Faron Mist Cave", player),
        "Mist Area Inside Mist -> Mist Area Outside Faron Mist Cave",
    )

    multiworld.get_region("Mist Area Inside Mist", player).connect(
        multiworld.get_region("Mist Area Near North Faron Woods", player),
        "Mist Area Inside Mist -> Mist Area Near North Faron Woods",
    )

    multiworld.get_region("Mist Area Under Owl Statue Chest", player).connect(
        multiworld.get_region("Mist Area Inside Mist", player),
        "Mist Area Under Owl Statue Chest -> Mist Area Inside Mist",
    )

    multiworld.get_region("Mist Area Under Owl Statue Chest", player).connect(
        multiworld.get_region("Mist Area Center Stump", player),
        "Mist Area Under Owl Statue Chest -> Mist Area Center Stump",
    )

    multiworld.get_region("Mist Area Near Owl Statue Chest", player).connect(
        multiworld.get_region("Mist Area Under Owl Statue Chest", player),
        "Mist Area Near Owl Statue Chest -> Mist Area Under Owl Statue Chest",
    )

    multiworld.get_region("Mist Area Near Owl Statue Chest", player).connect(
        multiworld.get_region("South Faron Woods Above Owl Statue", player),
        "Mist Area Near Owl Statue Chest -> South Faron Woods Above Owl Statue",
    )

    multiworld.get_region("Mist Area Center Stump", player).connect(
        multiworld.get_region("Mist Area Inside Mist", player),
        "Mist Area Center Stump -> Mist Area Inside Mist",
    )

    multiworld.get_region("Mist Area Center Stump", player).connect(
        multiworld.get_region("Mist Area Near North Faron Woods", player),
        "Mist Area Center Stump -> Mist Area Near North Faron Woods",
    )

    multiworld.get_region("Mist Area Outside Faron Mist Cave", player).connect(
        multiworld.get_region("Mist Area Inside Mist", player),
        "Mist Area Outside Faron Mist Cave -> Mist Area Inside Mist",
    )

    multiworld.get_region("Mist Area Outside Faron Mist Cave", player).connect(
        multiworld.get_region("Mist Area Faron Mist Cave", player),
        "Mist Area Outside Faron Mist Cave -> Mist Area Faron Mist Cave",
    )

    multiworld.get_region("Mist Area Near North Faron Woods", player).connect(
        multiworld.get_region("Mist Area Inside Mist", player),
        "Mist Area Near North Faron Woods -> Mist Area Inside Mist",
    )

    multiworld.get_region("Mist Area Near North Faron Woods", player).connect(
        multiworld.get_region("Mist Area Near Faron Woods Cave", player),
        "Mist Area Near North Faron Woods -> Mist Area Near Faron Woods Cave",
    )

    multiworld.get_region("Mist Area Near North Faron Woods", player).connect(
        multiworld.get_region("North Faron Woods", player),
        "Mist Area Near North Faron Woods -> North Faron Woods",
    )

    multiworld.get_region("Faron Woods Cave Northern Entrance", player).connect(
        multiworld.get_region("Mist Area Near Faron Woods Cave", player),
        "Faron Woods Cave Northern Entrance -> Mist Area Near Faron Woods Cave",
    )

    multiworld.get_region("Faron Woods Cave Northern Entrance", player).connect(
        multiworld.get_region("Faron Woods Cave", player),
        "Faron Woods Cave Northern Entrance -> Faron Woods Cave",
    )

    multiworld.get_region("Mist Area Faron Mist Cave", player).connect(
        multiworld.get_region("Mist Area Outside Faron Mist Cave", player),
        "Mist Area Faron Mist Cave -> Mist Area Outside Faron Mist Cave",
    )

    multiworld.get_region("North Faron Woods", player).connect(
        multiworld.get_region("Mist Area Near North Faron Woods", player),
        "North Faron Woods -> Mist Area Near North Faron Woods",
    )

    multiworld.get_region("North Faron Woods", player).connect(
        multiworld.get_region("Lost Woods", player),
        "North Faron Woods -> Lost Woods",
    )

    multiworld.get_region("North Faron Woods", player).connect(
        multiworld.get_region("Forest Temple Entrance", player),
        "North Faron Woods -> Forest Temple Entrance",
    )

    multiworld.get_region("Faron Field", player).connect(
        multiworld.get_region("Faron Field Behind Boulder", player),
        "Faron Field -> Faron Field Behind Boulder",
    )

    multiworld.get_region("Faron Field", player).connect(
        multiworld.get_region("South Faron Woods", player),
        "Faron Field -> South Faron Woods",
    )

    multiworld.get_region("Faron Field", player).connect(
        multiworld.get_region("Kakariko Gorge", player),
        "Faron Field -> Kakariko Gorge",
    )

    multiworld.get_region("Faron Field", player).connect(
        multiworld.get_region("Lake Hylia Bridge", player),
        "Faron Field -> Lake Hylia Bridge",
    )

    multiworld.get_region("Faron Field", player).connect(
        multiworld.get_region("Faron Field Corner Grotto", player),
        "Faron Field -> Faron Field Corner Grotto",
    )

    multiworld.get_region("Faron Field", player).connect(
        multiworld.get_region("Faron Field Fishing Grotto", player),
        "Faron Field -> Faron Field Fishing Grotto",
    )

    multiworld.get_region("Faron Field Behind Boulder", player).connect(
        multiworld.get_region("Faron Field", player),
        "Faron Field Behind Boulder -> Faron Field",
    )

    multiworld.get_region("Faron Field Behind Boulder", player).connect(
        multiworld.get_region("Outside Castle Town South Inside Boulder", player),
        "Faron Field Behind Boulder -> Outside Castle Town South Inside Boulder",
    )

    multiworld.get_region("Faron Field Corner Grotto", player).connect(
        multiworld.get_region("Faron Field", player),
        "Faron Field Corner Grotto -> Faron Field",
    )

    multiworld.get_region("Faron Field Fishing Grotto", player).connect(
        multiworld.get_region("Faron Field", player),
        "Faron Field Fishing Grotto -> Faron Field",
    )

    multiworld.get_region("Lost Woods", player).connect(
        multiworld.get_region("Lost Woods Lower Battle Arena", player),
        "Lost Woods -> Lost Woods Lower Battle Arena",
    )

    multiworld.get_region("Lost Woods", player).connect(
        multiworld.get_region("Lost Woods Upper Battle Arena", player),
        "Lost Woods -> Lost Woods Upper Battle Arena",
    )

    multiworld.get_region("Lost Woods", player).connect(
        multiworld.get_region("North Faron Woods", player),
        "Lost Woods -> North Faron Woods",
    )

    multiworld.get_region("Lost Woods Lower Battle Arena", player).connect(
        multiworld.get_region("Lost Woods", player),
        "Lost Woods Lower Battle Arena -> Lost Woods",
    )

    multiworld.get_region("Lost Woods Lower Battle Arena", player).connect(
        multiworld.get_region("Sacred Grove Lower", player),
        "Lost Woods Lower Battle Arena -> Sacred Grove Lower",
    )

    multiworld.get_region("Lost Woods Lower Battle Arena", player).connect(
        multiworld.get_region("Lost Woods Baba Serpent Grotto", player),
        "Lost Woods Lower Battle Arena -> Lost Woods Baba Serpent Grotto",
    )

    multiworld.get_region("Lost Woods Upper Battle Arena", player).connect(
        multiworld.get_region("Sacred Grove Before Block", player),
        "Lost Woods Upper Battle Arena -> Sacred Grove Before Block",
    )

    multiworld.get_region("Lost Woods Baba Serpent Grotto", player).connect(
        multiworld.get_region("Lost Woods Lower Battle Arena", player),
        "Lost Woods Baba Serpent Grotto -> Lost Woods Lower Battle Arena",
    )

    multiworld.get_region("Sacred Grove Before Block", player).connect(
        multiworld.get_region("Lost Woods Upper Battle Arena", player),
        "Sacred Grove Before Block -> Lost Woods Upper Battle Arena",
    )

    multiworld.get_region("Sacred Grove Before Block", player).connect(
        multiworld.get_region("Sacred Grove Upper", player),
        "Sacred Grove Before Block -> Sacred Grove Upper",
    )

    multiworld.get_region("Sacred Grove Upper", player).connect(
        multiworld.get_region("Sacred Grove Lower", player),
        "Sacred Grove Upper -> Sacred Grove Lower",
    )

    multiworld.get_region("Sacred Grove Upper", player).connect(
        multiworld.get_region("Sacred Grove Past", player),
        "Sacred Grove Upper -> Sacred Grove Past",
    )

    multiworld.get_region("Sacred Grove Lower", player).connect(
        multiworld.get_region("Lost Woods Lower Battle Arena", player),
        "Sacred Grove Lower -> Lost Woods Lower Battle Arena",
    )

    multiworld.get_region("Sacred Grove Lower", player).connect(
        multiworld.get_region("Sacred Grove Upper", player),
        "Sacred Grove Lower -> Sacred Grove Upper",
    )

    multiworld.get_region("Sacred Grove Past", player).connect(
        multiworld.get_region("Sacred Grove Past Behind Window", player),
        "Sacred Grove Past -> Sacred Grove Past Behind Window",
    )

    multiworld.get_region("Sacred Grove Past", player).connect(
        multiworld.get_region("Sacred Grove Upper", player),
        "Sacred Grove Past -> Sacred Grove Upper",
    )

    multiworld.get_region("Sacred Grove Past Behind Window", player).connect(
        multiworld.get_region("Sacred Grove Past", player),
        "Sacred Grove Past Behind Window -> Sacred Grove Past",
    )

    multiworld.get_region("Sacred Grove Past Behind Window", player).connect(
        multiworld.get_region("Temple of Time Entrance", player),
        "Sacred Grove Past Behind Window -> Temple of Time Entrance",
    )

    multiworld.get_region("Gerudo Desert Cave of Ordeals Floors 01-11", player).connect(
        multiworld.get_region("Gerudo Desert Cave of Ordeals Plateau", player),
        "Gerudo Desert Cave of Ordeals Floors 01-11 -> Gerudo Desert Cave of Ordeals Plateau",
    )

    multiworld.get_region("Gerudo Desert Cave of Ordeals Floors 01-11", player).connect(
        multiworld.get_region("Gerudo Desert Cave of Ordeals Floors 12-21", player),
        "Gerudo Desert Cave of Ordeals Floors 01-11 -> Gerudo Desert Cave of Ordeals Floors 12-21",
    )

    multiworld.get_region("Gerudo Desert Cave of Ordeals Floors 12-21", player).connect(
        multiworld.get_region("Gerudo Desert Cave of Ordeals Floors 22-31", player),
        "Gerudo Desert Cave of Ordeals Floors 12-21 -> Gerudo Desert Cave of Ordeals Floors 22-31",
    )

    multiworld.get_region("Gerudo Desert Cave of Ordeals Floors 22-31", player).connect(
        multiworld.get_region("Gerudo Desert Cave of Ordeals Floors 32-41", player),
        "Gerudo Desert Cave of Ordeals Floors 22-31 -> Gerudo Desert Cave of Ordeals Floors 32-41",
    )

    multiworld.get_region("Gerudo Desert Cave of Ordeals Floors 32-41", player).connect(
        multiworld.get_region("Gerudo Desert Cave of Ordeals Floors 42-50", player),
        "Gerudo Desert Cave of Ordeals Floors 32-41 -> Gerudo Desert Cave of Ordeals Floors 42-50",
    )

    multiworld.get_region("Gerudo Desert Cave of Ordeals Floors 42-50", player).connect(
        multiworld.get_region("Lake Hylia Lanayru Spring", player),
        "Gerudo Desert Cave of Ordeals Floors 42-50 -> Lake Hylia Lanayru Spring",
    )

    multiworld.get_region("Gerudo Desert", player).connect(
        multiworld.get_region("Gerudo Desert Cave of Ordeals Plateau", player),
        "Gerudo Desert -> Gerudo Desert Cave of Ordeals Plateau",
    )

    multiworld.get_region("Gerudo Desert", player).connect(
        multiworld.get_region("Gerudo Desert Basin", player),
        "Gerudo Desert -> Gerudo Desert Basin",
    )

    multiworld.get_region("Gerudo Desert", player).connect(
        multiworld.get_region("Gerudo Desert Skulltula Grotto", player),
        "Gerudo Desert -> Gerudo Desert Skulltula Grotto",
    )

    multiworld.get_region("Gerudo Desert Cave of Ordeals Plateau", player).connect(
        multiworld.get_region("Gerudo Desert", player),
        "Gerudo Desert Cave of Ordeals Plateau -> Gerudo Desert",
    )

    multiworld.get_region("Gerudo Desert Cave of Ordeals Plateau", player).connect(
        multiworld.get_region("Gerudo Desert Cave of Ordeals Floors 01-11", player),
        "Gerudo Desert Cave of Ordeals Plateau -> Gerudo Desert Cave of Ordeals Floors 01-11",
    )

    multiworld.get_region("Gerudo Desert Basin", player).connect(
        multiworld.get_region("Gerudo Desert", player),
        "Gerudo Desert Basin -> Gerudo Desert",
    )

    multiworld.get_region("Gerudo Desert Basin", player).connect(
        multiworld.get_region("Gerudo Desert North East Ledge", player),
        "Gerudo Desert Basin -> Gerudo Desert North East Ledge",
    )

    multiworld.get_region("Gerudo Desert Basin", player).connect(
        multiworld.get_region("Gerudo Desert Outside Bulblin Camp", player),
        "Gerudo Desert Basin -> Gerudo Desert Outside Bulblin Camp",
    )

    multiworld.get_region("Gerudo Desert Basin", player).connect(
        multiworld.get_region("Gerudo Desert Chu Grotto", player),
        "Gerudo Desert Basin -> Gerudo Desert Chu Grotto",
    )

    multiworld.get_region("Gerudo Desert North East Ledge", player).connect(
        multiworld.get_region("Gerudo Desert Basin", player),
        "Gerudo Desert North East Ledge -> Gerudo Desert Basin",
    )

    multiworld.get_region("Gerudo Desert North East Ledge", player).connect(
        multiworld.get_region("Gerudo Desert Rock Grotto", player),
        "Gerudo Desert North East Ledge -> Gerudo Desert Rock Grotto",
    )

    multiworld.get_region("Gerudo Desert Outside Bulblin Camp", player).connect(
        multiworld.get_region("Gerudo Desert Basin", player),
        "Gerudo Desert Outside Bulblin Camp -> Gerudo Desert Basin",
    )

    multiworld.get_region("Gerudo Desert Outside Bulblin Camp", player).connect(
        multiworld.get_region("Bulblin Camp", player),
        "Gerudo Desert Outside Bulblin Camp -> Bulblin Camp",
    )

    multiworld.get_region("Gerudo Desert Skulltula Grotto", player).connect(
        multiworld.get_region("Gerudo Desert", player),
        "Gerudo Desert Skulltula Grotto -> Gerudo Desert",
    )

    multiworld.get_region("Gerudo Desert Chu Grotto", player).connect(
        multiworld.get_region("Gerudo Desert Basin", player),
        "Gerudo Desert Chu Grotto -> Gerudo Desert Basin",
    )

    multiworld.get_region("Gerudo Desert Rock Grotto", player).connect(
        multiworld.get_region("Gerudo Desert North East Ledge", player),
        "Gerudo Desert Rock Grotto -> Gerudo Desert North East Ledge",
    )

    multiworld.get_region("Bulblin Camp", player).connect(
        multiworld.get_region("Gerudo Desert Outside Bulblin Camp", player),
        "Bulblin Camp -> Gerudo Desert Outside Bulblin Camp",
    )

    multiworld.get_region("Bulblin Camp", player).connect(
        multiworld.get_region("Outside Arbiters Grounds", player),
        "Bulblin Camp -> Outside Arbiters Grounds",
    )

    multiworld.get_region("Outside Arbiters Grounds", player).connect(
        multiworld.get_region("Bulblin Camp", player),
        "Outside Arbiters Grounds -> Bulblin Camp",
    )

    multiworld.get_region("Outside Arbiters Grounds", player).connect(
        multiworld.get_region("Arbiters Grounds Entrance", player),
        "Outside Arbiters Grounds -> Arbiters Grounds Entrance",
    )

    multiworld.get_region("Mirror Chamber Lower", player).connect(
        multiworld.get_region("Arbiters Grounds Boss Room", player),
        "Mirror Chamber Lower -> Arbiters Grounds Boss Room",
    )

    multiworld.get_region("Mirror Chamber Lower", player).connect(
        multiworld.get_region("Mirror Chamber Upper", player),
        "Mirror Chamber Lower -> Mirror Chamber Upper",
    )

    multiworld.get_region("Mirror Chamber Upper", player).connect(
        multiworld.get_region("Mirror Chamber Lower", player),
        "Mirror Chamber Upper -> Mirror Chamber Lower",
    )

    multiworld.get_region("Mirror Chamber Upper", player).connect(
        multiworld.get_region("Mirror of Twilight", player),
        "Mirror Chamber Upper -> Mirror of Twilight",
    )

    multiworld.get_region("Mirror of Twilight", player).connect(
        multiworld.get_region("Mirror Chamber Upper", player),
        "Mirror of Twilight -> Mirror Chamber Upper",
    )

    multiworld.get_region("Mirror of Twilight", player).connect(
        multiworld.get_region("Palace of Twilight Entrance", player),
        "Mirror of Twilight -> Palace of Twilight Entrance",
    )

    multiworld.get_region("Castle Town West", player).connect(
        multiworld.get_region("Outside Castle Town West", player),
        "Castle Town West -> Outside Castle Town West",
    )

    multiworld.get_region("Castle Town West", player).connect(
        multiworld.get_region("Castle Town Center", player),
        "Castle Town West -> Castle Town Center",
    )

    multiworld.get_region("Castle Town West", player).connect(
        multiworld.get_region("Castle Town South", player),
        "Castle Town West -> Castle Town South",
    )

    multiworld.get_region("Castle Town West", player).connect(
        multiworld.get_region("Castle Town STAR Game", player),
        "Castle Town West -> Castle Town STAR Game",
    )

    multiworld.get_region("Castle Town STAR Game", player).connect(
        multiworld.get_region("Castle Town West", player),
        "Castle Town STAR Game -> Castle Town West",
    )

    multiworld.get_region("Castle Town Center", player).connect(
        multiworld.get_region("Castle Town West", player),
        "Castle Town Center -> Castle Town West",
    )

    multiworld.get_region("Castle Town Center", player).connect(
        multiworld.get_region("Castle Town North", player),
        "Castle Town Center -> Castle Town North",
    )

    multiworld.get_region("Castle Town Center", player).connect(
        multiworld.get_region("Castle Town East", player),
        "Castle Town Center -> Castle Town East",
    )

    multiworld.get_region("Castle Town Center", player).connect(
        multiworld.get_region("Castle Town South", player),
        "Castle Town Center -> Castle Town South",
    )

    multiworld.get_region("Castle Town Center", player).connect(
        multiworld.get_region("Castle Town Goron House Left Door", player),
        "Castle Town Center -> Castle Town Goron House Left Door",
    )

    multiworld.get_region("Castle Town Center", player).connect(
        multiworld.get_region("Castle Town Goron House Right Door", player),
        "Castle Town Center -> Castle Town Goron House Right Door",
    )

    multiworld.get_region("Castle Town Center", player).connect(
        multiworld.get_region("Castle Town Malo Mart", player),
        "Castle Town Center -> Castle Town Malo Mart",
    )

    multiworld.get_region("Castle Town Goron House Left Door", player).connect(
        multiworld.get_region("Castle Town Center", player),
        "Castle Town Goron House Left Door -> Castle Town Center",
    )

    multiworld.get_region("Castle Town Goron House Left Door", player).connect(
        multiworld.get_region("Castle Town Goron House", player),
        "Castle Town Goron House Left Door -> Castle Town Goron House",
    )

    multiworld.get_region("Castle Town Goron House Right Door", player).connect(
        multiworld.get_region("Castle Town Center", player),
        "Castle Town Goron House Right Door -> Castle Town Center",
    )

    multiworld.get_region("Castle Town Goron House Right Door", player).connect(
        multiworld.get_region("Castle Town Goron House", player),
        "Castle Town Goron House Right Door -> Castle Town Goron House",
    )

    multiworld.get_region("Castle Town Goron House", player).connect(
        multiworld.get_region("Castle Town Goron House Left Door", player),
        "Castle Town Goron House -> Castle Town Goron House Left Door",
    )

    multiworld.get_region("Castle Town Goron House", player).connect(
        multiworld.get_region("Castle Town Goron House Right Door", player),
        "Castle Town Goron House -> Castle Town Goron House Right Door",
    )

    multiworld.get_region("Castle Town Malo Mart", player).connect(
        multiworld.get_region("Castle Town Center", player),
        "Castle Town Malo Mart -> Castle Town Center",
    )

    multiworld.get_region("Castle Town North", player).connect(
        multiworld.get_region("Castle Town North Behind First Door", player),
        "Castle Town North -> Castle Town North Behind First Door",
    )

    multiworld.get_region("Castle Town North", player).connect(
        multiworld.get_region("Castle Town Center", player),
        "Castle Town North -> Castle Town Center",
    )

    multiworld.get_region("Castle Town North Behind First Door", player).connect(
        multiworld.get_region("Castle Town North", player),
        "Castle Town North Behind First Door -> Castle Town North",
    )

    multiworld.get_region("Castle Town North Behind First Door", player).connect(
        multiworld.get_region("Castle Town North Inside Barrier", player),
        "Castle Town North Behind First Door -> Castle Town North Inside Barrier",
    )

    multiworld.get_region("Castle Town North Inside Barrier", player).connect(
        multiworld.get_region("Castle Town North Behind First Door", player),
        "Castle Town North Inside Barrier -> Castle Town North Behind First Door",
    )

    multiworld.get_region("Castle Town North Inside Barrier", player).connect(
        multiworld.get_region("Hyrule Castle Entrance", player),
        "Castle Town North Inside Barrier -> Hyrule Castle Entrance",
    )

    multiworld.get_region("Castle Town East", player).connect(
        multiworld.get_region("Castle Town Center", player),
        "Castle Town East -> Castle Town Center",
    )

    multiworld.get_region("Castle Town East", player).connect(
        multiworld.get_region("Outside Castle Town East", player),
        "Castle Town East -> Outside Castle Town East",
    )

    multiworld.get_region("Castle Town East", player).connect(
        multiworld.get_region("Castle Town South", player),
        "Castle Town East -> Castle Town South",
    )

    multiworld.get_region("Castle Town East", player).connect(
        multiworld.get_region("Castle Town Doctors Office Left Door", player),
        "Castle Town East -> Castle Town Doctors Office Left Door",
    )

    multiworld.get_region("Castle Town East", player).connect(
        multiworld.get_region("Castle Town Doctors Office Right Door", player),
        "Castle Town East -> Castle Town Doctors Office Right Door",
    )

    multiworld.get_region("Castle Town Doctors Office Balcony", player).connect(
        multiworld.get_region("Castle Town East", player),
        "Castle Town Doctors Office Balcony -> Castle Town East",
    )

    multiworld.get_region("Castle Town Doctors Office Balcony", player).connect(
        multiworld.get_region("Castle Town Doctors Office Upper", player),
        "Castle Town Doctors Office Balcony -> Castle Town Doctors Office Upper",
    )

    multiworld.get_region("Castle Town Doctors Office Left Door", player).connect(
        multiworld.get_region("Castle Town East", player),
        "Castle Town Doctors Office Left Door -> Castle Town East",
    )

    multiworld.get_region("Castle Town Doctors Office Left Door", player).connect(
        multiworld.get_region("Castle Town Doctors Office Entrance", player),
        "Castle Town Doctors Office Left Door -> Castle Town Doctors Office Entrance",
    )

    multiworld.get_region("Castle Town Doctors Office Right Door", player).connect(
        multiworld.get_region("Castle Town East", player),
        "Castle Town Doctors Office Right Door -> Castle Town East",
    )

    multiworld.get_region("Castle Town Doctors Office Right Door", player).connect(
        multiworld.get_region("Castle Town Doctors Office Entrance", player),
        "Castle Town Doctors Office Right Door -> Castle Town Doctors Office Entrance",
    )

    multiworld.get_region("Castle Town Doctors Office Entrance", player).connect(
        multiworld.get_region("Castle Town Doctors Office Left Door", player),
        "Castle Town Doctors Office Entrance -> Castle Town Doctors Office Left Door",
    )

    multiworld.get_region("Castle Town Doctors Office Entrance", player).connect(
        multiworld.get_region("Castle Town Doctors Office Right Door", player),
        "Castle Town Doctors Office Entrance -> Castle Town Doctors Office Right Door",
    )

    multiworld.get_region("Castle Town Doctors Office Entrance", player).connect(
        multiworld.get_region("Castle Town Doctors Office Lower", player),
        "Castle Town Doctors Office Entrance -> Castle Town Doctors Office Lower",
    )

    multiworld.get_region("Castle Town Doctors Office Lower", player).connect(
        multiworld.get_region("Castle Town Doctors Office Entrance", player),
        "Castle Town Doctors Office Lower -> Castle Town Doctors Office Entrance",
    )

    multiworld.get_region("Castle Town Doctors Office Lower", player).connect(
        multiworld.get_region("Castle Town Doctors Office Upper", player),
        "Castle Town Doctors Office Lower -> Castle Town Doctors Office Upper",
    )

    multiworld.get_region("Castle Town Doctors Office Upper", player).connect(
        multiworld.get_region("Castle Town Doctors Office Lower", player),
        "Castle Town Doctors Office Upper -> Castle Town Doctors Office Lower",
    )

    multiworld.get_region("Castle Town Doctors Office Upper", player).connect(
        multiworld.get_region("Castle Town Doctors Office Balcony", player),
        "Castle Town Doctors Office Upper -> Castle Town Doctors Office Balcony",
    )

    multiworld.get_region("Castle Town South", player).connect(
        multiworld.get_region("Castle Town West", player),
        "Castle Town South -> Castle Town West",
    )

    multiworld.get_region("Castle Town South", player).connect(
        multiworld.get_region("Castle Town Center", player),
        "Castle Town South -> Castle Town Center",
    )

    multiworld.get_region("Castle Town South", player).connect(
        multiworld.get_region("Castle Town East", player),
        "Castle Town South -> Castle Town East",
    )

    multiworld.get_region("Castle Town South", player).connect(
        multiworld.get_region("Outside Castle Town South", player),
        "Castle Town South -> Outside Castle Town South",
    )

    multiworld.get_region("Castle Town South", player).connect(
        multiworld.get_region("Castle Town Agithas House", player),
        "Castle Town South -> Castle Town Agithas House",
    )

    multiworld.get_region("Castle Town South", player).connect(
        multiworld.get_region("Castle Town Seer House", player),
        "Castle Town South -> Castle Town Seer House",
    )

    multiworld.get_region("Castle Town South", player).connect(
        multiworld.get_region("Castle Town Jovanis House", player),
        "Castle Town South -> Castle Town Jovanis House",
    )

    multiworld.get_region("Castle Town South", player).connect(
        multiworld.get_region("Castle Town Telmas Bar", player),
        "Castle Town South -> Castle Town Telmas Bar",
    )

    multiworld.get_region("Castle Town Agithas House", player).connect(
        multiworld.get_region("Castle Town South", player),
        "Castle Town Agithas House -> Castle Town South",
    )

    multiworld.get_region("Castle Town Seer House", player).connect(
        multiworld.get_region("Castle Town South", player),
        "Castle Town Seer House -> Castle Town South",
    )

    multiworld.get_region("Castle Town Jovanis House", player).connect(
        multiworld.get_region("Castle Town South", player),
        "Castle Town Jovanis House -> Castle Town South",
    )

    multiworld.get_region("Castle Town Telmas Bar", player).connect(
        multiworld.get_region("Castle Town South", player),
        "Castle Town Telmas Bar -> Castle Town South",
    )

    multiworld.get_region("Lanayru Field", player).connect(
        multiworld.get_region("Lanayru Field Cave Entrance", player),
        "Lanayru Field -> Lanayru Field Cave Entrance",
    )

    multiworld.get_region("Lanayru Field", player).connect(
        multiworld.get_region("Lanayru Field Behind Boulder", player),
        "Lanayru Field -> Lanayru Field Behind Boulder",
    )

    multiworld.get_region("Lanayru Field", player).connect(
        multiworld.get_region("Hyrule Field Near Spinner Rails", player),
        "Lanayru Field -> Hyrule Field Near Spinner Rails",
    )

    multiworld.get_region("Lanayru Field", player).connect(
        multiworld.get_region("North Eldin Field", player),
        "Lanayru Field -> North Eldin Field",
    )

    multiworld.get_region("Lanayru Field", player).connect(
        multiworld.get_region("Outside Castle Town West", player),
        "Lanayru Field -> Outside Castle Town West",
    )

    multiworld.get_region("Lanayru Field", player).connect(
        multiworld.get_region("Lanayru Field Chu Grotto", player),
        "Lanayru Field -> Lanayru Field Chu Grotto",
    )

    multiworld.get_region("Lanayru Field", player).connect(
        multiworld.get_region("Lanayru Field Skulltula Grotto", player),
        "Lanayru Field -> Lanayru Field Skulltula Grotto",
    )

    multiworld.get_region("Lanayru Field", player).connect(
        multiworld.get_region("Lanayru Field Poe Grotto", player),
        "Lanayru Field -> Lanayru Field Poe Grotto",
    )

    multiworld.get_region("Lanayru Field Cave Entrance", player).connect(
        multiworld.get_region("Lanayru Field", player),
        "Lanayru Field Cave Entrance -> Lanayru Field",
    )

    multiworld.get_region("Lanayru Field Cave Entrance", player).connect(
        multiworld.get_region("Lanayru Ice Puzzle Cave", player),
        "Lanayru Field Cave Entrance -> Lanayru Ice Puzzle Cave",
    )

    multiworld.get_region("Lanayru Field Behind Boulder", player).connect(
        multiworld.get_region("Lanayru Field", player),
        "Lanayru Field Behind Boulder -> Lanayru Field",
    )

    multiworld.get_region("Lanayru Field Behind Boulder", player).connect(
        multiworld.get_region("Zoras Domain West Ledge", player),
        "Lanayru Field Behind Boulder -> Zoras Domain West Ledge",
    )

    multiworld.get_region("Hyrule Field Near Spinner Rails", player).connect(
        multiworld.get_region("Lanayru Field", player),
        "Hyrule Field Near Spinner Rails -> Lanayru Field",
    )

    multiworld.get_region("Hyrule Field Near Spinner Rails", player).connect(
        multiworld.get_region("Lake Hylia Bridge", player),
        "Hyrule Field Near Spinner Rails -> Lake Hylia Bridge",
    )

    multiworld.get_region("Lanayru Ice Puzzle Cave", player).connect(
        multiworld.get_region("Lanayru Field Cave Entrance", player),
        "Lanayru Ice Puzzle Cave -> Lanayru Field Cave Entrance",
    )

    multiworld.get_region("Lanayru Field Chu Grotto", player).connect(
        multiworld.get_region("Lanayru Field", player),
        "Lanayru Field Chu Grotto -> Lanayru Field",
    )

    multiworld.get_region("Lanayru Field Skulltula Grotto", player).connect(
        multiworld.get_region("Lanayru Field", player),
        "Lanayru Field Skulltula Grotto -> Lanayru Field",
    )

    multiworld.get_region("Lanayru Field Poe Grotto", player).connect(
        multiworld.get_region("Lanayru Field", player),
        "Lanayru Field Poe Grotto -> Lanayru Field",
    )

    multiworld.get_region("Outside Castle Town West", player).connect(
        multiworld.get_region("Outside Castle Town West Grotto Ledge", player),
        "Outside Castle Town West -> Outside Castle Town West Grotto Ledge",
    )

    multiworld.get_region("Outside Castle Town West", player).connect(
        multiworld.get_region("Lanayru Field", player),
        "Outside Castle Town West -> Lanayru Field",
    )

    multiworld.get_region("Outside Castle Town West", player).connect(
        multiworld.get_region("Castle Town West", player),
        "Outside Castle Town West -> Castle Town West",
    )

    multiworld.get_region("Outside Castle Town West", player).connect(
        multiworld.get_region("Lake Hylia Bridge", player),
        "Outside Castle Town West -> Lake Hylia Bridge",
    )

    multiworld.get_region("Outside Castle Town West Grotto Ledge", player).connect(
        multiworld.get_region("Outside Castle Town West", player),
        "Outside Castle Town West Grotto Ledge -> Outside Castle Town West",
    )

    multiworld.get_region("Outside Castle Town West Grotto Ledge", player).connect(
        multiworld.get_region("Outside Castle Town West Helmasaur Grotto", player),
        "Outside Castle Town West Grotto Ledge -> Outside Castle Town West Helmasaur Grotto",
    )

    multiworld.get_region("Outside Castle Town West Helmasaur Grotto", player).connect(
        multiworld.get_region("Outside Castle Town West Grotto Ledge", player),
        "Outside Castle Town West Helmasaur Grotto -> Outside Castle Town West Grotto Ledge",
    )

    multiworld.get_region("Outside Castle Town East", player).connect(
        multiworld.get_region("Eldin Field Near Castle Town", player),
        "Outside Castle Town East -> Eldin Field Near Castle Town",
    )

    multiworld.get_region("Outside Castle Town East", player).connect(
        multiworld.get_region("Castle Town East", player),
        "Outside Castle Town East -> Castle Town East",
    )

    multiworld.get_region("Outside Castle Town South", player).connect(
        multiworld.get_region("Castle Town South", player),
        "Outside Castle Town South -> Castle Town South",
    )

    multiworld.get_region("Outside Castle Town South Inside Boulder", player).connect(
        multiworld.get_region("Faron Field Behind Boulder", player),
        "Outside Castle Town South Inside Boulder -> Faron Field Behind Boulder",
    )

    multiworld.get_region("Outside Castle Town South", player).connect(
        multiworld.get_region("Lake Hylia", player),
        "Outside Castle Town South -> Lake Hylia",
    )

    multiworld.get_region("Outside Castle Town South", player).connect(
        multiworld.get_region("Outside Castle Town South Tektite Grotto", player),
        "Outside Castle Town South -> Outside Castle Town South Tektite Grotto",
    )

    multiworld.get_region("Outside Castle Town South Inside Boulder", player).connect(
        multiworld.get_region("Outside Castle Town South", player),
        "Outside Castle Town South Inside Boulder -> Outside Castle Town South",
    )

    multiworld.get_region("Outside Castle Town South", player).connect(
        multiworld.get_region("Outside Castle Town South Inside Boulder", player),
        "Outside Castle Town South -> Outside Castle Town South Inside Boulder",
    )

    multiworld.get_region("Outside Castle Town South Tektite Grotto", player).connect(
        multiworld.get_region("Outside Castle Town South", player),
        "Outside Castle Town South Tektite Grotto -> Outside Castle Town South",
    )

    multiworld.get_region("Lake Hylia Bridge", player).connect(
        multiworld.get_region("Lake Hylia Bridge Grotto Ledge", player),
        "Lake Hylia Bridge -> Lake Hylia Bridge Grotto Ledge",
    )

    multiworld.get_region("Lake Hylia Bridge", player).connect(
        multiworld.get_region("Hyrule Field Near Spinner Rails", player),
        "Lake Hylia Bridge -> Hyrule Field Near Spinner Rails",
    )

    multiworld.get_region("Lake Hylia Bridge", player).connect(
        multiworld.get_region("Outside Castle Town West", player),
        "Lake Hylia Bridge -> Outside Castle Town West",
    )

    multiworld.get_region("Lake Hylia Bridge", player).connect(
        multiworld.get_region("Lake Hylia", player),
        "Lake Hylia Bridge -> Lake Hylia",
    )

    multiworld.get_region("Lake Hylia Bridge", player).connect(
        multiworld.get_region("Faron Field", player),
        "Lake Hylia Bridge -> Faron Field",
    )

    multiworld.get_region("Lake Hylia Bridge Grotto Ledge", player).connect(
        multiworld.get_region("Lake Hylia Bridge", player),
        "Lake Hylia Bridge Grotto Ledge -> Lake Hylia Bridge",
    )

    multiworld.get_region("Lake Hylia Bridge Grotto Ledge", player).connect(
        multiworld.get_region("Lake Hylia Bridge Bubble Grotto", player),
        "Lake Hylia Bridge Grotto Ledge -> Lake Hylia Bridge Bubble Grotto",
    )

    multiworld.get_region("Lake Hylia Bridge Bubble Grotto", player).connect(
        multiworld.get_region("Lake Hylia Bridge Grotto Ledge", player),
        "Lake Hylia Bridge Bubble Grotto -> Lake Hylia Bridge Grotto Ledge",
    )

    multiworld.get_region("Lake Hylia", player).connect(
        multiworld.get_region("Lake Hylia Cave Entrance", player),
        "Lake Hylia -> Lake Hylia Cave Entrance",
    )

    multiworld.get_region("Lake Hylia", player).connect(
        multiworld.get_region("Lake Hylia Lakebed Temple Entrance", player),
        "Lake Hylia -> Lake Hylia Lakebed Temple Entrance",
    )

    multiworld.get_region("Lake Hylia", player).connect(
        multiworld.get_region("Lake Hylia Bridge", player),
        "Lake Hylia -> Lake Hylia Bridge",
    )

    multiworld.get_region("Lake Hylia", player).connect(
        multiworld.get_region("Gerudo Desert", player),
        "Lake Hylia -> Gerudo Desert",
    )

    multiworld.get_region("Lake Hylia", player).connect(
        multiworld.get_region("Upper Zoras River", player),
        "Lake Hylia -> Upper Zoras River",
    )

    multiworld.get_region("Lake Hylia", player).connect(
        multiworld.get_region("Lake Hylia Lanayru Spring", player),
        "Lake Hylia -> Lake Hylia Lanayru Spring",
    )

    multiworld.get_region("Lake Hylia", player).connect(
        multiworld.get_region("Lake Hylia Shell Blade Grotto", player),
        "Lake Hylia -> Lake Hylia Shell Blade Grotto",
    )

    multiworld.get_region("Lake Hylia", player).connect(
        multiworld.get_region("Lake Hylia Water Toadpoli Grotto", player),
        "Lake Hylia -> Lake Hylia Water Toadpoli Grotto",
    )

    multiworld.get_region("Lake Hylia", player).connect(
        multiworld.get_region("City in The Sky Entrance", player),
        "Lake Hylia -> City in The Sky Entrance",
    )

    multiworld.get_region("Lake Hylia Cave Entrance", player).connect(
        multiworld.get_region("Lake Hylia", player),
        "Lake Hylia Cave Entrance -> Lake Hylia",
    )

    multiworld.get_region("Lake Hylia Cave Entrance", player).connect(
        multiworld.get_region("Lake Hylia Long Cave", player),
        "Lake Hylia Cave Entrance -> Lake Hylia Long Cave",
    )

    multiworld.get_region("Lake Hylia Lakebed Temple Entrance", player).connect(
        multiworld.get_region("Lake Hylia", player),
        "Lake Hylia Lakebed Temple Entrance -> Lake Hylia",
    )

    multiworld.get_region("Lake Hylia Lakebed Temple Entrance", player).connect(
        multiworld.get_region("Lakebed Temple Entrance", player),
        "Lake Hylia Lakebed Temple Entrance -> Lakebed Temple Entrance",
    )

    multiworld.get_region("Lake Hylia Lanayru Spring", player).connect(
        multiworld.get_region("Lake Hylia", player),
        "Lake Hylia Lanayru Spring -> Lake Hylia",
    )

    multiworld.get_region("Lake Hylia Long Cave", player).connect(
        multiworld.get_region("Lake Hylia Cave Entrance", player),
        "Lake Hylia Long Cave -> Lake Hylia Cave Entrance",
    )

    multiworld.get_region("Lake Hylia Shell Blade Grotto", player).connect(
        multiworld.get_region("Lake Hylia", player),
        "Lake Hylia Shell Blade Grotto -> Lake Hylia",
    )

    multiworld.get_region("Lake Hylia Water Toadpoli Grotto", player).connect(
        multiworld.get_region("Lake Hylia", player),
        "Lake Hylia Water Toadpoli Grotto -> Lake Hylia",
    )

    multiworld.get_region("Upper Zoras River", player).connect(
        multiworld.get_region("Lanayru Field", player),
        "Upper Zoras River -> Lanayru Field",
    )

    multiworld.get_region("Upper Zoras River", player).connect(
        multiworld.get_region("Fishing Hole", player),
        "Upper Zoras River -> Fishing Hole",
    )

    multiworld.get_region("Upper Zoras River", player).connect(
        multiworld.get_region("Zoras Domain", player),
        "Upper Zoras River -> Zoras Domain",
    )

    multiworld.get_region("Upper Zoras River", player).connect(
        multiworld.get_region("Upper Zoras River Izas House", player),
        "Upper Zoras River -> Upper Zoras River Izas House",
    )

    multiworld.get_region("Upper Zoras River Izas House", player).connect(
        multiworld.get_region("Upper Zoras River", player),
        "Upper Zoras River Izas House -> Upper Zoras River",
    )

    multiworld.get_region("Upper Zoras River Izas House", player).connect(
        multiworld.get_region("Lake Hylia", player),
        "Upper Zoras River Izas House -> Lake Hylia",
    )

    multiworld.get_region("Fishing Hole", player).connect(
        multiworld.get_region("Upper Zoras River", player),
        "Fishing Hole -> Upper Zoras River",
    )

    multiworld.get_region("Fishing Hole", player).connect(
        multiworld.get_region("Fishing Hole House", player),
        "Fishing Hole -> Fishing Hole House",
    )

    multiworld.get_region("Fishing Hole House", player).connect(
        multiworld.get_region("Fishing Hole", player),
        "Fishing Hole House -> Fishing Hole",
    )

    multiworld.get_region("Zoras Domain", player).connect(
        multiworld.get_region("Zoras Domain West Ledge", player),
        "Zoras Domain -> Zoras Domain West Ledge",
    )

    multiworld.get_region("Zoras Domain", player).connect(
        multiworld.get_region("Upper Zoras River", player),
        "Zoras Domain -> Upper Zoras River",
    )

    multiworld.get_region("Zoras Domain", player).connect(
        multiworld.get_region("Zoras Domain Throne Room", player),
        "Zoras Domain -> Zoras Domain Throne Room",
    )

    multiworld.get_region("Zoras Domain", player).connect(
        multiworld.get_region("Snowpeak Climb Lower", player),
        "Zoras Domain -> Snowpeak Climb Lower",
    )

    multiworld.get_region("Zoras Domain West Ledge", player).connect(
        multiworld.get_region("Zoras Domain", player),
        "Zoras Domain West Ledge -> Zoras Domain",
    )

    multiworld.get_region("Zoras Domain West Ledge", player).connect(
        multiworld.get_region("Lanayru Field Behind Boulder", player),
        "Zoras Domain West Ledge -> Lanayru Field Behind Boulder",
    )

    multiworld.get_region("Zoras Domain Throne Room", player).connect(
        multiworld.get_region("Zoras Domain", player),
        "Zoras Domain Throne Room -> Zoras Domain",
    )

    multiworld.get_region("Outside Links House", player).connect(
        multiworld.get_region("Ordon Village", player),
        "Outside Links House -> Ordon Village",
    )

    multiworld.get_region("Outside Links House", player).connect(
        multiworld.get_region("Ordon Spring", player),
        "Outside Links House -> Ordon Spring",
    )

    multiworld.get_region("Outside Links House", player).connect(
        multiworld.get_region("Ordon Links House", player),
        "Outside Links House -> Ordon Links House",
    )

    multiworld.get_region("Ordon Links House", player).connect(
        multiworld.get_region("Outside Links House", player),
        "Ordon Links House -> Outside Links House",
    )

    multiworld.get_region("Ordon Village", player).connect(
        multiworld.get_region("Outside Links House", player),
        "Ordon Village -> Outside Links House",
    )

    multiworld.get_region("Ordon Village", player).connect(
        multiworld.get_region("Ordon Ranch Entrance", player),
        "Ordon Village -> Ordon Ranch Entrance",
    )

    multiworld.get_region("Ordon Village", player).connect(
        multiworld.get_region("Ordon Seras Shop", player),
        "Ordon Village -> Ordon Seras Shop",
    )

    multiworld.get_region("Ordon Village", player).connect(
        multiworld.get_region("Ordon Shield House", player),
        "Ordon Village -> Ordon Shield House",
    )

    multiworld.get_region("Ordon Village", player).connect(
        multiworld.get_region("Ordon Sword House", player),
        "Ordon Village -> Ordon Sword House",
    )

    multiworld.get_region("Ordon Village", player).connect(
        multiworld.get_region("Ordon Bos House Left Door", player),
        "Ordon Village -> Ordon Bos House Left Door",
    )

    multiworld.get_region("Ordon Village", player).connect(
        multiworld.get_region("Ordon Bos House Right Door", player),
        "Ordon Village -> Ordon Bos House Right Door",
    )

    multiworld.get_region("Ordon Seras Shop", player).connect(
        multiworld.get_region("Ordon Village", player),
        "Ordon Seras Shop -> Ordon Village",
    )

    multiworld.get_region("Ordon Shield House", player).connect(
        multiworld.get_region("Ordon Village", player),
        "Ordon Shield House -> Ordon Village",
    )

    multiworld.get_region("Ordon Sword House", player).connect(
        multiworld.get_region("Ordon Village", player),
        "Ordon Sword House -> Ordon Village",
    )

    multiworld.get_region("Ordon Bos House Left Door", player).connect(
        multiworld.get_region("Ordon Village", player),
        "Ordon Bos House Left Door -> Ordon Village",
    )

    multiworld.get_region("Ordon Bos House Left Door", player).connect(
        multiworld.get_region("Ordon Bos House", player),
        "Ordon Bos House Left Door -> Ordon Bos House",
    )

    multiworld.get_region("Ordon Bos House Right Door", player).connect(
        multiworld.get_region("Ordon Village", player),
        "Ordon Bos House Right Door -> Ordon Village",
    )

    multiworld.get_region("Ordon Bos House Right Door", player).connect(
        multiworld.get_region("Ordon Bos House", player),
        "Ordon Bos House Right Door -> Ordon Bos House",
    )

    multiworld.get_region("Ordon Bos House", player).connect(
        multiworld.get_region("Ordon Bos House Left Door", player),
        "Ordon Bos House -> Ordon Bos House Left Door",
    )

    multiworld.get_region("Ordon Bos House", player).connect(
        multiworld.get_region("Ordon Bos House Right Door", player),
        "Ordon Bos House -> Ordon Bos House Right Door",
    )

    multiworld.get_region("Ordon Ranch Entrance", player).connect(
        multiworld.get_region("Ordon Ranch", player),
        "Ordon Ranch Entrance -> Ordon Ranch",
    )

    multiworld.get_region("Ordon Ranch Entrance", player).connect(
        multiworld.get_region("Ordon Village", player),
        "Ordon Ranch Entrance -> Ordon Village",
    )

    multiworld.get_region("Ordon Ranch", player).connect(
        multiworld.get_region("Ordon Ranch Entrance", player),
        "Ordon Ranch -> Ordon Ranch Entrance",
    )

    multiworld.get_region("Ordon Ranch", player).connect(
        multiworld.get_region("Ordon Ranch Stable", player),
        "Ordon Ranch -> Ordon Ranch Stable",
    )

    multiworld.get_region("Ordon Ranch Stable", player).connect(
        multiworld.get_region("Ordon Ranch", player),
        "Ordon Ranch Stable -> Ordon Ranch",
    )

    multiworld.get_region("Ordon Ranch Stable", player).connect(
        multiworld.get_region("Ordon Ranch Grotto", player),
        "Ordon Ranch Stable -> Ordon Ranch Grotto",
    )

    multiworld.get_region("Ordon Ranch Grotto", player).connect(
        multiworld.get_region("Ordon Ranch Stable", player),
        "Ordon Ranch Grotto -> Ordon Ranch Stable",
    )

    multiworld.get_region("Ordon Spring", player).connect(
        multiworld.get_region("Outside Links House", player),
        "Ordon Spring -> Outside Links House",
    )

    multiworld.get_region("Ordon Spring", player).connect(
        multiworld.get_region("Ordon Bridge", player),
        "Ordon Spring -> Ordon Bridge",
    )

    multiworld.get_region("Ordon Bridge", player).connect(
        multiworld.get_region("Ordon Spring", player),
        "Ordon Bridge -> Ordon Spring",
    )

    multiworld.get_region("Ordon Bridge", player).connect(
        multiworld.get_region("South Faron Woods", player),
        "Ordon Bridge -> South Faron Woods",
    )

    multiworld.get_region("Snowpeak Climb Lower", player).connect(
        multiworld.get_region("Snowpeak Climb Upper", player),
        "Snowpeak Climb Lower -> Snowpeak Climb Upper",
    )

    multiworld.get_region("Snowpeak Climb Lower", player).connect(
        multiworld.get_region("Zoras Domain", player),
        "Snowpeak Climb Lower -> Zoras Domain",
    )

    multiworld.get_region("Snowpeak Climb Upper", player).connect(
        multiworld.get_region("Snowpeak Climb Lower", player),
        "Snowpeak Climb Upper -> Snowpeak Climb Lower",
    )

    multiworld.get_region("Snowpeak Climb Upper", player).connect(
        multiworld.get_region("Snowpeak Summit Upper", player),
        "Snowpeak Climb Upper -> Snowpeak Summit Upper",
    )

    multiworld.get_region("Snowpeak Climb Upper", player).connect(
        multiworld.get_region("Snowpeak Ice Keese Grotto", player),
        "Snowpeak Climb Upper -> Snowpeak Ice Keese Grotto",
    )

    multiworld.get_region("Snowpeak Climb Upper", player).connect(
        multiworld.get_region("Snowpeak Freezard Grotto", player),
        "Snowpeak Climb Upper -> Snowpeak Freezard Grotto",
    )

    multiworld.get_region("Snowpeak Ice Keese Grotto", player).connect(
        multiworld.get_region("Snowpeak Climb Upper", player),
        "Snowpeak Ice Keese Grotto -> Snowpeak Climb Upper",
    )

    multiworld.get_region("Snowpeak Freezard Grotto", player).connect(
        multiworld.get_region("Snowpeak Climb Upper", player),
        "Snowpeak Freezard Grotto -> Snowpeak Climb Upper",
    )

    multiworld.get_region("Snowpeak Summit Upper", player).connect(
        multiworld.get_region("Snowpeak Summit Lower", player),
        "Snowpeak Summit Upper -> Snowpeak Summit Lower",
    )

    multiworld.get_region("Snowpeak Summit Upper", player).connect(
        multiworld.get_region("Snowpeak Climb Upper", player),
        "Snowpeak Summit Upper -> Snowpeak Climb Upper",
    )

    multiworld.get_region("Snowpeak Summit Lower", player).connect(
        multiworld.get_region("Snowpeak Ruins Left Door", player),
        "Snowpeak Summit Lower -> Snowpeak Ruins Left Door",
    )

    multiworld.get_region("Snowpeak Summit Lower", player).connect(
        multiworld.get_region("Snowpeak Ruins Right Door", player),
        "Snowpeak Summit Lower -> Snowpeak Ruins Right Door",
    )
