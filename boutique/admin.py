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
        """Vue pour traiter l'import CSV"""
        if request.method == 'POST' and request.FILES.get('csv_file'):
            # Traiter le fichier en utilisant la même logique que l'API
            try:
                import csv
                import io

                from django.contrib.auth.models import User
                from django.core.exceptions import ValidationError

                csv_file = request.FILES['csv_file']

                if not csv_file.name.endswith('.csv'):
                    messages.error(request, "Le fichier doit être au format CSV")
                    return HttpResponseRedirect(reverse('admin:boutique_commande_changelist'))

                # Lire le fichier CSV
                decoded_file = csv_file.read().decode('utf-8-sig')  # Support du BOM UTF-8
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string, delimiter=';')

                imported_count = 0
                errors = []

                for row_num, row in enumerate(reader, start=2):  # Start=2 car ligne 1 = headers
                    try:
                        # Validation des champs requis
                        required_fields = ['Numero_Commande', 'Client_Username', 'Total_Commande']
                        for field in required_fields:
                            if not row.get(field):
                                raise ValidationError(f'Champ requis manquant: {field}')

                        # Vérifier si la commande existe déjà
                        if Commande.objects.filter(numero_commande=row['Numero_Commande']).exists():
                            errors.append(f"Ligne {row_num}: Commande {row['Numero_Commande']} déjà existante")
                            continue

                        # Récupérer l'utilisateur
                        try:
                            user = User.objects.get(username=row['Client_Username'])
                        except User.DoesNotExist:
                            errors.append(f"Ligne {row_num}: Utilisateur {row['Client_Username']} introuvable")
                            continue

                        # Convertir le total (format français vers décimal)
                        total_str = row['Total_Commande'].replace(',', '.')
                        total = float(total_str)

                        # Fonction pour convertir le statut
                        def get_status_from_display(display_name):
                            status_mapping = {
                                'En attente': 'en_attente',
                                'Confirmée': 'confirmee',
                                'Expédiée': 'expediee',
                                'Livrée': 'livree',
                                'Annulée': 'annulee',
                            }
                            return status_mapping.get(display_name, 'en_attente')

                        # Créer la commande
                        commande = Commande.objects.create(
                            numero_commande=row['Numero_Commande'],
                            user=user,
                            statut=get_status_from_display(row.get('Statut', 'En attente')),
                            total=total,
                            adresse_livraison=row.get('Adresse_Livraison', ''),
                            telephone=row.get('Telephone', ''),
                            notes=row.get('Notes', '')
                        )

                        imported_count += 1

                    except Exception as e:
                        errors.append(f"Ligne {row_num}: {str(e)}")

                # Messages de résultat
                if imported_count > 0:
                    messages.success(request, f"{imported_count} commande(s) importée(s) avec succès")

                if errors:
                    for error in errors[:5]:  # Limiter à 5 erreurs pour l'affichage
                        messages.warning(request, error)
                    if len(errors) > 5:
                        messages.warning(request, f"... et {len(errors)-5} autres erreurs")

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
