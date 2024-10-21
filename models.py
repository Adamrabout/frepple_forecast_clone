from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection
engine = create_engine('sqlite:///frepple_forecast.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Define Forecast Model
class Forecast(Base):
    __tablename__ = 'forecasts'
    id = Column(Integer, primary_key=True)
    item = Column(String)
    location = Column(String)
    time_bucket = Column(Date)
    forecast_value = Column(Float)

# Create tables in the database
Base.metadata.create_all(engine)
