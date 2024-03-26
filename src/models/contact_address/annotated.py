from fastapi import Depends
from typing import Annotated

from .manager import ContactAddressManager

__all__ = (
    'ContactAddressManagerAnnotated',
)


async def get_contact_address_manager() -> ContactAddressManager:
    return ContactAddressManager()


ContactAddressManagerAnnotated = Annotated[ContactAddressManager, Depends(get_contact_address_manager)]
