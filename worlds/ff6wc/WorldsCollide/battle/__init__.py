from ..battle import formation_flags
from ..battle.multipliers import Multipliers
from ..battle import load_enemy_level
from ..battle import no_exp_party_divide
from ..battle import suplex_train_check
from ..battle import auto_status
from ..battle import end_checks
from ..battle import magitek_upgrade
from ..battle.animations import Animations

__all__ = ["Battle"]
class Battle:
    def __init__(self):
        self.multipliers = Multipliers()
        self.animations = Animations()
