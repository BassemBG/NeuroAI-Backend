FROM python:3.10-slim

RUN pip install --upgrade pip setuptools wheel

RUN apt-get update && apt-get install -y build-essential gcc gfortran libatlas-base-dev

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]