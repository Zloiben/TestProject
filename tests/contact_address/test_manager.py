import pytest

from fastapi import HTTPException
from pydantic import ValidationError

from src.models.contact_address import ContactAddressManager, CreateContactAddressSchema


@pytest.mark.asyncio
async def test_create_and_get():
    """
    Тест номер 1.
    Условия полностью соответствуют требованиям
    Ожидаемый результат:
    Создастся запись и потом получится ее получить
    """
    contact_address_manager = ContactAddressManager()
    phone_number = "79500555355"
    address_test = 'Тестовый адрес'
    await contact_address_manager.create(
        schema=CreateContactAddressSchema(
            address=address_test,
            phone_number=phone_number
        )
    )
    address_value = await contact_address_manager.get(phone_number=phone_number)
    assert address_value == address_test


@pytest.mark.asyncio
async def test_invalid_contact_1():
    """
    Тест номер 2.
    Условие что будет не верный формат номера телефона.
    Ожидаемый результат:
    Будет ошибка, что не верный номер телефона
    """
    contact_address_manager = ContactAddressManager()
    phone_number = "89500555355"
    address_test = 'Тестовый адрес'
    with pytest.raises(ValidationError) as _:
        await contact_address_manager.create(
            schema=CreateContactAddressSchema(
                address=address_test,
                phone_number=phone_number
            )
        )


@pytest.mark.asyncio
async def test_invalid_contact_2():
    """
    Тест номер 3
    Условие что будет не полный номер отправлен
    Ожидаемый результат:
    Будет ошибка, что не верный номер телефона
    """
    contact_address_manager = ContactAddressManager()
    phone_number = "895005"
    address_test = 'Тестовый адрес'
    with pytest.raises(ValidationError) as _:
        await contact_address_manager.create(
            schema=CreateContactAddressSchema(
                address=address_test,
                phone_number=phone_number
            )
        )


@pytest.mark.asyncio
async def test_contact_exist_add_address():
    """
    Условие что будет отправлен существует номер телефона которому нужно будет создать адрес
    Ожидаемый результат:
    будет ошибка, которая указывает на то что у этого номера уже есть адрес
    """
    contact_address_manager = ContactAddressManager()
    phone_number = "79500555355"
    address_test = 'Тестовый адрес'
    with pytest.raises(HTTPException) as _:
        await contact_address_manager.create(
            schema=CreateContactAddressSchema(
                address=address_test,
                phone_number=phone_number
            )
        )


@pytest.mark.asyncio
async def test_update_not_exist_contact():
    """
    Условие изменить адрес у не существующего контакта
    Ожидаемый результат:
    будет ошибка, которая указывает на то что номера телефона не существует
    """
    contact_address_manager = ContactAddressManager()
    phone_number = "79500555000"
    address_test = 'Тестовый адрес'
    with pytest.raises(HTTPException) as _:
        await contact_address_manager.update(
            schema=CreateContactAddressSchema(
                address=address_test,
                phone_number=phone_number
            )
        )


@pytest.mark.asyncio
async def test_update_exist_contact():
    """
    Условие изменить у существующего контакта адрес
    Ожидаемый результат:
    все пройдет успешно
    """
    contact_address_manager = ContactAddressManager()
    phone_number = "79500555355"
    address_test = 'Новый тестовый адрес'
    await contact_address_manager.update(
        schema=CreateContactAddressSchema(
            address=address_test,
            phone_number=phone_number
        )
    )
    address_value = await contact_address_manager.get(phone_number=phone_number)
    assert address_value == address_test
