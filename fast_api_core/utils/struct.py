from typing import TypeVar, Set, Dict
import json

T = TypeVar('T')


def is_iterable(obj: T) -> bool:
    """Функция для проверки является ли объект итерируемым"""

    if isinstance(obj, str):
        return False
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def convert_to_set(obj: T) -> Set:
    """Функция для конвертации различных данных в множество"""

    if not is_iterable(obj):
        return {obj}
    return set(obj)


def convert_bytes_to_dict(bytes_value: bytes, encoding: str = 'utf-8') -> Dict:
    """Функция конвертирует биты в словарь. Кодировка UTF-8"""

    return json.loads(bytes_value.decode(encoding))
