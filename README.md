## Find nearest truck service

This is a simple project that can show a list of trucks nearest to a cargo.

If you wanna try it, just clone this repo :)

```commandline
git clone https://github.com/Svogg/fastapi_geopy.git
```
#### 1)  Make .env file named ".dbenv" before starting docker-compose
```commandline
touch .dbenv
```
```
DB_DRIVER=postgresql
DB_CONNECTOR=asyncpg
DB_USER=postgres
DB_PASS=test
DB_HOST=database
DB_PORT=5432
DB_NAME=test

CELERY_DB_CONNECTOR=psycopg2
```
#### 2) Run docker-compose
```commandline
docker-compose up --build
```

#### 3) Open your browser at: 
```commandline
http://localhost:8000/docs
```

