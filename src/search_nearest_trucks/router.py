from typing import List, Optional

from fastapi import APIRouter, Depends
from geopy import distance
from sqlalchemy import insert, exc, update, delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from database import get_async_session
from search_nearest_trucks.logic import get_postal_location
from search_nearest_trucks.models import NearByTrucks, AllTrucks
from search_nearest_trucks.schemas import CargoSchema, LocationSchema, TruckSchema

router = APIRouter()


@router.post('/cargo')
async def add_cargo(
        pic_up_zip: str,
        delivery_zip: str,
        weight: int,
        description: str,
        session: AsyncSession = Depends(get_async_session)
):
    pic_up_state = await get_postal_location(pic_up_zip)
    delivery_state = await get_postal_location(delivery_zip)

    stmt = insert(CargoSchema).values(
        pic_up_location=select(LocationSchema.id).filter_by(
            state=pic_up_state,
            zip_code=pic_up_zip
        ).as_scalar(),
        delivery_location=select(LocationSchema.id).filter_by(
            state=delivery_state,
            zip_code=delivery_zip
        ).as_scalar(),
        weight=weight,
        description=description
    )
    try:
        await session.execute(stmt)
    except exc.IntegrityError:
        await session.rollback()
        return {
            'status': 'error'
        }
    await session.commit()

    return {
        'status': 'success'
    }


@router.get('/cargos', response_model=List[NearByTrucks])
async def all_cargos(session: AsyncSession = Depends(get_async_session)):
    a = aliased(CargoSchema)
    b = aliased(TruckSchema)
    c = aliased(LocationSchema)

    cargo_query = select(
        a.id, a.pic_up_location, a.delivery_location,
        c.lat, c.lng, a.weight, a.description
    ).join(c, a.pic_up_location == c.id, isouter=True)

    truck_query = select(
        b.id, c.lat, c.lng,
        b.unique_num, b.load_capacity
    ).join(c, b.current_location == c.id, isouter=True)

    cargo_results = await session.execute(cargo_query)
    trucks_results = await session.execute(truck_query)

    cargos = [cargo for cargo in cargo_results.all()]
    trucks = [truck for truck in trucks_results.all()]

    cargo_lst = []
    for cargo in cargos:
        counter = 0
        for truck in trucks:
            if distance.distance(cargo[3:5], truck[1:3]).miles <= 450:
                counter += 1
        cargo_lst.append(NearByTrucks(
            cargo_id=cargo[0],
            pic_up_location=cargo[1],
            delivery_location=cargo[2],
            nearby_trucks=counter,
            weight=cargo[5],
            description=cargo[6]
        ))
    return cargo_lst


@router.get('/cargos/{id}')
async def get_cargo(
        cargo_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    a = aliased(CargoSchema)
    b = aliased(TruckSchema)
    c = aliased(LocationSchema)

    cargo_query = select(
        a.id, a.pic_up_location, a.delivery_location,
        c.lat, c.lng, a.weight, a.description
    ).join(c, a.pic_up_location == c.id, isouter=True).filter(a.id == cargo_id)

    truck_query = select(
        b.id, c.lat, c.lng,
        b.unique_num, b.load_capacity
    ).join(c, b.current_location == c.id)

    cargo_results = await session.execute(cargo_query)
    trucks_results = await session.execute(truck_query)

    cargos = [cargo for cargo in cargo_results.all()]
    trucks = [truck for truck in trucks_results.all()]
    cargo_lst = []
    for i, cargo in enumerate(cargos):
        cargo_lst.append(AllTrucks(
            cargo_id=cargo[0],
            pic_up_location=cargo[1],
            delivery_location=cargo[2],
            weight=cargo[5],
            description=cargo[6],
            truck_info=[{
                'truck_id': i[0],
                'trucks_distance': distance.distance(cargo[3:5], [truck for truck in i][1:3]).miles,
                'unique_num': [truck for truck in i][3]
            } for i in trucks]
        ))

    return cargo_lst


@router.put('/trucks/{id}')
async def change_truck(
        truck_id: int,
        zip_code: str,
        unique_num: str,
        load_capacity: int,
        session: AsyncSession = Depends(get_async_session)
):
    current_location = await get_postal_location(zip_code)
    stmt = update(TruckSchema).values(
        unique_num=unique_num,
        current_location=select(LocationSchema.id).filter_by(city=current_location).scalar_subquery(),
        load_capacity=load_capacity
    ).filter_by(id=truck_id)
    try:
        await session.execute(stmt)
    except Exception:
        await session.rollback()
        return {
            'code': 422,
            'status': 'error'
        }
    await session.commit()


@router.patch('/cargos/{id}')
async def patch_cargo(
        id: int,
        weight: int,
        description: str,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = update(CargoSchema).values(
        weight=weight,
        description=description
    ).filter_by(id=id)

    await session.execute(stmt)
    await session.commit()


@router.delete('/cargos/{id}')
async def del_cargo(
        id: int,
        session: AsyncSession = Depends(get_async_session)
):
    query = delete(CargoSchema).filter_by(id=id)
    await session.execute(query)
    await session.commit()


@router.get('/cargos_filtered/')
async def filter_cargos(
        id: Optional[int] = None,
        weight: Optional[int] = None,
        trucks_distance: Optional[float] = None,
        session: AsyncSession = Depends(get_async_session)
):
    a = aliased(CargoSchema)
    b = aliased(TruckSchema)
    c = aliased(LocationSchema)
    if id is not None:
        cargo_query = select(
            a.id, a.pic_up_location, a.delivery_location,
            c.lat, c.lng, a.weight, a.description
        ).join(c, a.pic_up_location == c.id, isouter=True).filter(a.id == id)
    else:
        cargo_query = select(
            a.id, a.pic_up_location, a.delivery_location,
            c.lat, c.lng, a.weight, a.description
        ).join(c, a.pic_up_location == c.id, isouter=True)

    truck_query = select(
        b.id, c.lat, c.lng,
        b.unique_num, b.load_capacity
    ).join(c, b.current_location == c.id)

    cargo_results = await session.execute(cargo_query)
    trucks_results = await session.execute(truck_query)

    cargos = [cargo for cargo in cargo_results.all()]
    trucks = [truck for truck in trucks_results.all()]

    # id
    if id is not None and weight is None and trucks_distance is None:
        cargo_lst = []
        for cargo in cargos:
            if cargo[0] == id:
                cargo_lst.append(dict(
                    cargo_id=cargo[0],
                    pic_up_location=cargo[1],
                    delivery_location=cargo[2],
                    weight=cargo[5],
                    description=cargo[6],
                    truck_info=[{
                        'truck_id': i[0],
                        'trucks_distance': distance.distance(cargo[3:5], [truck for truck in i][1:3]).miles,
                        'unique_num': [truck for truck in i][3]
                    } for i in trucks]
                ))
        return cargo_lst
    # id weight
    elif id is not None and weight is not None and trucks_distance is None:
        cargo_lst = []
        for cargo in cargos:
            if cargo[0] == id and cargo[5] == weight:
                cargo_lst.append(dict(
                    cargo_id=cargo[0],
                    pic_up_location=cargo[1],
                    delivery_location=cargo[2],
                    weight=cargo[5],
                    description=cargo[6],
                    truck_info=[{
                        'truck_id': i[0],
                        'trucks_distance': distance.distance(cargo[3:5], [truck for truck in i][1:3]).miles,
                        'unique_num': [truck for truck in i][3]
                    } for i in trucks]
                ))
        return cargo_lst
    # id trucks_distance
    elif id is not None and weight is None and trucks_distance is not None:
        cargo_lst = []
        for i, cargo in enumerate(cargos):
            if cargo[0] == id:
                for truck in trucks:
                    if distance.distance(cargo[3:5], truck[1:3]).miles == trucks_distance:
                        cargo_lst.append(dict(
                            cargo_id=cargo[0],
                            pic_up_location=cargo[1],
                            delivery_location=cargo[2],
                            weight=cargo[5],
                            description=cargo[6],
                            truck_info=[{
                                'truck_id': truck[0],
                                'trucks_distance': distance.distance(cargo[3:5], [j for j in truck][1:3]).miles,
                                'unique_num': [j for j in truck][3]
                            }]
                        ))
        return cargo_lst
    # weight trucks_distance
    elif id is None and weight is not None and trucks_distance is not None:
        cargo_lst = []
        for i, cargo in enumerate(cargos):
            if cargo[5] == weight:
                for truck in trucks:
                    if distance.distance(cargo[3:5], truck[1:3]).miles == trucks_distance:
                        cargo_lst.append(dict(
                            cargo_id=cargo[0],
                            pic_up_location=cargo[1],
                            delivery_location=cargo[2],
                            weight=cargo[5],
                            description=cargo[6],
                            truck_info=[{
                                'truck_id': truck[0],
                                'trucks_distance': distance.distance(cargo[3:5], [j for j in truck][1:3]).miles,
                                'unique_num': [j for j in truck][3]
                            }]
                        ))
        return cargo_lst
    # weight
    elif id is None and weight is not None and trucks_distance is None:
        cargo_lst = []
        for cargo in cargos:
            if cargo[5] == weight:
                cargo_lst.append(dict(
                    cargo_id=cargo[0],
                    pic_up_location=cargo[1],
                    delivery_location=cargo[2],
                    weight=cargo[5],
                    description=cargo[6],
                    truck_info=[{
                        'truck_id': i[0],
                        'trucks_distance': distance.distance(cargo[3:5], [truck for truck in i][1:3]).miles,
                        'unique_num': [truck for truck in i][3]
                    } for i in trucks]
                ))
        return cargo_lst
    # trucks_distance
    elif id is None and weight is None and trucks_distance is not None:
        cargo_lst = []
        for i, cargo in enumerate(cargos):
            for truck in trucks:
                if distance.distance(cargo[3:5], truck[1:3]).miles == trucks_distance:
                    cargo_lst.append(dict(
                        cargo_id=cargo[0],
                        pic_up_location=cargo[1],
                        delivery_location=cargo[2],
                        weight=cargo[5],
                        description=cargo[6],
                        truck_info=[{
                            'truck_id': truck[0],
                            'trucks_distance': distance.distance(cargo[3:5], [j for j in truck][1:3]).miles,
                            'unique_num': [j for j in truck][3]
                        }]
                    ))
        return cargo_lst
