import pytest
from pytest_httpx import HTTPXMock

from arcade_tdk import ToolContext, ToolSecretItem

from tessie.tools.drivers import list_driver, delete_driver

@pytest.fixture
def mock_context():
    context = ToolContext()
    context.secrets = []
    context.secrets.append(
        ToolSecretItem(
            key="TESSIE_TOKEN", value="TESSIE_TOKEN"
        )
    )

    return context

@pytest.mark.asyncio
async def test_get_drivers_no_drivers(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="GET",
        status_code=200,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/drivers",
        json={
            "response": []
        },
    )

    assert await list_driver("5YJ3E1EA4KF555555", mock_context) == {
        "drivers": []
    }

@pytest.mark.asyncio
async def test_get_drivers_bad_request(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="GET",
        status_code=500,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/drivers",
        json={
            "response": []
        },
    )

    with pytest.raises(Exception):
        await list_driver("5YJ3E1EA4KF555555", mock_context)

@pytest.mark.asyncio
async def test_get_drivers_retuned_list(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/drivers",
        status_code=200,
        json={
            "response": [
                {
                    "my_tesla_unique_id": 88888888,
                    "user_id": 1234567,
                    "user_id_s": "1234567",
                    "driver_first_name": "Jane",
                    "driver_last_name": "Doe",
                    "granular_access": {
                        "hide_private": False
                    },
                    "active_pubkeys": [
                        "043da2708632f7d7c01f6casdf824007465408d475c37a6adfaa19aed565f3e254790c1baaac94ee2c68349642d21e16bf89c70a13019516ed475104c945cb3d53"
                    ],
                    "public_key": ""
                },
            ]
        }
    )

    assert await list_driver("5YJ3E1EA4KF555555", mock_context) == {
        "drivers":[
            {
                "name": "Jane Doe",
                "user_id": "1234567"
            }
        ]
    }

@pytest.mark.asyncio
async def test_delete_driver_success(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="DELETE",
        status_code=200,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/drivers?share_user_id=user_123",
        json={
            "response": "ok"
        },
    )

    assert await delete_driver("5YJ3E1EA4KF555555", "user_123", mock_context) == {"success": True}

@pytest.mark.asyncio
async def test_delete_driver_failed_response(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="DELETE", 
        status_code=200,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/drivers?share_user_id=user_123",
        json={
            "response": "error"
        },
    )

    assert await delete_driver("5YJ3E1EA4KF555555", "user_123", mock_context) == {
        "success": False
    }

@pytest.mark.asyncio
async def test_delete_driver_bad_request(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="DELETE",
        status_code=404,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/drivers?share_user_id=invalid_user",
        json={
            "error": "User not found"
        },
    )

    with pytest.raises(Exception):
        await delete_driver("5YJ3E1EA4KF555555", "invalid_user", mock_context)

@pytest.mark.asyncio
async def test_delete_driver_server_error(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="DELETE",
        status_code=500,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/drivers?share_user_id=user_123",
        json={
            "error": "Internal server error"
        },
    )

    with pytest.raises(Exception):
        await delete_driver("5YJ3E1EA4KF555555", "user_123", mock_context)
