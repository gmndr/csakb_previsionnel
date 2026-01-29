# CSAKB Prévisionnel

Application web de gestion des formulaires prévisionnels pour les sections du CSAKB.

## 🚀 Fonctionnalités

- **Saisie de données** : 4 thématiques (Budget prévisionnel, Bureau directeur, Diplômes et plan de formation, Salariés).
- **Identification par section** : Sélection de la section au démarrage pour personnaliser les exports.
- **Sauvegarde automatique** : Les formulaires peuvent être remplis indépendamment et sont conservés en base de données.
- **Exports complets** :
    - **Excel (XLSX)** : Un seul fichier avec 4 onglets correspondant aux 4 thématiques.
    - **PDF** : Un seul document avec les thématiques se suivant sur plusieurs pages.
- **Espace Administrateur** :
    - Gestion de la liste des sections.
    - Modification des libellés des questions.
    - **Gestion des versions** : Toute modification de libellé crée une nouvelle version du formulaire sans altérer les anciennes saisies.

## 🛠️ Installation

### 1. Prérequis
- Python 3.8+
- pip

### 2. Installation (Environnement virtuel)

Sur les versions récentes de Linux (comme Ubuntu 23.04+), Python empêche l'installation globale de paquets pour protéger le système. Il est donc **nécessaire** d'utiliser un environnement virtuel.

**Création et activation de l'environnement virtuel :**

```bash
# Créer l'environnement (nommé 'venv')
python3 -m venv venv

# Activer l'environnement
# Sur Linux / macOS :
source venv/bin/activate

# Sur Windows :
# venv\Scripts\activate
```

*Note : Si vous n'avez pas `venv` installé sur Ubuntu/Debian, faites d'abord : `sudo apt install python3-venv`*

**Installation des dépendances (une fois l'environnement activé) :**

```bash
pip install -r requirements.txt
```

### 3. Initialisation des données
Pour créer la base de données et importer les sections et structures de base depuis les fichiers CSV :
```bash
python ingest_csv.py
```

## 🏃 Lancement

```bash
python app.py
```
L'application sera accessible sur `http://localhost:5000`.

## 🧪 Tests

Pour lancer les tests automatisés :
```bash
pytest test_app.py
```

## 📂 Structure du projet

- `app.py` : Point d'entrée de l'application et définition des routes.
- `models.py` : Modèles de données SQLAlchemy (Sections, Templates, Réponses).
- `exports.py` : Logique de génération des fichiers Excel et PDF.
- `ingest_csv.py` : Script d'initialisation de la base de données.
- `templates/` : Fichiers HTML (Jinja2).
- `modele_csv/` : Contient les fichiers CSV originaux servant de base aux formulaires.
- `exports/` : Dossier local où sont stockés les fichiers générés (exclus du Git).
- `instance/` : Contient la base de données SQLite `database.db` (exclue du Git).

## 🔐 Accès Administrateur

L'accès se fait via le bouton "Admin" en haut à droite (ou via `/admin`).
Le mot de passe est **admin123**.
