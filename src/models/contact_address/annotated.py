from fastapi import Depends
from typing import Annotated

from .manager import ContactAddressManager

__all__ = (
    'ContactAddressManagerAnnotated',
)


async def get_contact_address_manager() -> ContactAddressManager:
    contact_manager = ContactAddressManager()
    yield contact_manager
    await contact_manager.client.aclose()


ContactAddressManagerAnnotated = Annotated[ContactAddressManager, Depends(get_contact_address_manager)]
