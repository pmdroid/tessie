import pytest
from pytest_httpx import HTTPXMock

from arcade_tdk import ToolContext, ToolSecretItem

from tessie.tools.car import get_location, get_battery

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
async def test_get_location_success(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="GET",
        status_code=200,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/vehicle_data?endpoints=drive_state",
        json={
            "response": {
                "drive_state": {
                    "latitude": 37.4929681,
                    "longitude": -121.9453489,
                }
            }
        },
    )

    assert await get_location("5YJ3E1EA4KF555555", mock_context) == {
        "latitude": "37.492968100",
        "longitude": "-121.945348900",
    }

@pytest.mark.asyncio
async def test_get_location_bad_request(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="GET",
        status_code=500,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/vehicle_data?endpoints=drive_state",
        json={
            "error": "Internal server error"
        },
    )

    with pytest.raises(Exception):
        await get_location("5YJ3E1EA4KF555555", mock_context)

@pytest.mark.asyncio
async def test_get_battery_success(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="GET",
        status_code=200,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/vehicle_data?endpoints=charge_state",
        json={
            "response": {
                "charge_state": {
                    "battery_level": "85",
                    "battery_range": "275"
                },
            }
        },
    )

    assert await get_battery("5YJ3E1EA4KF555555", mock_context) == {
        "battery_level": "85",
        "battery_range": "275"
    }

@pytest.mark.asyncio
async def test_get_battery_bad_request(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="GET",
        status_code=404,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/vehicle_data?endpoints=charge_state",
        json={
            "error": "Car not found"
        },
    )

    with pytest.raises(Exception):
        await get_battery("5YJ3E1EA4KF555555", mock_context)
