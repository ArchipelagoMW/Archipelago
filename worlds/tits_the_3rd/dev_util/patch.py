import os
import sys

WORLD_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(WORLD_DIR))

# pylint: disable=import-error, wrong-import-position
from tits_the_3rd.patch.patch import (
    create_patch,
    apply_patch,
    diff
)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./patch.py [create|apply|diff]")
        sys.exit(1)

    if sys.argv[1] == "create":
        create_patch()
    elif sys.argv[1] == "apply":
        apply_patch()
    elif sys.argv[1] == "diff":
        diff()
    else:
        print("Invalid argument. Usage: ./patch.py [create|apply|diff]")
        sys.exit(1)
