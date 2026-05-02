import tkinter as tk
from tkinter import messagebox
from database import SessionLocal
from controllers.auth_controller import inscrire_user

def ouvrir_inscription(root):
    window = tk.Toplevel(root)
    window.title("Nafs App - Inscription")
    window.geometry("400x600")
    window.configure(bg="#F0F4F8")
    window.resizable(False, False)

    # Titre
    tk.Label(window, text="نفس", font=("Arial", 36, "bold"),
             bg="#F0F4F8", fg="#2D6A4F").pack(pady=20)
    tk.Label(window, text="Créer un compte", font=("Arial", 16),
             bg="#F0F4F8", fg="#555").pack()

    # Cadre formulaire
    frame = tk.Frame(window, bg="white", padx=30, pady=30)
    frame.pack(pady=20, padx=30, fill="both")

    # Nom
    tk.Label(frame, text="Nom", font=("Arial", 11),
             bg="white", fg="#333").pack(anchor="w")
    nom_entry = tk.Entry(frame, font=("Arial", 12), relief="solid", bd=1)
    nom_entry.pack(fill="x", pady=(0, 10), ipady=8)

    # Prénom
    tk.Label(frame, text="Prénom", font=("Arial", 11),
             bg="white", fg="#333").pack(anchor="w")
    prenom_entry = tk.Entry(frame, font=("Arial", 12), relief="solid", bd=1)
    prenom_entry.pack(fill="x", pady=(0, 10), ipady=8)

    # Email
    tk.Label(frame, text="Email", font=("Arial", 11),
             bg="white", fg="#333").pack(anchor="w")
    email_entry = tk.Entry(frame, font=("Arial", 12), relief="solid", bd=1)
    email_entry.pack(fill="x", pady=(0, 10), ipady=8)

    # Mot de passe
    tk.Label(frame, text="Mot de passe", font=("Arial", 11),
             bg="white", fg="#333").pack(anchor="w")
    password_entry = tk.Entry(frame, show="*", font=("Arial", 12),
                              relief="solid", bd=1)
    password_entry.pack(fill="x", pady=(0, 10), ipady=8)

    # Rôle
    tk.Label(frame, text="Je suis", font=("Arial", 11),
             bg="white", fg="#333").pack(anchor="w")
    role_var = tk.StringVar(value="patient")
    role_frame = tk.Frame(frame, bg="white")
    role_frame.pack(fill="x", pady=(0, 15))
    tk.Radiobutton(role_frame, text="Patient", variable=role_var,
                   value="patient", bg="white", font=("Arial", 11)).pack(side="left")
    tk.Radiobutton(role_frame, text="Thérapeute", variable=role_var,
                   value="therapeute", bg="white", font=("Arial", 11)).pack(side="left")

    def inscrire():
        nom = nom_entry.get()
        prenom = prenom_entry.get()
        email = email_entry.get()
        mot_de_passe = password_entry.get()
        role = role_var.get()

        if not all([nom, prenom, email, mot_de_passe]):
            messagebox.showerror("Erreur", "Remplis tous les champs")
            return

        db = SessionLocal()
        user, message = inscrire_user(db, nom, prenom, email, mot_de_passe, role)
        db.close()

        if user:
            messagebox.showinfo("Succès", "Compte créé avec succès !")
            window.destroy()
        else:
            messagebox.showerror("Erreur", message)

    tk.Button(frame, text="S'inscrire", font=("Arial", 12, "bold"),
              bg="#2D6A4F", fg="white", relief="flat",
              cursor="hand2", command=inscrire).pack(fill="x", ipady=10)