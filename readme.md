# 🧠 Emotion Recognition Platform — Microservices Architecture

This project uses a **microservice architecture** to build an emotion recognition system with different independent services.

Each microservice handles a specific use case, such as:

- 🎤 Speech Emotion Recognition  
- 👤 Facial Emotion Recognition  
- 🧠 EEG Emotion Recognition  
- ❤️ ECG Emotion Recognition

---

## 🧱 Project Structure

root/
│
├── microservices/
│   ├── microservice_a/ # One use case (e.g. speech)
│   ├── microservice_b/ # Another use case (e.g. facial)
│   └── ...
│
├── gateway/ # API gateway (user entry point)
├── docker-compose.yml # Runs all microservices together
└── README.md

---

## ⚙️ How It Works

- Each team member creates their **own Flask project** inside `microservices/`.
- Each microservice has:
  - Its own `Dockerfile`
  - Its own `requirements.txt`
  - Its own `app.py`
  - Optionally:  
    - `models/` → for ML/DL models  
    - `routes/` → for Flask routes  
    - `tests/` → for unit or integration tests  

- All services are run together using `docker-compose.yml`.

- The **gateway** is a single entry point. It receives user requests and **redirects them to the right microservice** based on the endpoint path.

---

## 🚀 Quick Start

1. Clone the repo.
2. Create your microservice inside `microservices/your_service_name/`.
3. Build and run all services:

```bash
docker-compose up --build
```

Use the API Gateway to make requests. For example:

### 🔄 Routing Example in the Gateway

Here’s how to expose a new microservice in the gateway:

```python
@app.route("/predict/service-a", methods=["GET"])
def predict_service_a():
    print("Received request for Service A")
    response = requests.get("http://service_a_container:5000/predict")
    return jsonify(response.json())
```

`http://service_a_container:5000/`  
Format: `http://<container_name>:<internal_port>/`

### 📦 docker-compose.yml Snippet

Here’s how to add a new microservice to docker-compose.yml:

```yaml
services:
  service_a_container:
    build:
      context: ./microservices/service_a
    container_name: service_a_container
    ports:
      - "5001:5000"  # Format: <host_port>:<container_port>
    volumes:
      - ./microservices/service_a:/app
```

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

## 🤝 Want to Contribute?

Check out `CONTRIBUTING.md` for guidelines.
