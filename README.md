# KAGEtestCode

**KAGEtestCode** est une application Python conçue pour analyser la force d'un mot de passe. Elle combine une méthode d'évaluation personnalisée (avec détection de motifs, longueur, diversité des caractères, etc.) et, si disponible, l'analyse avancée fournie par la bibliothèque [zxcvbn](https://github.com/dropbox/zxcvbn).  
L'interface graphique, réalisée avec Tkinter et ttk, offre des fonctionnalités pratiques telles que :

- Affichage/Cachage du mot de passe saisi  
- Génération automatique de mots de passe robustes  
- Conseils personnalisés pour améliorer la sécurité  
- Option de copier le résultat dans le presse-papiers  
- Boutons pour accéder aux astuces et à la section feedback

---

## Prérequis

- **Python 3.6** ou version ultérieure  
- **Tkinter** (inclus généralement avec Python)  
- [**zxcvbn**](https://pypi.org/project/zxcvbn/) (facultatif, pour une analyse avancée)  
- (Optionnel) [**PyInstaller**](https://www.pyinstaller.org/) pour générer un exécutable autonome

---

## Installation

### 1. Cloner le dépôt ou télécharger le fichier source

Clonez le dépôt Git ou téléchargez directement le fichier `KAGEtestCode.py` dans le répertoire de votre choix.

```bash
git clone https://github.com/votre-utilisateur/KAGEtestCode.git
cd KAGEtestCode
```

### 2. (Optionnel) Créer et activer un environnement virtuel

Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances.

```bash
# Création d'un environnement virtuel nommé 'venv'
python -m venv venv

# Activation de l'environnement
# Sous Windows
venv\Scripts\activate
# Sous macOS/Linux
source venv/bin/activate
```

### 3. Installer les dépendances

Si vous souhaitez bénéficier de l'analyse avancée avec **zxcvbn**, installez-le via pip :

```bash
pip install zxcvbn
```

_Votre installation de Tkinter devrait déjà être incluse dans votre distribution Python. Sinon, consultez la documentation de votre système pour l'installer._

---

## Utilisation

### Lancer l'application

Pour démarrer l'interface graphique, exécutez :

```bash
python KAGEtestCode.py
```

L'application s'ouvre alors avec toutes les fonctionnalités décrites (analyse, génération de mot de passe, conseils, etc.).

### Exécuter les tests unitaires

Pour vérifier le bon fonctionnement de l'ensemble des fonctionnalités, vous pouvez lancer les tests unitaires :

```bash
python KAGEtestCode.py --test
```

Les tests s'exécuteront et vous indiqueront si tout est conforme.

---

## Packaging

Pour distribuer l'application sous forme d'exécutable autonome, vous pouvez utiliser **PyInstaller** :

1. Installez PyInstaller (si ce n'est pas déjà fait) :

   ```bash
   pip install pyinstaller
   ```

2. Générez l'exécutable :

   ```bash
   pyinstaller --onefile KAGEtestCode.py
   ```

L'exécutable sera créé dans le répertoire `dist`.

---

## Feedback et contributions

Pour toute suggestion, retour ou contribution, n'hésitez pas à contacter :

**KAGEH@CK3R - GUY KOUAKOU**  
_Email :(mailto:gkouakou174@gmail.com)_

---

## Licence

Ce projet est publié sous licence [Indiquez ici la licence, par exemple MIT License].  
Consultez le fichier `LICENSE` pour plus d'informations.

---
