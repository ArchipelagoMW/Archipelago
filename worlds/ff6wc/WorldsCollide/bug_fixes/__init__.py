from ..bug_fixes.evade import Evade
from ..bug_fixes.sketch import Sketch
from ..bug_fixes.vanish_doom import VanishDoom
from ..bug_fixes.jump import Jump
from ..bug_fixes.retort import Retort
from ..bug_fixes.enemy_damage_counter import EnemyDamageCounter
from ..bug_fixes.capture import Capture

__all__ = ["BugFixes"]
class BugFixes:
    def __init__(self):
        self.evade = Evade()
        self.sketch = Sketch()
        self.vanish_doom = VanishDoom()
        self.jump = Jump()
        self.retort = Retort()
        self.enemy_damage_counter = EnemyDamageCounter()
        self.capture = Capture()
