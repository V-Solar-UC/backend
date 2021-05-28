from typing import Optional

from pydantic import BaseModel


# Shared properties
class DonorBase(BaseModel):
    name: Optional[str] = None
    logo_path: Optional[str] = None


# Properties to receive via API on creation
class DonorCreate(DonorBase):
    # TODO: file upload
    name: str


class DonorUpdate(DonorBase):
    # later when there's an update route
    pass


class DonorInDBBase(DonorBase):
    id: int
    name: str
    logo_path: str

    class Config:
        orm_mode = True


# Properties to return via API
class Donor(DonorInDBBase):
    pass
