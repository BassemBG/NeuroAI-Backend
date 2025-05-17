FROM python:3.11.2-slim

# 2. Upgrade pip & friends so "Requires-Python" metadata is respected
RUN pip install --upgrade pip setuptools wheel


WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
