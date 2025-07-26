# ChecksMate Chess

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What is considered a location check in ChecksMate?

Perform various feats of style, grace, and conquest.

 - Capture individual enemy pieces and pawns (e.g. capture pawn E, the pawn that begins on the E file)
 - Capture multiple enemy pieces and pawns in 1 match (e.g. capture any 2 pawns), including sequences of pairs (e.g. both 2 pieces and 2 pawns)
 - Attack (e.g. threaten) any opposing pawn, minor piece, major piece, or queen
 - Attack multiple opposing pieces with a single piece (Sacrificial if it is itself attacked, True otherwise): two pieces, three pieces, and the King and Queen
 - Move your King each of: forward one space, to the A file, to the center 4 squares, to the opposing home rank, and to capture a piece
 - Perform the French move

## When the player receives an item, what happens?

The player will receive either:

 - The white pieces (permitting the player to make the first move)
 - A piece of material, being a pawn, piece, or upgrade for a piece
 - Engine Elo reduction, eagerly bringing the 2000+ Elo engine down to a beatable level
   - Before calculation penalties are applied, the current supported engines have an approximate Elo (in an AI-only tournament) of at least 2030. See: https://www.computerchess.org.uk/ccrl/404/
 - Pawn forwardness - placing a random pawn on the 3rd rank rather than the 2nd
 - A pocket piece, which can be played from one of your three pockets onto the board! 
   - Powerful pieces cannot be played onto the board at the start of the game. One must wait turns equal to their material value before playing such a piece
   - In addition, the player may receive "Pocket Gems", which grant "turns passed" toward pocket pieces
   - Finally, "Pocket Range" allows these pocket pieces to deploy onto ranks beyond the home rank, from 1st up to the 7th rank
 - A Consul, adding an extra King piece. You lose when all of your Kings are captured
 - A King Upgrade, where your primary King (not Consuls) becomes a Mounted King and gains Knight movement
   - When you gain both King Upgrades, your primary King becomes a Hyper King and gains Nightrider (Knight slider) and Elephant (2x diagonal leaper) movement

## What is the victory condition?

Put the opposing King in checkmate.
