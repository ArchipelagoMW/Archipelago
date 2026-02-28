"""Path Hint Tree data for evaluating the strength of path hints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Dict

from randomizer.Enums.Locations import Locations


class PathHintTreeNode:
    """A node on the greater path hint tree."""

    def __init__(self, loc: Locations) -> None:
        """Create a path hint tree node for the parameter location."""
        self.node_location_id = loc
        self.path_hinted = False
        self.in_region_with_path_hint = False
        self.woth_hinted = False
        self.region_hinted = False
        self.goals = []
        self.parents = []
        self.children = []
        self.unhinted_score = 0.0
        self.score_multiplier = 1.0


def BuildPathHintTree(woth_paths: Dict[Locations, List[Locations]]) -> Dict[Locations, PathHintTreeNode]:
    """Assemble a list of multipath nodes that represent a tree from a list of Way of the Hoard paths."""
    # TWO EXTREMELY IMPORTANT ASSUMPTIONS:
    # 1. The woth_paths keys are in order, meaning no earlier path has any elements that are a key for a future path.
    # 2. The woth_paths values are ordered such that each path is a subset of the list of all keys without any reordering. (The order of each path matches the order of the dict's keys)
    tree: Dict[Locations, PathHintTreeNode] = {}
    # Traverse the list of paths in that careful order - this ensures we make the top-level parentless nodes first
    for woth_loc_id, path in woth_paths.items():
        node = PathHintTreeNode(woth_loc_id)
        seen_nodes = set()
        # For each item in the path in reverse order - this ensures we find the most-direct parents of this child first
        for path_loc_id in reversed(path):
            # If we've seen this location in our traversal, it's not a direct parent of this node - obviously you're also not your own parent.
            if path_loc_id not in seen_nodes and path_loc_id != woth_loc_id and path_loc_id in woth_paths.keys() and path_loc_id in tree.keys():
                # Any node we haven't seen must be a direct parent of this node
                node.parents.append(path_loc_id)
                # Which means this is a child of that node as well
                tree[path_loc_id].children.append(woth_loc_id)
                # All nodes on the path to the parent now count as seen - this is how we prevent inaccurate parentage
                seen_nodes = seen_nodes.union(set(woth_paths[path_loc_id]))
        # By adding this node here, all future loops will be able to add this as a parent and this node can have it's children added as well
        tree[woth_loc_id] = node
    return tree
