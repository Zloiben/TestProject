from fast_api_core.router import BaseAPIRouter, is_route_method
from fast_api_core.enums.request import HTTPMethods
from fast_api_core.response import ResponsesStructure, ResponseSchema
from fastapi import status

from src.models.contact_address import ContactAddressManagerAnnotated
from src.core.pydentic_field import AnnotatedQueryPhoneNumber
from .schema import CreateContactAddressSchemaV1, ResponseAddressSchemaV1

__all__ = (
    'ContactAddressAPIRouter',
)


class ContactAddressAPIRouter(BaseAPIRouter):
    group_name = 'Адрес Контакта'

    @is_route_method(
        '/write_data',
        method=HTTPMethods.POST,
        summary='Создать новый адрес',
        responses=ResponsesStructure(
            ResponseSchema(
                status_code=status.HTTP_400_BAD_REQUEST,
                description='По указанному номеру телефону уже записан адрес'
            ),
            ResponseSchema(
                status_code=status.HTTP_201_CREATED,
                description='Успешно создан'
            )
        )
    )
    async def create_contact_address(
            self,
            contact_address_manager: ContactAddressManagerAnnotated,
            schema: CreateContactAddressSchemaV1
    ):
        """Метод позволяет сохранить по указанному номеру адрес который ему принадлежит"""
        await contact_address_manager.create(schema)
        return self.interface.insert()

    @is_route_method(
        '/write_data',
        method=HTTPMethods.PUT,
        summary='Редактировать адрес',
        responses=ResponsesStructure(
            ResponseSchema(
                status_code=status.HTTP_400_BAD_REQUEST,
                description='По указанному номеру телефону не записан адрес'
            ),
        )
    )
    async def update_data(
            self,
            contact_address_manager: ContactAddressManagerAnnotated,
            schema: CreateContactAddressSchemaV1
    ):
        """Метод позволяет изменить адрес по указанному номеру телефона"""
        await contact_address_manager.update(schema)
        return self.interface.update()

    @is_route_method(
        '/check_data',
        method=HTTPMethods.GET,
        summary="Получить адрес по номеру телефона",
        responses=ResponsesStructure(
            ResponseSchema(
                status_code=status.HTTP_404_NOT_FOUND,
                description='Не найден адрес'
            )
        ),
        response=ResponseAddressSchemaV1
    )
    async def get_contact_address(
            self,
            contact_address_manager: ContactAddressManagerAnnotated,
            phone_number: AnnotatedQueryPhoneNumber
    ):
        contact_address_data = await contact_address_manager.get(phone_number)
        if not contact_address_data:
            return self.interface.not_found(message='Не найден адрес')
        return {
            'address': contact_address_data
        }
