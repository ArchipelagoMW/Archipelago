from typing import List, Callable

from BaseClasses import CollectionState

REGION_TO_ENTRANCES: dict[str, List[str]] = {
    "Treehouse": ["Treehouse Meadow Zone Gate", "Treehouse Drifblim Fast Travel Meadow Zone", "Treehouse Beach Zone "
                                                                                              "Gate",
                  "Treehouse Drifblim Fast Travel Beach Zone", "Treehouse Drifblim Fast Travel Ice Zone",
                  "Treehouse Cavern Zone Gate", "Treehouse Drifblim Fast Travel Cavern Zone",
                  "Treehouse Drifblim Fast Travel Magma Zone",
                  "Treehouse Haunted Zone Gate", "Treehouse Drifblim Fast Travel Haunted Zone", "Treehouse Granite "
                                                                                                "Zone Gate",
                  "Treehouse Drifblim Fast Travel Granite Zone", "Treehouse Drifblim Fast Travel Flower Zone",
                  "Treehouse Piplup Air Balloon"],
    "Meadow Zone Main Area": ["Meadow Zone Main Area - Bulbasaur's Daring Dash Attraction",
                              "Meadow Zone Main Area - Venusaur's Gate"],
    "Meadow Zone Venusaur Area": ["Meadow Zone Venusaur Area - Venusaur's Vine Swing Attraction"],
    "Beach Zone Main Area": ["Beach Zone Main Area - Pelipper's Circle Circuit Attraction",
                             "Beach Zone Main Area - Gyarado's Aqua Dash Attraction",
                             "Beach Zone Main Area Lapras Travel"],
    "Ice Zone Main Area": ["Ice Zone Main Area Lift", "Ice Zone Main Area Empoleon Gate"],
    "Ice Zone Empoleon Area": ["Ice Zone Empoleon Area - Empoleon's Snow Slide Attraction"],
    "Cavern Zone Main Area": ["Cavern Zone Main Area - Bastiodon's Panel Crush Attraction",
                              "Cavern Zone Magma Zone Gate"],
    "Magma Zone Main Area": ["Magma Zone Main Area - Rhyperior's Bumper Burn Attraction",
                             "Magma Zone Main Area Blaziken Gate"],
    "Magma Zone Blaziken Area": ["Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction"],
    "Haunted Zone Main Area": ["Haunted Zone Main Area - Tangrowth's Swing-Along Attraction",
                               "Haunted Zone Mansion Entrance"],
    "Haunted Zone Mansion Area": ["Haunted Zone Mansion Area - Dusknoir's Speed Slam Attraction",
                                  "Haunted Zone Mansion Rotom's Hidden Entrance"],
    "Haunted Zone Rotom Area": ["Haunted Zone Rotom Area - Rotom's Spooky Shoot-'em-Up Attraction"],
    "Granite Zone Main Area": [
        "Granite Zone Main Area - Absol's Hurdle Bounce Attraction",
        "Granite Zone Main Area - Salamence's Sky Race Attraction",
        "Granite Zone Flower Zone Entrance"
    ],
    "Flower Zone Main Area": [
        "Flower Zone Main Area - Rayquaza's Balloon Panic Attraction"
    ]
}

VANILLA_ENTRANCES_TO_EXITS: dict[str, str] = {
    "Treehouse Meadow Zone Gate": "Meadow Zone Main Area",
    "Treehouse Drifblim Fast Travel Meadow Zone": "Meadow Zone Main Area",
    "Meadow Zone Main Area - Bulbasaur's Daring Dash Attraction": "Bulbasaur's Daring Dash Attraction",
    "Meadow Zone Main Area - Venusaur's Gate": "Meadow Zone Venusaur Area",
    "Meadow Zone Venusaur Area - Venusaur's Vine Swing Attraction": "Venusaur's Vine Swing Attraction",

    "Treehouse Beach Zone Gate": "Beach Zone Main Area",
    "Treehouse Drifblim Fast Travel Beach Zone": "Beach Zone Main Area",
    "Beach Zone Main Area - Pelipper's Circle Circuit Attraction": "Pelipper's Circle Circuit Attraction",
    "Beach Zone Main Area - Gyarado's Aqua Dash Attraction": "Gyarado's Aqua Dash Attraction",

    "Beach Zone Main Area Lapras Travel": "Ice Zone Main Area",
    "Treehouse Drifblim Fast Travel Ice Zone": "Ice Zone Main Area",
    "Ice Zone Main Area Lift": "Ice Zone Lower Lift Area",
    "Ice Zone Main Area Empoleon Gate": "Ice Zone Empoleon Area",
    "Ice Zone Empoleon Area - Empoleon's Snow Slide Attraction": "Empoleon's Snow Slide Attraction",

    "Treehouse Cavern Zone Gate": "Cavern Zone Main Area",
    "Treehouse Drifblim Fast Travel Cavern Zone": "Cavern Zone Main Area",
    "Cavern Zone Main Area - Bastiodon's Panel Crush Attraction": "Bastiodon's Panel Crush Attraction",

    "Cavern Zone Magma Zone Gate": "Magma Zone Main Area",
    "Treehouse Drifblim Fast Travel Magma Zone": "Magma Zone Main Area",
    "Magma Zone Main Area - Rhyperior's Bumper Burn Attraction": "Rhyperior's Bumper Burn Attraction",
    "Magma Zone Main Area Blaziken Gate": "Magma Zone Blaziken Area",
    "Magma Zone Blaziken Area - Blaziken's Boulder Bash Attraction": "Blaziken's Boulder Bash Attraction",

    "Treehouse Haunted Zone Gate": "Haunted Zone Main Area",
    "Treehouse Drifblim Fast Travel Haunted Zone": "Haunted Zone Main Area",
    "Haunted Zone Main Area - Tangrowth's Swing-Along Attraction": "Tangrowth's Swing-Along Attraction",
    "Haunted Zone Mansion Entrance": "Haunted Zone Mansion Area",
    "Haunted Zone Mansion Area - Dusknoir's Speed Slam Attraction": "Dusknoir's Speed Slam Attraction",
    "Haunted Zone Mansion Rotom's Hidden Entrance": "Haunted Zone Rotom Area",
    "Haunted Zone Rotom Area - Rotom's Spooky Shoot-'em-Up Attraction": "Rotom's Spooky Shoot-'em-Up Attraction",

    "Treehouse Granite Zone Gate": "Granite Zone Main Area",
    "Treehouse Drifblim Fast Travel Granite Zone": "Granite Zone Main Area",
    "Granite Zone Main Area - Absol's Hurdle Bounce Attraction": "Absol's Hurdle Bounce Attraction",
    "Granite Zone Main Area - Salamence's Sky Race Attraction": "Salamence's Sky Race Attraction",

    "Granite Zone Flower Zone Entrance": "Flower Zone Main Area",
    "Treehouse Drifblim Fast Travel Flower Zone": "Flower Zone Main Area",
    "Flower Zone Main Area - Rayquaza's Balloon Panic Attraction": "Rayquaza's Balloon Panic Attraction",

    "Treehouse Piplup Air Balloon": "Skygarden",

}


