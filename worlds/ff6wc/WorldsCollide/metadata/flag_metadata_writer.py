from argparse import _StoreTrueAction
import json

blacklisted_args = [
    'help',
    'input_file',
    'output_file',
    'manifest_file',
    'seed_id',
    'debug',
    'no_rom_output',
    'stdout_log'
]

class Object:
    def toJSON(self):
        return self.__dict__

class FlagMetadataWriter:
    def __init__(self, args):
        self.groups = args.parser._action_groups
        self.mutually_exclusive_groups = args.parser._mutually_exclusive_groups
        self.metadata = {}
        
    def get_flag_metadata(self):
        for group in self.groups:
            title = group.title
            description = group.description
            actions = group._group_actions
            group_title =  getattr(group, 'title', '')

            for action in actions:
                if action.dest in blacklisted_args:
                    continue
                for meg in self.mutually_exclusive_groups:
                    if action in (meg._group_actions or []):
                        action.mutually_exclusive_group_title = meg.title

                key = action.option_strings[0]
                self.metadata[key] = Object()
                self.metadata[key].key = action.dest

                if isinstance(action, _StoreTrueAction):
                    self.metadata[key].type = 'bool'
                else:
                    self.metadata[key].type = action.type.__name__ if action.type else str.__name__

                self.metadata[key].flag = action.option_strings[0]

                if action.default:
                    self.metadata[key].default = action.default
                if action.help:
                    self.metadata[key].description = action.help
                if action.nargs:
                    self.metadata[key].nargs = action.nargs
                if action.metavar:
                    self.metadata[key].args = action.metavar
                if action.choices is not None and isinstance(action.choices, list) and not isinstance(action.choices, range):
                    self.metadata[key].allowed_values = list(action.choices)
                if type(group_title):
                    self.metadata[key].group = group_title if type(group_title) == str else None if group_title == None else group_title()
                if getattr(action, 'mutually_exclusive_group_title', None) is not None:
                    self.metadata[key].mutually_exclusive_group = action.mutually_exclusive_group_title
                if getattr(action, 'choices', None) is not None:
                    if isinstance(action.choices, range):
                        self.metadata[key].options = {
                            'min_val': action.choices[0] if isinstance(action.choices, range) else None,
                            'max_val': action.choices[-1] if isinstance(action.choices, range) else None
                        }
        
        val = {key: value.toJSON() for key, value in self.metadata.items()}
        return val

    def write(self):
        from .. import args as args
        import json
        file_name = f"{args.output_file}"
        with open(file_name, "w") as out_file:
            out_file.write(json.dumps(self.get_flag_metadata(), indent = 4))
