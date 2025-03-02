from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

Base = declarative_base()

load_dotenv()

class WBSElement(Base):
    __tablename__ = 'wbs_elements'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    parent_id = Column(Integer, ForeignKey('wbs_elements.id'), nullable=True)  # Allows hierarchy
    budget = Column(Float, default=0.0)

# Initialize the database
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)