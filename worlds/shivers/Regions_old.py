shivers_regions = [
    ["Menu", ["Registry"]],
    ["Registry", ["Outside Museum"]],
    ["Outside Museum", ["Underground Tunnels"]],
    ["Underground Tunnels", ["Underground Lake"]],
    ["Underground Lake", ["Underground Blue Tunnels"]],
    ["Underground Blue Tunnels", ["Office Elevator"]],
    ["Office Elevator", ["Office"]],
    ["Office", ["Workshop", "Lobby", "Bedroom Elevator"]],
    ["Workshop", []],
    ["Bedroom Elevator", ["Bedroom"]],
    ["Bedroom", []],
    ["Lobby", ["Library", "Theater", "Prehistoric", "Egypt"]], #Figure out how handle tar river connection
    ["Library", ["Maintenance Tunnels"]],
    ["Maintenance Tunnels", ["Three Floor Elevator", "Generator"]],
    ["Generator", []],
    ["Theater", ["Theater Back Hallways"]],
    ["Theater Back Hallways", ["Clock Tower Staircase", "Maintenance Tuennls", "Projector Room"]], #Figure out maintenance tunnel connection
    ["Clock Tower Staircase", ["Clock Tower"]],
    ["Clock Tower", []],
    ["Projector Room", []],
    ["Prehistoric", ["Plants", "Ocean"]],
    ["Plants", []],
    ["Ocean", ["Maze Staircase"]],
    ["Maze Staircase", ["Maze"]],
    ["Maze", ["Tar River"]],
    ["Tar River", ["Lobby"]], #Figure out this connection
    ["Egypt", ["Burial", "Blue Maze"]],
    ["Burial", ["Tiki"]],
    ["Tiki", ["Gods Room"]],
    ["Gods Room", ["Anansi"]], #Figure out this connection
    ["Anansi", ["Werewolf"]],
    ["Werewolf", ["Night Staircase"]],
    ["Night Staircase", ["Janitor Closet", "UFO"]],
    ["Janitor Closet", []],
    ["UFO", ["Inventions"]],
    ["Blue Maze", ["Three Floor Elevator", "Fortune Teller", "Inventions"]],
    ["Three Floor Elevator", []], #Figure out if I did this right
    ["Fortune Teller", []],
    ["Inventions", ["Torture"]], #Figure out if I did this right
    ["Torture", ["Puzzle Room Mastermind"]],
    ["Puzzle Room Mastermind", ["Puzzle Room Marbles"]],
    ["Puzzle Room Marbles", ["Skull Dial Bridge"]],
    ["Skull Dial Bridge", ["Slide Room"]],
    ["Slide Room", ["Lobby"]],
]

mandatory_connections = [

]
