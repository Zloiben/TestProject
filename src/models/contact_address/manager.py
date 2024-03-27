from redis.asyncio import Redis

from fast_api_core.validate import ValidationResult
from src.core.redis_client import redis_pool
from .schema import *

__all__ = (
    'ContactAddressManager',
)


class ContactAddressManager:

    def __init__(self):
        self.client = Redis(connection_pool=redis_pool, decode_responses=True)

    async def create(self, schema: CreateContactAddressSchema) -> None:
        validate_result = await self._validate_create(schema)
        validate_result.raise_for_is_valid()
        await self.client.set(name=schema.phone_number, value=schema.address)

    async def update(self, schema: CreateContactAddressSchema) -> None:
        validate_result = await self._validate_update(schema)
        validate_result.raise_for_is_valid()
        await self.client.set(name=schema.phone_number, value=schema.address)

    async def get(self, phone_number: str) -> str:
        return await self.client.get(name=phone_number)

    async def _validate_create(self, schema: CreateContactAddressSchema) -> ValidationResult:
        contact_address = await self.get(schema.phone_number)
        if contact_address:
            return ValidationResult(
                is_valid=False,
                detail='попытка добавить по существующему номеру телефону адрес'
            )
        return ValidationResult(is_valid=True)

    async def _validate_update(self, schema: CreateContactAddressSchema) -> ValidationResult:
        contact_address = await self.get(schema.phone_number)
        if not contact_address:
            return ValidationResult(
                is_valid=False,
                detail='попытка изменить не существующий адрес'
            )
        return ValidationResult(is_valid=True)