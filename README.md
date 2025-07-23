# Boutique en ligne Django 🛒

Une application de boutique en ligne complète développée avec Django, permettant la gestion des utilisateurs, l'authentification, la gestion des produits et les commandes.

## 🚀 Fonctionnalités implémentées

### Authentification

- ✅ **Inscription des utilisateurs** avec formulaire personnalisé
- ✅ **Connexion/Déconnexion** avec redirection automatique selon le type d'utilisateur
- ✅ **Gestion des profils utilisateur** avec informations complémentaires
- ✅ **Différenciation Client/Super User** avec redirections appropriées

### Boutique & Catalogue

- ✅ **Page d'accueil avec listing des articles** paginé et filtrable
- ✅ **Filtrage par catégorie** avec barre de recherche
- ✅ **Page détaillée de chaque article** avec images et descriptions
- ✅ **Articles en vedette** mis en avant sur la page d'accueil
- ✅ **Système de promotions** avec prix réduits et pourcentages de remise
- ✅ **Gestion du stock** avec affichage de disponibilité

### Panier & Commandes

- ✅ **Panier d'achat persistant** pour chaque utilisateur
- ✅ **Ajout/Modification/Suppression d'articles** du panier
- ✅ **Gestion des quantités** avec vérification du stock
- ✅ **Processus de commande simplifié** (paiement fictif)
- ✅ **Historique des commandes** avec statuts de suivi
- ✅ **Page compte client** avec informations personnelles

### Administration

- ✅ **Interface Django Admin personnalisée** pour la gestion des produits
- ✅ **Gestion des catégories et articles** avec images
- ✅ **Suivi des commandes** et modification des statuts
- ✅ **Dashboard pour super users** avec vue d'ensemble

### Interface utilisateur

- ✅ **Design responsive** avec Bootstrap 5
- ✅ **Navigation adaptive** selon le statut de connexion
- ✅ **Compteur de panier** dans la navigation
- ✅ **Messages de confirmation** et d'erreur
- ✅ **Pagination** pour tous les listings

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

## 📱 Utilisation

### Navigation et découverte

- **Page d'accueil** : Affichage des articles avec filtrage par catégorie et recherche
- **Catégories** : Électronique, Vêtements, Maison & Jardin, Sports & Loisirs, Livres
- **Articles en vedette** : Mis en avant automatiquement sur la page d'accueil
- **Recherche** : Barre de recherche dans le nom et description des articles

### Pour les clients connectés

1. **Parcourir le catalogue :**
   - Filtrer par catégorie
   - Rechercher des articles
   - Voir les détails des produits

2. **Gérer son panier :**
   - Ajouter des articles (vérification du stock)
   - Modifier les quantités
   - Supprimer des articles

3. **Passer commande :**
   - Finaliser le panier
   - Paiement fictif (un clic)
   - Suivi de commande

4. **Gérer son compte :**
   - Voir l'historique des commandes
   - Modifier ses informations personnelles
   - Suivre le statut des livraisons

### Pour tester l'authentification

**Avec les comptes créés par le script d'initialisation :**

1. **Tester le compte admin :**
   - Se connecter avec admin@boutique.com / 1234@
   - → Redirection vers le dashboard
   - → Accès à l'administration Django

2. **Tester le compte client :**
   - Se connecter avec client@boutique.com / 1234
   - → Accès complet à la boutique
   - → Possibilité d'acheter et de gérer le panier

### Administration (Super Users)

- **Gestion des catégories** : Création, modification, upload d'images
- **Gestion des articles** : Ajout de produits, gestion du stock, prix promotionnels
- **Suivi des commandes** : Changement de statut, détails des commandes
- **Dashboard** : Vue d'ensemble des ventes et commandes

## 🎯 Modèles de données

### Articles et Catégories
- **Categorie** : nom, description, image, ordre d'affichage
- **Article** : nom, description, prix, prix promotionnel, image, stock, catégorie

### Panier et Commandes
- **Panier** : associé à un utilisateur, calculs automatiques
- **PanierItem** : articles dans le panier avec quantités
- **Commande** : commandes finalisées avec numéro unique
- **CommandeItem** : snapshot des articles commandés

### Fonctionnalités avancées
- **Gestion du stock** : vérification automatique lors des ajouts au panier
- **Prix promotionnels** : calcul automatique des pourcentages de remise
- **Images** : upload et affichage des images de produits et catégories
- **Pagination** : navigation optimisée pour les grands catalogues

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
