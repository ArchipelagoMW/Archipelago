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

## What are the supported Goals?

 - Single: Checkmate your opponent on a normal 8x8 board. There is no board growth.
 - Ordered Progressive (the default): Checkmate on 8x8, then each checkmate grows the board (10x8, 10x10, 12x10,
   12x12, in that fixed order). The Board Files/Board Ranks unlocks are locked directly to your own Checkmate
   Minima/Maxima/10x10/12x10 checks rather than being shuffled into the general multiworld pool, so board growth
   always follows this exact order. Checkmate on the final 12x12 board to win.
 - Progressive: As Ordered Progressive, but the Board Files/Board Ranks unlocks are ordinary shuffled items in the
   multiworld pool, so which board grows next (and when, and for whom) can vary.
 - Super: As Progressive, but you start already holding the first Board Files unlock, skipping straight past 8x8;
   later Board Files/Board Ranks unlocks still come from the shuffled pool.

Larger boards also unlock their own harder checks (e.g. later Capture Pawn/Fork/Play Turns locations and the tougher
Checkmate Maxima material target), so Goal affects both the victory condition and how much of the location pool you
can reach.

## What's the difference between Legacy and Fundamental itemization (Progression Itemization)?

Legacy is the original item family: separate Progressive items per piece family (Pawn, Minor Piece, Major Piece,
Major To Queen, Jack), each tracked and counted individually. Fundamental instead uses two shared items for that same
piece/pawn progression - "Chessmen" (any pawn or piece) and "Material" (overall strength) - plus a "Castler" item,
trading per-family precision for a smaller, simpler item set. Items unrelated to piece/pawn progression (Consuls,
King Upgrades, Pockets, Board Files/Ranks, etc.) are unaffected and work the same in both modes. Both modes produce
the same kinds of in-game rewards; this option only changes how piece/pawn progress is itemized and counted for
logic.

## What unlocks castling?

Castling (the "O-O Castle" and "O-O-O Castle" checks) requires enough of your Major-piece-family progress to be
uncommitted to Queen promotion. In Fundamental itemization this is a single "Castler" item (bounded by your Chessmen
and Material progress). In Legacy itemization it's derived from your Progressive Major Piece and Progressive Jack
counts after reserving for every obtainable Progressive Major To Queen, so finding later upgrades cannot make a
previously reachable castle check inaccessible.

## What's the difference between Early Material, Locked Items, Start Inventory, and Start Inventory From Pool?

 - Early Material: Guarantees the "King to E2/E7 Early" check gives you a chessman of the chosen family
   immediately, regardless of exclusions. It's still drawn from, and counted against, that family's normal pool.
 - Locked Items: Forces a minimum count of specific items into the generated pool somewhere - guaranteed to exist,
   but not guaranteed to be found quickly or in your own world.
 - Start Inventory (a standard Archipelago option): Gives you extra copies as free starting items, in addition to
   the normal pool - a bonus that doesn't reduce what's randomized elsewhere.
 - Start Inventory From Pool: Also starts you with the item, but removes those copies from the shuffled pool - it
   doesn't add extra material, it just guarantees you already hold specific pieces from turn one.

## What is the victory condition?

Put the opposing King in checkmate.
