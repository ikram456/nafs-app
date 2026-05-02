import tkinter as tk
from tkinter import ttk
from database import SessionLocal
from controllers.therapeute_controller import get_tous_therapeutes

def ouvrir_therapeutes(root):
    window = tk.Toplevel(root)
    window.title("Nafs App - Thérapeutes")
    window.geometry("600x500")
    window.configure(bg="#F0F4F8")

    # Titre
    tk.Label(window, text="Nos Thérapeutes", font=("Arial", 20, "bold"),
             bg="#F0F4F8", fg="#2D6A4F").pack(pady=20)

    # Cadre liste
    frame = tk.Frame(window, bg="white")
    frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Colonnes
    columns = ("Nom", "Spécialité", "Ville", "Tarif", "Langue")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=110, anchor="center")

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Charger les données
    db = SessionLocal()
    therapeutes = get_tous_therapeutes(db)
    db.close()

    if therapeutes:
        for therapeute, user in therapeutes:
            tree.insert("", "end", values=(
                f"{user.nom} {user.prenom}",
                therapeute.specialite,
                therapeute.ville,
                f"{therapeute.tarif} MAD",
                therapeute.langue
            ))
    else:
        tk.Label(frame, text="Aucun thérapeute disponible pour le moment",
                 font=("Arial", 12), bg="white", fg="#888").pack(pady=50)

    # Bouton fermer
    tk.Button(window, text="Fermer", font=("Arial", 11),
              bg="#2D6A4F", fg="white", relief="flat",
              cursor="hand2", command=window.destroy).pack(pady=10)