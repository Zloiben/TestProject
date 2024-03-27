from httpx import AsyncClient
import pytest
from fastapi import status
from src.app import app

base_url="http://127.0.0.1:8000"

@pytest.mark.asyncio
async def test_check_not_exist_contact():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/v1/contact-address/check_data?phone_number=79500555355")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {
            "message": "Не найден адрес",
            "detail": None,
            "error": None
        }


@pytest.mark.asyncio
async def test_check_invalid_contact():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/v1/contact-address/check_data?phone_number=7950055535")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_update_not_exist_contact():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.put(
            "/v1/contact-address/write_data",
            json={
                "phone_number": "71234567890",
                "address": "г Иркутск, ул Дзержинского"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_create_address():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post(
            "/v1/contact-address/write_data",
            json={
                "phone_number": "71234567890",
                "address": "г Иркутск, ул Дзержинского"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_update_address_exist_contact():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.put(
            "/v1/contact-address/write_data",
            json={
                "phone_number": "71234567890",
                "address": "г Иркутск, ул Дзержинского"
            }
        )
        assert response.status_code == status.HTTP_200_OK
