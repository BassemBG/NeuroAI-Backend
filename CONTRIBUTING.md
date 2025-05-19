# 🤝 Contributing Guide

Welcome! If you're adding a new microservice or improving an existing one, follow these simple rules so everything works smoothly.

---

## 📁 1. Project Structure

- All microservices live inside the `microservices/` folder.
- Create your own folder with a meaningful name (e.g. `facial_emotion`, `eeg_emotion`, etc.).
- Inside your folder, include at least:
  - `app.py` or your Flask entry point
  - `requirements.txt`
  - `Dockerfile`

Optional folders you might need:
- `models/` → for ML/DL models
- `routes/` → Flask route logic
- `tests/` → unit or integration tests

---

## 🐳 2. Docker Setup

Each microservice must have a `Dockerfile`. Example:

```Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
```

Update requirements.txt before building:

```bash
pip freeze > requirements.txt
```

---

## 🧩 3. Add to docker-compose.yml

After adding your service, register it in docker-compose.yml like this:

```yaml
services:
  your_service_name:
    build:
      context: ./microservices/your_service_name
    container_name: your_service_name
    ports:
      - "5002:5000"  # Choose a unique host port
    volumes:
      - ./microservices/your_service_name:/app
```

```yaml
services:
  gateway:
    depends_on:
      # Other containers here 
      - service_a_container
```

---

## 🚪 4. Connect Your Service to the Gateway

In the gateway/ project, register your route. Example:

```python
@app.route("/predict/your-service", methods=["GET"])
def predict():
    response = requests.get("http://your_service_name:5000/predict")
    return jsonify(response.json())
```

`http://service_a_container:5000/`  
Format: `http://<container_name>:<internal_port>/`


---

## 🧪 5. Test Before Pushing

Make sure your microservice runs without errors:

```bash
docker-compose up --build
```

Check your endpoint via the gateway to ensure it's properly connected.

---

## 🧹 6. Clean Code Rules

- Keep code readable and well-commented.
- Separate logic into files/folders when needed.
- Use `.env` files if you need environment variables.

### 🧪 Local Development Tip

You can test locally using virtualenv:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

✅ Before building Docker, always update requirements.txt:

```bash
pip freeze > requirements.txt
```

---


---

✅ Ready to Go

Once your service works and is connected:

- Push your changes
- Open a Pull Request (PR)
- Mention what you added in the PR description

Thanks for contributing! 🎉