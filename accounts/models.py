from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Profil utilisateur pour étendre le modèle User de Django
    Permet de différencier les clients des super_users
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_client = models.BooleanField(default=True, verbose_name="Est un client")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    address = models.TextField(blank=True, verbose_name="Adresse")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"

    def __str__(self):
        user_type = "Client" if self.is_client else "Super User"
        return f"{self.user.username} - {user_type}"

    @property
    def full_name(self):
        """Retourne le nom complet de l'utilisateur"""
        return f"{self.user.first_name} {self.user.last_name}".strip()



