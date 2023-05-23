from sqlalchemy import insert

from search_nearest_trucks.schemas import LocationSchema
from src.database import get_async_session

import asyncio
import csv


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


async def run_stmt():
    async for session in get_async_session():
        await fill_location_table(LocationSchema, session)


asyncio.run(run_stmt())
