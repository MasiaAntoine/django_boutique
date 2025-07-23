from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import (Article, Categorie, Commande, CommandeItem, Panier,
                     PanierItem)


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'actif', 'ordre', 'nombre_articles', 'image_preview', 'created_at']
    list_filter = ['actif', 'created_at']
    search_fields = ['nom', 'description']
    list_editable = ['actif', 'ordre']
    prepopulated_fields = {}
    ordering = ['ordre', 'nom']

    def nombre_articles(self, obj):
        return obj.articles.count()
    nombre_articles.short_description = "Nb articles"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />', obj.image.url)
        return "Pas d'image"
    image_preview.short_description = "Image"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'categorie', 'prix', 'prix_promo', 'stock', 'actif', 'en_vedette', 'image_preview', 'created_at']
    list_filter = ['actif', 'en_vedette', 'categorie', 'created_at']
    search_fields = ['nom', 'description', 'description_courte']
    list_editable = ['prix', 'prix_promo', 'stock', 'actif', 'en_vedette']
    fieldsets = [
        ('Informations générales', {
            'fields': ('nom', 'categorie', 'description_courte', 'description', 'image')
        }),
        ('Prix et stock', {
            'fields': ('prix', 'prix_promo', 'stock')
        }),
        ('Options', {
            'fields': ('actif', 'en_vedette')
        }),
    ]
    ordering = ['-created_at']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />', obj.image.url)
        return "Pas d'image"
    image_preview.short_description = "Image"


class PanierItemInline(admin.TabularInline):
    model = PanierItem
    extra = 0
    readonly_fields = ['prix_unitaire', 'sous_total']


@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_articles', 'total_prix', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['total_articles', 'total_prix']
    inlines = [PanierItemInline]

    def has_add_permission(self, request):
        return False


class CommandeItemInline(admin.TabularInline):
    model = CommandeItem
    extra = 0
    readonly_fields = ['article_nom', 'article_description', 'prix_unitaire', 'quantite', 'sous_total']


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['numero_commande', 'user', 'statut', 'total', 'created_at']
    list_filter = ['statut', 'created_at']
    search_fields = ['numero_commande', 'user__username', 'user__email']
    readonly_fields = ['numero_commande', 'total', 'created_at']
    fieldsets = [
        ('Informations commande', {
            'fields': ('numero_commande', 'user', 'statut', 'total', 'created_at')
        }),
        ('Livraison', {
            'fields': ('adresse_livraison', 'telephone')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    ]
    inlines = [CommandeItemInline]
    ordering = ['-created_at']
    actions = ['export_commandes_csv']

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'export-csv/',
                self.admin_site.admin_view(self.export_csv_view),
                name='boutique_commande_export_csv',
            ),
            path(
                'import-csv/',
                self.admin_site.admin_view(self.import_csv_view),
                name='boutique_commande_import_csv',
            ),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({
            'export_csv_url': reverse('admin:boutique_commande_export_csv'),
            'import_csv_url': reverse('admin:boutique_commande_import_csv'),
        })
        return super().changelist_view(request, extra_context=extra_context)

    def export_csv_view(self, request):
        """Redirige vers l'API d'export CSV"""
        from django.urls import reverse
        api_url = reverse('boutique_api:export_commandes_csv')
        return HttpResponseRedirect(api_url)

    def import_csv_view(self, request):
        """Vue pour afficher le formulaire d'import CSV"""
        if request.method == 'POST' and request.FILES.get('csv_file'):
            # Rediriger vers l'API d'import ou le dashboard pour l'import
            try:
                messages.success(request, "Utilisez le dashboard ou l'API directement pour l'import CSV.")
            except Exception as e:
                messages.error(request, f"Erreur lors de l'import: {e}")

            return HttpResponseRedirect(reverse('admin:boutique_commande_changelist'))

        # Afficher le formulaire d'import
        from django.shortcuts import render
        return render(request, 'admin/boutique/commande/import_csv.html')

    def export_commandes_csv(self, request, queryset):
        """Action pour exporter les commandes sélectionnées en CSV"""
        from django.urls import reverse
        api_url = reverse('boutique_api:export_commandes_csv')
        return HttpResponseRedirect(api_url)

    export_commandes_csv.short_description = "Exporter les commandes en CSV"
