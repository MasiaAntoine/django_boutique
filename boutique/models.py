from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Categorie(models.Model):
    """
    Modèle pour les catégories d'articles
    """
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Image")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['ordre', 'nom']

    def __str__(self):
        return self.nom


class Article(models.Model):
    """
    Modèle pour les articles de la boutique
    """
    nom = models.CharField(max_length=200, verbose_name="Nom de l'article")
    description = models.TextField(verbose_name="Description")
    description_courte = models.CharField(max_length=255, blank=True, verbose_name="Description courte")
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Prix")
    prix_promo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Prix promotionnel")
    image = models.ImageField(upload_to='articles/', verbose_name="Image principale")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock disponible")
    actif = models.BooleanField(default=True, verbose_name="Article actif")
    en_vedette = models.BooleanField(default=False, verbose_name="En vedette")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="articles", verbose_name="Catégorie")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-created_at']

    def __str__(self):
        return self.nom

    @property
    def prix_final(self):
        """Retourne le prix final (promotionnel si disponible, sinon prix normal)"""
        return self.prix_promo if self.prix_promo else self.prix

    @property
    def en_promotion(self):
        """Vérifie si l'article est en promotion"""
        return self.prix_promo is not None and self.prix_promo < self.prix

    @property
    def pourcentage_reduction(self):
        """Calcule le pourcentage de réduction si en promotion"""
        if self.en_promotion:
            return int(((self.prix - self.prix_promo) / self.prix) * 100)
        return 0

    @property
    def disponible(self):
        """Vérifie si l'article est disponible"""
        return self.actif and self.stock > 0


class Panier(models.Model):
    """
    Modèle pour le panier d'un utilisateur
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="panier", verbose_name="Utilisateur")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"

    def __str__(self):
        return f"Panier de {self.user.username}"

    @property
    def total_articles(self):
        """Nombre total d'articles dans le panier"""
        return sum(item.quantite for item in self.items.all())

    @property
    def total_prix(self):
        """Prix total du panier"""
        return sum(item.sous_total for item in self.items.all())

    def vider(self):
        """Vide le panier"""
        self.items.all().delete()


class PanierItem(models.Model):
    """
    Modèle pour un article dans le panier
    """
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name="items", verbose_name="Panier")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Article")
    quantite = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Quantité")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")

    class Meta:
        verbose_name = "Article du panier"
        verbose_name_plural = "Articles du panier"
        unique_together = ['panier', 'article']

    def __str__(self):
        return f"{self.quantite} x {self.article.nom}"

    @property
    def sous_total(self):
        """Calcule le sous-total pour cet item"""
        return self.prix_unitaire * self.quantite

    def save(self, *args, **kwargs):
        """Sauvegarde le prix unitaire actuel de l'article"""
        if not self.prix_unitaire:
            self.prix_unitaire = self.article.prix_final
        super().save(*args, **kwargs)


class Commande(models.Model):
    """
    Modèle pour les commandes
    """
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commandes", verbose_name="Client")
    numero_commande = models.CharField(max_length=20, unique=True, verbose_name="Numéro de commande")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente', verbose_name="Statut")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    adresse_livraison = models.TextField(verbose_name="Adresse de livraison")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de commande")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created_at']

    def __str__(self):
        return f"Commande {self.numero_commande} - {self.user.username}"

    def save(self, *args, **kwargs):
        """Génère automatiquement un numéro de commande"""
        if not self.numero_commande:
            import uuid
            self.numero_commande = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)


class CommandeItem(models.Model):
    """
    Modèle pour un article dans une commande
    """
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name="items", verbose_name="Commande")
    article_nom = models.CharField(max_length=200, verbose_name="Nom de l'article")
    article_description = models.TextField(verbose_name="Description de l'article")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    quantite = models.PositiveIntegerField(verbose_name="Quantité")
    sous_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sous-total")

    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"

    def __str__(self):
        return f"{self.quantite} x {self.article_nom}"
