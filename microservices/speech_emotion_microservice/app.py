from flask import Flask
from routes.speech_routes import speech_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Register the speech blueprint
app.register_blueprint(speech_bp, url_prefix='/api/speech')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=False)
