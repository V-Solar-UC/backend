from typing import Optional

from pydantic import BaseModel


# Shared properties
class SponsorBase(BaseModel):
    name: Optional[str] = None
    logo_path: Optional[str] = None


# Properties to receive via API on creation
class SponsorCreate(SponsorBase):
    # TODO: file upload
    name: str
    logo_path: str


class SponsorUpdate(SponsorBase):
    # later when there's an update route
    pass


class SponsorInDBBase(SponsorBase):
    id: int
    name: str
    logo_path: str

    class Config:
        orm_mode = True


# Properties to return via API
class Sponsor(SponsorInDBBase):
    pass
