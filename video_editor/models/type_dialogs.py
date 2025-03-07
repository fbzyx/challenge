from enum import unique, Enum, auto


@unique
class TypeDialog(str, Enum):
    def _generate_next_value_(item_name, start, count, last_values):
        return str(item_name)

    info = auto()
    error = auto()
    warning = auto()
    question = auto()
