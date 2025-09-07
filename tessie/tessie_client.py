import httpx

from typing import Optional
from tessie.model import InvitationList, Invitation, DriverList, Driver, Location, Battery, ActionResult


class TessieClient:
    _api_token: str

    def __init__(self, api_token: str) -> None:
        self._api_token = api_token

    async def do_request(self, method: str, url: str, payload: Optional[dict] = None) -> dict:
        headers = {"Authorization": f"Bearer {self._api_token}"}
        async with httpx.AsyncClient() as client:
            request = httpx.Request(method, url, headers=headers, json=payload)
            resp = await client.send(request)
            resp.raise_for_status()
            return resp.json()  # type: ignore[no-any-return]

    async def list_invitations(self, vin: str) -> InvitationList:
        url = f"https://api.tessie.com/api/1/vehicles/{vin}/invitations"
        data = await self.do_request("GET", url)
        return InvitationList(
            invitations=[
                Invitation(
                    id=invitation["id_s"],
                    share_link=invitation["share_link"],
                    state=invitation["state"]
                )
                for invitation in data["response"]
            ]
        )

    async def create_invitation(self, vin: str) -> Invitation:
        url = f"https://api.tessie.com/api/1/vehicles/{vin}/invitations"
        data = await self.do_request("POST", url)

        return Invitation(
            id=data["response"]["id_s"],
            share_link=data["response"]["share_link"],
            state=data["response"]["state"]
        )

    async def revoke_invitation(self, vin: str, invite_id: str) -> ActionResult:
        url = f"https://api.tessie.com/api/1/vehicles/{vin}/invitations/{invite_id}/revoke"
        data = await self.do_request("POST", url)
        return ActionResult(
            success=data["response"] == "true" or data["response"] == True
        )

    async def list_driver(self, vin: str) -> DriverList:
        url = f"https://api.tessie.com/api/1/vehicles/{vin}/drivers"
        data = await self.do_request("GET", url)
        return DriverList(
            drivers=[
                Driver(
                    user_id=driver["user_id_s"],
                    name=driver["driver_first_name"] + " " + driver["driver_last_name"]
                )
                for driver in data["response"]
            ]
        )

    async def delete_driver(self, vin: str, user_id: str) -> ActionResult:
        url = f"https://api.tessie.com/api/1/vehicles/{vin}/drivers?share_user_id={user_id}"
        data = await self.do_request("DELETE", url)
        return ActionResult(
            success=data["response"] == "ok"
        )

    async def get_location(self, vin: str) -> Location:
        url = f"https://api.tessie.com/api/1/vehicles/{vin}/vehicle_data?endpoints=drive_state"
        data = await self.do_request("GET", url)
        return Location(
            latitude=f'{data["response"]["drive_state"]["latitude"]:.9f}',
            longitude=f'{data["response"]["drive_state"]["longitude"]:.9f}'
        )

    async def get_battery_level(self, vin: str) -> Battery:
        url = f"https://api.tessie.com/api/1/vehicles/{vin}/vehicle_data?endpoints=charge_state"
        data = await self.do_request("GET", url)

        return Battery(
            battery_level=data["response"]["charge_state"]["battery_level"],
            battery_range=data["response"]["charge_state"]["battery_range"],
        )



