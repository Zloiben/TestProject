import re
from datetime import timedelta, timezone
from time import struct_time

from ..enums.time import WeekDay

__all__ = (
    "FORMAT_HH_MM",
    "seconds_since_week_start",
    "get_timezone",
    'replace_russian_to_english'
)
FORMAT_HH_MM = re.compile(r'^([01]\d|2[0-3]):[0-5]\d$')


def seconds_since_week_start(week_day: WeekDay, time_: str) -> struct_time:
    """
    Возвращает временную точку в секундах. Отчет идет от начала недели и до конца недели
    :param week_day: День недели
    :param time_: Время в формате HH:MM
    :return: Объект time
    """
    if not FORMAT_HH_MM.match(time_):
        raise ValueError("Некорректный формат времени. Используйте формат HH:MM")

    second_in_day = 86_400
    hours, minutes = map(int, time_.split(':'))
    seconds_today = hours * 3600 + minutes * 60
    return ((week_day - 1) * second_in_day) + seconds_today


def get_timezone(tz: int = 0) -> timezone:
    """
    Возвращает объект datetime с временной зоной
    :param tz: временная зона
    :return: datetime
    """
    return timezone(timedelta(hours=tz))


def replace_russian_to_english(text: str):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya'
    }

    # Замена каждого символа в тексте
    return ''.join([translit_dict.get(char, char) for char in text.lower()])
