from typing import Optional, NamedTuple, Dict, List, Union, Any

from pydantic import BaseModel
from sqlalchemy import DECIMAL


class LocationModel(BaseModel):
    id: int
    state: str
    city: str
    zip_code: str
    lat: float
    lng: float

    class Config:
        orm_mode = True


class CargoModel(BaseModel):
    pic_up_location: Optional[str]
    delivery_location: Optional[str]
    weight: Optional[int]
    description: Optional[str]

    class Config:
        orm_mode = True


class TruckModel(BaseModel):
    id: int
    unique_num: int
    current_location: int
    load_capacity: str

    class Config:
        orm_mode = True


class NearByTrucks(BaseModel):
    cargo_id: str
    pic_up_location: str
    delivery_location: str
    nearby_trucks: int
    weight: int
    description: str


class TruckInfo(BaseModel):
    truck_id: int
    trucks_distance: float
    unique_num: str


class AllTrucks(BaseModel):
    cargo_id: str
    pic_up_location: str
    delivery_location: str
    weight: int
    description: str
    truck_info: List[TruckInfo]
