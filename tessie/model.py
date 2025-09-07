from pydantic import BaseModel

class Driver(BaseModel):
    user_id: str
    name: str

class DriverList(BaseModel):
    drivers: list[Driver]

class Invitation(BaseModel):
    id: str
    share_link: str
    state: str

class InvitationList(BaseModel):
    invitations: list[Invitation]

class Location(BaseModel):
    latitude: str
    longitude: str

class Battery(BaseModel):
    battery_level: str
    battery_range: str

class ActionResult(BaseModel):
    success: bool