import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-secret")
    app.config["DATABASE"] = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "incidents.db")

    from .routes import bp
    app.register_blueprint(bp)

    from .db import init_db
    init_db(app.config["DATABASE"])
    return app
