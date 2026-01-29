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

Il est fortement recommandé d'utiliser un environnement virtuel pour installer les dépendances de l'application. Cela permet d'isoler le projet et d'éviter les erreurs de type "externally-managed-environment" sur les systèmes Linux récents (Ubuntu 23.04+).

**Étape 1 : Créer l'environnement virtuel**
Ouvrez un terminal dans le dossier du projet et exécutez :
```bash
python3 -m venv venv
```
*(Si vous avez une erreur indiquant que venv n'est pas installé sur Ubuntu/Debian, lancez : `sudo apt install python3-venv`)*

**Étape 2 : Activer l'environnement virtuel**
- **Sur Linux / macOS :**
  ```bash
  source venv/bin/activate
  ```
- **Sur Windows :**
  ```bash
  venv\Scripts\activate
  ```

**Étape 3 : Installer les dépendances**
Une fois l'environnement activé (le nom `(venv)` doit apparaître au début de votre ligne de commande), installez les bibliothèques nécessaires :
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
