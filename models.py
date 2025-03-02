from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class WBSElement(Base):
    __tablename__ = 'wbs_elements'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    parent_id = Column(Integer, ForeignKey('wbs_elements.id'), nullable=True)  # Allows hierarchy
    budget = Column(Float, default=0.0)

# Initialize the database
engine = create_engine('postgresql://postgres:123Hupex123-@localhost:5432/budget_app')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)