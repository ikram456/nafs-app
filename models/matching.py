from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Questionnaire(Base):
    __tablename__ = "questionnaires"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), unique=True)
    problematique = Column(String)
    langue = Column(String)
    genre_therapeute = Column(String)
    disponibilite = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Matching(Base):
    __tablename__ = "matchings"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    therapeute_id = Column(Integer, ForeignKey("users.id"))
    statut = Column(String, default="actif")  # actif, termine, annule
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Seance(Base):
    __tablename__ = "seances"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    therapeute_id = Column(Integer, ForeignKey("users.id"))
    date_heure = Column(DateTime, nullable=False)
    duree_minutes = Column(Integer, default=50)
    type_seance = Column(String, default="video")  # video, chat
    statut = Column(String, default="confirmee")   # confirmee, annulee, terminee
    notes_therapeute = Column(Text, nullable=True) # notes privées du thérapeute
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Avis(Base):
    __tablename__ = "avis"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    therapeute_id = Column(Integer, ForeignKey("users.id"))
    seance_id = Column(Integer, ForeignKey("seances.id"), nullable=True)
    note = Column(Integer)           # note de 1 à 5
    commentaire = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Demande(Base):
    __tablename__ = "demandes"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    therapeute_id = Column(Integer, ForeignKey("users.id"))
    statut = Column(String, default="en_attente")  # en_attente, acceptee, refusee
    message = Column(Text, nullable=True)           # message du patient
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
