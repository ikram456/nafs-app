import tkinter as tk
from tkinter import messagebox
from database import SessionLocal
from controllers.auth_controller import connecter_user

def ouvrir_login(root):
    window = tk.Toplevel(root)
    window.title("Nafs App - Connexion")
    window.geometry("400x500")
    window.configure(bg="#F0F4F8")
    window.resizable(False, False)

    # Titre
    tk.Label(window, text="نفس", font=("Arial", 36, "bold"),
             bg="#F0F4F8", fg="#2D6A4F").pack(pady=20)
    tk.Label(window, text="Connexion", font=("Arial", 16),
             bg="#F0F4F8", fg="#555").pack()

    # Cadre formulaire
    frame = tk.Frame(window, bg="white", padx=30, pady=30,
                     relief="flat", bd=0)
    frame.pack(pady=20, padx=30, fill="both")

    # Email
    tk.Label(frame, text="Email", font=("Arial", 11),
             bg="white", fg="#333").pack(anchor="w")
    email_entry = tk.Entry(frame, font=("Arial", 12),
                           relief="solid", bd=1)
    email_entry.pack(fill="x", pady=(0, 15), ipady=8)

    # Mot de passe
    tk.Label(frame, text="Mot de passe", font=("Arial", 11),
             bg="white", fg="#333").pack(anchor="w")
    password_entry = tk.Entry(frame, show="*", font=("Arial", 12),
                              relief="solid", bd=1)
    password_entry.pack(fill="x", pady=(0, 20), ipady=8)

    def connecter():
        email = email_entry.get()
        mot_de_passe = password_entry.get()

        if not email or not mot_de_passe:
            messagebox.showerror("Erreur", "Remplis tous les champs")
            return

        db = SessionLocal()
        user, message = connecter_user(db, email, mot_de_passe)
        db.close()

        if user:
            messagebox.showinfo("Succès", f"Marhaba {user.prenom} !")
            window.destroy()
        else:
            messagebox.showerror("Erreur", message)

    # Bouton connexion
    tk.Button(frame, text="Se connecter", font=("Arial", 12, "bold"),
              bg="#2D6A4F", fg="white", relief="flat",
              cursor="hand2", command=connecter).pack(fill="x", ipady=10)