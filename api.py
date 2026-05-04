from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import HTTPException
from pydantic import BaseModel
import httpx
from database import engine, Base, SessionLocal
from models import user, therapeute
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
    return FileResponse("static/index.html")

@app.get("/login")
def login():
    return FileResponse("static/login.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("static/dashboard.html")

@app.get("/therapeutes")
def therapeutes():
    return FileResponse("static/therapeutes.html")

@app.get("/reservation")
def reservation():
    return FileResponse("static/reservation.html")

@app.get("/chat")
def chat():
    return FileResponse("static/chat.html")

@app.get("/profil")
def profil():
    return FileResponse("static/profil.html")

@app.get("/video")
def video():
    return FileResponse("static/video.html")

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
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.daily.co/v1/rooms",
            headers={
                "Authorization": f"Bearer {DAILY_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "properties": {
                    "max_participants": 2,
                    "enable_chat": True,
                    "enable_screenshare": True,
                    "exp": 3600
                }
            }
        )
        data = response.json()
        return {"url": data["url"], "name": data["name"]}

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
