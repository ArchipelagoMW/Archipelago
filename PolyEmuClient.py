import sys
import ModuleUpdate
ModuleUpdate.update()

from worlds._polyemu.context import launch

if __name__ == "__main__":
    launch(*sys.argv[1:])
