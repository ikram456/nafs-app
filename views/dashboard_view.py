import tkinter as tk
from views.therapeute_view import ouvrir_therapeutes

def ouvrir_dashboard(root, user):
    window = tk.Toplevel(root)
    window.title("Nafs App - Dashboard")
    window.geometry("500x600")
    window.configure(bg="#F0F4F8")
    window.resizable(False, False)

    # Header
    header = tk.Frame(window, bg="#2D6A4F", height=100)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(header, text="نفس", font=("Arial", 28, "bold"),
             bg="#2D6A4F", fg="white").pack(side="left", padx=20)
    tk.Label(header, text=f"Marhaba, {user.prenom} !",
             font=("Arial", 14), bg="#2D6A4F", fg="white").pack(side="left")

    # Menu principal
    frame = tk.Frame(window, bg="#F0F4F8", padx=30, pady=30)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Que veux-tu faire ?",
             font=("Arial", 16, "bold"),
             bg="#F0F4F8", fg="#333").pack(pady=(0, 20))

    # Boutons menu
    boutons = [
        ("Voir les thérapeutes", lambda: ouvrir_therapeutes(window)),
        ("Mes réservations", lambda: None),
        ("Mon profil", lambda: None),
        ("Chat", lambda: None),
    ]

    for texte, commande in boutons:
        btn_frame = tk.Frame(frame, bg="white", relief="flat")
        btn_frame.pack(fill="x", pady=8)
        tk.Button(btn_frame, text=texte,
                  font=("Arial", 13),
                  bg="white", fg="#2D6A4F",
                  relief="flat", cursor="hand2",
                  anchor="w", padx=20,
                  command=commande).pack(fill="x", ipady=15)

    # Bouton déconnexion
    tk.Button(window, text="Se déconnecter",
              font=("Arial", 11),
              bg="#E63946", fg="white",
              relief="flat", cursor="hand2",
              command=window.destroy).pack(pady=20)