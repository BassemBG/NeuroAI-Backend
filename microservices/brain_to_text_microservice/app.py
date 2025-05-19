from flask import Flask
from routes.brain2text_routes import brain_to_text_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(brain_to_text_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
