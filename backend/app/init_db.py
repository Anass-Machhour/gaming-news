import time
from .database import Base, engine
from .models import Website, Article
from sqlalchemy.exc import OperationalError

count = 3
for count in range(count):
    try:
        print(f"\nAttempting to connect to the database...[{count +1}/3]")
        engine.connect()
        print("\nDatabase connection successful!")
        break
    except OperationalError as e:
        if count == 2:
            print("\nDatabase could not connect:", e)
            break
        else:
            print("Database is not ready, Retrying in 2 seconds...")
            time.sleep(2)
            count += 1


Base.metadata.create_all(bind=engine)
print("\n----Database initialized.----\n")


