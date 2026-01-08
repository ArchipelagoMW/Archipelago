from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Range, Toggle, OptionGroup, Removed, Visibility

class NumberOfPieces(Range):
    """
    Approximate number of pieces in the puzzle.
    Note that this game is more difficult than regular jigsaw puzzles, because you don't start with all pieces :)
    Also make sure the pieces are not too small on your screen if you choose many.
    """

    display_name = "Number of pieces"
    range_start = 4
    range_end = 2000
    default = 50
    
class NumberOfPieceBundles(Range):
    """
    The (maximum) number of piece bundles; items that give you 1 or more pieces.
    Having too many of these may hurt the multiworld and put too much emphasis on the jigsaw puzzle.
    For solo games I would recommend to put this to the maximum.
    """
    
    display_name = "Number of piece bundles"
    range_start = 25
    range_end = 2000
    default = 250
    
class MinimumNumberOfPiecesPerBundle(Range):
    """
    This is another way to choose the number of piece bundles.
    With this option you can choose the minimum number of pieces per bundle.
    For example if you make this 2, you will get at least 2 pieces at a time. Probably more fun for others!
    For solo games I would recommend to put this to 1.        
    """
    
    display_name = "Minimum number of pieces per bundle"
    range_start = 1
    range_end = 100
    default = 1
        
class AddFillers(Toggle):
    """
    Enabling this option makes every merge a check and adds filler items.
    The next option allows you to choose how many are local and how many are shuffled across the multiworld.
    """
    
    display_name = "Add fillers"
    default = True
    
    
class PercentageFillersItempool(Range):
    """
    If fillers are added, this option determines how many of the fillers are shuffled across the multiworld.
    """
    
    display_name = "Percentage fillers itempool"
    range_start = 0
    range_end = 100
    default = 0

    
class OrientationOfImage(Choice):
    """
    If you're using a custom image, select the orientation here.
    This affects the shape of the puzzle pieces.
    It doesn't have to be exactly right.

    Here's the aspect ratio's that are calculated with (width x height)
    square: 1 x 1
    landscape: 1.5 x 1
    portrait: 0.8 x 1
    more_landscape: 2 x 1
    more_portrait: 0.5 x 1
    """

    display_name = "Orientation of image"
    option_square = 1
    option_landscape = 2
    option_portrait = 3
    option_more_landscape = 4
    option_more_portrait = 5
    default = 2


class UniformPieceSize(Toggle):
    """
    If enabled, all puzzle pieces will have equal width and height.
    Especially fun with rotations, you won't be able to see which rotations are clearly wrong.
    Note: your image will be cropped if necessary!
    Note: this setting is turned off when using meme one row or column.
    """
    display_name = "Uniform piece size"
    default = False


class WhichImage(Range):
    """
    Only if you selected the landscape orientation option.
    This option decides which landscape picture will be set for you. Don't worry, you can change it in the game.
    Every number corresponds to a set image. See the images here: https://jigsaw-ap.netlify.app/images.html
    """
    
    display_name = "Which image"
    range_start = 1
    range_end = 54
    default = "random"
    
class PercentageOfExtraPieces(Range):
    """
    This option allows for there being more pieces in the pool than necessary.
    When you have all your items already, the additional pieces don't do anything anymore.
    0 means there are exactly enough pieces in the pool.
    100 means there are twice as many pieces in the pool than necessary.
    That means you would only need half of your items to finish the game.
    """

    display_name = "Percentage of extra pieces"
    range_start = 0
    range_end = 100
    default = 10
    
class PieceTypeOrder(Choice):
    """
    This option affects the order in which you receive puzzle piece types.
    This is prioritized over the Piece Order option.
    
    random_order: no order is followed
    
    corners_edges_normal: you will first get all corner pieces, then edge pieces, then normal pieces
    (...)
    
    four_parts and four_parts_non_rotated:
    The board will be divided into four (rotated) quadrants.
    You will first get all pieces of one of the first quadrant, then for the second, etc.
    This makes it so that you're basically starting and finishing a section four times in your playthrough.
    This may be nice for big puzzles, it decreases the pressure at the start, while making the ending more interesting.
    four_parts_non_rotated always gives axis-aligned quadrants (rectangular grid-like splits, like a +).
    four_parts can involve rotated splits, so the quadrants may be split like + or x etc.
    """

    display_name = "Piece type order"
    option_random_order = 1
    option_corners_edges_normal = 2
    option_normal_edges_corners = 3
    option_edges_normal_corners = 4
    option_corners_normal_edges = 5
    option_normal_corners_edges = 6
    option_edges_corners_normal = 7
    option_four_parts = 8
    option_four_parts_non_rotated = 9
    default = 1
    
class StrictnessPieceTypeOrder(Range): 
    """
    This option determines how strictly the above piece type order is followed.
    1 means it is barely followed, 100 means it is followed in the strictest way possible.
    """

    display_name = "Strictness piece type order"
    range_start = 1
    range_end = 100
    default = 100
    
class PieceOrder(Choice):
    """
    This option affects the order in which you receive puzzle pieces.
    random_order: pieces are added in random order with no extra constraints
    every_piece_fits: every piece you receive, will be able to merge with another piece
    least_merges_possible: you will receive pieces in an order that gives the least number of possible merges
    """

    display_name = "Piece order"
    option_random_order = 1
    option_every_piece_fits = 3
    option_least_merges_possible = 4
    default = 1
    
class StrictnessPieceOrder(Range): 
    """
    This option determines how strictly the above piece order is followed.
    1 means it is barely followed, 100 means it is followed in the strictest way possible.
    """

    display_name = "Strictness piece order"
    range_start = 1
    range_end = 100
    default = 100
    
class ChecksOutOfLogic(Range):
    """
    This option will make it so that there are always additional checks not considered by logic.
    This makes it easier to get "all your checks in logic".
    Of course this won't make a difference at the very end when few merges are left.
    The number of checks out of logic will never be more than 10% of the number of pieces.
    """

    display_name = "Checks out of logic"
    range_start = 0
    range_end = 200
    default = 1
    
class StartingFakePieces(Range):
    """
    Number of fake pieces that appear at the start of the game.
    These pieces cannot merge with any other pieces.
    """

    display_name = "Starting fake pieces"
    range_start = 0
    range_end = 500
    default = 0
    
class NumberOfFakePieceBundles(Range):
    """
    Number of fake piece bundles in the itempool.
    """

    display_name = "Number of fake piece bundles"
    range_start = 0
    range_end = 50
    default = 0
    
class ImpactOfFakePieceBundles(Range):
    """
    How many fake pieces each fake piece bundle gives.
    """

    display_name = "Impact of fake piece bundles"
    range_start = 1
    range_end = 10
    default = 1
    
class NumberOfRotateTraps(Range):
    """
    Number of rotate traps in the itempool, that randomly rotate small clusters (<10 pieces).
    This trap is only added when the rotations option is enabled.
    """
    
    display_name = "Number of rotate traps"
    range_start = 0
    range_end = 500
    default = 0
    
class ImpactOfRotateTraps(Range):
    """
    How many clusters each rotate trap affects.
    """

    display_name = "Impact of rotate traps"
    range_start = 1
    range_end = 10
    default = 1

class NumberOfSwapTraps(Range):
    """
    Number of swap traps in the itempool, that randomly swap two small clusters (<10 pieces).
    """

    display_name = "Number of swap traps"
    range_start = 0
    range_end = 500
    default = 0
    
class ImpactOfSwapTraps(Range):
    """
    How many clusters each swap trap affects.
    """

    display_name = "Impact of swap traps"
    range_start = 1
    range_end = 10
    default = 1
    
class EnableClues(Toggle):
    """
    Enable clues for the jigsaw puzzle.
    If enabled, there is a button that shows the outline of pieces that can merge (unlimited uses).
    If disabled, the button is simply not there.
    """

    display_name = "Enable clues"
    default = True
    
class SizeOfImage(Range):
    """
    How large the pieces will be. 100 means the puzzle is maximum size. 50 means width and height are halved.
    If you want a lot of free space around the puzzle, you can set this to a lower value.
    """

    display_name = "Size of image"
    range_start = 30
    range_end = 100
    default = 85
    
class DeathLink(Range):
    """
    When someone else dies, you'll get rotate traps and swap traps.
    The number you set here determines how many traps you get.
    If you set this to 0, deathlink is disabled.
    (Jigsaw will never trigger death link.)
    """

    display_name = "Death link"
    range_start = 0
    range_end = 10
    default = 0
    
class GridType(Choice):
    """
    The type of grid used for the jigsaw puzzle. Square is the default and most common type.
    But hexagonal grids are also possible, which can make the puzzle more interesting.
    
    Also, these are meme options: all pieces are just in one row or one column.
    This means pieces are really long. Be careful with too many pieces, 
    and consider using the "straight" shape you can select in the game before pressing start.
    """

    display_name = "Grid type"
    option_square = 4
    option_hexagonal = 6
    
    option_meme_one_row = 90
    option_meme_one_column = 91
    default = 4
    
class GridTypeAndRotations(Choice):
    """
    The type of grid used for the jigsaw puzzle, along with the rotation options.
    The "meme" options create really long or wide pieces in just one row or one column.
    """

    display_name = "Grid type and rotations"
    option_square_no_rotation = 1
    option_square_180_rotation = 2
    option_square_90_rotation = 3
    option_hex_no_rotation = 4
    option_hex_180_rotation = 5
    option_hex_120_rotation = 6
    option_hex_60_rotation = 7
    option_meme_one_row_no_rotation = 8
    option_meme_one_row_180_rotation = 9
    option_meme_one_column_no_rotation = 10
    option_meme_one_column_180_rotation = 11
    default = 1

class BorderType(Choice):
    """
    The type of border used for the jigsaw puzzle. You can change this in-game.
    
    Classic: the typical jigsaw pieces with the innies and outies.
    Triangle: the typical jigsaw pieces where innies and outies are triangles.
    Curved: each of the borders are round curves.
    Diagonal: the borders are straight edges but at an angle.
    Straight: the borders are straight edges. So the pieces are actual rectangles or hexagons.
    Chaos: every border can be each of the other border types.
    """

    display_name = "Border type"
    option_classic = 1
    option_triangle = 2
    option_curved = 3
    option_diagonal = 4
    option_straight = 5
    option_chaos = 6
    default = 1


@dataclass
class JigsawOptions(PerGameCommonOptions):
    death_link: DeathLink
    number_of_pieces: NumberOfPieces
    grid_type_and_rotations: GridTypeAndRotations
    uniform_piece_size: UniformPieceSize
    percentage_of_extra_pieces: PercentageOfExtraPieces
    number_of_piece_bundles: NumberOfPieceBundles
    minimum_number_of_pieces_per_bundle: MinimumNumberOfPiecesPerBundle
    add_fillers: AddFillers
    percentage_fillers_itempool: PercentageFillersItempool
    checks_out_of_logic: ChecksOutOfLogic
    orientation_of_image: OrientationOfImage
    which_image: WhichImage
    piece_order_type: PieceTypeOrder
    strictness_piece_order_type: StrictnessPieceTypeOrder
    piece_order: PieceOrder
    strictness_piece_order: StrictnessPieceOrder
    enable_clues: EnableClues
    total_size_of_image: SizeOfImage
    starting_fake_pieces: StartingFakePieces
    number_of_fake_piece_bundles: NumberOfFakePieceBundles
    impact_of_fake_piece_bundles: ImpactOfFakePieceBundles
    number_of_rotate_traps: NumberOfRotateTraps
    impact_of_rotate_traps: ImpactOfRotateTraps
    number_of_swap_traps: NumberOfSwapTraps
    impact_of_swap_traps: ImpactOfSwapTraps
    #removed:
    maximum_number_of_real_items: Removed
    minimum_number_of_pieces_per_real_item: Removed
    placement_of_fillers: Removed
    enable_forced_local_filler_items: Removed
    percentage_of_fillers_globally: Removed
    permillage_of_checks_out_of_logic: Removed
    fake_pieces: Removed
    rotate_traps: Removed
    swap_traps: Removed
    grid_type: Removed
    rotations: Removed
    border_type: BorderType
    
jigsaw_option_groups = [
    OptionGroup("Important options: gameplay",
        [
            NumberOfPieces,
            GridTypeAndRotations,
            UniformPieceSize,
            BorderType
        ],
    ),
    OptionGroup(
        "Important options: image",
        [
            OrientationOfImage,
            WhichImage,
        ],
    ),
    OptionGroup(
        "Optional options: extra pieces, items and checks",
        [
            PercentageOfExtraPieces,
            NumberOfPieceBundles,
            MinimumNumberOfPiecesPerBundle,
            AddFillers,
            PercentageFillersItempool,
            ChecksOutOfLogic,
        ],
    ),
    OptionGroup(
        "Optional options: piece order",
        [
            PieceTypeOrder,
            StrictnessPieceTypeOrder,
            PieceOrder,
            StrictnessPieceOrder,
        ],
    ),
    OptionGroup(
        "Optional options: traps & deathlink",
        [
            StartingFakePieces,
            NumberOfFakePieceBundles,
            ImpactOfFakePieceBundles,
            NumberOfRotateTraps,
            ImpactOfRotateTraps,
            NumberOfSwapTraps,
            ImpactOfSwapTraps,
            DeathLink,
        ],
    ),
    OptionGroup(
        "Optional options: other",
        [
            EnableClues,
            SizeOfImage,
        ],
    ),
]
