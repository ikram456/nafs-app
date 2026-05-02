from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Therapeute(Base):
    __tablename__ = "therapeutes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    specialite = Column(String, nullable=False)
    langue = Column(String, default="arabe,français")
    ville = Column(String, nullable=False)
    tarif = Column(Float, nullable=False)
    bio = Column(String)
    est_disponible = Column(Boolean, default=True)
    note_moyenne = Column(Float, default=0.0)
    date_creation = Column(DateTime, server_default=func.now())