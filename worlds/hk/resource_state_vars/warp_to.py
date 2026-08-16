from . import RCStateVariable, cs, rs
from .resetter import BenchResetVariable, SaveQuitResetVariable, StartRespawnResetVariable


class WarpToBenchResetVariable(RCStateVariable):
    prefix = "$WARPTOBENCH"
    sq_reset: SaveQuitResetVariable
    bench_reset: BenchResetVariable

    def parse_term(self) -> None:
        self.sq_reset = SaveQuitResetVariable(SaveQuitResetVariable.prefix, self.player)
        self.bench_reset = BenchResetVariable(BenchResetVariable.prefix, self.player)

    @classmethod
    def try_match(cls, term: str) -> bool:
        return term.startswith(cls.prefix)

    @property
    def terms(self) -> list[str]:
        return self.sq_reset.terms + self.bench_reset.terms

    def _modify_state(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        valid, state_blob = self.sq_reset._modify_state(state_blob, item_state)
        if valid:
            return self.bench_reset._modify_state(state_blob, item_state)
        else:  # noqa: RET505
            return False, state_blob

    def can_exclude(self, options) -> bool:
        return False


class WarpToStartResetVariable(RCStateVariable):
    prefix = "$WARPTOSTART"
    sq_reset: SaveQuitResetVariable
    start_reset: StartRespawnResetVariable

    def parse_term(self) -> None:
        self.sq_reset = SaveQuitResetVariable(SaveQuitResetVariable.prefix, self.player)
        self.start_reset = StartRespawnResetVariable(StartRespawnResetVariable.prefix, self.player)

    @classmethod
    def try_match(cls, term: str) -> bool:
        return term.startswith(cls.prefix)

    @property
    def terms(self) -> list[str]:
        return self.sq_reset.terms + self.start_reset.terms

    def _modify_state(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        valid, state_blob = self.sq_reset._modify_state(state_blob, item_state)
        if valid:
            return self.start_reset._modify_state(state_blob, item_state)
        else:  # noqa: RET505
            return False, state_blob

    def can_exclude(self, options) -> bool:
        return False
