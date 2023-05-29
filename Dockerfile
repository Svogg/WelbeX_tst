FROM python:3.11.1

WORKDIR /fastapi_geopy

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . ./

EXPOSE 8000





