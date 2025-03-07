from enum import unique, Enum, auto


@unique
class TypeLoadStatus(str, Enum):
    def _generate_next_value_(item_name, start, count, last_values):
        return str(item_name)

    ok = auto()
    error = auto()
    video_too_short = auto()
    video_size_small = auto()
    video_file_empty = auto()
    video_file_unsupported = auto()
    video_file_broken = auto()


@unique
class TypeExportStatus(str, Enum):
    def _generate_next_value_(item_name, start, count, last_values):
        return str(item_name)

    ok = auto()
    error = auto()
