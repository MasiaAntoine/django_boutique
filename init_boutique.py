#!/usr/bin/env python
"""
Script d'initialisation des données de démonstration pour la boutique
Ajoute des catégories et articles d'exemple
"""

import os
import sys

import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_boutique.settings')
django.setup()

from boutique.models import Article, Categorie


def main():
    print("🚀 Initialisation des données de démonstration...")

    # Création des catégories
    categories_data = [
        {
            'nom': 'Électronique',
            'description': 'Smartphones, ordinateurs, accessoires électroniques',
            'ordre': 1
        },
        {
            'nom': 'Vêtements',
            'description': 'Mode homme, femme et enfant',
            'ordre': 2
        },
        {
            'nom': 'Maison & Jardin',
            'description': 'Décoration, mobilier, jardinage',
            'ordre': 3
        },
        {
            'nom': 'Sports & Loisirs',
            'description': 'Équipements sportifs, jeux, hobbies',
            'ordre': 4
        },
        {
            'nom': 'Livres',
            'description': 'Romans, BD, manuels, magazines',
            'ordre': 5
        }
    ]

    print("📂 Création des catégories...")
    categories = {}
    for cat_data in categories_data:
        categorie, created = Categorie.objects.get_or_create(
            nom=cat_data['nom'],
            defaults=cat_data
        )
        categories[cat_data['nom']] = categorie
        status = "✅ Créée" if created else "⚠️  Existe déjà"
        print(f"  - {cat_data['nom']}: {status}")

    # Création des articles
    articles_data = [
        # Électronique
        {
            'nom': 'iPhone 15 Pro',
            'description': 'Le dernier iPhone avec puce A17 Pro, appareil photo professionnel et écran Super Retina XDR.',
            'description_courte': 'Smartphone Apple dernière génération',
            'prix': 1199.00,
            'prix_promo': 1099.00,
            'stock': 25,
            'categorie': 'Électronique',
            'en_vedette': True
        },
        {
            'nom': 'MacBook Air M3',
            'description': 'Ordinateur portable ultra-fin avec puce M3, 8 Go de RAM et 256 Go de stockage SSD.',
            'description_courte': 'Ordinateur portable Apple M3',
            'prix': 1299.00,
            'stock': 15,
            'categorie': 'Électronique',
            'en_vedette': True
        },
        {
            'nom': 'AirPods Pro 2',
            'description': 'Écouteurs sans fil avec réduction de bruit active et son spatial.',
            'description_courte': 'Écouteurs sans fil Apple',
            'prix': 279.00,
            'prix_promo': 249.00,
            'stock': 50,
            'categorie': 'Électronique'
        },
        {
            'nom': 'Samsung Galaxy S24',
            'description': 'Smartphone Android avec appareil photo 200MP et intelligence artificielle intégrée.',
            'description_courte': 'Smartphone Samsung flagship',
            'prix': 899.00,
            'stock': 30,
            'categorie': 'Électronique'
        },

        # Vêtements
        {
            'nom': 'Jean Levi\'s 501',
            'description': 'Le jean iconique Levi\'s coupe droite, 100% coton denim.',
            'description_courte': 'Jean classique Levi\'s',
            'prix': 89.00,
            'prix_promo': 69.00,
            'stock': 40,
            'categorie': 'Vêtements',
            'en_vedette': True
        },
        {
            'nom': 'T-shirt Nike Dri-FIT',
            'description': 'T-shirt de sport respirant avec technologie Dri-FIT pour évacuer la transpiration.',
            'description_courte': 'T-shirt de sport Nike',
            'prix': 35.00,
            'stock': 60,
            'categorie': 'Vêtements'
        },
        {
            'nom': 'Sneakers Adidas Stan Smith',
            'description': 'Baskets en cuir blanc iconiques avec accents verts.',
            'description_courte': 'Baskets Adidas classiques',
            'prix': 79.00,
            'stock': 35,
            'categorie': 'Vêtements'
        },

        # Maison & Jardin
        {
            'nom': 'Canapé 3 places',
            'description': 'Canapé confortable en tissu gris avec coussins amovibles.',
            'description_courte': 'Canapé 3 places moderne',
            'prix': 699.00,
            'prix_promo': 599.00,
            'stock': 8,
            'categorie': 'Maison & Jardin'
        },
        {
            'nom': 'Plante verte Monstera',
            'description': 'Plante d\'intérieur décorative, facile d\'entretien, pot inclus.',
            'description_courte': 'Plante d\'intérieur Monstera',
            'prix': 29.00,
            'stock': 20,
            'categorie': 'Maison & Jardin',
            'en_vedette': True
        },
        {
            'nom': 'Lampe de bureau LED',
            'description': 'Lampe de bureau réglable avec éclairage LED et port USB.',
            'description_courte': 'Lampe LED avec USB',
            'prix': 45.00,
            'stock': 25,
            'categorie': 'Maison & Jardin'
        },

        # Sports & Loisirs
        {
            'nom': 'Vélo VTT 27.5"',
            'description': 'VTT tout-terrain avec 21 vitesses et freins à disque.',
            'description_courte': 'VTT 21 vitesses',
            'prix': 399.00,
            'prix_promo': 349.00,
            'stock': 12,
            'categorie': 'Sports & Loisirs'
        },
        {
            'nom': 'Tapis de yoga',
            'description': 'Tapis antidérapant en TPE écologique, épaisseur 6mm.',
            'description_courte': 'Tapis de yoga antidérapant',
            'prix': 25.00,
            'stock': 45,
            'categorie': 'Sports & Loisirs',
            'en_vedette': True
        },

        # Livres
        {
            'nom': 'Le Petit Prince',
            'description': 'Roman classique d\'Antoine de Saint-Exupéry, édition illustrée.',
            'description_courte': 'Roman classique illustré',
            'prix': 12.00,
            'stock': 30,
            'categorie': 'Livres'
        },
        {
            'nom': 'Apprendre Python',
            'description': 'Guide complet pour apprendre la programmation Python, 500 pages.',
            'description_courte': 'Manuel de programmation Python',
            'prix': 39.00,
            'prix_promo': 29.00,
            'stock': 20,
            'categorie': 'Livres',
            'en_vedette': True
        }
    ]

    print("📦 Création des articles...")
    for article_data in articles_data:
        categorie_nom = article_data.pop('categorie')
        categorie = categories[categorie_nom]

        article_data['categorie'] = categorie

        article, created = Article.objects.get_or_create(
            nom=article_data['nom'],
            defaults=article_data
        )
        status = "✅ Créé" if created else "⚠️  Existe déjà"
        print(f"  - {article_data['nom']}: {status}")

    print(f"\n🎉 Initialisation terminée !")
    print(f"📊 Résumé :")
    print(f"  - Catégories : {Categorie.objects.count()}")
    print(f"  - Articles : {Article.objects.count()}")
    print(f"  - Articles en vedette : {Article.objects.filter(en_vedette=True).count()}")
    print(f"  - Articles en promotion : {Article.objects.filter(prix_promo__isnull=False).count()}")

    print(f"\n🔗 Accédez à votre boutique : http://127.0.0.1:8000/")
    print(f"🔧 Administration Django : http://127.0.0.1:8000/admin/")


if __name__ == '__main__':
    main()
