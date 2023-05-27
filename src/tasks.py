import random

from celery import Celery
from fastapi import Depends
from sqlalchemy import select, func, update
from sqlalchemy.orm import Session, sessionmaker

from database import celery_engine, Base
from search_nearest_trucks.schemas import TruckSchema, LocationSchema

celery = Celery(
    "tasks",
    broker='redis://localhost:6379'
)


def fill_truck_table(truck: TruckSchema, engine: celery_engine):
    with Session(engine) as session:
        stmt = select(truck.id)
        ids = session.execute(stmt)

        for i in [current_id for current_id in ids.scalars().all()]:
            query = select(func.count("*")).select_from(LocationSchema)
            count = session.execute(query)
            stmt = update(truck).values(
                current_location=random.randint(0, int(count.scalars().all()[0]) + 1),
            ).filter_by(id=i)
            session.execute(stmt)
        session.commit()


@celery.task
def run_task():
    fill_truck_table(TruckSchema, celery_engine)
    return 0


celery.conf.beat_schedule = {
    "run_update_task_every_1_minute": {
        "task": "tasks.run_task",
        "schedule": 180.0,

    }
}



