from datetime import datetime, timedelta, timezone
from ..models import Article
from ..database import SessionLocal
import logging

logger = logging.getLogger(__name__)

# Delete articles older than 2 Days
def delete_old_articles():
    try:
        with SessionLocal() as db:
            cutoff = datetime.now(timezone.utc) - timedelta(days=2)
            db.query(Article).filter(Article.created_at < cutoff).delete()
            db.commit()
            logger.info("Old articles deleted successfully")
    except Exception as e:
        logger.exception("Error deleting old articles")