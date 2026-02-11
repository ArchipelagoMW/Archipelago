
import ast
import os.path

import astor  # You might need to install via `pip install astor`

from worlds.shadow_the_hedgehog import Levels, Weapons
from worlds.shadow_the_hedgehog.ObjectTypes import SETObject, ObjectType
from .Items import GetAllItemInfo


class AddArgumentToSETObject(ast.NodeTransformer):
    replaceWith = None

    def __init__(self, setReplacement):
        super().__init__()  # not strictly required, but good practice
        self.replaceWith = setReplacement

    def visit_Call(self, node: ast.Call):
        # First, transform children
        self.generic_visit(node)

        index_value = node.args[2].value

        # Only touch calls to SETObject(...)
        if isinstance(node.func, ast.Name) and node.func.id == "SETObject" and \
            self.replaceWith.index == index_value:
            # Check if keyword already present (e.g. SETObject(..., optional_arg=...)
            already_has_kw = any(
                isinstance(kw, ast.keyword) and kw.arg == "weapon"
                for kw in node.keywords
            )

            if not already_has_kw:
                # Add optional keyword argument with a default value
                node.keywords.append(
                    ast.keyword(
                        arg="weapon",
                        value=ast.Constant(value=self.replaceWith.weapon),
                    )
                )

        return node

def modify_file(file_path):
    # Read source

    with open(file_path, "r") as f:
        source = f.read()

    # Parse into AST
    tree = ast.parse(source)

    # Transform the AST

    s = SETObject(ObjectType.VEHICLE, Levels.STAGE_THE_ARK, 1, "Black Volt 1",
              vehicle=ObjectTypeVehicles.BLACK_VOLT, weapon=WEAPONS.BLACK_BARREL)

    transformer = AddArgumentToSETObject(s)
    modified_tree = transformer.visit(tree)


    # Generate new source code
    modified_source = astor.to_source(modified_tree)
    modified_source = modified_source.replace(", SET", ",\n\tSET")

    print(modified_source)  # Or write back to file

# Example usage
if __name__ == "__main__":
    modify_file("worlds/shadow_the_hedgehog/Objects_TheArk.py")