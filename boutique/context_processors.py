"""
Context processors pour la boutique
Permet d'ajouter des données dans le contexte de tous les templates
"""

from .models import Panier


def panier_context(request):
    """
    Ajoute le nombre d'articles dans le panier pour tous les templates
    """
    panier_total = 0

    if request.user.is_authenticated and not request.user.is_superuser:
        try:
            panier = Panier.objects.get(user=request.user)
            panier_total = panier.total_articles
        except Panier.DoesNotExist:
            panier_total = 0

    return {
        'panier_total': panier_total
    }
