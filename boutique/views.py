from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home_view(request):
    """
    Vue de la page d'accueil pour les clients
    Affiche un message de bienvenue différent selon le statut de connexion
    """
    context = {
        'title': 'Boutique en ligne - Accueil',
    }
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # Rediriger les super_users vers le dashboard
            from django.shortcuts import redirect
            return redirect('dashboard:dashboard')
        else:
            context['welcome_message'] = f'Bienvenue {request.user.first_name or request.user.username} ! Vous êtes connecté en tant que client.'
    else:
        context['welcome_message'] = 'Bienvenue sur notre boutique en ligne ! Connectez-vous pour accéder à toutes nos fonctionnalités.'
    
    return render(request, 'boutique/home.html', context)
