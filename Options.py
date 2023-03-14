import typing
from Options import Choice, Option, Toggle, Range, DeathLink


class Keysanity(Choice):
	"""
	Whether to shuffle the doors Keyzers unlock
	Off: Keyzer unlocks the next door in this passage
	Simple: Keyzer unlocks the next door in a random passage
	Full: Keyzer unlocks a random door
	"""
	display_name = "Shuffle Keyzers"
	option_off = 0
	option_simple = 1
	option_full = 2
	default = 0


class MusicShuffle(Choice):
	"""
	Music shuffle type
	None: Music is not shuffled
	Levels only: Only shuffle music between the main levels besides the Golden Passage
	Full: Shuffle all music
	"""
	display_name = "Music Shuffle"
	option_none = 0
	option_levels_only = 1
	option_full = 2
	default = 0


wl4_options: typing.Dict[str, type(Option)] = {
	"death_link": DeathLink
	# "keyzer": Keysanity
	# "music_shuffle": MusicShuffle
}