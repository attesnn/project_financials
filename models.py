from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from dotenv import load_dotenv
import os

Base = declarative_base()

load_dotenv()


class ProjectDetails(Base):
    __tablename__ = 'project_details'

    id = Column(Integer, primary_key=True)
    project_name = Column(String(50), nullable=False)
    project_number = Column(String(50), nullable=False)
    #project_manager = Column(String(50), nullable=False)
    #project_start = Column(String(50), nullable=False)
    #project_end = Column(String(50), nullable=False)
    wbs_elements = relationship("WBSElement", back_populates="project")

class WBSElement(Base):
    __tablename__ = 'wbs_elements'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    project_id = Column(Integer, ForeignKey('project_details.id'), nullable=False)
    parent_id = Column(Integer, ForeignKey('wbs_elements.id'), nullable=True)  # Allows hierarchy
    budget = Column(Float, default=0.0)    
    project = relationship("ProjectDetails", back_populates="wbs_elements")
    #actual_costs = Column(Float, default=0.0)
    #planned_costs = Column(Float, default=0.0)
    #cumulative_costs = Column(Float, default=0.0)

# Initialize the database
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)