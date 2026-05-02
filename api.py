from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from pydantic import BaseModel
from database import engine, Base, SessionLocal
from models import user, therapeute
from controllers.auth_controller import connecter_user, inscrire_user

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nafs App API",
    description="Plateforme de santé mentale pour la communauté marocaine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginData(BaseModel):
    email: str
    mot_de_passe: str

class InscriptionData(BaseModel):
    nom: str
    prenom: str
    email: str
    mot_de_passe: str
    role: str = "patient"

@app.get("/")
def home():
    return {"message": "Marhaba ! Nafs App est en ligne", "status": "ok"}

@app.post("/auth/connexion")
def connexion(data: LoginData):
    db = SessionLocal()
    user, message = connecter_user(db, data.email, data.mot_de_passe)
    db.close()
    if not user:
        raise HTTPException(status_code=400, detail=message)
    return {
        "message": "Connexion réussie",
        "id": user.id,
        "nom": user.nom,
        "prenom": user.prenom,
        "role": user.role
    }

@app.post("/auth/inscription")
def inscription(data: InscriptionData):
    db = SessionLocal()
    user, message = inscrire_user(db, data.nom, data.prenom, data.email, data.mot_de_passe, data.role)
    db.close()
    if not user:
        raise HTTPException(status_code=400, detail=message)
    return {
        "message": "Inscription réussie",
        "id": user.id,
        "nom": user.nom,
        "prenom": user.prenom,
        "role": user.role
    }