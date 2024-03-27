from fastapi.testclient import TestClient
from fastapi import status
from src.app import app

client = TestClient(app)


def test_check_not_exist_contact():
    response = client.get("/v1/contact-address/check_data?phone_number=79500555355")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "message": "Не найден адрес",
        "detail": None,
        "error": None
    }


def test_check_invalid_contact():
    response = client.get("/v1/contact-address/check_data?phone_number=7950055535")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_not_exist_contact():
    response = client.put(
        "/v1/contact-address/write_data",
        json={
            "phone_number": "71234567890",
            "address": "г Иркутск, ул Дзержинского"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_address():
    response = client.post(
        "/v1/contact-address/write_data",
        json={
            "phone_number": "71234567890",
            "address": "г Иркутск, ул Дзержинского"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_update_address_exist_contact():
    response = client.put(
        "/v1/contact-address/write_data",
        json={
            "phone_number": "71234567890",
            "address": "г Иркутск, ул Дзержинского"
        }
    )
    assert response.status_code == status.HTTP_200_OK
