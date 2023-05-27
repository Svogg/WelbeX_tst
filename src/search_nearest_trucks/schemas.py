from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import Mapped

from database import Base


class _Abstract(object):
    id: Mapped[Optional[str]] = Column(Integer, primary_key=True, index=True, autoincrement=True)


class LocationSchema(_Abstract, Base):
    __tablename__ = 'location'
    state = Column(String, nullable=False)
    city = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    lat = Column(DECIMAL, nullable=False)
    lng = Column(DECIMAL, nullable=False)


class CargoSchema(_Abstract, Base):
    __tablename__ = 'cargo'
    pic_up_location = Column(Integer, ForeignKey('location.id'), nullable=False)
    delivery_location = Column(Integer, ForeignKey('location.id'), nullable=False)
    weight = Column(Integer, nullable=False)
    description = Column(String, nullable=False)


class TruckSchema(_Abstract, Base):
    __tablename__ = 'truck'
    unique_num = Column(String, nullable=False, unique=True)
    current_location = Column(Integer, ForeignKey('location.id'), nullable=False)
    load_capacity = Column(Integer, nullable=False)
