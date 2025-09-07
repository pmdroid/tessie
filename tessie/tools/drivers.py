import httpx
from typing import Annotated

from arcade_tdk import ToolContext, tool
from tessie import utils

from ..tessie_client import TessieClient
from arcade_tdk.errors import ToolExecutionError


@tool(requires_secrets=["TESSIE_TOKEN"])
async def list_driver(vin: Annotated[str, "The VIN of the car for which the drivers should be retrieved."],
                      context: ToolContext) -> dict[str, list[dict[str, str]]]:
    """Returns a list of drivers for a car with the given VIN."""
    utils.validate_vin(vin)
    client = TessieClient(context.get_secret("TESSIE_TOKEN"))

    try:
        drivers = await client.list_driver(vin)
        return drivers.model_dump()
    except httpx.HTTPError as exc:
        raise ToolExecutionError(
            message=f"Failed to list drivers for VIN {vin}",
            developer_message=(
                f"Error occurred while listing drivers for VIN {vin}: {exc}"
            )
        )

@tool(requires_secrets=["TESSIE_TOKEN"])
async def delete_driver(vin: Annotated[str, "VIN of the car for which the driver should be removed."],
                user_id: Annotated[str, "User ID."],
                context: ToolContext) -> dict[str, bool]:
    """Removes a driver's access to a Tesla vehicle by removing access to the car."""
    utils.validate_vin(vin)
    client = TessieClient(context.get_secret("TESSIE_TOKEN"))

    try:
        result = await client.delete_driver(vin, user_id)
        return result.model_dump()
    except httpx.HTTPError as exc:
        raise ToolExecutionError(
            message=f"Failed to delete driver for VIN {vin}",
            developer_message=(
                f"Error occurred while deleting driver for VIN {vin}: {exc}"
            )
        )