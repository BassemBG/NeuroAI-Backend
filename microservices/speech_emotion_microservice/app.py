from flask import Flask
from routes.speech_routes import speech_bp

app = Flask(__name__)

# Register the speech blueprint
app.register_blueprint(speech_bp, url_prefix='/api/speech')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
