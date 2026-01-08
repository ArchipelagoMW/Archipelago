from ..constants.objectives.conditions import ConditionType

class ObjectiveConditionMetadata:
    def __init__(self, id, condition: ConditionType):
        self.id = id
        self.condition = condition

    def to_json(self):
        fn = self.condition.string_function
        value_descriptions = []
        for value in (self.condition.value_range or []):
            if value == "r":
                value_descriptions.append('Random')
            elif hasattr(fn, '__call__'):
                value_descriptions.append(fn(value))
            else:
                value_descriptions.append(value)
        return {
            'id': self.id,
            'condition_type_name': self.condition.name,
            'value_range': getattr(self.condition, 'value_range', None),
            'value_descriptions': value_descriptions,
            'range': self.condition.min_max
        }
