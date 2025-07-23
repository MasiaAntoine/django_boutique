from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomAuthenticationForm, CustomUserCreationForm
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

    if request.method == 'POST':
        action = request.POST.get('action', 'update_profile')

        if action == 'change_password':
            # Gestion du changement de mot de passe
            current_password = request.POST.get('current_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            # Vérifications
            if not request.user.check_password(current_password):
                messages.error(request, 'Le mot de passe actuel est incorrect.')
            elif new_password1 != new_password2:
                messages.error(request, 'Les nouveaux mots de passe ne correspondent pas.')
            elif len(new_password1) < 8:
                messages.error(request, 'Le nouveau mot de passe doit contenir au moins 8 caractères.')
            else:
                # Changer le mot de passe
                request.user.set_password(new_password1)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Maintient la session
                messages.success(request, 'Votre mot de passe a été modifié avec succès.')

        else:
            # Gestion de la modification du profil
            try:
                # Mise à jour des informations utilisateur
                request.user.username = request.POST.get('username', request.user.username)
                request.user.email = request.POST.get('email', request.user.email)
                request.user.first_name = request.POST.get('first_name', '')
                request.user.last_name = request.POST.get('last_name', '')
                request.user.full_clean()  # Validation
                request.user.save()

                # Mise à jour du profil
                profile.phone = request.POST.get('phone', '')
                profile.address = request.POST.get('address', '')
                birth_date = request.POST.get('birth_date')
                if birth_date:
                    profile.birth_date = birth_date
                else:
                    profile.birth_date = None

                profile.save()
                messages.success(request, 'Votre profil a été mis à jour avec succès.')

            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
            except Exception as e:
                messages.error(request, 'Une erreur est survenue lors de la mise à jour.')

    # Calculer les statistiques pour les clients
    total_depense = 0
    if not request.user.is_superuser:
        total_depense = request.user.commandes.aggregate(total=Sum('total'))['total'] or 0

    context = {
        'profile': profile,
        'user': request.user,
        'total_depense': total_depense,
    }

    return render(request, 'accounts/profile.html', context)
