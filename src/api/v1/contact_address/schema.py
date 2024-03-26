from pydantic import BaseModel

from src.core.pydentic_field import AnnotatedFieldPhoneNumber, AnnotatedFieldAddress

__all__ = (
    'CreateContactAddressSchemaV1',
    'ResponseAddressSchemaV1'
)


class CreateContactAddressSchemaV1(BaseModel):
    phone_number: AnnotatedFieldPhoneNumber
    address: AnnotatedFieldAddress


class ResponseAddressSchemaV1(BaseModel):
    address: AnnotatedFieldAddress