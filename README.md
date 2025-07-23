# Boutique en ligne Django 🛒

Une application de boutique en ligne développée avec Django permettant la gestion des utilisateurs, l'authentification et la différenciation entre clients et super utilisateurs.

## 🚀 Fonctionnalités actuelles

### Authentification

- ✅ **Inscription des utilisateurs** avec formulaire personnalisé
- ✅ **Connexion/Déconnexion** avec redirection automatique selon le type d'utilisateur
- ✅ **Gestion des profils utilisateur** avec informations complémentaires
- ✅ **Différenciation Client/Super User** avec redirections appropriées

### Interface utilisateur

- ✅ **Page d'accueil responsive** avec Bootstrap 5
- ✅ **Navigation adaptive** selon le statut de connexion
- ✅ **Dashboard pour super users** avec vue d'ensemble
- ✅ **Messages de bienvenue personnalisés** selon le type d'utilisateur

### Administration

- ✅ **Interface Django Admin personnalisée** pour la gestion des profils
- ✅ **Gestion des utilisateurs** avec informations de profil intégrées

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
# Option 1 : Script standalone
python initialisation.py

# Option 2 : Commande Django (recommandée)
python manage.py init_db
```

Cela crée automatiquement :
- **Admin** : admin@boutique.com / 1234@
- **Client** : client@boutique.com / 1234

6. **Lancer le serveur de développement**

```bash
python manage.py runserver
```

7. **Accéder à l'application**

- Site web : http://127.0.0.1:8000/
- Administration : http://127.0.0.1:8000/admin/

## 📱 Utilisation

### Pour tester l'authentification

**Avec les comptes créés par le script d'initialisation :**

1. **Tester le compte admin :**
   - Se connecter avec admin@boutique.com / 1234@
   - → Redirection vers le dashboard

2. **Tester le compte client :**
   - Se connecter avec client@boutique.com / 1234
   - → Redirection vers l'accueil

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
