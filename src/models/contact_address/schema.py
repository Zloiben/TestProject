from src.core.pydentic_field import AnnotatedFieldPhoneNumber, AnnotatedFieldAddress

from pydantic import BaseModel

__all__ = (
    'CreateContactAddressSchema',
)


class CreateContactAddressSchema(BaseModel):
    phone_number: AnnotatedFieldPhoneNumber
    address: AnnotatedFieldAddress
