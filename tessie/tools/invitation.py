import httpx
from typing import Annotated, Dict, List

from arcade_tdk import ToolContext, tool
from tessie import utils

from ..tessie_client import TessieClient
from arcade_tdk.errors import ToolExecutionError


@tool(requires_secrets=["TESSIE_TOKEN"])
async def list_invitation(vin: Annotated[str, "The VIN of the car for which the invite should be created."],
                    context: ToolContext) -> dict[str, list[dict[str, str]]]:
    """Returns a list of invitations for a car with the given VIN."""
    utils.validate_vin(vin)
    client =  TessieClient(context.get_secret("TESSIE_TOKEN"))

    try:
        invitations = await client.list_invitations(vin)
        return invitations.model_dump()
    except httpx.HTTPError as exc:
        raise ToolExecutionError(
            message=f"Failed to list invitations for VIN {vin}",
            developer_message=(
                f"Error occurred while listing invitations for VIN {vin}: {exc}"
            )
        )


@tool(requires_secrets=["TESSIE_TOKEN"])
async def create_invitation(vin: Annotated[str, "The VIN of the car for which the invite should be created."],
                      context: ToolContext) -> dict[str, str]:
    """Returns an invitation message for a car with the given VIN."""
    utils.validate_vin(vin)
    client = TessieClient(context.get_secret("TESSIE_TOKEN"))

    try:
        invitation = await client.create_invitation(vin)
        return invitation.model_dump()
    except httpx.HTTPError as exc:
        raise ToolExecutionError(
            message=f"Failed to create invite for VIN {vin}",
            developer_message=(
                f"Error occurred while creating invite for VIN {vin}: {exc}"
            )
        )

@tool(requires_secrets=["TESSIE_TOKEN"])
async def revoke_invitation(vin: Annotated[str, "The VIN of the car for which the invite should be revoked."],
                      invite_id: Annotated[str, "Previously generated invite ID."],
                      context: ToolContext) -> dict[str, bool]:
    """Revokes the invite for a car with the given VIN."""
    utils.validate_vin(vin)
    client = TessieClient(context.get_secret("TESSIE_TOKEN"))

    try:
        result = await client.revoke_invitation(vin, invite_id)
        return result.model_dump()
    except httpx.HTTPError as exc:
        raise ToolExecutionError(
            message=f"Failed to revoking invite for VIN {vin}",
            developer_message=(
                f"Error occurred while revoking invite for VIN {vin}: {exc}"
            )
        )