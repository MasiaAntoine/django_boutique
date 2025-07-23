from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden


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
    context = {
        'user': request.user,
        'title': 'Dashboard Administration',
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required  
def access_denied_view(request):
    """
    Vue d'accès refusé pour les utilisateurs non autorisés
    """
    return render(request, 'dashboard/access_denied.html', status=403)
