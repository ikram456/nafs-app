from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    mot_de_passe = Column(String, nullable=False)
    role = Column(String, default="patient")
    est_actif = Column(Boolean, default=True)
    date_creation = Column(DateTime, server_default=func.now())

    # ─── CHAMPS PATIENT ────────────────────────────────────────
    # Questionnaire
    problematique = Column(String, nullable=True)       # anxiete, depression...
    langue_preferee = Column(String, nullable=True)     # arabe, francais...
    genre_therapeute = Column(String, nullable=True)    # homme, femme, indifferent
    disponibilite = Column(String, nullable=True)       # matin, soir, weekend...

    # ─── CHAMPS THÉRAPEUTE ─────────────────────────────────────
    # Profil public
    bio = Column(Text, nullable=True)                   # description courte
    specialites = Column(String, nullable=True)         # anxiete,depression,couple...
    langues = Column(String, nullable=True)             # arabe,francais,amazigh
    tarif = Column(Integer, nullable=True)              # prix par séance en MAD
    experience_ans = Column(Integer, nullable=True)     # années d'expérience
    diplome = Column(String, nullable=True)             # diplôme principal
    genre = Column(String, nullable=True)               # homme ou femme
    disponibilites = Column(String, nullable=True)      # lundi,mardi,mercredi...
    profil_complete = Column(Boolean, default=False)    # a-t-il complété son profil ?
    photo_url = Column(String, nullable=True)           # photo de profil
    note_moyenne = Column(Integer, default=0)           # note /5
    nombre_avis = Column(Integer, default=0)            # nombre d'avis reçus
