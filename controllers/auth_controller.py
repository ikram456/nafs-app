from sqlalchemy.orm import Session
from models.user import User
import hashlib


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str):
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def inscrire_user(db: Session, nom: str, prenom: str, email: str, mot_de_passe: str, role: str = "patient"):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return None, "Email déjà utilisé"

    nouveau_user = User(
        nom=nom,
        prenom=prenom,
        email=email,
        mot_de_passe=hash_password(mot_de_passe),
        role=role
    )
    db.add(nouveau_user)
    db.commit()
    db.refresh(nouveau_user)
    return nouveau_user, "Inscription réussie"


def connecter_user(db: Session, email: str, mot_de_passe: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None, "Utilisateur non trouvé"
    if not verify_password(mot_de_passe, user.mot_de_passe):
        return None, "Mot de passe incorrect"
    return user, "Connexion réussie"