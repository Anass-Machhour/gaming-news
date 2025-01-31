from flask import Blueprint, jsonify
from sqlalchemy.orm import joinedload
import subprocess
from .database import SessionLocal
from .models import Website


main = Blueprint("main", __name__)


@main.route("/api/initialize", methods=["POST"])
def initialize():
    subprocess.run(["python", "-m", "app.init_db"], check=True)
    return jsonify({"message": "Database initialized."}), 200


@main.route("/api/scrape", methods=["POST"])
def scrape():
    subprocess.run(["python", "-m", "app.scraper"], check=True)
    return jsonify({"message": "Scrapping completed successfully."}), 200


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

    response = []
    for website in websites:
        website_data = {
            "id": website.id,
            "name": website.name,
            "url": website.url,
            "favicon_url": website.favicon_url,
            "created_at": website.created_at.isoformat(),
            "articles": [],
        }

        for article in website.articles:
            article_data = {
                "id": article.id,
                "url": article.url,
                "headline": article.headline,
                "thumbnail_url": article.thumbnail_url,
                "website_id": article.website_id,
                "created_at": article.created_at.isoformat(),
            }
            website_data["articles"].append(article_data)

        response.append(website_data)

    return jsonify(response)


@main.route("/")
def home():
    return "<h1>running</h1>"
