import typing
from Options import Choice, Option


class SampleOption(Choice):
    """
    This is a sample option.
    """
    display_name = "Sample Option"
    option_1 = 1
    option_2 = 2
    default = 0


dark_souls_options: typing.Dict[str, type(Option)] = {
    "sample_option": SampleOption,
}

