import csv
import io
from datetime import date
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from boutique.models import Commande, CommandeItem
import json


def is_superuser(user):
    """Vérifie si l'utilisateur est un superuser"""
    return user.is_superuser


@login_required
@user_passes_test(is_superuser)
@require_http_methods(["GET"])
def export_commandes_csv(request):
    """
    API endpoint pour exporter les commandes du jour en CSV
    """
    try:
        # Date du jour (peut être personnalisée via paramètre GET)
        date_param = request.GET.get('date')
        if date_param:
            try:
                target_date = timezone.datetime.strptime(date_param, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({
                    'error': 'Format de date invalide. Utilisez YYYY-MM-DD'
                }, status=400)
        else:
            target_date = timezone.now().date()
        
        # Récupérer les commandes du jour
        commandes = Commande.objects.filter(
            created_at__date=target_date
        ).select_related('user').prefetch_related('items')
        
        # Créer la réponse CSV
        response = HttpResponse(
            content_type='text/csv; charset=utf-8',
            headers={
                'Content-Disposition': f'attachment; filename="commandes_{target_date.strftime("%Y%m%d")}.csv"'
            }
        )
        
        # Ajouter le BOM UTF-8 pour Excel
        response.write('\ufeff')
        
        writer = csv.writer(response, delimiter=';')
        
        # En-têtes CSV
        headers = [
            'Numero_Commande',
            'Date_Commande',
            'Client_Username',
            'Client_Email',
            'Client_Nom',
            'Client_Prenom',
            'Statut',
            'Total_Commande',
            'Adresse_Livraison',
            'Telephone',
            'Notes',
            'Nombre_Articles',
            'Articles_Details'
        ]
        writer.writerow(headers)
        
        # Données des commandes
        for commande in commandes:
            # Détails des articles
            articles_details = []
            for item in commande.items.all():
                articles_details.append(
                    f"{item.article_nom} (Qté: {item.quantite}, Prix: {item.prix_unitaire}€, Sous-total: {item.sous_total}€)"
                )
            
            row = [
                commande.numero_commande,
                commande.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                commande.user.username,
                commande.user.email or '',
                commande.user.last_name or '',
                commande.user.first_name or '',
                commande.get_statut_display(),
                str(commande.total).replace('.', ','),  # Format français pour Excel
                commande.adresse_livraison.replace('\n', ' ').replace('\r', ' '),
                commande.telephone,
                commande.notes.replace('\n', ' ').replace('\r', ' ') if commande.notes else '',
                commande.items.count(),
                ' | '.join(articles_details)
            ]
            writer.writerow(row)
        
        return response
        
    except Exception as e:
        return JsonResponse({
            'error': f'Erreur lors de l\'export: {str(e)}'
        }, status=500)


@login_required
@user_passes_test(is_superuser)
@csrf_exempt
@require_http_methods(["POST"])
def import_commandes_csv(request):
    """
    API endpoint pour importer des commandes depuis un fichier CSV
    """
    try:
        if 'csv_file' not in request.FILES:
            return JsonResponse({
                'error': 'Aucun fichier CSV fourni'
            }, status=400)
        
        csv_file = request.FILES['csv_file']
        
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({
                'error': 'Le fichier doit être au format CSV'
            }, status=400)
        
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
                
                # Récupérer ou créer l'utilisateur
                try:
                    from django.contrib.auth.models import User
                    user = User.objects.get(username=row['Client_Username'])
                except User.DoesNotExist:
                    errors.append(f"Ligne {row_num}: Utilisateur {row['Client_Username']} introuvable")
                    continue
                
                # Convertir le total (format français vers décimal)
                total_str = row['Total_Commande'].replace(',', '.')
                total = float(total_str)
                
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
        
        return JsonResponse({
            'success': True,
            'imported_count': imported_count,
            'errors': errors
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Erreur lors de l\'import: {str(e)}'
        }, status=500)


def get_status_from_display(display_name):
    """
    Convertit un nom d'affichage de statut vers la valeur de base de données
    """
    status_mapping = {
        'En attente': 'en_attente',
        'Confirmée': 'confirmee',
        'Expédiée': 'expediee',
        'Livrée': 'livree',
        'Annulée': 'annulee',
    }
    return status_mapping.get(display_name, 'en_attente')


@login_required
@user_passes_test(is_superuser)
@require_http_methods(["GET"])
def api_status(request):
    """
    Endpoint pour vérifier le statut de l'API
    """
    today = timezone.now().date()
    commandes_count = Commande.objects.filter(created_at__date=today).count()
    
    return JsonResponse({
        'status': 'OK',
        'date': today.isoformat(),
        'commandes_today': commandes_count,
        'endpoints': {
            'export_csv': '/api/commandes/export/csv/',
            'import_csv': '/api/commandes/import/csv/',
        }
    })
