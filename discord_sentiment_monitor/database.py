import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    content = Column(String)
    user_id = Column(String)
    sentiment_score = Column(Float)
    topic_category = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Use environment variable for database connection
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("No DATABASE_URL environment variable has been set.")

# For Heroku, we need to update the URL scheme
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def test_db_connection():
    try:
        session = Session()
        session.execute(text("SELECT 1"))
        print("Successfully connected to the database!")
        session.close()
    except Exception as e:
        print(f"Failed to connect to the database: {str(e)}")

if __name__ == "__main__":
    test_db_connection()