
from ..constants.objectives.results import ResultType

class ObjectiveMetadata:
    def __init__(self, objective: ResultType, group):
        self.objective = objective
        self.id = objective.id
        self.name = objective.name
        self.group = group

    def to_json(self):
        formatter = self.objective.format_string
        if "{:+d}" in formatter:
            formatter = formatter.replace('{:+d}', "{{ . }}", True)
        elif "{}" in formatter:
            formatter = formatter.replace('{}', "{{ . }}", True)

        return {
            'id': self.objective.id,
            'name': self.objective.name,
            'value_range': self.objective.value_range,
            'format_string': formatter,
            'group': self.group
        }