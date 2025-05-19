from flask import Flask
from routes.brain2text_routes import brain_to_text_blueprint

app = Flask(__name__)
app.register_blueprint(brain_to_text_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)
