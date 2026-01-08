import math
from collections import Counter, defaultdict
from typing import List, Optional

from BaseClasses import MultiWorld

from worlds.generic.Rules import set_rule


class PuzzleBoard:
    """
    Puzzle board implementation.

    Optimized for efficiently adding pieces to the board and calculating the number of new merges that would be made
    when adding a piece.

    A board stores a cluster ID value for each piece placed on the board, where `None` indicates an empty space on the
    board.
    _0____3_
    ____4_3_
    __1_____
    __1_22__

    Piece placement behaviours:
    A)
    A newly placed piece that does not connect to any existing placed pieces is given a new unique cluster ID and is
    added to a new cluster that is given that ID.
    _0____3_
    ____4_3_
    __1_____
    __1_22_5 <--

    B)
    A newly placed piece that connects to only a single piece gains the cluster ID of the connecting piece.
    _0____3_
    ____4_33 <--
    __1_____
    __1_22_5

    C)
    When a piece is placed that would connect to multiple existing clusters of pieces, the largest of the clusters is
    found and all pieces in the smaller clusters are added into the largest cluster.
    The cluster IDs of the smaller clusters are then returned to the board's list of unique cluster IDs, to be re-used
    later on for new clusters.
    _0____3_     _0____3_
    ____4_33     ____4_33
    __1____X <-- __1____3 <--
    __1_22_5     __1_22_3 <--
    """

    # The puzzle board itself. A 1D list used to represent a 2D board.
    board: list[int | None]
    # A lookup of the adjacent pieces of each piece, used like a dict[int, tuple[int, ...]].
    adjacent_pieces: tuple[tuple[int, ...], ...]
    # The count of merged clusters of connected pieces.
    merges_count: int
    # cluster ID -> piece indices in the cluster.
    clusters: dict[int, list[int]]

    # Unused cluster IDs that newly added pieces can be assigned to if they do not merge into an existing cluster.
    _unused_ids: list[int]

    def __init__(self, width: int, height: int, hexagonal: bool):
        pieces = range(width * height)
        # The maximum number of IDs that could be needed is the maximum number of isolated pieces possible, which is
        # half the number of spaces on the board when even, or half one-more-than-the-number-of-spaces when odd.
        #                   X_X_X
        #      X_X_  X_X_X  _X_X_
        # X_X  _X_X  _X_X_  X_X_X
        # _X_  X_X_  X_X_X  _X_X_
        # X_X  _X_X  _X_X_  X_X_X
        # 5/9  8/16  10/20  13/25
        max_isolated_pieces = len(pieces) // 2 + len(pieces) % 2
        self._unused_ids = list(range(max_isolated_pieces))
        self.board = [None] * (len(pieces))

        # Pre-calculate the pieces that are adjacent to each piece.
        adjacent_pieces = []
        for i in pieces:
            piece_connections = []
            x = i % width
            y = i // width
            if not hexagonal:
                if x > 0:
                    piece_connections.append(i - 1)
                if x < width - 1:
                    piece_connections.append(i + 1)
                if y > 0:
                    piece_connections.append(i - width)
                if y < height - 1:
                    piece_connections.append(i + width)
            else:
                if x > 0:
                    piece_connections.append(i - 1)
                    if x % 2 == 0:
                        piece_connections.append(i - width - 1)
                    else:
                        piece_connections.append(i + width - 1)
                if x < width - 1:
                    piece_connections.append(i + 1)
                    if x % 2 == 0:
                        piece_connections.append(i - width + 1)
                    else:
                        piece_connections.append(i + width + 1)
                piece_connections.append(i - width)
                piece_connections.append(i + width)
                piece_connections = [p for p in piece_connections if p in pieces]
                    
                
            adjacent_pieces.append(tuple(piece_connections))
        self.adjacent_pieces = tuple(adjacent_pieces)
        self.merges_count = 0
        self.clusters = {}

    def add_piece(self, piece_index: int):
        """
        Add a piece to the board.

        The behavior of attempting to add a piece which is already present on the board is undefined.
        """
        board = self.board
        assert board[piece_index] is None, "Attempted to add a piece already present on the board"

        # Get all adjacent cluster IDs.
        # Use incorrect typing to begin with because it is more efficient to remove `None` this way.
        adjacent_clusters: set[int] = {board[adjacent_piece] for adjacent_piece in self.adjacent_pieces[piece_index]}  # type: ignore
        # Empty spaces on the board are set to `None`.
        adjacent_clusters.discard(None)  # type: ignore

        num_adjacent_clusters = len(adjacent_clusters)
        if num_adjacent_clusters == 0:
            # The new piece is isolated, add it to a new cluster.
            new_cluster_id = self._unused_ids.pop()
            board[piece_index] = new_cluster_id
            self.clusters[new_cluster_id] = [piece_index]
        elif num_adjacent_clusters == 1:
            # The new piece is adjacent to only one cluster, add it to that cluster.
            self.merges_count += 1
            found_cluster = next(iter(adjacent_clusters))
            board[piece_index] = found_cluster
            self.clusters[found_cluster].append(piece_index)
        else:
            # The new piece is adjacent to multiple clusters, add it to the largest cluster and move all pieces in the
            # other clusters into the largest cluster.
            self.merges_count += num_adjacent_clusters
            clusters = self.clusters

            # Find the largest of the clusters.
            # Get the first cluster and set it as the current largest.
            clusters_iter = iter(adjacent_clusters)
            first_cluster_id: int = next(clusters_iter)
            pieces_in_cluster = clusters[first_cluster_id]
            # The clusters and their IDs need to be looped through again once the largest cluster has been determined,
            # so a list is created to skip having to get the clusters a second time.
            clusters_and_ids = [(first_cluster_id, pieces_in_cluster)]
            # Initialise variables for storing the largest cluster.
            largest_cluster_id = first_cluster_id
            largest_pieces_in_cluster = pieces_in_cluster
            largest_cluster_size = len(pieces_in_cluster)
            # Iterate through the remaining clusters.
            for cluster_id in clusters_iter:
                pieces_in_cluster = clusters[cluster_id]
                cluster_size = len(pieces_in_cluster)
                clusters_and_ids.append((cluster_id, pieces_in_cluster))
                if cluster_size > largest_cluster_size:
                    largest_cluster_size = cluster_size
                    largest_cluster_id = cluster_id
                    largest_pieces_in_cluster = pieces_in_cluster

            # Add the new piece to the largest cluster and write cluster ID onto the board for the new piece.
            board[piece_index] = largest_cluster_id
            largest_pieces_in_cluster.append(piece_index)

            # Add the pieces in the smaller clusters into the largest cluster.
            unused_ids = self._unused_ids
            for cluster_id, pieces_in_cluster in clusters_and_ids:
                if pieces_in_cluster is largest_pieces_in_cluster:
                    continue
                largest_pieces_in_cluster.extend(pieces_in_cluster)
                # Remove the cluster from the board's clusters.
                del clusters[cluster_id]
                # Release the cluster's ID back to the board.
                unused_ids.append(cluster_id)
                # Write the new cluster ID onto the board for each piece.
                for piece_idx in pieces_in_cluster:
                    board[piece_idx] = largest_cluster_id

    def get_merges_from_adding_piece(self, piece_index: int):
        """
        Get the number of merges that would be made by adding a piece.

        The behavior of attempting to get the number of merges from adding a piece which is already present in the board
        is undefined.
        """
        # Get all adjacent cluster IDs.
        board = self.board
        assert board[piece_index] is None, "Attempted to get the merges for adding a piece already present on the board"
        found_cluster_ids = {board[connection] for connection in self.adjacent_pieces[piece_index]}
        # Empty spaces on the board are set to `None`, so don't count `None` when counting the number of clusters.
        return len(found_cluster_ids) - 1 if None in found_cluster_ids else len(found_cluster_ids)

    def remove_piece(self, piece_index: int):
        """
        Remove a piece from the board.

        This is more expensive than adding pieces and is more expensive the larger the cluster that the removed piece
        was part of.
        """
        board = self.board
        cluster_id = board[piece_index]
        assert cluster_id is not None, "Attempted to remove a piece that is not present on the board"
        # Remove the cluster this piece is in.
        pieces_in_cluster = self.clusters.pop(cluster_id)
        # The cluster ID is now unused, so give it back to the board.
        self._unused_ids.append(cluster_id)

        # Clear the space on the board where the cluster was.
        for i in pieces_in_cluster:
            board[i] = None

        # Remove the piece, that has been removed from the board, from the list.
        pieces_in_cluster.remove(piece_index)

        # Reduce the total merges by the merges of the real cluster.
        # Note that `piece_index` has already been removed from `pieces_in_cluster`.
        self.merges_count -= len(pieces_in_cluster)

        # Add all the pieces back on, besides the removed piece.
        add_piece = self.add_piece
        for i in pieces_in_cluster:
            add_piece(i)
