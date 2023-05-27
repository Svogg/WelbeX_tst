from time import time

from sqlalchemy import insert, select, func

from search_nearest_trucks.schemas import LocationSchema, TruckSchema
from database import get_async_session

import asyncio
import csv
import random
import string


async def fill_location_table(location: LocationSchema, session: get_async_session):
    with open('../uszips.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            stmt = insert(location).values(
                id=i,
                state=row['state_name'],
                city=row['city'],
                zip_code=row['zip'],
                lat=row['lat'],
                lng=row['lng']
            )
            await session.execute(stmt)
        await session.commit()


async def fill_truck_table(truck: TruckSchema, session: get_async_session):
    for i in range(20):
        query = select(func.count("*")).select_from(LocationSchema)
        count = await session.execute(query)
        stmt = insert(truck).values(
            id=i,
            unique_num=str(random.randint(1000, 10000)) + random.choice(string.ascii_uppercase),
            current_location=random.randint(0, int(count.scalars().all()[0]) + 1),
            load_capacity=random.randint(0, 1001)
        )
        await session.execute(stmt)
    await session.commit()


async def run_stmt():
    async for session in get_async_session():
        await fill_location_table(LocationSchema, session)
        await fill_truck_table(TruckSchema, session)


start = time()
asyncio.run(run_stmt())
print(time() - start)
