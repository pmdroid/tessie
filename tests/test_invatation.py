import pytest
from pytest_httpx import HTTPXMock

from arcade_tdk import ToolContext, ToolSecretItem

from tessie.tools.invitation import list_invitation, create_invitation, revoke_invitation

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
async def test_list_invitation_empty_list(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="GET",
        status_code=200,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/invitations",
        json={
            "response": []
        },
    )

    assert await list_invitation("5YJ3E1EA4KF555555", mock_context) == {"invitations": []}

@pytest.mark.asyncio
async def test_list_invitation_with_invitations(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="GET",
        status_code=200,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/invitations",
        json={
            "response": [
                {
                    "id": 2252266471835261,
                    "owner_id": 1311857,
                    "share_user_id": None,
                    "product_id": "7SAXCBE6XPF123456",
                    "state": "pending",
                    "code": "d9SZ0FG_CuVqQ7OoVx1_e5-UOGLt83MqxT7BY8DsaeCs",
                    "expires_at": "2023-11-29T00:55:31.000Z",
                    "revoked_at": None,
                    "borrowing_device_id": None,
                    "key_id": None,
                    "product_type": "vehicle",
                    "share_type": "customer",
                    "active_pubkeys": [
                        None
                    ],
                    "id_s": "2252266471835261",
                    "owner_id_s": "1311857",
                    "share_user_id_s": "2311857",
                    "borrowing_key_hash": None,
                    "vin": "5YJ3E1EA4KF555555",
                    "share_link": "https://www.tesla.com/_rs/1/d9SZ0FG_CuVqQ7OoVx1_e5-UOGLt83MqxT7BY8DsaeCs"
                },
            ]
        },
    )

    assert await list_invitation("5YJ3E1EA4KF555555", mock_context) == {
        "invitations": [
            {
                "id": "2252266471835261",
                "share_link": "https://www.tesla.com/_rs/1/d9SZ0FG_CuVqQ7OoVx1_e5-UOGLt83MqxT7BY8DsaeCs",
                "state": "pending"
            }
        ]
    }

@pytest.mark.asyncio
async def test_list_invitation_bad_request(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="GET",
        status_code=403,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/invitations",
        json={
            "error": "Forbidden"
        },
    )

    with pytest.raises(Exception):
        await list_invitation("5YJ3E1EA4KF555555", mock_context)

@pytest.mark.asyncio
async def test_create_invitation_success(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="POST",
        status_code=200,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/invitations",
        json={
            "response": {
                "id_s": "429509621657",
                "state": "pending",
                "share_link": "https://tessie.com/share/new_inv_123"
            }
        },
    )

    assert await create_invitation("5YJ3E1EA4KF555555", mock_context) == {
        "id": "429509621657",
        "state": "pending",
        "share_link": "https://tessie.com/share/new_inv_123"
    }

@pytest.mark.asyncio
async def test_create_invitation_bad_request(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="POST",
        status_code=400,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/invitations",
        json={
            "error": "Bad request"
        },
    )

    with pytest.raises(Exception):
        await create_invitation("5YJ3E1EA4KF555555", mock_context)

@pytest.mark.asyncio
async def test_revoke_invitation_success(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="POST",
        status_code=200,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/invitations/inv_123/revoke",
        json={
            "response": "true"
        },
    )

    assert await revoke_invitation("5YJ3E1EA4KF555555", "inv_123", mock_context) == {
        "success": True
    }

@pytest.mark.asyncio
async def test_revoke_invitation_failed_revocation(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="POST",
        status_code=200,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/invitations/inv_123/revoke",
        json={
            "response": "false"
        },
    )

    assert await revoke_invitation("5YJ3E1EA4KF555555", "inv_123", mock_context) == {"success": False}

@pytest.mark.asyncio
async def test_revoke_invitation_bad_request(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="POST",
        status_code=404,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/invitations/invalid_id/revoke",
        json={
            "error": "Invitation not found"
        },
    )

    with pytest.raises(Exception):
        await revoke_invitation("5YJ3E1EA4KF555555", "invalid_id", mock_context)

@pytest.mark.asyncio
async def test_revoke_invitation_server_error(httpx_mock: HTTPXMock, mock_context: ToolContext) -> None:
    httpx_mock.add_response(
        method="POST",
        status_code=500,
        url="https://api.tessie.com/api/1/vehicles/5YJ3E1EA4KF555555/invitations/inv_123/revoke",
        json={
            "error": "Internal server error"
        },
    )

    with pytest.raises(Exception):
        await revoke_invitation("5YJ3E1EA4KF555555", "inv_123", mock_context)