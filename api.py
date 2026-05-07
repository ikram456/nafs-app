from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from database import engine, Base, SessionLocal
from models.user import User
from models.matching import Questionnaire, Matching, Seance, Avis, Demande
from controllers.auth_controller import connecter_user, inscrire_user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

DAILY_API_KEY = "282286f7928b1501d7d6bf2a71ea38400a9e20b5671ac3938761de4a1fd38953"

# ─── MODÈLES PYDANTIC ──────────────────────────────────────────

class LoginData(BaseModel):
    email: str
    mot_de_passe: str

class InscriptionData(BaseModel):
    nom: str
    prenom: str
    email: str
    mot_de_passe: str
    role: str = "patient"

class QuestionnaireData(BaseModel):
    patient_id: int
    problematique: str
    langue: str
    genre_therapeute: str
    disponibilite: str

class ChoixTherapeuteData(BaseModel):
    patient_id: int
    therapeute_id: int

class ProfilTherapeuteData(BaseModel):
    therapeute_id: int
    bio: Optional[str] = None
    specialites: Optional[str] = None
    langues: Optional[str] = None
    tarif: Optional[int] = None
    experience_ans: Optional[int] = None
    diplome: Optional[str] = None
    genre: Optional[str] = None
    disponibilites: Optional[str] = None

class SeanceData(BaseModel):
    patient_id: int
    therapeute_id: int
    date_heure: str
    type_seance: str = "video"

class AvisData(BaseModel):
    patient_id: int
    therapeute_id: int
    seance_id: Optional[int] = None
    note: int
    commentaire: Optional[str] = None

class NotesSeanceData(BaseModel):
    seance_id: int
    notes: str

class DemandeData(BaseModel):
    patient_id: int
    therapeute_id: int
    message: Optional[str] = None

class ReponseDemandeData(BaseModel):
    demande_id: int
    statut: str


# ─── PAGES STATIQUES ───────────────────────────────────────────

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/login")
def login():
    return FileResponse("static/login.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("static/login.html")

@app.get("/dashboard-patient")
def dashboard_patient():
    return FileResponse("static/dashboard-patient.html")

@app.get("/dashboard-therapeute")
def dashboard_therapeute_page():
    return FileResponse("static/dashboard-therapeute.html")

@app.get("/dashboard-admin")
def dashboard_admin():
    return FileResponse("static/dashboard-admin.html")

@app.get("/questionnaire")
def questionnaire():
    return FileResponse("static/questionnaire.html")

@app.get("/therapeutes")
def therapeutes():
    return FileResponse("static/therapeutes.html")

@app.get("/therapeute")
def therapeute_profil():
    return FileResponse("static/therapeute.html")

@app.get("/reservation")
def reservation():
    return FileResponse("static/reservation.html")

@app.get("/chat")
def chat():
    return FileResponse("static/chat.html")

@app.get("/chat-therapeute")
def chat_therapeute():
    return FileResponse("static/chat-therapeute.html")

@app.get("/profil")
def profil():
    return FileResponse("static/profil.html")

@app.get("/profil-therapeute")
def profil_therapeute():
    return FileResponse("static/profil-therapeute.html")

@app.get("/video")
def video():
    return FileResponse("static/video.html")


# ─── API VIDÉO DAILY.CO ────────────────────────────────────────

@app.post("/api/video/creer-salle")
async def creer_salle_video():
    import urllib.request
    import json
    import ssl

    url = "https://api.daily.co/v1/rooms"
    headers = {
        "Authorization": f"Bearer {DAILY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "properties": {
            "max_participants": 2,
            "enable_chat": True,
            "exp": 3600
        }
    }).encode('utf-8')

    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            result = json.loads(response.read().decode('utf-8'))
            return {"url": result["url"], "name": result["name"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── AUTH ──────────────────────────────────────────────────────

@app.post("/auth/connexion")
def connexion(data: LoginData):
    db = SessionLocal()
    result, message = connecter_user(db, data.email, data.mot_de_passe)
    db.close()
    if not result:
        raise HTTPException(status_code=400, detail=message)
    return {
        "message": "Connexion réussie",
        "id": result.id,
        "nom": result.nom,
        "prenom": result.prenom,
        "role": result.role,
        "profil_complete": result.profil_complete if result.role == "therapeute" else True
    }

@app.post("/auth/inscription")
def inscription(data: InscriptionData):
    db = SessionLocal()
    result, message = inscrire_user(db, data.nom, data.prenom, data.email, data.mot_de_passe, data.role)
    db.close()
    if not result:
        raise HTTPException(status_code=400, detail=message)
    return {
        "message": "Inscription réussie",
        "id": result.id,
        "nom": result.nom,
        "prenom": result.prenom,
        "role": result.role,
        "profil_complete": False
    }


# ─── QUESTIONNAIRE ─────────────────────────────────────────────

@app.post("/api/questionnaire")
def soumettre_questionnaire(data: QuestionnaireData):
    db = SessionLocal()
    existant = db.query(Questionnaire).filter(
        Questionnaire.patient_id == data.patient_id
    ).first()
    if existant:
        db.close()
        return {"message": "Questionnaire déjà soumis", "therapeute_id": None}
    q = Questionnaire(
        patient_id=data.patient_id,
        problematique=data.problematique,
        langue=data.langue,
        genre_therapeute=data.genre_therapeute,
        disponibilite=data.disponibilite
    )
    db.add(q)
    db.commit()
    db.close()
    return {"message": "Questionnaire soumis", "therapeute_id": None}


# ─── DEMANDES ──────────────────────────────────────────────────

@app.post("/api/demande")
def envoyer_demande(data: DemandeData):
    db = SessionLocal()
    existante = db.query(Demande).filter(
        Demande.patient_id == data.patient_id,
        Demande.therapeute_id == data.therapeute_id
    ).first()
    if existante:
        db.close()
        return {
            "message": "Demande déjà envoyée",
            "statut": existante.statut,
            "demande_id": existante.id
        }
    demande = Demande(
        patient_id=data.patient_id,
        therapeute_id=data.therapeute_id,
        message=data.message,
        statut="en_attente"
    )
    db.add(demande)
    db.commit()
    db.refresh(demande)
    db.close()
    return {
        "message": "Demande envoyée",
        "statut": "en_attente",
        "demande_id": demande.id
    }

@app.get("/api/demande-statut/{patient_id}/{therapeute_id}")
def get_demande_statut(patient_id: int, therapeute_id: int):
    db = SessionLocal()
    demande = db.query(Demande).filter(
        Demande.patient_id == patient_id,
        Demande.therapeute_id == therapeute_id
    ).first()
    db.close()
    if not demande:
        return {"statut": "aucune"}
    return {"statut": demande.statut, "demande_id": demande.id}

@app.get("/api/demandes-therapeute/{therapeute_id}")
def get_demandes_therapeute(therapeute_id: int):
    db = SessionLocal()
    demandes = db.query(Demande).filter(
        Demande.therapeute_id == therapeute_id,
        Demande.statut == "en_attente"
    ).all()
    result = []
    for d in demandes:
        p = db.query(User).filter(User.id == d.patient_id).first()
        if p:
            result.append({
                "id": d.id,
                "patient_id": d.patient_id,
                "patient_nom": p.nom,
                "patient_prenom": p.prenom,
                "message": d.message or "",
                "created_at": d.created_at.isoformat() if d.created_at else ""
            })
    db.close()
    return result

@app.post("/api/repondre-demande")
def repondre_demande(data: ReponseDemandeData):
    db = SessionLocal()
    demande = db.query(Demande).filter(Demande.id == data.demande_id).first()
    if not demande:
        db.close()
        raise HTTPException(status_code=404, detail="Demande non trouvée")
    demande.statut = data.statut
    db.commit()
    if data.statut == "acceptee":
        existant = db.query(Matching).filter(
            Matching.patient_id == demande.patient_id,
            Matching.therapeute_id == demande.therapeute_id
        ).first()
        if not existant:
            matching = Matching(
                patient_id=demande.patient_id,
                therapeute_id=demande.therapeute_id,
                statut="actif"
            )
            db.add(matching)
            db.commit()
    db.close()
    return {"message": "Réponse enregistrée", "statut": data.statut}


# ─── THÉRAPEUTES ───────────────────────────────────────────────

@app.get("/api/therapeutes")
def get_therapeutes():
    db = SessionLocal()
    liste = db.query(User).filter(User.role == "therapeute").all()
    db.close()
    return [
        {
            "id": t.id,
            "nom": t.nom,
            "prenom": t.prenom,
            "bio": t.bio or "",
            "specialites": t.specialites or "",
            "langues": t.langues or "",
            "tarif": t.tarif or 0,
            "experience_ans": t.experience_ans or 0,
            "genre": t.genre or "",
            "note_moyenne": t.note_moyenne or 0,
            "nombre_avis": t.nombre_avis or 0,
            "profil_complete": t.profil_complete or False
        }
        for t in liste
    ]

@app.get("/api/therapeute/{therapeute_id}")
def get_therapeute(therapeute_id: int):
    db = SessionLocal()
    t = db.query(User).filter(User.id == therapeute_id, User.role == "therapeute").first()
    db.close()
    if not t:
        raise HTTPException(status_code=404, detail="Thérapeute non trouvé")
    return {
        "id": t.id,
        "nom": t.nom,
        "prenom": t.prenom,
        "bio": t.bio or "",
        "specialites": t.specialites or "",
        "langues": t.langues or "",
        "tarif": t.tarif or 0,
        "experience_ans": t.experience_ans or 0,
        "diplome": t.diplome or "",
        "genre": t.genre or "",
        "disponibilites": t.disponibilites or "",
        "note_moyenne": t.note_moyenne or 0,
        "nombre_avis": t.nombre_avis or 0
    }

@app.post("/api/profil-therapeute")
def mettre_a_jour_profil(data: ProfilTherapeuteData):
    db = SessionLocal()
    t = db.query(User).filter(User.id == data.therapeute_id).first()
    if not t:
        db.close()
        raise HTTPException(status_code=404, detail="Thérapeute non trouvé")
    if data.bio is not None: t.bio = data.bio
    if data.specialites is not None: t.specialites = data.specialites
    if data.langues is not None: t.langues = data.langues
    if data.tarif is not None: t.tarif = data.tarif
    if data.experience_ans is not None: t.experience_ans = data.experience_ans
    if data.diplome is not None: t.diplome = data.diplome
    if data.genre is not None: t.genre = data.genre
    if data.disponibilites is not None: t.disponibilites = data.disponibilites
    t.profil_complete = True
    db.commit()
    db.close()
    return {"message": "Profil mis à jour"}


# ─── PATIENTS ──────────────────────────────────────────────────

@app.get("/api/mes-patients/{therapeute_id}")
def get_mes_patients(therapeute_id: int):
    db = SessionLocal()
    matchings = db.query(Matching).filter(
        Matching.therapeute_id == therapeute_id
    ).all()
    patients = []
    for m in matchings:
        p = db.query(User).filter(User.id == m.patient_id).first()
        if p:
            patients.append({
                "id": p.id,
                "nom": p.nom,
                "prenom": p.prenom,
                "problematique": p.problematique or ""
            })
    db.close()
    return patients


# ─── SÉANCES ───────────────────────────────────────────────────

@app.post("/api/seance")
def creer_seance(data: SeanceData):
    import datetime
    db = SessionLocal()
    seance = Seance(
        patient_id=data.patient_id,
        therapeute_id=data.therapeute_id,
        date_heure=datetime.datetime.fromisoformat(data.date_heure),
        type_seance=data.type_seance,
        statut="confirmee"
    )
    db.add(seance)
    db.commit()
    db.refresh(seance)
    db.close()
    return {"message": "Séance créée", "seance_id": seance.id}

@app.get("/api/seances-patient/{patient_id}")
def get_seances_patient(patient_id: int):
    db = SessionLocal()
    seances = db.query(Seance).filter(
        Seance.patient_id == patient_id
    ).order_by(Seance.date_heure).all()
    result = []
    for s in seances:
        t = db.query(User).filter(User.id == s.therapeute_id).first()
        result.append({
            "id": s.id,
            "date_heure": s.date_heure.isoformat() if s.date_heure else "",
            "type_seance": s.type_seance,
            "statut": s.statut,
            "therapeute_nom": t.nom if t else "",
            "therapeute_prenom": t.prenom if t else ""
        })
    db.close()
    return result

@app.get("/api/seances-therapeute/{therapeute_id}")
def get_seances_therapeute(therapeute_id: int):
    db = SessionLocal()
    seances = db.query(Seance).filter(
        Seance.therapeute_id == therapeute_id
    ).order_by(Seance.date_heure).all()
    result = []
    for s in seances:
        p = db.query(User).filter(User.id == s.patient_id).first()
        result.append({
            "id": s.id,
            "date_heure": s.date_heure.isoformat() if s.date_heure else "",
            "type_seance": s.type_seance,
            "statut": s.statut,
            "patient_nom": p.nom if p else "",
            "patient_prenom": p.prenom if p else ""
        })
    db.close()
    return result

@app.post("/api/notes-seance")
def ajouter_notes(data: NotesSeanceData):
    db = SessionLocal()
    seance = db.query(Seance).filter(Seance.id == data.seance_id).first()
    if not seance:
        db.close()
        raise HTTPException(status_code=404, detail="Séance non trouvée")
    seance.notes_therapeute = data.notes
    seance.statut = "terminee"
    db.commit()
    db.close()
    return {"message": "Notes sauvegardées"}


# ─── AVIS ──────────────────────────────────────────────────────

@app.post("/api/avis")
def ajouter_avis(data: AvisData):
    db = SessionLocal()
    avis = Avis(
        patient_id=data.patient_id,
        therapeute_id=data.therapeute_id,
        seance_id=data.seance_id,
        note=data.note,
        commentaire=data.commentaire
    )
    db.add(avis)
    db.commit()
    tous_avis = db.query(Avis).filter(Avis.therapeute_id == data.therapeute_id).all()
    moyenne = sum(a.note for a in tous_avis) // len(tous_avis)
    t = db.query(User).filter(User.id == data.therapeute_id).first()
    if t:
        t.note_moyenne = moyenne
        t.nombre_avis = len(tous_avis)
        db.commit()
    db.close()
    return {"message": "Avis ajouté"}


# ─── MIGRATION ─────────────────────────────────────────────────

@app.get("/api/migration-demandes")
def migration_demandes():
    from sqlalchemy import text
    db = SessionLocal()
    try:
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS demandes (
                id SERIAL PRIMARY KEY,
                patient_id INTEGER REFERENCES users(id),
                therapeute_id INTEGER REFERENCES users(id),
                statut VARCHAR DEFAULT 'en_attente',
                message TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """))
        db.commit()
    except Exception as e:
        db.rollback()
        db.close()
        return {"message": str(e)}
    db.close()
    return {"message": "Table demandes créée"}


# ─── ADMIN ─────────────────────────────────────────────────────

@app.get("/admin/supprimer-fake-therapeutes")
def supprimer_fake():
    db = SessionLocal()
    db.query(User).filter(User.role == "therapeute").delete()
    db.commit()
    db.close()
    return {"message": "Thérapeutes supprimés avec succès"}

@app.get("/admin/alter-tables")
def alter_tables():
    from sqlalchemy import text
    db = SessionLocal()
    colonnes = [
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS bio TEXT",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS specialites VARCHAR",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS langues VARCHAR",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS tarif INTEGER",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS experience_ans INTEGER",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS diplome VARCHAR",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS genre VARCHAR",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS disponibilites VARCHAR",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS profil_complete BOOLEAN DEFAULT FALSE",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS photo_url VARCHAR",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS note_moyenne INTEGER DEFAULT 0",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS nombre_avis INTEGER DEFAULT 0",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS problematique VARCHAR",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS langue_preferee VARCHAR",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS genre_therapeute VARCHAR",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS disponibilite VARCHAR",
    ]
    for col in colonnes:
        try:
            db.execute(text(col))
        except:
            pass
    db.commit()
    db.close()
    return {"message": "Tables mises à jour"}
