from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Profile


class CustomLoginView(LoginView):
    """
    Vue de connexion personnalisée qui redirige selon le type d'utilisateur
    """
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        """
        Redirection après connexion selon le type d'utilisateur
        """
        user = self.request.user
        if user.is_superuser:
            return '/dashboard/'
        else:
            return '/'


class SignUpView(CreateView):
    """
    Vue d'inscription utilisant une classe générique
    """
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        """
        Traitement après validation du formulaire d'inscription
        """
        response = super().form_valid(form)
        messages.success(self.request, 'Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.')
        return response


def home_redirect(request):
    """
    Vue de redirection après connexion
    Affiche un message différent selon le type d'utilisateur
    """
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    context = {
        'user': request.user,
        'is_superuser': request.user.is_superuser,
    }
    
    if request.user.is_superuser:
        return render(request, 'dashboard/dashboard.html', context)
    else:
        return render(request, 'boutique/home.html', context)


@login_required
def profile_view(request):
    """
    Vue pour afficher et modifier le profil utilisateur
    """
    profile = request.user.profile
    
    context = {
        'profile': profile,
        'user': request.user,
    }
    
    return render(request, 'accounts/profile.html', context)
