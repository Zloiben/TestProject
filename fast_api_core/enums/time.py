from enum import Enum

__all__ = (
    "WeekDay",
)


class WeekDay(int, Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class TimeUnit(Enum):
    Milliseconds = 'ms'
    Seconds = 's'
    Minutes = 'min'
    Hours = 'h'
    Days = 'd'
