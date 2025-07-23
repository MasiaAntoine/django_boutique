from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal pour créer automatiquement un profil lors de la création d'un utilisateur
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal pour sauvegarder le profil lors de la sauvegarde d'un utilisateur
    """
    instance.profile.save()
