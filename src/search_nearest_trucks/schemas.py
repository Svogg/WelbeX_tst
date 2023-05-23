from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL

from src.database import Base, metadata, engine


class _Abstract(object):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    class Config:
        orm_mode = True


class LocationSchema(_Abstract, Base):
    __tablename__ = 'location'
    metadata = metadata
    state = Column(String, nullable=False)
    city = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    lat = Column(DECIMAL, nullable=False, unique=True)
    lng = Column(DECIMAL, nullable=False, unique=True)


class CargoSchema(_Abstract, Base):
    __tablename__ = 'cargo'
    pic_up_lat = Column(DECIMAL, ForeignKey('location.lat'), nullable=False)
    pic_up_lon = Column(DECIMAL, ForeignKey('location.lng'), nullable=False)
    delivery_lat = Column(DECIMAL, ForeignKey('location.lat'), nullable=False)
    delivery_lng = Column(DECIMAL, ForeignKey('location.lng'), nullable=False)
    weight = Column(Integer, nullable=False)
    description = Column(String, nullable=False)


class TruckSchema(_Abstract, Base):
    __tablename__ = 'truck'
    unique_num = Column(String, nullable=False)
    current_lat = Column(DECIMAL, ForeignKey('location.lat'), nullable=False)
    current_lng = Column(DECIMAL, ForeignKey('location.lng'), nullable=False)
    load_capacity = Column(Integer, nullable=False)



