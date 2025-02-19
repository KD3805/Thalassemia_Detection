# File: database.py
import urllib
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Build the ODBC connection string for Windows Authentication.
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=HP\\SQLEXPRESS;"
    "DATABASE=BBMS;"
    "Trusted_Connection=yes;"
    "Encrypt=No;"  # Use 'No' instead of 'False'
)

# URL-encode the connection string.
params = urllib.parse.quote_plus(connection_string)

# Create the SQLAlchemy engine using the pyodbc connection.
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(DATABASE_URL, fast_executemany=True)

# Create a configured "Session" class.
SessionLocal = sessionmaker(bind=engine)

# Declare a Base for our models.
Base = declarative_base()

class BloodReport(Base):
    __tablename__ = "blood_reports"
    id = Column(Integer, primary_key=True, index=True)
    sex = Column(String(10))
    hb = Column(Float)
    pcv = Column(Float)
    rbc = Column(Float)
    mcv = Column(Float)
    mch = Column(Float)
    mchc = Column(Float)
    rdw = Column(Float)
    wbc = Column(Float)
    neut = Column(Float)
    lymph = Column(Float)
    plt = Column(Float)
    hba = Column(Float)
    hba2 = Column(Float)
    hbf = Column(Float)
    prediction = Column(Integer)  # Changed from String(50) to Integer

# Create tables if they do not exist.
Base.metadata.create_all(bind=engine)
