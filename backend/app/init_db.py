import time
from .database import Base, engine
from .models import Website, Article
from sqlalchemy.exc import OperationalError

count = 3
for attempt in range(count):
    try:
        print(f"\nAttempting to connect to the database...[{attempt + 1}/{count}]")
        engine.connect()
        print("\nDatabase connection successful!")
        break
    except OperationalError as e:
        if attempt == count - 1:
            print("\nDatabase could not connect:", e)
        else:
            print("Database is not ready, retrying in 2 seconds...")
            time.sleep(2)


Base.metadata.create_all(bind=engine)
print("\n----Database initialized.----\n")


