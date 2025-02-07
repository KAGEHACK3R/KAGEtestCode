#!/usr/bin/env python3
"""
KAGEtestCode - Analyse de Mot de Passe avec Interface Graphique Améliorée

Ce programme intègre plusieurs améliorations :
- Analyse de la robustesse du mot de passe (méthode personnalisée et via zxcvbn si installé)
- Interface graphique modernisée avec Tkinter ttk
- Options pour afficher/cacher le mot de passe, générer un mot de passe robuste, copier le résultat
- Affichage de conseils personnalisés et d'astuces pour créer un bon mot de passe
- Tests unitaires intégrés pour assurer la qualité du code

Packaging : Utilisez PyInstaller ou cx_Freeze pour créer un exécutable.
Feedback : Envoyez vos retours à guy.kouakou@example.com

Sincèrement,
KAGEH@CK3R - GUY KOUAKOU
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import string
import sys

# Tentative d'importation de zxcvbn pour une analyse avancée du mot de passe
try:
    from zxcvbn import zxcvbn
    USE_ZXCVBN = True
except ImportError:
    USE_ZXCVBN = False

# -------------------------------
# Fonctions d'analyse du mot de passe
# -------------------------------

def is_common_password(password: str) -> bool:
    """
    Vérifie si le mot de passe figure dans une liste de mots de passe trop courants.
    """
    common_passwords = [
        "password", "123456", "12345678", "qwerty", "abc123",
        "monkey", "letmein", "iloveyou", "admin", "welcome",
        # Liste enrichie
        "1234567", "12345", "1234", "000000", "sunshine", "princess",
        "football", "charlie", "donald", "dragon", "qwertyuiop"
    ]
    return password.lower() in common_passwords

def has_sequential_chars(s: str) -> bool:
    """
    Détecte la présence d'une séquence de 3 caractères consécutifs (ascendants ou descendants)
    pour des chiffres ou des lettres.
    """
    for i in range(len(s) - 2):
        # Séquences numériques
        if s[i].isdigit() and s[i+1].isdigit() and s[i+2].isdigit():
            a, b, c = int(s[i]), int(s[i+1]), int(s[i+2])
            if (a + 1 == b and b + 1 == c) or (a - 1 == b and b - 1 == c):
                return True
        # Séquences alphabétiques
        if s[i].isalpha() and s[i+1].isalpha() and s[i+2].isalpha():
            a, b, c = ord(s[i].lower()), ord(s[i+1].lower()), ord(s[i+2].lower())
            if (a + 1 == b and b + 1 == c) or (a - 1 == b and b - 1 == c):
                return True
    return False

def has_repeated_chars(s: str) -> bool:
    """
    Vérifie si la chaîne contient le même caractère répété 3 fois de suite.
    """
    for i in range(len(s) - 2):
        if s[i] == s[i+1] and s[i+1] == s[i+2]:
            return True
    return False

def evaluate_password_strength(password: str) -> str:
    """
    Évalue la force d'un mot de passe en utilisant zxcvbn si disponible, sinon une méthode personnalisée.
    Retourne "faible", "moyen" ou "fort".
    """
    if len(password) < 8:
        return "faible"
    if is_common_password(password):
        return "faible"
    
    if USE_ZXCVBN:
        result = zxcvbn(password)
        score = result.get('score', 0)  # score entre 0 et 4
        if score <= 1:
            return "faible"
        elif score == 2:
            return "moyen"
        else:
            return "fort"
    else:
        # Méthode personnalisée
        score = 0
        length = len(password)
        
        # Bonus selon la longueur
        if 8 <= length < 12:
            score += 1
        elif 12 <= length < 16:
            score += 2
        elif length >= 16:
            score += 3
        
        # Diversité des caractères
        if any(c.isupper() for c in password):
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        special_characters = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~"
        if any(c in special_characters for c in password):
            score += 1
        
        # Pénalités pour motifs évidents
        if has_sequential_chars(password):
            score -= 1
        if has_repeated_chars(password):
            score -= 1
        
        score = max(score, 0)
        
        if score < 4:
            return "faible"
        elif score < 6:
            return "moyen"
        else:
            return "fort"

def generate_password(length: int = 16) -> str:
    """
    Génère un mot de passe robuste avec au moins une majuscule, une minuscule, un chiffre et un symbole.
    """
    if length < 12:
        length = 12
    characters = {
        'upper': string.ascii_uppercase,
        'lower': string.ascii_lowercase,
        'digits': string.digits,
        'symbols': "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~"
    }
    # Assurer la présence d'un caractère de chaque catégorie
    password_chars = [
        random.choice(characters['upper']),
        random.choice(characters['lower']),
        random.choice(characters['digits']),
        random.choice(characters['symbols'])
    ]
    all_chars = characters['upper'] + characters['lower'] + characters['digits'] + characters['symbols']
    password_chars.extend(random.choice(all_chars) for _ in range(length - 4))
    random.shuffle(password_chars)
    return "".join(password_chars)

# -------------------------------
# Fonctions d'interface graphique
# -------------------------------

def analyze_password():
    """
    Récupère le mot de passe, l'analyse et affiche le résultat ainsi que des conseils.
    """
    password = entry_password.get()
    if not password:
        messagebox.showwarning("Attention", "Veuillez entrer un mot de passe.")
        return

    strength = evaluate_password_strength(password)
    label_result.config(text=f"Force : {strength.upper()}")

    # Conseils personnalisés selon le résultat
    if strength == "faible":
        advice = ("Votre mot de passe est FAIBLE.\n"
                  "Conseils : Utilisez au moins 12 caractères, mélangez lettres, chiffres et symboles, "
                  "et évitez les séquences ou répétitions évidentes.")
    elif strength == "moyen":
        advice = ("Votre mot de passe est MOYEN.\n"
                  "Conseils : Ajoutez davantage de caractères spéciaux et augmentez la longueur pour renforcer sa robustesse.")
    else:
        advice = "Votre mot de passe est FORT. Bon travail !"
    label_advice.config(text=advice)
    status_label.config(text="Analyse terminée.")

def toggle_password_visibility():
    """
    Permet d'afficher ou de masquer le mot de passe saisi.
    """
    if entry_password.cget('show') == '':
        entry_password.config(show="*")
        btn_toggle.config(text="Afficher")
    else:
        entry_password.config(show="")
        btn_toggle.config(text="Cacher")

def copy_result():
    """
    Copie le texte du résultat (force et conseils) dans le presse-papiers.
    """
    result_text = f"{label_result.cget('text')}\n{label_advice.cget('text')}"
    if result_text.strip():
        root.clipboard_clear()
        root.clipboard_append(result_text)
        status_label.config(text="Résultat copié dans le presse-papiers !")
    else:
        status_label.config(text="Rien à copier !")

def generate_password_callback():
    """
    Génère un mot de passe robuste, le place dans le champ de saisie et lance l'analyse.
    """
    pwd = generate_password()
    entry_password.delete(0, tk.END)
    entry_password.insert(0, pwd)
    status_label.config(text="Mot de passe généré.")
    analyze_password()

def show_tips():
    """
    Affiche une fenêtre avec des astuces pour créer un bon mot de passe.
    """
    tips = (
        "Astuces pour un bon mot de passe :\n"
        "- Utilisez au moins 12 caractères.\n"
        "- Mélangez majuscules, minuscules, chiffres et symboles.\n"
        "- Évitez les séquences évidentes et les répétitions.\n"
        "- Ne pas utiliser d'informations personnelles.\n"
        "- Pensez à utiliser un gestionnaire de mots de passe."
    )
    messagebox.showinfo("Astuces pour un bon mot de passe", tips)

def send_feedback():
    """
    Affiche une fenêtre avec des informations pour envoyer vos retours.
    """
    feedback = (
        "Pour toute suggestion ou retour, veuillez envoyer un email à :\n"
        "gkouakou174@gmail.com"
    )
    messagebox.showinfo("Feedback", feedback)

# -------------------------------
# Construction de l'interface graphique avec Tkinter ttk
# -------------------------------

root = tk.Tk()
root.title("KAGEtestCode - Analyse de Mot de Passe")
root.geometry("550x500")
root.resizable(False, False)
root.configure(bg="#f0f8ff")  # Fond bleu clair

# Utilisation de ttk pour une interface moderne
style = ttk.Style()
style.theme_use("clam")

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True)

# Titre et sous-titre
label_title = ttk.Label(main_frame, text="KAGEtestCode", font=("Helvetica", 20, "bold"))
label_title.pack(pady=(0, 10))

label_subtitle = ttk.Label(main_frame, text="Analyse de la Force de Votre Mot de Passe", font=("Helvetica", 14))
label_subtitle.pack(pady=(0, 20))

# Zone de saisie du mot de passe
label_entry = ttk.Label(main_frame, text="Entrez votre mot de passe :", font=("Helvetica", 12))
label_entry.pack(anchor="w")
entry_password = ttk.Entry(main_frame, show="*", width=40, font=("Helvetica", 12))
entry_password.pack(pady=5)

# Boutons pour les actions sur le mot de passe
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=10)

btn_toggle = ttk.Button(button_frame, text="Afficher", command=toggle_password_visibility)
btn_toggle.grid(row=0, column=0, padx=5)

btn_generate = ttk.Button(button_frame, text="Générer", command=generate_password_callback)
btn_generate.grid(row=0, column=1, padx=5)

btn_analyze = ttk.Button(button_frame, text="Analyser", command=analyze_password)
btn_analyze.grid(row=0, column=2, padx=5)

btn_copy = ttk.Button(button_frame, text="Copier", command=copy_result)
btn_copy.grid(row=0, column=3, padx=5)

# Boutons supplémentaires : Astuces et Feedback
extra_button_frame = ttk.Frame(main_frame)
extra_button_frame.pack(pady=10)

btn_tips = ttk.Button(extra_button_frame, text="Astuces", command=show_tips)
btn_tips.grid(row=0, column=0, padx=5)

btn_feedback = ttk.Button(extra_button_frame, text="Feedback", command=send_feedback)
btn_feedback.grid(row=0, column=1, padx=5)

# Zone d'affichage du résultat et des conseils
label_result = ttk.Label(main_frame, text="", font=("Helvetica", 14, "bold"), foreground="#d32f2f")
label_result.pack(pady=(20, 10))

label_advice = ttk.Label(main_frame, text="Conseils pour un bon mot de passe :\n- Utilisez au moins 12 caractères\n- Mélangez lettres, chiffres et symboles\n- Évitez les séquences évidentes",
                         font=("Helvetica", 10), justify="left")
label_advice.pack(pady=(0, 20))

# Zone de statut pour les messages temporaires
status_label = ttk.Label(main_frame, text="", font=("Helvetica", 10, "italic"))
status_label.pack(pady=(10, 0))

# Lancer l'analyse en appuyant sur la touche "Entrée"
root.bind('<Return>', lambda event: analyze_password())

# -------------------------------
# Tests unitaires
# -------------------------------
import unittest

class TestPasswordFunctions(unittest.TestCase):
    def test_common_password(self):
        self.assertTrue(is_common_password("password"))
        self.assertFalse(is_common_password("UniquePass123!"))
    
    def test_sequential_chars(self):
        self.assertTrue(has_sequential_chars("abc"))
        self.assertTrue(has_sequential_chars("321"))
        self.assertFalse(has_sequential_chars("a1b2c3"))
    
    def test_repeated_chars(self):
        self.assertTrue(has_repeated_chars("aaa"))
        self.assertFalse(has_repeated_chars("ababab"))
    
    def test_evaluate_password_strength_custom(self):
        # Test de la méthode personnalisée (si zxcvbn n'est pas utilisé)
        if not USE_ZXCVBN:
            self.assertEqual(evaluate_password_strength("Aa1!aa"), "faible")  # Moins de 8 caractères
            self.assertEqual(evaluate_password_strength("Aa1!Aa1!"), "moyen")
            self.assertEqual(evaluate_password_strength("Aa1!Aa1!Aa1!"), "fort")
    
    def test_generate_password(self):
        pwd = generate_password()
        self.assertTrue(len(pwd) >= 12)
        self.assertTrue(any(c.isupper() for c in pwd))
        self.assertTrue(any(c.islower() for c in pwd))
        self.assertTrue(any(c.isdigit() for c in pwd))
        special_characters = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~"
        self.assertTrue(any(c in special_characters for c in pwd))

# -------------------------------
# Exécution principale
# -------------------------------
if __name__ == '__main__':
    # Si l'argument '--test' est fourni, exécutez les tests unitaires
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        unittest.main(argv=[sys.argv[0]])
    else:
        root.mainloop()

