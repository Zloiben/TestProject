from pydantic import Field
from typing import Annotated
from fastapi import Query

__all__ = (
    'AnnotatedFieldPhoneNumber',
    'AnnotatedQueryPhoneNumber',
    'AnnotatedFieldAddress'
)

PHONE_NUMBER_TITLE = 'Номер телефона'
PHONE_NUMBER_PATTERN = r"7\d{10}"
PHONE_NUMBER_EXAMPLES = ['71234567890']

AnnotatedFieldPhoneNumber = Annotated[
    str,
    Field(
        title=PHONE_NUMBER_TITLE,
        examples=PHONE_NUMBER_EXAMPLES,
        pattern=PHONE_NUMBER_PATTERN
    )
]
AnnotatedQueryPhoneNumber = Annotated[
    str,
    Query(
        title=PHONE_NUMBER_TITLE,
        examples=PHONE_NUMBER_EXAMPLES,
        regex=PHONE_NUMBER_PATTERN,
        max_length=11
    )

]
AnnotatedFieldAddress = Annotated[
    str,
    Field(
        title='Адрес',
        examples=['г Иркутск, ул Дзержинского'],
        max_length=1024
    )
]
