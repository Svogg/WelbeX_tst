from pydantic import BaseModel


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
    id: int
    pic_up_lat: float
    pic_up_lng: float
    delivery_lat: float
    delivery_lng: float
    weight: int
    description: str

    class Config:
        orm_mode = True


class TruckModel(BaseModel):
    id: int
    unique_num: int
    current_lat: float
    current_lng: float
    load_capacity: str

    class Config:
        orm_mode = True
