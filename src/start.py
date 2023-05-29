from fastapi import FastAPI
from search_nearest_trucks.router import router

app = FastAPI(
    title='WelbeX_tst_service',
)

app.include_router(
    router,
    prefix='/router',
    tags=['router']
)
