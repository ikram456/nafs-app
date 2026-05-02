from sqlalchemy.orm import Session
from models.therapeute import Therapeute
from models.user import User

def get_tous_therapeutes(db: Session):
    therapeutes = db.query(Therapeute, User).join(
        User, Therapeute.user_id == User.id
    ).all()
    return therapeutes

def get_therapeute_par_ville(db: Session, ville: str):
    therapeutes = db.query(Therapeute, User).join(
        User, Therapeute.user_id == User.id
    ).filter(Therapeute.ville == ville).all()
    return therapeutes

def creer_therapeute(db: Session, user_id: int, specialite: str,
                     ville: str, tarif: float, bio: str, langue: str):
    therapeute = Therapeute(
        user_id=user_id,
        specialite=specialite,
        ville=ville,
        tarif=tarif,
        bio=bio,
        langue=langue
    )
    db.add(therapeute)
    db.commit()
    db.refresh(therapeute)
    return therapeute