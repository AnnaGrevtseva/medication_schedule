from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from database.database import engine


Base = declarative_base()


class ScheduleDb(Base):
    __tablename__ = "schedule"
    schedule_id = Column(Integer, primary_key=True, index=True)
    drug_name = Column(String)
    reception_frequency = Column(Integer)
    treatment_period = Column(Date)
    user_id = Column(Integer)


Base.metadata.create_all(bind=engine)
