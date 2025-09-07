import httpx
from typing import Annotated

from arcade_tdk import ToolContext, tool
from tessie import utils

from ..tessie_client import TessieClient
from arcade_tdk.errors import ToolExecutionError


@tool(requires_secrets=["TESSIE_TOKEN"])
async def get_location(vin: Annotated[str, "The VIN of the car for which the invite should be revoked."],
                      context: ToolContext) -> dict[str, str]:
    """Returns the current location of the car with the given VIN."""
    utils.validate_vin(vin)
    client = TessieClient(context.get_secret("TESSIE_TOKEN"))

    try:
        location = await client.get_location(vin)
        return location.model_dump()
    except httpx.HTTPError as exc:
        raise ToolExecutionError(
            message=f"Failed to get location for VIN {vin}",
            developer_message=(
                f"Error occurred while getting location for VIN {vin}: {exc}"
            )
        )

@tool(requires_secrets=["TESSIE_TOKEN"])
async def get_battery(vin: Annotated[str, "The VIN of the car for which the invite should be revoked."],
                context: ToolContext) -> dict[str, str]:
    """Returns the battery level of the car with the given VIN."""
    utils.validate_vin(vin)
    client = TessieClient(context.get_secret("TESSIE_TOKEN"))

    try:
        battery = await client.get_battery_level(vin)
        return battery.model_dump()
    except httpx.HTTPError as exc:
        raise ToolExecutionError(
            message=f"Failed to get battery level for VIN {vin}",
            developer_message=(
                f"Error occurred while getting battery level for VIN {vin}: {exc}"
            )
        )