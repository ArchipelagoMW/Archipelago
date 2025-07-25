def set_rules(world: World, world: World, options: GrinchOptions, int):

rules_dict = {

}

access_rules_dict = {
    "Whoville": (
        "WV Key"
    "Post Office": (
        "Who Cloak"
    ),
    "City Hall": (
        connect_region = "Whoville",
        "REL"
    ),
    "Who Forest": (
        "WF Key",
        "Prog Access Key": 1
    ),
    "Ski Resort": (
        connect_region = "Who Forest",
        "Cable Car Access Card"
    ),
    "Civic Center": (
        connect_region = "Who Forest",
        "GC",
        "OCD"
    ),
    "Who Dump": (
        "WD Key",
        "Prog Access Key": 2
    ),
    "Minefield" (
        connect_region = "Who Dump",
        "REL+SS+RS",
        "REL+GC"
    ),
    "Outside Power Plant": (
        connect_region = "Who Dump",
        "(REL|SS)+GC",
        "(REL|SS)+OCD+SS+RS"
    ),
    "Inside Power Plant": (
        connect_region = "Outside Power Plant",
        "REL+GC",
        "REL+OCD+SS+RS"
    ),
    "Who Lake": (
        "WL Key",
        "Prog Access Key": 3
    ),
    "North Shore": (
        connect_region: "Who Lake",
        "Scout Clothes"
    ),
    "Mayor's Villa": (
        connect_region = "North Shore"
    ),
    "Submarine World": (
        connect_region = "Who Lake",
        "MM"
    )
}