from flask import Blueprint, jsonify
from sqlalchemy.orm import joinedload
import subprocess
from .database import SessionLocal
from .models import Website
from .tasks import scrape_website_task
from .serializer import WebsiteSchema


main = Blueprint("main", __name__)


@main.route("/api/initialize", methods=["POST"])
def initialize():
    subprocess.run(["python", "-m", "app.init_db"], check=True)
    return jsonify({"message": "Database initialized."}), 200


@main.route("/api/scrape", methods=["POST"])
def scrape():
    scrape_website_task.delay()
    return jsonify({"message": "Scrapping started."}), 200


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@main.route("/api/websites", methods=["GET"])
def get_articles():
    db = next(get_db())
    websites = db.query(Website).options(joinedload(Website.articles)).all()
    
    schema = WebsiteSchema(many=True)
    results = schema.dump(websites)

    return jsonify(results)


@main.route("/")
def home():
    return "<h1>running</h1>"
