from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import date, timedelta
from boutique.models import Commande, CommandeItem, Article
from django.contrib.auth.models import User


def is_superuser(user):
    """
    Fonction pour vérifier si l'utilisateur est un superuser
    """
    return user.is_superuser


@login_required
@user_passes_test(is_superuser)
def dashboard_view(request):
    """
    Vue du dashboard pour les super_users
    Affiche les informations de gestion de la boutique
    """
    # Date du jour
    today = timezone.now().date()
    
    # Commandes validées (confirmées, expédiées, livrées)
    commandes_validees = Commande.objects.filter(
        statut__in=['confirmee', 'expediee', 'livree']
    ).select_related('user').prefetch_related('items')
    
    # Statistiques du jour
    commandes_jour = commandes_validees.filter(created_at__date=today)
    ca_jour = commandes_jour.aggregate(total=Sum('total'))['total'] or 0
    
    # Statistiques globales
    total_commandes = commandes_validees.count()
    ca_total = commandes_validees.aggregate(total=Sum('total'))['total'] or 0
    total_produits = Article.objects.filter(actif=True).count()
    total_clients = User.objects.filter(commandes__isnull=False).distinct().count()
    
    # Commandes récentes (10 dernières)
    commandes_recentes = commandes_validees.order_by('-created_at')[:10]
    
    context = {
        'user': request.user,
        'title': 'Dashboard Administration',
        'commandes_jour_count': commandes_jour.count(),
        'ca_jour': ca_jour,
        'total_produits': total_produits,
        'total_clients': total_clients,
        'commandes_validees': commandes_validees,
        'commandes_recentes': commandes_recentes,
        'ca_total': ca_total,
        'total_commandes': total_commandes,
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required  
def access_denied_view(request):
    """
    Vue d'accès refusé pour les utilisateurs non autorisés
    """
    return render(request, 'dashboard/access_denied.html', status=403)
