from enum import Enum, auto, unique


@unique
class TypeVideoTypeStatus(str, Enum):
    def _generate_next_value_(item_name, start, count, last_values):
        return str(item_name)

    video_ok = auto()
    video_undefined = auto()
    video_too_short = auto()
    video_size_framesize_small = auto()
    video_file_empty = auto()
    video_file_broken = auto()


@unique
class TypeLoadStatus(str, Enum):
    def _generate_next_value_(item_name, start, count, last_values):
        return str(item_name)

    ok = auto()
    error = auto()


@unique
class TypeExportStatus(str, Enum):
    def _generate_next_value_(item_name, start, count, last_values):
        return str(item_name)

    ok = auto()
    error = auto()
