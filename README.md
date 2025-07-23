# Boutique en ligne Django 🛒

Une application de boutique en ligne complète développée avec Django, permettant la gestion des utilisateurs, l'authentification, la gestion des produits et les commandes.

## 🛠️ Installation et lancement

### Prérequis

- Python 3.8+
- pip

### Installation

1. **Cloner le repository**

```bash
git clone https://github.com/MasiaAntoine/django_boutique.git
cd django_boutique
```

2. **Créer un environnement virtuel**

```bash
python -m venv .venv
source .venv/bin/activate  # Sur macOS/Linux
# ou
.venv\\Scripts\\activate  # Sur Windows
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

4. **Appliquer les migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Initialiser la base de données avec les comptes par défaut** (optionnel)

```bash
# Option 1 : Script standalone pour les comptes utilisateurs
python initialisation.py

# Option 2 : Commande Django (recommandée)
python manage.py init_db
```

Cela crée automatiquement :
- **Admin** : admin@boutique.com / 1234@
- **Client** : client@boutique.com / 1234

6. **Initialiser les données de démonstration** (optionnel mais recommandé)

```bash
# Option 1 : Script Python standalone
python init_boutique.py

# Option 2 : Commande Django (recommandée)
python manage.py init_boutique

# Commande Django sans confirmation interactive
python manage.py init_boutique --confirm
```

Cela ajoute :
- **5 catégories** : Électronique, Vêtements, Maison & Jardin, Sports & Loisirs, Livres
- **14 articles** avec descriptions, prix, stock et promotions
- **Articles en vedette** pour la page d'accueil

7. **Lancer le serveur de développement**

```bash
python manage.py runserver
```

7. **Accéder à l'application**

- Site web : http://127.0.0.1:8000/
- Administration : http://127.0.0.1:8000/admin/

## 👨‍💻 Auteur

Projet développé dans le cadre du cours Python - Boutique en ligne.

### Utilisation

```bash
# Option 1 : Script Python standalone
python initialisation.py

# Option 2 : Commande Django (recommandée)
python manage.py init_db

# Commande Django sans confirmation interactive
python manage.py init_db --confirm
```

### Comptes créés automatiquement

- **👑 Administrateur**
  - Email : admin@boutique.com
  - Mot de passe : 1234@
  - Type : Superuser (accès admin + dashboard)

- **👤 Client de test**
  - Email : client@boutique.com
  - Mot de passe : 1234
  - Type : Client normal

⚠️ **Attention** : Ce script supprime TOUTES les données existantes avant de créer les nouveaux comptes.
