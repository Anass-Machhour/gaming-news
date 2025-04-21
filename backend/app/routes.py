import asyncio
from typing import List
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
import subprocess
from .database import SessionLocal
from .models import Website, Article
from .scraper import start_scrape
from .serializer import WebsiteSchema


main = Blueprint("main", __name__)


@main.route("/api/initialize", methods=["POST"])
def initialize():
    subprocess.run(["python", "-m", "app.init_db"], check=True)
    return jsonify({"message": "Database initialized."}), 200


@main.route("/api/scrape", methods=["POST"])
def scrape():
    asyncio.run(start_scrape())
    return jsonify({"message": "Scrapping started."}), 200


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@main.route("/api/news", methods=["GET"])
def get_news_per_page():
    db = next(get_db())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 32, type=int)
    start = (page - 1) * per_page

    total_articles = db.query(Article).count()

    total_pages = (total_articles + per_page - 1) // per_page

    articles = db.query(Article) \
        .order_by(Article.created_at.desc()).offset(start).limit(per_page).all()

    # Dictionary for articles by website_id, like grouping articles of each website for efficient lookup.
    articles_by_website = {}
    for article in articles:
        if article.website_id not in articles_by_website:
            articles_by_website[article.website_id] = []
        articles_by_website[article.website_id].append(article)

    websites = db.query(Website).all()
    websites_per_page: List[Website] = []
    for website in websites:
        websites_per_page.append({
            "id": website.id,
            "name": website.name,
            "url": website.url,
            "favicon_url": website.favicon_url,
            "created_at": website.created_at,
            "articles": [article for article in articles_by_website.get(website.id, [])]
        })

    schema = WebsiteSchema(many=True)
    results = schema.dump(websites_per_page)

    return jsonify({
        "total_pages": total_pages,
        "results": results,
    })


@main.route("/api/allnews", methods=["GET"])
def get_all_news():
    db = next(get_db())

    articles = db.query(Article).order_by(Article.created_at.desc()).all()

    # Dictionary for articles by website_id, like grouping articles of each website for efficient lookup.
    articles_by_website = {}
    for article in articles:
        if article.website_id not in articles_by_website:
            articles_by_website[article.website_id] = []
        articles_by_website[article.website_id].append(article)

    websites = db.query(Website).all()
    news = []
    for website in websites:
        news.append({
            "id": website.id,
            "name": website.name,
            "url": website.url,
            "favicon_url": website.favicon_url,
            "created_at": website.created_at,
            "articles": [article for article in articles_by_website.get(website.id, [])]
        })

    schema = WebsiteSchema(many=True)
    results = schema.dump(news)

    return jsonify({
        "results": results,
    })

@main.route("/")
def home():
    return "<h1>running</h1>"
