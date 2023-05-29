FROM python:3.11.1

WORKDIR /WelbeX_tst

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . ./

RUN alembic --autogenerate -m "initial"

RUN python -m db_fill.py

EXPOSE 8000





