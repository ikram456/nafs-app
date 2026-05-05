from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Questionnaire(Base):
    __tablename__ = "questionnaires"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), unique=True)
    problematique = Column(String)   # ex: "anxiete", "depression", "couple", "trauma"
    langue = Column(String)          # "arabe", "francais", "amazigh"
    genre_therapeute = Column(String) # "homme", "femme", "indifferent"
    disponibilite = Column(String)   # "matin", "soir", "weekend"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Matching(Base):
    __tablename__ = "matchings"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), unique=True)
    therapeute_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
