from flask import Flask
from routes.facial_routes import facial_bp

app = Flask(__name__)
app.register_blueprint(facial_bp, url_prefix='/api/facial')  # ✅ this is critical

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001) 