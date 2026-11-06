from typing import ClassVar
from copy import copy
import random

from test.bases import WorldTestBase
from .. import CMWorld


class CMTestBase(WorldTestBase):
	game = "ChecksMate"
	world: CMWorld
	player: ClassVar[int] = 1

	def setUp(self) -> None:
		# WorldTestBase seeds the process-wide RNG during world setup.
		self.addCleanup(random.setstate, random.getstate())
		super().setUp()

	def world_setup(self, *args, **kwargs) -> None:
		# TODO(chesslogic): Subclasses could implement a "modify_options" method
		# to modify the options before the world is constructed
		self.options = copy(self.options)
		super().world_setup(*args, **kwargs)
		if self.constructed:
			self.world = self.multiworld.worlds[self.player]  # noqa

