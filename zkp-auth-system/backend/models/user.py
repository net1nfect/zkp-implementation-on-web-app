"""
User model for storing public keys
"""
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
from config import DATABASE_URL

Base = declarative_base()


class User(Base):
    """User model storing public key for ZKP authentication"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    public_key_x = Column(String(100), nullable=False)  # Hex representation
    public_key_y = Column(String(100), nullable=False)  # Hex representation
    created_at = Column(DateTime, default=datetime.now)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            "id": self.id,
            "username": self.username,
            "public_key": {
                "x": self.public_key_x,
                "y": self.public_key_y
            },
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def get_public_key_point(self):
        """Get public key as Point object"""
        from auth.crypto_utils import Point
        return Point(int(self.public_key_x, 16), int(self.public_key_y, 16))


# Database setup
engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


