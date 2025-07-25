from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    """
    Inline admin pour afficher le profil dans l'admin des utilisateurs
    """
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profil'
    fields = ('is_client', 'phone', 'address', 'birth_date')


class CustomUserAdmin(UserAdmin):
    """
    Admin personnalisé pour les utilisateurs avec leur profil
    """
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_user_type')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__is_client')

    def get_user_type(self, obj):
        """Affiche le type d'utilisateur"""
        if obj.is_superuser:
            return "Super User"
        return "Client" if hasattr(obj, 'profile') and obj.profile.is_client else "Client"
    get_user_type.short_description = 'Type utilisateur'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin pour les profils utilisateur
    """
    list_display = ('user', 'get_full_name', 'is_client', 'phone', 'created_at')
    list_filter = ('is_client', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Type de compte', {
            'fields': ('is_client',)
        }),
        ('Informations personnelles', {
            'fields': ('phone', 'address', 'birth_date')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_full_name(self, obj):
        """Affiche le nom complet"""
        return obj.full_name or "Non renseigné"
    get_full_name.short_description = 'Nom complet'


# Réenregistrer UserAdmin avec notre classe personnalisée
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
