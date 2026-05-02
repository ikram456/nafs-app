import tkinter as tk
from tkinter import messagebox
from database import engine, Base
from models import user, therapeute
from controllers.auth_controller import connecter_user, inscrire_user
from views.inscription_view import ouvrir_inscription
from views.dashboard_view import ouvrir_dashboard
from database import SessionLocal

Base.metadata.create_all(bind=engine)

class NafsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Nafs App - صحة نفسية للمغاربة")
        self.root.geometry("400x550")
        self.root.configure(bg="#F0F4F8")
        self.root.resizable(False, False)
        self.afficher_accueil()

    def afficher_accueil(self):
        # Titre principal
        tk.Label(self.root, text="نفس", font=("Arial", 52, "bold"),
                 bg="#F0F4F8", fg="#2D6A4F").pack(pady=30)
        tk.Label(self.root, text="صحتك النفسية تهمنا",
                 font=("Arial", 14), bg="#F0F4F8", fg="#555").pack()
        tk.Label(self.root, text="Votre santé mentale nous tient à cœur",
                 font=("Arial", 11), bg="#F0F4F8", fg="#888").pack(pady=5)

        # Formulaire connexion
        frame = tk.Frame(self.root, bg="white", padx=30, pady=30)
        frame.pack(pady=20, padx=30, fill="both")

        tk.Label(frame, text="Email", font=("Arial", 11),
                 bg="white", fg="#333").pack(anchor="w")
        self.email_entry = tk.Entry(frame, font=("Arial", 12),
                                    relief="solid", bd=1)
        self.email_entry.pack(fill="x", pady=(0, 15), ipady=8)

        tk.Label(frame, text="Mot de passe", font=("Arial", 11),
                 bg="white", fg="#333").pack(anchor="w")
        self.password_entry = tk.Entry(frame, show="*",
                                       font=("Arial", 12),
                                       relief="solid", bd=1)
        self.password_entry.pack(fill="x", pady=(0, 20), ipady=8)

        tk.Button(frame, text="Se connecter",
                  font=("Arial", 12, "bold"),
                  bg="#2D6A4F", fg="white", relief="flat",
                  cursor="hand2",
                  command=self.connecter).pack(fill="x", ipady=10)

        tk.Button(frame, text="Créer un compte",
                  font=("Arial", 11),
                  bg="#F0F4F8", fg="#2D6A4F", relief="flat",
                  cursor="hand2",
                  command=lambda: ouvrir_inscription(self.root)).pack(pady=10)

    def connecter(self):
        email = self.email_entry.get()
        mot_de_passe = self.password_entry.get()

        if not email or not mot_de_passe:
            messagebox.showerror("Erreur", "Remplis tous les champs")
            return

        db = SessionLocal()
        user, message = connecter_user(db, email, mot_de_passe)
        db.close()

        if user:
            ouvrir_dashboard(self.root, user)
        else:
            messagebox.showerror("Erreur", message)

    def lancer(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = NafsApp()
    app.lancer()
