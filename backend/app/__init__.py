# Initialize the Flask app
from flask import Flask
from flask_cors import CORS
import logging


def create_app():
    app = Flask(__name__)
    CORS(app, origins=["https://gaming-news-opal.vercel.app", "http://localhost:3000"])

    from .routes import main
    app.register_blueprint(main)

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    return app