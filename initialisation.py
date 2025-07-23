#!/usr/bin/env python
"""
Script d'initialisation de la base de données
Ce script supprime toutes les données et crée les comptes par défaut
"""

import os
import sys

import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_boutique.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction

from accounts.models import Profile


def clear_database():
    """
    Supprime toutes les données de la base de données
    """
    print("🗑️  Suppression de toutes les données...")

    try:
        with transaction.atomic():
            # Supprimer tous les utilisateurs (cela supprimera aussi les profils grâce à CASCADE)
            User.objects.all().delete()
            print("✅ Toutes les données ont été supprimées avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de la suppression des données : {e}")
        return False

    return True


def create_admin_user():
    """
    Crée le compte administrateur
    """
    print("👑 Création du compte administrateur...")

    try:
        # Créer l'utilisateur admin
        admin = User.objects.create_user(
            username='admin',
            email='admin@boutique.com',
            password='1234@',
            first_name='Admin',
            last_name='Boutique',
            is_staff=True,
            is_superuser=True
        )

        # Mettre à jour le profil pour indiquer que ce n'est pas un client
        admin.profile.is_client = False
        admin.profile.save()

        print(f"✅ Compte administrateur créé : {admin.email}")
        return True

    except Exception as e:
        print(f"❌ Erreur lors de la création du compte admin : {e}")
        return False


def create_client_user():
    """
    Crée le compte client
    """
    print("👤 Création du compte client...")

    try:
        # Créer l'utilisateur client
        client = User.objects.create_user(
            username='client',
            email='client@boutique.com',
            password='1234',
            first_name='Client',
            last_name='Test',
            is_staff=False,
            is_superuser=False
        )

        # Le profil est automatiquement créé avec is_client=True par défaut
        print(f"✅ Compte client créé : {client.email}")
        return True

    except Exception as e:
        print(f"❌ Erreur lors de la création du compte client : {e}")
        return False


def main():
    """
    Fonction principale du script d'initialisation
    """
    print("🚀 Début de l'initialisation de la base de données")
    print("=" * 50)

    # Étape 1 : Supprimer toutes les données
    if not clear_database():
        print("❌ Échec de la suppression des données. Arrêt du script.")
        sys.exit(1)

    print()

    # Étape 2 : Créer le compte administrateur
    if not create_admin_user():
        print("❌ Échec de la création du compte admin. Arrêt du script.")
        sys.exit(1)

    # Étape 3 : Créer le compte client
    if not create_client_user():
        print("❌ Échec de la création du compte client. Arrêt du script.")
        sys.exit(1)

    print()
    print("=" * 50)
    print("🎉 Initialisation terminée avec succès !")
    print()
    print("📋 Comptes créés :")
    print("   👑 Admin:")
    print("      Email    : admin@boutique.com")
    print("      Password : 1234@")
    print("      Type     : Superuser")
    print()
    print("   👤 Client:")
    print("      Email    : client@boutique.com")
    print("      Password : 1234")
    print("      Type     : Client")
    print()
    print("🌐 Vous pouvez maintenant lancer le serveur avec : python manage.py runserver")


if __name__ == '__main__':
    main()
