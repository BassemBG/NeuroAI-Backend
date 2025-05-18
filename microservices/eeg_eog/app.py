from flask import Flask
from routes.eeg_eog_routes import eeg_eog_bp  # Import the blueprint

app = Flask(__name__)
app.register_blueprint(eeg_eog_bp, url_prefix='/api/eeg-eog')  # Register with URL prefix

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
